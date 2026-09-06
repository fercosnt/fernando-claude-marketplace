# Sistema de Avaliacao de Qualidade — Scorecard Completo

## Indice

1. [Visao Geral](#1-visao-geral)
2. [Dimensao 1: Clareza e Comunicacao](#2-dimensao-1)
3. [Dimensao 2: Tecnicas e Estrutura](#3-dimensao-2)
4. [Dimensao 3: Otimizacao de Plataforma](#4-dimensao-3)
5. [Dimensao 4: Completude e Robustez](#5-dimensao-4)
6. [Calculo e Classificacao](#6-calculo)
7. [Thresholds e Acoes](#7-thresholds)
8. [Template Visual](#8-template-visual)
9. [Guia de Remediacao](#9-remediacao)

---

## 1. Visao Geral

O scorecard avalia prompts em 4 dimensoes com pesos diferenciados, sub-metricas com multiplicadores de importancia, e penalidades para falhas criticas.

**Quando usar o scorecard completo:**
- Prompts para producao (vao ser usados repetidamente)
- Prompts criticos (impactam negocios, clientes, ou automacoes)
- Quando o prompt falhou e precisa de diagnostico

**Quando usar avaliacao rapida (5 criterios no SKILL.md):**
- Prompts simples ou one-off
- Iteracao rapida onde velocidade importa mais que rigor

---

## 2. Dimensao 1: Clareza e Comunicacao (35%)

A dimensao mais importante. Prompts confusos produzem resultados confusos.

### Naturalidade e Fluidez (peso 3x)

| Score | Descricao |
|-------|-----------|
| 9-10 | Leitura natural, conversacional, zero jargao desnecessario |
| 7-8 | Claro e direto, ocasionalmente tecnico demais |
| 5-6 | Funcional mas robotico, requer releitura |
| 3-4 | Confuso, estrutura fragmentada |
| 1-2 | Incompreensivel |

**O que avaliar:**
- Linguagem natural vs robotica?
- Tom apropriado para o audience?
- Livre de jargao desnecessario?
- Facil de entender na primeira leitura?

### Instrucoes Explicitas com Contexto (peso 2.5x)

| Score | Descricao |
|-------|-----------|
| 9-10 | Toda instrucao tem PORQUE. Zero ambiguidade. |
| 7-8 | Maioria tem justificativa. Poucas ambiguidades menores. |
| 5-6 | Instrucoes claras mas sem contexto do porque. |
| 3-4 | Instrucoes vagas. Multiplas interpretacoes possiveis. |
| 1-2 | Instrucoes contraditorias ou ausentes. |

**O que avaliar:**
- Cada instrucao tem justificativa (o PORQUE)?
- Contexto suficiente para decisoes em edge cases?
- Zero ambiguidades criticas?

### Especificidade sem Over-Engineering (peso 2x)

| Score | Descricao |
|-------|-----------|
| 9-10 | Equilibrio perfeito: detalhado onde importa, flexivel onde nao |
| 7-8 | Bom balanco com leves excessos em um sentido |
| 5-6 | Muito vago OU muito prescritivo |
| 3-4 | Claramente sub ou super especificado |
| 1-2 | Totalmente aberto OU microgerencia cada decisao |

---

## 3. Dimensao 2: Tecnicas e Estrutura (30%)

Avalia o uso correto das tecnicas de prompt engineering.

### XML Structuring (peso 3x)

| Score | Descricao |
|-------|-----------|
| 9-10 | Tags semanticas separando todos os componentes. Nomes descritivos. |
| 7-8 | XML usado mas com gaps (faltam tags em algumas secoes). |
| 5-6 | Separacao basica, sem XML ou com tags genericas. |
| 3-4 | Dados misturados com instrucoes. |
| 1-2 | Bloco monolitico sem qualquer estrutura. |

### Tecnicas Aplicadas (peso 2.5x)

| Score | Descricao |
|-------|-----------|
| 9-10 | Tecnicas corretas para a tarefa. Combinacoes eficazes. |
| 7-8 | Tecnicas adequadas com pequenas oportunidades perdidas. |
| 5-6 | Tecnicas basicas, faltam as que mais beneficiariam. |
| 3-4 | Tecnicas erradas para a tarefa ou ausentes. |
| 1-2 | Nenhuma tecnica de prompt engineering. |

**Checklist rapido:**
- CoT presente em tarefa de raciocinio?
- Exemplos present em tarefa de formato?
- Role definido quando expertise importa?
- Chaining usado quando ha 3+ passos?

### Exemplos e Demonstracoes (peso 2x)

| Score | Descricao |
|-------|-----------|
| 9-10 | 2-5 exemplos relevantes, diversos, anotados ("por que e bom"). |
| 7-8 | Exemplos presentes e uteis, sem anotacao. |
| 5-6 | 1 exemplo basico ou exemplos genericos. |
| 3-4 | Exemplos irrelevantes ou mal formulados. |
| 1-2 | Sem exemplos em tarefa que precisa. |

### Anti-Patterns e Validacao (peso 1.5x)

| Score | Descricao |
|-------|-----------|
| 9-10 | Triade DO/DON'T/VERIFY completa e especifica. |
| 7-8 | DO e DON'T presentes, sem VERIFY. |
| 5-6 | Apenas instrucoes positivas (sem anti-patterns). |
| 3-4 | Anti-patterns obvios nao mencionados. |
| 1-2 | Sem qualquer guideline de qualidade. |

---

## 4. Dimensao 3: Otimizacao de Plataforma (20%)

Avalia se o prompt aproveita as capacidades da plataforma-alvo.

### Claude Desktop (peso 3x se target)

| Score | Descricao |
|-------|-----------|
| 9-10 | Prepara para artifacts, tools, adaptive thinking (com effort adequado) quando relevante. |
| 7-8 | Aproveita features principais, ignora secundarias. |
| 5-6 | Funcional mas nao aproveita a plataforma. |
| 3-4 | Ignora capabilities. Poderia ser para qualquer LLM. |

### Claude Code (peso 3x se target)

| Score | Descricao |
|-------|-----------|
| 9-10 | Principios de persuasao, progressive disclosure, graus de liberdade adequados. |
| 7-8 | Boa estrutura de skill/hook, faltam refinamentos. |
| 5-6 | Funcional mas nao segue padroes do Claude Code. |
| 3-4 | Ignora convencoes da plataforma. |

### N8N (peso 3x se target)

| Score | Descricao |
|-------|-----------|
| 9-10 | Conciso, deterministico, output parseavel, fallbacks definidos. |
| 7-8 | Boa estrutura, faltam fallbacks ou formato de output rigoroso. |
| 5-6 | Funcional mas verbose demais para automacao. |
| 3-4 | Prompt de conversacao usado em contexto de automacao. |

### Iteracao e Refinamento (peso 2x)

| Score | Descricao |
|-------|-----------|
| 9-10 | Protocolo de iteracao embutido. Perguntas de feedback especificas. |
| 7-8 | Menciona refinamento, sem protocolo especifico. |
| 5-6 | Assume output perfeito na primeira vez. |
| 3-4 | Nenhuma consideracao de iteracao. |

---

## 5. Dimensao 4: Completude e Robustez (15%)

### Cobertura de Edge Cases (peso 3x)

| Score | Descricao |
|-------|-----------|
| 9-10 | Fallbacks para inputs inesperados. Instrucoes para ambiguidade. |
| 7-8 | Cobre casos principais, faltam edge cases raros. |
| 5-6 | Funciona para happy path, quebra em variantes. |
| 3-4 | Funciona so para o exemplo exato imaginado. |

### Prevencao de Alucinacao (peso 2.5x)

| Score | Descricao |
|-------|-----------|
| 9-10 | "Saida" explicita, grounding em evidencia, verificacao embutida. |
| 7-8 | Alguma prevencao mas nao sistematica. |
| 5-6 | Nenhuma prevencao explicita. |
| 3-4 | Incentiva resposta mesmo sem certeza. |

### Rastreabilidade (peso 1.5x)

| Score | Descricao |
|-------|-----------|
| 9-10 | Fontes documentadas, decisoes justificadas, versionavel. |
| 7-8 | Alguma documentacao de decisoes. |
| 5-6 | Prompt funcional sem contexto de criacao. |
| 3-4 | Impossivel entender por que foi estruturado assim. |

---

## 6. Calculo e Classificacao

### Formula

```python
def calcular_score(dimensoes):
    pesos = {
        'clareza': 0.35,         # Dimensao 1
        'tecnicas': 0.30,        # Dimensao 2
        'plataforma': 0.20,      # Dimensao 3
        'completude': 0.15       # Dimensao 4
    }

    score_final = sum(
        dimensoes[dim] * peso
        for dim, peso in pesos.items()
    )

    # Penalidades
    if alguma_metrica_critica < 6.0:
        score_final *= 0.85  # -15%

    if nao_otimizado_para_plataforma:
        score_final *= 0.90  # -10%

    return min(score_final, 10.0)
```

### Metricas Criticas (que disparam penalidade de -15%)

- Naturalidade e Fluidez < 6.0
- Instrucoes Explicitas < 6.0
- XML Structuring < 5.0 (se prompt complexo)
- Plataforma target < 5.0

### Classificacao

| Score | Rating |
|-------|--------|
| >= 9.0 | Elite — Pronto para producao, excelencia |
| >= 8.0 | Profissional — Alta qualidade |
| >= 7.0 | Competente — Solido, funcional |
| >= 6.0 | Em desenvolvimento — Precisa refinamento |
| < 6.0 | Inadequado — Revisao major necessaria |

---

## 7. Thresholds e Acoes

| Condicao | Acao |
|----------|------|
| Score >= 8.5 + todas metricas >= 7.0 | Aprovacao automatica |
| Score >= 7.5 | Aprovado com sugestoes opcionais |
| Score < 7.5 | Iteracao obrigatoria |
| Qualquer metrica critica < 6.0 | BLOQUEADO — corrigir antes de entregar |

---

## 8. Template Visual

```
AVALIACAO: [X.X/10] - [Rating]

Dim 1: Clareza e Comunicacao (35%)
  |-- Naturalidade e Fluidez: [X/10] (3x)
  |-- Instrucoes com Contexto: [X/10] (2.5x)
  +-- Especificidade: [X/10] (2x)
  Subtotal: [X.X/10]

Dim 2: Tecnicas e Estrutura (30%)
  |-- XML Structuring: [X/10] (3x)
  |-- Tecnicas Aplicadas: [X/10] (2.5x)
  |-- Exemplos: [X/10] (2x)
  +-- Anti-Patterns/VERIFY: [X/10] (1.5x)
  Subtotal: [X.X/10]

Dim 3: Otimizacao Plataforma (20%)
  |-- Features da Plataforma: [X/10] (3x)
  +-- Iteracao: [X/10] (2x)
  Subtotal: [X.X/10]

Dim 4: Completude e Robustez (15%)
  |-- Edge Cases: [X/10] (3x)
  |-- Anti-alucinacao: [X/10] (2.5x)
  +-- Rastreabilidade: [X/10] (1.5x)
  Subtotal: [X.X/10]

SCORE FINAL: [X.X/10]
CLASSIFICACAO: [Rating]

Pontos de Atencao:
[Metricas < 7.0]

Pontos Fortes:
[Metricas >= 9.0]
```

---

## 9. Guia de Remediacao

### Se Score < 7.5

1. Identifique a dimensao mais fraca
2. Consulte a tabela de diagnostico abaixo
3. Aplique max 3 mudancas de maior impacto
4. Re-avalie

### Tabela de Diagnostico

| Dimensao Fraca | Causa Tipica | Correcao Prioritaria |
|---------------|-------------|---------------------|
| Clareza baixa | Instrucoes vagas, sem PORQUE | Adicionar justificativas a cada instrucao |
| Tecnicas baixa | Sem CoT/Examples quando necessario | Adicionar tecnica mais impactante para o caso |
| Plataforma baixa | Prompt generico para qualquer LLM | Customizar para features da plataforma target |
| Completude baixa | Happy path only | Adicionar fallbacks e "so responda se souber" |

### Sintomas Comuns

| Sintoma no Uso | Causa | Solucao |
|---------------|-------|---------|
| Respostas inconsistentes entre execucoes | Falta de exemplos | Add 2-3 few-shot |
| Claude pula passos | Prompt monolitico | Quebrar em chain ou add CoT |
| Tom errado na resposta | Role generico | Especificar role com dominio |
| Respostas vagas/genericas | Falta de contexto | Add cenario e audience |
| Inventa fatos | Sem grounding | Add "cite fontes" e saida para incerteza |
| Formato inconsistente | Sem XML output spec | Add tags de output + prefill |
| Resposta muito longa | Sem restricao de tamanho | "Max X palavras" ou "Exatamente N bullets" |
