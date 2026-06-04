# Bucket Decision Matrix

O coracao da skill. Toda divergencia entre NotebookLM / manifesto / pesquisas cai em **exatamente 1 dos 6 buckets** (5 estaveis + 1 da v2 Fase B: `captcha_page_disguised`). Se voce encontrar um caso real que nao cai em nenhum, abra issue — a taxonomia esta incompleta.

## Matriz de classificacao

Para cada canonical_key, responda 3 perguntas:

1. **Esta no NBM?** (Yes / No)
2. **Esta no manifesto?** (Yes-ok / Yes-error / Yes-deleted / No)
3. **Esta no expected state (pesquisas passadas)?** (Yes / No)

| NBM | Manifesto | Expected | Bucket | Acao |
|---|---|---|---|---|
| No  | No         | Yes | **missing** | Delega a sci_fetch/upload_to_nblm.py (1 call por pesquisa) |
| No  | Yes-error  | Yes | **retryable** | Retry direto (url_direct ou pdf_upload); captcha_bypass_flow_v1 → manual |
| No  | Yes-ok     | No  | **stale_manifest** | Auto mark_deleted(reason=deleted_from_nbm_externally) |
| No  | Yes-ok     | Yes | **retryable** ou **missing** | Tratado como missing; manifesto fica stale ate ser atualizado |
| No  | Yes-deleted| —   | noop | Historico, nao participa |
| Yes | No         | No  | **orphan** | Listado ou interactive [k]/[d]/[l] |
| Yes | No         | Yes | noop + warning | Deveria ter registro — warning "fora do manifesto mas em expected"; nao destrutivo |
| Yes | Yes-ok     | Yes | noop | Caso feliz |
| Yes | Yes-ok     | No  | noop | Usuario nao passou a pesquisa — silencioso |
| Yes | Yes-error  | Yes | noop + warning | NBM OK mas manifesto stale; warning, nao altera (evita overwrite) |
| Yes | Yes-deleted| —   | noop + warning | Conflito: manifesto diz deleted mas NBM ainda tem. Warning, nao toca |

E a regra de **duplicatas**: se 2+ sources do NBM resolvem pra mesma canonical_key, saem de onde estariam (noop/orphan/etc) e vao para `duplicates`.

**Precedencia do `captcha_page_disguised` (F1b, v2 Fase B):** se o titulo do source bate o regex F15 (`is_captcha_title`), o source SAI das duplicatas e dos orphans e vai direto pro bucket `captcha_page_disguised`. Motivo: o unico acao racional eh delete+readd via sci_fetch; manter como keep de um grupo duplicate deixaria a pagina de captcha no notebook. Quando a captcha-page NAO tem entry no manifesto (caso comum: deep-research achou que a ingesta falhou), fazemos apenas delete + readd sem mark_deleted. Quando TEM entry, flipamos status → deleted com `deletion_reason=captcha_page_detected`.

## Detalhes por bucket

### missing

**Criterio:** `canonical_key in expected` AND `canonical_key not in current_nbm_canonical_keys` AND `canonical_key not in retryable`

**Acao em apply:**
1. Agrupa por `origin_pesquisas[0]` (primeira pesquisa listada como origem)
2. 1 call para `sci_fetch/upload_to_nblm.py --urls <tmp> --notebook <id> --pesquisa <slug> --pesquisas-root <root> --from-auditor`
3. Se subprocess rc != 0, marca cada canonical_key como `error: sci_fetch rc=N` no relatorio
4. sci_fetch atualiza o manifesto sozinho — auditor nao duplica

**Edge cases:**
- Source sem URL (nem em manifest_entry, nem em signal_url, nem em pesquisa) → goes to `manual_required` com reason `missing_url`

### retryable

**Criterio:** manifest entry com `status in {captcha_pending, failed}` AND `ingest_method in {url_direct, pdf_upload}` AND `attempts < max_retry` AND `canonical_key not in current_nbm`

**Acao em apply por ingest_method:**
- `url_direct`: `notebooklm source add <url> -n <id> --json` — url vem de `ingest_metadata.signal_url` ou `manifest_entry.url`
- `pdf_upload`: `notebooklm source add <pdf_local_path> -n <id> --json` — se arquivo nao existe, marca `failed:pdf_not_found`
- `captcha_bypass_flow_v1`: NUNCA automatiza — entra em `manual_required`

Sucesso: `record_source(status=ok, notebooklm_source_id=...)` — attempts incrementa automaticamente.
Falha: `record_source(status=failed, error=...)` — attempts incrementa.

### duplicates

**Criterio:** 2+ sources do NBM resolvem pra mesma canonical_key.

**Estrategia de keep:**
1. Sort por `added_at` ASC (mais antigo primeiro) com fallback por `source_id` lexical
2. Keep = primeiro; delete = resto

**Acao em apply:**
- `notebooklm source delete <sid> -n <id> -y` para cada delete
- Se todos deletaram: `mark_deleted(canonical_key, reason=duplicate_of:<keep_id>)` no manifesto (nota: so 1 entrada do manifesto e marcada — a do canonical_key; fontes duplicadas que nao tinham entrada propria no manifesto ja nao existiam la)
- Se algum delete falhou: status `partial_failure` + exit 4 no final

**Guardrail:** defensivo — se por erro de grouping um grupo tiver 0 ou 1 elementos, skip (nunca deixa notebook com 0 sources).

### orphans

**Criterio:** source no NBM sem canonical_key em expected AND sem entrada no manifesto para aquele canonical_key.

**Default (sem `--interactive`):** listado no relatorio, nao age.

**Com `--interactive`:**
- `[k]eep`: `record_source(origin_pesquisa="manual_keep")` — nao pergunta de novo em runs futuras
- `[d]elete`: `notebooklm source delete` + `mark_deleted(reason="orphan_user_choice")`
- `[l]ink to <slug>`: `record_source(origin_pesquisa=<slug>)` — promove para no-op daqui em diante
- `[s]kip`: nada

Com 5+ pesquisas, `[l]ink` apresenta menu indexado (`[1] slug ... [5] slug`). Usuario digita numero.

#### Caso comum: orfas que sao captcha-pages mascaradas

Validacao real (notebook Hashimoto, 2026-04-23): 47 das 90 orfas tinham titulo `"Checking your browser - reCAPTCHA"` — sao **paginas Cloudflare salvas como source** porque a deep-research v2 fez upload do HTML do challenge em vez do PDF do paper. Como nao foram registradas no manifesto (a deep-research achou que tinha falhado), a auditor as classifica como orfa.

**Reconhecimento manual em `--interactive`:** se voce ver titulo contendo "Checking your browser", "reCAPTCHA", "Just a moment", ou "Sage Journals: Discover world-class research", quase sempre e captcha-page. Acao recomendada: `[d]elete` (some do NBM e do manifesto), depois rode a deep-research em `--scientific-deep` no PMID/DOI da URL pra re-adicionar via `sci_fetch/`.

**v2 Fase B (F1b) entregou** esse bucket dedicado: `captcha_page_disguised`. O diff engine roda `is_captcha_title` em todo source do NBM; os que batem vao direto pro bucket novo (nao aparecem mais como orfa nem como duplicate). Sem `--interactive`: o resolver padrao em `--apply` deleta + re-adiciona a URL via `sci_fetch` (com `--skip-dupe` da F8). Em `--dry-run` so lista — como os outros buckets.

### stale_manifest (bonus v1)

**Criterio:** `manifest_entry.status == "ok"` AND `canonical_key not in current_nbm` AND `manifest_entry.origin_pesquisa NOT in passed_slugs`.

Motivo operacional: manifest ainda lembra de uma source cuja pesquisa-origem nao foi passada para esta auditoria (pesquisa foi renomeada, movida ou a pasta foi removida). Se essa source tambem nao esta no NBM, eh seguro marcar como deletada — o usuario ja nao a considera parte do escopo atual.

**Acao em apply:** `mark_deleted(canonical_key, reason="deleted_from_nbm_externally")` — silencioso, nao pergunta. Baixo risco: nao deleta nada no NBM; so atualiza o manifesto para refletir a realidade.

**O que NAO conta como stale:**
- Source cuja `origin_pesquisa` ESTA em `passed_slugs` mas foi removida do NBM pelo usuario → vai para `missing`, auditor tenta re-adicionar. Se o usuario quer mesmo remover, ele precisa tambem tirar da pesquisa (deletar referencia no PESQUISA-*.md ou nao passar a pesquisa).

### captcha_page_disguised (F1b, v2 Fase B)

**Criterio:** source no NBM cujo `title` bate `captcha_patterns.CAPTCHA_PATTERNS` (F15). Aplicado antes de `duplicates` e `orphans` para evitar reclassificacao.

**Acao em dry-run:** lista no relatorio, nao toca.

**Acao em `--apply` (por source):**
1. `notebooklm source delete <sid> -n <id> -y`
2. Se `canonical_key` derivada esta no manifesto (`in_manifest=True`): `mark_deleted(canonical_key, reason="captcha_page_detected")` pra preservar historico
3. Coleta a URL numa lista de re-add

**Acao em `--apply` (batch final):**
- 1 call a `sci_fetch/upload_to_nblm.py --skip-dupe` com todas as URLs, usando o primeiro pesquisa slug como target
- F8 skip-dupe previne reintroduzir o que o NBM ja tem (caso um source legit exista pra mesma canonical_key)
- Falha no batch → exit 4 (`any_failure=True`)

**Diferenca vs `--fix-captcha` (F7):**
- F7 e composite mode: pula o diff de 6 buckets, delete+readd, roda dedupe ate convergencia (F11)
- F1b e inline no standard audit: delete+readd sem loop de dedupe. Se quiser convergencia, use `--fix-captcha`

**Sem manifesto:** captcha page com `in_manifest=False` so e deletada; nao ha historico pra marcar. Isso cobre o caso comum da Fase 5 (a deep-research achou que tinha falhado, nao registrou).

## Caso especial: `bootstrap_unknown` (v2)

Em v2 (bootstrap mode), sources NBM de notebooks legados sem manifesto sao adicionadas com `ingest_method="bootstrap_unknown"`. Essa flag sinaliza para retryable: nao tente retry automatico — nao sabemos como foi adicionada originalmente.

v1 nao faz bootstrap: exit code 3 recomenda.
