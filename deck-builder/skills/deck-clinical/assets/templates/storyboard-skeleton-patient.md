# Deck: {nome-deck}

## Meta
- Skill geradora: deck-clinical
- Objetivo unico: {U1 — acao que o paciente vai tomar}
- Audiencia: {U2 — perfil paciente: idade, condicao, contexto}
- Duracao: {U3} min (consulta)
- Formato: {U4 — geralmente presencial em consultorio}
- Big Idea: {U5}
- Marca: {U6}
- Framework principal: AIDET (Studer Group)
- Modo: patient-facing
- max_ctas: 1
- Compliance tags: {ex: cfo-cfm, beauty-smile}
- Gerado em: {ISO date}
- Versao: v1
- Storyboard ID: STORYBOARD-{slug}-{YYYYMMDD-HHmm}

## Estrutura Narrativa
AIDET aplicado: Acknowledge + Introduce (slide 2), Explanation (slides 3-4), Duration (slide 5), Alternativas obrigatorias (slide 6 — consentimento informado), Thank (slide 7). Linguagem leiga em TODOS os titulos e speaker notes. Jargao tecnico substituido. Procedimento invasivo: alternativas obrigatorias incluindo "nao fazer nada".

---

## Slide 1 — Capa
Tipo: capa
Action title: "{Acolhedor, em linguagem leiga, com nome do paciente se possivel}"
Mensagem-chave: {1 frase recebendo o paciente}
Speaker notes: cumprimento + ambiente acolhedor, tom calmo
Visual: identidade visual da clinica, sem clinico-frio
Prompt de imagem: {deck-image-prompts preenche}
Tempo estimado: 30-60s

## Slide 2 — Acknowledge + Introduce (AIDET A + I)
Tipo: problema
Action title: "{Dr. Nome} + equipe {Clinica} vao acompanhar voce"
Mensagem-chave: quem somos + credenciais que geram confianca
Speaker notes:
- Cumprimentar paciente pelo nome
- Apresentar profissional responsavel (CRO + tempo de pratica + especializacao relevante)
- Apresentar equipe que estara envolvida
- Demonstrar que o paciente foi visto/ouvido
Visual: foto da equipe ou identidade Beauty Smile, NAO procedimento
Prompt de imagem: {deck-image-prompts preenche}
Tempo estimado: 60s

## Slide 3 — Sua situacao hoje (AIDET E inicio)
Tipo: problema
Action title: "{Situacao em linguagem leiga, sem jargao}"
Mensagem-chave: o paciente entende o que tem
Speaker notes:
- Explicar diagnostico em linguagem do paciente
- Usar analogias do dia a dia
- Validar o que o paciente ja sabe
- NAO usar: osseointegracao, hipersensibilidade, periodontite, etc.
- USAR: "o osso ao redor", "sensibilidade", "doenca da gengiva"
Visual: esquema simples OU foto da boca do paciente (se TCLE assinado para uso interno em consulta)
Prompt de imagem: {deck-image-prompts preenche — tipo conceitual + tom acolhedor}
Tempo estimado: 60-90s

## Slide 4 — Plano proposto (AIDET E continuacao)
Tipo: conceitual
Action title: "{Plano em 1 frase leiga}" (ex: "4 implantes que sustentam todos os dentes superiores")
Mensagem-chave: o que vamos fazer
Speaker notes:
- Explicar O QUE sera feito em sequencia simples
- POR QUE essa e a melhor opcao para o caso especifico
- COMO funciona (analogias)
- Esclarecer que paciente pode interromper a qualquer momento (consentimento)
Visual: esquema mostrando o plano sem detalhes cirurgicos assustadores
Prompt de imagem: {deck-image-prompts preenche — tipo conceitual + tom acolhedor}
Tempo estimado: 90-120s

## Slide 5 — Duracao (AIDET D)
Tipo: dados
Action title: "Tempo do procedimento + recuperacao"
Mensagem-chave: cronograma realista
Speaker notes:
- Tempo da cirurgia/procedimento principal (horas)
- Tempo de provisoriedade ou recuperacao imediata (dias/semanas)
- Tempo ate definitivo (meses)
- Frequencia de retornos
- Disclaimer verbal: "esses tempos variam de pessoa pra pessoa, vamos acompanhar de perto"
Visual: timeline simples
Prompt de imagem: skip — tipo dados em patient-facing
Tempo estimado: 60s

## Slide 6 — Suas opcoes (alternativas — CRITICO consentimento informado)
Tipo: comparativo
Action title: "Suas opcoes — comparacao justa"
Mensagem-chave: paciente decide com informacao
Speaker notes:
- Listar TODAS as alternativas viaveis, NAO apenas o plano proposto
- Para procedimento invasivo, OBRIGATORIO incluir "nao fazer nada" como opcao legitima
- Comparar honestamente: prazo, custo aproximado, durabilidade, riscos, conforto
- NAO vender — informar
- Exemplos para All-on-4: All-on-4 proposto | Protese removivel | Implantes unitarios | Nao fazer nada
Visual: tabela comparativa simples (4 colunas se 4 opcoes)
Prompt de imagem: {deck-image-prompts preenche — tipo comparativo + tom acolhedor, NAO marketing}
Tempo estimado: 90-120s

## Slide 7 — Proximos passos (AIDET T)
Tipo: CTA
Action title: "Proximos passos — estamos com voce"
Mensagem-chave: agradecimento + disponibilidade pos-procedimento
Speaker notes:
- Agradecer a confianca
- Definir proximos passos concretos (agendamento, exames complementares, prazo de retorno)
- Reforcar canais de contato pos-procedimento
- Convite a perguntar
Visual: contato + identidade clinica acolhedora
Prompt de imagem: skip — tipo CTA
Tempo estimado: 30-60s

---

## Slide 8 (opcional) — Antes-e-depois se TCLE OK
Tipo: comparativo
Action title: "Caso similar ao seu (paciente autorizou o uso da imagem)"
Mensagem-chave: ver um resultado real similar
Speaker notes:
- USAR APENAS se TCLE assinado pelo paciente do caso de referencia
- Apresentar como "caso similar", evitar promessa de resultado igual
- Reforcar: "cada caso e individual, resultados variam"
Visual: antes/depois COM crop, sem rosto identificavel se possivel
Prompt de imagem: {deck-image-prompts preenche — comparativo + placeholder TCLE + tom acolhedor + sem identificacao}
Tempo estimado: 60s

**Se TCLE pendente:** OMITIR este slide e marcar 🔴 BLOCKER no bloco final. NAO incluir antes-e-depois sem TCLE.

---

## Storyboard de Imagens (handoff pra deck-image-prompts)
- Slide 1 (capa): {brief — acolhedor, identidade clinica}
- Slide 2 (problema): {brief — equipe/profissional, NAO procedimento}
- Slide 3 (problema): {brief — esquema simples, tom acolhedor}
- Slide 4 (conceitual): {brief — plano visual sem detalhes cirurgicos}
- Slide 6 (comparativo): {brief — tabela alternativas, NAO marketing}
- Slide 8 SE existir (comparativo): {brief — antes/depois, TCLE OK, crop, sem identificacao}

## Checklist de Revisao (handoff pra deck-reviewer)
- [ ] Action titles em linguagem leiga
- [ ] 1 ideia por slide
- [ ] Hook do slide 1 acolhedor
- [ ] CTA unico (max_ctas: 1)
- [ ] AIDET aplicado (A+I, D, E, T)
- [ ] Alternativas obrigatorias presentes (slide 6)
- [ ] Compliance CFO/CFM/Anvisa preenchido abaixo
- [ ] Jargao tecnico ausente (grep no STORYBOARD)
- [ ] Antes-e-depois SOMENTE se TCLE

## Compliance & Disclaimers (3 tiers — D7)

🔴 Issues bloqueantes (resolver antes de apresentar):
- {issues 🔴 — ex: TCLE pendente OBRIGATORIO se mencionar antes-e-depois; ausencia de alternativas em procedimento invasivo; promessa de cura/garantia/100% detectada}

🟡 Verificar antes:
- {issues 🟡 — ex: jargao restante slide N (revisar speaker notes), tempos a confirmar com cirurgiao, disclaimer individual variation precisa ser dito verbalmente}

✅ OK:
- {confirmacoes — AIDET aplicado completo, alternativas mostradas, linguagem leiga em titulos, sem promessa de cura/garantia detectada}
