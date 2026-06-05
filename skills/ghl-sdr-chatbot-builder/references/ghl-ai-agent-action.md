# GHL AI Agent Action (Workflow Premium)

## Quando carregar
Quando o usuario quer que o bot/agente **execute acoes autonomas dentro de um workflow** (mover pipeline, enriquecer lead, preencher campos, nudge de deal parado) em vez de so conversar. Diferente do Conversation AI bot: a AI Agent action vive no Workflow Builder e roda como passo do workflow.

> Para construcao profunda de workflows com AI Agent / Agent Studio, a skill `ghl-workflow-expert` cobre os detalhes de mecanica. Este reference foca no uso/custo para o SDR bot.

---

## 1. O que e a AI Agent action

Uma acao de workflow **premium** que executa multiplas ferramentas (tools) a partir de uma instrucao em linguagem natural — **sem branches hard-coded**. Voce descreve o objetivo; o agente decide quais tools chamar e em que ordem.

**Templates prontos uteis para SDR:**
- **Form Lead Follow Up** — segue lead que preencheu formulario
- **Lead Research & Enrichment** — enriquece dados do lead (web search + update fields)
- **Stale Deal Nudge** — reativa deal parado no pipeline
- **Pipeline Tracker** — move o lead no pipeline e preenche campos autonomamente

Botao **"Enhance Prompt"**: estrutura uma instrucao casual em um prompt bem-formado.

---

## 2. Billing — o que custa

| Categoria | Exemplos | Custo |
|-----------|----------|-------|
| **Standard tools** | Send SMS/Email, Update Contact Field, Add/Remove Tag, Create Task, Update Opportunity/Pipeline, acesso ao transcript | **Sem custo extra** |
| **Premium tools** | Decision Maker, Intent Detection, ClickUp/Airtable/Notion | **$0.01 por execucao, cada** |
| **Internal tools** | Date Calculator, Web Search, KB Search, MCP, API Call | **Nao contam** para o limite de tools |

- **Limite: maximo 10 tools por agente** (internal excluidas da contagem).
- **Tokens (recomendado GPT-5 Mini para SDR):** ~$0.25/1M input + $2.00/1M output. Uma interacao SDR tipica (~2k tokens) sem premium tool custa **fracao de centavo**.
- **AI Studio gratuito ate 1/set/2026** — depois disso, validar o pricing vigente.

**Implicacao pratica:** para qualificacao SDR, manter o agente em standard + internal tools deixa o custo desprezivel. Premium tools (Decision Maker, Intent Detection) so quando o ganho justificar os $0.01/exec.

---

## 3. AI Agent action vs Conversation AI bot

| | Conversation AI bot | AI Agent action |
|--|---------------------|-----------------|
| Onde vive | AI Agents → Conversation AI | Workflow Builder (passo do workflow) |
| Funcao | Conversa com o lead | Executa acoes no CRM autonomamente |
| Dispara | Mensagem inbound | Trigger de workflow |
| Uso SDR | Qualificar via chat | Enriquecer lead, mover pipeline, nudge pos-qualificacao |

Os dois se combinam: o **bot qualifica na conversa**; a **AI Agent action cuida do back-office** (enriquecimento, movimentacao de pipeline, follow-up de deal parado) sem o lead ver.

---

## 4. "Let AI decide"

- Configuravel **global** (o agente decide tudo) ou **por campo** (so campos especificos ficam a cargo do agente).
- Para SDR: deixar campos criticos de qualificacao sob controle do agente, mas manter campos de compliance (consentimento, opt-out) deterministicos.

---

## Fontes
- GHL Help: AI Agent Workflow Action (https://help.gohighlevel.com/support/solutions/articles/155000007600)
- Skill irma para mecanica de workflow: `ghl-workflow-expert`
