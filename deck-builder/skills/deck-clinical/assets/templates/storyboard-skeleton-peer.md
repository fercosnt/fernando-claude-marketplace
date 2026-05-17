# Deck: {nome-deck}

## Meta
- Skill geradora: deck-clinical
- Objetivo unico: {U1}
- Audiencia: {U2}
- Duracao: {U3} min
- Formato: {U4}
- Big Idea: {U5}
- Marca: {U6}
- Framework principal: EBM + Calgary-Cambridge {+ GRADE quando outcomes definidos}
- Modo: peer-facing
- max_ctas: 1
- Compliance tags: {ex: anvisa-laser-classe-iii, cfo-cfm}
- Gerado em: {ISO date}
- Versao: v1
- Storyboard ID: STORYBOARD-{slug}-{YYYYMMDD-HHmm}

## Estrutura Narrativa
Calgary-Cambridge adaptado: caso clinico abre, evidencia justifica, protocolo opera, outcome+follow-up validam. Bloco evidencia separado do protocolo. GRADE explicito por outcome. Antes-e-depois SEMPRE com TCLE mencionado no body. COI + Anvisa em slide proprio.

---

## Slide 1 — Capa
Tipo: capa
Action title: {headline assertivo conectado a Big Idea, NAO descritivo}
Mensagem-chave: {1 frase}
Speaker notes: {abertura curta, CRO + credenciais do relator, contexto da apresentacao 2-3 paragrafos}
Visual: {tom clinico, sem cosmetico-vendedor}
Prompt de imagem: {deck-image-prompts preenche — tipo na whitelist}
Tempo estimado: 45-60s

## Slide 2 — Caso clinico abertura
Tipo: problema
Action title: "Caso: {perfil paciente} — {problema principal apresentado}"
Mensagem-chave: paciente real, anonimo, problema concreto
Speaker notes: descrever caso de forma engajante — idade, queixa principal, historico, tentativas anteriores. NAO comecar com teoria.
Visual: {esquema clinico inicial OU foto crop area tratada}
Prompt de imagem: {deck-image-prompts preenche}
Tempo estimado: 90-120s

## Slide 3 — Problema clinico geral
Tipo: problema
Action title: "{Limitacao quantificada da abordagem atual}" (ex: "Peroxido falha em 30-40% dos casos com recessao")
Mensagem-chave: gancho — por que precisamos de alternativa
Speaker notes: contextualizar dentro do estado da arte clinico
Prompt de imagem: skip — tipo cabe mas use grafico se citar numero
Tempo estimado: 60s

## Slide 4 — Mecanismo de acao
Tipo: conceitual
Action title: "{Como funciona o protocolo proposto, 1 frase mecanistica}"
Mensagem-chave: principio fisico/biologico
Speaker notes: esquema visual + 1-2 paragrafos
Visual: esquema anatomico/fisiopatologico
Prompt de imagem: {deck-image-prompts preenche — conceitual}
Tempo estimado: 60-90s

## Slide 5 — Estado da evidencia
Tipo: dados
Action title: "GRADE {nivel} para {outcome principal}" — se multiplos outcomes, multiplos slides
Mensagem-chave: nivel de evidencia citado, papers de referencia
Speaker notes: explicar tipo de estudo, tamanho de amostra, risco de vies
Visual: tabela GRADE OU forest plot se aplicavel
Prompt de imagem: skip por default (override --include-dados se ilustracao academica)
Tempo estimado: 90-120s

## Slide 6 — Protocolo passo-a-passo
Tipo: conceitual
Action title: "Protocolo: {parametros chave} ({N} sessoes)"
Mensagem-chave: dosimetria + sequencia
Speaker notes: passo a passo + alertas clinicos
Visual: fluxograma do protocolo
Prompt de imagem: {deck-image-prompts preenche}
Tempo estimado: 90-120s

## Slide 7 — Demo procedural
Tipo: demo
Action title: "{Procedimento demonstrado}"
Mensagem-chave: ver e crer
Speaker notes: narrar enquanto mostra
Visual: foto procedimento OU video frame
Prompt de imagem: {deck-image-prompts preenche — demo + tom clinico}
Tempo estimado: 90-180s

## Slide 8 — Antes-e-depois
Tipo: comparativo
Action title: "{Outcome quantificado}" (ex: "Delta SGU 6 unidades, 4 sessoes")
Mensagem-chave: caso real
Speaker notes: SEMPRE incluir: "TCLE assinado pelo paciente, finalidade educativa, conforme CFO Res. 196/2019."
Visual: antes/depois lado-a-lado, crop area tratada (sem rosto identificavel se possivel)
Prompt de imagem: {deck-image-prompts preenche — incluir placeholder TCLE + tom clinico}
Tempo estimado: 60-90s

## Slide 9 — Outcome curto-prazo
Tipo: dados
Action title: "{Sumario N pacientes, outcome imediato}"
Mensagem-chave: resultados pos-procedimento
Speaker notes: numeros + interpretacao clinica
Prompt de imagem: skip
Tempo estimado: 60s

## Slide 10 — Follow-up
Tipo: dados
Action title: "{Outcome em 6m/12m — recidiva, manutencao}"
Mensagem-chave: durabilidade do efeito
Speaker notes: dados de follow-up + limites (se follow-up curto)
Prompt de imagem: skip
Tempo estimado: 60-90s

## Slide 11 — Compliance + COI
Tipo: disclaimer
Action title: "Disclosures e regulatorio"
Mensagem-chave: registro + COI
Speaker notes:
- Equipamento: {fabricante + modelo} — registro Anvisa {NUMERO REAL OU PLACEHOLDER}, Classe {N}
- COI: {declaracao explicita — patrocinio, KOL status, consultoria}
- Uso conforme bula OU off-label explicitamente declarado
Visual: texto-only
Prompt de imagem: skip — tipo disclaimer
Tempo estimado: 30s

## Slide 12 — Discussao + Q&A (CTA)
Tipo: CTA
Action title: "{Topicos de discussao antecipados — 3-5 perguntas previsiveis}"
Mensagem-chave: convite ao dialogo
Speaker notes: lista de perguntas antecipadas com respostas curtas
Prompt de imagem: skip
Tempo estimado: tempo restante para Q&A

---

## Apendice (slides opcionais — off-stage)

### Apendice A — Papers de referencia
Tipo: apendice
5 referencias completas (autor + ano + titulo + journal + DOI).

---

## Storyboard de Imagens (handoff pra deck-image-prompts)
- Slide 1 (capa): {brief}
- Slide 2 (problema): {brief — paciente anonimo, tom clinico}
- Slide 4 (conceitual): {brief — esquema anatomico/fisiopatologico}
- Slide 6 (conceitual): {brief — fluxograma protocolo}
- Slide 7 (demo): {brief — foto procedimento, tom clinico}
- Slide 8 (comparativo): {brief — antes/depois COM placeholder TCLE, crop area, sem identificacao}

## Checklist de Revisao (handoff pra deck-reviewer)
- [ ] Action titles (nao titulos descritivos)
- [ ] 1 ideia por slide
- [ ] Horizontal logic test
- [ ] Hook do slide 1 testado contra /copy
- [ ] CTA unico (max_ctas: 1)
- [ ] Compliance CFO/CFM/Anvisa preenchido abaixo
- [ ] Citacoes com GRADE em slide(s) de evidencia
- [ ] Antes-e-depois com TCLE mencionado no body

## Compliance & Disclaimers (3 tiers — D7)

🔴 Issues bloqueantes (resolver antes de apresentar):
- {issues 🔴 — ex: registro Anvisa placeholder pendente, off-label sem disclaimer}

🟡 Verificar antes:
- {issues 🟡 — ex: COI graduacao, dosimetria conforme bula, off-label disclaimer explicito no body}

✅ OK:
- {confirmacoes — TCLE mencionado, GRADE citado, COI declarado, Anvisa Classe N referenciada}
