# Workflows e Automacoes GHL para Chatbot SDR

## Quando carregar
Fase 2 (configuracao de workflows no GHL), Fase 3 (compilacao do briefing), e sempre que precisar configurar triggers, handoff, follow-up ou isolamento de bot.

---

## 1. Triggers de Workflow para Bot SDR

### Customer Replied (principal)
- Trigger padrao para mensagens inbound
- OBRIGATORIO filtrar por canal (WhatsApp, SMS, Email, etc.)
- Filtros adicionais recomendados: source do lead, tag especifica, pipeline stage
- Uso: ativar bot quando lead responde em canal especifico

### Click to WhatsApp Ads
- Trigger para trafego vindo de anuncios WhatsApp (Meta Ads)
- Lead entra direto no chat WhatsApp — bot deve responder imediatamente
- Combinar com tag de origem (ex: `trafego-pago-whatsapp`)

### Chat Initiated
- Trigger nativo do Flow-Based Builder
- Dispara quando conversa e iniciada pelo lead
- Disponivel apenas dentro do Flow Builder (nao no Workflow Builder classico)

### Custom Triggers
- Ate 3 triggers customizados por fluxo
- Niveis de sensibilidade para deteccao de intencao: Low, Medium, High
- Low: match exato ou quase exato
- Medium: match semantico moderado
- High: match amplo (mais false positives, mais cobertura)

---

## 2. Acoes de Controle do Bot

### Update Conversation AI Bot and Status
- Seleciona QUAL bot assume o lead
- Define status: Active ou Inactive
- ESSENCIAL para campanhas DBR (Database Reactivation) e isolamento por canal
- Sem essa acao, o bot Primary assume todos os leads — causa conflito

### Transfer Bot Action
- Transferencia bot-para-bot dentro do fluxo
- Exemplo: Triage Bot → Closer Bot
- O segundo bot herda o contexto da conversa
- Usar quando a qualificacao exige bots com personalidades/instrucoes distintas

### Conversation AI Workflow Action
- Envia UMA mensagem de IA e aguarda resposta do lead
- Permite roteamento via Branches (condicoes) apos a resposta
- "Advanced Bot Configuration": override de Personality e Instructions por interacao
- Util para micro-interacoes pontuais sem criar bot separado

---

## 3. Acoes de CRM no Flow Builder

### Tags
- **Add Tag**: aplicar tag apos analise de intencao (ex: `trafego-pago`, `servicos`, `bot-qualificado`)
- **Remove Tag**: limpar tags temporarias apos transicao de stage
- AI Splitter analisa intencao do lead e aplica tags dinamicamente

### Oportunidades e Pipeline
- **Create Opportunity**: preencher pipeline, stage, status e valor monetario apos qualificacao
- **Move Pipeline Stage**: mover lead entre stages com base no resultado do bot
- Campos obrigatorios: pipeline ID, stage name, status (open/won/lost), monetary value (se aplicavel)

### Atribuicao
- **Assign to User**: delegar lead para vendedor especifico apos triage
- Pode usar round-robin ou atribuicao fixa por regra

---

## 4. Auto Follow-Up (Nativo)

### Configuracao
- Localizado em: Bot Goals → Auto Follow-Up
- Ate 5 mensagens sequenciais programadas
- Dispara quando lead para de responder
- Substituiu as acoes classicas de "Wait" nos workflows

### Horarios e Restricoes
- Configurar Active Hours para envio (horario comercial)
- Timezone: pode usar timezone do cliente ou do negocio
- **WhatsApp: janela de 24h do Meta se aplica** — apos 24h sem resposta do lead, so e possivel enviar template messages aprovadas

### Sequencia recomendada
1. Follow-up 1: 1 hora apos silencio
2. Follow-up 2: 24 horas
3. Follow-up 3: 72 horas
4. Follow-up 4: 7 dias
5. Follow-up 5: 14 dias (mensagem final)

---

## 5. Padroes de Handoff via Workflow

### Lead Qualificado

```
1. Bot aplica tag `bot-qualificado`
2. Create Opportunity no pipeline (stage: Qualificado)
3. Assign to User (closer/consultor)
4. Enviar notificacao interna (email/SMS para o closer)
5. Bot envia mensagem de transicao ao lead
   Ex: "Vou te passar para [nome], nosso especialista. Ele ja tem todo o contexto."
6. Bot pausa (status → Inactive)
```

### Lead Desqualificado

```
1. Bot aplica tag `bot-desqualificado`
2. Move Pipeline Stage → Nurturing
3. Adicionar lead a sequencia de nurturing (email/SMS)
4. Programar follow-up em 7, 14 e 30 dias
```

### Lead Inativo (sem resposta)

```
1. Auto Follow-Up dispara sequencia nativa (ate 5 mensagens)
2. Apos X tentativas sem resposta:
   - Aplicar tag `bot-inativo`
   - Move Pipeline Stage → Frio/Cold
   - Entrar em nurturing de longo prazo
```

---

## 6. Padrao de Isolamento de Bot (WhatsApp-only)

Quando o bot NAO deve ser Primary (ex: bot especifico para campanha ou canal):

```
1. Criar bot no Conversation AI — NAO marcar como Primary
2. Criar Workflow com trigger: Customer Replied
   - Filtro: canal = WhatsApp
   - Filtro adicional: source do lead ou tag especifica
3. Acao: Update Conversation AI Bot and Status
   - Selecionar o bot correto
   - Status: Active
4. Bot assume APENAS leads que matcham os filtros
5. Leads de outros canais/fontes nao sao afetados
```

**Por que usar**: sem isolamento, o bot Primary assume TODOS os leads de todos os canais, causando conflito em campanhas DBR ou quando ha multiplos bots configurados.

---

## 7. Ferramentas GHL-MCP Disponiveis

### Workflows (limitado)
| Ferramenta | Capacidade |
|---|---|
| `ghl_get_workflows` | READ ONLY — listar workflows existentes |
| Criar/editar workflows | NAO disponivel via API — usar UI ou Snapshots |

### CRM
| Ferramenta | Capacidade |
|---|---|
| `add_contact_tags` | Aplicar tags a contatos |
| `create_opportunity` | Criar oportunidade no pipeline |
| `ghl_get_custom_fields_by_object_key` | Listar custom fields |
| `ghl_create_custom_field` | Criar custom fields |

### Conversation AI (API Publica)
| Operacao | Descricao |
|---|---|
| Create Agent | Criar novo bot |
| Search Agents | Buscar bots existentes |
| Update Agent | Atualizar configuracao do bot |
| Get Agent | Obter detalhes de um bot |
| Delete Agent | Remover bot |
| Attach/Update/Remove Action | Gerenciar acoes do bot |
| Update Followup Settings | Configurar auto follow-up |

**Acao de runtime**: "Update Conversation AI Bot and Status" — disponivel como acao de workflow, nao como chamada API direta.

---

## 8. Gotchas e Armadilhas

### Conflito de bots em DBR
- Multiplos bots ativos sem isolamento = leads recebem respostas de bots errados
- SEMPRE usar "Update Conversation AI Bot and Status" antes de campanhas DBR
- Definir qual bot e Primary e quais sao ativados por workflow

### Janela de 24h do WhatsApp (Meta)
- Apos 24h sem mensagem do lead, WhatsApp so permite template messages aprovadas
- Follow-ups apos 24h devem usar templates pre-aprovados ou outro canal (SMS/email)
- Planejar os primeiros follow-ups dentro da janela de 24h

### Toggle critico: "Send Bot to sleep when I send a message manually"
- Se ativado: quando humano envia mensagem manual, bot desativa automaticamente
- Se desativado: bot pode interferir durante atendimento humano
- RECOMENDADO: manter ativado para evitar conflito bot vs humano

### Workflows NAO podem ser criados via API
- Skill deve orientar o usuario a configurar workflows manualmente na UI do GHL
- Alternativa: usar Snapshots para importar workflows pre-configurados
- GHL-MCP so permite LEITURA de workflows existentes
