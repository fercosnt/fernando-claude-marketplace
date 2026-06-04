# Catalogo Completo de Actions — GHL Workflows

## Indice
1. [Contact Actions](#contact-actions)
2. [Internal Tools](#internal-tools)
3. [Data Formatting](#data-formatting)
4. [Communication Actions](#communication-actions)
5. [Send Data (Premium)](#send-data-premium)
6. [IVR Actions](#ivr-actions)
7. [Workflow AI Actions](#workflow-ai-actions)
8. [Integration Actions](#integration-actions)
9. [Categorias Adicionais](#categorias-adicionais)

---

## Contact Actions

| Action | Descricao | Notas |
|--------|-----------|-------|
| Create Contact | Cria novo contato | Verificar duplicatas antes |
| Find Contact | Busca contato existente | Usar antes de Update para garantir que existe |
| Update Contact Field | Atualiza campo (padrao ou custom) | Suporta date type |
| Add Contact Tag | Adiciona tag | Principal conector entre workflows |
| Remove Contact Tag | Remove tag | — |
| Add to Notes | Adiciona nota ao contato | Util para logging interno |
| Remove Assigned User | Remove usuario atribuido | — |
| DND Contact | Ativa/desativa Do Not Disturb | Cuidado: bloqueia TODAS as comunicacoes |
| Copy Contact To Sub Account | Copia para outra subconta | Para agencias multi-location |
| Assign To User | Atribui contato a usuario | Round-robin ou especifico |
| Go To | Loop/jump para outro passo | Cuidado com loops infinitos |
| GPT History | Historico de interacoes GPT | — |
| Delete Contact | Deleta contato permanentemente | IRREVERSIVEL — usar com extremo cuidado |
| Modify Contact Engagement Score | Altera score de engajamento | +/- valor numerico |
| Add/Remove Contact Follower | Gerencia seguidores do contato | — |
| Add Leads Under Affiliate | Vincula lead a afiliado | — |
| Add Manual Sales For Affiliate | Registra venda manual de afiliado | — |
| Log External Call | Registra chamada externa | — |
| Generate One Time Booking Link | Link de agendamento unico | Expira apos uso |

---

## Internal Tools

Estas sao as acoes de logica e controle de fluxo — o cerebro do workflow.

### If/Else (Branching Condicional)

O action mais poderoso do builder. Conditions disponiveis:

| Categoria | Conditions |
|-----------|------------|
| Contact Fields | Qualquer campo padrao ou custom (texto, numero, data, dropdown) |
| Contact Tag | Tem/nao tem tag especifica |
| Appointment | Status, data do agendamento |
| Time of Day | Intervalos de 15 minutos |
| Current Hour | Hora atual |
| Payment | Amount, status, source, product |
| Email Events | Open, click, unsubscribe, complaint, spam |
| Trigger Link | Clicou/nao clicou |
| Document Status | Viewed/Signed/Declined/Completed |
| Form Submitted | Formulario especifico submetido |
| Custom Values | Variaveis customizadas |

**Features**: 10 Scenario Recipes pre-configurados, text summaries nas branches, drag-and-drop para reordenar, dropdown pesquisavel.

### Split (A/B Testing)

- Ate **5 paths** com distribuicao percentual
- Nomes customizaveis por path
- Stats por path
- **Limitacao critica**: contato SEMPRE segue o mesmo path se re-entrar — nao randomiza em re-entries

### Math Operation

- Operacoes: Add, Subtract, Multiply, Divide (numeros)
- Operacoes de data: Add/Subtract dias, meses, anos
- **Output reutilizavel** em steps subsequentes (nao precisa de campo intermediario)

### Goal Event

Milestone comportamental que pode encerrar/continuar/pausar o workflow.

7 tipos: Form Submitted, Payment Received, Document Status, Email Events, Trigger Link, Tags, Appointment Status.

**Limitacao**: Maximo 1 Goal Event por workflow. Planejar estrategia de saida antes.

### Wait (Delay)

4 modos:
- **Por tempo**: X minutos/horas/dias
- **Por evento**: Espera acao especifica do contato
- **Por reply**: Espera resposta a mensagem
- **Por email event**: Espera open/click

### Go To

Jump/loop para outro step. Usar com moderacao para evitar loops infinitos.

---

## Data Formatting

### Text Formatter

| Operacao | Descricao |
|----------|-----------|
| Upper Case | Converte para maiusculas |
| Lower Case | Converte para minusculas |
| Title Case | Primeira letra de cada palavra maiuscula |
| Capitalize | Primeira letra maiuscula |
| Default Value | Valor fallback se campo vazio |
| Trim | Remove espacos inicio/fim |
| Trim Whitespace | Remove todos os espacos extras |
| Replace Text | Substitui texto |
| Find | Encontra texto |
| Length | Conta caracteres |
| Extract URL | Extrai URL de texto |
| Extract Email | Extrai email de texto |
| Word Count | Conta palavras |
| Remove HTML Tags | Limpa HTML |
| Split | Divide texto por separador |

### Date/Time Formatter

| Operacao | Descricao |
|----------|-----------|
| Format Date | Formata data (ex: DD/MM/YYYY) |
| Format Date-Time | Formata data e hora |
| Compare Dates | Calcula diferenca em dias entre duas datas |

### Number Formatter

Formatacao numerica (moeda, percentual, etc.)

---

## Communication Actions

| Action | Detalhes |
|--------|----------|
| Send Email | Com AI writer integrado, 4 tonalidades. Suporta HTML |
| Send SMS | Texto simples. Limite de caracteres por segmento |
| Send WhatsApp | Mercados suportados. Templates pre-aprovados necessarios |
| Edit Conversation | Edita conversa existente no inbox |

### Dicas

- **Wait de 1-4 min** antes de qualquer communication action para parecer humano
- **Perguntas yes/no** em SMS medem engajamento e alimentam proximo If/Else
- **Max 2-3 emails/dia** por contato somando todas as automacoes
- WhatsApp exige templates pre-aprovados pela Meta para mensagens iniciadas pelo business

---

## Send Data (Premium)

Estas acoes contam como execucoes premium e impactam seu plano.

### Custom Webhook

- Metodos: POST, GET, PUT, DELETE
- Auth: Basic, Bearer, API Key, OAuth2
- Retry com exponential backoff
- **Dica**: Usar para integrar com n8n, Make, APIs externas

### Google Sheets

- Criar linha
- Buscar linha
- Deletar linha
- Auth via OAuth

### Slack

- Enviar mensagem para usuario
- Enviar mensagem para canal
- Auth via OAuth

---

## IVR Actions

Para workflows de telefonia (trigger: Start IVR):

| Action | Detalhes |
|--------|----------|
| Gather Input on Call | DTMF, stop-after 5-30s, loops, match conditions |
| Say/Play Message | TTS ou audio pre-gravado, voz masc/fem, loops |
| Connect Call | Ate 10 numeros, timeout 1-600s, voicemail detection, recording |
| End Call | Com mensagem opcional |
| Record Voicemail | Silence detection 5s, max 14.400s (4h) |

---

## Workflow AI Actions

| Action | Descricao | Uso Recomendado |
|--------|-----------|-----------------|
| AI Translate | Traduz texto para outro idioma | Workflows multilinguais |
| AI Summarize | Resume texto longo | Resumir conversas antes de handoff |
| AI Intent Detection | Detecta intencao do contato | Routing por intencao |
| AI Decision Maker | Roteia contatos entre branches automaticamente | Substituir If/Else complexo |
| Send Email using AI | Email gerado por AI | Personalizacao em escala |

### AI Decision Maker

Roteia contatos automaticamente com base em:
- Engagement score
- Company size
- Comportamento/historico

Sem configuracao manual de condicoes — a AI decide o melhor branch. Usar quando as condicoes sao complexas demais para If/Else manual.

---

## Integration Actions

### ClickUp (16+ actions)

Create/Update/Delete Task, Post Comment, Post Attachment, Find Task, Create Space, Create Folder, Create List, Create Document, Edit Document, Find Document, Find User.

### Airtable (4 actions)

Find Record, Create Record, Update Record, Delete Record.

### Google Contact

Create Contact, Update Contact.

---

## Categorias Adicionais

Actions identificados na documentacao mas sem detalhamento completo:

- **Opportunity Actions** — criar/mover/atualizar opportunities no pipeline
- **Company Actions** — CRUD de empresas (B2B)
- **Custom Object Actions** — manipular objetos customizados
- **Appointments Actions** — criar/cancelar agendamentos + Create Appointment Note (novo)
- **Payments Actions** — criar invoices, processar pagamentos
- **Affiliate Actions** — gerenciar afiliados
- **Memberships & Communities** — Grant Leaderboard Points (novo), gerenciar acesso
- **Social Media Communication** — postar em redes sociais
- **Documents & Contracts** — enviar/gerenciar documentos

> Para detalhes atualizados de qualquer action, consultar o NotebookLM.
