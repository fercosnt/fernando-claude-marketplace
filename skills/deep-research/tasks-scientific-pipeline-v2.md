# Tasks — Scientific Pipeline v2

**PRD:** `PRD-scientific-pipeline-v2.md`
**Skill:** `~/.claude/skills/deep-research/`
**Data:** 2026-04-23
**Estimativa total:** 21-27h (2-3 sessoes focadas Claude Code)

---

## Arquivos Relevantes

### Existentes (v1, serao modificados)
- `scripts/sci_fetch/_http.py` — adicionar hook `handle_429_globally()` acoplando ao token bucket
- `scripts/sci_fetch/pubmed_abstract.py` — integrar cache
- `scripts/sci_fetch/pmid_to_pmc.py` — integrar cache
- `scripts/sci_fetch/pmc_fulltext.py` — integrar cache
- `scripts/sci_fetch/unpaywall_resolver.py` — integrar cache + error cache
- `scripts/sci_fetch/open_access_pdf.py` — integrar cache (por sha256)
- `scripts/sci_fetch/upload_to_nblm.py` — refatorar completamente (F6 + F9)
- `SKILL.md` — secoes v2, flags novas, env vars novas
- `references/sci-pipeline.md` — secao v2

### Novos (v2)
- `scripts/sci_fetch/_cache.py` — modulo de cache com TTL diferenciado
- `scripts/sci_fetch/_token_bucket.py` — rate limiter thread-safe
- `scripts/sci_fetch/semantic_scholar.py` — cliente Semantic Scholar API
- `scripts/sci_fetch/openalex.py` — cliente OpenAlex API
- `scripts/sci_fetch/biorxiv_fallback.py` — cliente bioRxiv/medRxiv API
- `scripts/sci_fetch/paper_scorer.py` — scorer composto de sinais academicos
- `references/cache-and-rate-limits.md` — documentacao F8 + F9
- `references/academic-scoring.md` — documentacao v3 scorer
- `assets/templates/academic-ranking-report.md` — template secao do PESQUISA-*.md
- `evals/test_cache_behavior.py` — testes unitarios cache
- `evals/test_token_bucket.py` — testes concorrencia bucket
- `evals/test_paper_scorer.py` — testes scorer com fixtures reais

---

## Instrucoes para o executor

1. **Stdlib-only** (RNF-05 do v1 mantido): `urllib`, `json`, `re`, `time`, `threading`, `concurrent.futures`, `queue`, `hashlib`, `pathlib`, `datetime`. **NAO** adicionar `requests`, `aiohttp`, `beautifulsoup4`, etc.
2. **Retrocompatibilidade:** todo script standalone da v1 deve continuar funcional. `--no-cache`, `--serial`, `--skip-scoring` devem degradar para comportamento v1-like.
3. **Atomic I/O:** writes sempre via `.tmp` + `os.rename()` (ja padrao no `notebook_manifest.py`).
4. **Test-first quando critico:** cache e token bucket precisam de testes com threads antes de integracao (F9 depende deles funcionarem). Para v3 APIs, validar com 1 fixture real antes de scalar.
5. **Commits atomicos por task:** cada sub-task entrega um commit funcional. Nao bundle multiplas tasks.
6. **Env vars novas:** `SEMANTIC_SCHOLAR_API_KEY` (opcional), `OPENALEX_EMAIL` (obrigatoria para polite pool). Skill avisa no boot se faltar.
7. **Evitar regressao:** apos cada fase, rodar `python scripts/sci_fetch/classify_url.py --batch evals/test_urls_pharmacology.json` e confirmar 26/26 PASS (smoke test).

---

## Tasks

### Fase 1: Infra (F8 + F9 base) — 3-4h

**Depende de:** nada. Bloqueador de F2-F6.

#### T1.1 — Criar `_cache.py`
**Arquivos:** `scripts/sci_fetch/_cache.py` (novo)
**Refs:** RF-04 a RF-10 do PRD v2

- [ ] 1.1.1 Implementar `cache_path(kind, key) -> Path` com sanitizacao de key (barras/colons viram `_`)
- [ ] 1.1.2 Implementar `cache_get(kind, key, ttl_days=None) -> Optional[str|bytes]` retornando `None` em miss/expired
- [ ] 1.1.3 Implementar `cache_put(kind, key, content)` com atomic write (`.tmp` + rename)
- [ ] 1.1.4 Implementar `cache_get_error(kind, key) / cache_put_error(kind, key, status, ttl_days=7)` para cache de erros
- [ ] 1.1.5 Implementar `cache_clear(before_date=None, kinds=None) -> int` retornando numero de entradas removidas
- [ ] 1.1.6 Defaults de TTL: `TTL_DEFAULTS = {"pmid": 365, "pmcid": 365, "doi": 30, "pdf": 365, "errors": 7}`
- [ ] 1.1.7 Layout: `~/.cache/deep-research-sci/{kind}/{safe_key}.{ext}`; criar dirs lazy em put
- [ ] 1.1.8 Handle JSON corrupt: renomear para `.corrupt-{ts}.json` e retornar miss

**Verificacao:**
```bash
python -c "
from scripts.sci_fetch._cache import cache_put, cache_get
cache_put('pmid', '12345', 'hello world')
print(cache_get('pmid', '12345'))  # hello world
"
```

#### T1.2 — Criar `_token_bucket.py`
**Arquivos:** `scripts/sci_fetch/_token_bucket.py` (novo)
**Refs:** RF-11, RF-12, RF-15

- [ ] 1.2.1 Classe `TokenBucket(rate_per_sec, burst=None)` com `threading.Lock`
- [ ] 1.2.2 Metodo `acquire(tokens=1)` que dorme o minimo necessario; atomicamente refilla tokens baseado em `time.monotonic()`
- [ ] 1.2.3 Metodo `penalize(seconds: int)` que congela bucket zerando tokens + definindo `next_refill = now + seconds`
- [ ] 1.2.4 Factory `get_bucket(name: str) -> TokenBucket` com singletons pre-configurados:
  ```python
  BUCKETS = {
    "ncbi": TokenBucket(10 if os.environ.get("NCBI_API_KEY") else 3),
    "unpaywall": TokenBucket(5),
    "semantic_scholar": TokenBucket(10 if os.environ.get("SEMANTIC_SCHOLAR_API_KEY") else 1),
    "openalex": TokenBucket(10),
    "biorxiv": TokenBucket(2),
  }
  ```
- [ ] 1.2.5 Hook em `_http.py::fetch_with_retry()` que chama `penalize(retry_after)` ao detectar 429

**Verificacao:**
```bash
python evals/test_token_bucket.py  # (criado em T1.3)
```

#### T1.3 — Tests unitarios infra
**Arquivos:** `evals/test_cache_behavior.py`, `evals/test_token_bucket.py` (novos)

- [ ] 1.3.1 `test_cache_behavior.py`:
  - hit/miss basicos
  - TTL expiration (mock `os.path.getmtime`)
  - atomic write: kill-process-during-write simulado via `KeyboardInterrupt` no `.tmp`
  - concurrent write: 10 threads escrevendo mesmo key → last-writer-wins sem corrupcao
  - corrupt JSON handling
- [ ] 1.3.2 `test_token_bucket.py`:
  - 10 threads acquiring → contar req/s resultante, assertar <= rate
  - `penalize(5)` → acquire bloqueia ~5s
  - sem penalize, 3 acquires em <1s sem bloquear (burst)
- [ ] 1.3.3 Ambos rodam em <5s total

**Verificacao:**
```bash
python evals/test_cache_behavior.py && python evals/test_token_bucket.py
echo "Exit $?"  # 0 = pass
```

**Done Fase 1:** quando todos os 3 tasks fecham e tests passam.

---

### Fase 2: F6 Unpaywall-first — 2-3h

**Depende de:** T1.1 (cache para resposta Unpaywall)

#### T2.1 — Integrar cache em `unpaywall_resolver.py`
**Arquivos:** `scripts/sci_fetch/unpaywall_resolver.py`
**Refs:** RF-06 (TTL 30d DOI), RF-07 (error cache)

- [ ] 2.1.1 Antes de chamar API: `cached = cache_get("doi", safe_doi, ttl_days=30)`; se hit, retorna
- [ ] 2.1.2 Antes da API: check `cache_get_error("doi", safe_doi)` — se error recente (< 7d), retorna `{"is_oa": false}` sem bater API
- [ ] 2.1.3 Apos resposta: se `is_oa=true`, `cache_put("doi", ..., json_response)`; se `is_oa=false`, `cache_put_error("doi", ..., "not_oa")`
- [ ] 2.1.4 Throttle via `get_bucket("unpaywall").acquire()` antes do request

**Verificacao:**
```bash
# 1a chamada (cache miss) - deve bater API
time python scripts/sci_fetch/unpaywall_resolver.py "10.1089/thy.2014.0028"
# 2a chamada (cache hit) - deve ser instantanea (<50ms)
time python scripts/sci_fetch/unpaywall_resolver.py "10.1089/thy.2014.0028"
```

#### T2.2 — Refatorar `upload_to_nblm.py::_handle_doi()`
**Arquivos:** `scripts/sci_fetch/upload_to_nblm.py`
**Refs:** RF-01, RF-02, RF-03

- [ ] 2.2.1 Import `unpaywall_resolver`, `open_access_pdf`
- [ ] 2.2.2 Implementar funcao `_handle_doi(url, cls, work_dir) -> tuple[Path|None, str, dict]`:
  ```python
  def _handle_doi(url, cls, work_dir):
      doi = cls["metadata"]["doi"]
      canonical = f"doi:{doi}"
      try:
          result = unpaywall_resolver.resolve(doi, os.environ["UNPAYWALL_EMAIL"])
      except Exception as e:
          return None, canonical, {"reason": f"Unpaywall error: {e}"}
      if not result["is_oa"] or not result["oa_pdf_url"]:
          return None, canonical, {"reason": "DOI nao-OA no Unpaywall"}
      pdf_path = work_dir / f"doi_{_safe_slug(doi)}.pdf"
      try:
          open_access_pdf.fetch(result["oa_pdf_url"], out=pdf_path)
      except Exception as e:
          return None, canonical, {"reason": f"PDF fetch falhou: {e}", "unpaywall_url": result["oa_pdf_url"]}
      return pdf_path, canonical, {"unpaywall_host_type": result["host_type"]}
  ```
- [ ] 2.2.3 Substituir bloco `elif cls["type"] == "doi":` atual pela nova chamada
- [ ] 2.2.4 Manter fallback para manual bucket quando `_handle_doi` retorna `None, _, {reason: ...}`
- [ ] 2.2.5 No registro do manifesto: `ingest_method="pdf_upload"` quando sucesso, com `ingest_metadata={"unpaywall_host_type": ...}`

**Verificacao (manual):**
```bash
# Teste com DOI conhecido OA (Thyroid journal)
echo "https://doi.org/10.1089/thy.2014.0028" > /tmp/test_urls.txt
python scripts/sci_fetch/upload_to_nblm.py \
  --urls /tmp/test_urls.txt \
  --notebook test_nb \
  --pesquisa test \
  --pesquisas-root /tmp/pesquisas \
  --skip-upload  # nao tenta upload real, so fetch
# Deve ter arquivo em /tmp/pesquisas/test/fontes/sci_fetch/doi_10_1089_thy_2014_0028.pdf
```

#### T2.3 — Test integracao F6
**Arquivos:** `evals/test_doi_unpaywall.py` (novo, pequeno)

- [ ] 2.3.1 Test: DOI conhecido OA → retorna Path
- [ ] 2.3.2 Test: DOI nao-OA (ex: 10.1016/paywalled) → retorna None + reason
- [ ] 2.3.3 Test: DOI mock com is_oa=true mas oa_pdf_url=None → retorna None + reason

**Done Fase 2:** quando DOI OA vira source de arquivo no NotebookLM em vez de manual bucket.

---

### Fase 3: F8 Cache em handlers existentes — 2h

**Depende de:** T1.1

#### T3.1 — Cache em `pubmed_abstract.py`
**Arquivos:** `scripts/sci_fetch/pubmed_abstract.py`

- [ ] 3.1.1 Antes de `ncbi_throttle()`: `cached = cache_get("pmid", pmid, ttl_days=365)`; se hit, retorna imediatamente
- [ ] 3.1.2 Apos sucesso: `cache_put("pmid", pmid, formatted_output)`
- [ ] 3.1.3 Erro < 100 chars: `cache_put_error("pmid", pmid, "empty_abstract", ttl_days=7)` (evita re-bater)

#### T3.2 — Cache em `pmc_fulltext.py`
**Arquivos:** `scripts/sci_fetch/pmc_fulltext.py`

- [ ] 3.2.1 Cache hit: retorna tuple `(title, cached_text)` sem fetch
- [ ] 3.2.2 Cache miss + captcha detected (< 5000 chars): `cache_put_error("pmcid", pmcid, "captcha_or_redirect")`

#### T3.3 — Cache em `pmid_to_pmc.py`
**Arquivos:** `scripts/sci_fetch/pmid_to_pmc.py`

- [ ] 3.3.1 Cache da resposta elink por PMID individual (`{"12345": "PMC6789"}` ou `{"12345": null}`)
- [ ] 3.3.2 Em batch: primeiro filtrar cached, so bater API nos miss

#### T3.4 — Cache em `open_access_pdf.py`
**Arquivos:** `scripts/sci_fetch/open_access_pdf.py`

- [ ] 3.4.1 Key e `sha256(url)[:16]` (nao o URL raw, evita filenames longos)
- [ ] 3.4.2 Cache PUT gravando os bytes em `pdf/{key}.pdf`
- [ ] 3.4.3 Copia do cache path para `--out` solicitado pelo chamador

#### T3.5 — Flags CLI no orquestrador
**Arquivos:** `scripts/sci_fetch/upload_to_nblm.py`

- [ ] 3.5.1 Adicionar `--no-cache` (bypass total)
- [ ] 3.5.2 Adicionar `--invalidate-cache-before YYYY-MM-DD` (chama `cache_clear(before_date=...)`)
- [ ] 3.5.3 Se `--no-cache` setado: exportar env `DR_SCI_NO_CACHE=1` que os scripts respeitam

**Verificacao:**
```bash
# Cold run (cache vazio)
rm -rf ~/.cache/deep-research-sci
time python scripts/sci_fetch/pubmed_abstract.py 33567185
# Warm run (cache hit)
time python scripts/sci_fetch/pubmed_abstract.py 33567185  # <100ms
```

**Done Fase 3:** warm run 20x mais rapido que cold run em amostra de 10 PMIDs.

---

### Fase 4: F9 Paralelismo — 3-4h

**Depende de:** T1.2, todas as tasks de F3 (cache funcional antes de paralelizar)

#### T4.1 — Refatorar `upload_to_nblm.py` com pools
**Arquivos:** `scripts/sci_fetch/upload_to_nblm.py`
**Refs:** RF-13

- [ ] 4.1.1 Extrair logica do loop serial atual para funcoes `_handle_ncbi_worker(url, cls, upload_queue, manifest)`, `_handle_academic_worker(...)`, `_handle_generic_worker(...)`
- [ ] 4.1.2 Cada worker:
  1. Classify ja feito, receba pronto
  2. Fetch content (usando cache)
  3. `upload_queue.put(UploadTask(url, file_path|None, canonical, metadata))`
- [ ] 4.1.3 Orquestrador usa 3 `ThreadPoolExecutor` separados (max_workers: 3 ncbi, 3 academic, 5 generic) em `with ... as ...:` blocks aninhados
- [ ] 4.1.4 Coleta `as_completed` com try/except: erros agregados em `download_errors`, nao cancelam outros

#### T4.2 — Uploader thread + queue serial
**Arquivos:** `scripts/sci_fetch/upload_to_nblm.py`
**Refs:** RF-14

- [ ] 4.2.1 Funcao `_upload_worker(upload_queue, notebook_id, manifest_path, pesquisa_slug)` que faz `while True: task = queue.get(); if task is None: break; upload + record_manifest`
- [ ] 4.2.2 Uploader spawna em `threading.Thread`, nao em pool (single consumer)
- [ ] 4.2.3 Main envia sentinel `None` apos todos os futures completarem
- [ ] 4.2.4 `uploader.join()` antes de retornar summary

#### T4.3 — Flags F9
**Arquivos:** `scripts/sci_fetch/upload_to_nblm.py`
**Refs:** RF-16, RF-17

- [ ] 4.3.1 `--serial` — desativa pools, volta ao loop v1 (util para debug)
- [ ] 4.3.2 `--max-parallel N` — override de pool sizes (split: 30% ncbi, 30% academic, 40% generic)

#### T4.4 — Test stress paralelismo
**Arquivos:** `evals/test_parallel_fetching.py` (novo)

- [ ] 4.4.1 Fixture: 20 PMIDs conhecidos, mock do NotebookLM CLI
- [ ] 4.4.2 Rodar com `--max-parallel 9` (3+3+3)
- [ ] 4.4.3 Medir: tempo total, contagem de req NCBI em janela de 1s (nunca > rate limit), zero 429
- [ ] 4.4.4 Comparar tempo vs `--serial` — esperado 2.5x-3x speedup com 20 URLs

**Verificacao:**
```bash
python evals/test_parallel_fetching.py
```

**Done Fase 4:** 20 PMIDs em <1min com paralelismo vs ~2min serial, zero 429.

---

### Fase 5: v3 Academic APIs — 4-5h

**Depende de:** T1.1, T1.2

#### T5.1 — Criar `semantic_scholar.py`
**Arquivos:** `scripts/sci_fetch/semantic_scholar.py` (novo)
**Refs:** RF-18

- [ ] 5.1.1 Funcao `fetch(paper_id: str, use_cache=True) -> Optional[dict]`
- [ ] 5.1.2 Detecta prefix: se comeca com `10.`, prefixa `DOI:`; se so digitos, prefixa `PMID:`
- [ ] 5.1.3 Endpoint: `https://api.semanticscholar.org/graph/v1/paper/{prefixed_id}?fields=citationCount,influentialCitationCount,year,venue,tldr,authors.name,authors.hIndex`
- [ ] 5.1.4 Header `x-api-key: ...` se env `SEMANTIC_SCHOLAR_API_KEY` setada
- [ ] 5.1.5 Bucket `semantic_scholar`
- [ ] 5.1.6 Cache por `paper_id` com TTL 90d (citations nao mudam dramaticamente em <3 meses)
- [ ] 5.1.7 404 → retorna `None` silenciosamente (paper nao indexado)

**Verificacao:**
```bash
python scripts/sci_fetch/semantic_scholar.py "DOI:10.1089/thy.2014.0028"
# Espera JSON com citationCount, venue, etc.
```

#### T5.2 — Criar `openalex.py`
**Arquivos:** `scripts/sci_fetch/openalex.py` (novo)
**Refs:** RF-19

- [ ] 5.2.1 Endpoint: `https://api.openalex.org/works/doi:{doi}?mailto={OPENALEX_EMAIL}`
- [ ] 5.2.2 Parse `primary_location.source.h_index` → `venue_h_index`
- [ ] 5.2.3 Derivar `venue_quartile` via thresholds: Q1 > 50, Q2 20-50, Q3 5-20, Q4 < 5
- [ ] 5.2.4 Top 3 `concepts` ordenados por `score`, filtrar score > 0.7
- [ ] 5.2.5 Bucket `openalex`
- [ ] 5.2.6 Cache TTL 90d

#### T5.3 — Criar `biorxiv_fallback.py`
**Arquivos:** `scripts/sci_fetch/biorxiv_fallback.py` (novo)
**Refs:** RF-20

- [ ] 5.3.1 Funcao `find_preprint(doi: str) -> Optional[dict]`
- [ ] 5.3.2 Tenta `https://api.biorxiv.org/details/biorxiv/{doi}`; se miss, tenta `medrxiv/{doi}`
- [ ] 5.3.3 Retorna preprint mais recente (maior `version`); fields: `preprint_doi`, `pdf_url`, `preprint_server`, `version`, `posted_date`
- [ ] 5.3.4 Validar `pdf_url` com HEAD request antes de retornar (evita URLs mortos)
- [ ] 5.3.5 Bucket `biorxiv`
- [ ] 5.3.6 Cache TTL 30d (preprints podem ter nova versao)

#### T5.4 — Tests v3 APIs
**Arquivos:** `evals/test_v3_apis.py` (novo)

- [ ] 5.4.1 Smoke tests com 1 DOI conhecido para cada API (contra APIs reais, sem mock, para pegar breakage de schema)
- [ ] 5.4.2 Handling de 404/erro (paper nao indexado em S2/OA)
- [ ] 5.4.3 Cache hit apos 1o fetch

**Done Fase 5:** 3 clientes funcionais, cacheados, rate-limited.

---

### Fase 6: v3 Scorer + integracao — 3-4h

**Depende de:** T5.1, T5.2, T5.3

#### T6.1 — Criar `paper_scorer.py`
**Arquivos:** `scripts/sci_fetch/paper_scorer.py` (novo)
**Refs:** RF-21

- [ ] 6.1.1 Funcao `score_paper(doi=None, pmid=None) -> dict` retornando schema de RF-21
- [ ] 6.1.2 Chamar `semantic_scholar.fetch()` e `openalex.fetch()` em paralelo (threading, pequeno inner pool)
- [ ] 6.1.3 Formula documentada em RF-21:
  ```python
  age_years = max(1, current_year - paper_year)
  citations_per_year = citation_count / age_years
  base = min(50, citations_per_year * 3)
  influential_bonus = min(20, influential_citations * 0.5)
  venue_bonus = {"Q1": 20, "Q2": 10, "Q3": 5, "Q4": 0}[quartile]
  preprint_bonus = 10 if (preprint_available and age_years < 2) else 0
  recency_bonus = 10 if (age_years < 3 and citations_per_year > 5) else 0
  score = min(100, base + influential_bonus + venue_bonus + preprint_bonus + recency_bonus)
  tier = 1 if score >= 70 else (2 if score >= 40 else 3)
  ```
- [ ] 6.1.4 Rationale gerado rule-based: identifica sinal dominante (maior contribuicao ao score) + idade + venue
- [ ] 6.1.5 Handle missing data: se S2 404 mas OA ok, usa so OA; se ambos 404, retorna `{"tier": "unknown", "signals": {}, "rationale": "not indexed in academic graphs"}`

**Verificacao:**
```bash
python scripts/sci_fetch/paper_scorer.py --doi "10.1089/thy.2014.0028"
# Espera JSON com score, tier, signals, rationale
```

#### T6.2 — Integrar scorer na Fase 4.5
**Arquivos:** `scripts/sci_fetch/upload_to_nblm.py`
**Refs:** RF-22, RF-24

- [ ] 6.2.1 Apos classificacao, para URLs cientificas (pubmed/pmc/doi), scorer roda em paralelo ao fetching
- [ ] 6.2.2 Resultado do scorer anexado ao `UploadTask` e ao manifesto (`ingest_metadata.academic_score`, `.academic_tier`)
- [ ] 6.2.3 Flag `--skip-scoring` bypassa tudo, volta ao tiering v1 heuristico

#### T6.3 — bioRxiv fallback automatico
**Arquivos:** `scripts/sci_fetch/upload_to_nblm.py`

- [ ] 6.3.1 Em `_handle_doi()`: se Unpaywall `is_oa=false`, tenta `biorxiv_fallback.find_preprint(doi)`
- [ ] 6.3.2 Se preprint encontrado: baixa PDF via `open_access_pdf.py`; registra `ingest_method="pdf_upload"` com `ingest_metadata.preprint_server` e `.preprint_version`

#### T6.4 — Template academic-ranking-report.md
**Arquivos:** `assets/templates/academic-ranking-report.md` (novo)
**Refs:** RF-23

- [ ] 6.4.1 Secao inserida no final do PESQUISA-*.md apos a secao nblm-upload-report
- [ ] 6.4.2 Tabela: Tier | Titulo | Venue | Year | Citations/yr | Infl.Cit. | Score | Rationale
- [ ] 6.4.3 Papers ordenados por score desc

#### T6.5 — Test scorer com fixtures reais
**Arquivos:** `evals/test_paper_scorer.py` (novo)

- [ ] 6.5.1 Fixture: 10 papers da pesquisa farmacologia (mix de venues, anos, citacoes)
- [ ] 6.5.2 Score cada um, assertar tiering faz sentido: Nature/NEJM → tier 1; MDPI recente sem citacoes → tier 3
- [ ] 6.5.3 Comparar com tiering v1 (heuristico): overlap top-5 <= 40% (epic E4 hypothesis)

**Done Fase 6:** scorer produz tiers coerentes em 2 dominios (farmacologia + 1 outro, ex: Next.js/tech).

---

### Fase 7: Docs + templates + SKILL.md — 2-3h

**Depende de:** F2-F6 implementadas

#### T7.1 — `references/cache-and-rate-limits.md`
**Arquivos:** `references/cache-and-rate-limits.md` (novo)

- [ ] 7.1.1 Layout do cache + TTL por tipo + exemplos de uso da API
- [ ] 7.1.2 Token bucket: quando cada API dispara, rate limits publicos, o que acontece em 429
- [ ] 7.1.3 Troubleshooting: "cache cheio" (`--invalidate-cache-before`), "ban em NCBI" (configurar key), "paralelismo quebra algo" (`--serial`)

#### T7.2 — `references/academic-scoring.md`
**Arquivos:** `references/academic-scoring.md` (novo)

- [ ] 7.2.1 3 APIs: o que cada uma fornece, rate limits, env vars
- [ ] 7.2.2 Formula do scorer explicada com exemplos numericos
- [ ] 7.2.3 Interpretacao de tiers: quando Tier 1 e confiavel, quando "unknown" aparece, como debugar um score surpreendente

#### T7.3 — Atualizar SKILL.md
**Arquivos:** `SKILL.md`

- [ ] 7.3.1 Adicionar subsecao "Otimizacoes v2" na Fase 4.5 (referenciando novos references)
- [ ] 7.3.2 Adicionar flags novas na tabela de flags
- [ ] 7.3.3 Adicionar env vars novas (`SEMANTIC_SCHOLAR_API_KEY`, `OPENALEX_EMAIL`)
- [ ] 7.3.4 Atualizar tabela de reference files
- [ ] 7.3.5 Manter linhas <= 700 (objetivo: refatorar outras secoes se passar)

#### T7.4 — Atualizar `references/sci-pipeline.md`
**Arquivos:** `references/sci-pipeline.md`

- [ ] 7.4.1 Adicionar secao "v2 additions" com: Unpaywall-first flow, cache layer, paralelismo, scorer
- [ ] 7.4.2 Atualizar fluxograma do ciclo de vida de uma URL para refletir F6, F8, F9, v3

**Done Fase 7:** docs cobrem todas as features novas; qualquer usuario leigo consegue configurar e rodar.

---

### Fase 8: Regression + close-out — 2h

**Depende de:** F1-F7

#### T8.1 — Regression test: re-executar pesquisa farmacologia
**Arquivos:** nenhum novo; usa fixtures de `~/.claude/skills/research/pdfs/` e `evals/test_urls_pharmacology.json` expandido com mais URLs

- [ ] 8.1.1 Pegar as 86 URLs da pesquisa original 2026-04-22 (extrair da `~/.claude/skills/research/pdfs/` + PRD v1)
- [ ] 8.1.2 Rodar `upload_to_nblm.py` com notebook novo dedicado a regression
- [ ] 8.1.3 Medir:
  - Sucesso NotebookLM total (>=95% esperado)
  - DOIs convertidos via Unpaywall (>=60% esperado)
  - Tempo total p95 (<=2.5min esperado em 50 URLs ou <=5min em 86)
  - HTTP 429 events (=0 esperado)
  - Cache hits em 2a rodada (>=80%)
- [ ] 8.1.4 Salvar resultados em `evals/regression-v2-2026-XX-XX.json`

#### T8.2 — Comparacao v1 vs v2
**Arquivos:** `evals/regression-v1-vs-v2.md` (novo)

- [ ] 8.2.1 Tabela lado-a-lado das metricas baseline vs v2
- [ ] 8.2.2 Analise qualitativa: tier 1 papers v1 vs v2 (quantos overlap?)
- [ ] 8.2.3 Dor residual: URLs que ainda vao para manual bucket mesmo com v2

#### T8.3 — Atualizar ROADMAP + memoria
**Arquivos:** `ROADMAP.md` no repo, `MEMORY.md` + novo `project_deep_research_sci_pipeline_v2.md`

- [ ] 8.3.1 ROADMAP: deep-research atualiza para v2026-XX-XX com resumo das mudancas
- [ ] 8.3.2 Memoria: novo projeto file com metricas v1→v2 medidas, decisoes que mudaram no caminho, gaps remanescentes
- [ ] 8.3.3 MEMORY.md index atualizado

#### T8.4 — Install + sync
**Arquivos:** toda a skill

- [ ] 8.4.1 Copiar `~/.claude/skills/deep-research/` para Claude Desktop
- [ ] 8.4.2 Copiar para `skills/deep-research/` no repo
- [ ] 8.4.3 Rodar DoD grep: zero deprecated IDs, zero budget_tokens, zero sampling hardcoded
- [ ] 8.4.4 Smoke test: `python scripts/sci_fetch/classify_url.py --batch evals/test_urls_pharmacology.json` retorna 26/26 PASS

**Done Fase 8:** v2 shipped com metricas medidas e documentadas.

---

## Ordem recomendada de commits

```
commit 1: T1.1 _cache.py + T1.2 _token_bucket.py + T1.3 tests (Fase 1 toda)
commit 2: T2.1 cache em unpaywall + T2.2 refactor _handle_doi + T2.3 tests (Fase 2)
commit 3: T3.1-T3.4 cache em handlers existentes (Fase 3 parcial)
commit 4: T3.5 flags CLI de cache (close Fase 3)
commit 5: T4.1 + T4.2 pools e uploader (core Fase 4)
commit 6: T4.3 flags + T4.4 stress test (close Fase 4)
commit 7: T5.1 semantic_scholar (isolado)
commit 8: T5.2 openalex (isolado)
commit 9: T5.3 biorxiv_fallback (isolado)
commit 10: T5.4 tests v3 APIs
commit 11: T6.1 paper_scorer
commit 12: T6.2 + T6.3 integracao + bioRxiv fallback
commit 13: T6.4 template + T6.5 tests scorer
commit 14: T7.1-T7.4 docs
commit 15: T8.1 regression + T8.2 comparacao
commit 16: T8.3 + T8.4 close-out
```

16 commits atomicos. Cada um deixa a skill em estado funcional (nada quebrado em meio).

---

## Done Global (match com PRD v2 secao 12)

- [ ] Todos os 8 "Done Fase N" fecharam
- [ ] Regression test: >=95% sucesso, >=60% DOIs OA, <=2.5min p95 para 50 URLs
- [ ] Cache hit rate >=80% em delta simulado
- [ ] Zero HTTP 429 em corrida tipica
- [ ] Scorer valida em 2+ dominios
- [ ] Flags `--serial`, `--no-cache`, `--skip-scoring` degradam graciosamente
- [ ] SKILL.md + 2 novos references atualizados
- [ ] DoD grep CLEAN (zero deprecated IDs / budget_tokens / sampling)
- [ ] Instalada Claude Code + Desktop + repo
- [ ] ROADMAP.md e memoria atualizados
