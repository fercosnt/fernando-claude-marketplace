# Guia: Secao Consideracoes Tecnicas

> Como documentar decisoes tecnicas no PRD alinhadas com as convencoes do CLAUDE.md e sql.md do projeto.

---

## Nivel de Detalhe: O Teste do Litmus

> "Se remover esta informacao causaria uma suposicao errada na implementacao, mantenha."

Inclua no PRD:
- Schema de entidades novas ou alteracoes significativas
- Endpoints de API e seus contratos
- Decisoes arquiteturais que fogem do padrao
- Integracoes com servicos externos
- **Deep modules** identificados (ver secao abaixo)

Nao inclua no PRD (esta no CLAUDE.md):
- Como configurar Supabase clients (ja documentado)
- Padrao de resposta de API Routes (ja documentado)
- Code style, linting, convencoes de import (ja documentado)

### Anti-Rot: o que NAO colar no PRD

PRDs ficam no tracker por meses. Coisas que mudam toda semana viram mentira documentada:

- ❌ Paths especificos de arquivos internos (`lib/utils/format-money.ts`) — refator renomeia, PRD passa a apontar pra lugar errado
- ❌ Code dump de demo/prototype completo — vira "exemplo legado"
- ❌ Nomes de funcoes/helpers internos — viram alvo de rename
- ❌ Numero da migration (`045_pagamentos.sql`) — numeracao muda em rebase

✅ **Excecao**: snippet de prototype que encoda uma DECISAO mais precisamente que prosa (state machine, reducer pattern, schema SQL de tabela nova, JSON shape de payload publico, tipo TypeScript de interface publica). Quando inlinar:
1. Trim para as partes que carregam a decisao (nao paste o demo todo)
2. Marcar `[do prototype]`
3. Verificar que o snippet sobrevive a refator interno — se nao sobrevive, vai pra prosa.

✅ **Topologia OK**: a secao "Estrutura de Arquivos" mais abaixo descreve TOPOLOGIA (onde mora cada categoria), nao IMPLEMENTACAO. Isso e estavel e ajuda navegacao.

---

## Deep Modules (Ousterhout)

> Principio do livro *A Philosophy of Software Design* (John Ousterhout): **um bom modulo encapsula muita funcionalidade por tras de uma interface simples que raramente muda**.

### Deep vs Shallow

| Aspecto | Deep module (bom) | Shallow module (ruim) |
|---------|-------------------|----------------------|
| Interface | Pequena, estavel | Larga, muda com implementacao |
| Implementacao | Complexa, escondida | Trivial, vaza |
| Mudancas internas | Nao afetam callers | Quebram callers |
| Testabilidade | Testar via interface publica | Forca testar internals |
| Exemplo | `auth.signIn(email, password)` | `validateEmail() + hashPassword() + insertUser() + sendWelcomeEmail()` expostos individualmente |

### Como aplicar no PRD

Ao desenhar a secao Tecnica, antes de listar arquivos/endpoints:

1. **Pergunta de orientacao**: "Que MODULOS este PRD vai criar/modificar?"
2. **Para cada modulo**, declarar:
   - **Interface publica** (1-3 funcoes/metodos com assinatura)
   - **Responsabilidade encapsulada** (em 1 frase: o que ele esconde do resto do sistema)
   - **Por que e deep** (que complexidade ele isola)
3. **Sinal de alerta** — se a interface tem >5 metodos publicos OU os metodos publicos refletem 1-pra-1 a implementacao interna, e shallow. Repensar agrupamento.

### Exemplo

```markdown
### Modulos

**`commission-calculator`** (deep)
- Interface publica: `calculate(payment: Payment): Commission`
- Encapsula: regras de comissao por tier, percentuais por categoria de produto,
  arredondamento monetario, casos de bonus, retencao de imposto
- Por que e deep: 200+ linhas de regra de negocio escondidas atras de 1 funcao;
  callers nao precisam saber sobre tiers, bonus, ou imposto.

**`payment-form`** (deep)
- Interface publica: `<PaymentForm onSubmit={fn} />`
- Encapsula: validacao Zod, formato monetario BR, mascara CNPJ, estados
  de submissao, error handling, accessibility
- Por que e deep: componente "burro" do ponto de vista do caller; toda
  complexidade de UX fica dentro.
```

### Anti-padrao (shallow disfarçado de modulo)

```markdown
### ❌ Modulos shallow (evitar)

- `validatePaymentValue()` — exporta validacao isolada
- `formatPaymentValue()` — exporta formatacao isolada
- `submitPaymentForm()` — exporta submissao isolada
- `handlePaymentError()` — exporta error handling isolado

Problema: caller precisa orquestrar 4 funcoes na ordem certa.
Refator: agrupar tudo dentro de `<PaymentForm>` ou `payment-service`.
```

### Checklist Deep Modules

- [ ] Cada modulo declara interface publica com <= 5 metodos/props?
- [ ] Cada modulo tem 1 frase de "o que encapsula"?
- [ ] Modulos identificados como deep nao expoem helpers internos?
- [ ] Validei com usuario que os modulos batem com expectativa antes de redigir o resto?

---

## Schema: Formato de Documentacao

### Tabela de Entidades

```markdown
### Schema

| Entidade | Campo | Tipo | Constraint | Descricao |
|----------|-------|------|-----------|-----------|
| pagamentos | id | UUID | PK, DEFAULT gen_random_uuid() | Identificador unico |
| pagamentos | tenant_id | UUID | FK tenants(id), NOT NULL | Isolamento multi-tenant |
| pagamentos | parceiro_id | UUID | FK parceiros(id), NOT NULL | Parceiro que recebeu |
| pagamentos | valor | DECIMAL(12,2) | NOT NULL, CHECK > 0 | Valor do pagamento |
| pagamentos | percentual_comissao | DECIMAL(5,2) | NOT NULL | Percentual de comissao |
| pagamentos | valor_comissao | DECIMAL(12,2) | NOT NULL | Valor calculado da comissao |
| pagamentos | data_pagamento | DATE | NOT NULL | Data do pagamento |
| pagamentos | status | status_pagamento | NOT NULL, DEFAULT 'pendente' | ENUM: pendente, confirmado, cancelado |
| pagamentos | ativo | BOOLEAN | NOT NULL, DEFAULT true | Soft delete |
| pagamentos | created_at | TIMESTAMPTZ | NOT NULL, DEFAULT now() | Data de criacao |
| pagamentos | updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT now() | Ultima atualizacao |
```

### Convencoes SQL Obrigatorias (do projeto)

Toda entidade nova DEVE seguir:

- **PKs**: `UUID DEFAULT gen_random_uuid()` — nunca SERIAL ou INT
- **Timestamps**: `created_at/updated_at TIMESTAMPTZ NOT NULL DEFAULT now()`
- **Valores monetarios**: `DECIMAL(12,2)` — NUNCA float
- **Percentuais**: `DECIMAL(5,2)`
- **Soft delete**: `ativo BOOLEAN NOT NULL DEFAULT true` — nunca DELETE fisico
- **Status**: `CREATE TYPE status_xxx AS ENUM (...)` — nunca TEXT livre
- **Tenant**: `tenant_id UUID NOT NULL REFERENCES tenants(id)`
- **Trigger**: `update_updated_at()` automatico em tabelas com `updated_at`

### Indexes e Constraints

```markdown
### Indexes

- `idx_pagamentos_tenant_mes` ON pagamentos(tenant_id, data_pagamento) — consultas por periodo
- `idx_pagamentos_parceiro` ON pagamentos(parceiro_id) WHERE ativo = true — filtro por parceiro
- UNIQUE(tenant_id, parceiro_id, data_pagamento, valor) — prevenir duplicatas
```

### RLS Policies

```markdown
### RLS

- `is_admin()` → full access em todas as operacoes
- `auth_tenant_id()` → parceiro ve apenas seus proprios pagamentos (SELECT)
- Service role via `lib/supabase/admin.ts` para operacoes privilegiadas

Funcoes helper: SECURITY DEFINER, nunca auth.uid() direto nas policies.
```

---

## API: Formato de Documentacao

### Tabela de Endpoints

```markdown
### API Endpoints

| Metodo | Rota | Proposito | Auth | Roles |
|--------|------|-----------|------|-------|
| GET | /api/pagamentos | Listar pagamentos (com filtros) | Obrigatoria | admin, parceiro (filtrado por RLS) |
| POST | /api/pagamentos | Registrar novo pagamento | Obrigatoria | admin |
| PUT | /api/pagamentos/[id] | Atualizar pagamento pendente | Obrigatoria | admin |
| DELETE | /api/pagamentos/[id] | Soft delete (ativo=false) | Obrigatoria | admin |
| GET | /api/pagamentos/export | Exportar CSV do periodo | Obrigatoria | admin |
```

### Padrao de Resposta (do projeto)

```typescript
// Sucesso
return NextResponse.json({ data: resultado }, { status: 200 })  // GET/PUT
return NextResponse.json({ data: criado }, { status: 201 })      // POST
return new NextResponse(null, { status: 204 })                   // DELETE

// Erro
return NextResponse.json({ error: "Mensagem clara" }, { status: 4xx })
```

### Validacao

- Toda API Route valida input com Zod ANTES de processar
- Verificar sessao via `createServerClient()` no inicio de toda route protegida

---

## Arquitetura: Estrutura de Arquivos

### Formato

Quando o PRD envolve criacao de novos modulos, mapeie a estrutura:

```markdown
### Estrutura de Arquivos

app/
├── (admin)/
│   └── pagamentos/
│       ├── page.tsx              # Lista de pagamentos com filtros
│       ├── novo/page.tsx         # Formulario de novo pagamento
│       └── components/
│           ├── PagamentoForm.tsx  # React Hook Form + Zod
│           ├── PagamentoTable.tsx # Tabela com paginacao
│           └── PagamentoKPIs.tsx  # Cards de KPI
├── (parceiro)/
│   └── pagamentos/
│       └── page.tsx              # Vista do parceiro (read-only, filtrado por RLS)
└── api/
    └── pagamentos/
        ├── route.ts              # GET (lista) + POST (criar)
        └── [id]/route.ts         # PUT (editar) + DELETE (soft delete)

lib/
└── schemas/
    └── pagamento.ts              # Zod schemas de validacao

supabase/
└── migrations/
    └── 00X_pagamentos.sql        # Schema + RLS + indexes
```

### Regras de Estrutura (do projeto)

- **Componentes co-locados**: componentes especificos ficam em `app/[pagina]/components/`
- **Componentes compartilhados**: usados em 2+ paginas ficam em `components/`
- **Supabase clients**: 4 arquivos distintos em `lib/supabase/` (client, server, middleware, admin)
- **Schemas Zod**: em `lib/schemas/` — validacao compartilhada entre frontend e backend
- **Migracoes**: numeracao sequencial `001_nome.sql`, `002_nome.sql`

---

## Diagrama de Arquitetura

Para features complexas, inclua diagrama ASCII:

```
                    ┌──────────────┐
                    │   Frontend   │
                    │  (Next.js)   │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │  API Routes  │
                    │ (Zod + Auth) │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │   Supabase   │
                    │  (RLS ativo) │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
        ┌─────▼────┐ ┌────▼─────┐ ┌───▼──────┐
        │ Tabela A │ │ Tabela B │ │ View SQL │
        └──────────┘ └──────────┘ └──────────┘
```

Use diagramas apenas quando o fluxo nao e obvio (integracoes, pipelines, webhooks).

---

## Integracoes Externas

Quando o PRD envolve servicos externos:

```markdown
### Integracoes

| Servico | Proposito | Autenticacao | Observacoes |
|---------|-----------|-------------|-------------|
| Stripe | Processar pagamentos | API Key via env | Webhook para confirmacao |
| SendGrid | Emails transacionais | API Key via env | Templates pre-definidos |
```

- Credenciais NUNCA hardcoded — sempre variaveis de ambiente
- Documentar webhooks necessarios (URL, eventos, payload esperado)

---

## Checklist de Validacao

- [ ] Schema segue convencoes SQL do projeto (UUID, TIMESTAMPTZ, DECIMAL, soft delete)?
- [ ] RLS policies documentadas com is_admin() e auth_tenant_id()?
- [ ] Endpoints de API listados com metodo, rota, auth e roles?
- [ ] Estrutura de arquivos mapeada seguindo convencoes do projeto?
- [ ] Migracoes SQL com numeracao sequencial?
- [ ] Nenhum secret hardcoded — apenas referencias a variaveis de ambiente?
- [ ] Nivel de detalhe passa no teste do litmus?
- [ ] **Deep modules** declarados com interface publica + responsabilidade encapsulada?
- [ ] Nenhum modulo identificado como "deep" expoe >5 metodos publicos ou vaza implementacao?
- [ ] Sem paths/code-dumps que vao envelhecer (anti-rot)?
- [ ] ADRs da area respeitados e citados (`[ADR-XXX]`)?
