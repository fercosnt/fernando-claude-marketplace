# Stack Tecnologico Padrao — Fernando

Stack consistente entre projetos, zero decisao repetida.

## Core

| Camada | Tecnologia | Versao | Justificativa |
|--------|-----------|--------|---------------|
| Framework | Next.js (App Router) | 14+ | SSR, API Routes, ecossistema React |
| Linguagem | TypeScript | Strict mode, sem `any` | Tipagem forte previne bugs |
| UI | @beautysmile/design-system | 0.1.0 | Componentes proprios, identidade BS |
| Estilizacao | Tailwind CSS | 4.x | Utility-first, sem CSS customizado |
| Componentes Base | Radix UI | Multiplos | Acessibilidade, headless |
| Auth | Supabase Auth | Email+Senha | Integracao nativa com RLS |
| Banco | Supabase PostgreSQL | — | Views SQL, functions, RLS |
| Multi-tenancy | Row Level Security (RLS) | — | Isolamento no banco |
| Graficos | Recharts | 3.x | React, KPIs, dashboards |
| Validacao | Zod + React Hook Form | — | Backend + formularios |
| Icons | Lucide React | — | Consistente |
| Deploy | Vercel | — | Zero config, preview deploys |
| Automacao | n8n (self-hosted Hostinger) | — | Sem limite, retry, logs |
| Notificacoes | Telegram via n8n | — | Integracao simples |
| Dev Tools | Cursor + Claude Code | — | AI-accelerated |

## Testes

| Tipo | Ferramenta | Script |
|------|-----------|--------|
| Unitarios | Jest + Testing Library | `npm test` |
| E2E | Playwright | `npm run test:e2e` |
| Integracao | Jest customizado | Testes de auth, RLS |

## Dependencias Recorrentes (package.json)

```
# Core
next ^14.x
react ^18.3.x
typescript (strict)

# Supabase
@supabase/supabase-js ^2.84.x
@supabase/ssr ^0.7.x

# UI
@radix-ui/react-* (dialog, checkbox, label, select, dropdown-menu, slot)
class-variance-authority ^0.7.x
clsx ^2.x
tailwind-merge ^3.x
lucide-react ^0.554.x
recharts ^3.x

# Formularios
react-hook-form ^7.x
@hookform/resolvers ^5.x
zod ^4.x
```

## Supabase Clients (SEMPRE 4 arquivos)

| Arquivo | Funcao | Quando |
|---------|--------|--------|
| `lib/supabase/client.ts` | `createBrowserClient()` | Componentes client-side |
| `lib/supabase/server.ts` | `createServerClient()` | Server Components, API Routes |
| `lib/supabase/middleware.ts` | Middleware de auth | Refresh sessao, protecao de rotas |
| `lib/supabase/admin.ts` | Service role client | Operacoes privilegiadas |

## RLS Helper Functions

```sql
CREATE OR REPLACE FUNCTION auth_tenant_id() RETURNS UUID AS $$
    SELECT [coluna_tenant] FROM profiles WHERE id = auth.uid()
$$ LANGUAGE sql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION is_admin() RETURNS BOOLEAN AS $$
    SELECT role = 'admin' FROM profiles WHERE id = auth.uid()
$$ LANGUAGE sql SECURITY DEFINER;
```

## Convencoes SQL

- PKs: `UUID DEFAULT gen_random_uuid()`
- Timestamps: `created_at/updated_at TIMESTAMPTZ NOT NULL DEFAULT now()`
- Soft delete: `ativo BOOLEAN NOT NULL DEFAULT true`
- Monetarios: `DECIMAL(12,2)` — NUNCA float
- Percentuais: `DECIMAL(5,2)`
- Enums: `CREATE TYPE status_xxx AS ENUM (...)`
- Indexes compostos: `(tenant_id, mes_referencia)` minimo
- Triggers: `update_updated_at()` automatico
- Views: para agregacoes de dashboard
- Migracoes: `001_nome.sql`, `002_nome.sql`

## API Routes Pattern

```typescript
// Sucesso
return NextResponse.json({ data: resultado }, { status: 200 })  // GET/PUT
return NextResponse.json({ data: criado }, { status: 201 })      // POST
return new NextResponse(null, { status: 204 })                   // DELETE

// Erro
return NextResponse.json({ error: "Mensagem clara" }, { status: 4xx })
```

## Padroes de Implementacao

- Dashboards: KPIs em cards no topo + graficos + drill-down
- Formularios: React Hook Form + Zod + design system
- Tabelas: filtros, paginacao, export
- Modais: Dialog para CRUD
- Atomicidade vertical: SQL + API + UI + teste JUNTOS

## n8n Workflows

- Padrao webhook: frontend -> API Route -> n8n webhook -> processamento -> Telegram
- Upload: staging table antes de tabelas definitivas
- Cron: processamento automatico diario
- Notificacoes: Telegram para eventos criticos

## O Que NAO Usa (Deliberadamente)

- CommonJS (tudo ES modules)
- CSS modules ou styled-components (Tailwind only)
- ORMs (Prisma, Drizzle) — Supabase client direto
- OAuth complexo (email+senha suficiente)
- Microservicos (monolito Next.js + n8n)
- Docker em dev (Supabase CLI + Vercel dev)
- pnpm/yarn (npm padrao)
- Vitest (Jest padrao)
