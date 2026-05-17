# [PREENCHER: Nome do Produto/Iniciativa]

| Campo | Valor |
|-------|-------|
| Autor | [PREENCHER] |
| Data | [PREENCHER: YYYY-MM-DD] |
| Status | Rascunho |
| Nivel | Comprehensive |
| Stakeholders | [PREENCHER] |
| Versao | 1.0 |
| Ultima revisao | [PREENCHER: YYYY-MM-DD] |

---

## 1. Problema & Contexto

[PREENCHER: 3-5 frases descrevendo o problema na voz do usuario. Contextualize o impacto no negocio.]

### Evidencias

- **Dados**: [PREENCHER: Metrica quantitativa com fonte — ex: "35% de churn nos primeiros 30 dias (analytics, jan-mar 2026)"]
- **Usuarios**: [PREENCHER: Quotes diretas — ex: "Perco 2h/dia nessa planilha" — Maria, gestora clinica X]
- **Suporte**: [PREENCHER: Volume de tickets — ex: "47 tickets/mes sobre erro de pagamento (Zendesk, Q1 2026)"]
- **Observacao**: [PREENCHER: Insights de shadowing, entrevistas ou testes de usabilidade]

### Contexto Historico

[PREENCHER: Tentativas anteriores, decisoes passadas, evolucao do problema. Remover se nao aplicavel.]

---

## 2. Objetivos & Metricas

**Objective**: [PREENCHER: Frase que descreve o resultado desejado para o usuario]

### OKRs

```
Objective: [PREENCHER: resultado desejado]

- KR1: [PREENCHER] (prazo: [PREENCHER])
- KR2: [PREENCHER] (prazo: [PREENCHER])
- KR3: [PREENCHER] (prazo: [PREENCHER])
```

### Metrica Primaria
| Metrica | Atual | Meta | Prazo | Como Medir |
|---------|-------|------|-------|-----------|
| [PREENCHER] | [PREENCHER] | [PREENCHER] | [PREENCHER] | [PREENCHER] |

### Metricas Secundarias
| Metrica | Atual | Meta | Prazo | Tipo | Como Medir |
|---------|-------|------|-------|------|-----------|
| [PREENCHER] | [PREENCHER] | [PREENCHER] | [PREENCHER] | Leading | [PREENCHER] |
| [PREENCHER] | [PREENCHER] | [PREENCHER] | [PREENCHER] | Leading | [PREENCHER] |
| [PREENCHER] | [PREENCHER] | [PREENCHER] | [PREENCHER] | Lagging | [PREENCHER] |

### Metricas Guardrail (NAO podem piorar)
| Metrica | Valor Atual | Limite Minimo Aceitavel | Como Monitorar |
|---------|-------------|------------------------|----------------|
| [PREENCHER] | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| [PREENCHER] | [PREENCHER] | [PREENCHER] | [PREENCHER] |

---

## 3. Escopo

### v1 (MVP) — [PREENCHER: estimativa de prazo]

- [PREENCHER]
- [PREENCHER]
- [PREENCHER]
- [PREENCHER]

### v2 (apos validacao) — [PREENCHER: estimativa de prazo]

- [PREENCHER]
- [PREENCHER]
- [PREENCHER]

### v3 (futuro)

- [PREENCHER]
- [PREENCHER]

---

## 3b. Fora do Escopo

| Item | Razao | Consideracao Futura |
|------|-------|---------------------|
| [PREENCHER: O que NAO sera feito] | [PREENCHER: Por que nao agora] | v2 / v3 / Nunca |
| [PREENCHER] | [PREENCHER] | v2 / v3 / Nunca |
| [PREENCHER] | [PREENCHER] | v2 / v3 / Nunca |

---

## 4. Personas & Jornadas

### Persona 1: [PREENCHER: Nome/Role]

- **Quem**: [PREENCHER: Perfil em 2-3 frases]
- **Motivacao**: [PREENCHER: O que essa persona busca]
- **Frustracao atual**: [PREENCHER: Pain point especifico]
- **Frequencia de uso**: [PREENCHER: Diario/Semanal/Mensal]

**Jornada atual (AS-IS)**:
1. [PREENCHER: Passo 1 do fluxo atual]
2. [PREENCHER: Passo 2 — onde esta o atrito?]
3. [PREENCHER: Passo 3]

**Jornada futura (TO-BE)**:
1. [PREENCHER: Passo 1 com a nova feature]
2. [PREENCHER: Passo 2 — como o atrito e eliminado]
3. [PREENCHER: Passo 3]

### Persona 2: [PREENCHER: Nome/Role]

- **Quem**: [PREENCHER]
- **Motivacao**: [PREENCHER]
- **Frustracao atual**: [PREENCHER]
- **Frequencia de uso**: [PREENCHER]

**Jornada atual (AS-IS)**:
1. [PREENCHER]
2. [PREENCHER]

**Jornada futura (TO-BE)**:
1. [PREENCHER]
2. [PREENCHER]

---

## 5. User Stories & Epic Hypotheses

### Epico: [PREENCHER: Nome do epico]

**Hipotese:**
```
Se nos [PREENCHER: acao/feature] para [PREENCHER: persona],
entao [PREENCHER: resultado esperado].
Saberemos que funcionou quando [PREENCHER: metrica/evidencia].

Tiny Act of Discovery: [PREENCHER: menor experimento para validar antes de construir tudo]
```

| ID | Como... | Quero... | Para... | Prioridade |
|----|---------|----------|---------|------------|
| US-01 | [PREENCHER: role] | [PREENCHER: acao] | [PREENCHER: beneficio] | Must |
| US-02 | [PREENCHER: role] | [PREENCHER: acao] | [PREENCHER: beneficio] | Must |
| US-03 | [PREENCHER: role] | [PREENCHER: acao] | [PREENCHER: beneficio] | Should |

### Criterios de Aceite Detalhados

**US-01: [PREENCHER: titulo]**

```
Cenario 1: [PREENCHER: cenario feliz]
  Given [PREENCHER: contexto]
  When [PREENCHER: acao]
  Then [PREENCHER: resultado]

Cenario 2: [PREENCHER: edge case]
  Given [PREENCHER: contexto]
  When [PREENCHER: acao]
  Then [PREENCHER: resultado]

Cenario 3: [PREENCHER: estado de erro]
  Given [PREENCHER: contexto]
  When [PREENCHER: acao invalida]
  Then [PREENCHER: mensagem de erro + sistema nao altera estado]
```

---

## 6. Requisitos Funcionais

| ID | Requisito | Criterio de Aceite | Prioridade | US Relacionada |
|----|-----------|-------------------|------------|----------------|
| RF-01 | [PREENCHER] | Given/When/Then | Must | US-01 |
| RF-02 | [PREENCHER] | Given/When/Then | Must | US-01 |
| RF-03 | [PREENCHER] | Given/When/Then | Must | US-02 |
| RF-04 | [PREENCHER] | Given/When/Then | Should | US-03 |
| RF-05 | [PREENCHER] | Given/When/Then | Should | US-03 |
| RF-06 | [PREENCHER] | Given/When/Then | Could | — |

### Edge Cases & Estados de Erro

| RF | Cenario | Comportamento Esperado |
|----|---------|----------------------|
| RF-01 | [PREENCHER: input invalido] | [PREENCHER: mensagem de erro] |
| RF-01 | [PREENCHER: estado vazio] | [PREENCHER: empty state] |
| RF-02 | [PREENCHER: limite] | [PREENCHER: comportamento] |
| RF-03 | [PREENCHER: falha de rede] | [PREENCHER: feedback ao usuario] |

---

## 7. Requisitos Nao-Funcionais

| ID | Categoria | Requisito | Metrica | Como Testar |
|----|-----------|-----------|---------|------------|
| RNF-01 | Performance | [PREENCHER] | < 2s P95 | Lighthouse, load test |
| RNF-02 | Seguranca | RLS com isolamento por tenant | Zero acessos cross-tenant | Teste de integracao RLS |
| RNF-03 | Seguranca | Inputs validados no backend | 100% das routes com Zod | Code review + testes |
| RNF-04 | Dados | Valores monetarios sem arredondamento | DECIMAL(12,2) | Schema review |
| RNF-05 | Acessibilidade | [PREENCHER] | WCAG AA | axe-core, teste manual |
| RNF-06 | Disponibilidade | [PREENCHER] | [PREENCHER: ex. 99.5%] | Monitoring |

---

## 8. Consideracoes Tecnicas

### Schema Completo

| Entidade | Campo | Tipo | Constraint | Descricao |
|----------|-------|------|-----------|-----------|
| [PREENCHER] | id | UUID | PK, DEFAULT gen_random_uuid() | Identificador unico |
| [PREENCHER] | tenant_id | UUID | FK tenants(id), NOT NULL | Multi-tenant |
| [PREENCHER] | [PREENCHER] | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| [PREENCHER] | [PREENCHER] | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| [PREENCHER] | [PREENCHER] | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| [PREENCHER] | ativo | BOOLEAN | NOT NULL, DEFAULT true | Soft delete |
| [PREENCHER] | created_at | TIMESTAMPTZ | NOT NULL, DEFAULT now() | Criacao |
| [PREENCHER] | updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT now() | Atualizacao |

### Indexes & Constraints

```sql
-- Index composto obrigatorio
CREATE INDEX idx_[PREENCHER]_tenant ON [PREENCHER](tenant_id, [PREENCHER]);

-- Partial index para queries frequentes
CREATE INDEX idx_[PREENCHER]_ativos ON [PREENCHER](tenant_id, [PREENCHER]) WHERE ativo = true;

-- Unique constraint para prevenir duplicatas
ALTER TABLE [PREENCHER] ADD CONSTRAINT uq_[PREENCHER] UNIQUE (tenant_id, [PREENCHER]);
```

### RLS Policies

```sql
-- Admin: acesso total
CREATE POLICY "admin_full_access" ON [PREENCHER]
  FOR ALL USING (is_admin());

-- Tenant: acesso filtrado
CREATE POLICY "[PREENCHER]_read_own" ON [PREENCHER]
  FOR SELECT USING ([PREENCHER] = auth_tenant_id());

-- [PREENCHER: policies adicionais se necessario]
```

### API Endpoints Completos

| Metodo | Rota | Proposito | Auth | Roles | Request Body | Response |
|--------|------|-----------|------|-------|-------------|---------|
| GET | [PREENCHER] | [PREENCHER] | Obrigatoria | [PREENCHER] | — | `{ data: [...] }` |
| POST | [PREENCHER] | [PREENCHER] | Obrigatoria | [PREENCHER] | [PREENCHER: campos] | `{ data: {...} }` 201 |
| PUT | [PREENCHER] | [PREENCHER] | Obrigatoria | [PREENCHER] | [PREENCHER: campos] | `{ data: {...} }` 200 |
| DELETE | [PREENCHER] | Soft delete | Obrigatoria | [PREENCHER] | — | 204 |

### Estrutura de Arquivos

```
app/
├── (admin)/
│   └── [PREENCHER]/
│       ├── page.tsx
│       ├── [PREENCHER]/page.tsx
│       └── components/
│           ├── [PREENCHER]Form.tsx
│           ├── [PREENCHER]Table.tsx
│           └── [PREENCHER]KPIs.tsx
├── ([PREENCHER: role])/
│   └── [PREENCHER]/
│       └── page.tsx
└── api/
    └── [PREENCHER]/
        ├── route.ts
        └── [id]/route.ts

lib/
└── schemas/
    └── [PREENCHER].ts

supabase/
└── migrations/
    └── [PREENCHER]_[nome].sql
```

### Diagrama de Arquitetura

```
[PREENCHER: Diagrama ASCII do fluxo de dados. Exemplo:]

    ┌──────────┐     ┌──────────┐     ┌──────────┐
    │ Frontend │────▶│   API    │────▶│ Supabase │
    │ (Next.js)│◀────│ (Routes) │◀────│  (RLS)   │
    └──────────┘     └─────┬────┘     └──────────┘
                           │
                    ┌──────▼──────┐
                    │ [PREENCHER] │
                    │ (servico    │
                    │  externo)   │
                    └─────────────┘
```

---

## 9. Riscos & Mitigacoes

| # | Risco | Probabilidade | Impacto | Mitigacao | Owner |
|---|-------|--------------|---------|-----------|-------|
| 1 | [PREENCHER] | [Alta/Media/Baixa] | [Alto/Medio/Baixo] | [PREENCHER] | [PREENCHER] |
| 2 | [PREENCHER] | [Alta/Media/Baixa] | [Alto/Medio/Baixo] | [PREENCHER] | [PREENCHER] |
| 3 | [PREENCHER] | [Alta/Media/Baixa] | [Alto/Medio/Baixo] | [PREENCHER] | [PREENCHER] |
| 4 | [PREENCHER] | [Alta/Media/Baixa] | [Alto/Medio/Baixo] | [PREENCHER] | [PREENCHER] |
| 5 | [PREENCHER] | [Alta/Media/Baixa] | [Alto/Medio/Baixo] | [PREENCHER] | [PREENCHER] |

### Pre-mortem

> "E 6 meses depois do lancamento. O projeto fracassou. Por que?"

1. [PREENCHER: Cenario de fracasso 1 — ex: "Parceiros nao adotaram porque o fluxo tem 8 passos"]
2. [PREENCHER: Cenario de fracasso 2 — ex: "Dados inconsistentes porque migracao nao cobriu edge cases"]
3. [PREENCHER: Cenario de fracasso 3]

---

## 10. Questoes em Aberto

| # | Questao | Responsavel | Prazo | Status |
|---|---------|-------------|-------|--------|
| 1 | [PREENCHER] | [PREENCHER] | [PREENCHER] | Aberta |
| 2 | [PREENCHER] | [PREENCHER] | [PREENCHER] | Aberta |
| 3 | [PREENCHER] | [PREENCHER] | [PREENCHER] | Aberta |

---

## 11. Timeline & Fases (opcional)

| Fase | Escopo | Duracao | Milestone |
|------|--------|---------|-----------|
| Fase 1 — MVP | [PREENCHER: escopo v1] | [PREENCHER] | [PREENCHER: entregavel] |
| Fase 2 — Expansao | [PREENCHER: escopo v2] | [PREENCHER] | [PREENCHER: entregavel] |
| Fase 3 — Otimizacao | [PREENCHER: escopo v3] | [PREENCHER] | [PREENCHER: entregavel] |

---

## 12. Analise Competitiva (opcional)

| Solucao | Pontos Fortes | Pontos Fracos | Diferencial Nosso |
|---------|--------------|---------------|-------------------|
| [PREENCHER] | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| [PREENCHER] | [PREENCHER] | [PREENCHER] | [PREENCHER] |

---

## 13. Estrategia de Rollout (opcional)

- [ ] **Feature flag**: [PREENCHER: nome da flag]
- [ ] **Rollout gradual**: [PREENCHER: % de usuarios por fase]
- [ ] **Rollback plan**: [PREENCHER: como reverter se necessario]
- [ ] **Comunicacao**: [PREENCHER: como informar usuarios]

---

## 14. Plano de Documentacao (opcional)

- [ ] Guia do usuario para [PREENCHER: persona 1]
- [ ] Guia do usuario para [PREENCHER: persona 2]
- [ ] Documentacao tecnica (API, schema)
- [ ] Changelog / release notes
- [ ] Treinamento interno [PREENCHER: se aplicavel]
