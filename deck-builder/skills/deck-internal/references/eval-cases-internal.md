# Eval Cases — deck-internal

3 cases que cobrem os 4 modos (pitch-to-leadership, concept-reveal D3 pipeline, all-hands com mudanca organizacional). Modo `strategy-presentation` validado indiretamente via overlap de framework com pitch.

---

## Case 1 — Pitch interno Beauty Smile: "Nova politica viagens corporativas com ROI" (Walkthrough 3 §12)

### Contexto

Convencer CEO Beauty Smile a aprovar nova politica de viagens corporativas condicional a ROI ≥3x antes do fim do trimestre. Reuniao 1:1 de 30min. Ja existe pre-alinhamento basico, mas CEO ainda nao viu numeros consolidados.

### Input

- **U1 (objetivo):** "CEO aprovar formalmente a politica de viagens corporativas condicional a ROI ≥3x antes do fim de Q3"
- **U2 (audiencia):** CEO Beauty Smile, 1 pessoa, conhece o problema parcialmente (ja autorizou 4 viagens em 2024)
- **U3 (duracao):** 8-10 min (opcao 2)
- **U4 (formato):** call remota 1:1
- **U5 (Big Idea):** "Toda viagem corp paga vira oportunidade investida, nao gasto"
- **U6 (marca):** Beauty Smile (auto-detect via regex `\bBeauty Smile\b`)
- **I1 (decisor):** CEO unico decisor
- **I2 (tipo):** aprovacao formal (NAO so buy-in)
- **I3 (ask especifico):** aprovacao da politica + budget pool inicial R$80k para Q3
- **I4 (business case):** 4 viagens corp em 2024 — 3 com ROI documentado (Wellness Mexico 4.2x, ICOI Boston 3.8x, AAOMS Chicago 5.1x) + 1 sem ROI atribuivel (Carnaval Rio — networking soft)
- **I5 (resistencia):** "CEO pode achar burocratico demais — preocupacao com friccao no time"

### Expected output

**Modo:** `pitch-to-leadership` (9 slides + anexo 6-pager)

**Estrutura esperada:**

| Slide | Tipo | Conteudo |
|-------|------|----------|
| 1 | Capa | "Politica viagens corp 2026 — toda viagem paga retorna investida" (action title relacional pre-BLUF) |
| 2 | **BLUF** (Pyramid Minto) | "Aprovar politica viagens com ROI ≥3x e budget pool R$80k para Q3, esperando reduzir gasto desperdicado em R$240k/ano com decisao hoje para implementacao em junho" |
| 3 | Problema/Status Quo (Raskin) | 4 viagens 2024 sem politica formal, 1 sem ROI atribuivel = R$60k em zona cinza |
| 4 | Solucao proposta | Politica de gating: aprovacao trimestral + ROI mensuravel por viagem + dashboard pos-viagem |
| 5 | Business case | Tabela 4 viagens 2024: Wellness Mexico R$32k → R$135k ROI; ICOI Boston R$28k → R$107k; AAOMS Chicago R$45k → R$229k; Carnaval Rio R$60k → sem ROI. Media 3.5x; sem politica = 25% sem retorno |
| 6 | Friccao mitigada (objecao I5) | Politica enxuta: 1 formulario pos-viagem (5 min) + dashboard automatico via planilha compartilhada. NAO comite de aprovacao previa. CEO aprova trimestral, time submete pos-viagem |
| 7 | Ask especifico (I3) | Aprovar politica HOJE + liberar R$80k pool para Q3 (max 3 viagens Q3) + revisao em outubro com dados Q3 |
| 8 | Proximos passos | Implementacao junho/2026; primeira revisao outubro/2026; politica completa em RH ate 30/maio |
| 9 | Q&A backup | 3 perguntas antecipadas: "e se viagem nao tiver ROI?", "quem aprova excecao?", "como medir networking soft?" |

**ANEXO obrigatorio:** `STORYBOARD-politica-viagens-ceo-XX.6pager.md` no mesmo diretorio.

**Schema do 6-pager esperado:**
1. **Introducao** (1 paragrafo): contexto + escopo
2. **Goals**: ROI medio ≥3x, ≥80% das viagens com ROI atribuivel, satisfacao do time ≥7/10
3. **Tenets**: viagem como investimento (nao perk); ROI mensuravel antes da viagem; pos-viagem obrigatorio em 7 dias
4. **State of business**: 4 viagens 2024, total R$165k, ROI medio 3.5x mas com 25% sem retorno
5. **Lessons learned**: viagens com pre-objetivo SMART → 100% ROI; sem pre-objetivo → 0% ROI
6. **Strategic priorities**: implementar politica junho; review trimestral; expandir pool em 2027 se ROI Q3 ≥3x

### Verificacoes do eval

- [ ] BLUF e slide 2 (NAO slide 8 — sem enterrar o lede)
- [ ] BLUF tem 5 elementos: recomendacao + investimento + retorno + prazo + ask
- [ ] Slide 6 enderaca explicitamente I5 (friccao = preocupacao do CEO)
- [ ] Slide 7 e ASK ESPECIFICO (R$80k + Q3 + decisao hoje), NAO vago
- [ ] Anexo 6-pager existe como arquivo separado `.6pager.md`
- [ ] 6-pager tem 6 secoes canonicas (intro, goals, tenets, state, lessons, priorities)
- [ ] 6-pager regras de escrita: ≤30 palavras por sentenca, sem bullets no corpo, prosa densa
- [ ] Schema §10.2 STORYBOARD valido
- [ ] Frontmatter Meta tem `Skill geradora: deck-internal`, `Framework principal: Pyramid Minto + Raskin`, `Modo: pitch-to-leadership`, `max_ctas: 1`, `Anexo 6-pager: sim`
- [ ] Auto-detect Beauty Smile carregou `beauty-smile-design-system`
- [ ] Pelo menos slides 1, 3 tem `Prompt de imagem:` preenchido (whitelist D5)
- [ ] Slides 5 (financeiro) e 9 (Q&A) tem `Prompt de imagem: —` (skip D5)

---

## Case 2 — Concept reveal "Sala VIP Carnaval 360 com IA hospedeira" (D3 PIPELINE)

### Contexto

Board do Carnaval 360 vai decidir aprovar conceito da Sala VIP + liberar budget R$1.5M para execucao. Skill-cenografia JA gerou renders + mood + layout em pasta dedicada.

### Input

- **U1 (objetivo):** "Board aprovar conceito Sala VIP + liberar budget R$1.5M execucao"
- **U2 (audiencia):** Board Carnaval 360, 5 pessoas, mix de comercial + curador artistico
- **U3 (duracao):** 15-20 min (opcao 3)
- **U4 (formato):** apresentacao presencial
- **U5/C2 (Big Idea sensorial):** "Sala VIP que te reconhece — IA hospedeira transforma o que e ser VIP em evento"
- **U6 (marca):** Carnaval 360 (auto-detect via regex `\bCarnaval 360\b`)
- **I1 (decisor):** Board (5 pessoas)
- **I2 (tipo):** aprovacao formal de conceito + budget
- **I3 (ask especifico):** aprovar conceito + liberar R$1.5M + cronograma execucao 90 dias
- **I4 (business case):** projecao 200 VIPs/noite × 6 noites × R$2.5k ingresso = R$3M receita VIP; ROI esperado 2x ano 1
- **I5 (resistencia):** "Board pode achar que IA hospedeira e gimmick — preocupacao com adocao do publico"
- **C1 (path artefatos):** `/Users/fernando/Cursor Repo/Eventos/cenografia/sala-vip-carnaval360-2026/`

### Pre-condicao

Pasta `cenografia/sala-vip-carnaval360-2026/` JA existe com:
- `renders/render-hero-sala-vip-v2.png`
- `renders/render-detalhe-iluminacao.png`
- `renders/render-bar-vip.png`
- `renders/render-area-foto.png`
- `mood/mood-board-textura.png`
- `mood/mood-board-iluminacao.png`
- `prompts/nano-banana-pro-prompts.json`

### Expected output

**Modo:** `concept-reveal` (8 slides Sparkline Duarte)

**Estrutura esperada:**

| Slide | Tipo | Visual | Conteudo |
|-------|------|--------|----------|
| 1 | Capa mood | mood-board-iluminacao.png (path absoluto) | "Imagine entrar em uma sala que ja te conhece" |
| 2 | Big Idea sensorial | — (texto) | "Sala VIP que te reconhece — IA hospedeira transforma o que e ser VIP em evento" |
| 3 | What is (status quo desconfortavel) | gerado via deck-image-prompts (capa fake) | Sala VIP generica = chip mais caro, mesmo servico, dezenas de eventos identicos |
| 4 | **What could be (REVEAL)** | **render-hero-sala-vip-v2.png** (path absoluto + prompt verbatim do JSON cenografia) | Walk-through 1ª pessoa: "Voce chega. A Eva te chama pelo nome. Ela sabe que voce e fa do MC Marcinho, que voce gosta de mojito sem gelo..." |
| 5 | Detalhe iluminacao + mood | render-detalhe-iluminacao.png + mood-board-textura.png | Luz indireta como onda, textura de areia molhada nas paredes acusticas |
| 6 | Detalhe bar + foto | render-bar-vip.png + render-area-foto.png | Bar com IA que sugere drink + area foto generativa |
| 7 | Ask executivo (I3) | — (texto + tabela) | R$1.5M (R$600k cenografia + R$400k IA dev + R$300k integracao + R$200k operacao 6 noites) + cronograma 90 dias |
| 8 | Proximos passos | — | Aprovar conceito hoje; contrato fornecedores ate 30/maio; soft-launch primeira noite ago/2026 |

**Pipeline validado:**
- [ ] Slides 4, 5, 6 tem campo `Visual:` com **path ABSOLUTO** dos renders cenografia
- [ ] Slides 4, 5, 6 tem `Prompt de imagem:` copiado VERBATIM do `prompts/nano-banana-pro-prompts.json`
- [ ] Slide 4 NAO regerou prompt (deck-internal usou o que cenografia ja produziu)
- [ ] Slide 3 (what is) usou `deck-image-prompts` para gerar capa fake (cenografia nao tem render de "sala VIP generica")
- [ ] Slide 1 (capa mood) usou mood-board existente da cenografia
- [ ] Slides 2, 7, 8 tem `Prompt de imagem: —` (skip)
- [ ] Frontmatter Meta tem `Artefatos cenografia: /Users/fernando/Cursor Repo/Eventos/cenografia/sala-vip-carnaval360-2026/`
- [ ] Framework principal = Sparkline Duarte
- [ ] Modo = concept-reveal
- [ ] Sparkline correto: 2 vales antes do reveal slide 4 (slide 3 what is = 1º vale; slide 4 = pico/reveal)
- [ ] Big Idea sensorial slide 2 (NAO slide 1)
- [ ] Walk-through 1ª pessoa no slide 4 (speaker notes)
- [ ] Ask especifico slide 7 (R$1.5M + cronograma + criterio aprovacao)

---

## Case 3 — All-hands Q1 Beauty Smile com mudanca organizacional

### Contexto

All-hands trimestral Q1 2026 da Beauty Smile. Empresa toda (40 pessoas + presencial + remoto). Nova estrutura organizacional sera anunciada (criacao de unidade dedicada para clinica B2B). Time tem ansiedade sobre mudancas.

### Input

- **U1 (objetivo):** "Time entende a nova estrutura organizacional + se alinha com prioridades Q1"
- **U2 (audiencia):** 40 pessoas, mix IC a VP, presencial + remoto, areas mistas
- **U3 (duracao):** 60min (opcao 5)
- **U4 (formato):** hibrido presencial + remoto
- **U5 (Big Idea):** "Beauty Smile cresce ao se especializar — B2B clinico ganha unidade dedicada"
- **U6 (marca):** Beauty Smile (auto-detect)
- **I1 (decisor):** empresa toda (alinhamento, nao decisao)
- **I2 (tipo):** alinhamento (NAO decisao)
- **I3 (ask especifico):** nenhum ask formal (apresentacao, nao pitch). Pedido implicito: engajar com nova estrutura
- **I4 (business case):** Q4 2025 crescimento 38%; receita B2B clinico cresceu 87% (de R$2.1M para R$3.9M); B2C estavel
- **I5 (resistencia):** "Ansiedade do time sobre quem vai pra qual unidade + medo de demissao"
- **A1 (mudanca organizacional?):** SIM — criacao de unidade B2B clinico dedicada, realocacao de 8 pessoas

### Expected output

**Modo:** `all-hands` (11 slides Sinek Why-How-What + Kotter visibilizado)

**Estrutura esperada:**

| Slide | Tipo | Conteudo |
|-------|------|----------|
| 1 | Abertura energizante | Video 60s recap Q4 (clientes, time, momentos) + boas-vindas CEO ao vivo |
| 2 | **Visao + proposito (Sinek WHY)** | "Beauty Smile existe para transformar como dentistas crescem suas clinicas — B2B clinico e onde a transformacao mais profunda acontece" |
| 3 | Estado do negocio | Q4 cresceu 38%; B2B clinico cresceu 87%; B2C estavel — leitura honesta do CEO, NAO so positivo (mencionar 2 friccoes operacionais) |
| 4 | Metricas-chave | 5 KPIs vs meta: receita total, receita B2B, NPS clientes, ciclo de vendas, headcount |
| 5 | Celebracoes Q4 | 3 historias de clientes + 5 peer shoutouts (multiplos apresentadores, nao so CEO) |
| 6 | **Topico estrategico 1 (Sinek HOW)** | "Para fazer B2B clinico melhor, criamos unidade dedicada — Kotter visibilizado: urgencia (87% growth), coalizao (3 lideres anunciados), visao (Beauty Clinic Solutions)" |
| 7 | Realocacao + estrutura | Quem vai pra unidade B2B (8 pessoas, anunciado por nome com convite previo, NUNCA surpresa publica), estrutura organizacional nova, sem demissoes (enderacar I5 explicitamente) |
| 8 | Reconhecimento individual | Peer shoutouts + premio "Beauty Star Q4" |
| 9 | **Prioridades Q1 (Sinek WHAT)** | 3 prioridades: lancar Beauty Clinic Solutions (B2B unit), sustentar B2C revenue, sistema NPS automatizado |
| 10 | Q&A aberto | 5 perguntas anonimas pre-coletadas; primeira pergunta obrigatoriamente de remoto |
| 11 | Proximos passos + encerramento | "Na sua semana: encontros com gestor sobre alocacao Q1 ate sexta. Em 2 semanas: kickoff B2B Solutions. Em 1 trimestre: primeira leitura do impacto." |

**Verificacoes do eval:**
- [ ] Sinek Why-How-What estrutural correto (slide 2 = WHY, slides 6-7 = HOW, slide 9 = WHAT)
- [ ] Slide 2 (visao) com 1 frase poderosa, emocional
- [ ] Slide 3 (estado do negocio) com leitura HONESTA (positivos + 2 friccoes, NAO so positivo)
- [ ] Slide 6 com Kotter visibilizado: urgencia + coalizao + visao
- [ ] Slide 7 enderaca I5 (ansiedade) explicitamente — anuncia que NAO ha demissoes + nomes de quem vai para unidade B2B
- [ ] Slide 5 (celebracoes) com multiplos apresentadores, NAO so CEO
- [ ] Slide 10 (Q&A) preparado com 5 perguntas anonimas pre-coletadas
- [ ] Primeira pergunta Q&A obrigatoriamente de remoto (hibrido)
- [ ] Arco emocional canonico respeitado: Energia alta → Sobriedade factual → Calor humano → Relevancia estrategica → Conexao pessoal → Abertura → Clareza
- [ ] Proporcao 30% factual / 70% engajamento (slides 4 + dados sao 30%; slides 1, 2, 5, 8, 10, 11 sao 70%)
- [ ] `max_ctas: 2` no Meta (override SHARED.md — all-hands pode ter 2)
- [ ] Modo = all-hands
- [ ] Framework principal = Sinek + Raskin + Kotter
- [ ] Anti-padroes evitados: NAO monologo CEO 30min; NAO apenas executivos como apresentadores; NAO metricas inconsistentes; NAO Q&A filtrado; NAO sem follow-up
- [ ] Slide 11 (proximos passos) tem ACOES CONCRETAS por horizonte temporal (semana / 2 semanas / 1 trimestre)

---

## Resumo dos cases (cobertura por modo + framework + DoD)

| Case | Modo | Frameworks | Pipeline D3 | 6-pager | BLUF slide 2 | Sinek | Kotter |
|------|------|------------|-------------|---------|--------------|-------|--------|
| 1 | pitch-to-leadership | Pyramid Minto + Raskin | NAO | **SIM** | **SIM** | NAO | NAO |
| 2 | concept-reveal | Sparkline Duarte | **SIM** | NAO | NAO | NAO | NAO |
| 3 | all-hands | Sinek + Raskin + Kotter | NAO | NAO | NAO | **SIM** | **SIM** |

DoD coverage: 4 modos (3 testados diretamente + strategy testado via overlap Pyramid no Case 1) × 6 frameworks × pipeline D3 + 6-pager + BLUF + Sinek estruturais.
