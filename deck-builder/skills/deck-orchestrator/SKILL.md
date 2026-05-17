---
name: deck-orchestrator
description: Entrypoint /deck do plugin deck-builder. Classifica vertical por keywords + auto-detection de marca, e delega a skill apropriada. Routing-first (D10), NUNCA auto-delega /idea-to-brief (D12).
intent: orchestration
effort: high
nb_ids:
  - 7f1b2e2b-4ba4-40de-ba56-ca2f55e2c0da
references:
  - references/routing-matrix.md
  - references/handoff-context.md
  - references/ask-user-templates.md
  - references/eval-cases-orchestrator.md
assets:
  - evals/orchestrator-cases.md
---

# deck-orchestrator

Entrypoint do plugin `deck-builder`. Recebe input livre, classifica vertical, delega a skill especialista. NAO gera STORYBOARD. NAO faz entrevista universal U1-U6 (verticais fazem).

> **Routing-first (D10).** 90% dos casos tem keywords obvias — roteia DIRETO sem entrevista. So pergunta quando ambiguo (2+ rotas empatadas) ou vago (0-1 keyword).
>
> **NUNCA auto-delega `/idea-to-brief` (D12).** Sempre pergunta via AskUserQuestion antes.

## Quando ativa

- `/deck {input livre}` (gatilho principal)
- "preciso fazer um deck", "preciso de slides"
- "vou apresentar", "preparar apresentacao"
- "tenho que pitchar", "monta uma deck"

## Fronteiras (LOCKED — SHARED.md §10.8)

- NAO gera STORYBOARD diretamente — sempre delega
- NAO faz entrevista universal U1-U6 (vertical destino faz)
- NAO escolhe vertical "no chute" em caso de ambiguidade — pergunta
- NAO auto-delega `/idea-to-brief` (D12) — sempre AskUserQuestion antes
- NAO chama APIs pagas
- NAO gera slides finais (PPTX/Gamma/Figma)

## Fluxo (1-pass)

```
1. Carrega routing matrix (references/routing-matrix.md)
2. Roda auto-detection de marca §10.5 (5 niveis precedencia)
3. Conta keywords do input contra matriz
4. Aplica algoritmo D10 (abaixo)
5. Delega + passa handoff context (references/handoff-context.md)
```

## Algoritmo de routing (D10 — routing-first)

| Situacao | Acao |
|---------:|------|
| **2+ keywords mesma rota** | Roteia DIRETO sem perguntar U1-U3 (vertical pergunta U1-U6 depois) |
| **2+ keywords de 2+ rotas distintas** | AskUserQuestion "É mais [A] ou [B]?" (template T1) |
| **0-1 keyword + sem contexto** | AskUserQuestion U1-U3 (template T2); re-classifica |
| **Apos U1 ainda vago** | AskUserQuestion sugere `/idea-to-brief` (template T3 — D12) |
| **Sinal `concept-reveal`** | Roteia `deck-internal` modo `concept-reveal` + sinaliza pipeline cenografia (template T4 — D3) |
| **Sinal delegacao externa** | `/copy` (carrossel/Instagram/reel/post) / agente `culture-lab` (cultura BS) / `skill-cenografia` (render/booth/camarote) — mensagem clara "isso NAO e deck" |

> Detalhe completo da matriz em [references/routing-matrix.md](references/routing-matrix.md) — espelha SHARED.md §10.3 (fonte canonica).

## Auto-detection de marca (§10.5 — 5 niveis precedencia, primeiro match vence)

```
1. Input do usuario → regex de ~/.config/deck-builder/brands.yaml
2. CLAUDE.md ativo (working dir)  → mencao explicita de marca
3. Agente `culture-lab` carregado → Beauty Smile (fallback)
4. Skill `laser-physics` carregada → Fotona (fallback)
5. Nenhum match → marca = "generico" (vertical pergunta U6)
```

**Acoes ao detectar:**
- Se `design_system_skill` no YAML existe e instalado → carrega tokens (ex: `beauty-smile-design-system`)
- Compliance tags injetadas no handoff context (ex: `anvisa-laser-classe-iii` para Fotona)

**brands.yaml default (3 marcas pre-povoadas):**
- **Beauty Smile** — regex `\bBeauty Smile\b|beautysmile` → design system `beauty-smile-design-system`, tags `odontologia-br,cfo-cfm`
- **Fotona** — regex `\bFotona\b|LightWalker|Er:YAG|Nd:YAG` → tags `anvisa-laser-classe-iii,cfo-laser`
- **Carnaval 360** — regex `\bCarnaval 360\b|carnaval360` → sem design system, sem tags

## Handoff context (passa para vertical)

Quando delega, monta este pacote (detalhes em [references/handoff-context.md](references/handoff-context.md)):

```yaml
handoff:
  input_original: "{string do usuario}"
  vertical_destino: "deck-{vertical}"
  modo: "{se aplicavel — ex: concept-reveal, peer-facing}"
  respostas_pre_coletadas:   # so existe se input vago + perguntou U1-U3
    U1: "..."
    U2: "..."
    U3: "..."
  marca_detectada: "Beauty Smile" | "Fotona" | "Carnaval 360" | "generico"
  design_system_skill: "beauty-smile-design-system" | null
  compliance_tags: ["odontologia-br", "cfo-cfm"]
  keywords_matched: ["pitchar", "anjo", "R$500k"]
  rota_score: {fundraising: 3, sales: 0, ...}
```

A vertical destino assume daqui — faz a entrevista universal U1-U6 (ou completa as faltantes se ja tem), depois suas perguntas especificas, e gera STORYBOARD.

## Quando usar AskUserQuestion (4 templates fixos)

Templates verbatim em [references/ask-user-templates.md](references/ask-user-templates.md). Resumo:

| Template | Quando | Pergunta-chave |
|----------|--------|----------------|
| **T1 — Ambiguidade de rotas** | 2+ keywords de 2+ rotas distintas | "É mais [A] ou [B]?" |
| **T2 — Coletar U1-U3** | 0-1 keyword (input vago) | objetivo + audiencia + duracao |
| **T3 — Sugerir /idea-to-brief** | Apos U1 ainda vago | "Quer rodar /idea-to-brief antes?" |
| **T4 — Pipeline cenografia** | Detectou concept-reveal | Confirma se ja tem artefatos `skill-cenografia` |

**NUNCA tente gerar deck sem rotear.** Empate sempre vai para AskUserQuestion (NUNCA "vou no fundraising porque parece").

## Pipeline `skill-cenografia` → `deck-internal concept-reveal` (D3)

Quando detecta `concept reveal | ativacao | conceito sala/booth/camarote | apresentar conceito`:

1. Roteia `deck-internal` modo `concept-reveal`
2. **Sinaliza na mensagem ao usuario** (template T4):
   ```
   Detectei pipeline cenografia. Modo `concept-reveal` consome artefatos
   da `skill-cenografia` (renders, mood, layout, set design).
   
   Voce ja gerou esses artefatos?
   1. Sim, tenho os paths/JSONs → me passa
   2. Nao, ainda preciso gerar → rode `skill-cenografia` primeiro e me chame de volta
   3. Quero apresentar o conceito SEM os artefatos visuais ainda (mais arriscado)
   ```
3. Se usuario escolhe 2, orchestrator PAUSA e nao delega ate ter os artefatos

## Delegacoes externas (NAO sao decks)

Routing matrix inclui 3 rotas para fora do plugin:

| Sinal | Delegacao | Mensagem |
|-------|-----------|----------|
| carrossel / Instagram / reel / TikTok / post | `/copy` | "Isso nao e um deck — carrossel/post de redes sociais e da skill `/copy`. Delegando." |
| cultura / onboarding / valores Beauty Smile | agente `culture-lab` | "Material de cultura e do agente `culture-lab`. Delegando." |
| render / layout 3D / stand / booth / camarote / set design / mood board espaco | `skill-cenografia` | "Render/cenografia e da `skill-cenografia` (nao e deck). Delegando." |

> Quando detectado, orchestrator NAO entra em fluxo de routing — manda mensagem clara e ja delega.

## NBs a consultar

- **NB1 Core** (`7f1b2e2b-4ba4-40de-ba56-ca2f55e2c0da`) — apenas para tie-breakers em routing ambiguo (raro). Falha de NB nao bloqueia (degrada com warning).

## Output (verbal — NAO arquivo)

NAO gera STORYBOARD. NAO escreve em `$DECKS_DIR`. O output e a propria delegacao + mensagem clara ao usuario:

```
[Auto-detection: Beauty Smile (regex match no input)]
[Keywords: "pitchar"(1) + "anjo"(1) + "R$500k"(1) = 3 → fundraising]

Routing → `deck-fundraising`

Vou te passar para a skill `deck-fundraising`. Ela vai:
1. Fazer entrevista universal U1-U6 (rapido)
2. Perguntar F1-F5 especificas de captacao
3. Gerar STORYBOARD em $DECKS_DIR/{YYYY-MM}/STORYBOARD-{slug}-{HHmm}.md

Design system Beauty Smile carregado.
Compliance tags: odontologia-br, cfo-cfm
```

Depois invoca `deck-fundraising` com o handoff context completo.

## Eval cases (5 obrigatorios — orchestrator e critico para qualidade do plugin)

Detalhes em [references/eval-cases-orchestrator.md](references/eval-cases-orchestrator.md). Resumo:

1. **Routing direto (3+ keywords)** — `/deck Beauty Smile pra anjo R$500k` → `deck-fundraising` direto sem U1-U3
2. **Ambiguidade rotas (2+2)** — `/deck aula Er:YAG pra dentistas em curso` → AskUserQuestion T1
3. **Delegacao externa** — `/deck carrossel sobre tratamento` → `/copy`
4. **Input vago + sugestao idea-to-brief** — `/deck preciso de slides` → U1-U3, U1 vago → T3 (NAO auto-delega)
5. **Concept-reveal pipeline D3** — `/deck apresentar conceito sala VIP Carnaval 360 pro board` → `deck-internal` concept-reveal + T4

**Smoke test extra (pos-instalacao):** 1 caso com 3 rotas ambiguas (ex: `/deck pitch tecnico-comercial pra investidor em congresso clinico`) → T1 entre 3 rotas.

## DoD especifico (Bundle 11 §13.6)

- [x] Frontmatter §10.7 com `intent: orchestration`, `effort: high`, NB1
- [x] 5 eval cases definidos
- [x] Routing matrix §10.3 implementada (reference espelha SHARED.md)
- [x] Algoritmo D10 (routing-first)
- [x] NAO auto-delega `/idea-to-brief` (D12)
- [x] Delegacoes externas (`/copy`, `culture-lab`, `skill-cenografia`)
- [x] Pipeline cenografia D3 sinalizado
- [x] Handoff context completo
- [x] Em empate, AskUserQuestion (NUNCA chuta)
- [x] Auto-detection §10.5 (5 niveis precedencia)
- [x] 4 templates AskUserQuestion documentados
- [x] Smoke test 6 cases (5 base + 1 ambiguo 3-rotas)
- [x] Instalada Code + Cowork
