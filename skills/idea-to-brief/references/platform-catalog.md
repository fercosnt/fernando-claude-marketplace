# Catalogo de Plataformas

Referencia para a Fase 6 do idea-to-brief. Usado para avaliar fit entre a ideia e as plataformas disponiveis.

## Como detectar plataformas do usuario

| Sinal | Onde encontrar | Plataforma indicada |
|-------|---------------|---------------------|
| Ambiente Claude Code ativo | Contexto da sessao | Claude Code |
| MCP servers conectados | Listar tools disponiveis | Varia (Notion, Supabase, etc.) |
| `package.json` com `@supabase/supabase-js` | `package.json` | Supabase |
| `package.json` com `next` | `package.json` | Next.js |
| `vercel.json` presente | Raiz do projeto | Vercel |
| `docker-compose.yml` presente | Raiz do projeto | Docker |
| Diretorio `GoHighLevel-MCP` | Estrutura de pastas | GoHighLevel |
| CLAUDE.md menciona n8n | CLAUDE.md | n8n |
| CLAUDE.md menciona Telegram | CLAUDE.md | Telegram |
| `.github/workflows/` presente | Estrutura de pastas | GitHub Actions |

## Plataformas e capacidades

### Claude Code (Skills)
- **Forca**: Automacao de codigo, CLI, agentes inteligentes
- **Melhor para**: Skills, ferramentas dev, agentes, automacao de workflows de desenvolvimento
- **Limitacoes**: Sem UI grafica nativa, depende de terminal
- **Quando recomendar**: Ideia envolve processamento de texto, codigo, pesquisa, ou workflow de desenvolvimento

### n8n
- **Forca**: Workflows visuais, 400+ integracoes, self-hosted
- **Melhor para**: Automacoes, webhooks, pipelines de dados, integracoes entre servicos
- **Limitacoes**: Logica complexa e verbosa, sem frontend nativo
- **Quando recomendar**: Ideia envolve conectar servicos, automacao de processos, webhooks

### Notion
- **Forca**: Documentacao, bases de dados relacionais, wikis, colaboracao
- **Melhor para**: Gestao de conhecimento, dashboards leves, bases de dados simples
- **Limitacoes**: Nao e banco de dados real, sem logica backend, lento para grandes volumes
- **Quando recomendar**: Ideia envolve organizacao de informacao, documentacao, gestao leve

### Supabase
- **Forca**: Postgres, auth, realtime, storage, edge functions
- **Melhor para**: Apps com dados, multi-tenant, auth, APIs REST/GraphQL
- **Limitacoes**: Vendor lock-in leve, edge functions em Deno
- **Quando recomendar**: Ideia precisa de banco de dados, autenticacao, ou API

### Vercel
- **Forca**: Deploy zero-config, CDN global, serverless functions
- **Melhor para**: Apps web, APIs, frontends React/Next.js
- **Limitacoes**: Serverless cold starts, limites de execucao
- **Quando recomendar**: Ideia precisa de deploy rapido de frontend ou API

### Next.js
- **Forca**: Framework full-stack, SSR/SSG, App Router, API Routes
- **Melhor para**: Apps web completos, dashboards, plataformas SaaS
- **Limitacoes**: Complexidade para coisas simples, curva de aprendizado
- **Quando recomendar**: Ideia e um app web com frontend + backend

### GoHighLevel
- **Forca**: CRM completo, automacao marketing, funnels, calendar
- **Melhor para**: Gestao de clientes, marketing digital, agendamento
- **Limitacoes**: API complexa, custos de licenca
- **Quando recomendar**: Ideia envolve CRM, marketing, ou gestao de leads

### GitHub
- **Forca**: Versionamento, CI/CD, colaboracao, issues, Actions
- **Melhor para**: Qualquer projeto de codigo, CI/CD, open source
- **Limitacoes**: Nao e plataforma de execucao
- **Quando recomendar**: Qualquer projeto que envolva codigo

### Telegram (Bots)
- **Forca**: API simples, notificacoes push, interface conversacional
- **Melhor para**: Alertas, interfaces conversacionais simples, notificacoes
- **Limitacoes**: Sem UI rica, dependencia de plataforma terceira
- **Quando recomendar**: Ideia precisa de notificacoes ou interface conversacional leve

### Make/Zapier
- **Forca**: No-code, milhares de integracoes, setup rapido
- **Melhor para**: Integracoes simples, usuarios nao-tecnicos, prototipagem
- **Limitacoes**: Caro em escala, logica limitada, vendor lock-in
- **Quando recomendar**: Ideia e simples, usuario nao e tecnico, ou para prototipar

## Matriz de decisao por tipo de ideia

| Tipo de ideia | Plataforma primaria | Alternativa |
|---------------|--------------------|-----------  |
| Skill / ferramenta dev | Claude Code | — |
| Automacao de processo | n8n | Make/Zapier |
| App web com dados | Next.js + Supabase | — |
| Dashboard | Next.js + Supabase | Notion (se simples) |
| Gestao de conhecimento | Notion | Supabase (se complexo) |
| CRM / marketing | GoHighLevel | Supabase custom |
| Bot / notificacoes | Telegram | n8n + Telegram |
| API / backend | Supabase Edge Functions | Next.js API Routes |
| Prompt / agente AI | Claude Code | OpenAI API |

## Como apresentar no brief

```markdown
## 8. Analise de Plataformas

### Plataformas atuais do usuario

| Plataforma | Detectada via | Fit (1-5) | Notas |
|------------|---------------|-----------|-------|
| [nome] | [fonte de deteccao] | [score] | [como ajuda ou limita] |

### Plataformas recomendadas (novas)

| Plataforma | Por que considerar | Esforco de adocao | Beneficio vs existente |
|------------|-------------------|--------------------|-----------------------|
| [nome] | [justificativa] | [Baixo/Medio/Alto] | [comparacao] |

### Recomendacao de stack

**Para abordagem [N]**: [lista de plataformas com justificativa]
```
