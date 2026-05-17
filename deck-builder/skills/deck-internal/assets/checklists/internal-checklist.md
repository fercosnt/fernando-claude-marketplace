# Checklist Final — deck-internal

Aplicar ANTES de entregar STORYBOARD ao usuario. Checklist combina universal §10 + especificos por modo.

---

## Universal (todos os modos)

- [ ] Schema §10.2 valido (Meta + Estrutura Narrativa + Slides + Apendice + Storyboard de Imagens + Checklist + Compliance)
- [ ] Frontmatter Meta tem todos os campos: Skill geradora, Objetivo unico, Audiencia, Duracao, Formato, Big Idea, Marca, Framework principal, Modo, max_ctas, Anexo 6-pager, Gerado em, Versao, Storyboard ID
- [ ] Action titles em TODOS os slides (NAO titulos descritivos)
- [ ] 1 ideia por slide
- [ ] Horizontal logic test (cada slide construct o argumento ao slide seguinte)
- [ ] Auto-detect marca aplicado (Beauty Smile / Fotona / Carnaval 360 / generico)
- [ ] Design system carregado se aplicavel (`beauty-smile-design-system` se Beauty Smile)
- [ ] Whitelist deck-image-prompts D5 aplicada (preencher capa/problema/conceitual/comparativo/demo/prova-social; skip dados/financeiro/CTA/disclaimer/apendice)
- [ ] Path output: `$DECKS_DIR/{YYYY-MM}/STORYBOARD-{slug}-{HHmm}.md`
- [ ] Anti-padroes ANTI-modelos-pitch-corporativo evitados (Enron retorica sem dados / Theranos prestigio sem produto / WeWork metricas inventadas / Twitter Musk ask invisivel / NASA Death by PowerPoint)
- [ ] Sugerir `/deck review` ao usuario (opt-in mas fortemente recomendado)

---

## Modo `pitch-to-leadership`

- [ ] **BLUF e slide 2** (NAO enterrar o lede — anti-padrao formato academico)
- [ ] BLUF tem 5 elementos: (a) recomendacao, (b) investimento, (c) retorno, (d) prazo, (e) ask
- [ ] Slide 1 = capa relacional (adaptacao Brasil — abertura antes do BLUF)
- [ ] Slide 3 (Problema) com custo de inacao QUANTIFICADO
- [ ] Slide 5 (Business case) com payback liderado (Brasil > NPV puro)
- [ ] Slide 6 (Friccao mitigada) enderaca I5 EXPLICITAMENTE
- [ ] Slide 7 (Ask) ESPECIFICO: valor + prazo + decisao + sponsor (NAO "vamos discutir")
- [ ] **Anexo 6-pager existe** como arquivo separado `STORYBOARD-{slug}-{HHmm}.6pager.md`
- [ ] 6-pager tem 6 secoes canonicas: Introducao, Goals, Tenets, State of Business, Lessons Learned, Strategic Priorities
- [ ] 6-pager regras de escrita: ≤30 palavras por sentenca, sem bullets no corpo principal, prosa densa
- [ ] CTA unico no slide 7 (max_ctas: 1)
- [ ] 8-10 slides + apendice

---

## Modo `strategy-presentation`

- [ ] SCR estrutural correto: Situation (slide 3) → Complication (slide 4) → Resolution (slide 5)
- [ ] 3 Horizontes McKinsey presentes (H1 = slide 6, H3 = slide 7, H2 = slide 8 — sequencia recomendada)
- [ ] Alocacao 70/20/10 explicita slide 10 ou justificativa de desvio
- [ ] KPIs por horizonte (NAO unico KPI agregado)
- [ ] Riscos top 3-5 com mitigacao no slide 12
- [ ] Roadmap visual com dependencias slide 9
- [ ] Direction SCR alinhado com audiencia (resistente: S→C→R / alinhada: R→S→C)
- [ ] CTA unico slide 13 (max_ctas: 1)
- [ ] 12-15 slides

---

## Modo `concept-reveal` (D3 pipeline)

- [ ] **Pasta de artefatos cenografia (C1) validada e existente**
- [ ] **Artefatos obrigatorios presentes:** ≥1 render-hero, ≥2 renders-detalhe, ≥1 mood-board, prompts.json
- [ ] Se artefatos faltam → PAROU e instruiu usuario a rodar `skill-cenografia` primeiro
- [ ] Sparkline correto: ≥2 vales antes do reveal (slide 3 = vale 1; slide 4 = pico)
- [ ] Big Idea sensorial slide 2 (NAO slide 1)
- [ ] REVEAL slide 4 NAO esta na primeira secao
- [ ] Walk-through 1ª pessoa nos speaker notes do slide 4
- [ ] **Paths ABSOLUTOS dos renders cenografia no campo `Visual:` dos slides 4, 5, 6**
- [ ] **Prompts copiados VERBATIM do `prompts/nano-banana-pro-prompts.json` (NAO regerados)**
- [ ] Mood board justificado (NAO Pinterest sem curadoria)
- [ ] Fechamento de loop com problema do slide 3 (Sparkline new bliss)
- [ ] Slide 7 Ask especifico (valor + cronograma + decisao)
- [ ] CTA unico (max_ctas: 1)
- [ ] Frontmatter Meta tem `Artefatos cenografia: {path absoluto}`
- [ ] 6-8 slides

---

## Modo `all-hands`

- [ ] Sinek Why-How-What estrutural: WHY=slide 2, HOW=slides 6-7, WHAT=slide 9
- [ ] Slide 2 (visao) em 1 frase poderosa emocional
- [ ] Slide 3 (estado) com leitura HONESTA (positivos + 2 friccoes operacionais)
- [ ] Slide 5 (celebracoes) com MULTIPLOS apresentadores (NAO so CEO)
- [ ] Slide 10 (Q&A) com 5+ perguntas anonimas pre-coletadas
- [ ] Primeira pergunta Q&A obrigatoriamente de remoto (hibrido)
- [ ] Arco emocional canonico respeitado (energia alta → factual → calor → estrategico → pessoal → abertura → clareza)
- [ ] Proporcao 30% factual / 70% engajamento
- [ ] `max_ctas: 2` no Meta (override SHARED.md)
- [ ] Slide 11 com acoes concretas por horizonte temporal (semana / 2 semanas / 1 trimestre)
- [ ] Follow-up escrito planejado em 24h
- [ ] NAO monologo CEO 30min
- [ ] Metricas slide 4 consistentes com Qs anteriores (NAO mudar definicao mid-quarter)
- [ ] 10-12 slides

### Se A1 = SIM (mudanca organizacional)

- [ ] Kotter visibilizado slide 6 com 4 elementos: urgencia + coalizao + visao + empoderamento
- [ ] Slide 7 (realocacao) enderaca I5 (ansiedade) EXPLICITAMENTE
- [ ] Slide 7 anuncia "sem demissoes" se for o caso, ou anuncia com precisao caso haja
- [ ] Pessoas afetadas FORAM AVISADAS EM PRIVADO antes do all-hands (NUNCA surpresa publica)
- [ ] Anti-padrao Yahoo Mayer 2013 evitado (CEO comunica mudanca, NAO HR)

---

## Compliance & Disclaimers (todos os modos)

3 tiers conforme §10.2 SHARED.md:

### 🔴 Bloqueantes
- Numeros financeiros sem marker `provisional`/`projecao` em decks externos
- Claims clinicos (Fotona/Beauty Smile) sem evidencia documentada
- Promessas de demissao/permanencia que nao podem ser cumpridas

### 🟡 Verificar antes
- Compliance tags da marca (anvisa-laser-classe-iii / cfo-cfm / odontologia-br)
- Premissas do business case (sensibilidade testada?)
- Anuncios organizacionais (HR aprovou mensagens?)

### ✅ OK
- Auto-detect marca correto
- Frameworks aplicados conforme modo
- Anti-padroes evitados

---

## Saidas do checklist

Se algum item bloqueante (🔴) falhar → NAO entregar; corrigir antes.

Se 🟡 falhar → marcar no Compliance & Disclaimers do STORYBOARD para usuario revisar.

Se todos os items passarem → entregar STORYBOARD + sugerir `/deck review` para passar pelo `deck-reviewer` (3 criticos adversariais SUCCESs Heath).
