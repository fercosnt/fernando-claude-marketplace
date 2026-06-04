# NotebookLM Manifest — schema e regras

Detalhamento de `_notebook-manifest.json` — o audit trail que rastreia todo source enviado ao NotebookLM. Leia quando:

- Esta implementando uma nova fase que escreve no NotebookLM
- Precisa entender como o dedup funciona
- Vai construir a `notebook-source-auditor` (futura skill)

## Localizacao

```
{pesquisas_root}/_notebook-manifest.json
```

Um por projeto (pasta `pesquisas/`). **Nunca** global em `~/`. Razao: o manifesto cataloga todas as pesquisas E todos os notebooks de um projeto coeso, permitindo reuso entre pesquisas relacionadas.

## Schema completo

```json
{
  "version": 1,
  "notebooks": {
    "<notebook_id>": {
      "title": "Nome do notebook no NotebookLM",
      "created_at": "ISO-8601",
      "updated_at": "ISO-8601",
      "pesquisas": [
        {
          "slug": "prd-4-avaliacao-bibliografia",
          "path": "pesquisas/prd-4-avaliacao-bibliografia",
          "added_at": "ISO-8601",
          "last_delta_at": "ISO-8601"
        }
      ],
      "sources": [
        {
          "canonical_key": "doi:10.1234/xyz",
          "title": "Titulo da fonte",
          "type": "article|url|youtube|pdf",
          "origin_pesquisa": "prd-4-avaliacao-bibliografia",
          "added_at": "ISO-8601",
          "status": "ok|captcha_pending|failed|skipped",
          "last_attempt_at": "ISO-8601",
          "attempts": 1,
          "notebooklm_source_id": "<id retornado pelo NotebookLM>",
          "ingest_method": "url_direct|pdf_upload|captcha_bypass_flow_v1",
          "ingest_metadata": {
            "original_url": "https://...",
            "pdf_local_path": "/tmp/xyz.pdf",
            "captcha_bypass_version": "v1"
          },
          "last_error": "optional, only when status=failed"
        }
      ]
    }
  }
}
```

## Canonical key — prioridade de dedup

Ordem fixa (primeiro que existir):

1. **DOI** → `doi:10.1089/thy.2014.0028`
2. **PMC ID** → `pmc:PMC7054893`
3. **PubMed ID** → `pmid:12345`
4. **URL normalizada** → `url:https://example.com/foo?id=1`
5. **SHA256 do PDF** → `sha256:abc123...`
6. **titulo + primeiro autor** (ultimo recurso) → `title:creatine+kreider`

Razao para priorizar DOI: dois URLs diferentes (publisher + preprint) apontam para o mesmo paper — o DOI e a verdade canonica.

## URL normalization (para canonical_key=url:)

Regras aplicadas por `notebook_manifest.normalize_url()`:

- Lowercase `scheme` + `host` (`HTTPS://Example.COM` → `https://example.com`)
- Remove trailing slash (`/foo/` → `/foo`), exceto para a raiz (`/` mantem)
- Path CASE-SENSITIVE preservado (`/Foo/Bar` != `/foo/bar` em muitos servers)
- Remove params de tracking: todos que comecam com `utm_`, + `fbclid`, `gclid`, `msclkid`, `dclid`, `yclid`, `mc_cid`, `mc_eid`, `ref`, `ref_src`, `source`, `igshid`, `s_cid`, `spm`, `_hsenc`, `_hsmi`, `hsCtaTracking`
- Drop `#fragment` exceto semanticos: `#page=5`, `#section-intro`, `#sec-3` (util em PDFs)
- Portas nao-default preservadas

Exemplos:

| Input | Normalized |
|---|---|
| `https://example.com/foo/?utm_source=x&real=1` | `https://example.com/foo?real=1` |
| `HTTPS://Example.com/Foo/Bar/` | `https://example.com/Foo/Bar` |
| `https://pubmed.ncbi.nlm.nih.gov/12345/?fbclid=abc` | `https://pubmed.ncbi.nlm.nih.gov/12345` |
| `https://paper.pdf#page=5` | `https://paper.pdf#page=5` |
| `https://paper.pdf#random-anchor` | `https://paper.pdf` |

## ingest_method — como foi adicionado

| Valor | Significado | Auditor retry? |
|-------|-------------|----------------|
| `url_direct` | Scraper do NotebookLM pegou o URL | Sim — re-tentar URL |
| `pdf_upload` | Arquivo local foi upload via CLI | Sim — re-subir arquivo se existe em `pdf_local_path` |
| `captcha_bypass_flow_v1` | Usuario fez o bypass manual (browser → download → arrastar) | Nao — requer mao humana |

`ingest_metadata` deve sempre conter `original_url` para audit. Outros campos dependem do `ingest_method`.

## status — estados validos

| status | Quando usar |
|--------|-------------|
| `ok` | Upload confirmado, source_id retornado |
| `captcha_pending` | CAPTCHA apareceu; usuario pode tentar bypass manual |
| `failed` | Erro permanente (paywall, DOI invalido, URL morta); preencher `last_error` |
| `skipped` | Intencionalmente pulado (ex: `--skip-upload` em run de teste) |

## Regras de escrita (enforced pelo helper)

1. **Bootstrap automatico:** se `_notebook-manifest.json` nao existir, `record_source()` cria com `{"version": 1, "notebooks": {}}` antes do primeiro write
2. **File lock com PID:** lockfile `_notebook-manifest.json.lock` contem PID; se o PID esta morto (stale lock), o helper reclama automaticamente. Evita corrupcao em runs paralelos de `deep-research`
3. **Atomic write:** helper escreve em `.tmp` + `os.rename()`, nao abre o arquivo original para escrita
4. **Upsert, nunca re-add:** se `canonical_key` ja existe, incrementa `attempts`, atualiza `last_attempt_at`/`status`, merges `ingest_metadata`
5. **Nunca remova entradas:** mesmo sources que falharam ficam no manifesto. Remocao e responsabilidade exclusiva da futura `notebook-source-auditor`
6. **pesquisas[] cresce incrementalmente:** cada chamada `record_source()` toca `last_delta_at` da pesquisa-origem

## Patterns comuns

### Checar se fonte ja foi enviada antes de re-tentar
```python
from notebook_manifest import lookup_source, normalize_url
from pathlib import Path

manifest = Path("pesquisas/_notebook-manifest.json")
existing = lookup_source(manifest, notebook_id, canonical_key="doi:10.1089/thy.2014.0028")
if existing and existing["status"] == "ok":
    print("ja enviada, pular")
elif existing and existing["attempts"] >= 3:
    print("muitas tentativas, pedir humano")
else:
    # tentar enviar
    ...
```

### Sumario CLI
```bash
python scripts/notebook_manifest.py show pesquisas/
# → {"version": 1, "notebooks": {"nb_abc": {"title": "...", "source_count": 42, "by_status": {"ok": 38, "failed": 4}}}}
```

### Inicializar explicitamente (opcional — helper auto-bootstrap tambem)
```bash
python scripts/notebook_manifest.py init pesquisas/
```

## Integracao com pesquisas paralelas

Se duas pesquisas rodam em paralelo (ex: tmux com duas sessoes de `deep-research`), ambas chamam `record_source()` contra o mesmo `_notebook-manifest.json`. O file lock com timeout de 30s garante que as escritas serialize sem corrupcao.

Se o lock esta preso por 30s (edge case: terminal crashed), o proximo caller detecta PID morto e reclama o lock.

## Failure modes

| Cenario | Comportamento |
|---------|---------------|
| Disk full | `record_source()` levanta OSError; capture, logue, continue sem bloquear pesquisa |
| Manifesto corrompido (JSON invalido) | `_load_or_bootstrap` levanta `RuntimeError`; renomear para `.corrupt-<timestamp>.json` e deixar helper recriar |
| Lock expirado mas PID ainda vivo (false stale) | Improvavel; se acontecer, timeout de 30s leva a `TimeoutError` explicito |
| Concorrencia extrema (10+ writers) | Lock serializa, throughput cai; mitigacao: pesquisas nao devem ser rodadas em batch > 3 em paralelo |

## Como a futura notebook-source-auditor deve ler

1. `python scripts/notebook_manifest.py show <root>` para listar notebooks
2. Para cada notebook, detectar sources com `status in ("failed", "captcha_pending")` ha > X dias
3. Por `ingest_method`, decidir ação:
   - `url_direct` → re-tentar com `notebooklm source add <url>`
   - `pdf_upload` → re-tentar com `ingest_metadata.pdf_local_path` se existe
   - `captcha_bypass_flow_v1` → listar para o usuario, apenas ele resolve
4. Remover entradas de sources que foram deletadas do NotebookLM (sync inverso)

## Por que este formato (e nao SQLite, CSV, etc.)

- **JSON:** git-friendly (diff legivel), inspecionavel a olho nu, sem dependencias
- **Arquivo unico:** nao assume cluster, funciona em macOS/Linux nu
- **Versionado (`"version": 1`):** permite evolucao de schema; o helper sabe migrar quando `version` subir
