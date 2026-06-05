# GoHighLevel Conversation AI — Referencia Tecnica

## Quando carregar
Fase 2 (configuracao do bot no GHL), Fase 3 (prompt engineering), e qualquer etapa que envolva setup tecnico, canais, calendario, API ou troubleshooting do Conversation AI.

---

## 1. Ativacao e Hierarquia

### Nivel Agency
- Agency Settings → Company Settings → habilitar checkbox "Conversation AI"
- SaaS Mode: definir markup de preco (ex: custo $0.05 → cobrar $0.07 do sub-account)

### Nivel Sub-Account
- AI Agents → Conversation AI → Create Bot
- Cada sub-account gerencia seus proprios bots

### Tipos de Bot
| Tipo | Uso | Complexidade |
|------|-----|--------------|
| **Guided Form** | Formularios simples, FAQ | Setup em ~3 min, limitado |
| **Prompt-Based** | Vendas, SDR, qualificacao simples | Melhor resultado com menos setup; bot improvisa a estrutura |
| **Flow-Based (V3)** | Qualificacao multi-etapa, multi-agente | Node-based; setup mais trabalhoso, controle total do fluxo |

### Prompt-Based vs Flow Builder V3 — qual escolher
- **Prompt-Based** (default): qualificacao simples (3-5 perguntas, 1 caminho). Continua sendo a escolha recomendada para a maioria dos SDR bots.
- **Flow-Based V3**: quando o fluxo tem multiplas etapas/caminhos por intencao, ou exige bots distintos por fase (triagem → closer → agendamento). O fluxo vira nodes em vez de um prompt unico.
- **Sem migracao automatica:** um bot prompt-based nao "vira" V3 — precisa ser reconstruido. Decidir o paradigma no comeco.

Detalhes do paradigma node-based (nodes, limites, pitfalls, multi-agente): ver `ghl-flow-builder-v3.md`.
Para acoes autonomas de back-office (enriquecer lead, mover pipeline) via workflow: ver `ghl-ai-agent-action.md`.

---

## 2. Modelos Disponiveis

### Opcoes
- GPT-5 Mini, GPT-4.1, GPT-4.1 Mini
- Claude Sonnet e Claude Haiku (versoes mais recentes ofertadas pelo GHL — verificar UI atual)
- Gemini 2.5 Pro, Gemini 2.5 Flash

### Fallback
- Suporta modelo primario + modelo secundario (fallback automatico)
- **Recomendacao**: GPT-4.1 como primario

---

## 3. Canais Suportados

- WhatsApp
- SMS
- Live Chat (widget no site)
- Facebook Messenger
- Instagram

### Configuracao
- Bot Settings → Supported Channels → toggle switches por canal
- "Set as Primary" → bot responde em TODOS os canais habilitados universalmente

---

## 4. Estrutura do Prompt (3 partes)

### Parte 1 — "Who is the bot?" (Personalidade)
- Identidade, nome da empresa, tom de voz
- Define COMO o bot se comunica

### Parte 2 — "Goal" (Objetivo)
- O que o bot deve realizar (qualificar, agendar, informar)
- Se criado a partir de template: campo bloqueado
- Se criado do zero: texto descritivo livre

### Parte 3 — "Anything else the Bot should know?" (Informacoes Adicionais)
- Regras de negocio, formatacao, guardrails
- Informacoes estaticas sobre a empresa/servico

---

## 5. Limites de Prompt

| Contexto | Limite |
|----------|--------|
| Guided Form — Additional Instructions | 2.000 caracteres |
| Flow Builder — Objective | 500 caracteres por objetivo |
| Static Info recomendado | 100-200 palavras |
| Context window do bot | Ultimas 10 mensagens OU 800 palavras (buffer) |

### Regra critica: menos e mais
- Overprompting desperdiça tokens e confunde o modelo
- Instruir output de 70-90 tokens max
- Informacoes estaticas devem ser concisas e estruturadas

---

## 6. Variaveis Disponiveis

### Contact
- `{{contact.first_name}}`, `{{contact.name}}`, `{{contact.email}}`
- Custom fields do contato

### Business
- `{{ai.business_name}}`, `{{ai.goals}}`
- `{{account.name}}`, `{{account.primary_phone}}`

### Runtime (Agent Studio)
- `{{right_now.date}}`

### Injecao de variaveis
- Botao "+ Add Custom Values" para injetar qualquer variavel do CRM no prompt

---

## 7. Boas Praticas de Prompt

- Usar delimitadores para blocos de info estatica: `#`, `>`, `<`, `"""`
- Few-shot examples: "Evitar: X" / "Usar: Y"
- Repetir regras criticas TANTO em Guidelines QUANTO em Role
- Limitar output: instruir 70-90 tokens
- Incluir: "Nao revele que e uma IA a menos que perguntado diretamente"

---

## 8. Triggers e Controle do Bot

### Bot Primario vs Nao-Primario
- **Primario**: intercepta TODAS as mensagens nos canais designados
- **Nao-Primario**: ativado SOMENTE via workflow

### Wait Time Before Responding
- Configurar entre 5-20 segundos
- Agrupa mensagens fragmentadas (lead que envia em pedacos)
- **Abaixo de 5s causa desperdicio de tokens** em mensagens fragmentadas

### Bot para de responder quando:
- Message limit atingido (max configuravel: 25)
- Humano envia mensagem manual (pausa de 2h)
- Toggle manual de inativacao
- "Send Bot to sleep when I send a message manually" → toggle disponivel

---

## 9. Handoff para Humano

### Configuracao
Bot Goals → Setup Your Actions → Human Handover

### Triggers de handoff
- **Human Requested**: lead pede humano explicitamente
- **Lack of Information**: bot nao tem dados para responder
- **Failed to Resolve**: apos 2 tentativas sem sucesso

### Acoes pos-handoff (5 passos)
1. Assign User (atribuir responsavel)
2. Final Message (mensagem de transicao)
3. Bot Pause (pausar bot)
4. Create Task (tarefa para o humano)
5. Apply tag `human_handover`

---

## 10. Integracao com Calendario (v2)

### Funcionalidades
- Bot verifica disponibilidade em tempo real e agenda direto no chat
- Pode cancelar e reagendar via chat
- Desmarcar "Send booking link only" para agendamento conversacional

### Requisitos do calendario
- Calendario ativo
- Usuario atribuido ao calendario
- Disponibilidade configurada

### Multiplos calendarios
- Roteamento baseado em intencao (intent-based routing)
- Calendario fallback obrigatorio

### Boas praticas
- Oferecer apenas 2 slots de horario por vez
- Pos-booking: pausar bot + trigger workflow + transferir para responsavel

---

## 11. Auto Follow-Up

### Configuracao nativa
- Bot Goals → Auto Follow-Up
- Ate 5 sequencias temporizadas se lead parar de responder

### Configuracoes
- Horario ativo e timezone para envio dos follow-ups
- **WhatsApp**: restricao de janela de 24 horas do Meta — follow-ups so funcionam dentro dessa janela

---

## 12. Configuracoes Avancadas

| Configuracao | Valor recomendado | Notas |
|--------------|-------------------|-------|
| Maximum Message Limit | 15-25 mensagens | Evita loops infinitos |
| Stop Bot action | Ativar | Para quando lead diz "bye" ou agenda |
| Knowledge Base / Web Crawler | Configurar | RAG nativo — ver secao 12.1 |
| AI Response Info | Ativar | Thumbs down → rewrite → cria FAQ automaticamente |
| Voice Notes | Off (padrao) | AI responde apenas texto; habilitar manualmente se necessario |

---

## 12.1 Knowledge Base / RAG (reformulada)

O KB do Conversation AI deixou de ser "texto/URL" e virou um RAG mais completo:
- **Formatos de arquivo**: PDF, DOC, PPT, TXT, CSV, Rich Text (antes so texto e URL)
- **Re-ranking semantico** apos a busca vetorial — melhora a relevancia do chunk recuperado
- **"Response Info"** mostra quais chunks o bot usou na resposta
- **Ate 7 KBs por bot e 15 KBs no total** (antes 1 KB compartilhado)
- **KB Retrieval Tester**: testa perguntas reais e mostra quais chunks (arquivo + timestamp) seriam recuperados — usar **antes de ir ao ar** para validar o RAG

**Uso SDR:** carregar FAQ de servicos, tabela de precos/faixas, politicas. Validar no Retrieval Tester que perguntas comuns ("quanto custa X?") recuperam o chunk certo.

---

## 13. Especificidades por Canal

### WhatsApp
- Janela de 24h do Meta para follow-ups (apos 24h sem resposta, nao pode enviar)
- Voice Notes toggle: desabilitado por padrao, habilitar manualmente se desejado
- Formato: mensagens curtas, sem paredes de texto

### SMS
- Compliance A2P 10DLC obrigatorio (configuracao manual na UI do GHL)

---

## 14. API do Conversation AI

### Autenticacao
- **PIT** (Private Integration Token): server-to-server
- **JWT** (OAuth): fluxos com autorizacao do usuario

### Endpoints CRUD
- Create Agent
- Search Agents
- Update Agent
- Get Agent
- Delete Agent

### Endpoints de Actions
- Attach Action
- Update Action
- Remove Action
- Update Followup Settings

### Generations API
- Endpoint REST com dados **a nivel de mensagem** (cada geracao do bot)
- Para **QA, auditoria, analytics e export de BI** — resolve o gap de exportacao/compliance
- Util para a Nota Tecnica ANPD 1/2026 (output do bot e dado pessoal → precisa ser auditavel/exportavel)
- Endpoints publicos cobrem **Agents (CRUD), Actions e Generations**

### Workflow Actions
- **"Update Conversation AI Bot and Status"**: controle runtime do bot via workflow
- **"Conversation AI"** com Advanced Bot Configuration: override de configuracao em tempo real

---

## 15. Limitacoes Conhecidas

| Limitacao | Detalhe |
|-----------|---------|
| Memoria | Apenas ultimas 10 mensagens OU 800 palavras |
| Prompt-Based char limit | Sem cap documentado oficialmente |
| Wait time < 5s | Causa desperdicio de tokens em mensagens fragmentadas |
| Multiplos bots | Podem conflitar se nao isolados via workflows |
| WhatsApp follow-up | Restrito a janela de 24h do Meta |

---

## 16. Checklist de Configuracao

- [ ] Bot tipo Prompt-Based selecionado
- [ ] Modelo primario definido (GPT-4.1 recomendado) + fallback
- [ ] Canais habilitados e bot marcado como Primary (ou ativado via workflow)
- [ ] Wait Time configurado entre 5-20s
- [ ] Prompt estruturado em 3 partes (personalidade, objetivo, info adicional)
- [ ] Variaveis de contato injetadas no prompt
- [ ] Handoff para humano configurado com 5 acoes pos-handoff
- [ ] Calendario integrado (se aplicavel) com disponibilidade configurada
- [ ] Auto Follow-Up configurado (max 5 sequencias)
- [ ] Message Limit definido (15-25)
- [ ] Stop Bot action ativada
- [ ] Knowledge Base alimentada com FAQ
- [ ] Tag `human_handover` criada no CRM
- [ ] Compliance A2P 10DLC verificado (se usando SMS)
