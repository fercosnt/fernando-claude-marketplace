---
name: deck-scientific
description: Cria STORYBOARD (oral/keynote) ou POSTER.md (modo poster, D8) para apresentacao cientifica em congressos (CIOSP/ICOI/AAOMS/IADR). 4 modos. Triggers: paper, poster, abstract, RCT, IMRAD, GRADE.
intent: action
effort: high
nb_ids:
  - 7f1b2e2b-4ba4-40de-ba56-ca2f55e2c0da
  - 1635d16b-773c-480d-89c2-79c717f4b2e1
references:
  - references/framework-imrad-grade.md
  - references/framework-tufte-doumont.md
  - references/framework-better-poster-morrison.md
  - references/compliance-consort-strobe-prisma-coi.md
  - references/eval-cases-scientific.md
assets:
  - assets/templates/storyboard-skeleton-oral.md
  - assets/templates/poster-skeleton.md
  - assets/checklists/scientific-checklist.md
---

# deck-scientific

Skill vertical do plugin **deck-builder**. Estrutura apresentacoes cientificas e academicas para congressos de saude. **Modo `poster` produz POSTER.md** com schema proprio (D8); demais modos produzem STORYBOARD.md padrao (§10.2 do SHARED.md).

Nao gera arte final — apos a estrutura, designer humano (ou IA com prompts gerados por `deck-image-prompts`) executa as figuras.

## Quando ativa

**Modo encadeado:** invocada pelo `deck-orchestrator` quando o input bate na rota cientifica (§10.3).

**Modo direto:** `/deck-scientific` ou frases que mencionem:
- Congressos: AAOMS, ICOI, CIOSP, IADR, EAO, AAID, FDI, ADA, EuroPerio
- Tipos de output: poster cientifico, abstract, oral presentation, keynote academico
- Tipos de estudo: RCT, systematic review, meta-analise, case series, cohort, case report
- Frameworks: IMRAD, GRADE, Better Poster, CONSORT, STROBE, PRISMA

## Os 4 modos

| Modo | Tempo / Espaco | Output | Estrutura | Slides/Painel |
|------|---------------|--------|-----------|---------------|
| `poster` | Painel A0/A1 | **POSTER-{slug}.md** (D8) | Better Poster Morrison + key-finding centro | 1 painel |
| `oral-short` | 7 min | STORYBOARD.md | IMRAD destilado | 7-8 slides |
| `oral-long` | 12-20 min | STORYBOARD.md | IMRAD completo | 15-18 slides |
| `keynote` | 45 min | STORYBOARD.md | 3 atos + Q&A bloco | 30-40 slides |

**Como deduzir o modo:**
- Usuario diz "poster" / "painel" / menciona congresso com formato poster → `poster`
- Usuario diz "oral 5-8 min" ou "lightning talk" → `oral-short`
- Usuario diz "oral 12-20 min" / "session talk" → `oral-long`
- Usuario diz "keynote" / "plenaria" / "45 min" / "1h" → `keynote`
- Ambiguo → perguntar via AskUserQuestion oferecendo 4 opcoes

## Entrevista

### Universal (§10.1) — sempre faz primeiro

U1-U6 (objetivo, audiencia, duracao, formato, big idea, marca).

### Vertical X1-X5 (depois de U1-U6)

| # | Pergunta | Tipo / formato |
|---|----------|----------------|
| X1 | Congresso + slot exato (min de fala ou tipo de painel A0/A1)? | texto |
| X2 | Tipo de estudo? | RCT / systematic review / meta-analise / case series / cohort / case report / outro |
| X3 | Outcome primario + secundarios? | texto |
| X4 | Conflito de interesse declaravel (industria, autoria, financiamento)? | texto OU "nenhum" |
| X5 | Audiencia mista (clinicians + researchers + industria)? | sim / nao + perfil dominante |

**Defaults sensatos quando inferiveis:**
- Se `U6 = Fotona` e X4 vazio → preencher "consultor/palestrante Fotona" e pedir confirmacao
- Se X2 nao informado mas brief mencionar "50 pacientes" / "n = 50" → inferir `case series` (confirmar)

## Protocolo de execucao

1. **Identificar modo** (deduzir do input ou perguntar)
2. **Rodar entrevista universal U1-U6** (rapido, ≤2 min)
3. **Rodar entrevista vertical X1-X5**
4. **Consultar NBs** (NB1 sempre + NB2 cientifico, max 3 queries):
   ```bash
   notebooklm use 1635d16b-773c-480d-89c2-79c717f4b2e1
   notebooklm ask "{tipo-estudo} + {outcome} + GRADE + framework reporting + Big Idea" --max-citations 5
   ```
   Falha de NB nao bloqueia — degrada com warning.
5. **Gerar output conforme modo:**
   - `poster` → `POSTER-{slug}-{HHmm}.md` usando `assets/templates/poster-skeleton.md` (D8)
   - `oral-short` / `oral-long` / `keynote` → `STORYBOARD-{slug}-{HHmm}.md` usando schema §10.2
6. **Invocar `deck-image-prompts` SE modo oral/keynote** (override D5: inclui tipo `dados` na whitelist para graficos cientificos)
7. **Aplicar compliance scientific** (3 tiers — §"Compliance" abaixo)
8. **Anexar checklist `assets/checklists/scientific-checklist.md`**

## Output path

Schema §10.4 do SHARED.md:
- Default: `$DECKS_DIR/{YYYY-MM}/STORYBOARD-{slug}-{HHmm}.md`
- Modo poster (D8): `$DECKS_DIR/{YYYY-MM}/POSTER-{slug}-{HHmm}.md`
- Slug: kebab-case do Big Idea (U5), max 30 chars

## Frameworks aplicados

Detalhe em `references/`. Resumo:

- **IMRAD** (Introduction → Methods → Results → Discussion) — coluna vertebral de todos os modos.
- **GRADE** — nivel de evidencia explicito por outcome (High / Moderate / Low / Very Low).
- **Tufte** — data-ink ratio alto, small multiples, sem chartjunk. Aplicado em figuras.
- **Doumont** — trees, maps, theorems (afirmacao assertiva + evidencia).
- **Better Poster Morrison** — key-finding GRANDE no centro, sumario destacado, detalhes pequenos em volta. **Modo poster apenas.**

Ver `references/framework-imrad-grade.md`, `references/framework-tufte-doumont.md`, `references/framework-better-poster-morrison.md`.

## Schema POSTER.md (modo poster — D8)

Modo `poster` **NAO gera STORYBOARD**. Gera arquivo `POSTER-{slug}-{HHmm}.md` com schema proprio.

Template completo em [assets/templates/poster-skeleton.md](assets/templates/poster-skeleton.md). Esqueleto resumido:

```markdown
# Poster: {titulo-paper}

## Meta
- Skill geradora: deck-scientific (modo poster)
- Congresso: {X1}
- Tipo de estudo: {X2}
- Outcome primario: {X3}
- COI: {X4 declarado}
- Big Idea: {U5}
- Authors: {lista}
- Tamanho painel: A0 / A1 / custom
- Estilo: Better Poster Morrison
- max_ctas: 3 (override scientific D14)
- Reporting guideline: CONSORT / STROBE / PRISMA / CARE
- Gerado em: {ISO date}

## Estrutura Visual (Better Poster)

### Centro — Key Finding (GRANDE)
{1 frase com o achado principal + 1 numero chave}

### Painel Esquerdo — Background
{2-3 paragrafos: contexto + research question}

### Painel Inferior Esquerdo — Methods (small)
{design + sample + outcome + analise}

### Painel Direito — Results (figuras)
{1-2 figuras + tabela}

### Painel Inferior Direito — Conclusion (small)
{Discussion destilada + significado clinico + limitacoes}

### Rodape — References + COI + Acknowledgments + QR Code
{papers + COI + grants + QR pra paper completo}

## CTAs (max 3 — D14)
1. Read paper: {DOI ou QR}
2. Replicate: {protocolo / OSF link}
3. Contact author: {email autor responsavel}

## Compliance & Disclaimers (3 tiers — D7)
🔴 Issues bloqueantes
🟡 Verificar
✅ OK
```

## Output STORYBOARD (modos oral / keynote)

Schema §10.2 do SHARED.md. **`max_ctas: 3`** declarado no cabecalho `## Meta` (override scientific — D14).

CTAs scientific canonicos:
- **Read paper** — DOI ou QR code para paper completo
- **Replicate** — protocolo descrito + OSF/Zenodo/repositorio aberto
- **Contact author** — email do autor responsavel ou ORCID

### Modo `oral-short` (7-8 slides, 7 min)

Slide 1 — Capa + autores + COI (60s budget total para slide 1 + 2)
Slide 2 — Background + research question
Slide 3 — Methods (design + sample + outcome operacionalizado)
Slides 4-5 — Results principais (90-120s, 1 figura/tabela por slide)
Slide 6 — Discussion + significado clinico
Slide 7 — Limitacoes + futuro
Slide 8 — Take-home + QR paper + 3 CTAs

### Modo `oral-long` (15-18 slides, 12-20 min)

IMRAD completo expandido:
- 1-2: Capa + COI + agenda
- 3-5: Introduction (background + gap + research question)
- 6-9: Methods detalhado (design + sample + outcome operacionalizado + analise estatistica + reporting guideline citado)
- 10-13: Results (4 slides — 1 figura/tabela por slide, Tufte)
- 14-16: Discussion (significado + comparacao com literatura + limitacoes + erro tipo II se aplicavel)
- 17-18: Take-home + futuro + 3 CTAs + Q&A trigger

### Modo `keynote` (30-40 slides, 45 min)

3 atos + Q&A bloco preparado:

- **Ato 1 (10-12 min, 10 slides):** Estado da arte + Big Idea como gancho. Slide 1 capa + COI. Slides 2-3 panorama campo. Slide 4 research question central. Slides 5-10 contexto historico + papers fundadores.
- **Ato 2 (15-20 min, 18 slides):** Metodos + resultados de multiplos estudos do grupo. Cada estudo: 1 slide methods + 2-3 slides results (graficos com `dados` na whitelist — override D5). GRADE level explicito por outcome.
- **Ato 3 (8-10 min, 7 slides):** Implicacoes + futuro + chamada a colaboracao + 3 CTAs.
- **Q&A bloco preparado (5-10 min):** 4-6 perguntas antecipadas + respostas curadas (slide oculto/apendice).

## Image-prompts — override scientific (D5)

Whitelist canonica `deck-image-prompts` ([SHARED.md §10.2](../../PRD/bundles/SHARED.md)):
- Preencher: capa | problema | conceitual | comparativo | demo | prova-social
- Skip: dados | financeiro | CTA | disclaimer | agradecimento | apendice

**Override `deck-scientific` (D5):** **inclui `dados` na whitelist** porque graficos cientificos sao imagens criticas (forest plot, Kaplan-Meier, scatter plot, small multiples). Ao invocar `deck-image-prompts` em modo oral/keynote, passa flag `--include-dados`.

Modo poster nao invoca `deck-image-prompts` — figuras do poster sao referencias diretas ao paper (Tufte aplicado pelo autor).

## Compliance scientific (D7 — 3 tiers)

Detalhe completo em [references/compliance-consort-strobe-prisma-coi.md](references/compliance-consort-strobe-prisma-coi.md).

### 🔴 BLOCKER (resolver antes de apresentar)

- p-value reportado incorretamente: "p<0.05" sem contexto, ou "p=0.06" descrito como "tendencia significativa"
- Cherry-picking: selecao seletiva de outcomes favoraveis sem reportar os negativos
- COI nao declarado quando aplicavel (industria, autoria, financiamento, equity)
- Numeros sem unidade ou denominador ("80% de melhora" sem n)
- Reporting guideline ausente quando obrigatorio (RCT sem CONSORT, cohort sem STROBE, meta-analise sem PRISMA)
- Plagio nao-citado (figura ou frase de paper alheio sem citacao)

### 🟡 VERIFICAR antes

- CONSORT / STROBE / PRISMA / CARE citado conforme tipo de estudo?
- Erro tipo II discutido em estudos com resultado nao-significativo (poder estatistico)?
- Limitacoes explicitas no slide Discussion?
- IC95% reportado junto com effect size?
- GRADE level explicito por outcome (nao so o primario)?

### ✅ OK (confirmacoes)

- p-value contextualizado (com IC95% + effect size)
- GRADE level explicito por outcome
- COI declarado slide 1
- Reporting guideline citado (CONSORT/STROBE/PRISMA/CARE)
- Sample size justificado (calculo de poder ou rationale)
- Outcomes pre-registrados (OSF / ClinicalTrials.gov / PROSPERO)

## Regras inviolaveis (DoD)

- **D8:** Modo `poster` SEMPRE gera POSTER.md (nao STORYBOARD). Schema em [assets/templates/poster-skeleton.md](assets/templates/poster-skeleton.md).
- **D5 override:** Modos oral/keynote incluem `dados` na whitelist `deck-image-prompts`.
- **D14:** `max_ctas: 3` declarado na Meta (read paper / replicate / contact author). Validado pelo `deck-reviewer`.
- **D7:** Bloco "Compliance & Disclaimers" com 3 tiers (🔴/🟡/✅) ao final do output.
- **COI no slide 1 sempre** — independente de ter COI declaravel ou nao (se nao tem, escrever "Nenhum COI a declarar").
- **p-value sempre contextualizado** — IC95% + effect size + GRADE level quando aplicavel.
- **Reporting guideline citado** conforme tipo de estudo (X2):
  - RCT → CONSORT
  - Cohort / case-control / cross-sectional → STROBE
  - Systematic review / meta-analise → PRISMA
  - Case report / case series → CARE
- **Big Idea (U5)** aparece como Take-home no ultimo slide (ou centro do poster).

## NBs a consultar

- **NB1 Core Transversal** (`7f1b2e2b-...`) — frameworks gerais, narrativa, Heath SUCCES
- **NB2 Densas** (`1635d16b-...`) — pasta `apresentacoes-cientificas-congressos-saude` (101 sources: Alley, Hofmann, Carter, Tufte, Doumont, Better Poster Morrison, CONSORT, STROBE, PRISMA, GRADE)

Templates de query em §10.6 do SHARED.md.

## Eval cases

3 cases em [references/eval-cases-scientific.md](references/eval-cases-scientific.md):

1. **CIOSP oral 7min** — sistema review Er:YAG vs convencional periimplantite → STORYBOARD com 8 slides + COI + GRADE moderate
2. **IADR poster** — case series LightWalker clareamento (50 pacientes) → POSTER.md (D8) com key finding centro
3. **ICOI keynote 45min** — futuro reabilitacao implantossuportada → STORYBOARD com 35 slides + 3 atos + Q&A bloco

## Cross-skill

- **Encadeada por:** `deck-orchestrator` (rota cientifica §10.3)
- **Encadeia:** `deck-image-prompts` (modos oral/keynote, com `--include-dados` flag override D5)
- **Followup recomendado:** `deck-reviewer` (valida compliance + max_ctas=3 + COI slide 1)

## Anti-patterns (NAO fazer)

- Gerar STORYBOARD em modo poster (deve ser POSTER.md — D8)
- Omitir COI slide 1 mesmo quando nao ha COI a declarar (escrever "Nenhum COI" e melhor que omitir)
- "p<0.05" sem IC95% ou effect size
- Mais de 3 CTAs (override scientific D14 — read paper / replicate / contact author)
- Slides oral-short com mais de 1 ideia (1 ideia/slide e regra)
- Poster com texto grande e key-finding pequeno (inverte Better Poster Morrison)
- Chartjunk (Tufte) — gradientes 3D, dropshadow em barras, pizza chart com >5 fatias
- Esquecer reporting guideline conforme tipo de estudo (CONSORT/STROBE/PRISMA/CARE)

## v1.1 — Adendo: `modo_entrega` + `[VERIFICAR]` + Layout sugerido

A partir de v1.1 do plugin, esta skill aplica 4 disciplinas adicionais ao gerar STORYBOARD. Detalhes canônicos em `../../shared/storyboard-schema.md` e `../../shared/verificar-flag.md`.

**1. `modo_entrega` adapta densidade do slide** (regra 7 do schema):
- `apresentado-ao-vivo` (U4=1/2): slides minimalistas (2-3 bullets) + speaker notes RICOS
- `enviado-para-leitura` (U4=3): slides DENSOS (4-6 bullets + dados inline + 1 quote curto) + speaker notes opcionais ou curtos
- `hibrido` (U4=4): meio-termo, ambos preenchidos

Preencher bloco `Conteúdo do slide (visível na projeção)` em cada slide, calibrado ao `modo_entrega`.

**2. `Layout sugerido` em cada slide** (regra 8 do schema): grid + tipografia + componentes visuais + animação. Sem isso, designer/Gamma/Claude Design/PowerPoint recebe o deck "no escuro".

**3. `[VERIFICAR]` em dados fabricados** (regra 9 do schema + `verificar-flag.md`): todo R$/%/n=/RCT/NPS/GRADE/CFO/Anvisa que a skill **inferir** (não veio do usuário; não é público canonicamente conhecido) recebe `[VERIFICAR: descrição]` inline ou em footnote. Lint v1.1 emite WARN quando ausente. Reviewer converte em 🟡 ou 🔴 no segundo passe.

**4. Bold opcional nos rótulos:** preferir `**Tipo:**`, `**Action title:**`, `**Mensagem-chave:**` para facilitar leitura visual. Lint aceita ambos formatos.

**Checklist v1.1 ao gerar cada slide:**
- [ ] `**Tipo:**`, `**Action title:**`, `**Mensagem-chave:**` em bold
- [ ] Bloco `Conteúdo do slide (visível na projeção)` preenchido com densidade adaptada ao `modo_entrega`
- [ ] Bloco `Layout sugerido` com grid + tipografia + componentes
- [ ] Dados específicos inferidos marcados com `[VERIFICAR: ...]`
- [ ] `Imagens sugeridas` no formato v1.1 (Quantidade explícita + variações em blocos separados)
