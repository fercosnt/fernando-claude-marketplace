# Technical Setup Checklist — SDR Chatbot [NICHO]

> Gerado pela skill `ghl-sdr-chatbot-builder` | Data: [DATA]

---

## Conversation AI

| Item | Status | Detalhe |
|------|--------|---------|
| Conversation AI ativado | [ ] | Sub-account: [ID] |
| Modelo selecionado | [ ] | [GPT-4 / Claude / outro] |
| Canal configurado | [ ] | [WhatsApp / SMS / Web Chat] |
| Horario de funcionamento | [ ] | [horarios] |
| System prompt inserido | [ ] | [caracteres: X/limite] |
| Triggers de ativacao | [ ] | [descricao dos triggers] |
| Condicoes de parada | [ ] | [handoff / inatividade / desqualificacao] |

---

## Custom Fields Criados

| Nome do Campo | Tipo | Objeto | Proposito | GHL ID | Status |
|---------------|------|--------|-----------|--------|--------|
| [campo] | [tipo] | [contact] | [proposito] | [id retornado pela API] | [ ] |

> Criados via `ghl_create_custom_field`

---

## Tags Criadas

| Tag | Proposito | Aplicada Quando |
|-----|-----------|-----------------|
| `bot-qualificando` | Lead em processo de qualificacao pelo bot | Bot inicia conversa |
| `bot-qualificado` | Lead qualificado pelo bot | Score >= threshold |
| `bot-desqualificado` | Lead desqualificado pelo bot | Criterio de desqualificacao atingido |
| `handoff-humano` | Lead transferido para atendimento humano | Qualificacao completa ou pedido explicito |
| `bot-inativo` | Lead parou de responder | Sem resposta apos X horas |
| `bot-agendado` | Lead agendou avaliacao (v2) | Agendamento confirmado |
| [tags adicionais especificas do nicho] | [proposito] | [quando] |

> Aplicadas via `add_contact_tags`

---

## Pipeline Setup

| Pipeline | Stage | Proposito | Automacao |
|----------|-------|-----------|-----------|
| [pipeline] | [stage 1] | Lead novo do bot | Bot inicia qualificacao |
| [pipeline] | [stage 2] | Em qualificacao | Bot coletando dados |
| [pipeline] | [stage 3] | Qualificado | Handoff para humano |
| [pipeline] | [stage 4] | Agendado (v2) | Bot agendou |
| [pipeline] | [stage 5] | Desqualificado | Nurturing sequence |

> Movimentacao via `create_opportunity` / `update_opportunity`

---

## Lead Scoring

### Acoes que Somam Pontos
| Acao | Pontos |
|------|--------|
| Respondeu primeira mensagem | +5 |
| Informou nome | +5 |
| Descreveu necessidade | +10 |
| Tem urgencia/evento | +15 |
| E o decisor | +10 |
| Ja pesquisou precos | +5 |
| Pediu para agendar | +20 |

### Acoes que Subtraem Pontos
| Acao | Pontos |
|------|--------|
| Sem resposta apos 24h | -10 |
| Disse "so pesquisando" | -5 |
| Localizacao fora da area | -15 |
| Pediu para nao enviar mais msgs | -30 |

### Thresholds
| Nivel | Score | Acao |
|-------|-------|------|
| Frio | 0-15 | Nurturing sequence |
| Morno | 16-35 | Follow-up em 24-48h |
| Quente | 36-50 | Priorizar handoff |
| Qualificado | 51+ | Handoff imediato |

---

## Workflows Configurados

### Workflow 1: Handoff Qualificado
- **Trigger**: Tag `bot-qualificado` aplicada
- **Acoes**:
  - [ ] Mover para stage [X] no pipeline
  - [ ] Atribuir para usuario [consultor/closer]
  - [ ] Enviar notificacao interna (WhatsApp/email)
  - [ ] Enviar mensagem ao lead: "Vou te conectar com [nome]..."

### Workflow 2: Nurturing (Desqualificado/Frio)
- **Trigger**: Tag `bot-desqualificado` ou `bot-inativo` aplicada
- **Acoes**:
  - [ ] Mover para stage [Y] no pipeline
  - [ ] Adicionar a sequencia de emails/SMS
  - [ ] Follow-up em [7/14/30] dias

### Workflow 3: Follow-up Inatividade
- **Trigger**: Sem resposta apos [X] horas
- **Acoes**:
  - [ ] Enviar lembrete: "Oi [nome], ainda posso te ajudar..."
  - [ ] Se sem resposta em 24h mais: segundo lembrete
  - [ ] Se sem resposta em 72h: aplicar tag `bot-inativo`

### Workflow 4: Agendamento (v2)
- **Trigger**: Lead qualificado + disponibilidade confirmada
- **Acoes**:
  - [ ] Criar appointment via `create_appointment`
  - [ ] Enviar confirmacao ao lead
  - [ ] Lembrete 24h antes
  - [ ] Lembrete 1h antes

---

## Status Geral

| Componente | Status | Observacao |
|------------|--------|------------|
| Conversation AI | [OK / Pendente / N/A] | |
| Custom Fields | [X/Y criados] | |
| Tags | [X/Y criadas] | |
| Pipeline | [OK / Pendente] | |
| Lead Scoring | [OK / Pendente] | |
| Workflows | [X/Y configurados] | |

---

## Passos Manuais Pendentes

> Itens que NAO puderam ser configurados via API e requerem acesso a UI do GHL:

- [ ] [Passo manual 1 — link para secao do GHL]
- [ ] [Passo manual 2]
- [ ] [Passo manual 3]

**Instrucoes detalhadas**: Ver `references/ghl-conversation-ai.md` e `references/ghl-workflows.md`
