# Scientific Source Pipeline — reference

Detalhamento da Fase 4.5. Leia este arquivo quando:
- O pipeline cientifico foi acionado e voce precisa entender roteamento por tipo
- Uma classificacao deu errado e voce precisa debugar
- Esta planejando estender o pipeline (novos publishers, novos metodos de fetch)

## Por que existe

A execucao real de 2026-04-22 (farmacologia) teve:

| Tipo | Tentadas | Sucesso URL direto | Sucesso apos pipeline |
|---|---|---|---|
| PubMed (PMID) | 21 | 0% (CAPTCHA) | 100% (E-utilities efetch) |
| PMC (PMCID) | 18 | 0% (CAPTCHA) | 89% (HTML fetch + strip) |
| MDPI / Karger / Liebert | 3 | 0% (Cloudflare) | 0% (bloqueio persistente → manual bucket) |
| NEJM | 7 | 100% | — |
| ClinicalTrials.gov | 1 | 100% | — |
| Blog (Peter Attia) | 3 | 33% | 100% |
| GovSites (FDA/WHO) | 10 | 80% | — |
| **Total** | **86** | **~40%** | **~95%** |

O pipeline transforma uma experiencia frustrante (60% de falha silenciosa no scraper) em um fluxo previsivel com buckets claros.

## Ciclo de vida de uma URL (v1 — serial, sem cache)

```
URL input
  │
  ▼
classify_url.py ──► type: pubmed | pmc | doi | cloudflare_known | gov_or_guideline | blog_or_news | generic_web
  │
  ├─► pubmed: pubmed_abstract.py  ──┐
  │       + pmid_to_pmc.py           │
  │       + pmc_fulltext.py (se OK) ─┤
  │                                   │
  ├─► pmc: pmc_fulltext.py ───────────┤
  │                                   │
  ├─► doi: unpaywall_resolver.py ─────┤ (OA encontrado → open_access_pdf.py)
  │                                   │
  ├─► gov/blog/generic: URL direta ────┘
  │
  ▼
cleanup_captcha_sources.py (1x por notebook, antes dos uploads)
  │
  ▼
notebooklm source add <file|url>
  │
  ▼
notebook_manifest.record_source(...)
  │
  ▼
bucket: auto_uploaded | manual_required | paywall_unavailable
```

## Ciclo de vida de uma URL (v2/v3 — paralelo, com cache + scorer)

v2 reorganiza o fluxo em quatro estagios: Classify → Fetch (paralelo com cache) → Score (paralelo, best-effort) → Upload (serial). `upload_to_nblm.py` orquestra tudo. Ver `references/cache-and-rate-limits.md` e `references/academic-scoring.md` para detalhes de cada camada.

```
URL input
  │
  ▼
classify_url.py ──► type + bucket (ncbi | academic | generic)
  │
  ▼
particionar em 3 filas de trabalho:
  - ncbi_tasks:     pubmed, pmc
  - academic_tasks: doi
  - generic_tasks:  gov_or_guideline, blog_or_news, generic_web, cloudflare_known
  │
  ▼
3 ThreadPoolExecutor paralelos (v2 F9):
  ┌─── ncbi_pool (max 3) ────────────────────────────────────────┐
  │   worker:                                                    │
  │     cache_get("pmid", pmid, TTL=365d) ──► hit? return early  │
  │     bucket("ncbi").acquire()                                 │
  │     pubmed_abstract.py + pmid_to_pmc + pmc_fulltext          │
  │     cache_put(...)                                           │
  │     upload_queue.put(UploadTask)                             │
  └──────────────────────────────────────────────────────────────┘
  ┌─── academic_pool (max 3) ────────────────────────────────────┐
  │   worker:                                                    │
  │     _handle_doi():                                           │
  │       cache_get("doi", safe_doi, TTL=30d)                    │
  │       bucket("unpaywall").acquire()                          │
  │       unpaywall_resolver.resolve()                           │
  │         ├─ is_oa=true  ─► open_access_pdf.fetch (PDF cache)  │
  │         └─ is_oa=false ─► biorxiv_fallback.find_preprint     │
  │                             (se preprint existe: PDF cache)  │
  │                             └─ senao: manual_required bucket │
  │     upload_queue.put(UploadTask)                             │
  └──────────────────────────────────────────────────────────────┘
  ┌─── generic_pool (max 5) ─────────────────────────────────────┐
  │   worker:                                                    │
  │     cloudflare_known → manual bucket direto                  │
  │     demais → upload_queue.put (URL-only)                     │
  └──────────────────────────────────────────────────────────────┘
  │
  ▼
_maybe_score(task) em paralelo dentro de cada worker ncbi/academic (v3 F6):
  - paper_scorer.score_paper(doi/pmid)
    ├─ semantic_scholar.fetch (cache s2/ TTL 90d)
    ├─ openalex.fetch         (cache openalex/ TTL 90d)
    └─ biorxiv_fallback.find_preprint (cache biorxiv/ TTL 30d)
  - compose formula: base + influential_bonus + venue_bonus + preprint_bonus + recency_bonus
  - tier 1/2/3 ou "unknown"
  - best-effort: exception nao bloqueia upload
  - task.academic_{score,tier,rationale,signals} preenchidos
  │
  ▼
cleanup_captcha_sources.py (1x por notebook, antes dos uploads)
  │
  ▼
uploader thread (serial, consumer unico da upload_queue):
  while task = upload_queue.get():
    if task is None: break                 # sentinel
    notebooklm source add <file|url>
    notebook_manifest.record_source(        # file lock + dedup canonical_key
      url, file_path, canonical_key,
      ingest_method, ingest_metadata={
        ...,
        "academic_score": task.academic_score,
        "academic_tier": task.academic_tier,
        "preprint_fallback": True/False,
      }
    )
  │
  ▼
_write_ranking_report() (v3):
  - lê manifesto, filtra sources com academic_score
  - ordena desc por score, tabela por tier
  - renderiza assets/templates/academic-ranking-report.md
  - salva em <work_dir>/academic-ranking-report.md
  │
  ▼
summary JSON + 3-bucket report + ranking report:
  - auto_uploaded | manual_required | paywall_unavailable
  - tier_distribution: {tier_1, tier_2, tier_3, unknown}
  - cache_hits, api_calls, elapsed_seconds, rate_limit_events
```

### Diferencas chave v1 → v2 → v3

| Aspecto | v1 | v2 | v3 |
|---|---|---|---|
| Cache | 0 (re-fetch sempre) | `~/.cache/deep-research-sci/` TTL diferenciado (pmid 365d, doi 30d, errors 7d) | Mesmo + cache para S2/OpenAlex/bioRxiv (90d/90d/30d) |
| Paralelismo | serial | 3 pools (ncbi/academic/generic) + uploader thread serial | Mesmo + scorer paraleliza 3 APIs dentro do worker |
| DOIs paywalled | → manual bucket | → Unpaywall-first, so manual se nao-OA | → bioRxiv fallback antes de manual |
| Tiering | heuristica (stars/views/data) | Mesmo | scorer composto 0-100 + tier 1/2/3/unknown + rationale |
| Rate limiting | `_http.py` throttle serial simples | token bucket thread-safe + backoff global em 429 | Mesmo + 3 buckets novos (s2/openalex/biorxiv) |
| Output extra | 3-bucket report | Mesmo + summary com cache_hits/api_calls | Mesmo + academic-ranking-report.md + tier_distribution |
| Flags de opt-out | — | `--no-cache`, `--serial`, `--max-parallel N`, `--invalidate-cache-before` | Mesmo + `--skip-scoring`, `--skip-biorxiv-fallback` |

## Roteamento detalhado por tipo

### `pubmed`
1. `pubmed_abstract.py <PMID>` → `.txt` com abstract (sempre disponivel)
2. `pmid_to_pmc.py <PMID>` → PMCID ou `null`
3. Se PMCID existe: `pmc_fulltext.py <PMCID>` → `.txt` com full-text
4. Upload o melhor arquivo disponivel (full-text preferido, abstract de fallback)
5. Canonical key: `pmc:<PMCID>` se full-text; caso contrario `pmid:<PMID>`

### `pmc`
1. `pmc_fulltext.py <PMCID>` direto
2. Se `< 5000 chars`, provavelmente captcha/redirect — vai para manual bucket
3. Canonical key: `pmc:<PMCID>`

### `doi`
1. `unpaywall_resolver.py <DOI>` — requer env `UNPAYWALL_EMAIL`
2. Se `is_oa=true` e `oa_pdf_url`: `open_access_pdf.py` para baixar PDF
3. Se nao-OA: vai para manual bucket (respeita paywall)
4. Canonical key: `doi:<DOI>`

### `cloudflare_known`
Nao tenta upload. Adiciona ao manual bucket com instrucao: "Abrir em browser, baixar PDF, arrastar pro NotebookLM".

Razao: Cloudflare detecta urllib e retorna pagina de challenge. Playwright fallback sera v2.

### `gov_or_guideline`, `blog_or_news`, `generic_web`
URL direto via `notebooklm source add <url>`. NotebookLM scraper lida bem com estes.

## Configuracoes de ambiente

```bash
# Obrigatoria para DOIs (Unpaywall API e free mas exige email)
export UNPAYWALL_EMAIL="fernandinho.costa.neto@gmail.com"

# Opcional — com key NCBI permite 10 req/s (sem: 3 req/s)
export NCBI_API_KEY="abc123..."
```

Para obter NCBI API key (gratis, 5 min): https://www.ncbi.nlm.nih.gov/account/settings/

## Padroes de erro e acao

| Sintoma | Causa provavel | Acao automatica |
|---------|---------------|-----------------|
| NCBI HTTP 429 | Rate limit | Sleep 5s exponencial; max 2 retries |
| PMC HTML < 5000 chars | Captcha ou redirect | Fail soft; manual bucket |
| Unpaywall `is_oa=false` | Paywall real | Skip; paywall bucket |
| PDF fetch sem `%PDF` signature | Landing HTML ao inves do arquivo | Salva como `.html`; warning |
| `notebooklm source add` falha com auth | Sessao expirada | Abort Fase 4.5; pedir `notebooklm login` |

## Debugging

### Testar classificacao sem rodar o pipeline
```bash
python scripts/sci_fetch/classify_url.py "https://pubmed.ncbi.nlm.nih.gov/12345/"
# → {"url": "...", "type": "pubmed", "confidence": 1.0, "metadata": {"pmid": "12345"}}
```

### Rodar classificacao em lote
```bash
python scripts/sci_fetch/classify_url.py --batch urls.txt > classifications.json
```

### Testar fetch sem upload
```bash
python scripts/sci_fetch/upload_to_nblm.py \
  --urls urls.txt \
  --notebook <NB_ID> \
  --pesquisa <slug> \
  --pesquisas-root pesquisas/ \
  --skip-upload
```

Isto baixa arquivos para `pesquisas/<slug>/fontes/sci_fetch/` sem tentar upload.

### Cleanup apenas (idempotente)
```bash
python scripts/sci_fetch/cleanup_captcha_sources.py --notebook <NB_ID> --dry-run
# Remova --dry-run para deletar de fato
```

## Quando NAO rodar Fase 4.5

- Pesquisa nao-cientifica (< 3 URLs pubmed/pmc/doi)
- Usuario passou `--skip-sci-pipeline`
- `notebooklm` CLI nao instalada / nao logada
- `UNPAYWALL_EMAIL` nao configurada E ha DOIs na pesquisa (logar warning, pular DOIs, continuar com PMID/PMC)

## Extendendo o pipeline

### Adicionar novo publisher Cloudflare-known
Edite `scripts/sci_fetch/classify_url.py`, adicione host a `_CLOUDFLARE_HOSTS`.

### Adicionar novo tipo (ex: bioRxiv)
1. Nova regex em `classify_url.py`
2. Novo handler em `upload_to_nblm.py` (ex: `_handle_biorxiv()`)
3. Documentar em `references/sci-pipeline.md` (este arquivo)

### Fallback Firecrawl para `cloudflare_known` (implementado)
Flag `--firecrawl-fallback`: antes de mandar a URL `cloudflare_known` para o bucket manual, o `_worker_generic` tenta `firecrawl scrape` (renderiza JS + bypassa Cloudflare) e, se obtem conteudo real (>= 600 bytes, sem cara de bloqueio), sobe como arquivo markdown ao NotebookLM com `fetch_method: firecrawl_scrape` no manifesto. Gated em `FIRECRAWL_API_KEY`; 1 credito/URL; respeita o limite de 2 scrapes paralelos do plano. Detalhes e tiers de fetch: `references/fetch-fallback.md`.

## Guardrails eticos

- **Nao** usar Sci-Hub / Library Genesis (politica Anthropic)
- **Nao** scrapping agressivo (max 2 retries)
- **Sim** a Unpaywall (legal, gratuito, preprints oficiais)
- **Sim** a NCBI E-utilities (API publica, reconhecida)
- Respeitar `robots.txt` em `generic_web`
