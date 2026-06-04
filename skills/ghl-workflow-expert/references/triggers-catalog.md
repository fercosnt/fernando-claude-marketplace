# Catalogo Completo de Triggers — GHL Workflows

## Indice
1. [Contact Triggers](#contact-triggers)
2. [Payment Triggers](#payment-triggers)
3. [Developer/Premium Triggers](#developerpremium-triggers)
4. [IVR Triggers](#ivr-triggers)
5. [Social/External Triggers](#socialexternal-triggers)
6. [Integration Triggers](#integration-triggers)
7. [Novos Triggers 2025-2026](#novos-triggers-2025-2026)
8. [Categorias Adicionais](#categorias-adicionais)

---

## Contact Triggers

| Trigger | Descricao | Filtros Disponiveis |
|---------|-----------|---------------------|
| Birthday Reminder | Dispara na data de aniversario do contato | — |
| Note Changed | Nota do contato alterada | — |
| Note Added | Nova nota adicionada ao contato | — |
| Task Completed | Tarefa do contato concluida | — |
| Task Added | Nova tarefa criada para o contato | — |
| Task Reminder | Lembrete de tarefa disparado | — |
| Contact Changed | Qualquer campo do contato alterado | Campo especifico |
| Contact Tag | Tag adicionada ou removida | Added/Removed, tag especifica |
| Contact Created | Novo contato criado no sistema | Source |
| Contact DND | DND (Do Not Disturb) ativado/desativado | — |
| Custom Date Reminder | Lembrete por campo de data customizado | Campo, antecedencia |
| Trigger Link Clicked | Link de trigger clicado pelo contato | Link especifico |
| Contact Engagement Score | Score de engajamento muda | Threshold |

### Dicas de Uso

- **Contact Tag** e o trigger mais versatil — use para conectar workflows entre si (modularidade)
- **Contact Changed** com filtro de campo especifico e ideal para workflows reativos
- **Custom Date Reminder** funciona para renovacoes, vencimentos, follow-ups periodicos

---

## Payment Triggers

| Trigger | Descricao | Filtros Disponiveis |
|---------|-----------|---------------------|
| Payment Received | Qualquer pagamento capturado | Source (Invoice/Funnel/Calendar), Sub-Source (Text2Pay, order forms, upsells), Transaction Type, Product, Status (success/failed) |
| Order Submitted | Pedido enviado pelo cliente | — |

### Dicas de Uso

- **Payment Received** com filtro de Status = "failed" permite workflow de recuperacao de pagamento
- Filtrar por Product para workflows pos-compra especificos por produto/servico

---

## Developer/Premium Triggers

| Trigger | Descricao | Filtros | Tipo |
|---------|-----------|---------|------|
| Inbound Webhook | Requisicao HTTP externa (POST/GET/PUT) | Mapeamento de campos JSON | Premium |
| Number Validation | Valida telefone na criacao do contato | Mobile/Landline/VoIP/Invalid | Standard |
| Video Tracking | Contato assiste X% de video | Funnel, Video, Duration % (25/50/75/100) | Standard |

### Inbound Webhook — Detalhes

O Inbound Webhook e o trigger mais poderoso para integracoes externas:
- Suporta POST, GET, PUT
- Mapeamento de campos JSON do payload para custom fields
- Cada webhook gera URL unica
- **Conta como execucao premium** — considerar custo
- Use para: integrar n8n, Make, sistemas externos, formularios custom

---

## IVR Triggers

| Trigger | Descricao |
|---------|-----------|
| Start IVR | Chamada entra no numero designado para IVR |

IVR workflows sao dedicados — usam actions especificas (Gather Input, Say/Play, Connect Call, End Call, Record Voicemail).

---

## Social/External Triggers

| Trigger | Descricao |
|---------|-----------|
| Facebook Conversion API | Evento de conversao no Facebook |
| Instagram Comment | Comentario em post do Instagram |
| Facebook Comment | Comentario em post do Facebook |

### Dicas de Uso

- Instagram/Facebook Comment triggers sao base dos recipes de Comment Automation
- Combinam bem com DM automatica + entrega de recurso (lead magnet)

---

## Integration Triggers

### ClickUp (9 triggers)

| Trigger | Descricao |
|---------|-----------|
| New Task | Nova tarefa criada |
| Task Changes | Tarefa alterada |
| New List | Nova lista criada |
| New Folder | Nova pasta criada |
| New Comment | Novo comentario |
| New Attachment | Novo anexo |
| New Reaction (Chat) | Nova reacao em chat |
| New Reaction (Comment) | Nova reacao em comentario |
| New Time Entry | Nova entrada de tempo |

### Airtable (2 triggers)

| Trigger | Descricao | Nota |
|---------|-----------|------|
| New Record | Novo registro criado | Polling ~5min |
| Updated Record | Registro atualizado | Polling ~5min |

**Importante**: Airtable usa polling (a cada ~5 minutos), nao webhook em tempo real.

---

## Novos Triggers 2025-2026

| Trigger | Periodo | Descricao | Impacto |
|---------|---------|-----------|---------|
| Company Created/Changed | 2025-2026 | Workflows B2B baseados em empresa | Alto — habilita automacao B2B |
| Workflow Scheduler | 2025-2026 | Cron nativo (hora/dia/semana/mes) | Alto — automacoes backend sem contato |
| Proposals & Estimates | 2025-2026 | Sent/Signed/Accepted/Completed | Medio |
| Community Leaderboard Level Changed | 2025-2026 | Mudanca de nivel no leaderboard | Baixo |
| New Affiliate Sales | 2025-2026 | Vendas de afiliados (one-time, recorrente, manual) | Medio |
| Opportunity Changed (Enhanced) | 2026-01 | Novos operadores "Has Changed" e "Has Changed To" | Alto — condicoes mais precisas |
| Conversation AI Trigger | 2025-2026 | AI bot aciona workflow por intencao detectada | Alto — AI-first workflows |

### Workflow Scheduler

Destaque especial: permite criar automacoes de backend (limpeza de dados, relatorios, sincronizacao) sem necessidade de um contato como trigger. Funciona como cron job nativo.

---

## Categorias Adicionais

Triggers identificados na documentacao mas sem detalhamento completo. Para detalhes atualizados, consultar NotebookLM:

- **Opportunity Triggers** — mudanca de stage, opportunity criada, etc.
- **Company Triggers** — B2B workflows
- **Events Triggers** — eventos do calendário
- **Appointments Triggers** — agendamento criado/modificado/cancelado (agora com suporte a Guests)
- **Courses Triggers** — progresso em cursos/memberships
- **Shopify Triggers** — pedidos, carrinhos abandonados
- **Communities Triggers** — atividade em comunidades GHL
- **Forms and Surveys Triggers** — submissao de formularios e pesquisas
- **TikTok Triggers** — eventos TikTok
- **LinkedIn Triggers** — eventos LinkedIn

> **Dica**: Para qualquer trigger nao detalhado aqui, consultar o NotebookLM que contem a documentacao oficial completa.
