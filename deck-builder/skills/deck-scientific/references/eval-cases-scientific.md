# Eval cases — `deck-scientific`

3 cases obrigatorios cobrindo os 3 outputs distintos (STORYBOARD oral, POSTER.md D8, STORYBOARD keynote multi-estudo).

---

## Case 1 — CIOSP oral 7min "Eficacia Er:YAG vs convencional periimplantite"

### Input

- **U1:** "Audiencia CIOSP entende eficacia Er:YAG vs convencional + replica protocolo"
- **U2:** Periodontistas + implantodontistas brasileiros (CIOSP plateia mista)
- **U3:** 7 min
- **U4:** pitch presencial
- **U5:** "Er:YAG reduz profundidade de bolsa periimplantar em 1.8 mm (IC95% -2.3/-1.3) vs convencional, GRADE moderate"
- **U6:** Fotona (auto-detection — match em "Er:YAG" do brief)
- **X1:** CIOSP 2026, sessao oral, 7 min
- **X2:** systematic review + meta-analise (8 RCTs, n=480)
- **X3:** outcome primario = reducao profundidade bolsa periimplantar; secundarios = sangramento + ganho clinico
- **X4:** Consultor pago Fotona Inc. + financiamento de pesquisa Fotona
- **X5:** mista (periodontistas + implantodontistas + industria)

### Output esperado

**Arquivo:** `$DECKS_DIR/2026-05/STORYBOARD-eryag-periimplantite-XXXX.md` (NAO POSTER — modo oral-short)

**Estrutura — 8 slides IMRAD destilado:**

1. **Capa + autores + COI explicito** (60s, action title: "Er:YAG reduziu profundidade de bolsa periimplantar em 1.8 mm vs convencional (meta-analise, n=480)")
2. **Background + research question** (60s, IMRAD intro 3 movimentos CARS)
3. **Methods** (60s — PRISMA citado, 8 RCTs, criterio inclusao/exclusao, GRADE)
4. **Results — forest plot** (60s, IC95% -2.3 a -1.3, p<0.001, Tufte forest plot)
5. **Results — small multiples 8 estudos** (60s, Tufte aplicado)
6. **Discussion + significado clinico** (60s — comparacao com literatura, limitacoes risco vies)
7. **Limitacoes + futuro** (30s — heterogeneidade I²=45%, RCT confirmatorio em curso)
8. **Take-home + 3 CTAs** (30s — read paper QR / replicate via OSF / contact author)

### Validacoes do output

- [ ] Action titles em todos os 8 slides (NAO titulos descritivos)
- [ ] COI declarado slide 1 ("Consultor Fotona + financiamento")
- [ ] **PRISMA citado** no slide Methods (X2 = systematic review)
- [ ] **GRADE moderate** explicito no outcome primario
- [ ] IC95% + effect size + p-value + n no slide Results
- [ ] **max_ctas: 3** declarado na Meta (read paper / replicate / contact author)
- [ ] **D5 override aplicado** — slides 4 e 5 (tipo `dados`) tem prompt de imagem preenchido por `deck-image-prompts`
- [ ] **Storyboard de Imagens** com brief para forest plot e small multiples
- [ ] **Checklist de Revisao** preenchida (handoff `deck-reviewer`)
- [ ] **Bloco Compliance 3 tiers** preenchido (🔴/🟡/✅) — esperado: ✅ COI declarado, ✅ PRISMA, ✅ GRADE, ✅ IC95%
- [ ] **Big Idea (U5)** aparece no slide 8 como take-home

---

## Case 2 — IADR poster A0 "Dosimetria LightWalker Fotona clareamento" (MODO POSTER D8)

### Input

- **U1:** "IADR audience aprende dosimetria LightWalker correta para clareamento sustentado"
- **U2:** Researchers IADR mista (basic + clinical research)
- **U3:** painel A0 (poster session)
- **U4:** poster session (presencial)
- **U5:** "Dosimetria LightWalker correta sustenta clareamento em 92% dos casos por 6 meses"
- **U6:** Fotona (auto)
- **X1:** IADR 2026, poster A0
- **X2:** case series (50 pacientes)
- **X3:** outcome primario = clareamento sustentado 6 meses (delta E ≥ 3.7); secundario = satisfacao paciente
- **X4:** Consultor Fotona + financiamento

### Output esperado

**Arquivo:** `$DECKS_DIR/2026-05/POSTER-dosimetria-lightwalker-XXXX.md` (**POSTER.md — D8 schema proprio, NAO STORYBOARD**)

**Estrutura — Better Poster Morrison:**

- **Cabecalho:** titulo + autores + COI + IADR 2026
- **Centro (GRANDE):** "Er:YAG sustenta clareamento por 6 meses em 92% dos casos (n=50)"
- **Painel esquerdo (Background):** contexto clareamento + dosimetria atual + research question
- **Painel inferior esquerdo (Methods, small):** 50 pacientes, protocolo dosimetrico operacionalizado, follow-up 6 meses, delta E como outcome, STROBE citado
- **Painel direito (Results):** 2 figuras Tufte:
  - Figura 1: curva delta E ao longo de 6 meses (linha unica + IC95% sombreado)
  - Figura 2: tabela densa Tufte com 50 pacientes (sparklines de evolucao)
- **Painel inferior direito (Conclusion, small):** discussion destilada + significado clinico + limitacoes (n=50, sem controle)
- **Rodape:** 5 references + COI Fotona explicito + grant + **QR code para paper completo** + ORCID autores

### Validacoes do output

- [ ] **Arquivo POSTER-{slug}.md** (NAO STORYBOARD — D8)
- [ ] **Schema bate com `assets/templates/poster-skeleton.md`**
- [ ] **Key finding centro com numero chave** ("92% dos casos (n=50)")
- [ ] **STROBE citado** (X2 = case series, mas STROBE aplica; CARE seria alternativa)
- [ ] COI declarado no rodape
- [ ] **QR code para paper completo** no rodape
- [ ] **max_ctas: 3** (read paper / replicate / contact author)
- [ ] **NAO invoca `deck-image-prompts`** (poster usa figuras do paper diretamente)
- [ ] Tufte aplicado em figura 1 (linha + IC95% sombreado, sem chartjunk)
- [ ] **Bloco Compliance 3 tiers** (🔴/🟡/✅)
- [ ] **Big Idea (U5)** aparece no centro do poster (key finding)

---

## Case 3 — ICOI keynote 45min "Futuro da reabilitacao implantossuportada"

### Input

- **U1:** "ICOI audience repensa estrategias de reabilitacao com nova visao integrada"
- **U2:** Implantodontistas seniores ICOI + lideres opiniao
- **U3:** 45 min
- **U4:** keynote presencial
- **U5:** "Reabilitacao implantossuportada digital reduz tempo total em 40% mantendo sucesso ≥98% em 5 anos"
- **U6:** generico (sem auto-detection)
- **X1:** ICOI 2026, keynote plenaria, 45 min
- **X2:** multiplos estudos do grupo + 1 cohort prospectivo 5 anos
- **X3:** outcome primario = sobrevida do implante 5 anos; secundarios = tempo total tratamento + satisfacao + complicacoes
- **X4:** Multiplos: consultor 2 industrias + autor 2 livros + grants institucionais
- **X5:** mista (implantodontistas + researchers + industria)

### Output esperado

**Arquivo:** `$DECKS_DIR/2026-05/STORYBOARD-futuro-reabilitacao-XXXX.md` (modo keynote — STORYBOARD)

**Estrutura — 35 slides em 3 atos + Q&A:**

- **Ato 1 (10 min, 10 slides) — Estado da arte + Big Idea:**
  - Slide 1: Capa + COI multiplo declarado
  - Slide 2: Agenda visual (Doumont tree)
  - Slides 3-7: Panorama do campo + papers fundadores
  - Slides 8-9: Gap atual (tempo total tratamento + sucesso variavel)
  - Slide 10: Research question / Big Idea (gancho narrativo)

- **Ato 2 (20 min, 18 slides) — Metodos + resultados multi-estudo:**
  - 3 estudos do grupo, cada um com 1 slide Methods + 2-3 slides Results (graficos com `dados` na whitelist — **override D5 aplicado**)
  - GRADE level explicito por outcome de cada estudo
  - Cohort 5 anos com STROBE citado + RCT com CONSORT
  - Tufte small multiples comparando 3 estudos

- **Ato 3 (10 min, 7 slides) — Implicacoes + futuro:**
  - Slide 28: Sintese 3 atos
  - Slides 29-32: Implicacoes para pratica + protocolos derivados
  - Slide 33: Chamada a colaboracao
  - Slide 34: 3 CTAs (read papers / replicate via OSF / contact author/ORCID)
  - Slide 35: Q&A trigger

- **Q&A bloco preparado (apendice, 6 perguntas antecipadas + respostas curadas)**

### Validacoes do output

- [ ] **35 slides em 3 atos** estruturados
- [ ] COI multiplo declarado slide 1
- [ ] **Big Idea (U5)** aparece slide 10 (transicao Ato 1 → Ato 2) e na sintese Ato 3
- [ ] **CONSORT + STROBE citados** conforme tipo de cada estudo (X2 = multi-estudo)
- [ ] **GRADE level por outcome** (nao so primario)
- [ ] **D5 override aplicado** — todos os slides `dados` (graficos Tufte) tem prompt de imagem
- [ ] **max_ctas: 3** declarado na Meta
- [ ] **Q&A bloco preparado** com 4-6 perguntas + respostas
- [ ] **Storyboard de Imagens** preenchido para slides whitelist (capa, conceitual, dados — override scientific)
- [ ] **Checklist de Revisao** (handoff `deck-reviewer`)
- [ ] **Bloco Compliance 3 tiers** preenchido

---

## Como validar (modo manual)

```bash
cd ~/.claude/skills/deck-scientific
cat references/eval-cases-scientific.md  # esta pagina

# Para cada case, simular invocacao:
# 1. /deck-scientific {input do case}
# 2. Verificar output bate com "Validacoes" acima
# 3. Marcar checkbox passou / falhou
```

## DoD eval cases (criterio §13.6 do brief)

- [ ] 3 cases cobertos
- [ ] Case 2 gera **POSTER.md** (NAO STORYBOARD — D8)
- [ ] Case 1 + Case 3 geram STORYBOARD.md schema §10.2
- [ ] Todos os cases tem **max_ctas: 3** declarado
- [ ] Todos os cases tem **COI slide 1 / rodape poster**
- [ ] Todos os cases tem **reporting guideline** conforme X2 (CONSORT/STROBE/PRISMA/CARE)
- [ ] Todos os cases tem **GRADE level** no outcome primario
- [ ] Todos os cases tem **p-value contextualizado** (IC95% + effect size + n)
