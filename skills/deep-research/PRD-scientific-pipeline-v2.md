# Scientific Source Pipeline v2 — PRD

**Autor:** Fernando Costa Neto | **Data:** 2026-04-23 | **Status:** Draft
**Nivel:** Standard
**Skill alvo:** `~/.claude/skills/deep-research/` (v2 upgrade)
**Upstream:** PRD v1 `PRD-scientific-pipeline.md` (implementado 2026-04-23); execucao real farmacologia 2026-04-22 (86 URLs, baseline 40% → ~95% apos improviso); discussao de gaps 2026-04-23

---

## 1. Problema & Contexto

### 1.1 Voz do Usuario

> "A v1 resolve o bloqueio principal de CAPTCHA, mas deixou quatro frustrations no fluxo: (1) DOIs caem para manual bucket mesmo quando existe preprint OA; (2) toda vez que faco delta research, re-baixo papers que ja tinha — desperdicio de 2-3 min + cota NCBI; (3) pesquisas grandes (50+ URLs) levam 7 minutos esperando uma por vez; (4) priorizacao de papers por stars/views/data e heuristica fraca — queria saber quais sao os seminais, os que realmente mudaram o campo, nao so os mais recentes ou com melhor SEO. Quero elevar de 'funciona' para 'funciona rapido e me da papers de qualidade sem eu ter que filtrar manualmente'."
> — Fernando, apos implementar v1 (2026-04-23)

### 1.2 Evidencia Quantitativa (do baseline v1 + estimativas v2)

| Metrica | v1 baseline (medido) | v2 meta | Fonte |
|---|---|---|---|
| Sucesso NotebookLM (URLs cientificas) | ~90% (meta v1) | >=95% | Medido apos implementacao v1 |
| DOIs viram source util | ~0% (todos para manual) | >=60% (via Unpaywall-first) | F6 |
| Tempo p95 para 50 URLs | ~7 min | <= 2.5 min | F9 |
| Cache hit rate em delta research | 0% | >= 80% | F8 |
| Tier-1 papers com sinal academico (citacoes/venue rank) | 0% | 100% em dominios cientificos | v3 |

### 1.3 MITRE Problem Framing

**Suposicoes implicitas da v1:**
- Usuario aceita re-baixar conteudo em cada run (nao ha cache persistente)
- DOIs sem upload direto no NotebookLM caem para manual bucket (aceitavel)
- Serial fetching e "rapido o suficiente" para pesquisas <= 50 URLs
- Ranking por stars/views/data de publicacao e suficiente para tiering de papers

**Quem sofre:**
- **Usuario primario (Fernando):** pesquisas cientificas grandes levam 7+ min, delta research re-faz trabalho; DOIs paywalled sempre exigem acao manual mesmo quando ha preprint gratuito; tiering ignora citacoes academicas
- **Usuario secundario (Claude Code users em saude/bio/longevidade):** mesma dor, agravada por nao ter tolerancia para debugar o pipeline

**How Might We:**
> Como podemos reduzir friction em pesquisas cientificas grandes (tempo), evitar re-fetch em deltas (cache), e priorizar papers por sinal academico real (citacoes, recencia em preprint server, venue rank) em vez de so heuristicas de URL?

### 1.4 Por Que Agora

- v1 foi validada — problema de CAPTCHA esta resolvido, mas friction residual virou gargalo
- Proximas pesquisas cientificas ja planejadas (longevidade + farmacologia follow-up + cliente de saude) vao multiplicar o custo do friction
- v3 (academic graph APIs) abre porta para skill futura `/paper-deep-dive` que recebe PMID e devolve impacto/replicacoes — infra de v3 habilita isso

---

## 2. Objetivos & Metricas

### 2.1 Metrica Primaria (North Star)

**Tempo e qualidade combinados em pesquisa cientifica padrao (50 URLs):**
- **Tempo total p95:** <= 2.5 min (vs ~7 min v1)
- **Qualidade (precision@10):** >= 80% dos papers no Tier 1 tem `citation_count > 50` OU `influential_citations > 5` OU `venue_h_index_top_quartile`

### 2.2 Metricas Secundarias (3 camadas)

**Camada 1 — Desempenho:**
| Metrica | v1 baseline | v2 meta |
|---|---|---|
| Tempo p95 50 URLs | ~7 min | <= 2.5 min |
| Tempo p50 20 URLs | ~3 min | <= 1 min |
| Cache hit rate (delta research) | 0% | >= 80% |

**Camada 2 — Cobertura:**
| Metrica | v1 baseline | v2 meta |
|---|---|---|
| DOIs viram source util | ~0% | >= 60% |
| Papers com sinal academico no relatorio | 0% | 100% em dominios cientificos |
| bioRxiv fallback ativado quando DOI paywalled + preprint existe | 0% | >= 50% |

**Camada 3 — Confiabilidade:**
| Metrica | v1 baseline | v2 meta |
|---|---|---|
| HTTP 429 por corrida (NCBI) | raros (serial) | 0 (token bucket) |
| Cache corruption (arquivo invalido) | N/A | 0 (atomic write) |
| Thread race em manifesto | N/A | 0 (file lock ja existe + testado) |

### 2.3 Guardrails (nao podem regredir)

- **NCBI rate limit:** nunca exceder 3/s sem key, 10/s com key — medido por corrida com log
- **Retrocompatibilidade:** scripts v1 continuam funcionando standalone (classify_url, pubmed_abstract, etc.)
- **Stdlib-only (RNF-05 do v1):** nao introduzir requests/aiohttp/beautifulsoup; `concurrent.futures` e `threading` sao stdlib
- **Opt-out:** flags `--no-cache`, `--serial`, `--skip-scoring` para degradar para comportamento v1 se algo quebrar
- **Custo:** APIs academicas de v3 sao todas free (Semantic Scholar 100 req/min, OpenAlex 100k/dia, bioRxiv sem limite)

---

## 3. Escopo

### 3.1 Dentro do Escopo — v2 (este PRD)

**Epic 1 — F6: Unpaywall-first para DOIs**
- RF-01: refatorar `upload_to_nblm.py::_handle_doi()` para tentar Unpaywall antes de cair em manual bucket
- RF-02: se `is_oa=true` + `oa_pdf_url`: fetch via `open_access_pdf.py` + upload como arquivo
- RF-03: registrar fluxo no manifesto com `ingest_method: pdf_upload` e `ingest_metadata.unpaywall_host_type`

**Epic 2 — F8: Cache local diferenciado**
- RF-04: novo modulo `scripts/sci_fetch/_cache.py` com TTL diferenciado
- RF-05: `pmid`/`pmcid` com TTL 365d (efetivamente imutavel)
- RF-06: `doi` (resposta Unpaywall) com TTL 30d (editor pode abrir OA)
- RF-07: cache de erros (`is_oa=false`, `404`, `captcha`) com TTL 7d
- RF-08: estrutura `~/.cache/deep-research-sci/{pmid|pmcid|doi|pdf|errors}/`
- RF-09: flag `--invalidate-cache-before YYYY-MM-DD` para forcar re-fetch
- RF-10: flag `--no-cache` para bypass total (debugging)

**Epic 3 — F9: Parallel fetching com rate-limit coordenado**
- RF-11: novo modulo `scripts/sci_fetch/_token_bucket.py` thread-safe
- RF-12: 3 buckets: `ncbi` (3/s ou 10/s com key), `unpaywall` (5/s), `semantic_scholar` (1/s sem key ou 10/s com key), `openalex` (10/s), `biorxiv` (2/s)
- RF-13: `ThreadPoolExecutor` com 3 pools separados em `upload_to_nblm.py`
  - Pool NCBI: 3 workers
  - Pool Unpaywall+academic: 3 workers
  - Pool generic (gov/blog/web): 5 workers
- RF-14: upload ao NotebookLM **serializado** (fila) mesmo com download paralelo (evita race server-side)
- RF-15: backoff global em 429 (penaliza bucket inteiro, nao so worker afetado)
- RF-16: flag `--max-parallel N` para override (default 3/3/5)
- RF-17: flag `--serial` para desativar paralelismo (debugging ou sistemas lentos)

**Epic 4 — v3: Seleção inteligente de papers via academic graph**
- RF-18: novo cliente `scripts/sci_fetch/semantic_scholar.py`
  - Endpoint: `https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}` ou `/PMID:{pmid}`
  - Fields: `citationCount,influentialCitationCount,year,tldr,venue,authors.name,authors.hIndex`
- RF-19: novo cliente `scripts/sci_fetch/openalex.py`
  - Endpoint: `https://api.openalex.org/works/doi:{doi}`
  - Fields: `cited_by_count,primary_location.source.h_index,concepts`
- RF-20: novo cliente `scripts/sci_fetch/biorxiv_fallback.py`
  - Endpoint: `https://api.biorxiv.org/details/biorxiv/{doi}` e `/medrxiv/{doi}`
  - Se DOI nao-OA no Unpaywall mas preprint existe: usa preprint como fonte
- RF-21: novo modulo `scripts/sci_fetch/paper_scorer.py` compondo:
  - `citation_count` normalizado por idade (citations/year, evita viés anti-novo)
  - `influential_citations` (Semantic Scholar — cita com contexto nao-trivial)
  - `venue_rank` (OpenAlex primary_location h-index, quartile)
  - `recency_bonus` (preprint < 2 anos OU published < 1 ano em journal top-tier)
  - `preprint_availability` (bioRxiv/medRxiv compensa paywall)
  - Output: score 0-100 + tier (1/2/3) + rationale curto
- RF-22: Fase 4.5 estendida para chamar scorer em paralelo com fetching
- RF-23: nova secao no `PESQUISA-*.md`: "Papers ranqueados por sinal academico" com tabela score+tier+citacoes+venue+rationale
- RF-24: flag `--skip-scoring` para degradar ao tiering heuristico v1

### 3.2 Futuro — v3+ (apos v2 ship)

**F10. Citation graph expansion:** dado os top 5 Tier-1 papers, consultar Semantic Scholar "papers that cite this" para descobrir papers relacionados que nao apareceram na busca. Loop de 1 nivel.

**F11. Venue whitelist/blacklist configuravel:** usuario marca venues confiaveis (NEJM, Lancet, Nature, etc.) e nao-confiaveis (predatory journals) — scorer usa pesos por venue.

**F12. Autor authority:** h-index do autor principal (OpenAlex) entra no scorer para topicos com autores-chave (ex: Peter Attia, David Sinclair).

**F13. `notebook-source-auditor` skill:** consome o manifesto, detecta sources `failed`/`captcha_pending` antigas, orquestra retry com estrategia apropriada.

**F14. Cache distribuido entre usuarios:** opt-in, um store S3/R2 com PMIDs + abstracts compartilhados (mas precisa resolver licenca + privacy).

### 3.3 Explicitamente Postergado (ate nova validacao)

**Playwright fallback para Cloudflare-known** (era F7 do v1): decisao deliberada de nao implementar — manual bucket e aceitavel; custo (200MB chromium + 5-10s por URL + risco de detecção) nao justifica com volumes tipicos de 3-4 Cloudflare URLs por pesquisa. Re-avaliar se volume subir acima de 10/pesquisa.

---

## 3b. Fora do Escopo (justificativas)

| Item | Por que fora | Trade-off |
|---|---|---|
| **F7. Playwright fallback** | Dependencia pesada, +5-10s/URL, risco de ban, volume atual pequeno | Cloudflare URLs continuam indo para manual bucket |
| **Sci-Hub / LibGen integration** | Politica Anthropic, ilegal em varias jurisdicoes | v2 melhora OA, mas paywalls legitimos continuam fora |
| **Translation de papers nao-ingles** | Out of scope; NotebookLM ja lida nativamente | — |
| **OCR de PDFs escaneados** | NotebookLM ja faz em upload | Nao duplicar trabalho |
| **Full-text search local dos papers cacheados** | Skill separada (`/paper-search`) se virar necessario | Cache e so para re-uso no fluxo, nao para grep |
| **Cache distribuido entre maquinas** | Complexidade + privacy + licenca | v3+ |
| **Author tracking / h-index pessoal** | Esperar v2 validar scorer basico antes de expandir | v3 futura |
| **Multi-notebook strategy** (split >300 sources) | Edge case raro; tratar quando aparecer | v3 |

---

## 4. Personas & Casos de Uso

### Persona Primaria: Fernando (usuario ativo, pesquisas recorrentes)
- **Contexto novo em v2:** ja validou v1, volume de pesquisas cientificas aumentou (3-4 por mes)
- **Dor atual:** esperar 7min, re-fetch em updates, DOIs manuais, filtrar papers por heuristica fraca
- **Expectativa v2:** "quero que a pesquisa cientifica seja tao rapida quanto uma pesquisa de Next.js, e que os Tier 1 sejam os de verdade seminais — nao os blogs mais bem escritos"
- **JTBD:** "preciso de uma base de conhecimento farmacologica E uma hierarquia confiavel de 'o que de fato importa' sem eu ter que ler 86 papers pra decidir"

### Persona Secundaria: Claude Code user em saude/bio (esporadico)
- Menos tolerancia a configuracao de cache/paralelismo
- Precisa de defaults sensatos + flag de override unica (`--scientific`)
- Espera o scorer academico "just work" sem configurar pesos

### Caso de Uso Principal — Pesquisa grande com delta research

```
Given: Fernando tem pesquisa anterior sobre GLP-1s (de 2026-04-22, 110 sources no NotebookLM)
When: 6 meses depois (2026-10-22), roda /deep-research "atualizar pesquisa GLP-1s" em modo Update
Then:
  - Subagentes delta retornam 40 URLs novas; 15 delas ja existem no cache (cited-by previous papers)
  - Fase 4.5 ativa:
    - 15 URLs resolvidas em <1s cada via cache (PMID/PMCID/DOI stable TTL)
    - 25 URLs novas processadas em paralelo: 3 workers NCBI + 3 Unpaywall + 5 generic
    - 6 DOIs encontraram preprint via bioRxiv fallback (3 eram paywalled, 3 eram OA mas preferimos preprint em repository)
    - Scorer roda em paralelo, enriquece relatorio com tier academico
  - Tempo total: 80s (vs ~5 min em v1 sem cache)
  - Relatorio destaca: "3 papers Tier 1 novos com >100 citacoes/ano; 1 paper Tier 2 atualizou evidencia de gap anterior"
```

---

## 5. Epic Hypotheses

### Epic 1 (F6): Unpaywall-first resolve DOIs paywalled

**Hipotese:** Se o orquestrador tentar Unpaywall ANTES de cair para manual bucket, resolveremos >=60% dos DOIs (baseline: ~40% dos DOIs academicos tem versao OA segundo estudos Unpaywall publicos).

**Tiny act of discovery:** modificar `_handle_doi()` para um DOI especifico (ex: 10.1089/thy.2014.0028) e validar que retorna PDF via open_access_pdf.py. Teste custa 30s de codigo + 1 chamada API.

### Epic 2 (F8): Cache diferenciado corta tempo em delta research

**Hipotese:** Se cachear PMID/PMCID com TTL 365d, tempo de delta research com >50% de URLs conhecidas cai de ~5min para <1min. Razao: fetching NCBI e gargalo em pesquisas pequenas/medias.

**Tiny act:** simular delta research usando fixtures ja baixadas (`~/.claude/skills/research/pdfs/` tem 18 PMCs da sessao de 2026-04-22). Pre-popular cache com eles e medir vs fetch real. Custo: 10 min de script.

### Epic 3 (F9): Paralelismo com token bucket preserva rate limits

**Hipotese:** Se cada API tem seu token bucket global (thread-safe) e pools de workers separados, 50 URLs sao processadas em <2.5min sem violar rate limit de nenhuma API.

**Tiny act:** implementar token bucket + rodar teste de stress com 20 PMIDs concorrentes. Contar HTTP 429 (esperado 0). Custo: 45 min.

### Epic 4 (v3): Academic scoring produz tiering superior

**Hipotese:** Se compusermos citacoes normalizadas + venue rank + preprint availability em um score 0-100, o top-5 por score v2 tem overlap <= 40% com top-5 por heuristica v1 (stars/views/data) — indicando que estamos pegando sinal diferente e mais academico.

**Tiny act:** pegar os 10 papers da sessao farmacologia 2026-04-22, ranquear pelos dois metodos, comparar manualmente qual lista Fernando acha "mais seminal". Custo: 20 min.

---

## 6. Requisitos Funcionais

### Epic 1 — F6 Unpaywall-first

#### RF-01. Refatorar `_handle_doi()` no orquestrador
**Antes (v1):**
```python
elif cls["type"] == "doi":
    canonical = f"doi:{cls['metadata']['doi']}"
    buckets["manual_required"].append({...})
```

**Depois (v2):**
```python
elif cls["type"] == "doi":
    doi = cls["metadata"]["doi"]
    canonical = f"doi:{doi}"
    unpaywall_result = unpaywall_resolver.resolve(doi, email=env)
    if unpaywall_result["is_oa"] and unpaywall_result["oa_pdf_url"]:
        pdf_path = work_dir / f"doi_{_safe_slug(doi)}.pdf"
        try:
            open_access_pdf.fetch(unpaywall_result["oa_pdf_url"], out=pdf_path)
            file_path = pdf_path
            ingest_method = "pdf_upload"
            metadata_meta["unpaywall_host_type"] = unpaywall_result["host_type"]
        except Exception as e:
            buckets["manual_required"].append({..., "reason": f"Unpaywall OK mas PDF fetch falhou: {e}"})
    else:
        buckets["manual_required"].append({..., "reason": "DOI nao-OA no Unpaywall"})
```

**Aceite:**
- [ ] DOI com `is_oa=true` resulta em upload como arquivo
- [ ] DOI com `is_oa=false` vai para manual bucket com reason explicita
- [ ] Falha de PDF fetch (ex: 403) nao derruba pipeline; cai em manual com reason
- [ ] Manifesto registra `ingest_method: pdf_upload` com `ingest_metadata.unpaywall_host_type` (publisher/repository)

### Epic 2 — F8 Cache

#### RF-04. Modulo `_cache.py`
**API:**
```python
def cache_get(kind: Literal["pmid", "pmcid", "doi", "pdf", "errors"], key: str,
              ttl_days: int = None) -> Optional[bytes | str]
def cache_put(kind: str, key: str, content: bytes | str, ttl_override_days: int = None) -> Path
def cache_clear(before_date: datetime = None, kinds: list[str] = None) -> int  # returns N removed
```

**Aceite:**
- [ ] Atomic write (`.tmp` + `os.rename`)
- [ ] Layout: `~/.cache/deep-research-sci/{kind}/{safe_key}.{ext}`
- [ ] Metadata no cache: mtime e TTL-tag no filename `PMC7054893.ttl365d.txt` ou header
- [ ] Concurrency-safe: duas threads escrevendo mesmo key → atomic, last-writer-wins sem corrupcao
- [ ] Tests unitarios cobrem: miss, hit, expired, atomic write, concurrent write

#### RF-05 a RF-07. TTL por tipo

| Kind | TTL default | Razao |
|---|---|---|
| `pmid` | 365d | PMID metadata praticamente imutavel |
| `pmcid` | 365d | Full-text final, muito estavel |
| `doi` | 30d | Resposta Unpaywall pode mudar (editor libera OA) |
| `pdf` | 365d | PDF content estavel; hash no filename |
| `errors` | 7d | Re-tenta semanalmente (transient 429, captcha, 503) |

**Aceite:**
- [ ] Cada handler respeita seu TTL
- [ ] Cache de erros persiste: `is_oa=false` cacheado evita bater Unpaywall 3x na mesma sessao

#### RF-08. Layout do cache
```
~/.cache/deep-research-sci/
├── pmid/33567185.txt
├── pmcid/PMC7054893.txt
├── doi/10.1089_thy.2014.0028.json
├── pdf/<sha256>.pdf
└── errors/
    ├── doi/10.1089_thy.2014.0028.json        # {"status": "not_oa", "cached_at": "...", "ttl_days": 7}
    └── pmcid/PMC9999999.json                 # {"status": "captcha_detected", ...}
```

#### RF-09/10. Flags de controle
- `--invalidate-cache-before 2026-01-01` — remove entradas com mtime < date
- `--no-cache` — bypass total (para debug ou quando desconfia)

### Epic 3 — F9 Paralelismo

#### RF-11. `_token_bucket.py`
```python
class TokenBucket:
    def __init__(self, rate_per_sec: float, burst: int = None): ...
    def acquire(self, tokens: int = 1) -> None: ...  # blocks if needed
    def penalize(self, seconds: int) -> None: ...  # for 429 global backoff
```

**Aceite:**
- [ ] Thread-safe (threading.Lock interno)
- [ ] `acquire()` dorme o minimo necessario
- [ ] `penalize(60)` congela bucket por 60s mesmo com tokens remanescentes
- [ ] Tests: 10 threads acquire, contar req/s resultante — nunca > rate

#### RF-12. Buckets pre-configurados
```python
BUCKETS = {
    "ncbi": TokenBucket(rate_per_sec=10 if has_ncbi_key() else 3),
    "unpaywall": TokenBucket(rate_per_sec=5),
    "semantic_scholar": TokenBucket(rate_per_sec=10 if has_s2_key() else 1),
    "openalex": TokenBucket(rate_per_sec=10),
    "biorxiv": TokenBucket(rate_per_sec=2),
}
```

#### RF-13/14. Pools e upload serializado

```python
def process_urls_parallel(urls, notebook_id, ...):
    classified = [(u, classify(u)) for u in urls]
    # Particiona
    ncbi_tasks = [...]
    academic_tasks = [...]   # doi + scoring
    generic_tasks = [...]

    upload_queue = queue.Queue()
    download_errors = []

    with ThreadPoolExecutor(max_workers=3) as ncbi_pool, \
         ThreadPoolExecutor(max_workers=3) as academic_pool, \
         ThreadPoolExecutor(max_workers=5) as generic_pool:

        futures = []
        futures += [ncbi_pool.submit(handle_ncbi, u, c, upload_queue) for u, c in ncbi_tasks]
        futures += [academic_pool.submit(handle_doi, u, c, upload_queue) for u, c in academic_tasks]
        futures += [generic_pool.submit(handle_generic, u, c, upload_queue) for u, c in generic_tasks]

        # Uploader thread consome fila
        uploader = threading.Thread(target=_upload_worker, args=(upload_queue, notebook_id))
        uploader.start()

        for fut in as_completed(futures):
            try:
                fut.result()
            except Exception as e:
                download_errors.append(e)

        upload_queue.put(None)  # sentinel
        uploader.join()
```

**Aceite:**
- [ ] Download paralelo; upload sequencial (NotebookLM CLI nao e thread-safe)
- [ ] Erro em 1 worker nao cancela os outros; coleta em `download_errors` e reporta
- [ ] `--serial` flag desativa pools (fallback modo v1)
- [ ] Test de stress: 20 PMIDs concorrentes → 0 HTTP 429

#### RF-15. Backoff global em 429
```python
def handle_429(bucket_name: str, retry_after: int = 60):
    BUCKETS[bucket_name].penalize(retry_after)
    log.warning(f"429 em {bucket_name}; pausando bucket por {retry_after}s")
```

### Epic 4 — v3 Academic scoring

#### RF-18. `semantic_scholar.py`
**Input:** DOI ou PMID
**Output:**
```json
{
  "paper_id": "DOI:10.1089/thy.2014.0028",
  "citation_count": 156,
  "influential_citation_count": 23,
  "year": 2015,
  "venue": "Thyroid",
  "tldr": {"text": "Magnesium supplementation..."},
  "authors": [{"name": "...", "h_index": 42}]
}
```

**API:** `https://api.semanticscholar.org/graph/v1/paper/{id}?fields=citationCount,influentialCitationCount,year,venue,tldr,authors.name,authors.hIndex`

**Rate limit:** 1 req/s sem key, 10 req/s com key. Suporta API key opcional via env `SEMANTIC_SCHOLAR_API_KEY`.

**Aceite:**
- [ ] Aceita DOI ou PMID como input, prefixa corretamente (`DOI:` ou `PMID:`)
- [ ] Respeita bucket `semantic_scholar`
- [ ] Retorna `None` em 404 (paper nao indexado), nao raise

#### RF-19. `openalex.py`
**Input:** DOI
**Output:**
```json
{
  "work_id": "W2057382412",
  "cited_by_count": 234,
  "venue_h_index": 68,
  "venue_quartile": "Q1",
  "concepts": [{"display_name": "Hashimoto disease", "score": 0.89}]
}
```

**API:** `https://api.openalex.org/works/doi:{doi}`
Polite pool: email via query param `?mailto=...`

**Aceite:**
- [ ] Mapeia `primary_location.source.h_index` para `venue_h_index`
- [ ] Computa quartile baseado em venue h-index (Q1 > 50, Q2 20-50, Q3 5-20, Q4 < 5 — calibravel)
- [ ] Retorna top 3 concepts com score > 0.7

#### RF-20. `biorxiv_fallback.py`
**Input:** DOI
**Output:**
```json
{
  "preprint_doi": "10.1101/2024.01.15.123456",
  "pdf_url": "https://www.biorxiv.org/content/10.1101/.../v1.full.pdf",
  "preprint_server": "bioRxiv",
  "version": 1,
  "posted_date": "2024-01-15"
}
```

**APIs (em ordem):**
1. `https://api.biorxiv.org/details/biorxiv/{doi}`
2. `https://api.biorxiv.org/details/medrxiv/{doi}`

**Quando chamar:** Unpaywall retornou `is_oa=false` E paper tem sinal de biomedico (concepts relevantes em OpenAlex).

**Aceite:**
- [ ] Retorna preprint mais recente (maior `version`)
- [ ] PDF URL valido (verifica com HEAD request)
- [ ] Cache com TTL 30d (preprints podem ter novas versoes)

#### RF-21. `paper_scorer.py`
**Input:** URL ou DOI ou PMID
**Output:**
```json
{
  "canonical_key": "doi:10.1089/thy.2014.0028",
  "score": 78,
  "tier": 1,
  "signals": {
    "citations_per_year": 14.2,
    "influential_citations": 23,
    "venue_h_index": 68,
    "venue_quartile": "Q1",
    "preprint_available": false,
    "recency_bonus": 0.0,
    "age_years": 11
  },
  "rationale": "High venue (Thyroid, H=68), moderate citation rate (14/yr), 23 influential citations — established reference"
}
```

**Formula (explicavel, calibravel):**
```
base = min(50, citations_per_year * 3)  # max 50 pts
influential_bonus = min(20, influential_citations * 0.5)  # max 20
venue_bonus = {"Q1": 20, "Q2": 10, "Q3": 5, "Q4": 0}[quartile]
preprint_bonus = 10 if (preprint_available and age < 2) else 0
recency_bonus = 10 if (age_years < 3 and citations_per_year > 5) else 0
score = base + influential_bonus + venue_bonus + preprint_bonus + recency_bonus
score = min(100, score)

tier = 1 if score >= 70 else (2 if score >= 40 else 3)
```

**Aceite:**
- [ ] Score reproduzivel (mesma entrada = mesma saida)
- [ ] Rationale gerado automaticamente com 1-2 frases explicando sinais dominantes
- [ ] Handle missing data: se sem Semantic Scholar (404), usa so OpenAlex; se sem ambos, tier-default "unknown" (nao falha)
- [ ] Flag `--score-weights path/to/weights.json` permite override (futuro F11)

#### RF-22. Integracao na Fase 4.5
Scorer roda **em paralelo** ao fetching, nao em serie. Workers academicos spawnam:
```python
def handle_doi(url, cls, upload_queue):
    doi = cls["metadata"]["doi"]
    # Tres chamadas em paralelo internas ao worker
    with ThreadPoolExecutor(max_workers=3) as inner_pool:
        unpaywall_fut = inner_pool.submit(unpaywall_resolver.resolve, doi)
        s2_fut = inner_pool.submit(semantic_scholar.fetch, doi)
        oa_fut = inner_pool.submit(openalex.fetch, doi)
        # scoring depende de s2 + oa
        ...
```

#### RF-23. Nova secao no PESQUISA-*.md
```markdown
## Papers ranqueados por sinal academico (v3)

**Metodo:** Semantic Scholar + OpenAlex + bioRxiv. Scoring composto (citacoes/ano + influential + venue + recencia).

| Tier | Titulo | Venue | Year | Citations/yr | Infl. Cit. | Score | Rationale |
|------|--------|-------|------|-------------:|-----------:|------:|-----------|
| 1 | ... | Nature | 2021 | 120 | 45 | 92 | Top venue + high influential |
| 1 | ... | NEJM | 2018 | 85 | 31 | 85 | Established, Q1 |
| 2 | ... | PLoS ONE | 2023 | 12 | 3 | 48 | Recent, moderate citations |
| 3 | ... | MDPI | 2024 | 2 | 0 | 22 | Too new, no established impact |
```

#### RF-24. Flag `--skip-scoring`
Desativa Epic 4 inteiro, volta ao tiering heuristico v1. Uso: debug, ou quando APIs academicas estao fora do ar.

---

## 7. Requisitos Nao-Funcionais

### RNF-01. Performance
- 50 URLs cientificas: p95 <= 2.5 min (vs ~7 min v1)
- 20 URLs: p95 <= 1 min
- Cache hit path: <= 100ms por URL
- Scorer overhead: <= 2s adicional por DOI (paralelo ao fetching, nao bloqueante)

### RNF-02. Confiabilidade
- Zero corrupcao de cache em concurrent writes (tests com 10 threads)
- Zero HTTP 429 em corridas tipicas (medidos por log)
- Fallback graceful: se Semantic Scholar 500, scorer continua com OpenAlex; se ambos falharem, tier "unknown" sem derrubar pipeline
- Atomic write em TODOS os paths de I/O (manifest, cache, files no work_dir)

### RNF-03. Observabilidade
- Log estruturado por API: `[api_name] [status] [elapsed_ms] [rate_limit_remaining]`
- Relatorio end-of-run: contagem por bucket, cache hits, API calls, 429 events
- Progress bar visivel durante Fase 4.5 para pesquisas > 20 URLs

### RNF-04. Seguranca
- Envs: `UNPAYWALL_EMAIL` (obrigatoria), `NCBI_API_KEY` (opcional), `SEMANTIC_SCHOLAR_API_KEY` (opcional), `OPENALEX_EMAIL` (obrigatoria p/ polite pool)
- User-Agent: `DeepResearchSkill/2.0 ({email})` em todas as APIs
- Respeitar robots.txt em generic URLs (ja implementado v1)
- Sem credenciais em cache (cache so armazena conteudo publico)

### RNF-05. Compatibilidade
- Scripts v1 permanecem funcionais standalone
- SKILL.md v1 → v2: aditivo, secoes novas, sem quebrar existentes
- Modo Update (delta research) se beneficia do cache automaticamente
- Usuario que nao configurar nada ganha v1-like com paralelismo (graceful default)

### RNF-06. Portabilidade
- Python 3.8+ stdlib-only (urllib, json, re, time, threading, concurrent.futures, queue)
- macOS e Linux testados; Windows best-effort (zsh/bash assumed)

---

## 8. Consideracoes Tecnicas

### 8.1 Arquitetura atualizada

```
~/.claude/skills/deep-research/
├── SKILL.md                              # + Fase 4.5 v2 notas
├── PRD-scientific-pipeline-v2.md         # este documento
├── scripts/
│   ├── notebook_manifest.py              # v1 inalterado
│   ├── sci_fetch/
│   │   ├── _http.py                      # v1 + penalize hook
│   │   ├── _cache.py                     # NOVO (F8)
│   │   ├── _token_bucket.py              # NOVO (F9)
│   │   ├── classify_url.py               # v1 inalterado
│   │   ├── pubmed_abstract.py            # + cache integration
│   │   ├── pmid_to_pmc.py                # + cache integration
│   │   ├── pmc_fulltext.py               # + cache integration
│   │   ├── unpaywall_resolver.py         # + cache + error cache
│   │   ├── open_access_pdf.py            # + cache integration
│   │   ├── cleanup_captcha_sources.py    # v1 inalterado
│   │   ├── upload_to_nblm.py             # REFATORADO (F6, F9)
│   │   ├── semantic_scholar.py           # NOVO (v3)
│   │   ├── openalex.py                   # NOVO (v3)
│   │   ├── biorxiv_fallback.py           # NOVO (v3)
│   │   └── paper_scorer.py               # NOVO (v3)
├── references/
│   ├── sci-pipeline.md                   # + secoes v2
│   ├── notebook-manifest.md              # v1 inalterado
│   ├── cache-and-rate-limits.md          # NOVO
│   └── academic-scoring.md               # NOVO
├── assets/templates/
│   ├── nblm-upload-report.md             # + linha para scoring
│   └── academic-ranking-report.md        # NOVO
└── evals/
    ├── test_urls_pharmacology.json       # v1
    ├── test_cache_behavior.py            # NOVO
    ├── test_token_bucket.py              # NOVO
    └── test_paper_scorer.py              # NOVO
```

### 8.2 APIs externas (novas + existentes)

| API | Endpoint | Rate limit | Key |
|---|---|---|---|
| Semantic Scholar (novo) | `api.semanticscholar.org/graph/v1/paper/{id}` | 1/s sem key, 10/s com | Opcional (`SEMANTIC_SCHOLAR_API_KEY`) |
| OpenAlex (novo) | `api.openalex.org/works/doi:{doi}` | 10/s polite pool | Email obrigatorio (`OPENALEX_EMAIL`) |
| bioRxiv/medRxiv (novo) | `api.biorxiv.org/details/{server}/{doi}` | 2/s informal | Nenhum |
| NCBI (v1) | v1 | v1 | v1 |
| Unpaywall (v1) | v1 | v1 | v1 |

### 8.3 Contratos de dados (novos)

**Cache entry metadata (implicito no filename + mtime):**
```
pmid/33567185.txt             # mtime > now - 365d → valido
errors/doi/10.1089_xyz.json   # {"status": "not_oa", "last_check": "...", "ttl_days": 7}
```

**Paper scorer output schema:** ver RF-21.

**Relatorio de execucao (novo, emitido ao final de Fase 4.5):**
```json
{
  "timestamp": "2026-04-23T10:15:00Z",
  "total_urls": 50,
  "cache_hits": 18,
  "cache_misses": 32,
  "api_calls": {
    "ncbi": 21,
    "unpaywall": 12,
    "semantic_scholar": 15,
    "openalex": 15,
    "biorxiv": 3
  },
  "rate_limit_events": {"429": 0},
  "elapsed_seconds": 142,
  "buckets": {
    "auto_uploaded": 42,
    "manual_required": 6,
    "paywall_unavailable": 2
  },
  "tier_distribution": {"tier_1": 8, "tier_2": 24, "tier_3": 10, "unknown": 8}
}
```

### 8.4 Padroes de erro (novos)

| Erro | Acao |
|---|---|
| Semantic Scholar 429 | `bucket.penalize(60)`; continua com OpenAlex apenas |
| OpenAlex 503 | Retry 1x em 30s; se falhar, scorer skip venue_bonus |
| bioRxiv 404 | Silencioso — paper simplesmente nao existe em preprint |
| Cache corrupt (JSON invalid) | Renomeia para `.corrupt-{ts}.json`, re-fetch |
| Thread pool task exception | Loga, coleta em `download_errors`, continua |
| Todas as APIs academicas falharam | Scorer retorna tier "unknown", pipeline continua com v1 tiering |

### 8.5 Extensao da SKILL.md

Adicionar apos bloco de env vars da Fase 4.5:

```markdown
### Otimizacoes v2 (opt-out via flags)

- **Cache local** em `~/.cache/deep-research-sci/` (default ON). `--no-cache` desativa
- **Paralelismo** com token buckets por API (default ON). `--serial` desativa
- **Scoring academico** via Semantic Scholar + OpenAlex + bioRxiv (default ON em dominios cientificos). `--skip-scoring` desativa

Ver `references/cache-and-rate-limits.md` e `references/academic-scoring.md` para detalhes.
```

---

## 9. Riscos & Mitigacoes

| # | Risco | Prob | Impacto | Mitigacao |
|---|---|---|---|---|
| R1 | Token bucket race condition em edge case | Baixa | Alto | Tests unitarios com 10+ threads; code review; fallback para `--serial` |
| R2 | Semantic Scholar rate limit muda sem aviso | Media | Medio | Buckets configuraveis via env; monitorar `X-RateLimit-Remaining` header |
| R3 | Unpaywall cache stale: paper foi retratado mas cache diz is_oa=true | Baixa | Medio | TTL 30d; flag `--invalidate-cache-before` manual |
| R4 | Upload serial vira gargalo quando download paraleliza bem | Media | Medio | Profile na pratica; se gargalo, fila com pre-fetch de metadata + batch uploads |
| R5 | Scorer formula vira overfit para farmacologia (dominio da validacao) | Media | Baixo | Weights configuraveis; validar em 2+ dominios (farmacologia + neurociencia) antes de ship |
| R6 | OpenAlex muda schema de `primary_location.source.h_index` | Baixa | Medio | Parse defensivo, log warning, degrade para `venue_h_index=None` |
| R7 | Usuario sem `OPENALEX_EMAIL` configurado quebra pipeline | Alta | Baixo | Skill avisa no boot e usa anonymous pool (rate limit menor) em vez de falhar |
| R8 | Cache disk usage cresce descontroladamente | Media | Baixo | Cleanup CLI `--invalidate-cache-before` + warning se cache > 1GB |
| R9 | Paralelismo quebra ordem no relatorio (determinismo) | Baixa | Baixo | Ordena por canonical_key antes de escrever relatorio |

---

## 10. Questoes em Aberto

- **Q1:** Scorer weights devem ser configuraveis agora (v2) ou so em v3 (F11)?
  - **Proposta:** hardcoded em v2 com formula documentada; externalizar so se validar que 1+ usuarios pediram calibragem.

- **Q2:** Cache global (`~/.cache/`) ou por-projeto (`pesquisas/.cache/`)?
  - **Proposta:** global. PMID 12345 e sempre o mesmo conteudo. Evita duplicacao entre projetos.

- **Q3:** bioRxiv fallback deve rodar PARA TODO DOI (mesmo OA) ou so para paywalled?
  - **Proposta:** so para paywalled em v2. Rodar pra todos dobra trafego em API externa sem ganho claro.

- **Q4:** Scoring deve considerar autor h-index (OpenAlex tem)?
  - **Proposta:** F12 (v3+). Complica formula e precisa validar que o sinal e util no dominio do usuario.

- **Q5:** Como lidar com papers sem DOI (ex: working papers, relatorios governamentais)?
  - **Proposta:** continuam indo pelo caminho v1 (generic_web). Scorer marca tier "unknown" sem rodar APIs.

- **Q6:** Cache compartilhado entre maquinas (iCloud / git)?
  - **Proposta:** out. Privacy + licenca + complexity. Se virar demanda, F14 separado.

- **Q7:** Integracao com `notebook-source-auditor` (skill futura) — v2 precisa expor API?
  - **Proposta:** manifesto ja tem tudo; auditor consome. Nao precisa de nada adicional em v2.

- **Q8:** Scorer deve chamar GPT/Claude para rationale mais rica?
  - **Proposta:** nao. Rationale rule-based (sinais dominantes) e suficiente e determinista.

---

## 11. Timeline & Fases (estimativa Claude Code como executor)

| Fase | Escopo | Horas | Depende de |
|---|---|---|---|
| **F1 - Infra** | `_cache.py` + `_token_bucket.py` + tests | 3-4h | — |
| **F2 - F6 Unpaywall-first** | Refatorar `_handle_doi()` + teste com 5 DOIs reais | 2-3h | F1 (cache) |
| **F3 - F9 Paralelismo** | Refatorar `upload_to_nblm.py` com pools + uploader thread | 3-4h | F1 (bucket) |
| **F4 - F8 Integracao cache** | Adicionar cache em cada handler existente | 2h | F1 |
| **F5 - v3 APIs** | `semantic_scholar.py` + `openalex.py` + `biorxiv_fallback.py` | 4-5h | F1 (bucket + cache) |
| **F6 - v3 Scorer** | `paper_scorer.py` + integracao na Fase 4.5 | 3-4h | F5 |
| **F7 - Docs + templates** | `cache-and-rate-limits.md` + `academic-scoring.md` + template + SKILL.md updates | 2-3h | Todas |
| **F8 - Regression** | Re-rodar pesquisa farmacologia; medir metricas vs v1 | 2h | Todas |
| **Total v2** | | **21-27h** | 2-3 sessions focadas |

**Ordem recomendada de implementacao:**
1. F1 (infra) — habilita tudo
2. F2 (F6) — quick win visivel (DOIs viram source util imediatamente)
3. F4 (F8 integracao) — cache funcional antes de paralelizar (mais facil debugar)
4. F3 (F9 paralelismo) — ganho maior em tempo
5. F5 + F6 (v3) — seletividade de papers
6. F7 + F8 (docs + regression) — close-out

---

## 12. Criterios de Aceite Global (Definition of Done)

v2 ship quando:

- [ ] Todos os RFs passam seus criterios individuais
- [ ] Regression test: re-executar pesquisa farmacologia → >=95% sucesso (vs 90% v1)
- [ ] DOIs: >=60% resolvidos via Unpaywall (vs 0% v1)
- [ ] Tempo p95 para 50 URLs: <=2.5 min (vs 7 min v1)
- [ ] Cache hit rate em simulated delta research: >=80%
- [ ] Zero HTTP 429 em corrida tipica
- [ ] Scorer produz tiering coerente em 2 dominios (farmacologia + 1 outro)
- [ ] `--serial`, `--no-cache`, `--skip-scoring` funcionam como fallback v1-like
- [ ] SKILL.md e references atualizados
- [ ] Grep DoD: zero deprecated model IDs, zero budget_tokens, zero sampling hardcoded
- [ ] Instalada em Claude Code + Desktop + repo
- [ ] ROADMAP.md e memoria atualizados

---

## 13. Anti-Patterns evitados (auto-verificados)

- ✅ Problema na voz do usuario com evidencia quantitativa (nao so narrativa)
- ✅ Escopo v1/v2/v3 + Fora do Escopo com justificativas
- ✅ Metricas em 3 camadas (primaria + secundarias + guardrails)
- ✅ Requisitos com criterios de aceite verificaveis (checkboxes)
- ✅ Schemas de dados + endpoints + rate limits concretos
- ✅ Questoes em aberto explicitas com propostas
- ✅ Nao comeca pela solucao — cada epic tem hipotese + tiny act of discovery
- ✅ Riscos com probabilidade + impacto + mitigacao
- ✅ Timeline realista com ordem de dependencia

---

## Referencias

- PRD v1: `PRD-scientific-pipeline.md` (implementado 2026-04-23)
- Execucao real baseline: sessao 2026-04-22 (`~/.claude/skills/research/pdfs/`)
- Unpaywall: https://unpaywall.org/products/api — public API free
- Semantic Scholar: https://api.semanticscholar.org/ — 100 req/min free, API key aumenta limits
- OpenAlex: https://docs.openalex.org/ — 100k/dia free, polite pool via email
- bioRxiv/medRxiv: https://api.biorxiv.org/ — no formal rate limit

---

**Status:** Draft pronto para review. Proximo passo: "Go" para gerar `tasks-scientific-pipeline-v2.md` com ordem de dependencia executavel, ou revisar secoes antes.
