# Guia: Geracao de Tarefas a partir do PRD

> Como transformar um PRD em uma lista de tarefas ordenada, atomica e executavel pelo Claude Code.

---

## Principio Central

Cada tarefa deve ser **atomica o suficiente para 1 sessao focada** do Claude Code. Se voce nao consegue descrever a mudanca em 2-3 frases, divida.

> **Por que atomicidade e nao apenas "cabe no contexto"**: o Opus 4.7 tem 1M de context window, entao o limite tecnico quase nunca aperta. O problema real e de **foco e qualidade**: tasks menores (a) reduzem "context rot" (contextos frescos por task), (b) aproveitam a literalidade do 4.7 (instrucoes especificas produzem saida mais precisa), (c) facilitam review humano, (d) permitem commits atomicos, e (e) tornam retries baratos quando algo falha. A regra e de disciplina de engenharia, nao de limite tecnico.

---

## Ordem de Dependencias

Tarefas SEMPRE seguem esta ordem:

```
0. Feature branch
1. Migracao SQL (schema + RLS + indexes)
2. Backend (API Routes + Zod schemas)
3. Frontend (componentes + paginas)
4. Testes (unitarios + integracao)
5. Integracao final + verificacao
```

**Por que esta ordem?**
- Schema define a estrutura de dados — tudo depende dele
- API Routes consomem o schema — precisam da tabela existindo
- Frontend consome as APIs — precisa dos endpoints prontos
- Testes validam tudo — precisam de codigo para testar

---

## Tarefa 0: Feature Branch (SEMPRE)

Toda lista comeca com:

```markdown
- [ ] **Tarefa 0: Criar feature branch**
  - Branch: `feature/[nome-descritivo]`
  - Base: `main`
  - Verificar que main esta atualizado (`git pull`)
```

---

## Formato de Tarefa

```markdown
- [ ] **Tarefa N: [Titulo curto e descritivo]**

  **Descricao**: [2-3 frases explicando O QUE fazer e PORQUÊ]

  **Subtarefas**:
  - [ ] [Passo concreto 1]
  - [ ] [Passo concreto 2]
  - [ ] [Passo concreto 3]

  **Arquivos relevantes**:
  - `caminho/para/arquivo1.ts`
  - `caminho/para/arquivo2.sql`

  **Verificacao**:
  - [ ] [Criterio testavel de que a tarefa esta completa]
  - [ ] [Segundo criterio se necessario]

  **Commit**: `feat: [descricao curta]`
```

---

## Principio de Atomicidade

### Sinais de tarefa grande demais:

- Lista de subtarefas com 7+ itens
- Arquivos relevantes em 4+ diretorios diferentes
- Descricao precisa de mais de 3 frases
- Mistura schema + API + frontend na mesma tarefa

### Como dividir:

```
ANTES (grande demais):
Tarefa 1: Implementar modulo de pagamentos completo

DEPOIS (atomico):
Tarefa 1: Criar migracao SQL para tabela pagamentos
Tarefa 2: Criar Zod schema de validacao de pagamento
Tarefa 3: Implementar API Route GET/POST para pagamentos
Tarefa 4: Implementar API Route PUT/DELETE para pagamentos
Tarefa 5: Criar componente PagamentoForm com React Hook Form
Tarefa 6: Criar componente PagamentoTable com filtros
Tarefa 7: Criar pagina de listagem de pagamentos
Tarefa 8: Criar pagina de novo pagamento
Tarefa 9: Testes unitarios para API de pagamentos
Tarefa 10: Testes de integracao para RLS de pagamentos
```

---

## Exemplo Completo: CRUD de Pagamentos

```markdown
## Tarefas de Implementacao

- [ ] **Tarefa 0: Criar feature branch**
  - Branch: `feature/pagamentos-crud`
  - Base: `main`

---

- [ ] **Tarefa 1: Migracao SQL — tabela pagamentos**

  **Descricao**: Criar tabela de pagamentos com schema completo, indexes, RLS policies
  e enum de status. Segue convencoes SQL do projeto.

  **Subtarefas**:
  - [ ] Criar enum `status_pagamento` (pendente, confirmado, cancelado)
  - [ ] Criar tabela `pagamentos` com todos os campos
  - [ ] Adicionar indexes compostos (tenant_id + data_pagamento)
  - [ ] Adicionar unique constraint para prevenir duplicatas
  - [ ] Habilitar RLS e criar policies com is_admin() e auth_tenant_id()
  - [ ] Adicionar trigger update_updated_at()

  **Arquivos relevantes**:
  - `supabase/migrations/00X_pagamentos.sql`

  **Verificacao**:
  - [ ] `npx supabase db reset` executa sem erros
  - [ ] RLS policies testadas com diferentes roles

  **Commit**: `feat: add pagamentos table with RLS and indexes`

---

- [ ] **Tarefa 2: Zod schemas de validacao**

  **Descricao**: Criar schemas Zod para validacao de input de pagamentos.
  Compartilhado entre frontend (UX) e backend (seguranca).

  **Subtarefas**:
  - [ ] Schema de criacao (CreatePagamentoSchema)
  - [ ] Schema de edicao (UpdatePagamentoSchema)
  - [ ] Schema de filtros (PagamentoFilterSchema)
  - [ ] Tipos TypeScript inferidos dos schemas

  **Arquivos relevantes**:
  - `lib/schemas/pagamento.ts`

  **Verificacao**:
  - [ ] Schemas rejeitam valores monetarios negativos
  - [ ] Schemas rejeitam datas futuras (se regra de negocio)
  - [ ] TypeScript compila sem erros

  **Commit**: `feat: add Zod schemas for pagamentos validation`

---

- [ ] **Tarefa 3: API Routes — GET e POST**

  **Descricao**: Implementar listagem com filtros e criacao de pagamentos.
  Validacao com Zod, auth com createServerClient().

  **Subtarefas**:
  - [ ] GET /api/pagamentos — lista com filtros (parceiro, mes, status)
  - [ ] POST /api/pagamentos — cria pagamento com validacao
  - [ ] Calcular comissao automaticamente (valor * percentual)
  - [ ] Retornar { data } para sucesso, { error } para erros

  **Arquivos relevantes**:
  - `app/api/pagamentos/route.ts`
  - `lib/schemas/pagamento.ts`
  - `lib/supabase/server.ts`

  **Verificacao**:
  - [ ] GET retorna lista filtrada por RLS
  - [ ] POST valida input e retorna 201
  - [ ] Input invalido retorna 400 com mensagem clara
  - [ ] Sem sessao retorna 401

  **Commit**: `feat: add GET/POST API routes for pagamentos`
```

---

## Verificacao por Tarefa (Padrao GSD)

Cada tarefa deve ter bloco de verificacao com criterios concretos:

```markdown
**Verificacao**:
- [ ] [Comando ou acao para verificar] — [resultado esperado]
- [ ] `npm test` — testes relevantes passam
- [ ] `npm run lint` — sem erros de tipo
```

Criterios devem ser **verificaveis** — nao "funciona corretamente" mas sim "GET /api/x retorna 200 com lista de items".

---

## Branch Naming

| Tipo | Formato | Exemplo |
|------|---------|---------|
| Feature | `feature/[nome-descritivo]` | `feature/pagamentos-crud` |
| Fix | `fix/[descricao-do-bug]` | `fix/calculo-comissao-decimal` |
| Chore | `chore/[tarefa]` | `chore/add-pagamento-indexes` |

---

## Commits

- Conventional Commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`
- 1 commit por tarefa (minimo)
- Mensagem curta e descritiva em ingles

---

## Checklist de Validacao

- [ ] Tarefa 0 e "Criar feature branch"?
- [ ] Ordem de dependencias respeitada (SQL → API → Frontend → Testes)?
- [ ] Cada tarefa e atomica (descricao em 2-3 frases, 1 sessao focada)?
- [ ] Subtarefas sao concretas (nao vagas)?
- [ ] Arquivos relevantes listados para cada tarefa?
- [ ] Bloco de verificacao com criterios testaveis?
- [ ] Commits seguem Conventional Commits?
