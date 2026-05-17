# Guia: Secao de Requisitos

> Como escrever requisitos claros, testaveis e priorizados que guiam tanto humanos quanto AI na implementacao.

---

## Requisitos Funcionais vs Nao-Funcionais

| Tipo | Pergunta que responde | Exemplo |
|------|----------------------|---------|
| **Funcional (RF)** | "O que o sistema faz?" | "Sistema calcula comissao automaticamente ao registrar pagamento" |
| **Nao-Funcional (RNF)** | "Como o sistema se comporta?" | "Dashboard carrega em < 2s com 10.000 registros" |

Requisitos funcionais descrevem **comportamento**. Requisitos nao-funcionais descrevem **qualidade**.

---

## Formato de Requisito Funcional

### Tabela Padrao

```markdown
| ID | Requisito | Criterio de Aceite | Prioridade |
|----|-----------|-------------------|------------|
| RF-01 | Sistema registra pagamento com valor, data e parceiro | Given pagamento valido, When submeter, Then registro aparece na lista com status "pendente" | Must |
| RF-02 | Sistema calcula comissao automaticamente | Given pagamento confirmado, When percentual definido, Then comissao = valor * percentual com DECIMAL(12,2) | Must |
| RF-03 | Admin exporta relatorio mensal em CSV | Given filtro de mes selecionado, When clicar exportar, Then CSV com todas colunas da tabela e baixado | Should |
```

### Convencao de IDs

- `RF-01`, `RF-02`, ... para requisitos funcionais
- `RNF-01`, `RNF-02`, ... para requisitos nao-funcionais
- IDs sao sequenciais e nunca reutilizados (mesmo se removidos)

---

## Priorizacao MoSCoW

| Nivel | Significado | Regra |
|-------|-------------|-------|
| **Must** | Sem isso, o produto nao funciona | Maximo 60% dos requisitos |
| **Should** | Importante, mas ha workaround | Proximo sprint/fase |
| **Could** | Bom ter, se sobrar tempo | Nao bloqueia lancamento |
| **Won't** | Explicitamente fora do escopo v1 | Documentar para evitar scope creep |

**Regra critica**: se mais de 60% dos requisitos sao "Must", repriorize. Nem tudo pode ser critico.

---

## Criterios de Aceite: Formato Given/When/Then

Cada requisito funcional deve ter criterio de aceite testavel.

### Estrutura

```
Given [contexto/pre-condicao]
When [acao do usuario ou evento]
Then [resultado esperado e verificavel]
```

### Exemplos

**Bom:**
```
Given usuario admin autenticado e parceiro com pagamentos no mes
When acessar dashboard e selecionar mes de referencia
Then KPIs exibem: total recebido, total comissoes, total liquido — todos com formato R$ X.XXX,XX
```

**Ruim (vago):**
```
Dashboard mostra dados financeiros corretamente
```

**Bom (com edge case):**
```
Given formulario de pagamento preenchido com valor "0,00"
When submeter formulario
Then sistema exibe erro "Valor deve ser maior que zero" e nao cria registro
```

**Ruim (ignora edge case):**
```
Sistema registra pagamento quando formulario e submetido
```

---

## Principio INVEST para User Stories

Quando requisitos sao escritos como user stories, devem seguir INVEST:

| Letra | Significado | Teste |
|-------|-------------|-------|
| **I** — Independent | Pode ser implementada sem depender de outra story | "Consigo entregar isso sozinho?" |
| **N** — Negotiable | Detalhes podem ser discutidos | "Ha espaco para decisao de design?" |
| **V** — Valuable | Entrega valor para o usuario | "O usuario percebe a diferenca?" |
| **E** — Estimable | Time consegue estimar esforco | "Sabemos o suficiente para estimar?" |
| **S** — Small | Cabe em 1 sprint (ou 1 sessao focada do Claude Code) | "Descrevemos em 2-3 frases?" |
| **T** — Testable | Criterio de aceite claro | "Sabemos quando esta pronto?" |

---

## Epic Hypothesis Template (Standard e Comprehensive)

Para PRDs nivel Standard e Comprehensive, formular cada epico como hipotese testavel. Isso conecta a feature ao resultado desejado e previne "feature factory".

### Formato

```
Se nos [acao/feature] para [persona], entao [resultado esperado].
Saberemos que funcionou quando [metrica/evidencia].

Tiny Act of Discovery: [menor experimento possivel para validar antes de construir tudo]
```

### Exemplos

**Dashboard financeiro:**
```
Se nos criarmos dashboard financeiro para parceiros, entao eles terao visibilidade sem depender do admin.
Saberemos que funcionou quando 70% acessarem semanalmente.

Tiny Act of Discovery: mockup estatico com dados reais para 3 parceiros testarem.
```

**Automacao de comissao:**
```
Se nos automatizarmos calculo de comissao para admins, entao erros de calculo serao eliminados.
Saberemos que funcionou quando erros reportados = 0.

Tiny Act of Discovery: planilha automatizada para 1 mes antes de codificar.
```

### Quando usar

| Nivel | Usar Epic Hypothesis? |
|-------|-----------------------|
| Lean | Nao — requisitos simples em tabela |
| Standard | Sim — cada epico como hipotese |
| Comprehensive | Sim — hipoteses + tiny acts obrigatorios |

### Checklist

- [ ] Epicos formulados como hipoteses testaveis? (Standard+)
- [ ] Cada hipotese tem metrica/evidencia de validacao?
- [ ] Pelo menos 1 "tiny act of discovery" por epico?

---

## Principio de Atomicidade

> "Se voce nao consegue descrever o requisito em 2-3 frases, divida."

### Sinal de requisito grande demais:

- Criterio de aceite tem mais de 5 "Then" clauses
- Descricao menciona 3+ telas ou fluxos
- Implementacao exige mudancas em 5+ arquivos
- Estimativa e "grande" ou "nao sei"

### Como dividir:

```
ANTES (grande demais):
RF-01: Sistema gerencia pagamentos completo (CRUD + relatorios + notificacoes)

DEPOIS (atomico):
RF-01: Admin registra pagamento com valor, data, parceiro e tipo
RF-02: Admin edita pagamento pendente (valor, data, tipo)
RF-03: Admin cancela pagamento pendente (soft delete, campo ativo=false)
RF-04: Sistema lista pagamentos com filtro por parceiro, mes e status
RF-05: Sistema envia notificacao ao parceiro quando pagamento e confirmado
```

---

## Requisitos Nao-Funcionais

### Categorias Comuns

| Categoria | Exemplo |
|-----------|---------|
| **Performance** | "Dashboard carrega em < 2s com 10.000 registros" |
| **Seguranca** | "RLS ativo em todas tabelas multi-tenant; inputs validados com Zod" |
| **Acessibilidade** | "Navegacao completa por teclado; contraste WCAG AA" |
| **Disponibilidade** | "99.5% uptime mensal" |
| **Compatibilidade** | "Funciona em Chrome, Firefox, Safari (ultimas 2 versoes)" |
| **Dados** | "Valores monetarios em DECIMAL(12,2); soft delete obrigatorio" |

### Formato

```markdown
| ID | Categoria | Requisito | Metrica |
|----|-----------|-----------|---------|
| RNF-01 | Performance | Paginas carregam em tempo aceitavel | < 2s no P95 |
| RNF-02 | Seguranca | Isolamento de dados por tenant | RLS com auth_tenant_id() em toda tabela |
| RNF-03 | Dados | Precisao monetaria sem arredondamento | DECIMAL(12,2), nunca float |
```

---

## Edge Cases e Estados de Erro

Todo requisito funcional deve considerar:

1. **Input invalido** — O que acontece com dados incorretos?
2. **Estado vazio** — Como a tela se comporta sem dados?
3. **Limites** — Valores maximo/minimo, listas com 10.000+ itens
4. **Concorrencia** — Dois usuarios editando o mesmo registro
5. **Falha de rede** — O que o usuario ve se a API falha?
6. **Permissao negada** — Usuario tenta acessar recurso de outro tenant

### Como documentar

Adicione edge cases como sub-itens do requisito principal:

```markdown
| RF-01 | Admin registra pagamento | ... | Must |
| RF-01a | Valor zero ou negativo: exibir erro de validacao | ... | Must |
| RF-01b | Parceiro inativo: bloquear registro com mensagem | ... | Must |
| RF-01c | Duplicata (mesmo parceiro+data+valor): exibir warning | ... | Should |
```

---

## Testing Decisions (OBRIGATORIO Standard+)

> Sem esta secao, o agente que implementa fica adivinhando estilo de teste do projeto e produz suite inconsistente.

### Formato

Adicionar como sub-secao da Tecnica OU como secao 7b autonoma do PRD:

```markdown
## Testing Decisions

### Definicao de "bom teste" (neste PRD)
- Testar comportamento externo visivel ao usuario/caller, NAO implementacao interna
- Cada teste deve falhar se o requisito quebrar; passar caso contrario
- Setup minimo — preferir factory/fixture do projeto a mocks ad-hoc

### Modulos com cobertura obrigatoria
| Modulo | Tipo de teste | Cenarios criticos |
|--------|---------------|-------------------|
| commission-calculator | Unit (puro) | Tier base, tier bonus, valor zero, retencao imposto |
| payment-form | Integration (Testing Library) | Submit valido, validacao Zod, erro de rede |
| /api/pagamentos POST | Integration (Supertest + Supabase test client) | Auth ok, RLS bloqueando outro tenant, payload invalido |

### Prior art (testes similares ja no codebase)
- `tests/lib/billing-calculator.test.ts` — exemplo de unit puro com tabela de casos
- `tests/components/InvoiceForm.test.tsx` — exemplo de Testing Library + Zod
- `tests/api/invoices.test.ts` — exemplo de RLS testado via 2 sessions distintas

### Fora do escopo de teste
- E2E completo (cobertura via QA manual no v1)
- Performance/carga (escopo de RNF-XX em outro PRD)
- Visual regression (sem Chromatic no projeto ainda)
```

### Por que prior art importa

O agente que vai implementar abre o codebase, procura padrao, copia. Se o PRD aponta o teste-modelo:
- Estilo (Vitest vs Jest, RTL vs Enzyme, supertest vs fetch) e herdado automatico
- Convencoes locais (factories, fixtures, helpers de auth de teste) sao reaproveitadas
- Zero divergencia de tooling

Se o PRD nao aponta, agente vai usar o que aprendeu fora do projeto — produz suite mista, custosa de manter.

### Checklist Testing Decisions

- [ ] Definicao explicita de "bom teste" neste contexto?
- [ ] Lista de modulos com cobertura obrigatoria + tipo de teste?
- [ ] Pelo menos 1 referencia de prior art por tipo de teste novo?
- [ ] Cenarios criticos listados (nao "testar X" generico)?
- [ ] Fora-de-escopo-de-teste declarado (evita backlog inflado)?

---

## Checklist de Validacao

- [ ] Todos os requisitos tem ID unico (RF-XX ou RNF-XX)?
- [ ] Criterios de aceite estao no formato Given/When/Then?
- [ ] Priorizacao MoSCoW aplicada com no maximo 60% "Must"?
- [ ] Requisitos atomicos (descrevem 1 comportamento em 2-3 frases)?
- [ ] Edge cases e estados de erro documentados para requisitos criticos?
- [ ] Requisitos nao-funcionais tem metricas concretas?
- [ ] Nenhum requisito e ambiguo ("o sistema deve ser rapido" — rapido quanto?)?
- [ ] Won't items documentados para evitar scope creep?
- [ ] Epicos formulados como hipoteses testaveis? (Standard+)
- [ ] Cada hipotese tem "tiny act of discovery"? (Standard+)
- [ ] **Testing Decisions** com prior art e modulos obrigatorios? (Standard+)
