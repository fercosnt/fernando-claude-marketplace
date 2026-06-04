# Template de Documento de Analise

## Instrucoes de Uso

- Preencha os placeholders `[entre colchetes]`
- Remova secoes nao aplicaveis (ex: Analise Comparativa se nao houve comparacao)
- Mantenha a numeracao e formatacao consistentes
- Cada score DEVE ter evidencia citada (trecho da skill analisada)
- Mostre o calculo completo — usuario deve poder verificar a matematica

---

## Template Completo

```markdown
# Analise de Qualidade: Skill `[nome-da-skill]`

**Data da Analise:** [YYYY-MM-DD]
**Skill Analisada:** `[path completo da skill]`
**Metodo:** Scorecard de 4 dimensoes com 16 sub-metricas (skill-analyzer)
**Score Final:** [X.X/10] — [Classificacao]

---

## 1. Fontes de Referencia Usadas

| Documento | Papel na Analise |
|-----------|-----------------|
| `[arquivo ou reference]` | [como informou a avaliacao] |
| `references/dimensoes-scorecard.md` | Rubricas de avaliacao (16 sub-metricas) |
| `references/skill-patterns.md` | Padroes de referencia para comparacao |
| [outros materiais consultados] | [papel] |

---

## 2. Estrutura da Skill Analisada

```
[path-da-skill]/
├── SKILL.md                              ([N] linhas)
├── references/
│   ├── [arquivo-1.md]                    ([N] linhas)
│   ├── [arquivo-2.md]                    ([N] linhas)
│   └── ...
├── scripts/                              (se existir)
│   └── [arquivo]                         ([N] linhas)
└── assets/                               (se existir)
    └── [arquivo]

Total: [N] arquivos, ~[N] linhas
```

---

## 3. Avaliacao por Dimensao

### Dim 1: Arquitetura da Skill (25%)

#### Estrutura de Arquivos: [X/10] (peso 3x)

**Pontos fortes:**
- [Ponto com evidencia direta da skill]

**Gaps identificados:**
- [Gap com evidencia e comparacao com padrao esperado]

**Evidencia da skill:**
> [Citacao direta de trecho relevante]

---

#### Metadata e Trigger: [X/10] (peso 2.5x)

**Pontos fortes:**
- [Ponto com evidencia]

**Gaps identificados:**
- [Gap com evidencia]

**Teste de trigger:**
- Pedido 1: "[forma alternativa]" — Aciona? [SIM/NAO]
- Pedido 2: "[forma alternativa]" — Aciona? [SIM/NAO]
- Pedido 3: "[forma alternativa]" — Aciona? [SIM/NAO]

---

#### Tamanho e Eficiencia: [X/10] (peso 2x)

**Metricas:**
- SKILL.md: [N] linhas (benchmark: <500)
- Total com references: [N] linhas
- Conteudo que poderia ser movido: [sim/nao, detalhar]

**Subtotal Dim 1: [X.X/10]**

---

### Dim 2: Qualidade das Instrucoes (30%)

#### Clareza e Naturalidade: [X/10] (peso 3x)

**Pontos fortes:**
- [Ponto com evidencia]

**Gaps identificados:**
- [Gap com evidencia]

**Evidencia da skill:**
> [Citacao de trecho que exemplifica o score]

---

#### Contexto e Justificativas: [X/10] (peso 2.5x)

**Metricas:**
- Instrucoes com PORQUE: [N]/[total] ([N]%)
- Numeros arbitrarios sem justificativa: [listar se houver]

**Exemplos de boas justificativas encontradas:**
> [Citacao]

**Exemplos de regras sem justificativa:**
> [Citacao, se houver]

---

#### Especificidade vs Liberdade: [X/10] (peso 2x)

**Analise dos graus de liberdade:**
- Alta liberdade (onde): [descricao]
- Media liberdade (onde): [descricao]
- Baixa liberdade (onde): [descricao]
- Equilibrio adequado? [sim/nao, justificar]

---

#### Anti-Patterns e Guardas: [X/10] (peso 1.5x)

**Guardas encontradas:**
- DO: [listar]
- DON'T: [listar]
- VERIFY: [listar ou "ausente"]

**Anti-patterns nomeados:** [N] com justificativa / [N] sem

**Subtotal Dim 2: [X.X/10]**

---

### Dim 3: Cobertura Funcional (25%)

#### Workflow e Modos: [X/10] (peso 3x)

**Modos detectados:** [listar modos e como sao ativados]
**Completude do workflow:**
- Inicio definido? [sim/nao]
- Passos sequenciais claros? [sim/nao]
- Fim/entrega definida? [sim/nao]
- Transicoes entre passos? [sim/nao]

---

#### Exemplos e Demonstracoes: [X/10] (peso 2.5x)

**Inventario de exemplos:**

| # | Tipo | Concreto? | Anotado? | Modo coberto |
|---|------|-----------|----------|-------------|
| 1 | [tipo] | [sim/nao] | [sim/nao] | [modo] |
| ... | | | | |

**Total:** [N] exemplos, [N] concretos, [N] anotados

---

#### Edge Cases e Fallbacks: [X/10] (peso 2x)

**Edge cases cobertos:**
- [caso]: [como trata]

**Edge cases ausentes:**
- [caso]: [por que seria importante]

---

#### Output e Entrega: [X/10] (peso 1.5x)

**Formato de entrega:** [definido/implicito/ausente]
**Template de output:** [presente/ausente]
**Checklist pre-entrega:** [presente/ausente]
**Metadata no output:** [presente/ausente]

**Subtotal Dim 3: [X.X/10]**

---

### Dim 4: Ecossistema e Manutencao (20%)

#### References e Recursos: [X/10] (peso 3x)

**Inventario:**

| Reference | Linhas | Proposito | Referenciado no SKILL.md? |
|-----------|--------|-----------|--------------------------|
| [arquivo] | [N] | [proposito] | [sim/nao] |

**Arquivos orfaos:** [listar se houver]

---

#### Integracao com Plataforma: [X/10] (peso 2.5x)

**Features do Claude Code utilizadas:**
- [feature]: [como usa]

**Oportunidades nao aproveitadas:**
- [feature]: [como poderia usar]

---

#### Consistencia Interna: [X/10] (peso 2x)

**Verificacoes:**
- Pratica o que prega? [sim/nao, detalhar]
- Cross-references validos? [sim/nao]
- Contradicoes encontradas? [listar se houver]

---

#### Evolucao: [X/10] (peso 1.5x)

**Modularidade:** [alta/media/baixa]
**Facilidade de iteracao:** [facil/media/dificil]
**Extensibilidade:** [preparada/limitada]

**Subtotal Dim 4: [X.X/10]**

---

## 4. Calculo do Score Final

### Formula Aplicada

```
score = (arquitetura × 0.25) + (instrucoes × 0.30) + (cobertura × 0.25) + (ecossistema × 0.20)
score = ([X.X] × 0.25) + ([X.X] × 0.30) + ([X.X] × 0.25) + ([X.X] × 0.20)
score = [parcial] + [parcial] + [parcial] + [parcial]
score = [total]
```

### Penalidades

| Condicao | Aplicavel? | Penalidade |
|----------|-----------|------------|
| Sub-metrica critica < 5.0 | [SIM/NAO — qual?] | [x 0.85 ou N/A] |
| Reference ausente para funcionalidade core | [SIM/NAO — qual?] | [x 0.90 ou N/A] |
| Description nao aciona corretamente | [SIM/NAO] | [x 0.90 ou N/A] |
| SKILL.md > 800 linhas sem references | [SIM/NAO] | [x 0.95 ou N/A] |

```
score_final = [raw] × [penalidades]
score_final = [resultado]
```

---

## 5. Resultado Consolidado

```
AVALIACAO: [X.X/10] - [Classificacao]

Dim 1: Arquitetura da Skill (25%)
  |-- Estrutura de Arquivos:     [X/10] (3x)
  |-- Metadata e Trigger:        [X/10] (2.5x)
  +-- Tamanho e Eficiencia:      [X/10] (2x)
  Subtotal: [X.X/10]

Dim 2: Qualidade das Instrucoes (30%)
  |-- Clareza e Naturalidade:    [X/10] (3x)
  |-- Contexto e Justificativas: [X/10] (2.5x)
  |-- Especificidade vs Liberdade:[X/10] (2x)
  +-- Anti-Patterns e Guardas:   [X/10] (1.5x)
  Subtotal: [X.X/10]

Dim 3: Cobertura Funcional (25%)
  |-- Workflow e Modos:          [X/10] (3x)
  |-- Exemplos e Demonstracoes:  [X/10] (2.5x)
  |-- Edge Cases e Fallbacks:    [X/10] (2x)
  +-- Output e Entrega:          [X/10] (1.5x)
  Subtotal: [X.X/10]

Dim 4: Ecossistema e Manutencao (20%)
  |-- References e Recursos:     [X/10] (3x)
  |-- Integracao Plataforma:     [X/10] (2.5x)
  |-- Consistencia Interna:      [X/10] (2x)
  +-- Evolucao:                  [X/10] (1.5x)
  Subtotal: [X.X/10]

SCORE BRUTO:  [X.X/10]
PENALIDADE:   [detalhes ou "nenhuma"]
SCORE FINAL:  [X.X/10]
CLASSIFICACAO: [Rating — descricao]
```

---

## 6. Pontos Fortes

| Metrica | Score | Destaque |
|---------|-------|---------|
| [metrica com score >= 8] | [X/10] | [o que faz bem] |
| [metrica com score >= 8] | [X/10] | [o que faz bem] |

---

## 7. Pontos de Atencao

| Metrica | Score | Problema |
|---------|-------|---------|
| [metrica com score < 7] | [X/10] | [qual e o gap] |
| [metrica com score < 7] | [X/10] | [qual e o gap] |

---

## 8. Plano de Melhoria

### Fase 1: [Descricao — ex: "Eliminar penalidades + maiores gaps"]

| # | Task | Sub-metrica | Atual -> Projetado | Impacto | Esforco | Detalhes |
|---|------|-------------|-------------------|---------|---------|----------|
| 1 | **[Nome da task]** | [sub-metrica] | [X -> Y] | [+N.N pts] | [B/M/A] | [o que fazer especificamente] |
| 2 | **[Nome da task]** | [sub-metrica] | [X -> Y] | [+N.N pts] | [B/M/A] | [detalhes] |

### Fase 2: [Descricao]

| # | Task | Sub-metrica | Atual -> Projetado | Impacto | Esforco | Detalhes |
|---|------|-------------|-------------------|---------|---------|----------|
| [N] | **[Nome]** | [sub-metrica] | [X -> Y] | [+N.N pts] | [B/M/A] | [detalhes] |

[Repetir fases conforme necessario]

### Mapa de Dependencias

| Task | Depende de | Motivo |
|------|-----------|--------|
| [N] | [N ou "nenhuma"] | [motivo] |

### Substituicoes (se houver)

| Task Original | Substituida por | Mudanca |
|--------------|----------------|---------|
| Task [N] (scope basico) | Task [M] (scope expandido) | [o que mudou] |

### Projecao de Score

| Cenario | Score Estimado | Classificacao |
|---------|---------------|---------------|
| Estado atual | [X.X] | [classe] |
| Fase 1 implementada | [X.X] | [classe] |
| Fases 1-2 implementadas | [X.X] | [classe] |
| Todas as fases | [X.X] | [classe] |

---

## 9. Tasklist de Implementacao

> Checkboxes acionaveis para o usuario acompanhar progresso das melhorias.

### Fase 1: [Descricao]
- [ ] [Task 1: descricao especifica do que fazer]
- [ ] [Task 2: descricao especifica do que fazer]

### Fase 2: [Descricao]
- [ ] [Task N: descricao especifica do que fazer]

### Fase 3: [Descricao] (se aplicavel)
- [ ] [Task N: descricao especifica do que fazer]

### Validacao Final
- [ ] Rodar checklist rapido da skill-analyzer para verificar melhorias
- [ ] Confirmar que score projetado foi atingido

---

## 10. Analise Comparativa (se aplicavel)

> Incluir apenas se usuario forneceu skill de referencia ou concorrente.

| Aspecto | [Skill Analisada] | [Skill Referencia] | Vantagem |
|---------|-------------------|-------------------|----------|
| Score total | [X.X] | [X.X] | [A/B] |
| Arquitetura | [X.X] | [X.X] | [A/B] |
| Instrucoes | [X.X] | [X.X] | [A/B] |
| Cobertura | [X.X] | [X.X] | [A/B] |
| Ecossistema | [X.X] | [X.X] | [A/B] |
| Destaque unico | [diferencial] | [diferencial] | — |

**Conclusao:** [Sao complementares? Uma e superior? Em que cenarios cada uma brilha?]

---

## 11. Conclusao

[Paragrafo sintetizando:]
- Fundamentos da skill (o que tem de solido)
- Principal bloqueador (o que mais precisa de atencao)
- Caminho para melhoria (resumo do plano em 1-2 frases)
- Projecao final (se todas as melhorias forem implementadas, score estimado)

---

*Analise realizada usando skill-analyzer v1.0 (scorecard de 4 dimensoes, 16 sub-metricas ponderadas).*
```
