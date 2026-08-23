---
name: deck-equipment
description: Cria STORYBOARD para vender equipamentos medicos/dentais. Auto-detecta Fotona/LightWalker/Er:YAG/Nd:YAG. Aplica FAB + TCO 5 anos + Payback + Sensitivity 3 cenarios. Compliance Anvisa Classe II/III.
intent: action
effort: high
nb_ids:
  - 7f1b2e2b-4ba4-40de-ba56-ca2f55e2c0da  # NB1 Core Transversal
  - 1635d16b-773c-480d-89c2-79c717f4b2e1  # NB2 Verticais Densas
references:
  - references/framework-fab-tco-payback.md
  - references/compliance-anvisa-equipment.md
  - references/eval-cases-equipment.md
assets:
  - assets/templates/storyboard-skeleton-equipment.md
  - assets/checklists/equipment-compliance.md
---

# deck-equipment

Skill vertical do plugin **deck-builder** (Onda 2, 4/8). Gera STORYBOARD para apresentar/vender equipamento medico ou dental para clinica/hospital/consultorio.

Aplica 4 frameworks combinados em todo output: **FAB** (Features-Advantages-Benefits) + **TCO 5 anos** + **Payback analysis** + **Sensitivity 3 cenarios** (otimista/realista/pessimista). Detalhamento dos frameworks em [references/framework-fab-tco-payback.md](references/framework-fab-tco-payback.md).

## Quando ativa

**Auto-rota do `deck-orchestrator`** (§10.3) ao detectar 2+ keywords:
- equipamento, device, laser, scanner, ROI clinica, payback, TCO, "vender [marca]"
- nomes proprios: Fotona, LightWalker, Lumenis, BTL, Megagen, Straumann, Neodent, 3Shape, Trios, iTero

**Standalone:** `/deck-equipment` ou frases como "preciso pitchar LightWalker pra clinica", "ROI do scanner Trios", "comparar Fotona vs Lumenis".

## Auto-detection Fotona (D6)

Regex em `~/.config/deck-builder/brands.yaml`: `\bFotona\b|LightWalker|Er:YAG|Nd:YAG`.

Ao match:
- Injeta `compliance_tags: ["anvisa-laser-classe-iii", "cfo-laser"]` no contexto
- Carrega skill `laser-physics` (se instalada) para citacoes de dosimetria
- Slide 14 (compliance) DEVE listar registro Anvisa Classe III explicitamente

Outras marcas detectadas seguem o mesmo padrao com a Classe correspondente. Se equipamento nao tem marca pre-registrada, perguntar Classe Anvisa em E1.

## Modos

| Modo | Quando aplica | Diferenca estrutural |
|------|---------------|----------------------|
| `padrao` (default) | Pitch unico de equipamento | Bloco comparativo (slide 8) e leve: 1-2 alternativas mencionadas com respeito |
| `comparativo` | Cliente avaliando 2-3 marcas simultaneamente | Bloco comparativo (slides 8a-8c) detalhado: tabela lado-a-lado forcas+limites por marca, ainda SEM badmouth |

**Como escolher:** se U1/E5 mencionam 2+ marcas que cliente esta comparando → modo `comparativo`. Senao → `padrao`.

## Entrevista vertical (apos U1-U6 da §10.1)

| # | Pergunta | Tipo |
|---|----------|------|
| E1 | Equipamento especifico + Classe Anvisa (I/II/III) + numero de registro se conhecido | texto |
| E2 | Cliente alvo: clinica boutique / clinica multi-cadeira / hospital / consultorio solo | escolha |
| E3 | Preco aquisicao + condicoes financiamento disponiveis (a vista / parcelado / leasing) | texto |
| E4 | Volume de pacientes/procedimentos por mes para payback alvo | numero + prazo |
| E5 | Concorrente(s) principal(is) que cliente considera | texto (multi) |

**Inferencias:**
- E1 sem numero de registro → marcar 🟡 verificar (compliance), NAO bloqueante na sessao de criacao
- E5 vazio → modo `padrao` (sem bloco comparativo detalhado)
- E5 com 2+ marcas → sugerir modo `comparativo`

## Frameworks aplicados (TODOS os outputs `padrao`)

Detalhe completo em [references/framework-fab-tco-payback.md](references/framework-fab-tco-payback.md). Sintese:

### FAB (slides 5-7)
Para cada caracteristica tecnica relevante: **Feature** (o que e) → **Advantage** (por que diferenciado vs alternativas) → **Benefit** (resultado clinico + impacto economico).

Maximo 3-4 features por deck. Mais que isso dilui mensagem.

### TCO 5 anos (slide 10)
Tabela com 5 linhas (Ano 1-5) e 5 colunas:
- Aquisicao (Ano 1; juros financeiro se parcelado distribuido)
- Consumiveis (pecas de mao, fibras, brocas, descartaveis)
- Manutencao (preventiva contratual + corretiva esperada)
- Treinamento (inicial Ano 1 + reciclagens)
- Total ano + acumulado

### Payback (slide 11)
- Margem por procedimento (preco cobrado - custo variavel - depreciacao por procedimento)
- Procedimentos/mes necessarios para zerar investimento no prazo alvo
- Comparar com volume realista da clinica (E2 + E4)
- Output: "X meses no cenario realista"

### Sensitivity 3 cenarios (slide 12)
Tabela com 3 colunas (Otimista / Realista / Pessimista) e linhas:
- Volume/mes
- Preco medio cobrado
- Margem por procedimento
- Payback (meses)
- ROI 5 anos

**Pessimista DEVE defender que mesmo no pior caso o investimento ainda paga** — se nao paga, ou o equipamento esta superdimensionado ou o cliente nao e perfil, e a skill recomenda revisitar E2/E4.

## Output STORYBOARD

Schema §10.2. Path default `$DECKS_DIR/{YYYY-MM}/STORYBOARD-{slug}-{HHmm}.md`. Esqueleto completo em [assets/templates/storyboard-skeleton-equipment.md](assets/templates/storyboard-skeleton-equipment.md).

**Estrutura 16-20 slides:**

| # | Tipo | Conteudo |
|---|------|----------|
| 1 | capa | Action title vendendo o desfecho (NAO "Apresentacao LightWalker") |
| 2 | problema | Problema clinico que o equipamento resolve |
| 3 | conceitual | Tecnologia + mecanismo de acao (esquema) |
| 4 | demo | Demo procedural (video curto, foto, ou simulacao com TCLE) |
| 5-7 | conceitual | FAB em 3 features-chave (1 feature por slide) |
| 8 | comparativo | Comparativo responsavel (1 slide modo `padrao`; 8a-8c modo `comparativo`) |
| 9 | prova-social | Caso clinico real (TCLE se imagem de paciente) |
| 10 | financeiro | TCO 5 anos |
| 11 | financeiro | Payback analysis |
| 12 | financeiro | Sensitivity 3 cenarios |
| 13 | conceitual | Treinamento + suporte tecnico |
| 14 | disclaimer | Compliance Anvisa Classe + registro |
| 15 | financeiro | Condicoes comerciais + financiamento |
| 16 | apendice | Especificacoes tecnicas detalhadas |
| 17-18 | CTA | CTA + proximos passos (1 ask claro) |

`max_ctas: 1` (default global). Se modo `comparativo`, expandir slide 8 em 8a (forcas tabelas), 8b (limites), 8c (criterio de escolha em uma frase neutra) — total cresce para 18-20 slides.

**Whitelist `deck-image-prompts` (D5):** capa, problema, conceitual, comparativo, demo, prova-social. Skip: dados, financeiro, CTA, disclaimer, agradecimento, apendice. Override `--include-dados` se o grafico de Payback ou Sensitivity for chave visual.

## Compliance Anvisa (3 tiers — D7)

Regras completas em [references/compliance-anvisa-equipment.md](references/compliance-anvisa-equipment.md) e checklist em [assets/checklists/equipment-compliance.md](assets/checklists/equipment-compliance.md). Sintese:

### 🔴 BLOCKER (resolver antes de apresentar)
- Equipamento mencionado SEM numero de registro Anvisa correspondente
- Claim fora de bula sem disclaimer "off-label" explicito
- Comparativo com badmouth (denegrir concorrente — risco juridico real conforme Codigo de Etica Publicitaria + CFM Resolucao 1.974/2011)

### 🟡 VERIFICAR
- Classe III declarada explicitamente para laser (CFO Resolucao 35/2018 exige curso de habilitacao)
- Conflito de interesse declarado (apresentador e distribuidor/representante/recebe comissao?)
- Imagens de paciente real com TCLE arquivado

### ✅ OK
- Registro Anvisa citado (formato `xxxxxxx-x` ou `MS xxxxxxx`)
- COI declarado em slide proprio ou rodape
- Comparativo responsavel (citar forcas e limites de cada device com respeito)

## Comparativo responsavel (regra anti-badmouth)

Risco juridico real: badmouth pode gerar acao por concorrencia desleal (Lei 9.279/96 art. 195) + denuncia CONAR + sancao CFM/CFO. **NUNCA** fazer.

**Estrutura obrigatoria do bloco comparativo (slide 8 ou 8a-c):**

1. Citar concorrente pelo nome com respeito ("Lumenis LightSheer e uma referencia consolidada em fotodepilacao desde 2003...")
2. Listar 2-3 forcas reconhecidas da alternativa
3. Listar 2-3 limites com fonte (bula, paper, benchmark independente — NUNCA achismo)
4. Posicionar nosso equipamento como **complementar ou superior em criterio especifico** (nao geral)
5. Fechar com "o melhor equipamento depende de [criterio do cliente: volume, mix de procedimentos, orcamento]"

**Frases proibidas:** "concorrente X e inferior", "marca Y nao funciona", "tecnologia Z e ultrapassada", qualquer adjetivo pejorativo.

**Frase modelo:** "Tanto o LightWalker quanto o LightSheer atendem fotodepilacao. O LightWalker se diferencia por integrar Er:YAG + Nd:YAG no mesmo chassi, eliminando necessidade de segundo equipamento para indicacoes periodontais. O LightSheer e mais especializado em fotodepilacao isolada e tem custo de aquisicao menor."

## Protocolo de execucao

1. **Auto-detect marca** (D6): regex contra `brands.yaml` no input + CLAUDE.md ativo
2. **Routing-first** (D10): se 2+ keywords da rota equipment, **NAO pergunta U1-U3** — entra direto
3. **Entrevista universal** U1-U6 (se necessaria) → entrevista vertical E1-E5
4. **Decide modo** (padrao vs comparativo) a partir de E5
5. **Consulta NB1 + NB2** via subcomando `notebooklm ask` (§10.6) — falha de NB nao bloqueia
6. **Aplica os 4 frameworks** preenchendo skeleton de [assets/templates/storyboard-skeleton-equipment.md](assets/templates/storyboard-skeleton-equipment.md)
7. **Roda checklist** [assets/checklists/equipment-compliance.md](assets/checklists/equipment-compliance.md) e classifica em 3 tiers
8. **Invoca `deck-image-prompts`** com lista de slides da whitelist + brief + Big Idea
9. **Escreve STORYBOARD** no path da §10.4 com header completo §10.2
10. **Sugere** `/deck review` se algum 🔴 ou 🟡 detectado

## Walkthrough (canonico — Case 1 dos evals)

**Input:** `/deck Smile Premium SP avaliando comprar Fotona LightWalker AT S, R$280k, payback 18m, comparar com Lumenis`

1. `deck-orchestrator` conta keywords: `Fotona` + `LightWalker` + `comprar` + `Lumenis` + `payback` → 5 hits rota equipment → entra direto
2. Auto-detect Fotona → carrega `anvisa-laser-classe-iii` + `cfo-laser` + tenta carregar `laser-physics`
3. U1-U6 (rapido, infere muito do input): U1 "Smile Premium aprova compra LightWalker em 60d", U5 "Dual Er:YAG + Nd:YAG paga em 18m sem dobrar equipamento", U6 Fotona
4. E1-E5: E1 LightWalker AT S Classe III, E2 boutique 4 cadeiras, E3 R$280k a vista / R$320k 36x, E4 18 laser/mes, E5 Lumenis LightSheer → **modo `padrao`** (1 alternativa unica, nao 2+)
5. NB1 ask "venda equipamento laser dental Brasil 2026" + NB2 ask "Fotona LightWalker FAB Er:YAG Nd:YAG payback"
6. Storyboard 18 slides: FAB Er:YAG (slide 5), FAB Nd:YAG (6), FAB integracao dual (7), comparativo respeitoso Lumenis (8), TCO 5 anos (10), Payback 18m realista (11), Sensitivity 9m/18m/30m (12), compliance Anvisa Classe III com numero de registro do AT S (14)
7. Checklist: 🟡 verificar numero registro (se nao conhecido); 🟡 TCLE caso clinico; ✅ comparativo respeitoso
8. `deck-image-prompts` para slides 1, 2, 3, 4, 7, 8, 9 (skip 5, 6 — sao tabelas FAB textuais)
9. Output: `$DECKS_DIR/2026-05/STORYBOARD-smile-premium-lightwalker-1430.md`

## Fronteiras (§10.8)

- NAO gera slides finais sem pedido explicito (D15) — default e STORYBOARD.md. Render e exclusividade de `deck-render-canva`, opt-in e so com MCP do Canva conectado. PPTX/Google Slides/Figma/Gamma seguem proibidos.
- NAO faz design visual — `deck-image-prompts` faz prompts
- NAO inventa preco, registro Anvisa, ou claim clinico — usuario fornece ou skill marca 🟡
- NAO faz comparativo badmouth — risco juridico
- NAO recomenda compra/nao-compra autonomamente — entrega ferramenta para o decisor

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

## Cross-references

- Plugin host: `deck-builder` (Onda 1+2)
- Contratos compartilhados: `SHARED.md` §10
- Auxiliares encadeadas: `deck-image-prompts`, `deck-reviewer` (opt-in)
- Fontes para FAB tecnico em laser: skill `laser-physics` (se Fotona/laser detectado)
- Output convention: `SHARED.md` §10.4

## DoD

- [ ] Frontmatter §10.7 com `intent: action`, `effort: high`, NB1+NB2
- [ ] 3 eval cases passando ([references/eval-cases-equipment.md](references/eval-cases-equipment.md))
- [ ] 2 modos (padrao/comparativo) com gatilho claro
- [ ] FAB + TCO 5 anos + Payback + Sensitivity 3 cenarios em TODOS outputs padrao
- [ ] Comparativo responsavel SEM badmouth — frases proibidas listadas
- [ ] Compliance Anvisa Classe declarada + numero registro
- [ ] Auto-detection Fotona injeta `anvisa-laser-classe-iii`
- [ ] Schema §10.2 valido
- [ ] Instalada Claude Code + Cowork Desktop (D13 — deck NAO e hm-*)

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
