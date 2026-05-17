# Frameworks aplicados pelo deck-clinical

Tres frameworks complementares, selecionados por modo. Carregado pela SKILL.md quando precisa montar estrutura narrativa.

---

## 1. Evidence-Based Medicine (EBM) hierarchy

Aplica-se: **`peer-facing` sempre** + opcionalmente `patient-facing` quando paciente faz pergunta sobre evidencia.

### Hierarquia (forte → fraco)

| Nivel | Tipo de evidencia | Quando citar |
|-------|-------------------|--------------|
| 1 | Meta-analise de RCTs / Systematic review | Outcome principal, modo peer |
| 2 | RCT individual com baixo risco de vies | Outcome principal, modo peer |
| 3 | Cohort prospectivo / case-control | Falta RCT, outcomes raros |
| 4 | Case series | Mecanismo, descricao inicial |
| 5 | Opiniao especialista / consensus paper | Quando nao ha evidencia formal |

### GRADE (Grading of Recommendations Assessment, Development and Evaluation)

Para CADA outcome relevante, classificar evidencia como:

- **HIGH:** evidencia muito provavel reflete efeito real (alterar pratica)
- **MODERATE:** evidencia provavel reflete efeito real, mas pesquisa futura pode mudar
- **LOW:** evidencia limitada, pesquisa futura provavelmente mudara estimativa
- **VERY LOW:** evidencia muito incerta

**Regra deck-clinical:** Em modo peer, slide "Estado da Evidencia" SEMPRE cita nivel GRADE por outcome. Diferentes outcomes podem ter GRADEs diferentes — explicitar.

Exemplo: "Laser em endodontia — descontaminacao canal: GRADE HIGH (3 systematic reviews). Cura sintomatica em 6 meses: GRADE LOW (1 RCT pequeno, alto risco vies)."

### Citacao obrigatoria

Formato minimo: **Primeiro autor, ano, journal abreviado.**

Exemplo: "Verheyen P, 2022, J Endod" ou "Olivi G et al., 2023, Lasers Med Sci".

Apendice (slide nao-essencial) com 3-5 papers completos quando modo peer.

---

## 2. AIDET (modo `patient-facing` — Studer Group)

Framework de comunicacao paciente-profissional. **Obrigatorio em `patient-facing`**, mapeia direto pra estrutura de 5 slides (mais capa, alternativas e proximos passos = 7-8 total).

| Letra | Significado | Slide correspondente | Conteudo |
|-------|------------|---------------------|----------|
| **A**cknowledge | Reconhecer | Slide 2 — abertura | Cumprimento pelo nome, ambiente acolhedor |
| **I**ntroduce | Apresentar | Slide 2 (combinado) | Quem somos (profissional + equipe + credenciais) — gera confianca |
| **D**uration | Duracao | Slide 5 — tempo | Tempo procedimento + tempo recuperacao realistas |
| **E**xplanation | Explicar | Slides 3-4 — situacao + plano | O QUE sera feito em linguagem leiga, POR QUE e seguro, COMO funciona |
| **T**hank | Agradecer | Slide 7-8 — proximos passos | Agradecimento + reforco que estamos disponiveis pos-procedimento |

### Linguagem leiga — substituicoes obrigatorias (NAO exaustivo)

| Jargao tecnico | Linguagem leiga |
|---------------|-----------------|
| Osseointegracao | "o osso se une ao implante naturalmente, formando uma raiz nova" |
| Carga imediata | "o dente provisorio entra no mesmo dia" |
| Hipersensibilidade dentinaria | "sensibilidade no dente" |
| Reabilitacao maxilar | "reconstrucao dos dentes de cima" |
| Periodontite | "doenca da gengiva" |
| Endodontia | "tratamento de canal" |
| Diastema | "espaco entre os dentes" |
| Adenoidectomia | "remocao das adenoides" |
| Profilaxia | "limpeza profissional" |
| Anestesia infiltrativa | "anestesia local" |

**Regra:** se um termo tecnico aparecer no STORYBOARD `patient-facing`, marca como 🟡 no bloco final compliance ("VERIFICAR: jargao restante slide N — substituir antes de apresentar").

### Alternativas obrigatorias (consentimento informado)

Em `patient-facing` para procedimentos invasivos (implantes, extracoes, cirurgias), slide de alternativas e OBRIGATORIO. Listar minimo:
- Alternativa A (menos invasiva)
- Alternativa B (status quo / nao fazer nada)
- Alternativa proposta (o plano que estamos sugerindo)

Comparacao justa (nao vender, apenas informar). Ausencia desse slide = 🔴 BLOCKER no bloco final.

---

## 3. Calgary-Cambridge (modo `peer-facing` — guia clinico academico)

Estrutura adaptada para apresentacao a outros profissionais — caso clinico como ponto de partida, depois evidencia, depois protocolo.

### Fluxo canonico (12-14 slides peer)

1. **Capa** — action title assertivo
2. **Caso clinico abertura** — paciente real, contexto, problema apresentado
3. **Problema clinico geral** — limitacoes da abordagem atual (gancho)
4. **Estado da evidencia** — GRADE por outcome, RCTs/systematic reviews citados
5. **Mecanismo de acao** — esquema anatomico/fisiopatologico (slide tipo `conceitual`)
6. **Protocolo passo-a-passo** — dosimetria, parametros, sequencia clinica
7. **Demo procedural** — imagens do procedimento (slide tipo `demo`)
8. **Antes-e-depois** — caso real COM TCLE explicito mencionado (slide tipo `comparativo`)
9. **Outcome curto-prazo** — resultados imediatos
10. **Outcome longo-prazo / follow-up** — 6 meses+ se disponivel
11. **Compliance + COI** — registro Anvisa do equipamento + conflito de interesse declarado
12. **Limites de uso / off-label** — disclaimer explicito quando aplicavel
13. **Discussao + Q&A** — perguntas-chave antecipadas
14. **Apendice** — papers completos (opcional, off-stage)

### Diferenciais Calgary-Cambridge vs apresentacao generica

- **Caso real abre, nao fecha:** medicos engajam com paciente, nao com teoria. Big Idea no slide 2-3 ja precisa estar conectada a um caso.
- **Bloco evidencia separado:** nao mistura evidencia com protocolo. Evidencia justifica, protocolo opera.
- **Outcome em duas janelas:** imediato + follow-up. Sem follow-up = 🟡 verificar.
- **Q&A antecipa objecao:** modo peer, audiencia desafia. Lista 3-5 perguntas previsiveis com resposta curta no body.

---

## Quando usar qual framework

| Situacao | Framework |
|----------|-----------|
| Aula em curso/congresso pra dentistas | Calgary-Cambridge + EBM |
| Apresentacao expert meeting (KOL) | Calgary-Cambridge + EBM + GRADE rigoroso |
| Consultoria a colega especifico | Calgary-Cambridge simplificado |
| Plano de tratamento ao paciente em consultorio | AIDET + alternativas |
| Briefing pra equipe interna sobre novo protocolo | Calgary-Cambridge sem bloco evidencia formal |
| Material educativo paciente (folder) | AIDET adaptado (escrita, nao apresentada) |

A skill detecta via C4 (especialista/generalista → peer; paciente leigo → patient).
