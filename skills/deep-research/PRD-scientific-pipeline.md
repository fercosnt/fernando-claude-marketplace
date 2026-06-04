# Scientific Source Pipeline — PRD

**Autor:** Fernando Costa Neto | **Data:** 2026-04-23 | **Status:** Draft
**Nivel:** Standard
**Skill alvo:** `~/.claude/skills/deep-research/` (v2 upgrade)
**Upstream:** Execucao real — sessao 2026-04-22 (pesquisa Hashimoto/farmacologia, 86 URLs alvo, 110 sources finais no NotebookLM)

---

## 1. Problema & Contexto

### 1.1 Voz do Usuario

> "Tentei adicionar 86 URLs cientificas ao NotebookLM e so ~40% funcionaram. 38 sources viraram 'Checking your browser - reCAPTCHA' inuteis. Tive que improvisar um pipeline de fetch manual no meio da execucao — NCBI E-utilities, strip HTML, upload como arquivo. Se eu nao fosse desenvolvedor, teria desistido. A skill deveria fazer isso sozinha quando detecta fontes cientificas."
> — Fernando, apos executar deep-research com briefing de farmacologia (22/04/2026)

### 1.2 Evidencia Quantitativa (desta execucao)

| Tipo de fonte | Tentadas | Sucesso URL direto | Sucesso apos improviso |
|---|---|---|---|
| PubMed (PMID) | 21 | 0% (CAPTCHA) | 100% (E-utilities efetch) |
| PMC (PMCID) | 18 | 0% (CAPTCHA) | 89% (HTML fetch + strip) |
| MDPI | 1 | 0% (Cloudflare) | 0% (bloqueio persistente) |
| Karger | 1 | 0% (Cloudflare) | 0% (bloqueio persistente) |
| Liebert | 1 | 0% (Cloudflare) | 0% (bloqueio persistente) |
| NEJM | 7 | 100% | — |
| ClinicalTrials.gov | 1 | 100% | — |
| Blog (Peter Attia) | 3 | 33% | 100% |
| GovSites (FDA/WHO) | 10 | 80% | — |
| **Total** | **86** | **~40%** | **~95%** |

### 1.3 MITRE Problem Framing

**Suposicoes implicitas da skill atual:**
- Assume que qualquer URL pode ser adicionada direto ao NotebookLM como "website source"
- Assume que o scraper do NotebookLM lida com anti-bot/CAPTCHA
- Assume que abstract de PubMed e suficiente (ignora PMC full-text disponivel)

**Quem sofre:**
- Usuario primario (Fernando): perde tempo improvisando scripts em tempo de execucao, precisa re-autenticar CLI do NotebookLM, tem que deletar sources CAPTCHA manualmente
- Usuarios secundarios (outros devs executando deep-research em topicos cientificos): experiencia degradada, frustracao, possivel abandono

**How Might We:**
> Como podemos detectar automaticamente fontes cientificas (PubMed/PMC/DOI) e rotea-las atraves de APIs oficiais (E-utilities, Unpaywall) ao inves do scraper generico, garantindo 95%+ de sucesso no NotebookLM sem improviso?

### 1.4 Por Que Agora

- Pesquisa de farmacologia revelou magnitude do problema (60% falha)
- Solucao foi descoberta experimentalmente e validada em producao (110 sources)
- Pipeline documentado em `~/.claude/skills/research/pdfs/` (scripts + logs)
- Risco de re-invencao: proxima pesquisa cientifica sem esta atualizacao repetira o improviso

---

## 2. Objetivos & Metricas

### 2.1 Metrica Primaria (North Star)

**Taxa de sucesso NotebookLM em pesquisas cientificas**: % de URLs cientificas que viram source util (conteudo real, nao CAPTCHA/error) no NotebookLM sem intervencao manual.

- **Baseline atual:** 40% (medido nesta execucao)
- **Meta v1:** >= 90%
- **Meta v2 (com Playwright fallback):** >= 95%

### 2.2 Metricas Secundarias

| Metrica | Baseline | Meta v1 |
|---|---|---|
| Cobertura full-text (PMIDs com PMC equivalente) | 0% (so abstract) | >= 80% |
| Sources CAPTCHA/error criadas | 38/86 (44%) | 0 |
| Tempo medio de execucao para 50 URLs cientificas | ~25 min (com improviso) | <= 8 min |
| URLs com relatorio "manual-upload" claro | 0 (usuario descobre ao falhar) | 100% dos casos legitimos |

### 2.3 Guardrails (nao podem regredir)

- **NCBI rate limit:** nao exceder 3 req/s sem API key, 10 req/s com key (evitar ban)
- **Compatibilidade:** `deep-research` existente (modo normal, YouTube, Update) nao pode quebrar
- **Opt-out:** usuario pode desativar com `--skip-sci-pipeline` se preferir fluxo antigo
- **Sem scraping agressivo:** nao tentar mais que 2 retries em qualquer URL; respeitar robots.txt

---

## 3. Escopo

### 3.1 Dentro do Escopo — v1 (obrigatorio)

**F1. Scripts em `scripts/sci_fetch/`:**
- `pubmed_abstract.py` — NCBI E-utilities efetch
- `pmid_to_pmc.py` — NCBI E-utilities elink (detecta PMCID)
- `pmc_fulltext.py` — HTML fetch com User-Agent + strip tags
- `unpaywall_resolver.py` — DOI → OA PDF URL (API gratuita)
- `open_access_pdf.py` — fetch generico com headers apropriados
- `classify_url.py` — detecta tipo (PubMed/PMC/DOI/generic/paywall)

**F2. Nova fase da skill** (entre Fase 4 Consolidar e Fase 5 Compilar):
- "Fase 4.5: Scientific Source Pipeline"
- Ativa automaticamente quando >= 3 URLs cientificas detectadas
- Ou manualmente via `--scientific` flag

**F3. Default "prefer file over URL":**
- Para PubMed/PMC/DOI: sempre baixar localmente, upload como arquivo
- Para generic sites conhecidos sem CAPTCHA (Peter Attia blog, etc): URL direto
- Para Cloudflare-known (MDPI/Karger/Liebert): skip + adiciona a "manual bucket"

**F4. Relatorio de 3 buckets no PESQUISA-*.md:**
- ✅ Auto-uploaded: lista de files subidos
- ⚠ Manual upload required: URL + motivo + instrucoes
- ❌ Paywall/unavailable: URL + razao (sem instrucao de workaround)

**F5. Cleanup de sources invalidas:**
- Antes de adicionar novos sources, detectar e deletar sources com titulo contendo "Checking your browser" / "reCAPTCHA" / status=error no notebook alvo

### 3.2 Futuro — v2 (after v1 ships)

**F6. Unpaywall como 1a tentativa para DOIs** — resolve ~60% de "paywalls aparentes" encontrando versao OA (preprint bioRxiv, repositorio institucional)

**F7. Playwright fallback opcional** (`--scientific-deep` flag):
- Spawn headless browser para Cloudflare-blocked sites
- Custo: +5-10s por URL
- Resolve ~90% dos MDPI/Karger/Liebert

**F8. Cache local** em `~/.cache/deep-research-sci/`:
- PMID/PMCID → fetched content
- Evita re-fetch em research updates
- TTL 90 dias

**F9. Parallel fetching com rate limit coordenado:**
- 3 workers para NCBI, 2 para Unpaywall, 5 para generic
- Respeita limits centralizado via token bucket

### 3.3 Versoes Futuras — v3+

- Semantic Scholar API (metadata + alguns full-texts)
- OpenAlex integration (academic graph)
- bioRxiv/medRxiv preprint fallback
- OCR de PDFs escaneados (se detectar imagem-only)

---

## 3b. Fora do Escopo (justificativas)

| Item | Por que fora | Trade-off |
|---|---|---|
| **Sci-Hub / Library Genesis** | Legal e etico questionavel; Anthropic policy | Usuarios com acesso institucional ainda servido; resto eh unavailable |
| **Sign-in automatizado** (Examine.com, ConsumerLab) | Credenciais em disco, sem solucao segura | Usuario baixa manual do browser logado |
| **Traducao automatica** de papers em outros idiomas | Out of scope pra este PRD | Deep-research ja loga idioma original |
| **Parsing estruturado** de PDFs (tables, figuras) | Out of scope — NotebookLM ja faz em upload | Skill nao duplica trabalho |
| **Scraper customizado para journal X** | Nao escala; manutencao alta | Prefere Unpaywall/APIs oficiais |
| **Reference management** (Zotero/Mendeley export) | Out of scope — usuario pode usar Notion ou outro | Skill foca em NotebookLM como RAG |

---

## 4. Personas & Casos de Uso

### Persona Primaria: Fernando (usuario ativo)

- **Contexto:** desenvolvedor, executa deep-research em topicos de saude pessoal (Hashimoto, farmacologia, longevidade) e projetos profissionais
- **Conhecimento tecnico:** alto — sabe debugar CLI, mas NAO quer improvisar pipelines a cada pesquisa
- **Tolerancia a falha:** baixa quando e problema resolvivel automaticamente; alta quando e limitacao legitima (paywall real)
- **Job-to-be-done:** "preciso de uma base de conhecimento farmacologica consultavel via NotebookLM, com papers completos quando possivel, para ancorar decisoes de saude"

### Persona Secundaria: Outro Claude Code user (esporadico)

- Executa deep-research ocasionalmente em topicos cientificos (medicos, pesquisadores amadores, escritores de divulgacao)
- Menor tolerancia a configuracao — quer que "funcione de primeira"
- Depende de relatorio claro do que precisa fazer manualmente

### Caso de Uso Principal

```
Given: Fernando executa deep-research sobre "GLP-1s em pacientes com Hashimoto"
When: Subagentes retornam 50 URLs, das quais 35 sao PubMed/PMC/NEJM/cientificas
Then:
  - Fase 4.5 ativa automaticamente
  - 21 PubMed IDs vao via E-utilities (abstract) + elink (PMCID)
  - 18 PMC IDs tem full-text baixado
  - 5 DOIs passam por Unpaywall
  - 3 sites generic (blog, gov) via URL direto
  - 4 Cloudflare-blocked vao pra bucket "manual"
  - Todos os arquivos uploaded como file (nao URL) ao NotebookLM
  - Relatorio em PESQUISA-*.md lista os 3 buckets
  - Fernando abre os 4 manuals no browser, arrasta PDFs pro NotebookLM
```

---

## 5. Epic Hypotheses

### Epic 1: Auto-detectar e rotear fontes cientificas

**Hipotese:** Se a skill classificar URLs em PubMed/PMC/DOI/generic/paywall antes do upload, entao evitamos 100% dos CAPTCHAs do NotebookLM scraper (baseline: 38 CAPTCHAs em 86 URLs).

**Tiny act of discovery:** Implementar `classify_url.py` isolado, rodar contra as 86 URLs desta execucao, validar que classificacao cobre todos os padroes vistos.

### Epic 2: Maximizar cobertura full-text via E-utilities

**Hipotese:** Se usarmos `elink` para descobrir PMCID de todo PMID, entao aumentamos cobertura full-text de 0% (so abstract) para >=80% dos papers disponiveis em PMC.

**Tiny act:** Rodar `pmid_to_pmc.py` contra os 21 PMIDs desta execucao. Meta: 18+ returns PMCID (validado — conseguimos 18/21).

### Epic 3: Report-driven manual workflow

**Hipotese:** Se gerarmos relatorio de 3 buckets com instrucoes claras para bucket "manual", entao usuarios conseguem completar 100% das URLs legitimas em <= 5 min sem frustracao.

**Tiny act:** Template de relatorio com exemplos concretos (abrir link X → botao "Download PDF" → arrastar pro NotebookLM).

---

## 6. Requisitos Funcionais

### RF-01. `classify_url.py`

**Input:** URL string
**Output:** JSON `{type, confidence, metadata}`
**Tipos:**
- `pubmed` (regex: `pubmed\.ncbi\.nlm\.nih\.gov/(\d+)`)
- `pmc` (regex: `pmc\.ncbi\.nlm\.nih\.gov/articles/PMC(\d+)` ou `ncbi\.nlm\.nih\.gov/pmc/articles/PMC(\d+)`)
- `doi` (regex: `doi\.org/10\.\d+/.*` ou URL com `/doi/10.`)
- `cloudflare_known` (hostname em lista: mdpi.com, karger.com, liebertpub.com, jamanetwork.com, academic.oup.com, sciencedirect.com)
- `gov_or_guideline` (fda.gov, who.int, nih.gov, cdc.gov)
- `blog_or_news` (medium.com, substack.com, peterattiamd.com, dominios wordpress conhecidos)
- `generic_web` (qualquer outro)

**Aceite:**
- [ ] Classifica corretamente as 86 URLs desta execucao (validacao em `evals/`)
- [ ] Retorna `metadata.pmid` ou `metadata.pmcid` ou `metadata.doi` quando aplicavel
- [ ] Tempo < 10ms por URL (so regex, sem rede)

### RF-02. `pubmed_abstract.py`

**Input:** PMID (string de digitos)
**Output:** arquivo `.txt` com header + abstract
**API:** `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pmid}&rettype=abstract&retmode=text`

**Aceite:**
- [ ] Retorna abstract com >= 500 chars para PMIDs validos
- [ ] Retry com backoff em HTTP 429 (NCBI rate limit)
- [ ] Falha graciosa com exit code 2 se abstract < 100 chars
- [ ] Usa NCBI API key se `NCBI_API_KEY` env var presente (permite 10 req/s)
- [ ] Formato output: `# PubMed {PMID}: {titulo}\n\nSource: {url}\n\n---\n\n{abstract}`

### RF-03. `pmid_to_pmc.py`

**Input:** PMID (ou lista de PMIDs)
**Output:** JSON `{pmid: pmcid | null}`
**API:** `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&db=pmc&id={pmid}`

**Aceite:**
- [ ] Detecta PMCID a partir de `<Link><Id>{num}</Id></Link>` no XML
- [ ] Valida: 18/21 PMIDs desta execucao retornam PMCID correto
- [ ] Batch: aceita lista de PMIDs e retorna dict em 1 chamada quando possivel

### RF-04. `pmc_fulltext.py`

**Input:** PMCID (string com prefixo PMC)
**Output:** arquivo `.txt` com header + full-text do artigo
**Metodo:** GET em `https://pmc.ncbi.nlm.nih.gov/articles/{PMCID}/` com User-Agent Chrome real, Accept text/html, parse HTML e strip tags via regex.

**Aceite:**
- [ ] Retorna > 10.000 chars para 80%+ dos PMCIDs validos (validado: 17/18 nesta execucao)
- [ ] Detecta quando landing page retorna captcha/redirect (< 5000 chars) e falha graciosamente
- [ ] Preserva estrutura basica (headings, paragraphs) via espacos; nao preserva tabelas
- [ ] Formato output: `# FULL-TEXT: {PMCID}\n\n{titulo}\n\nSource: {url}\nPubMed: {url_pubmed}\n\n---\n\n{texto}`

### RF-05. `unpaywall_resolver.py`

**Input:** DOI
**Output:** JSON `{is_oa, oa_pdf_url | null, oa_landing_url | null, host_type}`
**API:** `https://api.unpaywall.org/v2/{doi}?email={USER_EMAIL}`

**Aceite:**
- [ ] Retorna URL de PDF quando `is_oa=true`
- [ ] Prefere `host_type=repository` (pre-print seguro) sobre `publisher`
- [ ] Requer env var `UNPAYWALL_EMAIL` (API exige email, mas e free)
- [ ] Cache local 90 dias (DOI raramente muda)

### RF-06. `open_access_pdf.py`

**Input:** URL direto de PDF
**Output:** arquivo `.pdf` local
**Metodo:** GET com User-Agent Chrome, Referer do dominio, Accept `application/pdf`

**Aceite:**
- [ ] Valida signature `%PDF` nos primeiros 5 bytes; se nao, salva como `.html` fallback
- [ ] Timeout 60s
- [ ] Max size 50MB (aborta se maior)

### RF-07. Nova fase na SKILL.md — "Fase 4.5: Scientific Source Pipeline"

**Posicao:** entre Fase 4 (Consolidar) e Fase 5 (Compilar).

**Gatilho automatico:**
- >= 3 URLs classificadas como `pubmed|pmc|doi` nos resultados dos subagentes
- OU flag `--scientific` explicita
- OU usuario respondeu "sim" ao opt-in em Fase 1 ("Detectei fontes cientificas — ativar pipeline especializado?")

**Fluxo:**
1. Classificar todas URLs via `classify_url.py`
2. Para cada bucket, rodar script apropriado:
   - `pubmed` → `pubmed_abstract.py` + `pmid_to_pmc.py`; se PMCID encontrado → `pmc_fulltext.py`
   - `pmc` → `pmc_fulltext.py`
   - `doi` → `unpaywall_resolver.py`; se OA PDF → `open_access_pdf.py`
   - `gov_or_guideline`, `blog_or_news` → URL direto ao NotebookLM (deixa scraper tentar)
   - `cloudflare_known` → adiciona a bucket "manual"
3. Cleanup: deletar sources existentes com titulo CAPTCHA/error
4. Upload arquivos baixados via `notebooklm source add <file> -n <notebook_id>`
5. Adicionar URLs "ok via scraper" via `notebooklm source add <url>`
6. Gerar secao de relatorio no `PESQUISA-*.md`

**Aceite:**
- [ ] 90%+ das URLs `pubmed|pmc` viram source util no NotebookLM
- [ ] Tempo total para 50 URLs cientificas <= 8 min
- [ ] Relatorio lista 3 buckets com contagem e instrucoes

### RF-08. Template de relatorio em 3 buckets

Adicionado ao final de cada `PESQUISA-*.md` quando Fase 4.5 rodou:

```markdown
## NotebookLM — Status de Upload de Fontes

**Notebook:** [link]
**Total tentadas:** N
**Data:** YYYY-MM-DD

### ✅ Auto-uploaded (N sources)

- [titulo] ({PMID}/{PMCID}/{DOI}) → file source
- ...

### ⚠ Manual upload required (N sources)

| URL | Motivo | O que fazer |
|---|---|---|
| mdpi.com/... | Cloudflare 403 | Abrir → "Download PDF" → arrastar pro NotebookLM |
| examine.com/... | Login required | Logar, copiar texto, colar como text source |
| ... |

### ❌ Paywall/Unavailable (N sources)

- URL — motivo — (sem workaround gratuito)
```

**Aceite:**
- [ ] Buckets numerados corretamente
- [ ] Bucket "manual" tem instrucao acionavel por URL
- [ ] Bucket "paywall" NAO sugere workarounds eticamente questionaveis

### RF-09. Cleanup de CAPTCHA sources antes de upload

**Input:** notebook_id
**Acao:** listar sources, detectar titulos contendo `reCAPTCHA|Checking your browser|Access denied`, deletar.

**Aceite:**
- [ ] Roda antes de qualquer upload em Fase 4.5
- [ ] Loga quantidade deletada
- [ ] Nao deleta sources validas (whitelist por ID se necessario)

### RF-10. Opt-out / flags de controle

**Flags:**
- `--skip-sci-pipeline` — desativa Fase 4.5, volta ao fluxo antigo
- `--scientific` — forca ativacao mesmo com < 3 URLs cientificas
- `--scientific-deep` (v2) — ativa fallback Playwright

**Aceite:**
- [ ] Flags documentadas em SKILL.md
- [ ] Comportamento default: auto-detect baseado em threshold (3 URLs)

---

## 7. Requisitos Nao-Funcionais

### RNF-01. Performance
- Pipeline cientifico para 50 URLs: p95 <= 8 min (inclui rate limits NCBI)
- Para 1 URL: p95 <= 10s
- Sem impacto perceptivel em pesquisas nao-cientificas (zero overhead se 0 URLs cientificas detectadas)

### RNF-02. Confiabilidade
- Graceful degradation: qualquer script pode falhar sem derrubar Fase 4.5
- Todos os scripts produzem exit codes 0 (ok) / 1 (erro) / 2 (vazio/nao encontrado)
- Retry com backoff em 429/503 (max 2 retries)

### RNF-03. Observabilidade
- Log por script em `~/.claude/skills/deep-research/logs/sci_fetch_{timestamp}.log`
- Formato: `[{LEVEL}] {timestamp} {script} {url_or_id} {status} {elapsed_ms}`
- Relatorio summary no final da fase com contagens

### RNF-04. Seguranca
- Nenhum API key hardcoded
- Env vars: `NCBI_API_KEY` (opcional), `UNPAYWALL_EMAIL` (obrigatorio para DOIs)
- User-Agent identificavel (nao esconder que e automacao): `DeepResearchSkill/1.0 ({user_email})`
- Respeitar robots.txt em `generic_web` fetches

### RNF-05. Portabilidade
- Python 3.8+ (stdlib only — urllib, json, re, time)
- Nao depender de requests/beautifulsoup/lxml (evita installs extras)
- macOS e Linux (zsh/bash) — nao testado em Windows

### RNF-06. Compatibilidade regressiva
- SKILL.md novas secoes sao aditivas — nao altera Fases 1-4 existentes
- Usuarios que nao fazem pesquisa cientifica nao veem mudanca
- Modo Update (delta research) continua funcionando

---

## 8. Consideracoes Tecnicas

### 8.1 Arquitetura

```
~/.claude/skills/deep-research/
├── SKILL.md                           # main skill (atualizado com Fase 4.5)
├── scripts/
│   ├── yt_search.py                   # existente
│   ├── yt_transcript.py               # existente
│   └── sci_fetch/                     # NOVO
│       ├── __init__.py
│       ├── classify_url.py
│       ├── pubmed_abstract.py
│       ├── pmid_to_pmc.py
│       ├── pmc_fulltext.py
│       ├── unpaywall_resolver.py
│       ├── open_access_pdf.py
│       ├── upload_to_nblm.py          # orquestrador, usa notebooklm CLI
│       └── cleanup_captcha_sources.py
├── references/
│   ├── source-routing.md              # existente
│   ├── subagent-prompts.md            # existente
│   └── sci-pipeline.md                # NOVO — detalha Fase 4.5
├── assets/
│   └── templates/
│       └── nblm-upload-report.md      # NOVO — template 3 buckets
├── evals/
│   └── test_urls_pharmacology.json    # NOVO — 86 URLs com expected classification
└── logs/                              # NOVO — gerado em runtime
```

### 8.2 APIs Externas

| API | Endpoint | Rate Limit | Key required |
|---|---|---|---|
| NCBI efetch | `eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi` | 3/s sem key, 10/s com | Opcional |
| NCBI elink | `eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi` | mesmo | Opcional |
| Unpaywall | `api.unpaywall.org/v2/{doi}?email={email}` | 100k/dia free | Email obrigatorio (free) |
| PMC HTML | `pmc.ncbi.nlm.nih.gov/articles/{pmcid}/` | no formal limit | None |
| NotebookLM CLI | `notebooklm source add` | N/A (CLI local) | Browser login |

### 8.3 Contratos de Dados

**`classify_url.py` output:**
```json
{
  "url": "https://pubmed.ncbi.nlm.nih.gov/33567185/",
  "type": "pubmed",
  "confidence": 1.0,
  "metadata": {"pmid": "33567185"}
}
```

**`pmid_to_pmc.py` output:**
```json
{"31485980": "PMC6822786", "10838651": "PMC12990180", "1434777": null}
```

**`unpaywall_resolver.py` output:**
```json
{
  "doi": "10.1089/thy.2014.0028",
  "is_oa": true,
  "oa_pdf_url": "https://www.liebertpub.com/doi/pdfplus/10.1089/thy.2014.0028",
  "oa_landing_url": "...",
  "host_type": "publisher"
}
```

### 8.4 Integracao com notebooklm CLI

```bash
# Pre-req: usuario fez `notebooklm login` uma vez
# Fase 4.5 executa:
notebooklm source add /tmp/sci_fetch/pubmed_33567185.txt -n {NB_ID} --json
notebooklm source add /tmp/sci_fetch/fulltext_PMC7054893.txt -n {NB_ID} --json
# Para URLs generic ok:
notebooklm source add "https://peterattiamd.com/outlive/" -n {NB_ID} --json
# Para cleanup antes:
notebooklm source list -n {NB_ID} --json | jq '.sources[] | select(.title | test("reCAPTCHA|Checking your browser")) | .id' | xargs -I{} notebooklm source delete {} -n {NB_ID} -y
```

### 8.5 Padroes de Erro

| Erro | Acao |
|---|---|
| NCBI 429 | Sleep 5s, retry 1x, senao skip |
| PMC HTML < 5000 chars | Provavel captcha; skip, log, adiciona a manual bucket |
| Unpaywall `is_oa=false` | Skip, adiciona a paywall bucket |
| PDF fetch nao retorna %PDF | Salva como .html, adiciona warning no relatorio |
| NotebookLM `source add` falha com auth | Abort Fase 4.5, instrui usuario a `notebooklm login` |

### 8.6 Extensao da SKILL.md (pseudo-patch)

Inserir apos secao "Fase 4: Consolidar e Priorizar":

```markdown
---

## Fase 4.5: Scientific Source Pipeline (opcional, auto-detect)

Quando os subagentes retornarem >= 3 URLs cientificas (PubMed/PMC/DOI), ativa pipeline especializado que:
- Baixa conteudo localmente usando APIs oficiais (NCBI E-utilities, Unpaywall)
- Faz upload como arquivo ao NotebookLM (nao URL — evita CAPTCHA)
- Gera relatorio de 3 buckets: auto-uploaded / manual-required / unavailable

**Ativacao:**
- Auto: threshold de 3+ URLs cientificas
- Manual: flag `--scientific`
- Skip: flag `--skip-sci-pipeline`

**Scripts:** ver `scripts/sci_fetch/` e `references/sci-pipeline.md`

**Output:** secao "NotebookLM — Status de Upload de Fontes" no PESQUISA-*.md

---
```

---

## 9. Riscos & Mitigacoes

| # | Risco | Probabilidade | Impacto | Mitigacao |
|---|---|---|---|---|
| R1 | NCBI muda XML schema de elink/efetch | Baixa | Alto | Parse defensivo; tests em `evals/` com fixtures | 
| R2 | PMC muda estrutura de URL do HTML | Media | Medio | Multiple selectors fallback; log warnings |
| R3 | notebooklm-py CLI tem breaking change | Media | Alto | Pin versao em dependencias; testar antes de upgrade |
| R4 | Cloudflare escalation para mais publishers | Alta | Medio | Lista `cloudflare_known` e extensivel; v2 Playwright fallback |
| R5 | Usuario sem NCBI API key esbarra rate limit | Alta | Baixo | Pipeline tolera 429; documentar como criar key (5 min, gratis) |
| R6 | Unpaywall rate limit excedido em pesquisas grandes | Baixa | Medio | Cache 90 dias; lote <= 50 DOIs por sessao |
| R7 | Usuario confunde "manual bucket" com erro da skill | Media | Baixo | Relatorio com linguagem clara: "Isto e normal para X" |

---

## 10. Questoes em Aberto

- **Q1:** Cache em `~/.cache/deep-research-sci/` persiste entre sessoes? TTL?
  - Proposta: sim, 90 dias. Valida em v2 apos uso real.
- **Q2:** E se usuario ja tem NotebookLM cheio (> 300 sources no plan)?
  - Proposta: detectar antes de upload, alertar, oferecer split em multiplos notebooks.
- **Q3:** Deveriamos persistir o relatorio 3-buckets em arquivo separado (`.nblm-upload-report.md`) alem de inline no PESQUISA-*.md?
  - Proposta: apenas inline em v1. Usuario pode grep/copiar.
- **Q4:** Como tratar papers em outros idiomas (nao-ingles)?
  - Proposta: out of scope pra v1. E-utilities retorna no idioma original; NotebookLM lida.
- **Q5:** Criar script para "re-tentar manual bucket" depois de usuario baixar PDFs?
  - Proposta: v2 — script `sci_fetch/manual_reupload.py` que pega todos PDFs em um dir e sobe.
- **Q6:** Validar links de DOI antes de passar pro Unpaywall (evitar 404s)?
  - Proposta: nao — Unpaywall ja retorna erro claro, desperdicio de 1 req.

---

## 11. Timeline & Fases (estimativa)

**Assumindo Claude Code como executor:**

- **Fase 1 — Scripts core (4-6h):** RF-01 a RF-06 + testes unitarios
- **Fase 2 — Orquestrador + SKILL.md update (2-3h):** RF-07, RF-09, RF-10
- **Fase 3 — Relatorio + docs (1-2h):** RF-08, references/sci-pipeline.md
- **Fase 4 — Validacao end-to-end (2h):** re-rodar pesquisa farmacologia como regression test
- **Total v1: 9-13h** (1-2 sessions focadas do Claude Code)

**v2 (Unpaywall + Playwright + cache):** +6-8h quando priorizado

---

## 12. Criterios de Aceite Global (Definition of Done)

v1 ship quando:

- [ ] Todos os scripts em `scripts/sci_fetch/` passam seus criterios individuais
- [ ] SKILL.md atualizado com Fase 4.5 + flags
- [ ] `references/sci-pipeline.md` criado com detalhes
- [ ] Regression test: executar pesquisa farmacologia novamente → >= 90% das 86 URLs resultam em source util no NotebookLM (vs 40% atual)
- [ ] Cobertura full-text: >= 80% dos PMIDs com PMC equivalente viram full-text (vs 0% atual)
- [ ] Zero sources CAPTCHA/error no NotebookLM apos execucao
- [ ] Relatorio 3-buckets renderizado corretamente em PESQUISA-*.md
- [ ] Tempo total de pipeline cientifico <= 8 min para 50 URLs
- [ ] Pesquisa nao-cientifica (ex: Next.js docs) continua funcionando sem overhead
- [ ] Modo Update (delta research) nao quebra

---

## Referencias

- Pipeline descoberto em execucao real (sessao 2026-04-22)
- Scripts prototipos em `~/.claude/skills/research/pdfs/` (nao-canonicos, serao re-escritos)
- NotebookLM CLI: `pip install notebooklm-py` (v0.3.4 usada nesta execucao)
- NCBI E-utilities docs: https://www.ncbi.nlm.nih.gov/books/NBK25500/
- Unpaywall API: https://unpaywall.org/products/api

---

**Status:** pronto para geracao de tasks. Proximo passo: "Go" para gerar `tasks-scientific-pipeline.md` com ordem de dependencia.
