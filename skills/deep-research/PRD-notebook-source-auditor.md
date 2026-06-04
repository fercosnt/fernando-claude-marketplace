# NotebookLM Source Auditor — PRD

**Autor:** Fernando Costa Neto | **Data:** 2026-04-23 | **Status:** Draft
**Nivel:** Standard
**Skill alvo:** `~/.claude/skills/notebook-source-auditor/` (nova)
**Upstream:** `PRD-scientific-pipeline.md` (deep-research v2), `references/notebook-manifest.md` (schema), conversa de arquitetura 2026-04-22/23
**Depende de:** `~/.claude/skills/deep-research/` (scripts compartilhados), `~/.claude/skills/notebooklm/` (CLI)

---

## 1. Problema & Contexto

### 1.1 Voz do Usuario

> "Atualizei a deep-research pra driblar o captcha dos artigos cientificos e escrever o manifesto, mas o problema nao some sozinho. Tenho notebooks antigos com sources CAPTCHA, duplicatas que entraram antes do dedup, e sources que eu mesmo deletei na UI do NotebookLM sem ninguem saber. A deep-research nao pode mexer nisso — ela so ADICIONA. Preciso de uma outra skill que faca o oposto: olhe pro NotebookLM, olhe pro manifesto, olhe pras pesquisas, e reconcilie. Se faltam sources, ela readiciona. Se tem duplicata, ela limpa. E nao quero que ela rode em todos os notebooks de uma vez — eu passo o link do notebook e as pastas das pesquisas relacionadas, ela audita so aquele."
> — Fernando, conversa de arquitetura 2026-04-23, apos atualizar deep-research com pipeline cientifico

### 1.2 Evidencia Quantitativa

Baseado na execucao real 2026-04-22 (pesquisa Hashimoto, 86 URLs cientificas) documentada em `PRD-scientific-pipeline.md`:

| Problema residual (apos deep-research v2 rodar) | Contagem tipica | Quem resolve hoje |
|---|---|---|
| Sources com status `captcha_pending` apos execucao cientifica | 3-8 por pesquisa (dos casos Cloudflare-known) | Usuario manual (browser → download → arrastar) |
| Sources com status `failed` (DOI invalido, paywall real, URL morta) | 2-5 por pesquisa | Ninguem — fica no manifesto sem sync |
| Duplicatas pre-existentes em notebooks antigos (antes do canonical_key) | 5-15 por notebook legado | Usuario manual (sem ferramenta) |
| Sources deletadas na UI do NotebookLM pelo usuario mas ainda no manifesto | Ocasional (user experimentando) | Ninguem — manifesto fica "otimista" |
| Gap entre fontes listadas em PESQUISA-*.md e sources efetivas no notebook | Variavel (depende de re-execucoes parciais) | Ninguem — descoberta so ao abrir o notebook |

**Exemplo concreto (sessao 2026-04-22):** apos deep-research rodar, o notebook `Hashimoto Farmacologia` tinha 110 sources, 4 com status `captcha_pending` no manifesto (MDPI/Karger/Liebert), e 2 duplicatas de PMIDs que foram adicionados tanto como URL PubMed quanto como file full-text PMC (canonical_key foi registrado como diferente por acidente).

### 1.3 MITRE Problem Framing

**Suposicoes implicitas da situacao atual:**
- Assume que a deep-research e suficiente porque escreve no manifesto em tempo real
- Assume que sources `captcha_pending` viram `ok` sozinhos com o tempo
- Assume que o usuario nao mexe manualmente no NotebookLM (falso — Fernando experimenta, deleta, re-adiciona)
- Assume que dedup canonical_key e retroativo (falso — notebooks antigos tem duplicatas legadas)

**Quem sofre:**
- **Fernando (primario):** notebook acumula ruido com o tempo (sources CAPTCHA inuteis, duplicatas), perde confianca no RAG, faz trabalho manual de limpeza periodica
- **Qualquer consumidor do NotebookLM** (Claude Desktop Health Monitor, queries futuras): retrieval cita source CAPTCHA/duplicata, degradando qualidade da analise

**How Might We:**
> Como podemos reconciliar o estado real de um NotebookLM com o manifesto e com as pesquisas-origem, resolvendo automaticamente 90%+ dos gaps (missing sources, captcha retry-aveis, duplicatas) sem que o usuario precise debugar CLI ou manifesto a mao?

### 1.4 Por Que Agora

- Deep-research v2 acabou de shipar (2026-04-23) — pipeline cientifico + manifesto criam a fundacao necessaria
- Manifesto `_notebook-manifest.md` explicitamente documenta "Como a futura notebook-source-auditor deve ler" — dependencia ja antecipada
- Sem a auditor, toda entropia de longo prazo no NotebookLM e invisivel ate a qualidade do RAG degradar
- Fernando ja tem ~4 notebooks com sources legadas pre-manifesto; quanto mais pesquisas acumularem, pior o debt

### 1.5 Relacao com deep-research

**Regra arquitetural estabelecida:** deep-research e auditor NUNCA invocam uma a outra. Ambas compartilham scripts via `~/.claude/skills/deep-research/scripts/` (notebook_manifest.py, sci_fetch/) — executor compartilhado, consumidores independentes.

| Dimensao | deep-research | notebook-source-auditor |
|---|---|---|
| Papel | Orquestrador (pesquisa → compila → adiciona) | Reconciliador (diff → retry → dedup → sync) |
| Direcao | ADICIONA sources | ADICIONA ausentes, REMOVE duplicatas/obsoletas |
| Escopo | Gera conteudo novo | Opera sobre estado existente |
| Trigger | Usuario quer pesquisa sobre topico | Usuario quer auditar notebook especifico |
| Remove do manifesto? | Nunca | **Sim — unica skill autorizada** |

---

## 2. Objetivos & Metricas

### 2.1 Metrica Primaria (North Star)

**Taxa de gaps resolvidos automaticamente por run:** dos items classificados como `missing`, `captcha_pending`, `failed (retry-avel)`, ou `duplicate`, quantos % a auditor resolve sem intervencao humana.

- **Baseline:** 0% (auditor nao existe)
- **Meta v1:** >= 90% (exclui `captcha_bypass_flow_v1` que requer humano por design)
- **Meta v2 (com Playwright fallback para Cloudflare):** >= 95%

### 2.2 Metricas Secundarias

| Metrica | Baseline | Meta v1 |
|---|---|---|
| Duplicatas por notebook apos 1 run | 5-15 (legado) | 0 |
| Tempo medio por notebook (50 sources) | N/A | <= 5 min |
| Sources `captcha_pending` com ingest_method retry-avel resolvidas | 0% | >= 80% |
| Orfas identificadas e apresentadas ao usuario com contexto | 0 | 100% |
| Rounds ate idempotencia (2 runs consecutivas = 0 mudancas) | N/A | 1 round |

### 2.3 Guardrails (nao podem regredir)

- **Zero delecoes acidentais:** nenhuma source `ok` no manifesto pode ser deletada do NotebookLM por erro de matching — dry-run por padrao + confirmacao em destrutivo
- **Manifesto nunca corrompe:** file lock compartilhado com deep-research; runs paralelos serializam
- **Compatibilidade:** deep-research continua funcionando sem mudanca; manifesto schema v1 preservado
- **Idempotencia:** rodar auditor 2x seguidas = exatamente 0 diffs na segunda (exceto por mudancas externas reais)

---

## 3. Escopo

### 3.1 Dentro do Escopo — v1 (obrigatorio)

**F1. Skill `notebook-source-auditor` em `~/.claude/skills/notebook-source-auditor/`**
- `SKILL.md` — fluxo principal
- `scripts/` — scripts especificos da auditor (diff computation, orfa detection)
- `references/` — checklists de decisao, formato do relatorio de auditoria

**F2. Invocacao per-notebook com mapeamento explicito**
- Flag `--notebook <url_ou_id>` (aceita URL completa ou UUID)
- Flag `--pesquisas <path1>,<path2>,...` (lista separada por virgula)
- Sem fuzzy matching: usuario e a fonte de verdade do mapeamento

**F3. Pull do estado atual do NotebookLM**
- Via `notebooklm source list -n <id> --json`
- Parse: extrai `source_id`, `title`, `url` (quando aplicavel), `status` (da CLI)

**F4. Computacao do 4-bucket diff**
- `missing`: canonical_keys esperados (manifesto + pesquisas) ausentes do NotebookLM
- `captcha_pending / failed (retry-avel)`: manifesto marca erro E `ingest_method` permite retry automatico
- `duplicates`: mesma canonical_key em 2+ sources do NotebookLM
- `orphans`: source no NotebookLM sem canonical_key correspondente no manifesto

**F5. Resolucao automatica por bucket**
- `missing` + `captcha_pending (url_direct|pdf_upload)` → delegar para `sci_fetch/upload_to_nblm.py`
- `duplicates` → manter source com `added_at` mais antigo como canonica; deletar as demais via `notebooklm source delete`; atualizar manifesto
- `orphans` → listar no relatorio com contexto (titulo, url se detectavel); se `--interactive`, perguntar acao por orfa
- `captcha_pending (captcha_bypass_flow_v1)` → listar no relatorio como "manual required"; nunca tentar automatico

**F6. Atualizacao do manifesto**
- Sucessos: `record_source()` (ja existe, reuso)
- Delecoes de duplicatas: NOVA funcao `mark_deleted()` ou `remove_source()` em `notebook_manifest.py` — sera adicionada como parte do escopo desta skill, nao como mudanca separada da deep-research
- `mark_deleted()` preferido sobre `remove_source()`: mantem historico (status=`deleted` + `deleted_at`) em vez de apagar fisicamente

**F7. Relatorio de auditoria em `{pesquisas_root}/_audits/<notebook_id>-<YYYY-MM-DD>.md`**
- 4 secoes (uma por bucket) com contagem, acao tomada e lista detalhada
- Summary executivo no topo (deltas por bucket)
- Em modo `--dry-run`, relatorio mostra "o que seria feito" sem executar

**F8. Flags de controle**
- `--dry-run` (default: TRUE em v1, FALSE em v2+ apos confianca): mostra diff, nao executa
- `--apply`: executa (obrigatorio explicitar para operacoes destrutivas)
- `--skip-orphans`: ignora bucket orfa (util quando usuario gerencia orfas separadamente)
- `--skip-duplicates`: ignora dedup (util se notebook tem duplicatas intencionais, caso raro)
- `--interactive`: pergunta por orfa antes de qualquer acao
- `--max-retry N`: limite de tentativas por source (default: 3)
- `--audits-dir <path>`: local custom do relatorio (default: `pesquisas/_audits/`)

**F9. Dedup canonical_key retroativo em notebooks legados**
- Detectar sources no NotebookLM cujo titulo/url resolveriam para mesma canonical_key mas foram adicionados antes do dedup
- Aplicar regras de canonical_key do `notebook_manifest.normalize_url()` retroativamente
- Merge no manifesto: uma entrada com historico de `source_ids` legados

### 3.2 Futuro — v2 (apos validacao do v1)

**F10. Bootstrap mode**
- Quando manifesto nao tem o notebook passado: popular do zero usando as pesquisas como expected state
- Mapear sources atuais do NotebookLM → canonical_keys (best effort)
- Marcar como `bootstrap_unknown` em `ingest_method` (nao tentar retry sem saber como foi)

**F11. Auditoria em batch**
- Flag `--all` ou `--batch <file>` para rodar em multiplos notebooks
- Paraleliza com limite (3 workers max, respeita file lock do manifesto)

**F12. Playwright fallback para Cloudflare-known**
- Quando source `failed` teve razao `cloudflare_block`, oferecer retry via browser headless
- Acionavel com `--scientific-deep` (mesma flag da deep-research v2)

**F13. Cron-friendly mode**
- Flag `--quiet` (so exit code + summary JSON)
- Para schedule via launchd/cron: "auditar notebook X toda sexta as 7h"

### 3.3 Versoes Futuras — v3+

- Diff visual web UI (html report com highlights)
- Slack/email notification quando orfas detectadas (integracao externa)
- Auto-promote `captcha_pending` → `failed` apos N tentativas malsucedidas sem intervencao
- Merge de notebooks duplicados (usuario acidentalmente criou 2 para mesma pesquisa)

---

## 3b. Fora do Escopo (justificativas)

| Item | Por que fora | Trade-off |
|---|---|---|
| **Criar novos notebooks** | Responsabilidade da deep-research ou do usuario na UI | Auditor opera sobre notebook existente |
| **Scientific fetch / PubMed / Unpaywall** | Ja implementado em `sci_fetch/` — auditor delega | Evita duplicacao; se sci_fetch melhora, auditor ganha de graca |
| **YouTube transcript pipeline** | Escopo da deep-research (`yt_transcript.py`) | Idem — delega quando precisa re-adicionar video |
| **Gerar conteudo novo / compilar PESQUISA-*.md** | Deep-research faz isso | Auditor e read-mostly sobre pesquisas |
| **Fuzzy matching pesquisa ↔ notebook** | Ambiguo, propenso a erro destrutivo | Usuario passa mapping explicito via flag |
| **Auditar notebooks sem passar pelas pesquisas** | Sem "expected state", auditor so consegue dedup + orfa detection (perde o bucket mais valioso: missing) | v1 exige pelo menos 1 pesquisa; v2 pode afrouxar |
| **Editar conteudo de sources existentes** | NotebookLM CLI nao suporta; fora do escopo de auditoria | Resubmit e a semantica correta |
| **Resolver conflitos entre 2 sources com mesma canonical_key mas conteudos diferentes** | Raro e ambiguo — merge semantico e problema de ML, nao de reconciliacao | Flaggar para humano decidir |
| **Audit trail enviado a sistemas externos (Notion, Slack)** | Fora do escopo core; relatorio markdown local e suficiente pra v1 | v3+ se demanda surgir |
| **UI interativa de dedup (escolher qual ficar)** | Default "mais antigo" ja cobre 95% dos casos; interativo adiciona complexidade | `--interactive` flag resolve os 5% |

---

## 4. Personas & Casos de Uso

### Persona Primaria: Fernando (usuario ativo)

- **Contexto:** dev senior, mantém ~4-8 notebooks NotebookLM (saude pessoal, projetos Beauty Smile, pesquisas tecnicas). Cada notebook acumula sources ao longo de semanas/meses.
- **Frequencia de uso prevista:** 1x/semana por notebook ativo, 1x/mes em notebooks legados
- **Conhecimento tecnico:** alto — sabe ler JSON, editor CLI, mas NAO quer fazer audit manual
- **Intolerancia critica:** qualquer delecao acidental de source `ok` = trust broken. Dry-run por default e nao-negociavel em v1.
- **Job-to-be-done:** "quero rodar 1 comando passando URL do notebook e pastas das pesquisas, e saber em <= 5 min o que ta errado e o que foi consertado — sem eu precisar abrir o manifesto ou a UI do NotebookLM"

### Persona Secundaria: Outro Claude Code user (esporadico)

- **Contexto:** dev que adotou deep-research, comecou a ter notebooks, percebe degradacao do RAG
- **Menor tolerancia a configuracao:** quer que "funcione de primeira"
- **Depende de:** relatorio claro com instrucoes para casos nao-automatizaveis

### Caso de Uso Principal

```
Given: Fernando tem notebook "Hashimoto Farmacologia" com 110 sources
       apos 3 execucoes parciais da deep-research em 2 semanas
When:  Fernando executa
       /notebook-source-auditor \
         --notebook "https://notebooklm.google.com/notebook/abc-123" \
         --pesquisas pesquisas/hashimoto-farmacologia,pesquisas/glp1-hashimoto

Then:
  - Auditor faz pull via `notebooklm source list -n abc-123 --json`
  - Le _notebook-manifest.json da pasta pesquisas/
  - Le as duas pastas passadas, extrai canonical_keys esperados
  - Computa 4 buckets:
    * missing: 3 PMIDs (captcha_pending da ultima execucao)
    * duplicates: 2 PMIDs que foram adicionados como URL + como file
    * orphans: 1 source que Fernando adicionou manualmente na UI
    * captcha_bypass_flow_v1 pending: 2 MDPI (nao tenta auto)
  - --dry-run (default) mostra o plano
  - Fernando revisa, roda de novo com --apply
  - Auditor delega re-add dos 3 missing para sci_fetch/upload_to_nblm.py
  - Auditor deleta 2 duplicatas via notebooklm source delete (mantem mais antiga)
  - Auditor lista orfa no relatorio (com titulo + url) e 2 MDPI manuais
  - Gera relatorio em pesquisas/_audits/abc-123-2026-04-23.md
```

### Caso de Uso Secundario: Notebook legado

```
Given: Notebook "tecnologia-gesta-beauty-smile" tem 87 sources, criado
       antes da deep-research v2 ter manifesto (pre-2026-03)
When:  Fernando executa com --apply (sem dry-run extra pq notebook e estavel)
Then:
  - Auditor detecta que manifesto nao tem entrada para este notebook → sugere bootstrap (v2)
  - Em v1: auditor executa so dedup + orfa detection (missing bucket vazio pq
    nenhuma canonical_key no manifesto)
  - Retorna exit code 3 (info) + relatorio indicando "bootstrap recomendado"
```

---

## 5. Epic Hypotheses

### Epic 1: Diff de 4 buckets cobre 100% dos gaps observaveis

**Hipotese:** Se a auditor classificar toda divergencia entre NotebookLM/manifesto/pesquisas em exatamente 4 buckets (missing, retry-avel, duplicate, orphan), entao qualquer situacao no mundo real cai em um dos buckets com acao clara — nenhum caso "eu nao sei o que fazer com isso".

**Tiny act of discovery:** Classificar manualmente o estado atual dos 4 notebooks de Fernando (Hashimoto, GLP1, Beauty Smile Tech, outro). Cada source/gap deve entrar em um bucket. Se >5% nao couber, refinar taxonomia antes de escrever codigo.

### Epic 2: Delegacao ao inves de reimplementacao preserva investimento

**Hipotese:** Se a auditor delegar re-add para `sci_fetch/upload_to_nblm.py` (ja existe, testado, resolve 90%+ dos casos cientificos), entao auditor foca 100% em diff/dedup/sync — sem replicar logica de classificacao/fetch/upload.

**Tiny act:** Prototipar a chamada `subprocess.run(["python", "sci_fetch/upload_to_nblm.py", ...])` com as flags certas. Validar que retorna JSON parseable e respeita o manifesto. Se nao, adicionar flag `--from-auditor` em upload_to_nblm.py (pequena mudanca na deep-research, grande ganho arquitetural).

### Epic 3: Idempotencia via manifesto como source-of-truth-sincronizada

**Hipotese:** Se a segunda run da auditor sobre mesmo notebook = 0 diffs, entao usuario pode rodar com confianca em cron/schedule sem risco de "loop de mudancas".

**Tiny act:** Rodar auditor 2x em sequencia contra notebook teste. Segundo run deve retornar exit code 0 e relatorio "nothing to reconcile". Se retornar mudancas, identificar qual estado nao foi persistido na primeira run (ex: `last_attempt_at` que muda sempre = precisa ser ignorado no diff).

### Epic 4: Dry-run default constroi confianca para remover dry-run em v2

**Hipotese:** Se v1 exige `--apply` explicito para qualquer destrutivo, entao apos 4-6 semanas de uso sem surpresas Fernando confia o suficiente para o default virar `--apply` (com opt-out via `--dry-run`).

**Tiny act:** Instrumentar contador no relatorio: "N runs em dry-run, M em apply, P divergencias entre dry-run e apply". Se P = 0 apos 10 runs, considerar flip do default em v2.

---

## 6. Requisitos Funcionais

### RF-01. Parse de invocacao e resolucao de notebook

**Input:** flags `--notebook <url|id>` + `--pesquisas <csv>`
**Output:** `{notebook_id, pesquisas_paths[], pesquisas_root}`

**Aceite:**
- [ ] Aceita URL completa (`https://notebooklm.google.com/notebook/abc-123`) e extrai ID via regex
- [ ] Aceita UUID direto (`abc-123-456`)
- [ ] Valida que cada path em `--pesquisas` existe e contem pelo menos 1 `PESQUISA-*.md`
- [ ] Deriva `pesquisas_root` do parent comum dos paths (ex: `pesquisas/`)
- [ ] Erro claro se pesquisas estao em roots diferentes: "Todas as pesquisas devem estar sob o mesmo root (para compartilhar manifesto)"

### RF-02. Pull do estado atual do NotebookLM

**Metodo:** `notebooklm source list -n <notebook_id> --json`
**Output:** lista de sources: `[{id, title, url?, type, status?}, ...]`

**Aceite:**
- [ ] Timeout 30s; retry 1x em falha transiente
- [ ] Parse estrito do JSON — falha abortiva se schema invalido (nao deve acontecer; sinaliza bug na CLI)
- [ ] Se CLI retorna erro de auth, abortar com mensagem `Run: notebooklm login` (mesma UX da deep-research)
- [ ] Se notebook_id nao existe, abortar com exit code 2

### RF-03. Extracao de expected state das pesquisas

**Input:** `pesquisas_paths[]`, `manifest` (carregado)
**Output:** `expected_sources: {canonical_key → {title, type, origin_pesquisa, ...}}`

**Logica:**
1. Para cada pesquisa path, carregar entradas do manifesto filtradas por `origin_pesquisa == slug`
2. Para cada source listada nos PESQUISA-*.md mas ausente do manifesto, tentar derivar canonical_key via `classify_url.py` + `notebook_manifest.normalize_url`
3. Union: `expected = manifest_entries ∪ pesquisa_md_entries_derived`

**Aceite:**
- [ ] Le manifesto usando `notebook_manifest.py` helpers (nao parse manual)
- [ ] Se pesquisa tem source sem canonical_key derivavel (edge case), log warning e adiciona ao relatorio como "unclassifiable"
- [ ] Dedup entre pesquisas: se mesma canonical_key em 2+ pesquisas, mantem ambas como origins (array)

### RF-04. Computacao do 4-bucket diff

**Input:** `current_nbm_sources`, `expected_sources`, `manifest`
**Output:** `{missing[], retryable[], duplicates[], orphans[]}`

**Logica:**
- `missing`: `expected_sources.keys - canonical_keys_in_current`
- `retryable`: sources do manifesto com `status ∈ {captcha_pending, failed}` E `ingest_method ∈ {url_direct, pdf_upload}` E `attempts < max_retry`
- `duplicates`: grupos de sources em `current_nbm_sources` que resolvem pra mesma canonical_key (via dedup retroativo quando necessario)
- `orphans`: sources em `current_nbm_sources` sem canonical_key correspondente no manifesto (nenhuma entrada com esse ID registrado)

**Aceite:**
- [ ] Tempo <= 2s para notebooks com 300 sources (limite max do NotebookLM)
- [ ] Diff e determinista: mesma input → mesmo output (sem ordenacao baseada em timestamp volatil)
- [ ] Sources legados sem canonical_key no manifesto sao classificadas retroativamente usando regras v1 antes de cair em orphan bucket

### RF-05. Resolucao do bucket `missing`

**Metodo:** delegar para `sci_fetch/upload_to_nblm.py` com URLs faltantes
**Flags adicionadas:** `--from-auditor` (novo, na deep-research) para sinalizar que o caller e a auditor (manifesto ja sabe disso, mas flag ajuda em log/audit)

**Aceite:**
- [ ] Chamada via subprocess, captura stdout JSON
- [ ] Pass-through: NCBI_API_KEY, UNPAYWALL_EMAIL env vars
- [ ] Se subprocess falha com exit != 0, loga no relatorio e NAO aborta — continua para outros buckets
- [ ] Cada sucesso: manifesto ja atualizado pelo upload_to_nblm.py (nao re-escreve)

### RF-06. Resolucao do bucket `retryable`

**Metodo:** por `ingest_method`:
- `url_direct` → `notebooklm source add <url> -n <id> --json`
- `pdf_upload` → `notebooklm source add <ingest_metadata.pdf_local_path> -n <id> --json`
- `captcha_bypass_flow_v1` → NAO tentar; adicionar ao relatorio como "manual required"

**Aceite:**
- [ ] Respeita `--max-retry N` (default 3)
- [ ] Apos sucesso: `record_source(status='ok', notebooklm_source_id=...)` no manifesto
- [ ] Apos falha: `record_source(status='failed', error=...)` — incrementa attempts
- [ ] Se `ingest_metadata.pdf_local_path` nao existe mais no disco, marca como `failed` com error "pdf_not_found"

### RF-07. Resolucao do bucket `duplicates`

**Estrategia:** manter source com `added_at` mais antigo; deletar as demais

**Logica:**
1. Agrupar sources por canonical_key
2. Dentro de cada grupo com N >= 2, ordenar por `added_at` ASC; primeiro = canonical, resto = to_delete
3. Para cada to_delete: `notebooklm source delete <id> -n <notebook_id> -y`
4. Chamar `mark_deleted(notebook_id, source_id, reason='duplicate_of:<canonical_id>')` no manifesto

**Aceite:**
- [ ] Default nunca deleta o mais antigo
- [ ] Em `--interactive`, pergunta qual manter (default: mais antigo)
- [ ] Se sem `--apply`, apenas lista no relatorio com recomendacao
- [ ] Nunca deixa 0 sources — se por alguma razao so ha 1 elemento no grupo apos filtro, skip

### RF-08. Resolucao do bucket `orphans`

**Padrao:** nao-destrutivo por default — lista no relatorio, nao deleta

**Comportamento por flag:**
- Default: lista em relatorio, sem acao
- `--interactive`: pergunta por orfa: `[k]eep (marcar como legitima), [d]elete (remover do NBM + manifesto), [l]ink to <slug> (adicionar como origin_pesquisa)`
- `--skip-orphans`: nao aparece no relatorio

**Aceite:**
- [ ] Nunca deleta orfa sem `--interactive` OU flag explicita `--delete-orphans` (v2)
- [ ] "link to" chama `record_source()` com a canonical_key derivada e origin_pesquisa = escolha do usuario
- [ ] "keep" marca no manifesto como `origin_pesquisa='manual_keep'` + `notebook_id` (evita perguntar de novo)

### RF-09. Nova funcao `mark_deleted()` em `notebook_manifest.py`

**Input:** `notebook_id, source_canonical_key, reason`
**Output:** manifest atualizado (status='deleted', deleted_at, deletion_reason)

**Sera adicionada ao helper existente** (nao duplicar em arquivo novo). Mudanca minima para deep-research; valor alto para auditor.

**Aceite:**
- [ ] Respeita mesmo file lock que `record_source()`
- [ ] Nao remove entrada — muda status
- [ ] `lookup_source()` retorna entradas `deleted` (caller decide se filtra ou nao)
- [ ] CLI: `python notebook_manifest.py show <root>` inclui contagem `deleted` em `by_status`

### RF-10. Dedup retroativo canonical_key

**Contexto:** notebooks legados tem sources adicionadas antes do canonical_key existir

**Metodo:**
- Para cada source em `current_nbm_sources` sem entrada no manifesto:
  - Se `url` presente: derivar canonical_key via `classify_url.py` (PMID/PMC/DOI) ou `normalize_url`
  - Se so `title`: derivar via `title:<titulo_lowercased>+<autor_principal>` (ultimo recurso)
- Agrupar: se 2+ sources resolvem pra mesma canonical_key → bucket duplicates

**Aceite:**
- [ ] 80%+ das sources legadas conseguem canonical_key derivada (nao virar todas orphans)
- [ ] Warning no relatorio quando titulo e unico sinal (confianca baixa)
- [ ] Dedup retroativo NAO reescreve manifesto em runs dry-run — so em `--apply`

### RF-11. Relatorio de auditoria

**Local:** `{pesquisas_root}/_audits/<notebook_id>-<YYYY-MM-DD>.md` (path configuravel via `--audits-dir`)
**Template:** ver RF-12 abaixo

**Aceite:**
- [ ] Sempre escrito (mesmo em dry-run, com prefixo "DRY-RUN: " no titulo)
- [ ] Multiplos runs no mesmo dia sobrescrevem (nao acumula arquivos — idempotencia)
- [ ] Inclui timestamp exato do run no corpo
- [ ] Summary no topo com contagens

### RF-12. Template do relatorio

```markdown
# Audit Report — {notebook_title} ({notebook_id})

**Data:** 2026-04-23 14:32 UTC
**Modo:** dry-run | apply
**Pesquisas auditadas:** prd-4-bibliografia, prd-5-outra
**Total de sources no NotebookLM:** 110

## Summary

| Bucket | Contagem | Acao |
|---|---|---|
| ✅ Missing — re-added | 3 | auto via sci_fetch/ |
| 🔁 Retry-avel — resolved | 2 | auto via CLI |
| 🧹 Duplicates — merged | 2 | deletado N-1, mantido mais antigo |
| ❓ Orphans — listed | 1 | manual review |
| ⚠ Captcha/manual required | 2 | listado para humano |
| 💤 No-op (ja ok) | 100 | nada a fazer |

## ✅ Missing sources re-added (3)

| Canonical Key | Titulo | Origem | Acao |
|---|---|---|---|
| pmid:33567185 | ... | prd-4 | delegado a sci_fetch → ok |
| ... |

## 🔁 Retryable sources resolved (2)

| Canonical Key | Ingest Method | Attempts antes → depois | Status |
|---|---|---|---|
| url:https://... | url_direct | 2 → 3 (ok) | ok |
| ... |

## 🧹 Duplicates merged (2)

| Canonical Key | Sources deletadas (mantida: X) | Deletadas |
|---|---|---|
| pmc:PMC7054893 | mantida: src_abc (added 2026-03-01) | src_def, src_ghi |
| ... |

## ❓ Orphans identified (1)

| Source ID | Titulo | URL detectavel? | Acao sugerida |
|---|---|---|---|
| src_xyz | "Creatine supplementation..." | https://... | Use `--interactive` para resolver |

## ⚠ Manual required (2)

| Source | Motivo | Instrucao |
|---|---|---|
| mdpi.com/... | captcha_bypass_flow_v1 | Abrir URL → Download PDF → arrastar pro notebook |

## 💤 No-op — Sources ja conformes (100)

Collapsed. Ver JSON raw em `audits/raw/{notebook_id}-{date}.json` para lista completa.
```

### RF-13. Exit codes

| Code | Significado |
|---|---|
| 0 | Sucesso; 0 ou >0 diffs aplicados |
| 2 | Invocacao invalida (flags erradas, notebook nao existe) |
| 3 | Auditoria parcial — manifesto nao tinha entrada para notebook (bootstrap recomendado em v2) |
| 4 | Ao menos 1 delecao falhou (graceful continue, reportar no relatorio) |
| 5 | Manifesto corrompido ou locked por > 30s |

**Aceite:**
- [ ] Exit code 0 em dry-run sempre (mesmo com diffs detectados)
- [ ] Exit code 4 em apply se ao menos 1 acao destrutiva falhou
- [ ] Mensagem stderr clara correspondente a cada code

### RF-14. Flags completas

| Flag | Default | Efeito |
|---|---|---|
| `--notebook <url|id>` | (required) | Target notebook |
| `--pesquisas <csv>` | (required) | Expected state source |
| `--dry-run` | TRUE (v1) | Nao executa destrutivo |
| `--apply` | FALSE (v1) | Executa (obrigatorio para destrutivo) |
| `--skip-orphans` | FALSE | Ignora bucket orfa |
| `--skip-duplicates` | FALSE | Ignora dedup |
| `--interactive` | FALSE | Pergunta por orfa |
| `--max-retry N` | 3 | Limite de tentativas |
| `--audits-dir <path>` | `pesquisas/_audits/` | Destino do relatorio |
| `--quiet` | FALSE | Reduz output stdout (v2) |

---

## 7. Requisitos Nao-Funcionais

### RNF-01. Performance
- Auditoria de notebook com 50 sources: p95 <= 5 min end-to-end (inclui pulls + fetches + writes)
- Auditoria de 300 sources (limite max NotebookLM): p95 <= 15 min
- Diff computation in-memory: p95 <= 2s (nao importa tamanho)
- Sem impacto perceptivel no manifesto em runs consecutivas (dry-run nao escreve)

### RNF-02. Confiabilidade
- Graceful degradation por bucket: falha em `missing` nao impede `duplicates`
- Exit codes precisos permitem automacao downstream
- Retry com backoff em falhas de rede (mesma politica da deep-research: max 2, exponential)
- Lock do manifesto com timeout 30s + reclaim de stale PID

### RNF-03. Idempotencia
- 2 runs consecutivas com mesmo input = 0 mudancas na segunda run
- Campos volateis (`last_attempt_at`, `updated_at`) nao participam do diff
- Relatorios do mesmo dia sobrescrevem (nao acumulam lixo)

### RNF-04. Observabilidade
- Log em `~/.claude/skills/notebook-source-auditor/logs/audit_{timestamp}.log`
- Formato: `[{LEVEL}] {timestamp} {bucket} {canonical_key} {action} {result}`
- Relatorio markdown renderizavel sem ferramenta externa

### RNF-05. Seguranca
- Nunca delete em modo dry-run (enforced por bypass do subprocess)
- Nunca escrever no manifesto em dry-run
- User-Agent identificavel quando fizer fetch indireto: herdado de sci_fetch
- Nao aceitar paths fora do projeto em `--audits-dir` sem warning (evita gravar em local inesperado)

### RNF-06. Portabilidade
- Python 3.8+ stdlib only (mesma regra da deep-research)
- macOS e Linux (zsh/bash testados)
- Dependencia exclusiva: `notebooklm` CLI (ja instalado pra deep-research funcionar)
- Python imports: `from notebook_manifest import ...` (path relativo ao dir da deep-research)

### RNF-07. Compatibilidade regressiva
- Manifesto schema v1 preservado — nova funcao `mark_deleted()` adiciona campos (`deleted_at`, `deletion_reason`) sem quebrar leitores antigos
- Sources com status `deleted` continuam aparecendo em `lookup_source()` (filtragem e responsabilidade do caller)
- Deep-research v2 continua funcionando sem modificacao alem de:
  - (opcional) adicionar flag `--from-auditor` em `sci_fetch/upload_to_nblm.py` para telemetria de origem
  - Adicionar funcao `mark_deleted()` em `notebook_manifest.py` (pura adicao, nao-breaking)

---

## 8. Consideracoes Tecnicas

### 8.1 Arquitetura

```
~/.claude/skills/
├── deep-research/                      # EXISTENTE
│   ├── scripts/
│   │   ├── notebook_manifest.py        # + mark_deleted() (NOVO)
│   │   └── sci_fetch/
│   │       ├── classify_url.py         # reusado
│   │       ├── upload_to_nblm.py       # + flag --from-auditor (NOVO, opcional)
│   │       └── cleanup_captcha_sources.py  # reusado
│   └── references/
│       └── notebook-manifest.md        # EXISTENTE (schema canonico)
│
├── notebook-source-auditor/            # NOVO
│   ├── SKILL.md                        # fluxo principal
│   ├── scripts/
│   │   ├── auditor.py                  # main entry point
│   │   ├── diff_engine.py              # compute 4-bucket diff
│   │   ├── retroactive_dedup.py        # canonical_key para sources legados
│   │   ├── orphan_handler.py           # interativo + listagem
│   │   ├── report_writer.py            # gera audit report .md
│   │   └── url_extract.py              # extrai notebook_id de URL
│   ├── references/
│   │   ├── audit-flow.md               # detalhamento do fluxo
│   │   ├── bucket-decision-matrix.md   # como cada bucket mapeia em acao
│   │   └── integration-with-deep-research.md  # como delega pra sci_fetch
│   ├── assets/
│   │   └── templates/
│   │       └── audit-report-template.md
│   ├── evals/
│   │   └── test_scenarios.json         # 5-10 cenarios fixtures pra regression
│   └── logs/                           # runtime
│
└── notebooklm/                         # EXISTENTE
    └── (CLI usada via subprocess)
```

### 8.2 Contratos de Dados

**Input resolvido (apos RF-01):**
```python
{
    "notebook_id": "abc-123-456",
    "notebook_url": "https://notebooklm.google.com/notebook/abc-123-456",
    "pesquisas_paths": ["pesquisas/hashimoto", "pesquisas/glp1-hashimoto"],
    "pesquisas_root": "pesquisas/",
    "manifest_path": "pesquisas/_notebook-manifest.json",
    "flags": {
        "dry_run": True,
        "apply": False,
        "interactive": False,
        "max_retry": 3,
        "audits_dir": "pesquisas/_audits/",
    }
}
```

**Current NBM state (apos RF-02):**
```json
{
    "sources": [
        {
            "id": "src_abc",
            "title": "Effects of GLP-1...",
            "type": "article",
            "url": "https://pubmed.ncbi.nlm.nih.gov/33567185/",
            "status": "ok"
        }
    ],
    "total_count": 110,
    "fetched_at": "2026-04-23T14:30:00Z"
}
```

**Expected state (apos RF-03):**
```json
{
    "sources": {
        "pmid:33567185": {
            "title": "Effects of GLP-1...",
            "type": "article",
            "origin_pesquisas": ["hashimoto-farmacologia", "glp1-hashimoto"],
            "manifest_entry": { ... entrada completa do manifesto ... },
            "last_known_status": "ok"
        }
    }
}
```

**Diff output (apos RF-04):**
```json
{
    "missing": [
        {"canonical_key": "pmid:123", "expected": {...}}
    ],
    "retryable": [
        {"canonical_key": "url:...", "manifest_entry": {...}, "ingest_method": "url_direct"}
    ],
    "duplicates": [
        {
            "canonical_key": "pmc:PMC7054893",
            "sources": [
                {"id": "src_abc", "added_at": "2026-03-01T..."},
                {"id": "src_def", "added_at": "2026-03-15T..."}
            ],
            "keep": "src_abc",
            "delete": ["src_def"]
        }
    ],
    "orphans": [
        {"id": "src_xyz", "title": "...", "derived_canonical_key": null}
    ]
}
```

**Audit report (apos RF-11/12):** markdown renderizado conforme template

### 8.3 Integracao com Scripts Existentes

#### Chamada a sci_fetch/upload_to_nblm.py (delegate)

```python
import json
import subprocess
from pathlib import Path

def delegate_missing_to_scifetch(
    urls: list[str],
    notebook_id: str,
    pesquisa_slug: str,
    pesquisas_root: Path,
) -> dict:
    """Delegate re-add of missing URLs to deep-research's sci_fetch orchestrator."""
    # Write URLs to temp file (upload_to_nblm.py expects file input)
    urls_file = Path(f"/tmp/auditor-missing-{notebook_id}.txt")
    urls_file.write_text("\n".join(urls))

    result = subprocess.run(
        [
            "python",
            str(Path.home() / ".claude/skills/deep-research/scripts/sci_fetch/upload_to_nblm.py"),
            "--urls", str(urls_file),
            "--notebook", notebook_id,
            "--pesquisa", pesquisa_slug,
            "--pesquisas-root", str(pesquisas_root),
            "--from-auditor",  # NEW flag, opcional telemetria
        ],
        capture_output=True,
        text=True,
        timeout=600,  # 10 min max
    )

    if result.returncode != 0:
        return {"status": "failed", "error": result.stderr, "bucket_summary": None}

    return {"status": "ok", "bucket_summary": json.loads(result.stdout)}
```

#### Import direto de notebook_manifest (library mode)

```python
import sys
from pathlib import Path

# Add deep-research scripts to path
sys.path.insert(0, str(Path.home() / ".claude/skills/deep-research/scripts"))

from notebook_manifest import (
    record_source,
    lookup_source,
    normalize_url,
    mark_deleted,  # NOVO — parte do escopo desta skill
)
```

#### Chamada a notebooklm CLI

```python
def list_notebook_sources(notebook_id: str) -> dict:
    """Pull current state from NotebookLM."""
    result = subprocess.run(
        ["notebooklm", "source", "list", "-n", notebook_id, "--json"],
        capture_output=True, text=True, timeout=30,
    )
    if "authentication" in result.stderr.lower():
        raise AuthError("Run: notebooklm login")
    return json.loads(result.stdout)

def delete_notebook_source(notebook_id: str, source_id: str) -> bool:
    """Delete a duplicate from NotebookLM."""
    result = subprocess.run(
        ["notebooklm", "source", "delete", source_id, "-n", notebook_id, "-y"],
        capture_output=True, text=True, timeout=30,
    )
    return result.returncode == 0
```

### 8.4 Nova funcao `mark_deleted()` (mudanca em notebook_manifest.py)

```python
def mark_deleted(
    *,
    manifest_path: Path,
    notebook_id: str,
    canonical_key: str,
    reason: str,  # "duplicate_of:src_abc" | "orphan_user_choice" | "missing_from_nbm"
) -> dict | None:
    """Mark a source as deleted in the manifest. Preserves history.

    Unlike `record_source()`, this is destructive-by-intent — only auditor calls.
    """
    manifest_path = Path(manifest_path)
    lock_path = manifest_path.with_suffix(manifest_path.suffix + ".lock")

    with _FileLock(lock_path):
        data = _load_or_bootstrap(manifest_path)
        nb = data.get("notebooks", {}).get(notebook_id)
        if not nb:
            return None

        for src in nb.get("sources", []):
            if src.get("canonical_key") == canonical_key:
                src["status"] = "deleted"
                src["deleted_at"] = _now_iso()
                src["deletion_reason"] = reason
                nb["updated_at"] = _now_iso()
                _atomic_write(manifest_path, data)
                return src
        return None
```

### 8.5 Padroes de Erro

| Erro | Acao |
|---|---|
| NotebookLM CLI auth fail | Abort exit 5 + mensagem `notebooklm login` |
| notebook_id nao existe | Abort exit 2 |
| Manifesto corrompido | Abort exit 5, sugerir backup + restore manual |
| Lock timeout 30s | Abort exit 5, sugerir checar processo paralelo |
| Pesquisa path nao existe | Abort exit 2 antes de tocar NotebookLM |
| Subprocess sci_fetch timeout | Graceful: continue com outros buckets, reportar |
| Delete single source falha | Graceful: continue outras delecoes, exit 4 ao final |
| PDF local path desapareceu | Graceful: marcar source como failed(error="pdf_not_found") |

### 8.6 Exemplo de Invocacao End-to-End

```bash
# Dry-run (default em v1)
python ~/.claude/skills/notebook-source-auditor/scripts/auditor.py \
  --notebook "https://notebooklm.google.com/notebook/abc-123" \
  --pesquisas pesquisas/hashimoto-farmacologia,pesquisas/glp1-hashimoto

# Apply com interacao para orfas
python ~/.claude/skills/notebook-source-auditor/scripts/auditor.py \
  --notebook abc-123 \
  --pesquisas pesquisas/hashimoto-farmacologia,pesquisas/glp1-hashimoto \
  --apply --interactive

# Output:
# Pulled 110 sources from notebook abc-123
# Loaded expected state: 113 canonical_keys from 2 pesquisas
# Diff:
#   missing: 3 (captcha_pending from last run)
#   retryable: 2 (url_direct, attempts < 3)
#   duplicates: 2 groups (4 sources → keep 2, delete 2)
#   orphans: 1 (user-added via UI)
#
# --apply set, executing...
# [1/8] Delegating 3 missing to sci_fetch... ok (3/3)
# [2/8] Retrying 2 retryable... ok (2/2)
# [3/8] Deleting 2 duplicates... ok (2/2)
# [4/8] Orphan 'Creatine supplementation...': [k]eep [d]elete [l]ink? l
# [5/8] Link to which pesquisa? [1] hashimoto-farmacologia [2] glp1-hashimoto? 1
# [6/8] Linked orphan to hashimoto-farmacologia
# [7/8] Manifesto updated: +5 sources, 2 marked deleted
# [8/8] Report written: pesquisas/_audits/abc-123-2026-04-23.md
#
# Exit: 0
```

---

## 9. Riscos & Mitigacoes

| # | Risco | Probabilidade | Impacto | Mitigacao |
|---|---|---|---|---|
| R1 | Delecao acidental de source `ok` legitima por erro de canonical_key | Baixa | Critico | Dry-run default v1; confirmacao em `--apply`; teste em evals/ com 86 URLs do scientific-pipeline |
| R2 | Manifesto corrompido por escrita concorrente | Baixa | Alto | File lock PID-based ja implementado em notebook_manifest.py; auditor usa o mesmo helper |
| R3 | Auditor e deep-research rodando em paralelo geram race | Media | Medio | Lock serializa; auditor detecta em <30s ou aborta exit 5 |
| R4 | Dedup retroativo agrupa sources de papers diferentes (falsos positivos) | Media | Alto | Warnings quando canonical_key deriva de `title:` apenas; `--interactive` para revisao |
| R5 | Notebook com > 300 sources demora > 15min | Baixa | Baixo | Paginacao da CLI; timeout adequado; warning ao usuario |
| R6 | Usuario esquece de passar pesquisas relacionadas → missing bucket vazio falso | Media | Medio | Warning se expected_sources empty; sugerir quais pesquisas usar baseado em `origin_pesquisa` no manifesto |
| R7 | `mark_deleted()` breaking change no manifesto | Baixa | Alto | Campos adicionados sao optional; schema version mantida em 1; leitor antigo ignora campos extras |
| R8 | sci_fetch/upload_to_nblm.py muda contrato de saida sem auditor saber | Media | Medio | Versionar flag `--from-auditor`; auditor valida schema da resposta antes de interpretar |
| R9 | Usuario confunde orfa com bug da auditor ("porque ele nao sabe dessa source?") | Alta | Baixo | Relatorio explica: "orfa = voce adicionou manualmente ou veio de pesquisa nao passada" |
| R10 | Bootstrap (v2) mal-feito em notebook legado gera falsas orfas | Media | Medio | v2 trata — nao bloqueia v1; v1 exit code 3 indica "bootstrap recomendado" |

---

## 10. Questoes em Aberto

- [ ] **Q1:** Relatorios do mesmo dia devem sobrescrever ou anexar com timestamp? — Proposta: sobrescrever (idempotencia); raw JSON em `_audits/raw/` para audit trail — **Responsavel:** Fernando — **Prazo:** antes de v1 ship
- [ ] **Q2:** Em orfas, como apresentar "link to pesquisa" quando user passou 5+ pesquisas? — Proposta: multiple choice indexado; se > 5, pedir numero ao inves de nome — **Responsavel:** TBD em UX review
- [ ] **Q3:** `mark_deleted()` apaga entrada apos N dias (garbage collection) ou mantem pra sempre? — Proposta: manter pra sempre em v1; v3+ GC configuravel — **Responsavel:** Fernando
- [ ] **Q4:** Deve haver comando `undo` para reverter ultima auditoria? — Proposta: nao em v1; audit report serve como paper trail; v2+ considerar — **Responsavel:** aberto
- [ ] **Q5:** Como tratar notebook onde o usuario deletou MUITAS sources na UI (orfas reversas: manifesto tem, nbm nao)? — Proposta: bucket novo "stale_manifest"; `mark_deleted()` essas com reason `deleted_from_nbm_externally` — **Responsavel:** incluir no v1 se baixo esforco
- [ ] **Q6:** Se pesquisa foi renomeada (slug mudou), auditor ainda encontra origin_pesquisa? — Proposta: v1 falha com warning; v2 fuzzy match + ask user — **Responsavel:** Fernando
- [ ] **Q7:** Integrar com Notion (log de auditoria na DB Orientacoes AI do Health Monitor)? — Proposta: out of scope v1; pode ser hook v3+ — **Responsavel:** depois de validar adocao v1
- [ ] **Q8:** Schedule automatico (cron "toda sexta audita notebook X")? — v2 com `--quiet`; v1 e manual — **Responsavel:** v2

---

## 11. Timeline & Fases (estimativa)

**Assumindo Claude Code como executor:**

- **Fase 1 — Fundacao (3-4h):**
  - `mark_deleted()` em `notebook_manifest.py` (deep-research)
  - `url_extract.py` (parser de notebook URL)
  - Scaffolding da skill (SKILL.md + estrutura de pastas)
  - evals/test_scenarios.json com 5 cenarios fixtures

- **Fase 2 — Diff engine + Buckets (4-5h):**
  - `diff_engine.py` (RF-03, RF-04)
  - `retroactive_dedup.py` (RF-10)
  - Unit tests contra fixtures

- **Fase 3 — Resolvers (4-6h):**
  - Missing → sci_fetch delegation (RF-05)
  - Retryable resolver (RF-06)
  - Duplicates resolver (RF-07)
  - Orphan handler interativo (RF-08)

- **Fase 4 — Relatorio + CLI (2-3h):**
  - `report_writer.py` + template (RF-11, RF-12)
  - `auditor.py` main entry point (RF-01, RF-14, RF-13)
  - Exit codes

- **Fase 5 — Validacao e regression (2-3h):**
  - Rodar em notebook Hashimoto (baseline da evidencia): esperar resolucao de captcha_pending + duplicatas conhecidas
  - Rodar 2x seguidas (idempotencia)
  - Rodar com deep-research em paralelo (lock test)

- **Fase 6 — Docs (1-2h):**
  - `references/audit-flow.md`
  - `references/bucket-decision-matrix.md`
  - `references/integration-with-deep-research.md`
  - Update CLAUDE.md se aplicavel

**Total v1: 16-23h** (2-3 sessions focadas do Claude Code)

**v2 (Bootstrap + Batch + Playwright fallback):** +6-8h quando priorizado

---

## 12. Criterios de Aceite Global (Definition of Done)

v1 ship quando:

- [ ] `notebook_manifest.py::mark_deleted()` existe e tem testes
- [ ] Skill `notebook-source-auditor` completa em `~/.claude/skills/notebook-source-auditor/`
- [ ] SKILL.md documenta todas as flags da RF-14
- [ ] Todos os 14 requisitos funcionais passam seus criterios de aceite
- [ ] Regression test: rodar em notebook Hashimoto pos-deep-research v2 resolve pelo menos os 4 captcha_pending conhecidos e as 2 duplicatas PubMed/PMC
- [ ] Idempotencia: 2 runs consecutivas = segundo relatorio sem buckets com acao
- [ ] Dry-run nao modifica manifesto nem NotebookLM (verificavel por `git diff` + `notebooklm source list`)
- [ ] `--apply` em notebook com >= 1 item em cada bucket: todos resolvidos com sucesso OU relatorio mostra exatamente por que nao
- [ ] Deep-research continua funcionando sem mudancas nao-coordenadas
- [ ] Relatorio markdown renderizavel, com summary table no topo
- [ ] Exit codes precisos para automacao
- [ ] File lock serializa auditor + deep-research em paralelo (test manual: spawn 2 processos)
- [ ] evals/ cobre 5+ cenarios incluindo: (a) notebook limpo, (b) notebook com duplicatas, (c) notebook com captcha_pending retry-avel, (d) notebook com orfa, (e) notebook legado sem manifesto

---

## Referencias

- `~/.claude/skills/deep-research/SKILL.md` (v2 com Fase 4.5)
- `~/.claude/skills/deep-research/PRD-scientific-pipeline.md` (contexto upstream)
- `~/.claude/skills/deep-research/references/notebook-manifest.md` (schema canonico)
- `~/.claude/skills/deep-research/scripts/notebook_manifest.py` (helper compartilhado)
- `~/.claude/skills/deep-research/scripts/sci_fetch/upload_to_nblm.py` (orquestrador delegado)
- `~/.claude/skills/notebooklm/SKILL.md` (CLI consumida via subprocess)
- NotebookLM CLI: `pip install notebooklm-py` (v0.3.4+)
- Conversa de arquitetura: 2026-04-22 / 2026-04-23 (decisao de skill separada + per-notebook invocation)

---

**Status:** pronto para geracao de tasks. Proximo passo: `gera as tasks` para criar `tasks-notebook-source-auditor.md` com ordem de dependencia e scoping atomico por sessao Claude Code.
