---
name: deck-fundraising
description: STORYBOARD para deck de captacao (anjo/VC/family office/Rouanet) em 3 modos (padrao/sponsorship/demo-day). Use ao mencionar pitch investidor, captacao, seed, Series A, patrocinio.
intent: action
effort: high
nb_ids:
  - 7f1b2e2b-4ba4-40de-ba56-ca2f55e2c0da  # NB1 Core (Resonate, Made to Stick, Pitch Anything, Storytelling with Data)
  - 5a0aaabb-78c1-4d03-a400-e9ce1973737b  # NB3 Comerciais (pitch-decks-captacao + Sequoia + Raskin + Klaff)
references:
  - references/framework-sequoia-raskin.md
  - references/framework-klaff-strong.md
  - references/compliance-forward-looking-statements.md
  - references/eval-cases-fundraising.md
assets:
  - assets/templates/storyboard-skeleton-sequoia.md
  - assets/templates/sponsorship-mode-skeleton.md
  - assets/checklists/fundraising-checklist.md
---

# deck-fundraising

Vertical 1/8 do plugin **deck-builder** (Onda 2). Skill para gerar STORYBOARD de pitch decks de captacao — investidor anjo, VC (pre-seed/seed/Series A+), family office, patrocinio cultural (Rouanet) e parceria comercial estrategica equivalente a sponsorship.

Aplica 3 frameworks combinados: **Sequoia Capital** (estrutura canonica 10 slides), **Andy Raskin Strategic Narrative** (Big Change → Promised Land → Magic Gift sobreposto a Sequoia) e **Klaff STRONG** opcional para investidor sofisticado (Setup → Tension → Reveal → Outcome → New Game + Frame Stacking).

## Quando ativa

**Modo encadeado (via deck-orchestrator):** quando matriz de roteamento §10.3 conta ≥2 keywords fundraising ("investidor", "VC", "anjo", "captacao", "seed", "Series A/B", "Rouanet", "patrocinio").

**Modo direto:** `/deck-fundraising` ou frases como "preciso de um pitch pra investidor anjo de R$500k", "deck Series A pra fundo de saude", "patrocinio Carnaval 360 master".

## Modos

| Modo | Quando aplica | Estrutura | Slides estimados |
|------|--------------|-----------|------------------|
| `padrao` (default) | Pitch a investidor anjo/VC/family office | Sequoia + Raskin | 12-15 |
| `sponsorship` | Patrocinio cultural/Rouanet, parceiros corporativos | Sequoia adaptado + bloco contrapartidas | 10 + 3-4 |
| `demo-day` | Pitch curto 3-5min (acelerador, batch graduation) | Sequoia destilado (so Problem/Solution/Traction/Ask) | 7-8 |

**Auto-deteccao do modo:**
- Sinal "Rouanet", "patrocinio cultural", "patrocinador master/gold/silver", "contrapartida", "cota" → `sponsorship`
- Sinal "demo day", "3 minutos", "5 minutos", "batch", "graduacao acelerador" → `demo-day`
- Default → `padrao`
- Usuario pode forcar via flag `--modo sponsorship` ou `--modo demo-day`

## Protocolo de execucao (8 passos)

### 1. Auto-detect marca (§10.5 SHARED.md)
Aplica regex YAML em `~/.config/deck-builder/brands.yaml` na ordem: input usuario → CLAUDE.md → agentes carregados → fallback "generico". Carrega `design_system_skill` se declarado e instalado (Beauty Smile → `beauty-smile-design-system`). Injeta `compliance_tags` (Fotona → `anvisa-laser-classe-iii`).

### 2. Entrevista universal U1-U6 (§10.1 SHARED.md)
Se `deck-orchestrator` ja roteou direto (≥2 keywords da mesma rota), confirma so o que faltar. Inferir o que puder de CLAUDE.md/contexto. **Output obrigatorio:** `objetivo`, `audiencia`, `duracao_min`, `formato`, `big_idea`, `marca` → cabecalho `## Meta`.

### 3. Entrevista vertical F1-F5

| # | Pergunta | Tipo | Default inferido |
|---|----------|------|------------------|
| F1 | Estagio: pre-seed / seed / Series A+ / patrocinio cultural / patrocinio corporativo | enum | inferir de U1/U6 |
| F2 | Ticket alvo: valor + moeda + equity (% se aplicavel) | texto | extrair de U1 |
| F3 | Tracao atual: MRR/receita/usuarios/clientes/NPS/eventos historicos | texto | — |
| F4 | Concorrente principal + diferencial defensavel (1 linha cada) | texto | — |
| F5 | 1 risco que o investidor vai levantar primeiro (antecipar = ouro) | texto | — |

**Regra:** se F1=patrocinio cultural/corporativo → modo `sponsorship` (skip F4 substituido por "patrocinadores anteriores se houver").

### 4. Selecionar framework principal
- `padrao` + investidor anjo first-time → **Sequoia + Raskin** (default 13 slides)
- `padrao` + VC institucional / family office sofisticado → **Sequoia + Raskin + Klaff STRONG** (3 frames de Klaff stackados, +1 slide reveal)
- `sponsorship` → **Sequoia adaptado** (substitui ultimos 3 slides por bloco contrapartida/ROI/niveis) + Raskin Big Idea como Promised Land do patrocinador
- `demo-day` → **Sequoia destilado** (Problem/Solution/Traction/Ask em 7-8 slides, Raskin Big Change colado no slide 2)

Detalhes em [references/framework-sequoia-raskin.md](references/framework-sequoia-raskin.md) e [references/framework-klaff-strong.md](references/framework-klaff-strong.md).

### 5. Consultar NBs (NB1 + NB3)
Query exemplo (executar em paralelo se ambiente suporta):
```bash
notebooklm use 7f1b2e2b-4ba4-40de-ba56-ca2f55e2c0da  # NB1 Core
notebooklm ask "Andy Raskin strategic narrative aplicado a {vertical do U2} + Big Idea = {U5}" --max-citations 5

notebooklm use 5a0aaabb-78c1-4d03-a400-e9ce1973737b  # NB3 Comerciais
notebooklm ask "Sequoia pitch deck {estagio F1} {ticker F2} + diferencial defensavel vs {F4}" --max-citations 5
```
**Cite ate 3 hits maximos por skill. Falha NB nao bloqueia — degrada com warning `<!-- NB indisponivel; defaults da pesquisa aplicados -->`.**

### 6. Gerar STORYBOARD seguindo schema §10.2

**Action titles, NUNCA titulos descritivos.** Cada slide tem:
- `Tipo:` (capa | problema | contexto | conceitual | dados | comparativo | prova-social | equipe | demo | financeiro | CTA | disclaimer | agradecimento | apendice)
- `Action title:` (headline assertivo de 5-9 palavras)
- `Mensagem-chave:` (1 frase)
- `Speaker notes:` (2-3 paragrafos)
- `Visual:` (descricao neutra)
- `Prompt de imagem:` (preencher SE tipo na whitelist D5; senao gravar `—`)
- `Tempo estimado:` (segundos)
- `Objecao esperada:` (se aplicavel — usar F5)

**Regras especificas do fundraising:**
- Big Idea (U5) entra como **Promised Land do Raskin no slide 4 (Why Now)**, NAO como titulo do deck
- Slide 2 (Problema) usa **Loss Aversion do Raskin** ("X% das empresas/clinicas/eventos desapareceram em Y anos") quando dado disponivel
- Slide Tracao (F3) sempre vem ANTES do slide Equipe (DocSend 2024: time slide e o mais lido — 1min02s — entao deixa ele perto do final pra fechar com forca)
- Slide Ask (penultimo ou ultimo) tem **3 partes obrigatorias** (`NUNCA vago`):
  - **Valor + estrutura:** "R$500k em SAFE 8% equity post-money cap R$6M" (NAO so "R$500k")
  - **Uso de capital:** alocacao explicita em 3-4 buckets com %  (ex: "Produto 40% / GTM 35% / G&A 25%")
  - **Timeline + milestone:** "12 meses ate atingir R$400k MRR e destravar Series A"

### 7. Invocar `deck-image-prompts` para slides whitelist (D5)

**Whitelist preencher:** capa | problema | conceitual | comparativo | demo | prova-social | equipe (equipe = variante prova-social com retrato profissional)

**Skip default:** dados | financeiro | CTA | disclaimer | agradecimento | apendice

**Override:** se usuario passa `--include-dados` ou grafico do TAM/SAM/SOM e o hero visual do deck, sair do skip para `dados`. Default para fundraising: skip dados (financeiros sao numeros em texto, nao precisam visual gerado).

Passar para `deck-image-prompts` lista de slides whitelist com `{tipo, action_title, mensagem_chave, visual_brief, big_idea, marca}`. Skill auxiliar devolve bloco pronto pra colar.

### 8. Aplicar compliance (forward-looking statements + tier de issues)

**Disclaimer automatico se numeros projetados presentes** (MRR projetado, Series A timeline, ROI patrocinador) — ver [references/compliance-forward-looking-statements.md](references/compliance-forward-looking-statements.md). Disclaimer canonico vai como **slide separado** (tipo `disclaimer`) antes do agradecimento + rodape em todos os slides financeiros.

**Tier de issues (`Compliance & Disclaimers` no STORYBOARD):**
- 🔴 BLOQUEANTE — promessa de retorno garantido, confidencialidade sem NDA mencionado, oferta publica disfarcada (Res. CVM 160/22)
- 🟡 VERIFICAR — projecao sem premissa explicita, TAM top-down sem fundamentacao, claim regulatorio sem citacao
- ✅ OK — disclaimer canonico presente, ask especifico, diferencial defensavel

## Estrutura do STORYBOARD modo `padrao` (13 slides Sequoia + Raskin)

| # | Tipo | Action title exemplo | Raskin layer |
|---|------|---------------------|--------------|
| 1 | capa | "{Big Idea em 1 frase}" | hook |
| 2 | problema | "{Loss aversion / status quo dor}" | 1. Big Change in the world |
| 3 | comparativo | "Mundo velho vs mundo novo" | 2. Winners & Losers |
| 4 | conceitual | "{Promised Land — derivado de U5}" | 3. Promised Land |
| 5 | demo | "Como chegamos la — solucao" | 4. Magic Gift (features) |
| 6 | dados | "Por que agora (timing + tailwinds)" | Sequoia "Why Now" |
| 7 | dados | "Mercado TAM/SAM/SOM bottom-up" | Sequoia "Market" |
| 8 | financeiro | "Unit economics + business model" | Sequoia "Business Model" |
| 9 | prova-social | "Tracao: {numero F3 destacado}" | 5. Evidence |
| 10 | dados | "Roadmap 12-24 meses" | Sequoia "Financials" |
| 11 | equipe | "Por que ESSE time" | Sequoia "Team" |
| 12 | CTA | "Ask: {valor + uso + timeline}" | Sequoia "The Ask" |
| 13 | disclaimer | "Forward-looking statements" | Compliance |

**Apendice opcional:** competitive landscape detalhado, financial model completo, cap table, customer cases extras.

## Estrutura modo `sponsorship` (10 + bloco 3-4 slides)

Substitui slides 8-10-12 (Business Model / Financials / Ask) por bloco contrapartida:

| # | Tipo | Action title |
|---|------|--------------|
| 1-7 | (mesmos do padrao adaptados) | Big Idea = visao do EVENTO/MARCA, nao do produto |
| 8 | comparativo | "Niveis de patrocinio: bronze / silver / gold / master" |
| 9 | conceitual | "Contrapartidas master: visibilidade + branding + ativacao" |
| 10 | dados | "ROI patrocinador: alcance demografico + conversao indireta" |
| 11 | CTA | "Investimento master: R${F2} + Lei Rouanet aplicavel" |
| 12 | disclaimer | "PRONAC + forward-looking" |

**Para sponsorship cultural** sempre incluir:
- Numero PRONAC (se aprovado) ou status MinC
- Mecanismo Lei 8.313/91 + lei estadual/municipal aplicavel
- Disclaimer "Captacao sujeita a homologacao MinC"

## Estrutura modo `demo-day` (7-8 slides em 3-5 min)

| # | Tipo | Action title | Tempo |
|---|------|--------------|-------|
| 1 | capa | "{Big Idea}" | 15s |
| 2 | problema | "{status quo + Big Change colado}" | 30-40s |
| 3 | demo | "Solucao em 1 frase + 1 visual" | 30s |
| 4 | prova-social | "Tracao: {numero F3 grandao}" | 40s |
| 5 | dados | "Mercado + Why Now" | 30s |
| 6 | equipe | "Time em 3 bullets" | 30s |
| 7 | CTA | "Ask: {valor + uso + timeline}" | 30s |
| 8 (opt) | disclaimer | Forward-looking | rodape |

**Demo-day regra:** corta tudo que nao caiba em 3-5min. Big Idea aparece como slide 1 (capa) E como ultima frase do CTA — sandwich.

## Output convention

Path default: `$DECKS_DIR/{YYYY-MM}/STORYBOARD-{slug-big-idea-ou-cliente}-{HHmm}.md` (§10.4).

Slug max 30 chars kebab-case derivado do Big Idea (U5) ou nome cliente.

Anexos:
- Imagens (apos `deck-image-prompts`): `$DECKS_DIR/{YYYY-MM}/img/{slug}/slide-N.png`
- Review (apos `deck-reviewer`): `STORYBOARD-{slug}-{HHmm}.review.md` paralelo

## Guardrails

### Big Idea como Promised Land
Big Idea (U5) NAO vai no titulo do deck. Vai no slide 4 (Why Now / Promised Land) como frase aspiracional. Slide 1 (capa) usa derivacao curta ou nome da empresa + tagline. **Falha de Big Idea bloqueia:** se U5 esta vago ("ser a melhor X"), pedir refinamento — Big Idea precisa ser **especifica + improvavel sem voce + concreta**.

### Ask sempre tripartido
Slide CTA NUNCA pode ter so o valor. Tem que ter **valor + uso + timeline com milestone**. Se F2 nao especifica uso de capital, perguntar explicitamente antes de gerar slide. Default sugerido (Kupor/a16z): Produto 40% / GTM 35% / G&A 25% — mas confirmar com usuario.

### TAM bottom-up obrigatorio
Slide 7 (Mercado) NUNCA usa "1% de R$1tri" top-down. Sempre bottom-up: "X clinicas-alvo × Y% conversao × R$Z ticket medio = R$N TAM". Se usuario nao tem dados bottom-up, perguntar e ajudar a derivar.

### Anti-padroes fatais (rejeicao imediata)
- "Nao temos concorrentes" + slide tipo magic quadrant onde startup esta no #1
- Slide de exit no seed (Hunter Walk red flag)
- Vanity metrics (downloads, pageviews) sem MRR/receita
- Hockey stick sem mecanismo explicado
- Team slide currículo-only sem responder "por que ESSE time"

Detalhe completo em [references/framework-sequoia-raskin.md](references/framework-sequoia-raskin.md).

### Forward-looking statements
**Disparo automatico** se qualquer slide contem: projecao MRR/receita futura, ROI patrocinador estimado, timeline pra Series A/proxima rodada, qualquer numero futuro nao auditado. Disclaimer vai como slide separado + rodape. Texto canonico em [references/compliance-forward-looking-statements.md](references/compliance-forward-looking-statements.md).

### Brand compliance (auto-detect §10.5)
- Beauty Smile → carrega `beauty-smile-design-system` se instalado + compliance `odontologia-br`, `cfo-cfm` (slides com claim clinico tem footnote)
- Fotona → carrega compliance `anvisa-laser-classe-iii`, `cfo-laser` (slide produto tem footnote Anvisa Classe III + nome do responsavel tecnico)
- Carnaval 360 → sem design system declarado; aplica defaults editoriais

### Falha graceful
- NB indisponivel → segue com defaults da pesquisa + warning
- `design_system_skill` nao instalado → segue sem tokens + warning
- `deck-image-prompts` nao disponivel → grava placeholder `**Prompt de imagem:** [a definir — deck-image-prompts nao instalado]` nos slides whitelist
- Big Idea (U5) ausente → bloqueia geracao ate refinar com usuario

## Fronteiras (§10.8)

- NAO gera slides finais sem pedido explicito (D15) — default e STORYBOARD.md. Render e exclusividade de `deck-render-canva`, opt-in e so com MCP do Canva conectado. PPTX/Google Slides/Figma/Gamma seguem proibidos.
- NAO busca dados de mercado em tempo real — usuario fornece
- NAO faz design visual — `deck-image-prompts` gera prompts, designer/IA renderiza
- NAO chama APIs pagas sem confirmacao
- NAO escreve post de redes sociais sobre o pitch — delega `/copy`
- NAO projeta espaco/cenografia (D3) — delega `skill-cenografia`
- NAO substitui assessoria juridica/CVM — disclaimer e padrao, mas due diligence e do usuario

## Handoff: render no Canva (v2.0.0 — opt-in, D16)

Ao entregar o `STORYBOARD.md`, **se e somente se** o MCP do Canva estiver conectado, ofereca via `AskUserQuestion`:

> "Gero a base deste deck no Canva a partir do storyboard?"
> - Sim → `deck-render-canva`
> - Nao → encerra normalmente

Invioláveis:
- **Nunca** chama `deck-render-canva` automaticamente (D16).
- MCP do Canva desconectado → **nao oferece**. Sem aviso e sem opcao quebrada (D15).
- Recusa encerra o fluxo normalmente — nao insiste, nao repergunta.
- Sem brand template para a marca, o render reporta e pula. Nunca cai para geracao livre (D19).

## Eval cases

3 cases obrigatorios em [references/eval-cases-fundraising.md](references/eval-cases-fundraising.md):
1. **Beauty Smile** pitch anjo R$500k 8% — modo `padrao` 13 slides Sequoia + Raskin
2. **Carnaval 360** patrocinio master R$2M — modo `sponsorship` 10+4 slides
3. **Fotona** distribuidor exclusivo BR R$5M — modo `padrao` 14 slides + compliance Anvisa Classe III

Asserts em [evals/evals.json](evals/evals.json).

## Templates

- [assets/templates/storyboard-skeleton-sequoia.md](assets/templates/storyboard-skeleton-sequoia.md) — skeleton 13 slides padrao
- [assets/templates/sponsorship-mode-skeleton.md](assets/templates/sponsorship-mode-skeleton.md) — skeleton sponsorship 10+4
- [assets/checklists/fundraising-checklist.md](assets/checklists/fundraising-checklist.md) — checklist pre-apresentacao

## Referencias

- [references/framework-sequoia-raskin.md](references/framework-sequoia-raskin.md) — Sequoia 10 slides + Raskin 5 passos + mapeamento + anti-padroes
- [references/framework-klaff-strong.md](references/framework-klaff-strong.md) — STRONG + Frame Stacking + boas praticas BR
- [references/compliance-forward-looking-statements.md](references/compliance-forward-looking-statements.md) — disclaimer canonico CVM + SEC + Rouanet
- [references/eval-cases-fundraising.md](references/eval-cases-fundraising.md) — 3 cases detalhados com inputs + outputs esperados

## Definition of Done

- [ ] Frontmatter §10.7 com `intent: action`, `effort: high`, NB1 + NB3
- [ ] 3 eval cases passando (Beauty Smile / Carnaval 360 / Fotona)
- [ ] 3 modos implementados (padrao / sponsorship / demo-day)
- [ ] Disclaimer forward-looking statements automatico se numeros projetados
- [ ] Big Idea (U5) usada como Promised Land Raskin no slide 4 (Why Now)
- [ ] Slide Ask tripartido: valor + uso de capital + timeline (NUNCA vago)
- [ ] Auto-detection §10.5 funciona com Beauty Smile/Fotona/Carnaval 360
- [ ] Invoca `deck-image-prompts` para slides whitelist (capa/problema/conceitual/comparativo/demo/prova-social/equipe)
- [ ] STORYBOARD bate com schema §10.2 (lint via `deck-reviewer`)
- [ ] Instalada em `~/.claude/skills/deck-fundraising/` + Cowork Desktop skills-plugin

## v1.1 — Adendo: `modo_entrega` + `[VERIFICAR]` + Layout sugerido

A partir de v1.1 do plugin, esta skill aplica 4 disciplinas adicionais ao gerar STORYBOARD. Detalhes canônicos em `../../shared/storyboard-schema.md` e `../../shared/verificar-flag.md`.

**1. `modo_entrega` adapta densidade do slide** (regra 7 do schema):
- `apresentado-ao-vivo` (U4=1/2): slides minimalistas (2-3 bullets) + speaker notes RICOS
- `enviado-para-leitura` (U4=3): slides DENSOS (4-6 bullets + dados inline + 1 quote curto) + speaker notes opcionais ou curtos
- `hibrido` (U4=4): meio-termo, ambos preenchidos

Preencher bloco `Conteúdo do slide (visível na projeção)` em cada slide, calibrado ao `modo_entrega`.

**2. `Layout sugerido` em cada slide** (regra 8 do schema): grid + tipografia + componentes visuais + animação. Sem isso, designer/Gamma/Claude Design/PowerPoint recebe o deck "no escuro".

**3. `[VERIFICAR]` em dados fabricados** (regra 9 do schema + `verificar-flag.md`): todo R$/%/n=/RCT/NPS/GRADE/CFO/Anvisa que a skill **inferir** (não veio do usuário; não é público canonicamente conhecido) recebe `[VERIFICAR: descrição]` inline ou em footnote. Lint v1.1 emite WARN quando ausente. Reviewer converte em 🟡 ou 🔴 no segundo passe.

**4. Bold opcional nos rótulos:** preferir `**Tipo:**`, `**Action title:**`, `**Mensagem-chave:**` para facilitar leitura visual. Lint aceita ambos formatos.

**Checklist v1.1 ao gerar cada slide:**
- [ ] `**Tipo:**`, `**Action title:**`, `**Mensagem-chave:**` em bold
- [ ] Bloco `Conteúdo do slide (visível na projeção)` preenchido com densidade adaptada ao `modo_entrega`
- [ ] Bloco `Layout sugerido` com grid + tipografia + componentes
- [ ] Dados específicos inferidos marcados com `[VERIFICAR: ...]`
- [ ] `Imagens sugeridas` no formato v1.1 (Quantidade explícita + variações em blocos separados)
