# Frameworks de Prompt Engineering — Guia de Selecao

## Indice

1. [Quando Usar Qual Framework](#1-selecao-rapida)
2. [CO-STAR](#2-co-star)
3. [TIDD-EC](#3-tidd-ec)
4. [RISEN](#4-risen)
5. [RTF](#5-rtf)
6. [Chain of Thought](#6-chain-of-thought)
7. [Chain of Density](#7-chain-of-density)
8. [Combinacoes](#8-combinacoes)

---

## 1. Selecao Rapida

| Tarefa | Framework | Porque |
|--------|-----------|--------|
| Blog post, email, conteudo | **CO-STAR** | Audience e tom importam |
| Atendimento, documentacao tecnica | **TIDD-EC** | Precisa de DO/DON'T explicitos |
| Processo complexo com etapas | **RISEN** | Metodologia e restricoes importam |
| Tarefa simples e direta | **RTF** | Formato e a principal preocupacao |
| Raciocinio, analise, matematica | **Chain of Thought** | Precisa de passos logicos |
| Sumarizacao iterativa | **Chain of Density** | Refinamento progressivo |
| Nao sabe qual usar | **Estrutura base do SKILL.md** | A estrutura generica funciona para 80% dos casos |

---

## 2. CO-STAR

**Context, Objective, Style, Tone, Audience, Response**

Melhor para: Tarefas onde audience e estilo de comunicacao impactam o resultado.

### Template

```
CONTEXT:
[Situacao, background, restricoes]

OBJECTIVE:
[Objetivo claro e mensuravel]

STYLE:
[Estilo de escrita, formato, estrutura]

TONE:
[Qualidade emocional: formal, casual, empatico, urgente]

AUDIENCE:
[Quem vai consumir, nivel de expertise, pain points]

RESPONSE:
[Formato do output, tamanho, secoes]
```

### Exemplo

```
CONTEXT:
Criando conteudo para blog de saude. Publico: profissionais que trabalham 50+ horas/semana.

OBJECTIVE:
Artigo que convenca profissionais ocupados a priorizar exercicio, focando em beneficios alem da saude fisica.

STYLE:
Blog conversacional. Paragrafos curtos (2-3 frases). Subheadings a cada 150-200 palavras. Sem jargao medico.

TONE:
Motivacional sem ser condescendente. Reconhecer falta de tempo. Pratico e realista.

AUDIENCE:
Profissionais 30-50 anos, trabalham 50+ horas, com familias, ceticos sobre fitness.

RESPONSE:
Artigo de 800 palavras: headline, intro (2-3 frases), 4-5 secoes com subheadings, conclusao com proximos passos.
```

### Quando usar vs evitar

| Usar | Evitar |
|------|--------|
| Conteudo, marketing, comunicacao | Tarefas puramente analiticas |
| Multiplos stakeholders | Audience nao importa |
| Tom impacta eficacia | Tarefa tecnica simples |
| Consistencia de voz importa | Formato e unica preocupacao |

---

## 3. TIDD-EC

**Task type, Instructions, Do, Don't, Examples, Context**

Melhor para: Tarefas de alta precisao onde erros sao caros.

### Template

```
TASK TYPE:
[Tipo de atividade: analise, geracao, traducao, etc.]

INSTRUCTIONS:
1. [Passo 1]
2. [Passo 2]
3. [Passo 3]

DO:
- [Acao obrigatoria] — porque [razao]
- [Acao obrigatoria] — para [beneficio]

DON'T:
- [Erro a evitar] — pois [consequencia]
- [Erro a evitar] — que causa [problema]

EXAMPLES:
Bom: [exemplo detalhado de output ideal]
Ruim: [exemplo do que evitar]

CONTEXT:
[Background, dados, restricoes do cenario]
```

### Exemplo

```
TASK TYPE:
Resposta de Suporte ao Cliente — Resolucao de Reclamacao

INSTRUCTIONS:
1. Reconheca a frustracao e valide a preocupacao
2. Peca desculpas pelo inconveniente
3. Explique o que aconteceu em termos simples
4. Forneca solucao concreta com prazo
5. Ofereca contato direto para follow-up

DO:
- Use linguagem empatica e profissional
- Personalize com nome do cliente
- Inclua acoes especificas com prazos
- Mantenha entre 150-250 palavras

DON'T:
- Dar desculpas ou transferir culpa
- Usar linguagem template/robotica
- Prometer o que nao pode cumprir
- Incluir jargao tecnico ou codigos de erro
- Usar voz passiva ("erros foram cometidos")

EXAMPLES:
Bom: "Maria, lamento que seu pedido chegou danificado. Entendo a frustracao.
Ja estou enviando reposicao via sedex — chega sexta ate 14h. Reembolso do
original em 24h. Qualquer duvida: maria@empresa.com ou (11) 1234-5678."

Ruim: "Pedimos desculpas pelo inconveniente. Devido a erros de sistema, seu
pedido foi danificado. Contate nosso suporte. Ticket #12345."

CONTEXT:
- Empresa: E-commerce de decoracao
- Cliente: Membro premium, compra regular
- Problema: Item danificado, precisava para evento
- Politica: Reembolso total + reposicao para itens danificados
```

### Quando usar vs evitar

| Usar | Evitar |
|------|--------|
| Limites claros sao necessarios | Tarefa simples (use RTF) |
| Erros comuns precisam prevencao | Liberdade criativa e importante |
| Consistencia de qualidade e critica | Exploracao aberta |
| Dominios regulados (legal, medico) | Sem abordagens certas/erradas claras |

---

## 4. RISEN

**Role, Instructions, Steps, End goal, Narrowing**

Melhor para: Processos complexos com multiplas etapas e metodologia definida.

### Template

```
ROLE:
[Papel especializado com expertise]

INSTRUCTIONS:
[Principios e guidelines gerais]

STEPS:
1. [Etapa 1] — [o que produz]
2. [Etapa 2] — [o que produz]
3. [Etapa 3] — [o que produz]

END GOAL:
[Resultado final desejado com criterios de sucesso]

NARROWING:
[Restricoes, limites, escopo que deve ser respeitado]
```

### Quando usar vs evitar

| Usar | Evitar |
|------|--------|
| Processos multi-step sequenciais | Tarefas de passo unico |
| Metodologia importa | Resultado unico importa mais que processo |
| Restricoes de escopo sao criticas | Sem limites necessarios |

---

## 5. RTF

**Role, Task, Format**

Melhor para: Tarefas simples e diretas onde formato e a principal preocupacao.

### Template

```
ROLE:
[Papel/expertise necessaria]

TASK:
[Tarefa exata e especifica]

FORMAT:
[Formato de output desejado]
```

### Exemplo

```
ROLE: Redator tecnico senior

TASK: Escreva uma descricao de produto para landing page.
Produto: App de gestao financeira pessoal.
Destaque: Simplicidade e automacao.

FORMAT: 3 paragrafos de 2-3 frases cada.
Primeiro: Hook emocional.
Segundo: Funcionalidades-chave.
Terceiro: Call-to-action.
```

### Quando usar

- Tarefa bem definida e simples
- Formato e a principal variavel
- Nao precisa de DO/DON'T extensos
- Resultado rapido sem overhead de framework pesado

---

## 6. Chain of Thought

Melhor para: Raciocinio complexo, matematica, logica, analise.

### Variantes

**Zero-shot CoT:**
```
[Problema]
Pense passo a passo antes de responder.
```

**Structured CoT:**
```
[Problema]

Em <thinking> tags, raciocine passo a passo:
1. [Passo de raciocinio]
2. [Passo de raciocinio]
3. [Passo de raciocinio]

Depois, em <answer>, forneca sua resposta final.
```

**Few-shot CoT:**
```
<example>
Problema: [problema exemplo]
Raciocinio: [passo 1] → [passo 2] → [passo 3]
Resposta: [resposta]
</example>

Agora resolva: [novo problema]
```

---

## 7. Chain of Density

Melhor para: Sumarizacao onde qualidade melhora com iteracao.

### Template

```
Gere um resumo inicial do texto.
Depois, em 4 rodadas:
- Identifique entidades/detalhes faltantes
- Reescreva o resumo incluindo-os
- Mantenha o mesmo comprimento (~100 palavras)
- Cada versao deve ser mais densa de informacao

Output: As 5 versoes em sequencia.
```

---

## 8. Combinacoes

### CO-STAR + Chain of Thought
Para conteudo complexo que exige raciocinio:
```
[CO-STAR padrao]
PROCESS: Pense passo a passo antes de escrever. Considere multiplas abordagens.
```

### TIDD-EC + Few-Shot
Para precisao maxima:
```
[TIDD-EC padrao com EXAMPLES expandidos para 3-5 exemplos diversos]
```

### RISEN + CO-STAR
Para processos onde audience importa:
```
[RISEN para processo e restricoes]
[CO-STAR para audience e tom do output]
```

### Estrutura base (quando nenhum framework se encaixa)

Use a estrutura generica do SKILL.md principal:
```xml
<role_and_context>...</role_and_context>
<primary_objective>...</primary_objective>
<approach>...</approach>
<output_format>...</output_format>
<examples>...</examples>
<quality_guidelines>...</quality_guidelines>
```

Essa estrutura cobre 80% dos casos sem a rigidez de um framework especifico.
