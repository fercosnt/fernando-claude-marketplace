# Audit Flow — detalhamento passo a passo

Este documento expande o fluxo de 6 passos da skill (secao "Fluxo operacional" no `SKILL.md`). Leia em conjunto com `bucket-decision-matrix.md` (o que cada bucket significa) e `integration-with-deep-research.md` (contratos compartilhados).

## Passo 1 — Resolucao de input

### Entrada
- `--notebook`: URL completa OU bare id
- `--pesquisas`: lista CSV de paths

### Processamento
1. `url_extract.extract_notebook_id()` aplica regex `/notebook/([A-Za-z0-9_-]+)` ou valida bare id (`^[A-Za-z0-9_-]{8,}$`)
2. Cada path de pesquisa e resolvido com `Path.resolve()` — erro imediato se nao existir
3. Warning (nao aborta) se a pasta esta vazia de `.md`
4. `parents = {_root_of(p) for p in pesquisas_paths}` — se `len(parents) != 1`, aborta exit 2. Regra: todas as pesquisas compartilham um manifesto unico no parent comum. `_root_of(p)` = `p.parent` para arquivos `.md` soltos OU para pastas (ambos viram um root no mesmo nivel).
5. Slug de cada pesquisa: `p.stem` se for arquivo `.md`, `p.name` se for pasta. Ex: `~/research/hashimoto-reference.md` → slug `hashimoto-reference`.

### Estrategia de scan dos `.md` (em `diff_engine._md_files_for`)
- Path = arquivo `.md` direto → so esse arquivo
- Path = pasta com `PESQUISA-*.md` → glob canonico
- Path = pasta sem `PESQUISA-*.md` → fallback `*.md` (exclui nomes iniciados em `_`)

### Saida
```python
{
  "notebook_id": str,
  "pesquisas_paths": list[Path],
  "pesquisas_root": Path,
  "manifest_path": Path,  # {pesquisas_root}/_notebook-manifest.json
  "audits_dir": Path,     # {pesquisas_root}/_audits/ por default
}
```

## Passo 2 — Pull do NotebookLM

`notebooklm source list -n <id> --json` via subprocess (timeout 30s).

### Tratamento de erro
- stderr contem "authentication" ou "login" → `AuthError` → exit 5 com mensagem `Run: notebooklm login`
- rc != 0 na primeira tentativa → retry 1x
- rc != 0 na segunda → exit 2
- stdout nao parseavel como JSON → exit 2 ("CLI returned malformed JSON")

### Formato esperado
```json
{"sources": [{"id": "src_xyz", "title": "...", "url": "...", "type": "article"}]}
```

Caminho de fallback: se `sources` nao existe, tenta `data`.

## Passo 3 — Expected state

`diff_engine.load_expected_from_pesquisas()` retorna `{canonical_key: expected_entry}`.

### Fonte primaria — manifesto

Itera sobre `manifest.notebooks[notebook_id].sources`:
- Descarta `status == "deleted"` (sao historicos, nao expected)
- Entradas cujo `origin_pesquisa` esta fora da lista passada ainda contam como expected — porque o usuario pode ter passado so um subset das pesquisas que alimentam este notebook, e deletar sources "nao pertencentes" seria destrutivo.

### Fonte secundaria — PESQUISA-*.md

Scan regex `https?://[^\s]+` nos `.md`, depois `retroactive_dedup.derive_canonical_key` em cada URL.
Para evitar falsos positivos (URL mencionada em prose mas que nao foi adicionada como source), **so promove para expected se confidence == "high"** (PMID/PMC/DOI). URLs genericas sao ignoradas.

## Passo 4 — Diff (nucleo)

`diff_engine.compute_diff()` — funcao pura, 5 buckets + noop_count.

### Ordem de resolucao de conflitos

1. `missing` e `retryable` nao se sobrepoem: se um canonical_key cai em ambos, fica SO em `retryable` (caminho mais barato — manifesto ja tem o hint de como tentar).
2. `duplicates` tem prioridade sobre `noop`: se 2 sources resolvem pra mesma canonical_key, conta como 1 duplicata, nao 2 no-ops.
3. `orphans` so reporta sources realmente sem manifesto — se manifesto tem mas usuario nao passou a pesquisa, nao e orfa (e no-op silencioso).
4. `stale_manifest` e mutuamente exclusivo com `missing`/`retryable`: stale = manifesto diz "ok" mas NBM nao tem E expected nao tem (usuario removeu tanto da UI quanto das pesquisas).

### Determinismo

- Duplicates: ordenacao por `added_at` ASC, fallback `source_id` lexical. Sem timestamps voláteis.
- Listas sempre ordenadas para output estavel (missing sorted por canonical_key).

## Passo 5 — Resolvers

Ordem de execucao: **missing → retryable → duplicates → stale_manifest → orphans**.

A ordem importa porque:
- `missing` pode adicionar sources que depois aparecem em duplicates? Nao — o diff ja foi computado antes. Segunda run veria na proxima.
- `duplicates` muda o NBM. Stale_manifest nao depende do NBM pos-delete.
- `orphans` e ultimo porque pode ser interativo (bloqueia I/O).

Cada resolver retorna `{"results": [...], "summary_note": "..."}` para alimentar o report_writer.

### Falhas graceful
- `resolve_missing` continua para outros buckets mesmo que sci_fetch falhe
- `resolve_retryable` marca `failed` no manifesto (nao aborta) se URL nao existe ou PDF sumiu
- `resolve_duplicates` reporta partial_failure se ao menos 1 delete falhou — exit 4 no final
- `resolve_orphans` interativo respeita `[s]kip` como default em input vazio

## Passo 6 — Relatorio

`report_writer.write_report()`:
- Markdown em `{audits_dir}/<notebook_id>-<date>.md`
- Raw JSON em `{audits_dir}/raw/<notebook_id>-<date>.json`

Overwrite no mesmo dia (Q1). Raw JSON preserva paper trail.

## Exit codes recapitulados

| Code | Quando |
|---|---|
| 0 | Sucesso — dry-run sempre 0 (mesmo com diffs detectados); apply sem falhas tambem 0 |
| 2 | Invocacao invalida OU notebook nao acessivel |
| 3 | `partial_bootstrap` = True — manifesto nao existia antes desta run (criado vazio) |
| 4 | apply mode + duplicates ou orphans resultaram em `any_failure` |
| 5 | Auth / lock / corrupcao do manifesto |
