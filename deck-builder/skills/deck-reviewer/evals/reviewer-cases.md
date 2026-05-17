# Eval Cases — deck-reviewer

4 cases canonicos. DoD §13.6 exige 3+ passando. Alvo: 4/4.

Fixtures em [fixtures/](fixtures/).

---

## Case 1 — Fundraising sem ask 🔴

**Fixture:** [fixtures/case1-fundraising-sem-ask.md](fixtures/case1-fundraising-sem-ask.md)

**Caracteristicas do input:**
- 13 slides
- Slide final (13) e "Equipe completa" — NAO e CTA/Ask
- Vertical fundraising → exige CTA Ask (D14)
- max_ctas=1 declarado mas count_ctas=0
- Action titles fracos: slide 2 "Mercado odontologia", slide 4 "TAM", slide 8 "Nosso time" — descritivos sem verbo
- 0 numeros especificos nos primeiros 5 slides (Big Idea cita "R$48k/ano" mas slides nao reforcam)
- Muitos adjetivos vagos: "escalavel", "robusto", "inovador", "disruptivo"

**Issues esperadas do reviewer:**

🔴 BLOCKER esperados (1+):
- Slide 13 — CTA/Ask inexistente. Vertical fundraising exige Ask explicito (valuation + ticket + timeline + uso do capital).
- Suggestao: "Adicionar slide 14 'Ask' com R$500k @ 8% equity / 6 meses para 2a unidade. Term sheet em 7 dias."

🟡 MAJOR esperados (≥2):
- Action titles descritivos sistemicos (3+ slides)
- Razao numeros/adjetivos baixa (Critico SUCCESs — Concrete)

🟢 MINOR esperados (opcional)

**Recommended next action esperada:**
- "Resolver 1 blocker antes de apresentar." OU "Resolver {N} blockers..." se reviewer encontrar mais de 1

**Criterios de PASS:**
1. Pelo menos 1 🔴 BLOCKER mencionando "CTA" OU "Ask" OU "captacao sem chamada"
2. Sugestao concreta (numero R$, prazo OU estrutura "valuation + ticket + timeline")
3. Recommended action menciona "blocker"
4. NAO emite score numerico, nota, percentual ou estrelas
5. Arquivo de output e `.review.md` paralelo (NAO sobrescreve original)

---

## Case 2 — Clinical com promessa de cura 🔴

**Fixture:** [fixtures/case2-clinical-promessa-cura.md](fixtures/case2-clinical-promessa-cura.md)

**Caracteristicas do input:**
- 9 slides
- Slide 7 contem: "Implante All-on-4 garante recuperacao 100% em 90 dias" + speaker notes mencionando "cura definitiva, sem necessidade de manutencao no futuro"
- Vertical clinical → CFO Res. 196/2019 + CFM 1974/2011 vetam promessa de cura e sucesso 100%
- Resto do deck e relativamente OK (CTA presente no slide 9, evidencia citada slide 5)

**Issues esperadas do reviewer:**

🔴 BLOCKER esperados (1+):
- Slide 7 — Compliance: frase "garante recuperacao 100%" viola CFO Res. 196/2019 (promessa de cura) + CFM 1974/2011
- Sugestao: reescrita removendo "garante", "100%", "cura definitiva", "sem manutencao". Ex: "Implante All-on-4 — recuperacao tipica 3-6 meses, sucesso clinico documentado em 95% dos casos (literatura)"

🟡 MAJOR opcionais:
- "Cura definitiva, sem manutencao" nas speaker notes precisa ser revisada paralelamente
- Slide 8 "Investimento" pode ganhar action title mais persuasivo

**Recommended next action esperada:**
- "Resolver 1 blocker antes de apresentar."

**Criterios de PASS:**
1. Pelo menos 1 🔴 BLOCKER em slide 7 mencionando "promessa de cura" OU "garante" OU "100%" OU "CFO" OU "compliance"
2. Sugestao com texto reescrito alternativo (NAO so "remover")
3. NAO emite score numerico
4. Recommended action menciona "blocker"

---

## Case 3 — Teaching 4h sem hands-on 🟡 (CTAs OK porque max=4)

**Fixture:** [fixtures/case3-teaching-sem-hands-on.md](fixtures/case3-teaching-sem-hands-on.md)

**Caracteristicas do input:**
- Aula 4h (240min), 18 dentistas pos-grad
- 0 slides de hands-on (so teoria + discussao)
- max_ctas: 4 declarado na Meta (vertical teaching default)
- 3 CTAs presentes (slides 7, 8, 9) — count_ctas=3, ≤ max_ctas=4 → OK
- Modulos de 60-90min sem chunking (regra cognitiva chunks ≤7-10min)
- Objetivos de aprendizagem declarados (slide 2) — OK
- Avaliacao formativa presente (quiz, caso proprio)

**Issues esperadas do reviewer:**

🟡 MAJOR esperados (1+):
- 0 hands-on em 4h de aula tecnica adulta — viola Knowles Andragogy
- Sugestao: inserir chunks praticos (worksheet de calculo fluence, simulado de protocolo) entre Modulos 2 e 3

🟡 MAJOR opcionais:
- Chunks de 60-90min sem quebra (regra cognitiva ≤7-10min)
- Mover discussao de cases para hands-on real

**NAO esperado:**
- ❌ NAO marcar CTAs como problema (3 ≤ 4 = OK)
- ❌ NAO emite 🔴 (problema e pedagogico, nao bloqueante de apresentacao)

**Recommended next action esperada:**
- "Resolver {N} major(es) antes de polir." (formato com N=1 ou maior)

**Criterios de PASS:**
1. Pelo menos 1 🟡 MAJOR mencionando "hands-on" OU "pratica" OU "Andragogy" OU "Knowles"
2. NAO marca CTAs como issue (3 ≤ max_ctas=4)
3. NAO emite 🔴 BLOCKER
4. NAO emite score numerico
5. Recommended action menciona "major"

---

## Case 4 — Scientific oral-long 4 CTAs (excede max=3) 🟡

**Fixture:** [fixtures/case4-scientific-4-ctas.md](fixtures/case4-scientific-4-ctas.md)

**Caracteristicas do input:**
- 12 slides
- max_ctas: 3 declarado na Meta (vertical scientific default)
- 4 CTAs presentes (slides 9, 10, 11, 12) — count_ctas=4 > max_ctas=3 → 🟡 MAJOR
- Slide 12 e "CTA Bonus — newsletter" — candidato natural a remocao
- Metodologia OK (CONSORT mencionado), limitacoes declaradas, conflito de interesse declarado
- Citacoes presentes

**Issues esperadas do reviewer:**

🟡 MAJOR esperados (1):
- max_ctas=3 excedido por 1 (count_ctas=4)
- Sugestao: "Remover CTA bonus (slide 12 — newsletter) OU aumentar max_ctas para 4 na Meta com justificativa"

🟢 MINOR opcionais

**NAO esperado:**
- ❌ NAO marca como 🔴 BLOCKER (max_ctas violation e MAJOR, nao BLOCKER — pode ser intencional)
- ❌ NAO marca metodologia como issue
- ❌ NAO emite score numerico

**Recommended next action esperada:**
- "Resolver 1 major antes de polir." OU "Resolver {N} majores..."

**Criterios de PASS:**
1. Pelo menos 1 🟡 MAJOR mencionando "max_ctas" OU "CTAs excede" OU "4 CTAs" OU "remover bonus"
2. Sugestao oferece duas opcoes: remover CTA OU aumentar limite
3. NAO emite 🔴 BLOCKER por causa do max_ctas (regra D14)
4. NAO emite score numerico
5. Recommended action menciona "major"

---

## Resumo de validacao DoD

Para cada case rodar o reviewer manualmente OU spawned subagent com a skill carregada. Verificar contra `Criterios de PASS`.

| Case | 🔴 esperado | 🟡 esperado | 🟢 esperado | Pass se |
|------|------------|------------|------------|---------|
| 1. Fundraising sem ask | 1+ (CTA inexistente) | 2+ | optional | criterios 1-5 acima |
| 2. Clinical promessa cura | 1+ (slide 7) | optional | optional | criterios 1-4 acima |
| 3. Teaching sem hands-on | 0 | 1+ (hands-on) | optional | criterios 1-5 acima |
| 4. Scientific 4 CTAs | 0 | 1+ (max_ctas) | optional | criterios 1-5 acima |

**Universal (todos os 4 cases):**
- Output em arquivo `.review.md` paralelo (NUNCA sobrescreve fixture)
- SEM score numerico em nenhum lugar
- Recommended next action presente
- Meta inclui `Criticos aplicados: clareza + persuasao + SUCCESs`

## Como rodar (manual)

```
1. Copiar fixture pra um path temp: cp fixtures/case1-fundraising-sem-ask.md /tmp/STORYBOARD-test-1647.md
2. Invocar reviewer mentalmente OU via subagent: "Le /tmp/STORYBOARD-test-1647.md, aplica deck-reviewer (3 criticos), grava .review.md paralelo"
3. Inspecionar /tmp/STORYBOARD-test-1647.review.md
4. Validar contra Criterios de PASS deste case
```
