# Deck: {nome-deck}

## Meta
- Skill geradora: deck-sales
- Objetivo unico: {U1}
- Audiencia: {U2}
- Duracao: {U3} min
- Formato: {U4}
- Big Idea: {U5}
- Marca: {U6}
- Framework principal: Challenger Sale + Great Demo! (Do the Last Thing First) + ROI Sensitivity
- Modo: demo-presentation
- max_ctas: 1
- Gerado em: {ISO date}
- Versao: v1
- Storyboard ID: STORYBOARD-{slug}-{YYYYMMDD-HHmm}

## Estrutura Narrativa

Modo demo-presentation: 12-15 slides para demo guiada apos discovery. Slide 5 segue "Do the Last Thing First" (Cohan) — mostra OUTPUT FINAL do produto, nao login/dashboard/config. Slides 6-9 fazem "peel back the layers" sob demanda. Demo vencedora media (Gong Labs 67k demos): 47min duracao, talk:listen 65:35, max 76s de pitch continuo. Pricing entre minutos 38-46 (slide 12).

## Slide 1 — Capa
Tipo: capa
Action title: {Big Idea U5}
Mensagem-chave: 1 frase carrega o deck
Speaker notes: {2-3 paragrafos — abrir confirmando audiencia presente, ja no slide 2 anuncia insight (sem agenda cerimonial).}
Visual: cinematic
Prompt de imagem: {preenchido pela deck-image-prompts — capa whitelist D5}
Tempo estimado: 30 seg
Objecao esperada: —

## Slide 2 — Insight provocador (Challenger)
Tipo: problema
Action title: "{dado de mercado} + {reframe}"
Mensagem-chave: implicacao especifica
Speaker notes: {2-3 paragrafos. NUNCA "obrigado pela reuniao". Mesmo padrao do modo padrao.}
Visual: editorial impactante
Prompt de imagem: {preenchido pela deck-image-prompts}
Tempo estimado: 90 seg
Objecao esperada: "Esse dado vale pro meu caso?"

## Slide 3 — Recap discovery
Tipo: contexto
Action title: "Voce nos disse {X, Y, Z} — vamos enderecar nessa ordem"
Mensagem-chave: confirmacao do que ja foi discutido
Speaker notes: {2-3 paragrafos. Repete os 3 pontos principais da discovery anterior. Cria alinhamento + reduz ansiedade do prospect.}
Visual: 3 bullets visuais simples
Prompt de imagem: —
Tempo estimado: 60 seg
Objecao esperada: —

## Slide 4 — Promised Land especifico (Vision Generation Demo)
Tipo: conceitual
Action title: "Como e seu mundo se isso funcionar"
Mensagem-chave: future state vivido pelo prospect
Speaker notes: {2-3 paragrafos com VISAO do prospect operando no future state. Para executivos: Vision Generation Demos (Gong habit 6) — pintar cenario tangivel.}
Visual: foto / mockup do prospect no cenario futuro
Prompt de imagem: {preenchido pela deck-image-prompts — conceitual whitelist D5}
Tempo estimado: 90 seg
Objecao esperada: "Isso e plausivel pra mim?"

## Slide 5 — Output final do produto (Do the Last Thing First — Cohan)
Tipo: demo
Action title: "Resultado: {output mais valioso que o produto entrega}"
Mensagem-chave: o resultado FINAL — antes de explicar como
Speaker notes: {2-3 paragrafos. Mostre o OUTPUT FINAL nos primeiros 5 min. NAO segue UI do produto (login → dashboard → config). Mostra relatorio executivo / dashboard de impacto / automacao concluida.}
Visual: screenshot do output final / dashboard / relatorio
Prompt de imagem: {preenchido pela deck-image-prompts — demo whitelist D5}
Tempo estimado: 180 seg
Objecao esperada: "Como voce chegou nesse output?"

## Slide 6 — Peel back layer 1 (etapa final do fluxo)
Tipo: demo
Action title: "Como chegamos no output do slide anterior"
Mensagem-chave: ultima etapa do fluxo (mais proxima do output)
Speaker notes: {2-3 paragrafos com CAR (Context-Action-Result). Etapa final que produz o output.}
Visual: screenshot da etapa final
Prompt de imagem: {preenchido pela deck-image-prompts — demo whitelist D5}
Tempo estimado: 120 seg
Objecao esperada: —

## Slide 7 — Peel back layer 2 (etapa intermediaria critica)
Tipo: demo
Action title: "Etapa intermediaria: {nome da etapa}"
Mensagem-chave: ponto critico do meio do fluxo
Speaker notes: {2-3 paragrafos CAR}
Visual: screenshot etapa intermediaria
Prompt de imagem: —
Tempo estimado: 120 seg
Objecao esperada: —

## Slide 8 — Peel back layer 3 (integracoes / inputs)
Tipo: demo
Action title: "De onde vem os dados"
Mensagem-chave: integracoes / fontes de input
Speaker notes: {2-3 paragrafos. Integracoes com sistemas atuais do prospect. Reduz ansiedade de implementacao.}
Visual: diagrama de integracoes simples
Prompt de imagem: —
Tempo estimado: 90 seg
Objecao esperada: "Integra com {sistema X que ja uso}?"

## Slide 9 — Peel back layer 4 (setup/onboarding — opcional)
Tipo: contexto
Action title: "Onboarding tipico: {N} semanas"
Mensagem-chave: setup + treinamento
Speaker notes: {2-3 paragrafos sobre onboarding. Inclua APENAS se prospect perguntar — senao pular pra slide 10.}
Visual: timeline visual
Prompt de imagem: —
Tempo estimado: 60 seg
Objecao esperada: —

## Slide 10 — Casos de uso por persona
Tipo: contexto
Action title: "{Persona A} usa para {X}; {Persona B} usa para {Y}"
Mensagem-chave: cobertura multi-stakeholder do buying committee
Speaker notes: {2-3 paragrafos. 1 slide com 2-3 personas do buying committee do prospect. Cada persona tem 1 caso de uso especifico.}
Visual: 2-3 colunas (uma por persona)
Prompt de imagem: —
Tempo estimado: 90 seg
Objecao esperada: —

## Slide 11 — Prova social tecnica
Tipo: prova-social
Action title: "{S5} — {metrica chave}"
Mensagem-chave: case real similar ao prospect
Speaker notes: {2-3 paragrafos com case S5. Similar ao prospect (tamanho/setor/regiao).}
Visual: logo cliente + setting + metricas
Prompt de imagem: {preenchido pela deck-image-prompts — prova-social whitelist D5}
Tempo estimado: 90 seg
Objecao esperada: "Meu caso e diferente"

## Slide 12 — ROI / Payback
Tipo: financeiro
Action title: "Payback em {N} meses no cenario base"
Mensagem-chave: payback + linha do tempo
Speaker notes: {2-3 paragrafos com payback. Inputs visiveis. Conforme Gong Labs: timing ideal de pricing entre minutos 38-46 da demo.}
Visual: barra de tempo + break-even
Prompt de imagem: —
Tempo estimado: 90 seg
Objecao esperada: "Inputs realistas pro meu caso?"

## Slide 13 — Implementacao
Tipo: contexto
Action title: "Semana 0 → Mes 3 → Mes 6"
Mensagem-chave: timeline visual
Speaker notes: {2-3 paragrafos. Decisao → setup → treinamento → operacao → milestones de sucesso.}
Visual: timeline horizontal
Prompt de imagem: —
Tempo estimado: 60 seg
Objecao esperada: "Quanto tempo realmente pra operar?"

## Slide 14 — Comparativo responsavel (opcional)
Tipo: comparativo
Action title: "{Concorrente A} forte em {X} / Nos diferentes em {Z}"
Mensagem-chave: matriz fortalezas SEM badmouth
Speaker notes: {2-3 paragrafos — vide references/comparativo-responsavel.md. Incluir SE prospect mencionou comparacao explicita; SENAO pular.}
Visual: matriz simples
Prompt de imagem: {preenchido pela deck-image-prompts — comparativo whitelist D5}
Tempo estimado: 60 seg
Objecao esperada: "Por que voce e melhor que {concorrente}?"

## Slide 15 — CTA tecnico
Tipo: CTA
Action title: "Proximo passo: {Pilot / POC / SOW} em ate {data}"
Mensagem-chave: 1 acao tecnica especifica
Speaker notes: {2-3 paragrafos. UM CTA tecnico especifico com data. Pilot / POC / SOW preliminar. Gong: demos vencedoras gastam +12.7% mais tempo em proximos passos.}
Visual: minimalista
Prompt de imagem: —
Tempo estimado: 60 seg
Objecao esperada: —

## Apendice (slides opcionais)

- A1 — FAQ tecnica antecipada
- A2 — Specs detalhadas / datasheet
- A3 — Cases adicionais
- A4 — Roadmap produto (proximas releases)

## Storyboard de Imagens (handoff pra deck-image-prompts)

- Slide 1 (capa)
- Slide 2 (insight)
- Slide 4 (conceitual Promised Land)
- Slide 5 (demo output final)
- Slide 6 (demo layer 1)
- Slide 11 (prova-social)
- Slide 14 (comparativo — se incluido)

## Checklist de Revisao (handoff pra deck-reviewer)

- [ ] Slide 5 mostra OUTPUT FINAL (Do the Last Thing First)
- [ ] Slides 6-9 = peel back layers (NAO seguir UI do produto)
- [ ] Cada feature tem resposta explicita ao "e dai?" (CAR Framework)
- [ ] Action titles em todos os slides
- [ ] Slide 2 com insight provocador Challenger
- [ ] CTA unico tecnico no slide 15 (max_ctas=1)
- [ ] ROI/payback no slide 12 com inputs visiveis
- [ ] Comparativo SEM badmouth (se slide 14 incluido)
- [ ] Pricing timing: slide 12 = minuto 38-46 da demo
- [ ] Talk:listen ratio planejado 65:35

## Compliance & Disclaimers (3 tiers — D7)

🔴 Issues bloqueantes (resolver antes de apresentar):
- {se aplicavel}

🟡 Verificar antes:
- {se aplicavel — ANVISA / CFO / CONAR conforme marca}

✅ OK:
- Output final no slide 5 (Do the Last Thing First aplicado)
- Insight Challenger slide 2
- 1 CTA tecnico no slide 15
- Schema §10.2 valido
