# AI Agent Action — Guia Completo (Virada Agentic GHL)

> A action **AI Agent** (categoria "Workflow AI", premium, lancada abr/2026, beta) substitui arvores de If/Else por um **agente autonomo configurado por prompt**: voce escreve instrucoes em linguagem natural, da ate **10 tools**, e o agente decide quais usar e em que ordem para completar a tarefa. E a maior mudanca de paradigma do GHL desde o Advanced Builder: de "canvas com branches" para "AI employee".

## Indice
1. [As 3 formas de AI Agent](#as-3-formas-de-ai-agent)
2. [Configuracao da action](#configuracao-da-action-campos-exatos)
3. [Catalogo de tools (limite 10)](#catalogo-de-tools-limite-10)
4. [Conexoes MCP](#conexoes-mcp)
5. [Output e branching JSON](#output-e-branching)
6. [Modelos e billing](#modelos-e-billing)
7. [Observabilidade](#observabilidade)
8. [Limites e restricoes](#limites-e-restricoes)
9. [Prompt engineering C-T-T-C](#prompt-engineering-c-t-t-c)
10. [Templates prontos](#templates-prontos)
11. [Pitfalls reais](#pitfalls-reais)
12. [Caso end-to-end](#caso-end-to-end-roofing)
13. [Gaps documentais](#gaps-documentais)

---

## As 3 formas de AI Agent

Nao confundir — sao tres coisas distintas com pre-requisitos diferentes:

| | **AI Agent (action inline)** | **Invoke Agent Studio Agent** | **Agent Studio AI Agent Node** |
|---|---|---|---|
| O que e | Action nativa no workflow, configurada na hora | Action que chama um agente publicado no Agent Studio | Node dentro do canvas separado do Agent Studio |
| Escopo | Single-agent, 1 step | Invoca agente reutilizavel | Orquestracao multi-agente (AI + rule-based) |
| Pre-requisito | Premium actions habilitadas | Agente em **Production** + AI Employee add-on | Agent Studio (plataforma separada) |
| Timeout | nao documentado | **60s hard limit** | — |
| Reuso | Nao (config vive no workflow) | Sim (1 agente, N workflows) | Sim |
| Uso ideal | Automacoes diretas task-based | Mesmo agente em 3+ workflows | Pipelines multi-step AI + deterministico |

**Regra pratica:** comece com **AI Agent inline**. Migre para **Invoke Agent Studio Agent** quando o mesmo agente for reutilizado em 3+ workflows ou precisar de orquestracao multi-agente. O agente-alvo do Invoke deve ter sido buildado com o trigger "Workflows" e estar em Production (Draft nao e acessivel).

---

## Configuracao da action (campos exatos)

| Campo | Detalhe |
|-------|---------|
| **Action Name** | Label customizavel (default "AI Agent") — renomear por use case |
| **Template** | Seletor que pre-preenche Instructions + Tools, ou "Build Your Own". Alguns templates exigem trigger especifico (ficam bloqueados ate o trigger correto ser adicionado) |
| **Instructions** | Campo principal = system prompt. Rich text. Botao **"Enhance Prompt"** reestrutura texto solto em prompt detalhado com edge cases (reversivel) |
| **Model** | Dropdown de modelo LLM (obrigatorio) |
| **Tools** | "+ Add Tool" com busca; cada tool tem painel de config proprio |
| **Conversation Memory** (advanced) | Off por default. ON = mantem rolling summary das execucoes anteriores do MESMO contato naquele step (continuidade multi-toque). Custo oculto: aumenta tokens de input |
| **Output Format** (advanced) | None / Text / JSON (ver secao branching) |

**Contexto que o agente recebe automaticamente (sem setup):**
- **Conversation History** cross-channel (SMS, Email, WhatsApp, Instagram, FB Messenger, TikTok) — recuperado quando o agente julga relevante
- **Call Transcripts** — ativadas mencionando nas Instructions (ex: "use the last call transcript to identify objections")

---

## Catalogo de tools (limite 10)

**Limite: 10 tools por agente.** Tools internas (Date Calculator, Math Operations) NAO contam. O catalogo cresce continuamente (produto novo) — esta lista combina doc oficial + demos ao vivo:

| Categoria | Tools |
|-----------|-------|
| **Contato/CRM** | Create Contact, Find Contact, Update Contact Fields (toggle "let AI decide all field values" por campo), Add Tag, Add to Notes, Add a Task |
| **Oportunidade** | Add to Opportunities, Find Opportunities, Update Opportunities (move stage por prompt) |
| **Comunicacao** | Send SMS *(standard, sem charge premium)*, Send Email, Instagram DMs, Send Internal Notifications |
| **Agendamento** | Link to Appointment Calendars (create appointment / generate one-time booking link) |
| **Financeiro** | Link to Invoices, Send Estimates, Send Recurring Invoices, Documents & Contracts |
| **Knowledge** | Search Knowledge Base (query Static ou Dynamic/AI-decides; N chunks; pull-only para economizar contexto) |
| **Custom Data** | Update Custom Value (campo fixo + valor AI, ou AI escolhe campo+valor) |
| **Workflow** | Add to Existing Workflows |
| **Externas** | **MCP Tool** (ver secao MCP), integracoes ClickUp/Asana/Notion *(premium)*, Send Custom Webhooks |
| **Internas (nao contam)** | Date Calculator, Math Operations |

> Com teto de 10, escolha estrategica: nao adicione tools "por garantia". Cada tool extra dilui a atencao do modelo e aumenta a chance de uso indevido. Knowledge Base puxa so snippets recuperados, nunca docs inteiros.

---

## Conexoes MCP

MCP (Model Context Protocol) como tool nativa foi adicionado em abr/2026. Habilitar via **Agency Settings → Labs**.

### Setup passo a passo
1. Abrir o no AI Agent → **Add Tools** → aba **MCP**
2. **Add Connection**:
   - **Connection Name** — identificador interno
   - **Server URL** — endpoint do MCP server
   - **Transport Type** — HTTP Streamable ou SSE
   - **Auth** — None / Bearer Token / API Key / OAuth2 / Custom Header
3. **Test Connection** → descoberta automatica das tools do servidor
4. Habilitar/desabilitar tools especificas por agente (controle granular)

### Servidores
- **Nativos built-in:** Airtable, Basecamp, Monday.com, Notion, Google Forms, Google Contacts, Open Router, Manus + **Exa** (web search), **Tavily** (search + page extraction), **Browserbase** (browser automation)
- **Externos via URL:** **Zapier MCP** (8.000+ tools, Bearer), **Make MCP**, **Composio** (500+ apps: ClickUp, Notion, GitHub, Slack — Bearer), **custom** (qualquer HTTP/SSE)

Apos conectar, o agente descobre as tools pelo protocolo e decide qual usar — sem config manual por acao. **O limite de 10 tools vale para MCP + nativas combinadas.**

---

## Output e branching

| Output Format | Comportamento |
|---------------|---------------|
| **None** | Executa acoes, sem output estruturado downstream |
| **Text** | Resposta livre + campo "Output Description" para descrever o conteudo esperado |
| **JSON** | Schema definido (propriedades `name` / `type` / `description`). Use quando steps seguintes precisam referenciar valores especificos |

**Padrao recomendado (melhor dos dois mundos):** AI Agent retorna JSON tipo `{"qualified": true, "score": 85}` → **If/Else downstream faz o branching deterministico**. O agente raciocina, o If/Else roteia. Combina flexibilidade da AI com debugabilidade do branching.

> A sintaxe exata da variavel para acessar campos do JSON no If/Else nao esta documentada (provavel `{{ai_agent_output.campo}}`). Tambem existe "Store Output As" → salva resposta completa como custom value (via Invoke Agent action).

---

## Modelos e billing

### Modelos
| Modelo (label GHL) | Quando |
|---|---|
| **GPT-5.2 (Low thinking)** | Default recomendado — equilibrio qualidade/velocidade |
| GPT-5.2 (Higher thinking) | Logica complexa, decisoes multi-step |
| GPT-5 Nano | Tarefas simples, prioriza velocidade/custo |

> Os labels "GPT-5.x" sao nomenclatura interna do GHL e nao necessariamente correspondem a modelos OpenAI homonimos. (No produto *Conversation AI* — distinto — ha tambem Claude Sonnet/Opus selecionaveis.)

### Custo
```
Custo = (tokens totais x taxa do modelo) + (execucoes de premium tools x taxa por premium action)
```
- **Workflow AI action premium:** ~**$0.01/execucao**
- **Tools standard** (Send SMS, Add Tag, Update Field): sem charge premium adicional
- **MCP Tool:** sem charge proprio alem de tokens
- **Medido ao vivo:** **~$0.02** para fluxo completo (form → SMS + email + tag + oportunidade + booking link)

### Planos AI Employee
| Plano | Custo | Inclui |
|---|---|---|
| Pay-per-use | so tokens | sem mensalidade |
| AI Employee Growth | $50/mes/subconta | 1.000 respostas Conversation AI + 100 min Voice AI |
| **AI Employee Unlimited** | **$97/mes/subconta** | Conversation AI + Reviews + Content + Funnel AI ilimitados (fair use) |

> **Break-even:** comece o cliente no **pay-per-use**, migre para flat **$97** quando passar de **40-60 interacoes/mes**. Voice AI permanece pay-per-use mesmo no $97.

---

## Observabilidade

**Execution Logs → selecionar execucao do AI Agent.** O trace mostra:
1. **Agent Input** — input completo recebido
2. **LLM** — cada chamada ao modelo (raciocinio de cada step)
3. **Tool Executions** — nome da tool, tempo, status sucesso/falha

Suporta table view e raw JSON; token usage visivel por execucao. **Limitacao:** logs sao post-hoc (sem alertas/streaming) e mostram tokens, nao o "porque" da decisao — debugabilidade menor que If/Else deterministico.

---

## Limites e restricoes

| Item | Valor |
|---|---|
| Max tools por agente | **10** (internas nao contam) |
| Timeout Invoke Agent Studio | **60s** |
| Timeout AI Agent inline | nao documentado |
| Max instruction length / context window | nao documentado |

**O agente NAO pode:** acessar agentes Studio em Draft (so Production); auto-testar workflows (revisao manual obrigatoria); ler docs inteiros da KB (so snippets recuperados). Export/import de agents cross-subaccount esta no roadmap.

---

## Prompt engineering C-T-T-C

GHL recomenda estruturar as Instructions como **Context · Task · Tone · Constraints**:

- **Context (Role):** quem o agente e + negocio + cenario. *"You are a friendly appointment scheduler for Sunrise Dental, a family practice in Austin."*
- **Task:** o que fazer, passo a passo, objetivos. *"Answer questions, collect name + preferred time, book on the calendar."*
- **Tone:** Conversational / Empathetic / Friendly / Professional
- **Constraints:** limites explicitos com "do not" — **omitir constraints e o erro #1**; sem elas o agente inventa politicas e responde fora do escopo

**Regras de escrita:**
- Contexto enxuto (>100-200 palavras dilui importancia)
- Delimitadores (`#`, `>`, `"""`) para demarcar regras criticas
- Repetir instrucoes criticas em multiplas secoes (redundancia intencional aumenta compliance)
- Exemplos concretos > descricoes abstratas
- Roteamento de pipeline como regras `if/then` explicitas no proprio prompt

**Constraints obrigatorias (anti excesso-de-confianca) — sempre incluir alguma forma destas:**
- "Do NOT confirm services, prices, or availability you cannot verify with a tool."
- "If you are unsure or the request is outside your scope, hand off to a human instead of guessing."
- "Only state policies explicitly provided in these instructions or the knowledge base."
- "Never invent appointment times — only offer slots returned by the calendar tool."

> **Padrao "pre-construir no Claude/ChatGPT":** copie o template de prompt do GHL → personalize no Claude/ChatGPT com o brand profile da marca → cole de volta nas Instructions. Alternativa nativa: botao **Enhance Prompt**. Ver `assets/templates/ai-agent-prompt-template.md` para o esqueleto preenchivel.

---

## Templates prontos

~12-13 templates oficiais (alguns exigem trigger especifico):

1. **Form Lead Follow-Up** — agradece, atribui dono, cria oportunidade, SMS+email com booking link (so primeira resposta)
2. **No-Show Appointment Recovery** — SMS+email, rotacao de 3 abordagens, rebooking link
3. **Facebook Lead Nurturing** — engajamento imediato + enrichment + oportunidade
4. **Lead Pipeline Tracker (uses Memory)** — check-ins periodicos por stage com Conversation Memory
5. **Stale Deal Nudge Agent** — high-value → email+SMS+notify+task; standard → SMS+notify
6. **Lead Research & Enrichment** — pesquisa internet (MCP), enrichment, scoring, oportunidade
7. **New Appointment: Enrich & Confirm** — enrichment + confirmacao + brief pre-reuniao
8. **Quiz Lead Scoring & Routing** — le scores, segmenta hot/warm/cold, roteia
9. **Call Transcript Summary & Action Items** — sumariza call, extrai acoes, cria task
10. **Task Creation from Won Deals** — cria tasks em ClickUp/Asana, notifica
11. **Instagram/Facebook Comment-to-DM** — DM personalizada por contexto do comentario
12. **Objection / Billing Question Handler** — acknowledge + reframe + escalacao

---

## Pitfalls reais

- **Excesso de confianca = risco #1:** o agente responde com seguranca temas fora do escopo (servico inexistente, preco errado, disponibilidade nao verificada). Caso real: AI confirmou servico que a empresa nao oferecia → recuperacao manual + gift card $200. **Mitigacao:** handoff triggers explicitos + constraints "do not" fortes
- **Performance cai em high-ticket:** booking 65-72% em servicos simples vs **31%** em high-ticket ($15k+). Hibrido (AI <60s + handoff humano apos 3 trocas) → +40% em high-ticket
- **Auto mode cedo demais:** antes de ~90% acuracia no modo Suggestive, Auto cria respostas confusas. Revisar 2-4 semanas antes de ligar Auto
- **Estimativa de valor e humana:** o bot nao sabe precificar (ex: orcamento de telhado) — transicao de stage que depende de valor fica semi-manual, com **trigger separado** ("Estimate Status = Accepted" → outro workflow muda o stage)
- **Bug do AI Builder:** workflow gerado nao salva na pasta escolhida (cai em "recent"); custom values referenciados como placeholder mas **NAO criados** no CRM — criar manualmente
- **Conversation Memory tem custo oculto** (carrega historico → mais tokens)
- **Conflito de forms:** ativar novo workflow sem desativar forms/automacoes antigas gera execucao dupla

---

## Caso end-to-end: roofing

Trigger Facebook Lead Form → AI Agent (tools: Send SMS + Update Opportunity + Create Appointment "let AI decide"). Pipeline de 6 stages criado **manualmente** antes: Facebook Lead → Contacted → Qualified → Appointment Scheduled → Estimate Completed → Lost.

Prompt (gerado no ChatGPT) incluiu **pipeline movements como regras if/then**:
> "If lead responds → Contacted; if qualified → Qualified; if appointment booked → Appointment Scheduled; if no response → 6-day follow-up then Lost."

**Licao:** o pipeline e criado a mao; o agente so o **movimenta**. Stages que dependem de input humano (valor do estimate) precisam de trigger separado.

---

## Gaps documentais

- Sintaxe de merge field nas Instructions e de acesso ao JSON output no If/Else
- Timeout do AI Agent inline; max instruction length; context window por modelo
- Taxas de token por modelo (billing exige login)
- Catalogo exaustivo de tools (cresce continuamente)
- Retencao do Conversation Memory

> Para qualquer duvida nao coberta aqui, consultar o NotebookLM `307b88b8` via `/notebooklm`.
