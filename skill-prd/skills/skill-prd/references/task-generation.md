# Guia: Geracao de Tarefas a partir do PRD

> Como transformar um PRD em uma lista de tarefas ordenada, atomica e executavel pelo Claude Code.

---

## Principio Central

Cada tarefa deve ser **atomica o suficiente para 1 sessao focada** do Claude Code. Se voce nao consegue descrever a mudanca em 2-3 frases, divida.

> **Por que atomicidade e nao apenas "cabe no contexto"**: o Opus 4.7 tem 1M de context window, entao o limite tecnico quase nunca aperta. O problema real e de **foco e qualidade**: tasks menores (a) reduzem "context rot" (contextos frescos por task), (b) aproveitam a literalidade do 4.7 (instrucoes especificas produzem saida mais precisa), (c) facilitam review humano, (d) permitem commits atomicos, e (e) tornam retries baratos quando algo falha. A regra e de disciplina de engenharia, nao de limite tecnico.

---

## Vertical Slicing (Tracer Bullets) — Default

> Cada tarefa entrega uma **fatia vertical fina** que atravessa TODAS as camadas (schema + API + UI + teste) end-to-end. Uma fatia completa e demonstravel/verificavel sozinha. **Prefira muitas fatias finas a poucas grossas.**

Termo origem: *The Pragmatic Programmer* (Hunt & Thomas). Anti-padrao oposto: **horizontal slicing** — fazer "todas as migrations primeiro, depois todas as APIs, depois toda a UI". Resultado horizontal: nada e demonstravel ate o ultimo dia. Tracer bullets entregam valor incremental shipavel.

### Como desenhar uma fatia vertical

Para cada slice:
1. Escolher 1 user story ou 1 caso de uso pequeno do PRD
2. Listar o minimo necessario em cada camada para fechar o fluxo:
   - Schema: so as colunas/tabelas que ESSE slice precisa (incremental)
   - API: so o endpoint que ESSE slice consome
   - UI: so a tela/componente que ESSE slice mostra
   - Teste: cenario happy path do slice (edge cases sao slices futuros)
3. Verificar: "esse slice e demonstravel sozinho?" Se nao, expandir minimo.

### Exemplo: CRUD de Pagamentos — vertical vs horizontal

**❌ Horizontal (anti-padrao):**
```
Tarefa 1: Migration completa (pagamentos + comissoes + audit_log)
Tarefa 2: Todas as 5 API routes (GET list, GET one, POST, PUT, DELETE)
Tarefa 3: Todos os Zod schemas
Tarefa 4: PagamentoTable + PagamentoForm + PagamentoFilters
Tarefa 5: Pagina lista + pagina novo + pagina detalhe
Tarefa 6: Todos os testes
→ Feature so demonstravel apos Tarefa 5. Bug encontrado na Tarefa 4 forca rework.
```

**✅ Vertical (tracer bullets):**
```
Slice 1: "Admin ve lista vazia de pagamentos"
  - Migration minima (so tabela pagamentos, sem comissoes ainda)
  - GET /api/pagamentos (retorna [])
  - Pagina /admin/pagamentos com tabela vazia + empty state
  - Teste: GET retorna 200 com array vazio
  → DEMONSTRAVEL. Slice fechada, deployavel.

Slice 2: "Admin registra primeiro pagamento simples (valor+data+parceiro)"
  - Sem mudanca de schema
  - POST /api/pagamentos (sem calculo de comissao ainda)
  - Pagina /admin/pagamentos/novo com form basico
  - Teste: POST cria registro, GET agora retorna lista nao-vazia
  → DEMONSTRAVEL. Fluxo create-then-read funcionando.

Slice 3: "Pagamento confirmado calcula comissao automaticamente"
  - Migration adiciona percentual_comissao + valor_comissao
  - PUT /api/pagamentos/[id]/confirm trigga calculo
  - Botao "Confirmar" na tabela
  - Teste: confirma pagamento, valor_comissao = valor * percentual
  → DEMONSTRAVEL. Regra de negocio nuclear funcionando.

Slice 4: "Admin filtra pagamentos por mes"
  - Sem mudanca de schema (data_pagamento ja existe)
  - GET aceita ?mes=YYYY-MM
  - Componente PagamentoFilters acima da tabela
  - Teste: filtro retorna so os do mes
  → DEMONSTRAVEL. UX de filtragem fechada.

... e assim por diante (cancelar / exportar CSV / vista do parceiro / ...)
```

### Quando horizontal cabe (excecoes raras)

Vertical e default. Use horizontal SO quando:
- **Data migration grande** desacoplada de feature (ex: backfill de 50M linhas, particionamento) — nao tem fatia vertical natural
- **Infra/biblioteca compartilhada** que multiplas features dependem (ex: criar `lib/supabase/admin.ts` que 3 PRDs vao consumir) — fatiar vertical artificialmente atrasa tudo
- **Refator preparatorio** sem mudanca de comportamento (extracao de modulo, rename) — nao tem demo

Quando usar horizontal, **declarar explicitamente** no header do tasks-*.md: `Slicing: horizontal (justificativa: ...)`. Sem justificativa explicita, default vertical.

### Ordem dentro do slice

Dentro de UM slice vertical, a ordem interna ainda e: schema-minimo → API → UI → teste (ou TDD: teste → API → UI). Mas isso e ORDEM DE EXECUCAO de uma slice, nao quebra de slices.

---

## Header obrigatorio do tasks-*.md

Todo arquivo de tarefas comeca com header de rastreabilidade:

```markdown
# Tasks — [Nome do Projeto/Feature]

**Parent**: `PRD/PRD.md` (ou URL do issue/PRD upstream)
**Gerado em**: YYYY-MM-DD
**Slicing**: vertical (default) | horizontal (justificativa: ...)
**Total slices**: N (D direto / B bloqueante)
```

O `Parent` mantem rastreabilidade quando ha varios PRDs/tasks no projeto. `Slicing` declara abordagem (vertical e o padrao — qualquer outra coisa precisa de justificativa explicita).

---

## Classificacao: Direto vs Bloqueante

Cada slice recebe um label:

| Label | Significado | Quando usar |
|-------|-------------|-------------|
| **Direto (D)** | Executavel sem intervencao humana | Implementacao com decisao ja tomada no PRD; padrao reconhecivel; sem ambiguidade de design |
| **Bloqueante (B)** | Requer decisao/aprovacao humana antes ou durante | Design review necessario; trade-off arquitetural nao resolvido no PRD; impacto em outras areas; aprovacao de stakeholder |

**Por que rotular**: permite executar lote `Direto` em background (via `gsd-execute-phase` ou subagentes paralelos) enquanto `Bloqueante` aguarda janela humana. Tambem sinaliza visualmente onde o desenho do PRD ficou raso (se >40% das slices sao `B`, o PRD nao decidiu o suficiente — voltar e refinar).

**Sinais de Bloqueante**:
- Slice envolve escolha entre 2+ abordagens nao decidida no PRD
- Slice toca area com ADR pendente
- Slice precisa de aprovacao de copy/UX/design system
- Slice altera contrato publico (API breaking change) que outros times consomem

**Default**: se na duvida, `Direto` — `Bloqueante` deve ser excecao, nao norma.

---

## Tarefa 0: Feature Branch (SEMPRE)

Toda lista comeca com:

```markdown
- [ ] **Slice 0: Criar feature branch** [Direto]
  - Branch: `feature/[nome-descritivo]`
  - Base: `main`
  - Verificar que main esta atualizado (`git pull`)
```

---

## Formato de Slice

```markdown
- [ ] **Slice N: [Titulo end-to-end demonstravel]** [Direto | Bloqueante]

  **Demo**: [1 frase descrevendo o que e demonstravel apos esta slice — voz do usuario]

  **Camadas tocadas**: schema / API / UI / teste (marcar as aplicaveis)

  **Bloqueado por**: Slice X, Slice Y (ou "Nenhum — pode comecar imediato")

  **Se Bloqueante — decisao pendente**: [o que precisa ser decidido por humano + quem decide]

  **Subtarefas** (ordem interna schema → API → UI → teste):
  - [ ] [Passo 1]
  - [ ] [Passo 2]
  - [ ] [Passo 3]

  **Arquivos relevantes**:
  - `caminho/relevante1.ts`
  - `caminho/relevante2.sql`

  **Verificacao** (slice e DEMONSTRAVEL quando):
  - [ ] [Criterio end-to-end testavel]
  - [ ] [Comando de smoke test do fluxo]

  **Commit**: `feat: [descricao end-to-end do slice]`
```

**Diferenca chave do formato antigo**: campo `Demo` (descreve fluxo demonstravel ao usuario, nao codigo entregue) + `Camadas tocadas` (sempre multiplas — se so 1 camada, suspeitar de horizontal slicing) + label `Direto|Bloqueante` + `Bloqueado por` formal.

---

## Principio de Atomicidade (dentro do vertical slicing)

### Sinais de slice grande demais:

- Demo descreve 3+ fluxos distintos do usuario
- Subtarefas internas com 7+ itens
- Toca >2 entidades novas ou >3 endpoints
- Descricao da demo precisa de mais de 1 frase
- Slice nao e demonstravel em <5 min de uso

### Como dividir slice grande:

Divida pelo **fluxo do usuario**, nao pela camada:

```
❌ ANTES (slice grande horizontal):
Slice 1: CRUD completo de pagamentos

❌ ANTES (sub-divisao horizontal — erro comum):
Slice 1: Schema + RLS + indexes
Slice 2: Todas as APIs (GET/POST/PUT/DELETE)
Slice 3: Toda a UI

✅ DEPOIS (vertical por fluxo do usuario):
Slice 1: Admin ve lista vazia
Slice 2: Admin cria pagamento simples
Slice 3: Admin confirma pagamento (com comissao)
Slice 4: Admin filtra por mes
Slice 5: Admin cancela pagamento (soft delete)
Slice 6: Admin exporta CSV
Slice 7: Parceiro ve seus proprios pagamentos (RLS read-only)
```

Cada slice acima e: end-to-end, demonstravel, shipavel, e adiciona valor incremental para o usuario.

---

## Exemplo Completo: CRUD de Pagamentos (vertical)

```markdown
# Tasks — CRUD de Pagamentos

**Parent**: `PRD/PRD.md`
**Gerado em**: 2026-05-16
**Slicing**: vertical
**Total slices**: 5 (4 Direto / 1 Bloqueante)

---

- [ ] **Slice 0: Criar feature branch** [Direto]
  - Branch: `feature/pagamentos-crud`
  - Base: `main`

---

- [ ] **Slice 1: Admin ve lista vazia de pagamentos** [Direto]

  **Demo**: Admin acessa `/admin/pagamentos` e ve tabela vazia com empty state "Nenhum pagamento registrado".

  **Camadas tocadas**: schema + API + UI + teste

  **Bloqueado por**: Nenhum — pode comecar imediato

  **Subtarefas**:
  - [ ] Migration minima: tabela `pagamentos` (so id+tenant_id+valor+data_pagamento+parceiro_id+timestamps+ativo) + RLS basico
  - [ ] GET /api/pagamentos — retorna array filtrado por RLS
  - [ ] Pagina `/admin/pagamentos` com PagamentoTable + empty state
  - [ ] Teste integracao: GET retorna 200 com [] para tenant sem registros

  **Arquivos relevantes**:
  - `supabase/migrations/00X_pagamentos.sql`
  - `app/api/pagamentos/route.ts`
  - `app/(admin)/pagamentos/page.tsx`
  - `tests/api/pagamentos.test.ts`

  **Verificacao** (slice e DEMONSTRAVEL quando):
  - [ ] `npm run dev` + login admin + abrir /admin/pagamentos mostra empty state
  - [ ] `npm test pagamentos` passa

  **Commit**: `feat: empty payments list page with RLS-filtered API`

---

- [ ] **Slice 2: Admin registra primeiro pagamento (valor+data+parceiro)** [Direto]

  **Demo**: Admin clica "Novo", preenche valor+data+parceiro, submete, ve registro aparecer na tabela.

  **Camadas tocadas**: API + UI + teste (schema ja existe)

  **Bloqueado por**: Slice 1

  **Subtarefas**:
  - [ ] CreatePagamentoSchema (Zod) com valor>0 + data+parceiro_id obrigatorios
  - [ ] POST /api/pagamentos — valida Zod, insere, retorna 201
  - [ ] Pagina `/admin/pagamentos/novo` com PagamentoForm (React Hook Form + Zod resolver)
  - [ ] Teste: POST cria registro, GET passa a listar

  **Arquivos relevantes**:
  - `lib/schemas/pagamento.ts`
  - `app/api/pagamentos/route.ts`
  - `app/(admin)/pagamentos/novo/page.tsx`

  **Verificacao**:
  - [ ] Submit valido cria registro e redireciona pra lista
  - [ ] Submit invalido (valor=0) mostra erro inline
  - [ ] `npm test` passa

  **Commit**: `feat: create payment via form with Zod validation`

---

- [ ] **Slice 3: Pagamento confirmado calcula comissao automaticamente** [Bloqueante]

  **Demo**: Admin clica "Confirmar" em pagamento pendente, sistema calcula comissao via regra do parceiro e mostra valor na tabela.

  **Camadas tocadas**: schema + API + UI + teste

  **Bloqueado por**: Slice 2

  **Se Bloqueante — decisao pendente**: a regra de comissao varia por parceiro (percentual fixo? tier por volume? bonus retroativo?). PRD nao decidiu. Decisor: Financeiro + Fernando.

  **Subtarefas**:
  - [ ] Migration adiciona `percentual_comissao` + `valor_comissao` + enum `status_pagamento`
  - [ ] PUT /api/pagamentos/[id]/confirm aplica regra decidida
  - [ ] Botao "Confirmar" na tabela com confirmacao
  - [ ] Teste: confirma pagamento, `valor_comissao = valor * percentual`

  **Arquivos relevantes**:
  - `supabase/migrations/00Y_pagamentos_comissao.sql`
  - `app/api/pagamentos/[id]/confirm/route.ts`
  - `app/(admin)/pagamentos/components/PagamentoTable.tsx`

  **Verificacao**:
  - [ ] Confirmar atualiza status + calcula comissao
  - [ ] Pagamento ja confirmado nao re-confirma (idempotente)

  **Commit**: `feat: confirm payment with auto commission calculation`

---

- [ ] **Slice 4: Admin filtra pagamentos por mes** [Direto]

  **Demo**: Admin seleciona mes no filtro, tabela atualiza mostrando so registros do periodo.

  ...
```

**Note como cada slice e demonstravel sozinho** — depois da Slice 1 ja da pra mostrar pagina (empty state); depois da Slice 2 ja da pra criar e ver registro; depois da Slice 3 ja da pra confirmar e ver comissao. Sem slice horizontal "todas as migrations primeiro".

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

- [ ] Header presente com **Parent** + **Gerado em** + **Slicing** + **Total slices**?
- [ ] Slice 0 e "Criar feature branch"?
- [ ] **Cada slice e VERTICAL** (toca multiplas camadas + tem demo end-to-end)?
- [ ] Se algum slice e horizontal, justificativa esta declarada no header?
- [ ] Cada slice tem campo **Demo** descrevendo fluxo demonstravel ao usuario?
- [ ] Cada slice tem label **[Direto] ou [Bloqueante]**?
- [ ] Slices `Bloqueante` declaram **decisao pendente + decisor**?
- [ ] **Bloqueado por** declarado formalmente (ou "Nenhum")?
- [ ] Slices em **dependency order** (blockers antes)?
- [ ] Razao Bloqueante/Direto saudavel (<40% Bloqueante)?
- [ ] Cada slice e atomico (demo em 1 frase, demonstravel em <5min)?
- [ ] Subtarefas concretas (nao vagas)?
- [ ] Arquivos relevantes listados?
- [ ] Verificacao end-to-end (testa o fluxo da demo, nao so a camada)?
- [ ] Commits seguem Conventional Commits descrevendo end-to-end?
