# AskUserQuestion Templates — `deck-orchestrator`

> 4 templates fixos. SEMPRE invocar via tool `AskUserQuestion` (nunca tentar gerar deck sem rotear).

---

## T1 — Ambiguidade de rotas (2+ keywords de 2+ rotas distintas)

**Quando:** `top[0].score == top[1].score` e `top[0].score >= 1`.

### T1.a — 2 rotas empatadas

```python
AskUserQuestion(
  questions=[{
    "question": "Detectei sinais de duas verticais possiveis. Qual descreve melhor seu objetivo?",
    "header": "Rota deck",
    "multiSelect": False,
    "options": [
      {
        "label": "{Rota A — descricao curta}",
        "description": "{1 linha do que essa vertical entrega}"
      },
      {
        "label": "{Rota B — descricao curta}",
        "description": "{1 linha do que essa vertical entrega}"
      }
    ]
  }]
)
```

**Exemplo real (eval case 2):**
```
question: "Detectei sinais de aula tecnica E apresentacao clinica. É mais aula de dosimetria/protocolo Er:YAG, ou apresentacao do protocolo clinico ja consolidado?"
header: "Rota deck"
options:
  - label: "Aula tecnica (deck-teaching)"
    description: "Ensino estruturado, chunks ≤7min, hands-on, quiz Bloom-aplicar"
  - label: "Apresentacao clinica (deck-clinical)"
    description: "Peer-facing, EBM/GRADE, indicacao/contraindicacao, casos clinicos"
```

### T1.b — 3+ rotas empatadas (smoke test extra)

```python
options=[
  {label: "Rota A", description: "..."},
  {label: "Rota B", description: "..."},
  {label: "Rota C", description: "..."}
]
```

Limite max 4 opcoes (incluindo "Outro" auto-injetado pela tool). Se 4+ rotas empatam, pega as 3 com maior `score` global de keywords no input.

---

## T2 — Coletar U1-U3 (input vago, 0-1 keyword)

**Quando:** `top[0].score <= 1 and top[1].score == 0`.

Faz as 3 perguntas universais em **uma unica chamada** (AskUserQuestion aceita 1-4 questions):

```python
AskUserQuestion(
  questions=[
    {
      "question": "Qual o objetivo unico deste deck? (acao que a audiencia deve tomar apos assistir)",
      "header": "Objetivo",
      "multiSelect": False,
      "options": [
        {"label": "Convencer a investir/comprar/aprovar algo", "description": "Foco em decisao + ROI/payback"},
        {"label": "Ensinar/treinar/transferir conhecimento", "description": "Foco em aprendizado + hands-on"},
        {"label": "Alinhar/informar time interno", "description": "Foco em decisao colegiada ou status"},
        {"label": "Apresentar resultado de pesquisa/protocolo", "description": "Foco em rigor cientifico/clinico"}
      ]
    },
    {
      "question": "Quem e a audiencia?",
      "header": "Audiencia",
      "multiSelect": False,
      "options": [
        {"label": "Externa — investidor / cliente / paciente", "description": ""},
        {"label": "Externa — peer especialista (medico, cientista, dentista)", "description": ""},
        {"label": "Interna — board / CEO / lideranca", "description": ""},
        {"label": "Interna — squad / time operacional", "description": ""}
      ]
    },
    {
      "question": "Quanto tempo de apresentacao?",
      "header": "Duracao",
      "multiSelect": False,
      "options": [
        {"label": "3-5min (pitch curto / demo day)", "description": ""},
        {"label": "7-12min (call remota padrao)", "description": ""},
        {"label": "15-20min (reuniao decisoria)", "description": ""},
        {"label": "30-45min (aula curta / proposta deep)", "description": ""},
        {"label": "60min+ (workshop / aula longa / congresso)", "description": ""}
      ]
    }
  ]
)
```

**Apos coletar:** orchestrator re-roda algoritmo D10 com input + respostas U1-U3.
- Se agora identifica rota → roteia + handoff inclui `respostas_pre_coletadas`
- Se ainda vago → vai para T3

---

## T3 — Sugerir `/idea-to-brief` (apos U1 ainda vago — D12)

**Quando:** `respostas_pre_coletadas.U1` vago/curto/sem objetivo concreto.

> **NUNCA AUTO-DELEGA `/idea-to-brief` (D12).** Sempre pergunta explicitamente.

```python
AskUserQuestion(
  questions=[{
    "question": "Seu input ainda esta vago para escolher uma vertical especifica. Recomendo rodar `/idea-to-brief` primeiro para destilar a ideia em BRIEF estruturado antes de gerar o deck. Quer fazer isso?",
    "header": "Pre-deck",
    "multiSelect": False,
    "options": [
      {
        "label": "Sim, rodar /idea-to-brief primeiro (Recomendado)",
        "description": "Vai te fazer 5-10 perguntas + pesquisa automatica e retorna BRIEF.md. Depois voce roda /deck com o brief em maos."
      },
      {
        "label": "Nao, segue com deck-builder mesmo assim",
        "description": "Vou tentar inferir vertical com mais 2-3 perguntas e melhor palpite. Mais risco de erro."
      },
      {
        "label": "Cancelar — vou pensar e volto depois",
        "description": ""
      }
    ]
  }]
)
```

**Acoes pos-resposta:**
- Opcao 1 → orchestrator delega `/idea-to-brief` com input original como contexto
- Opcao 2 → orchestrator faz mais 1-2 perguntas (U4/U5) e roteia para `deck-internal all-hands` como melhor palpite default
- Opcao 3 → orchestrator sai limpo

---

## T4 — Pipeline cenografia (concept-reveal — D3)

**Quando:** rota = `concept-reveal` (rotas 9 da matriz).

```python
AskUserQuestion(
  questions=[{
    "question": "Detectei pipeline cenografia. Modo `concept-reveal` do `deck-internal` consome artefatos da `skill-cenografia` (renders, mood, layout, set design). Voce ja gerou esses artefatos?",
    "header": "Cenografia",
    "multiSelect": False,
    "options": [
      {
        "label": "Sim, tenho os paths/JSONs prontos",
        "description": "Vou te pedir os paths logo em seguida e ja delegar para deck-internal"
      },
      {
        "label": "Nao, ainda preciso gerar",
        "description": "Rode `skill-cenografia` primeiro e me chame de volta com os paths. Vou pausar aqui."
      },
      {
        "label": "Quero apresentar SEM os artefatos visuais ainda",
        "description": "Risco: concept-reveal sem render fica abstrato. Vou delegar com warning."
      }
    ]
  }]
)
```

**Acoes pos-resposta:**
- Opcao 1 → orchestrator pergunta os paths via Bash/mensagem aberta, monta `pipeline_cenografia.artefatos_paths`, delega `deck-internal` concept-reveal
- Opcao 2 → orchestrator imprime instrucao `/skill-cenografia + Carnaval 360/Beauty Smile/Fotona` e PAUSA (nao delega)
- Opcao 3 → orchestrator delega `deck-internal` com `pipeline_cenografia.status: "sem_artefatos_warning"` no handoff

---

## Regras inviolaveis de uso

1. **NUNCA gerar deck sem rotear.** Empate → SEMPRE AskUserQuestion. Vago → SEMPRE AskUserQuestion.
2. **NUNCA auto-delegar `/idea-to-brief`** (D12). Sempre T3 antes.
3. **NUNCA pular auto-detection §10.5** — roda antes do count de keywords.
4. **AskUserQuestion aceita max 4 opcoes** (incluindo "Outro" auto-injetado). Se ha 5+ rotas empatadas, pega top 3 por score global e adiciona "Outro" implicito.
5. **NUNCA tentar adivinhar marca** — se auto-detection falhar, marca = "generico" e a vertical pergunta U6.
6. **AskUserQuestion `header` max 12 chars** — usar abreviacoes (Rota, Objetivo, Cenografia, Pre-deck).

---

## Fluxograma decisao AskUserQuestion

```
score top[0] >= 2 AND top[1] < top[0]
  → routing direto SEM AskUserQuestion (caminho 90%)

score top[0] == top[1] >= 1
  → T1 (ambiguidade)

score top[0] <= 1 AND top[1] == 0
  → T2 (coletar U1-U3)
  → re-roda algoritmo
    → se agora classifica → routing direto + handoff com pre-coletadas
    → se ainda vago → T3 (sugere idea-to-brief)

rota == concept-reveal
  → T4 (pipeline cenografia) + roteia deck-internal

rota in [copy, culture_lab, cenografia]
  → mensagem clara "NAO e deck" + delega externamente SEM AskUserQuestion
```
