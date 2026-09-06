# Templates CLAUDE.md por Tipo de Projeto

## 1. Full-Stack Web (Next.js + Supabase) — Template Padrao

```markdown
# [Nome do Projeto]

[Uma frase: o que e, stack, problema que resolve]
Stack: Next.js 14 (App Router) + Supabase + TypeScript + Tailwind CSS

## REGRAS INVIOLAVEIS

- RLS ativo em TODAS as tabelas multi-tenant — isolamento no banco, nao no codigo
- Valores monetarios: DECIMAL(12,2) — float causa erros de arredondamento
- Validar TODOS os inputs no backend com Zod — frontend valida UX, backend valida seguranca
- Use variaveis de ambiente para secrets (.env) — zero hardcode
- Rode testes antes de considerar trabalho completo

## Comandos Essenciais

- `npm run dev` — Dev server (porta 3000)
- `npm run build` — Build de producao
- `npm test` — Testes Jest
- `npm run lint` — ESLint + TypeScript check
- `npx supabase db reset` — Reset banco local
- `npx supabase migration new <nome>` — Nova migracao SQL

## Arquitetura

app/
├── (auth)/          # Login, signup, reset
├── (admin)/         # Layout admin (acesso total)
├── ([role])/        # Layout por role (filtrado por RLS)
├── api/             # API Routes
└── layout.tsx
components/          # Componentes GLOBAIS compartilhados
lib/supabase/        # 4 clients: client.ts, server.ts, middleware.ts, admin.ts
lib/schemas/         # Zod schemas
supabase/migrations/ # Schema SQL versionado

## Code Style

- TypeScript strict, sem `any` — erros de tipo previnem bugs
- ES modules (import/export) em todo o projeto
- Named exports apenas
- Componentes funcionais com React Hooks
- Tailwind para estilos, @beautysmile/design-system para UI

## Supabase

- 4 clients distintos: NUNCA misture client.ts com server.ts
- RLS: `is_admin()` + `auth_tenant_id()` em todas as tabelas com tenant
- Admin cria contas, sem self-service
- Schema detalhado: @supabase/migrations/

## Gotchas

- Supabase RLS exige SECURITY DEFINER nas funcoes helper
- Formato BR "14.450,00" converter para 14450.00 antes do banco
- Dados de dashboard: ler de tabelas pre-calculadas, nao queries em tempo real
- Componentes especificos de pagina ficam em app/[pagina]/components/

## Verificacao Antes de Concluir

- [ ] `npm test` passa
- [ ] `npm run build` funciona
- [ ] `npm run lint` sem erros
- [ ] RLS aplicado em novas tabelas
- [ ] Inputs validados com Zod no backend
- [ ] Migracao SQL criada para mudancas de schema
```

---

## 2. MCP Server

```markdown
# [Nome] MCP Server

[Descricao do server e integracao]
Stack: Node.js + TypeScript + @modelcontextprotocol/sdk

## Comandos

- `npm run build` — Compilar TypeScript
- `npm run dev` — Dev com hot reload
- `npm test` — Testes
- `npm start` — Start stdio server
- `npm run start:http` — Start HTTP server

## Arquitetura

src/
├── clients/     # API client implementations
├── tools/       # MCP tool implementations
├── types/       # TypeScript types
├── server.ts    # stdio MCP server
└── http-server.ts # HTTP MCP server

## Regras

- Cada tool em arquivo separado em src/tools/
- Types em src/types/ (nunca inline)
- JSDoc em todas as funcoes publicas
- Novos tools: implementar + registrar em server.ts E http-server.ts
- Error handling: retornar mensagens claras, nunca stack traces

## Verificacao

- [ ] `npm test` passa
- [ ] `npm run build` compila
- [ ] Tool registrado nos dois servers (stdio + http)
- [ ] Types exportados
```

---

## 3. Design System

```markdown
# @beautysmile/design-system

Biblioteca de componentes React com estetica glass morphism.
Stack: React + TypeScript + Tailwind + Radix UI + Vite + Storybook

## Comandos

- `npm run dev` — Vite dev server
- `npm run build` — tsc + Vite build
- `npm run storybook` — Storybook (porta 6006)
- `npm run type-check` — tsc --noEmit

## Arquitetura

src/
├── components/glass/   # Glass morphism (identidade visual)
├── components/ui/      # Componentes base (Radix-based)
├── templates/admin/    # Templates admin
├── templates/public/   # Templates publicos
├── tokens/             # Design tokens (colors, typography, spacing)
├── assets/             # Logos, backgrounds
└── utils/              # cn(), use-mobile

## Regras

- Cada componente tem story no Storybook
- Tokens em arquivos separados (nao hardcode cores)
- Exports granulares: /tokens, /components, /templates, /assets
- Acessibilidade: Radix UI como base para todos os componentes interativos
```

---

## 4. N8N/Automacao

```markdown
# [Nome do Projeto] — Workflows n8n

[Descricao dos workflows e integracao]

## Comandos

- n8n: acessar via browser em [URL]
- Supabase: `npx supabase db reset` para reset local

## Workflows

| # | Nome | Trigger | Funcao |
|---|------|---------|--------|
| 1 | [Nome] | Webhook | [Descricao] |
| 2 | [Nome] | Cron | [Descricao] |

## Regras

- Code nodes: retornar `[{json: {...}}]` sempre
- Expressions: usar `{{ $json.campo }}` para acessar dados
- Error handling: retry automatico + notificacao Telegram
- Webhook data: acessar via `$json.body`

## Gotchas

- Expression syntax: `{{ }}` com espacos internos
- Code node JavaScript: `$input`, `$json`, `$node`
- Code node Python: `_input`, `_json`, `_node`
```

---

## 5. Backend API (Node.js/Express)

```markdown
# [Nome] API

[Descricao] — API REST com autenticacao JWT.
Stack: Node.js + TypeScript + Express

## Comandos

- `npm run dev` — Dev com hot-reload
- `npm run build` — Compilar TypeScript
- `npm test` — Testes Jest
- `npm run lint` — ESLint

## Arquitetura

src/
├── routes/       # Endpoints por dominio
├── services/     # Logica de negocio
├── models/       # Modelos de dados
├── middleware/    # Auth, validation, error handling
└── types/        # TypeScript types

## Regras

- Zod para validacao de request/response
- Status codes corretos (201 create, 204 delete)
- Logging estruturado (nunca log PII ou tokens)
- Rate limiting em endpoints publicos
```

---

## 6. Mobile (React Native + Expo)

```markdown
# [Nome] App

[Descricao] — App mobile.
Stack: React Native + Expo + TypeScript

## Comandos

- `npx expo start` — Dev server
- `npm test` — Testes Jest
- `npx expo build:ios` — Build iOS
- `npx expo build:android` — Build Android

## Arquitetura

src/
├── screens/      # Telas da app
├── components/   # Componentes reutilizaveis
├── navigation/   # Configuracao de rotas
├── hooks/        # Custom hooks
└── services/     # API calls + business logic

## Regras

- Expo managed workflow (nao eject)
- React Navigation para rotas
- Testar em iOS E Android sempre
```

---

## 7. Data/ML

```markdown
# [Nome] — Pipeline de Dados

[Descricao do pipeline]
Stack: Python + pandas + [framework ML]

## Comandos

- `pip install -r requirements.txt` — Instalar deps
- `python -m pytest` — Testes
- `python scripts/run_pipeline.py` — Executar pipeline

## Arquitetura

data/
├── raw/          # Dados brutos (nunca modificar)
├── processed/    # Dados processados
└── interim/      # Dados intermediarios
src/
├── data/         # Carga e transformacao
├── models/       # Treinamento e inferencia
└── visualization/ # Graficos e reports

## Regras

- Random seeds fixos para reproducibilidade
- Dados brutos sao imutaveis
- Logs de experimento com parametros completos
```

---

## Notas sobre Templates

1. Todos os templates seguem a estrutura: Nome -> Regras -> Comandos -> Arquitetura -> Code Style -> Gotchas -> Verificacao
2. Adaptar para o projeto real, removendo secoes irrelevantes
3. Stack padrao de Fernando (Next.js + Supabase) e o default — outros templates sao para casos especificos
4. Manter cada template em < 80 linhas quando aplicado
5. Mover detalhes para `.claude/rules/` quando template ficar longo
