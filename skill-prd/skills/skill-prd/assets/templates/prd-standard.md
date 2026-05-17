# [PREENCHER: Nome da Feature/Produto]

| Campo | Valor |
|-------|-------|
| Autor | [PREENCHER] |
| Data | [PREENCHER: YYYY-MM-DD] |
| Status | Rascunho |
| Nivel | Standard |
| Stakeholders | [PREENCHER] |

---

## 1. Problema & Contexto

[PREENCHER: 3-5 frases descrevendo o problema na voz do usuario. Sem mencionar solucao.]

### Evidencias

- [PREENCHER: Dado quantitativo com fonte]
- [PREENCHER: Quote direta de usuario ou ticket de suporte]
- [PREENCHER: Terceira evidencia]

### Contexto

[PREENCHER: Background necessario para quem nao conhece o dominio. Remover se audiencia ja conhece.]

---

## 2. Objetivos & Metricas

**Objetivo principal**: [PREENCHER: O que muda para o usuario]

### Metrica Primaria
| Metrica | Atual | Meta | Prazo |
|---------|-------|------|-------|
| [PREENCHER] | [PREENCHER] | [PREENCHER] | [PREENCHER] |

### Metricas Secundarias
| Metrica | Atual | Meta | Prazo |
|---------|-------|------|-------|
| [PREENCHER] | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| [PREENCHER] | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| [PREENCHER] | [PREENCHER] | [PREENCHER] | [PREENCHER] |

### Metricas Guardrail (NAO podem piorar)
| Metrica | Valor Atual | Limite Minimo Aceitavel |
|---------|-------------|------------------------|
| [PREENCHER] | [PREENCHER] | [PREENCHER] |
| [PREENCHER] | [PREENCHER] | [PREENCHER] |

---

## 3. Escopo

**v1 (MVP)**:
- [PREENCHER]
- [PREENCHER]
- [PREENCHER]

**v2 (apos validacao)**:
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

## 4. Personas & Casos de Uso

### Persona 1: [PREENCHER: Nome/Role]

- **Quem**: [PREENCHER: Descricao em 1 frase]
- **Necessidade**: [PREENCHER: O que precisa]
- **Caso de uso**: [PREENCHER: Como usa a feature]

### Persona 2: [PREENCHER: Nome/Role]

- **Quem**: [PREENCHER]
- **Necessidade**: [PREENCHER]
- **Caso de uso**: [PREENCHER]

---

## 5. Epic Hypotheses

### Epico 1: [PREENCHER: Nome do epico]

```
Se nos [PREENCHER: acao/feature] para [PREENCHER: persona],
entao [PREENCHER: resultado esperado].
Saberemos que funcionou quando [PREENCHER: metrica/evidencia].

Tiny Act of Discovery: [PREENCHER: menor experimento para validar antes de construir tudo]
```

### Epico 2: [PREENCHER: Nome do epico]

```
Se nos [PREENCHER: acao/feature] para [PREENCHER: persona],
entao [PREENCHER: resultado esperado].
Saberemos que funcionou quando [PREENCHER: metrica/evidencia].

Tiny Act of Discovery: [PREENCHER: menor experimento para validar]
```

---

## 6. Requisitos Funcionais

| ID | Requisito | Criterio de Aceite | Prioridade |
|----|-----------|-------------------|------------|
| RF-01 | [PREENCHER] | Given [contexto], When [acao], Then [resultado] | Must |
| RF-02 | [PREENCHER] | Given [contexto], When [acao], Then [resultado] | Must |
| RF-03 | [PREENCHER] | Given [contexto], When [acao], Then [resultado] | Must |
| RF-04 | [PREENCHER] | Given [contexto], When [acao], Then [resultado] | Should |
| RF-05 | [PREENCHER] | Given [contexto], When [acao], Then [resultado] | Should |
| RF-06 | [PREENCHER] | Given [contexto], When [acao], Then [resultado] | Could |

---

## 7. Requisitos Nao-Funcionais

| ID | Categoria | Requisito | Metrica |
|----|-----------|-----------|---------|
| RNF-01 | Performance | [PREENCHER] | [PREENCHER: ex. < 2s P95] |
| RNF-02 | Seguranca | RLS ativo com isolamento por tenant | auth_tenant_id() + is_admin() |
| RNF-03 | Dados | Valores monetarios sem arredondamento | DECIMAL(12,2) |
| RNF-04 | [PREENCHER] | [PREENCHER] | [PREENCHER] |

---

## 8. Consideracoes Tecnicas

### Schema

| Entidade | Campo | Tipo | Constraint | Descricao |
|----------|-------|------|-----------|-----------|
| [PREENCHER] | id | UUID | PK, DEFAULT gen_random_uuid() | Identificador unico |
| [PREENCHER] | tenant_id | UUID | FK tenants(id), NOT NULL | Multi-tenant |
| [PREENCHER] | [PREENCHER] | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| [PREENCHER] | ativo | BOOLEAN | NOT NULL, DEFAULT true | Soft delete |
| [PREENCHER] | created_at | TIMESTAMPTZ | NOT NULL, DEFAULT now() | Criacao |
| [PREENCHER] | updated_at | TIMESTAMPTZ | NOT NULL, DEFAULT now() | Atualizacao |

### API Endpoints

| Metodo | Rota | Proposito | Auth | Roles |
|--------|------|-----------|------|-------|
| GET | [PREENCHER] | [PREENCHER] | Obrigatoria | [PREENCHER] |
| POST | [PREENCHER] | [PREENCHER] | Obrigatoria | [PREENCHER] |
| PUT | [PREENCHER] | [PREENCHER] | Obrigatoria | [PREENCHER] |
| DELETE | [PREENCHER] | Soft delete | Obrigatoria | [PREENCHER] |

### Estrutura de Arquivos

```
[PREENCHER: Arvore de diretorios com arquivos que serao criados/modificados]
```

---

## 9. Riscos & Mitigacoes

| # | Risco | Probabilidade | Impacto | Mitigacao |
|---|-------|--------------|---------|-----------|
| 1 | [PREENCHER] | [Alta/Media/Baixa] | [Alto/Medio/Baixo] | [PREENCHER] |
| 2 | [PREENCHER] | [Alta/Media/Baixa] | [Alto/Medio/Baixo] | [PREENCHER] |
| 3 | [PREENCHER] | [Alta/Media/Baixa] | [Alto/Medio/Baixo] | [PREENCHER] |

---

## 10. Questoes em Aberto

- [ ] [PREENCHER: Questao] — Responsavel: [PREENCHER] — Prazo: [PREENCHER]
- [ ] [PREENCHER: Questao] — Responsavel: [PREENCHER] — Prazo: [PREENCHER]
- [ ] [PREENCHER: Questao] — Responsavel: [PREENCHER] — Prazo: [PREENCHER]
