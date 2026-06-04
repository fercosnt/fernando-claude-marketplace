# Tecnicas Oficiais da Anthropic — Referencia Detalhada

Baseado na documentacao oficial da Anthropic e no tutorial interativo de prompt engineering.

## Indice

1. [Clareza e Especificidade](#1-clareza-e-especificidade)
2. [Multishot / Few-Shot Examples](#2-multishot--few-shot-examples)
3. [Chain of Thought (CoT)](#3-chain-of-thought-cot)
4. [XML Tag Structuring](#4-xml-tag-structuring)
5. [Role Prompting](#5-role-prompting)
6. [Response Prefilling](#6-response-prefilling)
7. [Prompt Chaining](#7-prompt-chaining)
8. [Long Context Optimization](#8-long-context-optimization)
9. [Prevencao de Alucinacao](#9-prevencao-de-alucinacao)
10. [Adaptive Thinking](#10-adaptive-thinking-substitui-extended-thinking)
11. [Structured Outputs e Stop Sequences](#11-structured-outputs-e-stop-sequences)
12. [Variacoes Estrategicas](#12-variacoes-estrategicas)
13. [Combinacoes de Tecnicas](#13-combinacoes-de-tecnicas)

---

## 1. Clareza e Especificidade

**Fundamento:** Claude nao tem memoria da sua organizacao, padroes ou expectativas implicitas. Lacunas na instrucao levam a alucinacoes, formatos inconsistentes ou requisitos perdidos.

**Regra de ouro:** Mostre seu prompt a um colega com contexto minimo. Se ele ficar confuso, Claude tambem ficara.

**Tres pilares:**

| Pilar | O que incluir |
|-------|--------------|
| Contexto | Para que serve, quem e o publico, onde se encaixa no workflow |
| Especificidade | Formato exato, o que incluir/excluir, restricoes |
| Passos sequenciais | Lista numerada do procedimento exato |

**Exemplo — Vago vs Claro:**

```
VAGO: "Remova dados pessoais desse feedback."

CLARO: "Anonimize feedback de clientes para revisao trimestral.
1. Substitua nomes por CLIENTE_[ID] (ex: 'Maria' → 'CLIENTE_001')
2. Substitua emails por EMAIL_[ID]@example.com
3. Redija telefones como FONE_[ID]
4. Se mencionar produto especifico, mantenha intacto
5. Se nao encontrar dados pessoais, copie a mensagem como esta
6. Output: apenas mensagens processadas, separadas por '---'"
```

**Quando usar:** SEMPRE. E a base de todo prompt.

---

## 2. Multishot / Few-Shot Examples

**Fundamento:** Exemplos eliminam ambiguidade de forma mais eficiente que instrucoes sozinhas. Mostram formato, estilo, tom e profundidade esperados.

**Tres requisitos para bons exemplos:**

| Requisito | Descricao |
|-----------|-----------|
| Relevantes | Espelham seu caso de uso real |
| Diversos | Cobrem edge cases e variacoes, evitam overfitting |
| Claros | Envolvidos em `<example>` tags (aninhados em `<examples>`) |

**Exemplo:**

```xml
<examples>
<example>
Input: "O dashboard novo e uma bagunca! Demora pra carregar e nao acho o botao de exportar."
Output:
  Categoria: UI/UX, Performance
  Sentimento: Negativo
  Prioridade: Alta
</example>
<example>
Input: "Adorei a nova feature de relatorios, muito mais rapido!"
Output:
  Categoria: Feature
  Sentimento: Positivo
  Prioridade: Baixa
</example>
</examples>
```

**Dica:** Inclua anotacao "Por que e bom" no exemplo para ensinar o principio, nao so o padrao:

```xml
<example>
Input: [entrada]
Output: [saida]
Por que e bom: Classifica em multiplas categorias quando relevante, nao forca categoria unica.
</example>
```

**Quando usar:** Sempre que precisar de output estruturado, consistente ou em formato especifico. Especialmente eficaz para classificacao, extracao e formatacao.

---

## 3. Chain of Thought (CoT)

**Fundamento:** Raciocinio passo a passo reduz erros em matematica, logica e analise. O processo estruturado produz respostas mais coerentes e defenveis.

**REGRA CRITICA:** Sempre faca Claude externalizar o pensamento. Sem output de raciocinio = sem raciocinio real.

**Tres niveis:**

| Nivel | Metodo | Quando usar |
|-------|--------|-------------|
| Basico | "Pense passo a passo" | Tarefas moderadas, rapido de implementar |
| Guiado | Definir passos especificos de raciocinio | Controle sobre o caminho logico |
| Estruturado | `<thinking>` + `<answer>` XML tags | Maior qualidade, parsing facil |

**Exemplo — CoT Estruturado:**

```
Analise este bug report e determine a causa raiz.

<thinking>
Raciocine passo a passo:
1. Qual e o comportamento esperado?
2. Qual e o comportamento real?
3. O que mudou recentemente?
4. Quais componentes estao envolvidos?
5. Qual a causa mais provavel?
</thinking>

<answer>
[Sua conclusao aqui]
</answer>
```

**Quando usar:** Tarefas que um humano precisaria pensar — matematica complexa, analise multi-fator, decisoes com trade-offs, escrita complexa.

**Quando NAO usar:** Tarefas simples e factuais. CoT aumenta latencia e tokens.

---

## 4. XML Tag Structuring

**Fundamento:** XML tags separam componentes do prompt — instrucoes, dados, exemplos, contexto, formato de output. Claude foi especificamente treinado para reconhecer XML como mecanismo organizador.

**Boas praticas:**

| Pratica | Descricao |
|---------|-----------|
| Nomes semanticos | `<instructions>`, `<data>`, `<formatting_example>` |
| Consistencia | Use mesmos nomes e referencie-os: "Usando o contrato em `<contract>`..." |
| Aninhamento | Hierarquico: `<outer><inner></inner></outer>` |
| Combinacao | `<examples>` para multishot, `<thinking>` para CoT |

**Exemplo:**

```xml
<context>
Voce e analista financeiro na AcmeCorp. Gere relatorio Q2 para investidores.
</context>

<data>{{SPREADSHEET_DATA}}</data>

<instructions>
1. Inclua secoes: Receita, Margens, Fluxo de Caixa
2. Destaque pontos fortes e areas de melhoria
</instructions>

<formatting_example>{{Q1_REPORT}}</formatting_example>
```

**Quando usar:** Qualquer prompt com mais de uma "secao" — instrucoes separadas de dados, exemplos, contexto.

---

## 5. Role Prompting

**Fundamento:** Um papel ativa conhecimento especifico do dominio, ajusta estilo de comunicacao e mantem Claude focado nos limites da tarefa.

**Principio:** Mais especifico = melhor resultado.

| Especificidade | Exemplo |
|---------------|---------|
| Generico | "Voce e um cientista de dados" |
| Melhor | "Voce e um cientista de dados especializado em analise de churn" |
| Ideal | "Voce e o CFO de uma empresa SaaS B2B de alto crescimento" |

**Implementacao:**
- Use `system` prompt para o papel (estavel entre turnos)
- Use mensagem `user` para instrucoes da tarefa (varia por turno)

**Quando usar:** Quando expertise de dominio, vocabulario especializado ou estilo especifico de comunicacao melhorariam o output.

---

## 6. Response Prefilling

**Fundamento:** Semear o inicio da resposta de Claude controlando formato, eliminando preambulos e mantendo consistencia de persona.

**Tres usos principais:**

1. **Forcar JSON:** Prefill com `{`
2. **Eliminar preambulo:** Prefill com a tag de output esperada
3. **Manter persona:** Prefill com `[Nome do Personagem]`

```python
messages=[
    {"role": "user", "content": "Extraia nome, tamanho, preco: <description>...</description>"},
    {"role": "assistant", "content": "{"}  # Forca JSON direto
]
```

**Restricao:** Prefill nao pode terminar com whitespace. Nao suportado com Adaptive Thinking no Opus 4.7 (qualquer prefill de mensagem assistant retorna HTTP 400 — use `output_config.format` em vez disso). Em Sonnet 4.6 e modelos anteriores, prefill continua funcionando quando thinking esta desativado.

**Nota:** Para JSON garantido com schema especifico, use Structured Outputs em vez de prefilling.

---

## 7. Prompt Chaining

**Fundamento:** Quebrar tarefas complexas em sequencia de subtarefas, onde output de cada uma alimenta a proxima. Cada subtarefa recebe atencao total de Claude.

**Quando encadear vs prompt unico:**

| Prompt Unico | Encadeamento |
|-------------|-------------|
| Tarefa simples, objetivo unico | Transformacoes multi-step |
| Instrucoes cabem naturalmente | Pesquisa + sintese + citacoes |
| Operacoes one-pass | Criacao iterativa de conteudo |
| | Claude pula passos em prompt unico |

**Padroes comuns:**

| Padrao | Etapas |
|--------|--------|
| Criacao de conteudo | Pesquisa → Outline → Rascunho → Edicao → Formato |
| Processamento de dados | Extrair → Transformar → Analisar → Visualizar |
| Autocorrecao | Gerar → Revisar (nota A-F) → Refinar |

**Exemplo — Chain de Autocorrecao:**

```
Prompt 1: "Resuma este artigo. Foco em metodologia e achados."
    ↓ {{RESUMO}}
Prompt 2: "Avalie este resumo: preciso, claro, completo? Nota A-F.
    <resumo>{{RESUMO}}</resumo>
    <artigo>{{ARTIGO}}</artigo>"
    ↓ {{FEEDBACK}}
Prompt 3: "Melhore o resumo baseado no feedback.
    <resumo>{{RESUMO}}</resumo>
    <feedback>{{FEEDBACK}}</feedback>"
```

**Quando usar:** Tarefas com 3+ etapas distintas onde qualidade nao pode ser comprometida.

---

## 8. Long Context Optimization

**Fundamento:** Claude tem janelas de contexto grandes — 1M tokens no Opus 4.7 (GA desde abr/2026) e 200K-1M no Sonnet 4.6. Posicionamento e estrutura dos dados impactam qualidade da resposta em ate 30%, e essa sensibilidade aumenta quanto maior o contexto.

> **Nota Opus 4.7 (tokenizer novo):** o tokenizer consome 1.0x-1.35x mais tokens para o mesmo texto vs Opus 4.6. Se voce calcula custo ou define `max_tokens` com base em contagens antigas, adicione ~35% de headroom.

**Tres tecnicas:**

**1. Dados longos no topo, query no final:**
```
[DOCUMENTOS AQUI — 20K+ tokens]
[Sua query e instrucoes ABAIXO dos documentos]
```

**2. Metadata XML para documentos:**
```xml
<documents>
  <document index="1">
    <source>relatorio_anual_2023.pdf</source>
    <document_content>{{RELATORIO}}</document_content>
  </document>
</documents>
```

**3. Grounding em citacoes:**
```
Primeiro extraia citacoes relevantes em <quotes>.
Depois, baseado nessas citacoes, responda em <answer>.
```

---

## 9. Prevencao de Alucinacao

**Fundamento:** Claude tende a ser maximamente util, inventando respostas plausiveis quando nao sabe. Dar permissao para declinar reduz dramaticamente alucinacoes.

**Tecnicas:**

1. **De uma "saida":** "So responda se tiver certeza."
2. **Exija evidencia:** "Em `<scratchpad>`, extraia a citacao mais relevante e avalie se responde a pergunta."
3. **Guie o tom pelo prompt:** em modelos antigos (<= Opus 4.6, Sonnet 4.6 sem adaptive), `temperature=0` funcionava para tarefas factuais. **No Opus 4.7, `temperature`/`top_p`/`top_k` nao-default retornam HTTP 400** — o sampling agora e guiado por prompting e pelo effort level. Use instrucoes explicitas como "Responda de forma conservadora. Nao especule. So use fatos verificaveis."

---

## 10. Adaptive Thinking (substitui Extended Thinking)

**Fundamento:** Adaptive Thinking permite que Claude "pense mais" em tarefas complexas, alocando tokens de computacao para raciocinio antes de responder. E o **unico modo de thinking no Opus 4.7** (Extended Thinking classico com `budget_tokens` foi REMOVIDO — retorna HTTP 400 no 4.7).

**Como funciona:** Claude decide automaticamente quanto pensar, guiado pelo `effort` level. Voce nao controla o budget em tokens — voce controla a intensidade.

```python
# Novo padrao (Opus 4.7)
client.messages.create(
    model="claude-opus-4-7",
    max_tokens=86000,  # ~35% headroom para o tokenizer novo
    thinking={"type": "adaptive"},
    output_config={"effort": "xhigh"},  # low | medium | high | xhigh | max
    messages=[{"role": "user", "content": "..."}],
)
```

**Effort levels:**

| Level | Comportamento | Quando usar |
|-------|--------------|-------------|
| `low` | Pula thinking em problemas simples | Tarefas curtas, latencia-sensitivas |
| `medium` | Thinking moderado | Custo-sensitivo |
| `high` | Sempre pensa (default API) | Balanceado |
| `xhigh` | Sempre pensa profundamente | **Default Claude Code** Pro/Max; coding e agentic |
| `max` | Sem restricoes | Pode causar overthinking |

**Diferenca de CoT estruturado:**

| Aspecto | CoT Estruturado | Adaptive Thinking |
|---------|----------------|-------------------|
| Controle | Voce define os passos | Claude decide como pensar, guiado por `effort` |
| Visibilidade | Pensamento visivel no output | Depende de `thinking.display` (default `"omitted"` no 4.7) |
| Configuracao | Via prompt | Via `thinking: {type: "adaptive"}` + `effort` |
| Uso | Qualquer modelo | Opus 4.7 (unico modo), Sonnet 4.6 (opcional) |

**Quando usar Adaptive Thinking:**

| Situacao | Recomendado? | Justificativa |
|----------|-------------|---------------|
| Raciocinio multi-step complexo | SIM — `xhigh`/`max` | Melhora significativa de qualidade |
| Analise de trade-offs | SIM — `high`/`xhigh` | Exploracao mais profunda de opcoes |
| Planejamento detalhado | SIM — `xhigh` | Considera mais cenarios |
| Codigo complexo com interdependencias | SIM — `xhigh` (default Claude Code) | Reduz bugs e inconsistencias |
| Perguntas factuais simples | `low` ou pula | Overhead desnecessario |
| Formatacao ou conversao | `low` | Tarefa mecanica |

**Restricoes importantes:**
- **Incompativel com prefilling** — no Opus 4.7, prefill de mensagem assistant retorna 400; use `output_config.format` em vez disso
- **Nao microgerencie** — deixe Claude decidir como pensar; voce so ajusta o `effort`
- **`temperature`/`top_p`/`top_k` nao-default retornam 400** no Opus 4.7 — sampling e guiado por prompting + effort
- **Tokens de thinking contam no custo** mesmo nao sendo exibidos no output
- **Interleaved thinking e automatico** no Opus 4.7 com adaptive (sem beta header necessario) — Claude pode pensar entre tool calls
- **`thinking.display` default mudou** de `"summarized"` para `"omitted"` no 4.7: streams nao emitem `thinking_delta` por default; se voce mostra reasoning na UI, passe `display: "summarized"` explicitamente

**Promptable:** voce pode guiar a profundidade via system prompt:

```
Aborde esta tarefa de forma profunda e meticulosa. Pense cuidadosamente sobre:
- Multiplas abordagens possiveis e seus trade-offs
- Implicacoes e consequencias de cada decisao
- Como diferentes elementos se inter-relacionam

Nao se apresse — e melhor pensar profundamente e fornecer uma solucao robusta.
```

Ou, para tarefas rapidas:
```
Priorize responder rapidamente. Nao elabore alem do necessario.
```

**Task budgets (beta):** para loops agenticos longos, use `task_budget` (header `task-budgets-2026-03-13`, minimo 20k tokens) para limitar spend total:

```python
output_config={
    "effort": "high",
    "task_budget": {"type": "tokens", "total": 128000},
}
```

**Quando preferir CoT estruturado sobre Adaptive Thinking:**
- Precisa ver o raciocinio no output (auditoria, debugging, apresentacao)
- Quer controlar os passos especificos do raciocinio
- Modelo alvo nao suporta Adaptive Thinking (ex: modelos nao-Claude)
- Tarefas onde transparencia do raciocinio e crucial

**Migrando de Extended Thinking (`budget_tokens`) para Adaptive:**
- Remover `budget_tokens: N` do body (retorna 400 no 4.7)
- Substituir por `thinking: {type: "adaptive"}` + `output_config: {effort: "<level>"}`
- Regra pratica de mapping: `budget_tokens=8000` -> `effort: "medium"`, `16000-32000` -> `"high"`, `32000-64000` -> `"xhigh"`, `>64000` -> `"max"`
- `/claude-api migrate` no Claude Code automatiza parte do refactor

---

## 11. Structured Outputs e Stop Sequences

**Fundamento:** Complementos ao prefilling para garantir formato de output e economizar tokens.

### Structured Outputs

**O que e:** Feature da API que garante output em JSON valido seguindo um schema especifico. Diferente de prefilling, valida estrutura automaticamente.

**Quando usar Structured Outputs vs Prefilling:**

| Cenario | Usar | Justificativa |
|---------|------|---------------|
| JSON com schema rigido | Structured Outputs | Garantia de validacao |
| JSON simples sem validacao critica | Prefilling com `{` | Mais simples |
| Output que nao e JSON | Prefilling | Structured Outputs so para JSON |
| Integracao com sistemas tipados | Structured Outputs | Type safety |

**Exemplo de schema:**

```json
{
  "type": "object",
  "properties": {
    "categoria": {"type": "string", "enum": ["Tecnico", "Financeiro", "Comercial"]},
    "prioridade": {"type": "string", "enum": ["Alta", "Media", "Baixa"]},
    "justificativa": {"type": "string", "maxLength": 100}
  },
  "required": ["categoria", "prioridade", "justificativa"]
}
```

### Stop Sequences

**O que e:** Parametro `stop_sequences` que faz Claude parar de gerar quando emite uma sequencia especifica. Economia de tokens e precisao de formato.

**Tres usos principais:**

1. **Parar apos tag de fechamento:**
```python
stop_sequences=["</answer>"]
# Claude para imediatamente apos fechar a tag
```

2. **Evitar output extra:**
```python
stop_sequences=["---", "Nota:", "PS:"]
# Previne adendos e comentarios nao solicitados
```

3. **Economia em extracao:**
```python
# Prompt: "Extraia o email: "
# Prefill: "O email e: "
stop_sequences=["\n", " "]
# Para apos o email, sem texto adicional
```

**Combinacao poderosa — XML + Prefill + Stop:**

```python
messages=[
    {"role": "user", "content": "Classifique: <texto>...</texto>\n<classificacao>"},
    {"role": "assistant", "content": "<categoria>"}
],
stop_sequences=["</classificacao>"]
```

Resultado: Claude emite apenas o conteudo dentro das tags, sem preambulo nem postscript.

---

## 12. Variacoes Estrategicas

**Fundamento:** Todo prompt pode ter variacoes otimizadas para diferentes contextos de uso. Oferecer variacoes demonstra maestria e atende necessidades diversas.

### Variacao 1: Ultra-Conciso

**Objetivo:** Maxima eficiencia, minimo overhead.

**Caracteristicas:**
- Instrucoes diretas sem contexto extenso
- Maximo 200 palavras
- Sem exemplos ou apenas 1
- Output specification minimo

**Quando usar:**
- Usuario experiente que conhece o contexto
- Tarefas straightforward
- Iteracoes rapidas
- Contexto ja estabelecido na conversa

**Trade-offs:**
- (+) Velocidade, clareza imediata
- (-) Menos robusto para edge cases
- (-) Requer usuario que sabe o que quer

**Template:**

```xml
<role>[Papel em uma frase]</role>
<task>[Tarefa direta]</task>
<output>[Formato esperado]</output>
```

### Variacao 2: Profundidade Maxima

**Objetivo:** Maxima qualidade e robustez.

**Caracteristicas:**
- Contexto extenso com justificativas
- 500-1000 palavras
- 3-5 exemplos anotados
- Edge cases e fallbacks explicitos
- Anti-patterns detalhados
- Adaptive Thinking com effort `xhigh` ou `max` recomendado

**Quando usar:**
- Tarefas de alta consequencia
- Precisao critica
- Prompts de producao
- Usuario disposto a investir tempo

**Trade-offs:**
- (+) Qualidade maxima, robustez
- (+) Cobre edge cases
- (-) Maior latencia
- (-) Pode ser overwhelming

**Template:**

```xml
<role_and_context>
[Papel detalhado com expertise especifica]
[Contexto extenso do cenario]
[Restricoes e limites]
</role_and_context>

<primary_objective>
[Objetivo com criterios de sucesso mensuraveis]
</primary_objective>

<approach>
[Passos detalhados com justificativas]
</approach>

<examples>
[3-5 exemplos anotados com "Por que e bom"]
</examples>

<edge_cases>
[Casos especiais e como tratar]
</edge_cases>

<quality_guidelines>
[DO/DON'T/VERIFY completo]
</quality_guidelines>

<grounding>
[Anti-alucinacao e citacao de fontes]
</grounding>

<iteration_protocol>
[Como refinar baseado em feedback]
</iteration_protocol>
```

### Variacao 3: Hiper-Interativo

**Objetivo:** Maxima colaboracao e adaptabilidade.

**Caracteristicas:**
- Checkpoints de feedback embutidos
- Milestones iterativos
- Perguntas de clarificacao incentivadas
- Multiplas opcoes oferecidas ao usuario
- Co-criacao ativa

**Quando usar:**
- Resultado final incerto
- Exploracao criativa
- Usuario quer controle granular
- Refinamento colaborativo importante

**Trade-offs:**
- (+) Maxima adaptabilidade
- (+) Usuario satisfeito com controle
- (-) Requer mais engajamento
- (-) Menos eficiente para casos diretos

**Template:**

```xml
<role_and_context>
[Papel colaborativo, nao autoritario]
</role_and_context>

<primary_objective>
[Objetivo com espaco para refinamento]
</primary_objective>

<approach>
Milestone 1: [Primeira entrega parcial]
→ Checkpoint: Pedir feedback sobre [aspecto]

Milestone 2: [Segunda entrega]
→ Checkpoint: Confirmar direcao antes de continuar

Milestone 3: [Entrega final]
→ Checkpoint: Validacao e ajustes finais
</approach>

<interaction_style>
- Ofereca 2-3 opcoes quando houver ambiguidade
- Peca confirmacao em decisoes-chave
- Sugira alternativas mesmo quando nao solicitado
- Pergunte "Devo expandir [X] ou seguir para [Y]?"
</interaction_style>

<iteration_protocol>
Apos cada milestone:
1. Resuma o que foi feito
2. Pergunte satisfacao (1-10)
3. Ofereca ajustes especificos
4. So prossiga com confirmacao
</iteration_protocol>
```

### Tabela de Decisao: Qual Variacao Usar

| Contexto | Variacao Recomendada |
|----------|---------------------|
| Prompt para automacao/API | Ultra-Conciso |
| Prompt de producao critico | Profundidade Maxima |
| Primeira iteracao com usuario | Hiper-Interativo |
| Skill ou hook de Claude Code | Ultra-Conciso ou Profundidade Maxima |
| Custom Instructions de Project | Profundidade Maxima |
| System prompt de agente N8N | Ultra-Conciso |
| Exploracao criativa | Hiper-Interativo |
| Tarefa bem definida, baixa ambiguidade | Ultra-Conciso |
| Tarefa ambigua, alta consequencia | Hiper-Interativo |

---

## 13. Combinacoes de Tecnicas

As combinacoes mais eficazes:

| Combinacao | Caso de Uso | Eficacia |
|-----------|------------|---------|
| Role + CoT | Raciocinio complexo (math, logica) | Muito Alta |
| XML + Prefill + Stop Sequences | Pipelines de extracao estruturada | Muito Alta |
| Few-Shot + Output Format | Classificacao e categorizacao | Alta |
| CoT + Anti-alucinacao | Q&A baseado em documentos | Muito Alta |
| Role + Few-Shot + Prefill | Chatbots e agentes conversacionais | Alta |

**Hierarquia de prioridade para troubleshooting:**
1. Clareza → 2. Exemplos → 3. CoT → 4. XML → 5. Role → 6. Prefill → 7. Chaining → 8. Long Context

Quando algo nao funciona, trabalhe esta lista em ordem.
