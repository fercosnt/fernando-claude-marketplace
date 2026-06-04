<!--
Template: NotebookLM Upload Report (Fase 4.5)
Insira esta secao ao final do PESQUISA-*.md apos o pipeline cientifico rodar.
Substitua todos os placeholders {CAMELCASE}.
-->

## NotebookLM — Status de Upload de Fontes

**Notebook:** [{NOTEBOOK_TITLE}]({NOTEBOOK_URL})
**Data:** {YYYY-MM-DD}
**Total tentadas:** {N_TOTAL} URLs
**Pipeline:** Fase 4.5 (scientific source pipeline)

### Resumo

| Bucket | Count | % |
|--------|-------|---|
| Auto-uploaded (OK) | {N_AUTO} | {PCT_AUTO}% |
| Manual upload required | {N_MANUAL} | {PCT_MANUAL}% |
| Paywall/unavailable | {N_PAYWALL} | {PCT_PAYWALL}% |

---

### ✅ Auto-uploaded ({N_AUTO} sources)

Subidos automaticamente como arquivo (PubMed abstract, PMC full-text, OA PDF via Unpaywall) ou URL direta (gov/blog).

| Titulo | Canonical Key | Tipo | Source ID |
|--------|---------------|------|-----------|
| {TITULO_1} | {PMC:PMCxxxxx} | article | {NBLM_SOURCE_ID_1} |
| {TITULO_2} | {PMID:xxxxxx} | article | {NBLM_SOURCE_ID_2} |
| {URL_3} | {URL:https://...} | url | {NBLM_SOURCE_ID_3} |
<!-- repita para cada source auto-uploaded -->

---

### ⚠ Manual upload required ({N_MANUAL} sources)

Estas URLs nao podem ser subidas automaticamente (Cloudflare, login, DOI paywalled). Siga as instrucoes por linha.

| URL | Motivo | O que fazer |
|-----|--------|-------------|
| {URL_MDPI} | Cloudflare 403 | Abrir link → botao "Download PDF" → arrastar para o NotebookLM |
| {URL_DOI_PAYWALL} | DOI nao-OA no Unpaywall | Ver se voce tem acesso institucional; logar; baixar PDF; subir manualmente |
| {URL_LOGIN_REQUIRED} | Site exige login (Examine, ConsumerLab) | Logar, copiar texto relevante, colar como "Text source" no NotebookLM |
<!-- repita para cada manual -->

**Dica:** apos fazer o upload manual, voce pode rodar `python scripts/notebook_manifest.py show pesquisas/ {NOTEBOOK_ID}` para confirmar que o source aparece. Atualize o manifesto com `ingest_method: captcha_bypass_flow_v1`.

---

### ❌ Paywall / Unavailable ({N_PAYWALL} sources)

Sem workaround gratuito e etico dentro das politicas da Anthropic. Considere:
- Acesso institucional (biblioteca universitaria)
- Inter-library loan
- Contato direto com autor (os papers geralmente respondem)

| URL | Razao |
|-----|-------|
| {URL_PAYWALL_1} | Unpaywall indica `is_oa=false` em todos os hosts |
| {URL_PAYWALL_2} | Publisher fechado, sem preprint disponivel |
<!-- repita -->

---

### Notas operacionais

- CAPTCHAs que ja existiam no notebook foram deletados antes deste upload (via `cleanup_captcha_sources.py`)
- Manifesto atualizado: `{pesquisas_root}/_notebook-manifest.json`
- Arquivos locais baixados em: `pesquisas/{slug}/fontes/sci_fetch/`
- Para re-tentar manuals depois: veja `scripts/sci_fetch/upload_to_nblm.py --help`
