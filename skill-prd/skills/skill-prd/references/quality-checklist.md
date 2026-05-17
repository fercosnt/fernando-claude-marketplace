# Checklist de Qualidade & Scorecard

> Avaliacao obrigatoria em 5 dimensoes antes de entregar qualquer PRD.

---

## Scorecard de 5 Dimensoes

| Dimensao | Peso | O que avalia |
|----------|------|-------------|
| Problema | 25% | Clareza, evidencia, voz do usuario |
| Escopo | 15% | Limites claros, nao-objetivos explicitos |
| Requisitos | 25% | Testabilidade, atomicidade, priorizacao |
| Tecnico | 20% | Alinhamento com convencoes, schema, API |
| Riscos | 15% | Identificacao, mitigacao, questoes abertas |

**Nota minima para entrega: >= 7.5 (media ponderada)**

---

## Rubrica Detalhada

### 1. Problema (25%)

| Nota | Descricao |
|------|-----------|
| 1-3 | Problema vago ou ausente. Sem evidencias. Solucao disfarçada de problema. |
| 4-6 | Problema descrito mas generico. Apenas 1 evidencia fraca. Parcialmente na voz do desenvolvedor. |
| 7-8 | Problema claro na voz do usuario. 2+ evidencias concretas. Sem mencao de solucao. MITRE Problem Framing aplicado. |
| 9-10 | Problema compelling com dados quantitativos. Evidencias de multiplas fontes. HMW (How Might We) formulada e coerente. Audiencia entende imediatamente o impacto. |

### 2. Escopo (15%)

| Nota | Descricao |
|------|-----------|
| 1-3 | Sem definicao de escopo. Impossivel saber o que esta dentro ou fora. |
| 4-6 | Lista de features mas sem nao-objetivos. Limites implicitos. Fora do Escopo ausente ou vazio. |
| 7-8 | Escopo In e Out explicitos. Versionamento claro (v1/v2). **Fora do Escopo como secao H2 separada com justificativas e indicacao de futuro.** |
| 9-10 | Escopo cristalino com justificativa para cada decisao de corte. Fases bem definidas. Fora do Escopo com tabela completa (Item + Razao + Consideracao Futura). |

### 3. Requisitos (25%)

| Nota | Descricao |
|------|-----------|
| 1-3 | Requisitos vagos sem criterios de aceite. Tudo e "Must". Nao atomicos. |
| 4-6 | Criterios de aceite existem mas nao sao testaveis. Priorizacao parcial. Alguns requisitos grandes demais. |
| 7-8 | Given/When/Then em todos os requisitos. MoSCoW aplicado (<=60% Must). Requisitos atomicos. Edge cases nos criticos. **Epic Hypothesis presente em PRDs Standard+.** |
| 9-10 | Requisitos impecaveis. RNFs com metricas. Edge cases e estados de erro completos. IDs consistentes. Nenhum ambiguo. **Epicos como hipoteses testaveis com "tiny act of discovery" (Standard+).** |

### 4. Tecnico (20%)

| Nota | Descricao |
|------|-----------|
| 1-3 | Sem consideracoes tecnicas. Ou desalinhado com convencoes do projeto. |
| 4-6 | Schema parcial. API sem contratos claros. Estrutura de arquivos ausente. Sem deep modules. Code-dumps inlinados que vao envelhecer. |
| 7-8 | Schema completo seguindo convencoes (UUID, DECIMAL, RLS). API documentada. Estrutura mapeada. **Deep modules** declarados com interface publica. **Testing Decisions** com prior art. ADRs respeitados. |
| 9-10 | Tecnico impecavel. RLS policies detalhadas. Indexes justificados. Integracoes documentadas. Deep modules com responsabilidade encapsulada clara. Testing Decisions completo. Glossario aplicado. Sem anti-rot (zero paths/snippets que envelhecem). Diagrama quando necessario. |

### 5. Riscos (15%)

| Nota | Descricao |
|------|-----------|
| 1-3 | Sem secao de riscos. Ou "nenhum risco identificado". |
| 4-6 | Riscos listados mas sem mitigacao. Questoes abertas ausentes. |
| 7-8 | Top 3-5 riscos com mitigacao concreta. Questoes abertas com responsavel. |
| 9-10 | Pre-mortem completo. Riscos priorizados por probabilidade x impacto. Plano B para riscos criticos. Todas as questoes tem owner e deadline. |

---

## Como Calcular a Nota Final

```
Nota = (Problema * 0.25) + (Escopo * 0.15) + (Requisitos * 0.25) + (Tecnico * 0.20) + (Riscos * 0.15)
```

### Exemplo

| Dimensao | Nota | Peso | Ponderado |
|----------|------|------|-----------|
| Problema | 8 | 0.25 | 2.00 |
| Escopo | 7 | 0.15 | 1.05 |
| Requisitos | 8 | 0.25 | 2.00 |
| Tecnico | 9 | 0.20 | 1.80 |
| Riscos | 7 | 0.15 | 1.05 |
| **Total** | | | **7.90** |

Resultado: >= 7.5 — aprovado para entrega.

---

## Formato de Apresentacao

```markdown
### Avaliacao de Qualidade

| Dimensao | Nota | Peso | Observacao |
|----------|------|------|-----------|
| Problema | X/10 | 25% | [Comentario curto] |
| Escopo | X/10 | 15% | [Comentario curto] |
| Requisitos | X/10 | 25% | [Comentario curto] |
| Tecnico | X/10 | 20% | [Comentario curto] |
| Riscos | X/10 | 15% | [Comentario curto] |
| **Media ponderada** | **X.XX/10** | | |

[Se < 7.5: listar itens a melhorar antes de entregar]
```

---

## Perguntas de Validacao Rapida

Use estas perguntas para uma verificacao rapida antes do scorecard completo:

1. **Uma pessoa de fora do time entende o problema em 30 segundos?**
2. **Consigo dizer com certeza o que NAO sera feito?**
3. **Cada requisito tem criterio de aceite testavel?**
4. **As metricas de sucesso estao definidas ANTES de construir?**
5. **O schema segue as convencoes do projeto (UUID, DECIMAL, RLS)?**
6. **Os riscos tem plano de mitigacao, nao apenas listagem?**
7. **As questoes abertas tem responsavel e prazo?**
8. **O nivel de detalhe e proporcional ao risco da decisao?**
9. **Metricas guardrail estao definidas (o que NAO pode piorar)?**
10. **Fora do Escopo esta documentado como secao separada com justificativas?**
11. **Modulos foram desenhados como deep (interface pequena escondendo complexidade)?** (Std+)
12. **Testing Decisions aponta prior art (testes similares ja no codebase)?** (Std+)
13. **PRD esta livre de paths/code-dumps que vao envelhecer em semanas?**
14. **Glossario do projeto e ADRs da area foram consultados?**

Se respondeu "nao" para 3+ perguntas, o PRD precisa de revisao.

---

## 10 Anti-Patterns a Verificar (Formato Sintoma → Consequencia → Correcao)

Verificar internamente (via thinking cuidadoso) ANTES de entregar o PRD. Se detectar qualquer anti-pattern, corrigir automaticamente.

| # | Sintoma | Consequencia | Correcao |
|---|---------|-------------|----------|
| 1 | PM escreve PRD sozinho, sem input de eng/design | Sem buy-in do time, retrabalho pos-entrega | Colaborar em user stories com design + eng; incluir nota de stakeholders consultados |
| 2 | Problema sem evidencia (dados, quotes, tickets) | Time questiona se problema e real; risco de construir algo desnecessario | Incluir quotes de clientes, analytics, tickets de suporte — minimo 2 evidencias de forca alta |
| 3 | Solucao muito prescritiva no PRD ("precisamos de um dropdown") | Remove colaboracao de design, limita criatividade, enrijece implementacao | Manter solucao em alto nivel, detalhar apenas constraints tecnicas e comportamento esperado |
| 4 | Sem metricas de sucesso definidas | Impossivel validar se feature funcionou; sem accountability | Sempre definir metrica primaria + prazo de avaliacao + metrica guardrail |
| 5 | "Fora do escopo" nao documentado ou vazio | Scope creep inevitavel; time nao sabe o que dizer "nao" | Documentar explicitamente o que NAO sera feito, com justificativa e indicacao de futuro |
| 6 | Todos os requisitos sao "Must" (>60%) | Nada pode ser cortado quando prazo aperta; tudo vira critico | Aplicar MoSCoW com maximo 60% Must; forcar priorizacao honesta |
| 7 | PRD com 30+ paginas (O Romance) | Ninguem le, decisoes ficam enterradas, desatualiza rapido | Usar nivel adequado (Lean/Standard/Comprehensive); se >15 paginas, questionar |
| 8 | User stories sem criterio de aceite | Dev nao sabe quando terminou; QA nao sabe o que testar | Given/When/Then em toda story; incluir cenarios de erro |
| 9 | Schema sem tipos precisos (float para dinheiro, TEXT para status) | Erros de arredondamento em producao; dados inconsistentes | DECIMAL(12,2) para monetario, DECIMAL(5,2) para percentual, ENUM para status |
| 10 | PRD gerado por AI sem entrevista (bonito mas raso) | Parece completo mas falta profundidade real; suposicoes nao validadas | SEMPRE fazer entrevista antes de gerar; marcar suposicoes com [ASSUMIDO] |
| 11 | Paths e code-dumps inlinados no PRD ("ver `lib/utils/x.ts`", funcoes inteiras coladas) | PRD vira mentira em semanas; refator/rename quebra referencias; ninguem confia mais no doc | Remover paths/snippets que ficam outdated. Excecao: snippet que encoda DECISAO (state machine, schema SQL, JSON shape, tipo TS publico). Manter topologia (mapa de arquivos) — e estavel. |
| 12 | Sem Testing Decisions (Standard+) — quais modulos, que estilo, prior art | Agente que implementa adivinha estilo, produz suite inconsistente | Secao 7b obrigatoria em Std+: definicao de bom teste + tabela modulo/tipo + prior art apontando teste similar ja no codebase |
| 13 | Modulos shallow disfarçados de arquitetura (10 helpers expostos, sem encapsulamento) | Caller precisa orquestrar internals; mudanca interna quebra tudo; testes ficam acoplados | Aplicar Deep Modules: interface publica pequena (<= 5 metodos), responsabilidade encapsulada em 1 frase, complexidade interna escondida |
| 14 | Vocabulario inventado (PRD usa "Cliente" quando codebase usa "Tenant") | Implementacao mistura termos, schema fica inconsistente, onboarding sofre | Consultar glossario (GLOSSARY.md, secao no CLAUDE.md) no Passo 0 e usar termos canonicos do projeto |
| 15 | PRD reabre decisao ja resolvida em ADR (ex: "vamos usar REST" quando ADR-007 escolheu tRPC) | Time perde confianca; PRD ignora historico; risco de rebuild desnecessario | Buscar ADRs no Passo 0 (`docs/adr/`, `decisions/`); respeitar e citar `[ADR-XXX]`. Reabrir SO com justificativa explicita |

---

## Fluxo de Decisao

```
Scorecard >= 7.5?
├── SIM → Entregar PRD
└── NAO → Quais dimensoes < 7?
    ├── Problema → Voltar a secao, adicionar evidencias
    ├── Escopo → Definir nao-objetivos, versionar
    ├── Requisitos → Adicionar Given/When/Then, dividir grandes
    ├── Tecnico → Alinhar com CLAUDE.md, completar schema
    └── Riscos → Fazer pre-mortem, adicionar mitigacoes
```
