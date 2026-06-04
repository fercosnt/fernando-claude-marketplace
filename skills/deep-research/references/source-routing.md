# Source Routing — Mapa de Dominio para Fontes

Este arquivo mapeia dominios detectados para fontes especializadas. O skill principal le este arquivo na Fase 1 para rotear subagentes corretamente.

## Como usar

1. Detecte o dominio do topico (pode ser multiplo)
2. Consulte a tabela abaixo para identificar fontes especializadas
3. Passe as fontes ao subagente Domain-Specific (subagente 6)
4. Ajuste os outros subagentes para incluir queries especificas do dominio

---

## Mapa de Dominios

### Desenvolvimento Web — Frontend

| Dominio | Fontes Especializadas | Queries Sugeridas |
|---------|----------------------|-------------------|
| **React** | react.dev, Vercel blog, Dan Abramov blog, Kent C. Dodds | "react {topico} best practices", "react server components {topico}" |
| **Next.js** | nextjs.org/docs, Vercel blog, Context7 | "next.js app router {topico}", "nextjs 14 {topico}" |
| **Tailwind CSS** | tailwindcss.com/docs, Tailwind UI patterns | "tailwind {topico} pattern", "tailwind best practices" |
| **Vue/Nuxt** | vuejs.org, nuxt.com/docs | "vue 3 {topico}", "nuxt {topico}" |
| **TypeScript** | typescriptlang.org, Matt Pocock blog/videos | "typescript {topico} pattern", "ts strict {topico}" |

### Desenvolvimento Web — Backend

| Dominio | Fontes Especializadas | Queries Sugeridas |
|---------|----------------------|-------------------|
| **Node.js** | nodejs.org/docs, Node.js blog | "node.js {topico}", "express {topico}" |
| **Supabase** | supabase.com/docs, supabase.com/blog, github.com/supabase | "supabase {topico}", "supabase RLS {topico}", "supabase edge functions" |
| **PostgreSQL** | postgresql.org/docs, pganalyze blog, Crunchy Data blog | "postgresql {topico}", "postgres performance {topico}" |
| **APIs REST** | restfulapi.net, swagger.io/docs | "REST API {topico} best practices" |

### Plataformas CRM / SaaS

| Dominio | Fontes Especializadas | Queries Sugeridas |
|---------|----------------------|-------------------|
| **GoHighLevel** | developers.gohighlevel.com, LeadConnector API docs, GHL Ideas board, GHL Facebook groups | "gohighlevel api {topico}", "GHL {topico}", "leadconnector {topico}" |
| **HubSpot** | developers.hubspot.com, HubSpot Academy | "hubspot api {topico}", "hubspot CRM {topico}" |
| **Salesforce** | developer.salesforce.com, Trailhead | "salesforce {topico}", "apex {topico}" |

### Automacao / Workflows

| Dominio | Fontes Especializadas | Queries Sugeridas |
|---------|----------------------|-------------------|
| **n8n** | docs.n8n.io, community.n8n.io, github.com/n8n-io | "n8n {topico}", "n8n workflow {topico}", "n8n community node {topico}" |
| **Zapier** | zapier.com/apps, platform.zapier.com/docs | "zapier {topico}" |
| **Make (Integromat)** | make.com/en/help | "make.com {topico}", "integromat {topico}" |

### IA / LLMs / Agentes

| Dominio | Fontes Especializadas | Queries Sugeridas |
|---------|----------------------|-------------------|
| **Claude Code / Skills** | docs.anthropic.com, github.com/anthropics/skills (99k+ stars), github.com/anthropics/claude-cookbooks, github.com/wanshuiyin/Auto-claude-code-research-in-sleep (ARIS), github.com/K-Dense-AI/claude-scientific-skills, github.com/affaan-m/everything-claude-code | "claude code skill {topico}", "anthropic {topico}", "SKILL.md {topico}" |
| **Prompt Engineering** | docs.anthropic.com/prompt-engineering, learnprompting.org | "prompt engineering {topico}", "system prompt {topico}" |
| **MCP (Model Context Protocol)** | modelcontextprotocol.io, github.com/modelcontextprotocol | "MCP server {topico}", "model context protocol {topico}" |
| **Agent SDK** | docs.anthropic.com/agent-sdk | "claude agent sdk {topico}", "anthropic agent {topico}" |
| **OpenAI** | platform.openai.com/docs | "openai api {topico}", "gpt {topico}" |
| **LangChain** | python.langchain.com/docs, js.langchain.com/docs | "langchain {topico}" |
| **RAG** | blogs de Pinecone, Weaviate, Chroma | "RAG {topico}", "retrieval augmented generation {topico}" |

### Marketing / Ads / Growth

| Dominio | Fontes Especializadas | Queries Sugeridas |
|---------|----------------------|-------------------|
| **Meta Ads** | facebook.com/ads/library, developers.facebook.com | "meta ads {topico}", "facebook ads {topico}" |
| **Google Ads** | ads.google.com/aw/transparency, support.google.com/google-ads | "google ads {topico}" |
| **Copywriting** | copyhackers.com, marketingexamples.com | "copywriting {topico}", "ad copy {topico}" |
| **SEO** | ahrefs.com/blog, moz.com/blog, searchengineland.com | "SEO {topico}", "technical SEO {topico}" |

### Odontologia / Healthcare (Beauty Smile)

| Dominio | Fontes Especializadas | Queries Sugeridas |
|---------|----------------------|-------------------|
| **Procedimentos** | pubmed.ncbi.nlm.nih.gov, scielo.br | "{procedimento} clinical evidence", "{procedimento} meta-analysis" |
| **Marketing clinica** | cardosohealth.com, clinicx blog, clinical marketing blogs | "dental marketing {topico}", "clinic marketing {topico}" |
| **Regulamentacao** | CRO, CFO, ANVISA | "regulamentacao odontologica {topico}", "CFO norma {topico}" |

### DevOps / Infra

| Dominio | Fontes Especializadas | Queries Sugeridas |
|---------|----------------------|-------------------|
| **Vercel** | vercel.com/docs, vercel.com/blog | "vercel {topico}", "vercel deploy {topico}" |
| **Docker** | docs.docker.com, hub.docker.com | "docker {topico}", "dockerfile {topico}" |
| **CI/CD** | docs.github.com/actions, circleci.com/docs | "github actions {topico}", "CI/CD {topico}" |

### Notion / Produtividade

| Dominio | Fontes Especializadas | Queries Sugeridas |
|---------|----------------------|-------------------|
| **Notion** | developers.notion.com, notion.so/templates | "notion {topico}", "notion formula {topico}", "notion database {topico}" |
| **Produtividade** | fortelabs.com (Tiago Forte), Ali Abdaal | "productivity system {topico}" |

---

## Deteccao Automatica de Dominio

### Sinais no topico do usuario

| Palavra-chave | Dominio detectado |
|---------------|-------------------|
| skill, SKILL.md, claude code, prompt | IA / Claude Code / Skills |
| GHL, GoHighLevel, CRM, lead, pipeline | GoHighLevel |
| n8n, workflow, automacao, webhook | Automacao |
| supabase, RLS, postgres, migration | Supabase |
| next, react, tailwind, componente | Desenvolvimento Frontend |
| ads, campanha, criativo, copy, trafego | Marketing / Ads |
| clinica, tratamento, paciente, odonto | Odontologia / Healthcare |
| notion, database, formula, wiki | Notion |
| deploy, docker, vercel, CI/CD | DevOps |
| MCP, server, tool, protocol | MCP |
| RAG, embedding, vector, knowledge base | IA / RAG |

### Sinais no contexto (CLAUDE.md, projeto)

- `package.json` com `@supabase/supabase-js` → Supabase
- `package.json` com `next` → Next.js
- `package.json` com `@modelcontextprotocol/sdk` → MCP
- Diretorio `skills/` presente → Claude Code / Skills
- Mencao a GoHighLevel no CLAUDE.md → GHL
- Mencao a n8n no CLAUDE.md → Automacao
- Mencao a Beauty Smile → Odontologia + Marketing clinica

### Multiplos dominios

Um topico pode pertencer a multiplos dominios. Exemplo:
- "Criar skill de automacao n8n para GHL" → Skills + Automacao + GHL
- "Dashboard Next.js com Supabase" → Frontend + Supabase
- "Ads para clinica odontologica" → Marketing + Odontologia

Neste caso, combine as fontes de todos os dominios relevantes.
