---
name: deck-sales
description: Cria STORYBOARD para vendas B2B consultivas + demo de produto. Aplica Challenger Sale + Gap Selling + Raskin (Old World → New World) + PAS opcional. Use para sales deck, demo de produto, proposta B2B, recrutamento de franqueado, plano corporativo. Slide 2 SEMPRE insight provocador (nunca "obrigado pela reuniao"). ROI/payback obrigatorio. Comparativo SEM badmouth.
intent: action
effort: high
nb_ids:
  - 7f1b2e2b-4ba4-40de-ba56-ca2f55e2c0da
  - 5a0aaabb-78c1-4d03-a400-e9ce1973737b
references:
  - references/framework-challenger-gap-raskin.md
  - references/framework-pas.md
  - references/comparativo-responsavel.md
  - references/roi-payback.md
  - references/demo-presentation.md
  - references/eval-cases-sales.md
assets:
  - assets/templates/storyboard-skeleton-challenger.md
  - assets/templates/storyboard-skeleton-demo.md
  - assets/checklists/sales-checklist.md
---

# deck-sales

Skill vertical do plugin **deck-builder**. Gera `STORYBOARD-{slug}-{HHmm}.md` para vendas B2B consultivas e demos de produto, com narrativa Challenger Sale + Gap Selling + Andy Raskin (Old World → New World) + PAS opcional, ROI/payback explicito e comparativo responsavel (sem badmouth).

> **Esta skill NAO gera slides finais** (PPTX/Gamma/Figma) — produz apenas STORYBOARD.md schema §10.2. Designer/IA gera visual depois.

## Quando ativa

**Modo encadeado (via `deck-orchestrator`):** 2+ keywords da rota `deck-sales` na matriz §10.3 → roteia direto. Keywords: "vendas", "B2B", "demo", "proposta de software", "lead", "funil", "vender pra cliente", "recrutar franqueado", "plano corporativo".

**Modo direto (standalone):** `/deck-sales` ou frases tipo "preciso vender LightWalker pra clinica premium SP", "demo do produto pra diretor", "deck pra recrutar franqueado Beauty Smile".

**NAO ativa quando:** rota e fundraising (investidor/VC/captacao) → `deck-fundraising`. Proposta de servico/consultoria/M&A → `deck-proposal`. Aula/treinamento/curso → `deck-teaching`. Equipamento clinico em deck educacional → `deck-equipment`.

## Modos (2)

| Modo | Quando aplica | Estrutura | Slides | Template |
|------|--------------|-----------|--------|----------|
| `padrao` | Sales deck B2B consultivo geral | Challenger + Gap + Raskin | 15-18 | [storyboard-skeleton-challenger.md](assets/templates/storyboard-skeleton-challenger.md) |
| `demo-presentation` | Demo guiada de produto/servico (apos discovery) | Challenger + Great Demo! (Last Thing First) + ROI | 12-15 | [storyboard-skeleton-demo.md](assets/templates/storyboard-skeleton-demo.md) |

**Selecao automatica:** se input contem "demo", "demonstracao do produto", "demo presencial", "mostrar o produto funcionando" → `demo-presentation`. Senao → `padrao`.

## Fronteiras (LOCKED — SHARED.md §10.8)

- NAO gera slides finais (PPTX/Gamma/Figma) — so STORYBOARD.md
- NAO busca dados em tempo real (CIOSP datas, precos, etc.) — usuario fornece ou skill marca `{INPUT_USUARIO: ...}` no STORYBOARD
- NAO inventa cases de sucesso — se usuario nao fornecer em S5, slide prova-social vira generico ("inserir case real aqui") e marca em 🟡
- NAO faz badmouth de concorrente — risco juridico (Lei 9.279/96 art. 195). Detalhe em [references/comparativo-responsavel.md](references/comparativo-responsavel.md)
- NAO promete absolutos ("garantimos X%") — vira "tipicamente", "em cenarios similares observamos"
- NAO escreve post de redes sociais — delega `/copy`
- NAO chama APIs pagas sem confirmacao

## Protocolo (8 passos)

### Passo 1 — Auto-detection de marca (§10.5)

Antes da entrevista, rodar regex contra `~/.config/deck-builder/brands.yaml`:
- "Fotona", "LightWalker", "Er:YAG", "Nd:YAG" → marca = Fotona; carrega `laser-physics` se instalada; compliance tags `anvisa-laser-classe-iii`, `cfo-laser`
- "Beauty Smile" → marca = Beauty Smile; carrega `beauty-smile-design-system` se instalada; compliance tags `odontologia-br`, `cfo-cfm`
- "Carnaval 360" → marca = Carnaval 360; sem compliance tag
- Nenhum match → marca = generico; perguntar U6 na entrevista

### Passo 2 — Entrevista universal U1-U6 (§10.1)

Toda skill vertical roda U1-U6 ANTES de divergir. Se `deck-orchestrator` ja roteou via 2+ keywords da matriz, ele pulou U1-U3 — herdar do contexto. Saida → cabecalho `## Meta` do STORYBOARD.

### Passo 3 — Entrevista vertical S1-S5

Apos U1-U6 (e se input ainda nao trouxer dados), perguntar em ordem (uma por vez via `AskUserQuestion` ou pacote, dependendo do contexto):

| # | Pergunta | Default inferido |
|---|----------|------------------|
| S1 | Qual o ticket medio do produto/servico que voce vai vender? | inferir do U1 ("R$280k" ja resolve) |
| S2 | Ciclo de venda tipico (semanas/meses ate fechamento)? | 60-90d para healthcare premium |
| S3 | Quem decide na ponta cliente? (perfil + dor que esse decisor sente) | dentista-proprietario / CEO / diretor |
| S4 | Maior objecao recorrente em vendas (a que mais derruba deal)? | preco / ROI vs concorrente X / risco de adocao |
| S5 | Caso de sucesso mais forte que voce pode citar com nome (cliente, metrica, payback)? | se vazio → "inserir case real" em 🟡 |

**Antifricoes:**
- Se ja tem `BRIEF.md` ou contexto de sessao com essas respostas, NAO perguntar
- Se input do usuario ja respondeu (ex: "R$280k em 60 dias pra dentista-proprietario premium SP, derrota frequente para Lumenis, cliente referencia Smile Premium SP payback 14m"), NAO perguntar — confirmar interpretacao

### Passo 4 — Consultar NBs (cache-first, falha nao bloqueia)

```bash
notebooklm use 7f1b2e2b-4ba4-40de-ba56-ca2f55e2c0da   # NB1 Core
notebooklm ask "Padrao Andy Raskin Old World/New World para {marca + vertical}. Big Idea: {U5}" --max-citations 5

notebooklm use 5a0aaabb-78c1-4d03-a400-e9ce1973737b   # NB3 Comerciais
notebooklm ask "Sales deck B2B consultivo {ticket_S1} ciclo {S2} para {audiencia_U2}. Padrao Challenger + Gap Selling. Big Idea: {U5}" --max-citations 5
```

Cite ate 3 fontes por NB. Falha de NB → warning + degrade para references locais.

### Passo 5 — Selecionar modo + framework stack

- Modo `padrao` → stack Challenger (insight provocador slide 2) + Gap Selling (Current State → custo do status quo → Future State slides 3-5) + Raskin (Old World vs New World slide 6) + ROI sensitivity (slides 12-13)
- Modo `demo-presentation` → stack Challenger insight (slide 2) + Great Demo! "Do the Last Thing First" (slide 5 mostra output final do produto) + jornada produto reversa (slides 6-9) + ROI (slides 10-11)

**PAS opcional:** se S3 mencionar decisor "menos tecnico", "C-level que nao entra em detalhe", "comprador relacional/emocional" → INSERIR slides PAS antes do Gap Selling (slide 3 = Problem, slide 4 = Agitate emocional, depois Gap quantifica). Detalhe em [references/framework-pas.md](references/framework-pas.md).

### Passo 6 — Gerar STORYBOARD com schema §10.2

Estrutura padrao em [references/framework-challenger-gap-raskin.md](references/framework-challenger-gap-raskin.md). Use template em [assets/templates/storyboard-skeleton-challenger.md](assets/templates/storyboard-skeleton-challenger.md) (ou skeleton-demo.md para modo demo).

**REGRAS DURAS:**
- Slide 1 = capa com action title (NAO "Apresentacao da {empresa}" — sim "{Big Idea}" ou variante)
- Slide 2 = **insight provocador Challenger** (NUNCA comeca com "obrigado pela reuniao", "vamos apresentar a empresa", "agenda do dia"). Formato: dado de mercado + reframe + implicacao no cliente. Ex: "Ate 2027, 80% dos high-end paraestesico ja terao laser. Quem esperar 24 meses vira commodity."
- Action titles em TODOS os slides (frase assertiva, nao titulo descritivo). "Payback em 14 meses" > "ROI"
- 1 ideia por slide
- Speaker notes 2-3 paragrafos por slide (vendedor le, nao decora)
- `max_ctas: 1` (regra global; teaching/scientific tem override, sales NAO)
- Comparativo (slide 14): formato "Nos somos X especialistas em Y. Concorrente Z e forte em W mas diferente em escopo." NUNCA "Concorrente Z e ruim porque..."
- ROI/payback: usar Sensitivity Analysis 3 cenarios (pessimista/base/otimista) — formato em [references/roi-payback.md](references/roi-payback.md)
- CTA unico, especifico, com data ("Agendar call com COO em ate 7 dias" > "Entrar em contato")

### Passo 7 — Invocar `deck-image-prompts` (whitelist D5)

Apos STORYBOARD gerado, montar lista de slides whitelist e invocar a skill auxiliar:

- **Preencher prompt:** slide 1 (capa) | slide 2 (insight/problema) | slide 6 (Old vs New conceitual) | slide 11 (prova-social) | slide 14 (comparativo) | qualquer slide demo no modo demo-presentation
- **Skip:** slides dados/financeiro (12-13), CTA (final), disclaimer, agradecimento

Se `deck-image-prompts` nao instalada, marcar `**Prompt de imagem:** —` e seguir.

### Passo 8 — Compliance + handoff opcional

Aplicar tags de compliance da marca (§10.5):
- Fotona/laser → 🟡 ANVISA Classe III mencionar disclaimer no apendice; sem promessa de cura ou eficacia 100%
- Beauty Smile/odontologia → 🟡 CFO Resolucao 196/2019 (publicidade odontologica) — sem before/after sem consentimento expresso do paciente
- Generico → so checar contra checklist em [assets/checklists/sales-checklist.md](assets/checklists/sales-checklist.md)

Sugerir (NAO executar sozinha) `/deck review` se deck = alta consequencia (deal >= R$200k OU primeiro pitch importante OU presenca de C-level cliente).

## Saida

**Path:** `$DECKS_DIR/{YYYY-MM}/STORYBOARD-{slug}-{HHmm}.md` (default `~/Documents/decks/2026-05/`).

**Slug:** kebab-case do Big Idea (U5) ou nome cliente, max 30 chars. Ex: `lightwalker-smile-premium-sp`.

**Conformidade schema:** §10.2 exato (cabecalho Meta + Estrutura Narrativa + slides numerados com Tipo/Action title/Mensagem-chave/Speaker notes/Visual/Prompt de imagem/Tempo estimado/Objecao esperada + Apendice + Storyboard de Imagens + Checklist de Revisao + Compliance & Disclaimers 3 tiers).

**Versionamento:** v1 inicial. Se usuario pedir revisao na mesma sessao → v2 com `--version v2` no nome do arquivo.

## Frameworks (resumo — detalhe em references)

### Challenger Sale (Dixon/Adamson) — base do deck
Insight provocador → reframe do problema (cliente nao sabia que tinha) → tensao racional + emocional → ensina algo novo antes de vender. **Slide 2 e SEMPRE Challenger** — nunca abertura cerimonial.

### Gap Selling (Keenan) — Current → Gap → Future
Current State (onde cliente esta hoje, quantificado) → custo do status quo (Gap dimensionado em R$ ou tempo) → Future State (onde precisa estar) → solucao como ponte. **Custo do status quo deve ser explicito** — ex: "Cada paciente premium que voce nao consegue oferecer laser = R$ 4-8k de receita perdida + risco de defeccao."

### Andy Raskin (Old World → New World, atualizado 2023 "Old Game / New Game")
Slide 6: transformacao narrativa visual. **Foco em mudanca de mentalidade do buyer**, nao em produto. Inimigo = velho modelo mental, NAO concorrente. Ex: "Velho mundo: dentista compra equipamento isolado. Novo mundo: dentista compra plataforma de diferenciacao competitiva."

### PAS opcional (Problem → Agitate → Solution)
Para decisores menos tecnicos, hook emocional antes de logica. Detalhe em [references/framework-pas.md](references/framework-pas.md).

### Great Demo! (Peter Cohan, modo `demo-presentation`)
"Do the Last Thing First" — mostre o resultado de maior valor nos primeiros 5min. Depois "peel back the layers". Detalhe em [references/demo-presentation.md](references/demo-presentation.md).

## Comparativo responsavel (LOCKED — risco juridico)

Detalhe em [references/comparativo-responsavel.md](references/comparativo-responsavel.md). Em uma frase: cite concorrentes pelo que ELES fazem bem, posicione-se pelo que VOCE faz unico, NUNCA inverta. Vide Lei 9.279/96 art. 195 (concorrencia desleal).

**Formato canonico do slide 14 (comparativo):**
```
{Concorrente A} — forte em {dimensao X}, atende {publico Y}.
{Concorrente B} — forte em {dimensao Z}, atende {publico W}.
Nos — diferente em {dimensao K} para {publico do prospect}.
```
NUNCA: "X e caro", "Y nao funciona", "Z e ruim de suporte".

## ROI/payback obrigatorio (LOCKED — RNF compliance bundle)

Detalhe em [references/roi-payback.md](references/roi-payback.md). Em todo STORYBOARD `deck-sales`, slides 12-13 DEVEM conter:
- Payback Period em meses (Investimento Total ÷ Receita Adicional Mensal liquida)
- Sensitivity Analysis 3 cenarios (Pessimista / Base / Otimista) com inputs visiveis (transparencia metodologica — Forrester TEI / Nucleus)
- Premissas explicitas (sessoes/mes, receita por sessao, custo operacional)

Se usuario nao fornecer dados em S1-S5 suficientes para calcular, marcar slide 12 com `{INPUT_USUARIO: investimento + receita esperada}` e listar em 🔴 issues bloqueantes.

## Auto-detection de marca (§10.5)

YAML em `~/.config/deck-builder/brands.yaml`. 3 marcas pre-povoadas no install do plugin (Beauty Smile, Fotona, Carnaval 360). Ordem de deteccao:
1. Input do usuario (regex YAML)
2. CLAUDE.md ativo
3. Agente `culture-lab` carregado → Beauty Smile fallback
4. Skill `laser-physics` carregada → Fotona fallback
5. Nenhum match → "generico" + pergunta U6

## NBs

- **NB1 Core Transversal** (`7f1b2e2b-4ba4-40de-ba56-ca2f55e2c0da`) — Pitch Anything (Klaff), Made to Stick (Heath), Strategic Narrative (Raskin)
- **NB3 Comerciais** (`5a0aaabb-78c1-4d03-a400-e9ce1973737b`) — sales-decks-b2b-vendas-consultivas (91 sources), Challenger Sale (Dixon/Adamson), Gap Selling (Keenan), April Dunford (Sales Pitch), Win Without Pitching (Weinberg), Great Demo! (Cohan), Gong Labs 67k demos, padrao BR (Caetano, Romeo, Candeloro), healthcare/dental BR

## DoD especifico

- [ ] Frontmatter §10.7 com `intent: action`, `effort: high`, NB1 + NB3
- [ ] 3 eval cases passando (Fotona LightWalker dentista premium / Beauty Smile franchising / Carnaval 360 corporativo)
- [ ] 2 modos (`padrao` / `demo-presentation`)
- [ ] Insight provocador Challenger no slide 2 — NUNCA comeca com "obrigado pela reuniao"
- [ ] Comparativo responsavel sem badmouth (validado contra eval cases 1 e 2)
- [ ] ROI/payback explicito em TODOS os 3 cases (RNF compliance)
- [ ] Auto-detection §10.5 funcional (Fotona / Beauty Smile / Carnaval 360 reconhecidos)
- [ ] Schema §10.2 valido (cabecalho Meta + estrutura narrativa + slides + 3 tiers compliance)
- [ ] Instalada Code (`~/.claude/skills/deck-sales/`) + Cowork Desktop (`skills-plugin/.../skills/deck-sales/`)
- [ ] Testada com 1 caso real (nao-eval) — apos instalacao
