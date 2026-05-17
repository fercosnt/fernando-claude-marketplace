# Skeleton STORYBOARD oral / keynote (deck-scientific)

> Schema §10.2 do SHARED.md com `max_ctas: 3` (override D14) e `--include-dados` (override D5).

```markdown
# Deck: {nome-paper-ou-titulo}

## Meta
- Skill geradora: deck-scientific
- Modo: oral-short | oral-long | keynote
- Objetivo unico: {U1}
- Audiencia: {U2}
- Duracao: {U3} min
- Formato: {U4}
- Big Idea: {U5}
- Marca: {U6}
- Framework principal: IMRAD + GRADE + Tufte + Doumont
- Congresso: {X1}
- Tipo de estudo: {X2}
- Outcome primario: {X3}
- COI: {X4}
- Audiencia mista: {X5}
- max_ctas: 3 (override scientific — D14: read paper / replicate / contact author)
- Reporting guideline: CONSORT | STROBE | PRISMA | CARE (conforme X2)
- Gerado em: {ISO date}
- Versao: v1
- Storyboard ID: STORYBOARD-{slug}-{YYYYMMDD-HHmm}

## Estrutura Narrativa

{2-3 paragrafos sobre o arco narrativo IMRAD aplicado ao modo}

---

## Slide 1 — Capa
Tipo: capa
Action title: {headline assertivo com numero chave — ex: "Er:YAG reduziu profundidade de bolsa em 1.8 mm (n=480, GRADE moderate)"}
Mensagem-chave: {1 frase — Big Idea}
Speaker notes:
- COI declarado em voz alta (regra inviolavel)
- Apresentar autores + afiliacoes
- Citar congresso
Visual: capa institucional com titulo + autores + COI + logo congresso
Prompt de imagem: {deck-image-prompts preenche — tipo `capa` esta na whitelist canonica}
Tempo estimado: 30s

**COI explicito (regra inviolavel deck-scientific):**
{X4 — se vazio, escrever "Nenhum COI a declarar"}

---

## Slide 2 — Background (Introduction CARS movimento 1)
Tipo: contexto
Action title: {assertivo, NAO descritivo}
Mensagem-chave: {1 frase}
Speaker notes: {contexto + relevancia clinica}
Visual: {ex: timeline historico do campo OU mapa de prevalencia}
Prompt de imagem: {deck-image-prompts — tipo `contexto`/`conceitual` na whitelist}
Tempo estimado: {seg}

## Slide 3 — Gap + Research Question (CARS movimentos 2-3)
Tipo: problema
Action title: {ex: "Faltam meta-analises com GRADE moderate sobre Er:YAG vs convencional"}
Mensagem-chave: {pergunta de pesquisa explicita}
Speaker notes: {gap na literatura + pergunta de pesquisa}
Visual: {ex: diagrama do gap}
Prompt de imagem: {deck-image-prompts — tipo `problema` na whitelist}
Tempo estimado: {seg}

## Slide 4 — Methods (IMRAD M)
Tipo: conceitual
Action title: {ex: "Meta-analise PRISMA-compliant de 8 RCTs (n=480)"}
Mensagem-chave: {design + sample + outcome operacionalizado}
Speaker notes:
- Design: {X2}
- Sample: {n + criterios}
- Outcome operacionalizado: {X3}
- Analise: {testes + software}
- **Reporting per {CONSORT/STROBE/PRISMA/CARE}** (regra inviolavel)
- Ethics approval: {comite + numero}
Visual: {ex: PRISMA flow diagram OU CONSORT flow diagram}
Prompt de imagem: {deck-image-prompts — tipo `conceitual` na whitelist}
Tempo estimado: {seg}

## Slide 5 — Results outcome primario (IMRAD R)
Tipo: dados
Action title: {assertivo com numero chave — ex: "Er:YAG: -1.8 mm IC95% -2.3 a -1.3 (p<0.001, GRADE moderate)"}
Mensagem-chave: {effect size + IC95% + p-value + GRADE}
Speaker notes:
- Effect size: {numero + unidade}
- IC95%: {intervalo}
- p-value: {com 3 decimais}
- n: {sample}
- GRADE: {nivel + razao downgrade/upgrade}
Visual: forest plot Tufte (data-ink ratio alto, sem chartjunk)
Prompt de imagem: {deck-image-prompts — **override D5: tipo `dados` incluido na whitelist scientific**}
Tempo estimado: {seg}

## Slide 6 — Results outcomes secundarios (IMRAD R)
Tipo: dados
Action title: {ex: "Sangramento e ganho clinico tambem favorecem Er:YAG"}
Mensagem-chave: {todos os outcomes secundarios — sem cherry-picking}
Speaker notes: {tabela densa Tufte com TODOS os outcomes, incluindo negativos se houver}
Visual: tabela densa Tufte OU small multiples
Prompt de imagem: {deck-image-prompts — override D5 dados}
Tempo estimado: {seg}

## Slide 7 — Discussion (IMRAD D)
Tipo: conceitual
Action title: {assertivo — ex: "Magnitude clinicamente relevante (>1 mm threshold MCID)"}
Mensagem-chave: {significado clinico + comparacao literatura}
Speaker notes:
- Restatement do achado principal
- Comparacao com literatura
- Limitacoes (internas + externas)
- {se p>0.05 outcome primario} Erro tipo II: poder={valor}, estudo subdimensionado
- Implicacoes
Visual: {comparativo OU conceitual}
Prompt de imagem: {deck-image-prompts — tipo `conceitual`/`comparativo` na whitelist}
Tempo estimado: {seg}

## Slide 8 — Take-home + CTAs (max 3 — D14)
Tipo: CTA
Action title: {Big Idea (U5) como take-home}
Mensagem-chave: Big Idea + 3 CTAs scientific
Speaker notes: |
  CTAs scientific (max 3 — D14):
  1. **Read paper:** {DOI ou QR code}
  2. **Replicate:** {OSF / Zenodo / Figshare protocolo}
  3. **Contact author:** {email ou ORCID}
Visual: QR code centralizado + 3 bullets de CTA + Big Idea grande
Prompt de imagem: {tipo `CTA` NAO esta na whitelist — skip}
Tempo estimado: {seg}

---

## Apendice (slides opcionais)

- Q&A bloco preparado: {4-6 perguntas antecipadas + respostas curadas} — apenas em modo `keynote`
- Tabela densa Tufte com outcomes secundarios completos
- Funnel plot (se meta-analise)
- CONSORT/STROBE/PRISMA flow diagram detalhado
- Calculo de poder estatistico
- Protocolo operacional completo (replicabilidade)

---

## Storyboard de Imagens (handoff pra deck-image-prompts)

**Override D5 aplicado: tipo `dados` incluido na whitelist scientific.**

- Slide 1 (capa): {brief}
- Slide 2 (contexto): {brief}
- Slide 3 (problema): {brief}
- Slide 4 (conceitual — PRISMA flow): {brief}
- Slide 5 (dados — forest plot Tufte): {brief} ← **override D5**
- Slide 6 (dados — small multiples / tabela densa): {brief} ← **override D5**
- Slide 7 (conceitual / comparativo): {brief}
- Slide 8 (CTA): skip (CTA nao esta na whitelist)

Flag a passar para `deck-image-prompts`: `--include-dados`

---

## Checklist de Revisao (handoff pra deck-reviewer)

- [ ] Action titles (NAO titulos descritivos) em todos os slides
- [ ] 1 ideia por slide
- [ ] Horizontal logic test (slides 1→N contam a historia)
- [ ] COI declarado slide 1
- [ ] **max_ctas: 3** declarado na Meta (validado pelo reviewer)
- [ ] **Reporting guideline citado** ({CONSORT|STROBE|PRISMA|CARE}) no slide Methods
- [ ] **GRADE level** explicito no outcome primario
- [ ] **p-value contextualizado** (IC95% + effect size + n) — sem "p<0.05" solto
- [ ] Numeros sempre com unidade e denominador
- [ ] Sem cherry-picking — outcomes negativos reportados se houver
- [ ] {se p>0.05} Erro tipo II discutido (poder estatistico)
- [ ] Big Idea (U5) aparece no slide 1 ou no take-home

---

## Compliance & Disclaimers (3 tiers — D7)

🔴 Issues bloqueantes (resolver antes de apresentar):
- {ex: "p<0.05 sem effect size no slide 5 — adicionar IC95%"}
- {ex: "COI Fotona nao declarado slide 1"}

🟡 Verificar antes:
- {ex: "PRISMA flow diagram presente em apendice?"}
- {ex: "Funnel plot incluido em apendice?"}
- {ex: "Erro tipo II discutido (poder)?"}

✅ OK:
- COI declarado slide 1
- GRADE moderate citado outcome primario
- Reporting per {guideline} (slide Methods)
- p-value com IC95% + effect size + n
- Outcomes secundarios em tabela densa (nao cherry-picking)
```
