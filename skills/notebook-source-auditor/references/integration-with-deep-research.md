# Integration with deep-research

Esta skill **compartilha scripts** com `deep-research` mas **nao invoca** a deep-research diretamente (e vice-versa). As duas skills sao consumidoras do mesmo executor compartilhado.

## Mapa de dependencias

```
~/.claude/skills/deep-research/scripts/
├── notebook_manifest.py          ← usado por AMBAS
│   ├── record_source()           — auditor usa em retryable + orphans [l]ink/[k]eep
│   ├── lookup_source()           — auditor usa em orphan resolution
│   ├── normalize_url()           — auditor usa em retroactive_dedup
│   ├── mark_deleted()            — NOVA, auditor e UNICA consumidora
│   └── _load_or_bootstrap()      — auditor usa em diff_engine
└── sci_fetch/
    ├── classify_url.py           — auditor usa em retroactive_dedup
    └── upload_to_nblm.py         — auditor delega bucket `missing`
        └── flag --from-auditor   — NOVA, telemetria (tagged no JSON summary)
```

## O que a auditor ADICIONA ao deep-research (RF-07 compat)

### `mark_deleted()` em `notebook_manifest.py`

```python
def mark_deleted(
    *,
    manifest_path: Path,
    notebook_id: str,
    canonical_key: str,
    reason: str,  # "duplicate_of:src_abc" | "orphan_user_choice" | "deleted_from_nbm_externally"
) -> dict | None:
    """Mark a source as deleted. Preserves history (status='deleted', deleted_at, deletion_reason)."""
```

**Nao-breaking:** so adiciona campos (`deleted_at`, `deletion_reason`), nunca remove entrada.
Leitor antigo do manifesto ignora campos extras.

### `--from-auditor` em `upload_to_nblm.py`

Flag booleana opcional. Quando presente, adiciona `"caller": "notebook-source-auditor"` no JSON summary emitido no stdout. Nao altera comportamento.

## Como a auditor chama upload_to_nblm.py

```python
subprocess.run(
    [
        sys.executable,
        str(Path.home() / ".claude/skills/deep-research/scripts/sci_fetch/upload_to_nblm.py"),
        "--urls", str(tmp_file),
        "--notebook", notebook_id,
        "--pesquisa", slug,
        "--pesquisas-root", str(pesquisas_root),
        "--from-auditor",
    ],
    capture_output=True, text=True, timeout=600,
)
```

A auditor gera 1 subprocess call por **pesquisa slug** (porque upload_to_nblm espera 1 slug por invocacao). URLs da mesma pesquisa vao juntas num `/tmp/auditor-missing-<nbid>-<slug>.txt`.

## Contratos compartilhados

### Manifesto schema (schema v1, preservado)

Campos que a auditor adiciona a uma entrada existente (via `mark_deleted`):

```json
{
  "status": "deleted",
  "deleted_at": "2026-04-23T14:32:00+00:00",
  "deletion_reason": "duplicate_of:src_abc"
}
```

Campos que `record_source()` ja gerenciava (sem mudanca):

```json
{
  "canonical_key": "pmid:123",
  "title": "...",
  "type": "article",
  "origin_pesquisa": "hashimoto-farmacologia",
  "added_at": "...",
  "status": "ok | captcha_pending | failed | deleted",
  "last_attempt_at": "...",
  "attempts": 3,
  "notebooklm_source_id": "src_xyz",
  "ingest_method": "url_direct | pdf_upload | captcha_bypass_flow_v1",
  "ingest_metadata": {...},
  "last_error": "..."
}
```

## File lock compartilhado

`notebook_manifest._FileLock` usa PID-based locking com reclaim de stale PIDs apos timeout. auditor e deep-research rodando em paralelo serializam automaticamente no mesmo lock (`_notebook-manifest.json.lock`).

Se o lock nao for liberado em 30s (ex: processo paralelo travou sem liberar), auditor aborta exit 5. Nao ha tentativa de force-unlock — o usuario decide se kill o outro processo.

## O que a auditor NUNCA faz

- Invocar `deep-research` diretamente (escopo errado — deep-research pesquisa e cria PESQUISA-*.md)
- Modificar `PESQUISA-*.md` (escopo errado — pesquisa e artefato historico)
- Reimplementar classify_url ou fetch cientifico (delega sempre)
- Marcar entradas do manifesto com `status="deleted"` fora do helper `mark_deleted()` (unico caminho autorizado)

## O que a deep-research NUNCA faz (convencao)

- Invocar `auditor` apos terminar pesquisa
- Deletar sources do NotebookLM
- Chamar `mark_deleted()`

Convencao reforcada no codigo: `mark_deleted()` nao e chamada de nenhum script em deep-research/scripts/ (verificavel via `grep -r mark_deleted ~/.claude/skills/deep-research/`).
