# Guia: Secao Objetivos & Metricas

> Como definir metas mensuráveis que respondem "como sabemos que funcionou?"

---

## Por que Metricas sao Obrigatorias

Sem metricas, a feature lanca e ninguem sabe se resolveu o problema. Toda feature deve ter pelo menos 1 metrica de sucesso definida ANTES da implementacao.

---

## Metricas SMART

Toda metrica deve ser:

| Letra | Significado | Teste |
|-------|-------------|-------|
| **S** — Specific | Descreve exatamente o que mede | "Qual numero exato estamos olhando?" |
| **M** — Measurable | Pode ser capturada com dados existentes ou planejados | "Temos como coletar esse dado?" |
| **A** — Achievable | Meta e realista dado o contexto | "Alguem ja alcancou algo parecido?" |
| **R** — Relevant | Conectada diretamente ao problema | "Se melhorar, o problema diminui?" |
| **T** — Time-bound | Tem prazo para avaliacao | "Quando medimos?" |

---

## Leading vs Lagging Indicators

| Tipo | O que mede | Quando usar | Exemplo |
|------|-----------|-------------|---------|
| **Leading** | Comportamento que prediz resultado | Feedback rapido (dias/semanas) | Taxa de adocao da feature, cliques no novo botao |
| **Lagging** | Resultado final desejado | Confirmacao de impacto (semanas/meses) | Reducao de churn, aumento de receita |

**Recomendacao**: inclua pelo menos 1 leading + 1 lagging para features importantes.

### Exemplos por Tipo

**Feature de dashboard financeiro:**
- Leading: % de usuarios que acessam dashboard semanalmente
- Lagging: Reducao de tempo gasto gerando relatorios manuais

**Feature de onboarding:**
- Leading: % de usuarios que completam setup em 1 sessao
- Lagging: Reducao de churn nos primeiros 30 dias

---

## 3 Camadas de Metricas

Toda feature deve ter metricas organizadas em 3 camadas distintas. Isso previne otimizacoes que quebram outras areas.

| Camada | Proposito | Pergunta-chave |
|--------|-----------|----------------|
| **Metrica Primaria** | O que otimizar — o resultado principal desejado | "Qual numero UNICO define sucesso?" |
| **Metricas Secundarias** | Indicadores complementares que suportam a primaria | "Que sinais confirmam que estamos no caminho certo?" |
| **Metricas Guardrail** | O que NAO pode piorar ao otimizar a primaria | "O que pode quebrar se focarmos demais na primaria?" |

### Por que Guardrail Metrics importam

Quando otimizamos uma metrica primaria, e comum degradar outras areas sem perceber. Guardrail metrics definem limites que NAO podem ser ultrapassados.

**Exemplos de Guardrail Metrics por tipo de projeto:**

| Tipo de Projeto | Guardrail Metric | Limite |
|-----------------|-----------------|--------|
| SaaS | NPS do modulo afetado | Nao cai abaixo de X |
| SaaS | Tempo de resposta da API | < 500ms P95 |
| Ferramenta interna | Processo atual nao para durante migracao | Zero downtime |
| Financeiro | Erros de calculo de comissao | Zero erros |
| Financeiro | Tempo de carregamento do dashboard | < 2s |
| E-commerce | Taxa de conversao existente | Nao cai mais que 2% |

### Complementaridade com Leading/Lagging

As 3 camadas sao COMPLEMENTARES a classificacao Leading/Lagging (nao substituem). Uma metrica pode ser:
- Primaria + Lagging (ex: "Reducao de churn em 30 dias")
- Secundaria + Leading (ex: "Adocao do dashboard em 7 dias")
- Guardrail + Lagging (ex: "NPS nao cai abaixo de 7")

---

## Formato de Tabela (3 Camadas)

```markdown
## Objetivos & Metricas

### Metrica Primaria
| Metrica | Atual | Meta | Prazo |
|---------|-------|------|-------|
| [O que otimizar] | [baseline] | [target] | [quando medir] |

### Metricas Secundarias
| Metrica | Atual | Meta | Prazo |
|---------|-------|------|-------|
| [Indicador complementar 1] | ... | ... | ... |
| [Indicador complementar 2] | ... | ... | ... |

### Metricas Guardrail (NAO podem piorar)
| Metrica | Valor Atual | Limite Minimo Aceitavel |
|---------|-------------|------------------------|
| [O que proteger] | [baseline] | [threshold] |
```

### Exemplo Completo (Dashboard Financeiro)

```markdown
### Metrica Primaria
| Metrica | Atual | Meta | Prazo |
|---------|-------|------|-------|
| Tempo medio de conciliacao financeira | 3h/semana | < 30min/semana | 60 dias pos-lancamento |

### Metricas Secundarias
| Metrica | Atual | Meta | Prazo |
|---------|-------|------|-------|
| Adocao do dashboard por parceiros | 0% | > 70% | 30 dias pos-lancamento |
| Tickets de suporte sobre discrepancias | 47/mes | < 10/mes | 90 dias pos-lancamento |

### Metricas Guardrail (NAO podem piorar)
| Metrica | Valor Atual | Limite Minimo Aceitavel |
|---------|-------------|------------------------|
| Erros de calculo de comissao | ~5/mes | 0 (zero tolerancia) |
| Tempo de carregamento do dashboard | 1.2s | < 2s |
```

---

## Exemplos por Tipo de Projeto

### SaaS Multi-tenant
- Adocao: % de tenants usando a feature em 30 dias
- Retencao: Reducao de churn mensal
- Eficiencia: Tempo medio por tarefa (antes vs depois)

### Ferramenta Interna
- Produtividade: Horas economizadas por semana
- Erros: Reducao de erros manuais
- Adocao: % do time usando a ferramenta vs processo antigo

### API / Integracao
- Confiabilidade: Taxa de sucesso das chamadas (>99.5%)
- Latencia: P95 response time (<500ms)
- Adocao: Numero de integradores ativos

### Automacao (n8n, webhooks)
- Execucao: Taxa de sucesso dos workflows (>99%)
- Economia: Horas manuais eliminadas por mes
- Velocidade: Tempo entre evento e acao automatizada

---

## Anti-Patterns

| Anti-pattern | Problema | Correcao |
|-------------|----------|----------|
| "Melhorar UX" | Nao e mensuravel | "Reduzir tempo de tarefa X de 5min para 1min" |
| "Aumentar satisfacao" | Vago, sem baseline | "NPS do modulo financeiro de 6 para 8" |
| "Performance aceitavel" | Subjetivo | "P95 < 2s com 10.000 registros" |
| Sem baseline (valor atual) | Impossivel medir progresso | Sempre incluir valor atual, mesmo se estimado |
| Meta sem prazo | Nunca sera cobrada | Sempre incluir timeframe |

---

## OKRs vs Metas Simples

**Use metas simples** (tabela acima) quando:
- Feature isolada, 1 sprint a 1 mes
- PRD nivel Lean ou Standard

**Use OKRs** quando:
- Iniciativa de quarter+ com multiplas features
- PRD nivel Comprehensive
- Alinhamento cross-team necessario

```markdown
**Objective**: Parceiros tem visibilidade financeira completa sem depender do admin

- KR1: 80% dos parceiros acessam dashboard semanalmente (30 dias)
- KR2: Tickets de suporte sobre financeiro reduzem 60% (90 dias)
- KR3: Zero erros de calculo de comissao reportados (60 dias)
```

---

## Checklist de Validacao

- [ ] Pelo menos 1 metrica de sucesso definida?
- [ ] Metricas sao SMART (especificas, mensuraveis, com prazo)?
- [ ] Baseline (valor atual) incluido, mesmo se estimado?
- [ ] Meta e realista dado o contexto?
- [ ] Metrica conectada diretamente ao problema descrito na secao anterior?
- [ ] Metrica primaria claramente identificada (1 unica)?
- [ ] Metricas guardrail definidas (o que NAO pode piorar)?
- [ ] 3 camadas presentes: Primaria + Secundarias + Guardrail?
