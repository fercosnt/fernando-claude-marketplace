# Cache & Rate Limits — reference

Documentação operacional do cache local (`_cache.py`) e token bucket (`_token_bucket.py`) da Fase 4.5 v2 do deep-research.

**Leia quando:**
- A Fase 4.5 está acionada e você precisa entender *por que* um PMID respondeu em 40ms (cache hit) ou 800ms (cache miss)
- Apareceu HTTP 429 num log e você precisa saber o que penalizou o bucket
- O usuário reclama "está re-baixando tudo" em delta research (cache inválido ou desligado)
- Vai estender o pipeline com uma API nova e precisa do padrão de integração

---

## 1. Cache local — layout & TTL

Localização default: `~/.cache/deep-research-sci/`
Override: env `DR_SCI_CACHE_ROOT=/caminho/custom`
Kill-switch: env `DR_SCI_NO_CACHE=1` (get sempre `None`, put no-op)

### Layout

```
~/.cache/deep-research-sci/
├── pmid/33567185.txt                    # abstract formatado (TTL 365d)
├── pmcid/PMC7054893.json                # {"title": "...", "text": "..."} (TTL 365d)
├── pmc_link/33567185.json               # {"pmcid": "PMC7054893" | null} (TTL 365d)
├── doi/10.1089_thy.2014.0028.json       # resposta Unpaywall (TTL 30d)
├── pdf/<sha256-16>.pdf                  # PDF baixado (TTL 365d, key = sha256(url)[:16])
├── s2/doi_10.1089_thy.2014.0028.json    # resposta Semantic Scholar (TTL 90d)
├── openalex/10.1089_thy.2014.0028.json  # resposta OpenAlex (TTL 90d)
├── biorxiv/10.1101_2024.01.15.json      # resposta bioRxiv/medRxiv (TTL 30d)
└── errors/
    ├── doi/10.1089_xyz.json             # {"status": "not_oa", ...} (TTL 7d)
    ├── pmcid/PMC9999999.json            # {"status": "captcha_or_redirect", ...} (TTL 7d)
    └── s2/DOI_10.xxx.json               # {"status": "not_found", ...} (TTL 7d)
```

### TTL por kind (de `TTL_DEFAULTS` em `_cache.py`)

| Kind | TTL default | Racional |
|---|---|---|
| `pmid` | 365d | PMID metadata + abstract efetivamente imutável após publicação |
| `pmcid` | 365d | Full-text final estável; retraction é rara e pega re-run manual |
| `pmc_link` | 365d | Mapeamento PMID→PMCID via elink é estável (PubMed congela o match) |
| `pdf` | 365d | Bytes do PDF; chave é sha256(url) → URL mudar força refetch |
| `doi` | 30d | Resposta Unpaywall pode mudar (editor libera OA, embargo expira) |
| `s2` | 90d | Citation count cresce, mas dramaticamente pouco em 3 meses |
| `openalex` | 90d | Mesmo raciocínio que S2 — sinais de venue/cited_by estáveis em 90d |
| `biorxiv` | 30d | Preprints podem ter novas versões (v1→v2→v3) — curto TTL força refresh |
| `errors` | 7d | Retry semanal para 429 transiente, captcha, 503; evita spam em API |

**Regra geral:** TTL curto = refresh mais agressivo, TTL longo = menos tráfego mas risco de stale. `errors` é deliberadamente curto para não cimentar falhas transientes.

### API pública (`_cache.py`)

```python
from scripts.sci_fetch import _cache

# Hit normal (texto)
text = _cache.cache_get("pmid", "33567185", ttl_days=365)  # str | None

# Hit normal (binário, ex: PDF)
pdf_bytes = _cache.cache_get("pdf", sha_key, ttl_days=365, binary=True)  # bytes | None

# Put (texto ou JSON)
_cache.cache_put("pmid", "33567185", formatted_text)
_cache.cache_put("s2", "DOI_10.xxx", {"citationCount": 156, ...})  # auto-JSON

# Put (binário)
_cache.cache_put("pdf", sha_key, pdf_bytes, binary=True)

# JSON helper (dict ou None)
data = _cache.cache_get_json("openalex", safe_doi)

# Error cache — evita bater API 3x na mesma sessão em paper já 404'd
_cache.cache_put_error("s2", "DOI_10.xxx", "not_found", extra={"checked_at": "..."})
err = _cache.cache_get_error("s2", "DOI_10.xxx")  # dict | None

# Clear programático
_cache.cache_clear(before_date=timestamp, kinds=["doi", "s2"])  # int removidos
```

**Garantias de I/O:**
- Atomic write via `tempfile.mkstemp(dir=path.parent)` + `os.fsync` + `os.replace` — duas threads gravando o mesmo key nunca produzem arquivo corrompido
- JSON corrupto (decode falha) é renomeado para `.corrupt-<ts>` e tratado como miss — próximo put sobrescreve, não quebra o pipeline
- `mkdir(parents=True, exist_ok=True)` lazy em cada put — não precisa bootstrap

### CLI (`python -m scripts.sci_fetch._cache`)

```bash
# Estatísticas: files + size por kind + total
python -m scripts.sci_fetch._cache stats

# Exemplo de output:
# {
#   "root": "/Users/fernando/.cache/deep-research-sci",
#   "kinds": {
#     "pmid": {"files": 47, "size": "1.2MB"},
#     "pmcid": {"files": 31, "size": "8.4MB"},
#     "pdf": {"files": 52, "size": "124MB"}
#   },
#   "errors": {"files": 8, "size": "2.1KB"},
#   "total": {"files": 138, "size": "133.6MB"}
# }

# Clear seletivo
python -m scripts.sci_fetch._cache clear --before 2026-01-01
python -m scripts.sci_fetch._cache clear --kind s2 --kind openalex
python -m scripts.sci_fetch._cache clear  # apaga TUDO
```

### CLI do orquestrador (flags v2)

```bash
# Bypass total — não lê nem grava cache (debug)
python scripts/sci_fetch/upload_to_nblm.py --urls urls.txt --notebook NB --no-cache ...

# Invalida entradas antigas antes de rodar (delta research com retrospectiva limpa)
python scripts/sci_fetch/upload_to_nblm.py --invalidate-cache-before 2026-01-01 ...
```

`--no-cache` exporta `DR_SCI_NO_CACHE=1` — todos os scripts em sci_fetch respeitam.

---

## 2. Token bucket — coordenação de rate limits

Stdlib-only (`threading.Lock` + `time.monotonic`). Algoritmo leaky bucket clássico: tokens enchem a `rate_per_sec`, capacidade default = `ceil(rate)` (permite burst inicial pequeno). Singletons por nome via `get_bucket(name)`.

### Buckets pré-configurados (de `_default_rate()`)

| Bucket | Rate default | Rate com API key | Origem |
|---|---|---|---|
| `ncbi` | 3 req/s | 10 req/s (com `NCBI_API_KEY`) | NCBI E-utilities limit oficial |
| `unpaywall` | 5 req/s | — | Unpaywall polite convention |
| `semantic_scholar` | 1 req/s | 10 req/s (com `SEMANTIC_SCHOLAR_API_KEY`) | S2 Graph API public tier |
| `openalex` | 10 req/s | — (polite pool via `OPENALEX_EMAIL`) | OpenAlex documented limit |
| `biorxiv` | 2 req/s | — | bioRxiv API não tem limit oficial — valor conservador |

### Como integrar em um novo handler

```python
from scripts.sci_fetch._token_bucket import get_bucket, handle_429

def fetch_something(doi):
    bucket = get_bucket("openalex")  # lazy singleton
    bucket.acquire()                 # bloqueia até ter token disponível
    resp = urllib.request.urlopen(url)
    if resp.status == 429:
        handle_429("openalex", retry_after=60)  # congela bucket inteiro por 60s
        raise RuntimeError("rate limited")
    return parse(resp)
```

### Mecanismo de 429 global

Quando uma thread recebe 429, chama `handle_429(bucket_name, retry_after)`:

1. `bucket.penalize(retry_after)` zera tokens + define `penalty_until = now + retry_after`
2. Todas as outras threads chamando `acquire()` no mesmo bucket param de consumir tokens e dormem até `penalty_until`
3. Após o penalty expirar, tokens começam a refillar normalmente

**Por que global em vez de per-thread:** o 429 é informação sobre o *servidor*, não sobre a thread. Se thread A viu ban, thread B que ainda não disparou também deve esperar — caso contrário o ban se prolonga.

### Observabilidade

```bash
# Estado atual dos buckets (criados lazy — só mostra os que foram tocados)
python -m scripts.sci_fetch._token_bucket

# Output:
# {
#   "ncbi": {"name": "ncbi", "rate_per_sec": 10.0, "capacity": 10, "tokens": 8.3, "penalty_remaining": 0.0},
#   "semantic_scholar": {"name": "semantic_scholar", "rate_per_sec": 1.0, "capacity": 1, "tokens": 1.0, "penalty_remaining": 0.0}
# }
```

`penalty_remaining > 0` indica bucket em backoff — um 429 recente.

---

## 3. Troubleshooting

### "Cache está cheio" (disk > 1GB)

```bash
# Inspecionar o que cresceu
python -m scripts.sci_fetch._cache stats

# PDFs são os mais pesados — limpar seletivamente
python -m scripts.sci_fetch._cache clear --kind pdf --before 2026-01-01

# Ou limpar tudo e começar do zero (próxima pesquisa repovoa conforme demanda)
python -m scripts.sci_fetch._cache clear
```

Cache foi dimensionado para crescer ~50-200MB por pesquisa científica grande (50-100 PDFs). Se passar de 1GB sem razão clara, `stats` vai mostrar qual kind acumulou — geralmente `pdf` depois de muitas pesquisas.

### "HTTP 429 NCBI ban"

Causa mais comum: rodando sem `NCBI_API_KEY` com paralelismo agressivo (`--max-parallel 20`). Rate sem key é 3 req/s — 20 workers saturam em <1s.

**Fix:**
1. Configurar key (5 min em https://www.ncbi.nlm.nih.gov/account/settings/) → `export NCBI_API_KEY=...` sobe rate para 10 req/s
2. Ou reduzir paralelismo: `--max-parallel 3` até ter key

O bucket penaliza globalmente em 429 — mesmo que o orquestrador siga tentando, as chamadas param até o penalty expirar. Sem ação do usuário, o pipeline se auto-regula.

### "Paralelismo quebrou X"

Se `--max-parallel` está causando instabilidade (upload race no NotebookLM, manifesto conflitando apesar do lock, timeout em API externa), voltar para serial:

```bash
python scripts/sci_fetch/upload_to_nblm.py --urls urls.txt --serial ...
```

`--serial` desliga os 3 `ThreadPoolExecutor` e o uploader thread — volta ao loop v1. Mais lento (~2-3x em 20 URLs) mas determinístico para debug.

### "JSON cache renomeado para .corrupt-XXX"

Sintoma: arquivo no cache com sufixo `.corrupt-1730000000.json`. Causa: put interrompido no meio (Ctrl+C durante fsync, disk full, signal).

**Ação necessária:** nenhuma. Próximo `cache_get` dá miss, próximo `cache_put` sobrescreve o arquivo "limpo". Os `.corrupt-*` podem ser removidos manualmente se quiser reclaim de disco:

```bash
find ~/.cache/deep-research-sci -name "*.corrupt-*" -delete
```

### "Unpaywall retorna sempre is_oa=false e nunca refaz"

Error cache do `doi` kind tem TTL 7d. Se um editor liberou OA ontem mas seu cache ainda diz `not_oa` de ontem anteontem, o resultado antigo persiste até o TTL expirar.

**Fix rápido:**
```bash
# Força re-check de DOIs recentes (últimos 7 dias de erros)
python -m scripts.sci_fetch._cache clear --kind doi --before $(date -v-7d +%Y-%m-%d)

# Ou bypass na próxima rodada
python scripts/sci_fetch/upload_to_nblm.py --no-cache ...
```

### "Scorer retorna `tier: unknown` mas sei que o paper tem citações"

Dois cenários:
1. Paper não indexado em S2 E OpenAlex (raro mas acontece — preprints novos, conference papers específicos)
2. `SEMANTIC_SCHOLAR_API_KEY` não setada + burst de pedidos → rate limited → error cache + 7d sem retry

Validar com CLI direto:
```bash
python scripts/sci_fetch/semantic_scholar.py "DOI:10.xxx/xyz"
python scripts/sci_fetch/openalex.py "10.xxx/xyz"
```

Se ambos retornam dados, o scorer deveria ter pego. Verificar `~/.cache/deep-research-sci/errors/s2/` e `openalex/` — deletar os errors stale e re-rodar.

### "Quero forçar refresh de tudo mesmo sem TTL expirado"

```bash
# Nuclear: apaga cache inteiro
python -m scripts.sci_fetch._cache clear

# Cirúrgico: bypass só nesta rodada
python scripts/sci_fetch/upload_to_nblm.py --no-cache ...

# Preciso: entradas antes de uma data
python scripts/sci_fetch/upload_to_nblm.py --invalidate-cache-before 2026-01-01 ...
```

---

## 4. Quando NÃO cachear

A skill cacheia tudo que é determinístico (mesma URL → mesmo conteúdo). Alguns casos explicitamente não são cacheados:

- **Endpoints autenticados** — Google/NotebookLM CLI tem sessão própria, não passa por sci_fetch
- **URLs generic** (gov/blog/news) — vão direto para `notebooklm source add <url>` que scraper server-side. Conteúdo pode mudar (notícias), TTL seria complicado
- **Classificação de URL** — `classify_url.py` é O(regex), não precisa de cache
- **Manifesto `_notebook-manifest.json`** — tem file lock próprio e é append-mostly; cache causaria inconsistência
- **Progresso da rodada atual** — erros da sessão não são persistidos para a próxima (error cache é para API, não para estado)

---

## 5. Quick reference — integrando um novo handler

Template mínimo para adicionar um endpoint novo que se beneficia de cache + rate limit:

```python
from scripts.sci_fetch import _cache
from scripts.sci_fetch._token_bucket import get_bucket, handle_429

BUCKET = "my_api"  # adicionar em _default_rate() se quiser singleton customizado
CACHE_KIND = "my_api"  # adicionar em TTL_DEFAULTS + EXT_BY_KIND

def fetch(key: str, use_cache: bool = True):
    if use_cache:
        cached = _cache.cache_get_json(CACHE_KIND, key)
        if cached is not None:
            return cached
        err = _cache.cache_get_error(CACHE_KIND, key)
        if err is not None:
            return None  # known-bad, skip API

    get_bucket(BUCKET).acquire()
    try:
        resp = _http.fetch(url)
    except HTTPError as e:
        if e.code == 429:
            handle_429(BUCKET, retry_after=60)
            raise
        if e.code == 404:
            if use_cache:
                _cache.cache_put_error(CACHE_KIND, key, "not_found")
            return None
        raise

    data = parse(resp)
    if use_cache:
        _cache.cache_put(CACHE_KIND, key, data)
    return data
```

Referências vivas: `semantic_scholar.py`, `openalex.py`, `biorxiv_fallback.py` seguem exatamente este padrão.
