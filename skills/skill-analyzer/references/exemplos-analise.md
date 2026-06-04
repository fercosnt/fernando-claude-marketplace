# Exemplos Concretos de Analise

Exemplos reais de como avaliar, citar evidencia e calcular scores. Use como referencia para manter consistencia e qualidade no output.

---

## Indice

1. [Exemplo: Scoring de Sub-Metrica com Evidencia](#1-exemplo-scoring-de-sub-metrica-com-evidencia)
2. [Exemplo: Calculo de Subtotal com Numeros Reais](#2-exemplo-calculo-de-subtotal-com-numeros-reais)
3. [Exemplo: Task de Melhoria com ROI](#3-exemplo-task-de-melhoria-com-roi)
4. [Exemplo: Resultado do Modo Rapido](#4-exemplo-resultado-do-modo-rapido)
5. [Exemplo: Tasklist de Implementacao](#5-exemplo-tasklist-de-implementacao)

---

## 1. Exemplo: Scoring de Sub-Metrica com Evidencia

### Avaliacao de "Clareza e Naturalidade" para uma skill hipotetica `data-analyzer`

**Score: 7/10 (peso 3x)**

**Pontos fortes:**
- Forma imperativa consistente nas instrucoes principais
- Headers hierarquicos claros (H2 > H3)
- Tabela de decisao para selecao de modo

**Evidencia da skill:**
> "Leia o arquivo CSV usando pandas. Identifique colunas numericas e categoricas. Gere estatisticas descritivas para cada tipo."

(SKILL.md linhas 34-36 — forma imperativa exemplar)

**Gaps identificados:**
- Secao de "Interpretacao de Resultados" (linhas 89-120) contem paragrafo de 12 linhas sem quebra — parede de texto que prejudica escaneabilidade
- Falta negrito para termos-chave nas instrucoes de configuracao

**Evidencia do gap:**
> "Quando os dados apresentam distribuicao normal voce pode usar a media como medida central mas quando a distribuicao e assimetrica a mediana e mais apropriada e nesse caso voce deve calcular ambas e comparar para decidir qual reportar considerando que outliers podem distorcer significativamente a media..."

(SKILL.md linhas 92-96 — paragrafo longo sem hierarquia visual)

**Por que 7 e nao 8:** A parede de texto na secao de interpretacao e significativa porque e exatamente onde o Claude precisa tomar decisoes — instrucoes enterradas em prosa longa tem maior chance de serem ignoradas.

---

## 2. Exemplo: Calculo de Subtotal com Numeros Reais

### Dimensao 2: Qualidade das Instrucoes (30%)

| Sub-metrica | Score | Peso | Score × Peso |
|-------------|-------|------|-------------|
| Clareza e Naturalidade | 7 | 3x | 21 |
| Contexto e Justificativas | 6 | 2.5x | 15 |
| Especificidade vs Liberdade | 8 | 2x | 16 |
| Anti-Patterns e Guardas | 5 | 1.5x | 7.5 |

```
subtotal = (7 × 3 + 6 × 2.5 + 8 × 2 + 5 × 1.5) / (3 + 2.5 + 2 + 1.5)
subtotal = (21 + 15 + 16 + 7.5) / 9.0
subtotal = 59.5 / 9.0
subtotal = 6.61
```

### Score Final com Penalidade

```
raw = (8.20 × 0.25) + (6.61 × 0.30) + (7.50 × 0.25) + (7.80 × 0.20)
raw = 2.05 + 1.98 + 1.88 + 1.56
raw = 7.47

# Penalidades verificadas:
# - Anti-Patterns e Guardas = 5.0 (nao e sub-metrica critica, sem penalidade)
# - Nenhuma sub-metrica critica < 5.0 ✓
# - References presentes ✓
# - Description aciona ✓
# - SKILL.md < 800 linhas ✓

score_final = 7.47 × 1.0 = 7.47
CLASSIFICACAO: 7.5/10 — Competente
```

---

## 3. Exemplo: Task de Melhoria com ROI

### Task: "Adicionar exemplos concretos em novo reference"

**Sub-metrica alvo:** Exemplos e Demonstracoes (Dim 3, peso 2.5x)
**Score atual:** 3/10 → **Score projetado:** 7/10

**Calculo do impacto:**
```
delta_sub = 7 - 3 = 4
sub_influence = 2.5 / 9.0 = 0.278
dim_influence = 0.25
impacto = 4 × 0.278 × 0.25 = 0.278 pontos no score final
```

**Esforco:** Medio (2) — criar reference com 3+ exemplos concretos
**Dependencias:** Nenhuma
**ROI:** 0.278 / 2 = 0.139

**Detalhes especificos:**
Criar `references/exemplos.md` contendo:
- 1 exemplo completo de input/output do modo principal
- 1 exemplo de edge case tratado
- 1 par before/after mostrando transformacao
- Anotacoes em cada exemplo explicando "por que e bom"

---

## 4. Exemplo: Resultado do Modo Rapido

```
CHECKLIST RAPIDO: data-analyzer
Data: 2026-02-09

 1. Frontmatter valido:          OK  — name e description presentes, YAML valido
 2. Description aciona:          OK  — 8 triggers, cobre "analisar dados", "csv", "estatisticas"
 3. Tamanho adequado:            OK  — 287 linhas SKILL.md + 2 references
 4. Forma imperativa:            OK  — ~85% imperativo consistente
 5. Instrucoes com PORQUE:       FALHA — ~45% com justificativa, muitas regras arbitrarias
 6. Progressive disclosure:      OK  — 2 references tematicos (formatos.md, visualizacao.md)
 7. Workflow completo:            OK  — 5 etapas de leitura a entrega, transicoes claras
 8. Exemplos concretos:          FALHA — 0 exemplos concretos, apenas placeholders
 9. Anti-patterns/guardas:       FALHA — tem DON'T mas sem VERIFY
10. Consistencia interna:        OK  — sem contradicoes encontradas

RESULTADO: 7/10 OK — Ajustes menores

TOP 3 MELHORIAS:
1. Adicionar 2-3 exemplos concretos de output (CSV real → analise gerada)
2. Justificar regras arbitrarias (por que max 10 colunas? por que 3 graficos?)
3. Adicionar checklist de verificacao pre-entrega (VERIFY)
```

---

## 5. Exemplo: Tasklist de Implementacao

Ao final de cada analise, incluir tasklist clara com passos de implementacao para as melhorias sugeridas:

```markdown
## Tasklist de Implementacao

### Fase 1: Ganhos Rapidos (estimativa: 1-2 horas)
- [ ] Adicionar secao `<edge_cases>` no SKILL.md com 5 cenarios de erro
- [ ] Expandir description no frontmatter com 5 triggers adicionais
- [ ] Justificar numeros arbitrarios nas linhas 45, 72, 98

### Fase 2: Exemplos (estimativa: 2-3 horas)
- [ ] Criar `references/exemplos.md`
- [ ] Escrever exemplo completo do modo principal (input → output)
- [ ] Escrever exemplo de edge case tratado
- [ ] Adicionar par before/after com anotacoes

### Fase 3: Refinamentos (estimativa: 1 hora)
- [ ] Adicionar checklist de verificacao pre-entrega
- [ ] Quebrar parede de texto na secao de interpretacao (linhas 89-120)
- [ ] Adicionar negrito para termos-chave

### Validacao Final
- [ ] Rodar checklist rapido da skill-analyzer para verificar melhorias
- [ ] Confirmar que score projetado foi atingido
```

**Por que uma tasklist:** Transforma recomendacoes abstratas em passos acionaveis com checkbox. O usuario pode copiar diretamente para seu sistema de tracking ou seguir passo a passo.
