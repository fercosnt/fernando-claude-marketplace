# Sales Checklist — autoaplicar antes de fechar STORYBOARD

> Checklist final do `deck-sales`. Roda automaticamente antes do output. Toda linha 🔴 vira issue bloqueante no `Compliance & Disclaimers` do storyboard.

## Estrutural (schema §10.2)

- [ ] Cabecalho `## Meta` completo (Skill geradora, Objetivo, Audiencia, Duracao, Formato, Big Idea, Marca, Framework, Modo, max_ctas, Gerado em, Versao, Storyboard ID)
- [ ] Seccao `## Estrutura Narrativa` com 2-3 paragrafos
- [ ] Todos os slides numerados com Tipo + Action title + Mensagem-chave + Speaker notes (2-3 paragrafos) + Visual + Prompt de imagem + Tempo estimado + Objecao esperada
- [ ] Seccao `## Apendice` presente (mesmo que vazia)
- [ ] Seccao `## Storyboard de Imagens` com handoff para `deck-image-prompts`
- [ ] Seccao `## Checklist de Revisao` para `deck-reviewer`
- [ ] Seccao `## Compliance & Disclaimers` com 3 tiers (🔴 🟡 ✅)

## Narrativa (Challenger + Gap + Raskin)

- [ ] Slide 1 = capa com action title = Big Idea (NAO "Apresentacao da Empresa")
- [ ] Slide 2 = insight provocador Challenger
- [ ] Slide 2 contem dado de mercado + reframe + implicacao no cliente
- [ ] Slide 2 NAO contem: "obrigado pela reuniao", "vamos apresentar", "agenda do dia", "deixa eu me apresentar"
- [ ] Slides 3-5 = Gap Selling (Current State quantificado / Custo do status quo em R$ / Future State)
- [ ] Slide 6 (modo padrao) = Old World vs New World (Raskin) com visual lado a lado
- [ ] Slide 5 (modo demo-presentation) = OUTPUT FINAL do produto (Do the Last Thing First)
- [ ] Action titles em TODOS os slides (frase assertiva, nao titulo descritivo)
- [ ] 1 ideia por slide
- [ ] Horizontal logic test: ler so action titles → narrativa coerente

## ROI / Payback (LOCKED — RNF compliance)

- [ ] Slide 12 contem Payback em meses
- [ ] Slide 12 mostra inputs (sessoes/mes, receita/sessao, custo operacional/mes)
- [ ] Slide 13 contem Sensitivity 3 cenarios (Pessimista / Base / Otimista)
- [ ] Receita usada e LIQUIDA (descontados custos operacionais)
- [ ] Sem absolutos ("garantimos", "asseguramos") — usar "tipicamente", "em cenarios similares"
- [ ] Headline = Payback no cenario BASE (nao otimista)
- [ ] Se NPV usado: taxa de desconto declarada
- [ ] Sem comparativo de payback com concorrente sem fonte publica

## Comparativo responsavel (LOCKED — risco juridico)

- [ ] Slide 14 (se presente) cita concorrentes pelo que ELES fazem bem
- [ ] Slide 14 posiciona voce pelo que FAZ UNICO
- [ ] Sem adjetivo pejorativo sobre concorrente ("caro", "ruim", "lento", "ultrapassado")
- [ ] Sem comparativo de preco sem fonte publicada
- [ ] Sem matriz com Xs pejorativos / smileys negativos
- [ ] Speaker notes do slide 14 SEM badmouth (vendedor le, risco soltar em call)
- [ ] Tom de respeito profissional ao concorrente
- [ ] Caso de cliente que migrou (se citado): motivo concreto + sem difamacao

## CTA (max_ctas: 1)

- [ ] UM unico CTA no slide final (NAO multiplos)
- [ ] CTA tem acao especifica + data concreta
- [ ] CTA alinhado ao estagio do funil (discovery / demo / closing)

## Cases / Prova social

- [ ] Slide 11 contem case real (NAO generico)
- [ ] Cliente citado tem autorizacao publica OU foi anonimizado
- [ ] Metrica do case e quantitativa (NAO qualitativa)
- [ ] Speaker notes anotam NDA se cliente nao puder ser nominado

## Compliance por marca

### Fotona / laser
- [ ] 🟡 Disclaimer ANVISA Classe III no apendice
- [ ] Sem promessa de cura ou eficacia 100%
- [ ] Cita resolucoes ANVISA pertinentes se aplicavel

### Beauty Smile / odontologia BR
- [ ] 🟡 CFO Resolucao 196/2019 (publicidade odontologica)
- [ ] Before/after no slide 11 (se houver) com consentimento expresso do paciente
- [ ] Sem promessa de resultado especifico paciente-a-paciente

### Generico
- [ ] CONAR art. 32 (sem denegrir produto/marca alheia)
- [ ] Lei 9.279/96 art. 195 (sem concorrencia desleal)

## Padrao BR (overlay cultural)

- [ ] Slide 11 (prova social) ganha peso desproporcional vs US/EU
- [ ] Slide 16/17 (investimento) oferece valor nao-monetario (treinamento extra, certificacao, suporte) antes de mexer no preco
- [ ] CTA pode incluir componente presencial se contexto permitir
- [ ] Speaker notes mencionam gatekeeper/secretaria como parte do processo (se aplicavel)

## Modos

### Modo `padrao`
- [ ] 15-18 slides
- [ ] Estrutura Challenger + Gap + Raskin
- [ ] Slides 12-13 ROI/Sensitivity
- [ ] Slide 14 comparativo responsavel

### Modo `demo-presentation`
- [ ] 12-15 slides
- [ ] Slide 3 = recap discovery
- [ ] Slide 5 = Do the Last Thing First (output final do produto)
- [ ] Slides 6-9 = peel back layers
- [ ] Slide 12 = ROI no minuto 38-46 (Gong Labs timing)
- [ ] Slide 15 = CTA tecnico (POC / Pilot / SOW)

## PAS opcional (se ativado)

- [ ] Slides PAS inseridos entre slide 2 e slide 3 (renumeracao)
- [ ] Slide PAS-Problem = dor emocional
- [ ] Slide PAS-Agitate = implicacao identitaria
- [ ] Slide PAS-Solution-bridge = transicao para Gap Selling racional
- [ ] PAS NAO substituiu Gap Selling (adicionou apenas)

## Saida

- [ ] Path: `$DECKS_DIR/{YYYY-MM}/STORYBOARD-{slug}-{HHmm}.md`
- [ ] Slug kebab-case max 30 chars
- [ ] Versao v1 inicial
- [ ] Frontmatter NAO presente no STORYBOARD (e o cabecalho `## Meta` que cumpre)

## Pos-geracao (opcional)

- [ ] Invocar `deck-image-prompts` para slides whitelist (capa, problema, conceitual, comparativo, demo, prova-social)
- [ ] Sugerir `/deck review` se alta consequencia (deal >= R$200k OU C-level cliente OU primeiro pitch importante)

## Falhas conhecidas (NAO fazer)

- ❌ Slide 1 sobre "quem somos" (timeline empresa, logos, escritorios)
- ❌ Feature-dump linear sem CAR
- ❌ Demo seguindo UI do produto (login → dashboard → config)
- ❌ ROI sem premissas explicitas ("300% em 12 meses!")
- ❌ CTA multiplo ou generico
- ❌ Badmouth de concorrente
- ❌ Abertura cerimonial no slide 2
- ❌ Promessa absoluta ("garantimos X%")
- ❌ Caso ficticio passado como real
- ❌ Sensitivity so com cenario otimista
