# Tecnicas Oficiais da Anthropic — Referencia Detalhada

Baseado na documentacao oficial da Anthropic e no tutorial interativo de prompt engineering.

## Indice

1. [Clareza e Especificidade](#1-clareza-e-especificidade)
2. [Multishot / Few-Shot Examples](#2-multishot--few-shot-examples)
3. [Chain of Thought (CoT)](#3-chain-of-thought-cot)
4. [XML Tag Structuring](#4-xml-tag-structuring)
5. [Role Prompting](#5-role-prompting)
6. [Response Prefilling (legado)](#6-response-prefilling-legado)
7. [Prompt Chaining](#7-prompt-chaining)
8. [Long Context Optimization](#8-long-context-optimization)
9. [Prevencao de Alucinacao](#9-prevencao-de-alucinacao)
10. [Adaptive Thinking e Effort](#10-adaptive-thinking-e-effort-familia-claude-5)
11. [Structured Outputs e Stop Sequences](#11-structured-outputs-e-stop-sequences)
12. [Variacoes Estrategicas](#12-variacoes-estrategicas)
13. [Combinacoes de Tecnicas](#13-combinacoes-de-tecnicas)
14. [Ajustes para a familia Claude 5](#14-ajustes-para-a-familia-claude-5)

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

**Escopo (familia Claude 5):** em Opus 5.5 e Fable 5.1 o thinking adaptativo esta **sempre ligado**, e no Sonnet 5 vem ligado por default. Nesses modelos o CoT verbal e redundante: a profundidade se controla pelo `effort` (ver §10). Pior: pedir que o modelo **reproduza o raciocinio no texto da resposta** pode ser recusado com `stop_reason: "refusal"`, categoria `reasoning_extraction` (Opus 5.5, Fable 5.1). Se precisa ver o raciocinio, leia os blocos de thinking com `display: "summarized"`.

**Onde CoT verbal ainda vale:** modelos sem thinking nativo (Haiku 4.5 sem extended thinking, Notion Custom AI, OpenClaw, GPT/Llama sem reasoning). Nesses, **externalize o pensamento** — sem output de raciocinio nao ha raciocinio real.

**Tres niveis (para modelos sem thinking nativo):**

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

**Quando usar:** Tarefas que um humano precisaria pensar — matematica complexa, analise multi-fator, decisoes com trade-offs, escrita complexa — **em modelo sem thinking nativo**.

**Quando NAO usar:** Tarefas simples e factuais (CoT aumenta latencia e tokens), e em qualquer modelo Claude com adaptive thinking — la o "Guiado" com passos numerados tambem tende a piorar: a doc oficial diz *"Prefer general instructions over prescriptive steps. A prompt like 'think thoroughly' often produces better reasoning than a hand-written step-by-step plan."*

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

## 6. Response Prefilling (legado)

> **Nao funciona nos modelos Claude atuais.** Prefill de mensagem `assistant` retorna **HTTP 400** em toda a linha a partir de Opus 4.6 / Sonnet 4.6 — inclui Fable 5.1, Opus 5.5 e Sonnet 5. So funciona em Haiku 4.5 e em modelos legados (Opus 4.5, Sonnet 4.5 e anteriores). Para prompt novo, use as substituicoes abaixo; mantenha esta secao so para entender/manter integracoes antigas.

**Substituicoes oficiais:**

| Uso antigo do prefill | Substituto nos modelos atuais |
|-----------------------|------------------------------|
| Forcar JSON (`{`) | Structured Outputs / `output_config.format` (§11) |
| Eliminar preambulo | Instrucao no system: "Responda direto, sem preambulo. Nao comece com 'Aqui esta...', 'Com base em...'" |
| Manter persona | Role no system + lembrete no turno do usuario (ou mid-conversation system message) |
| Continuar resposta interrompida | Mover para o user: "Sua resposta anterior foi interrompida e terminou em `[...]`. Continue de onde parou." |

**Fundamento (historico):** Semear o inicio da resposta de Claude controlando formato, eliminando preambulos e mantendo consistencia de persona.

**Tres usos principais (so Haiku 4.5 / modelos legados):**

1. **Forcar JSON:** Prefill com `{`
2. **Eliminar preambulo:** Prefill com a tag de output esperada
3. **Manter persona:** Prefill com `[Nome do Personagem]`

```python
messages=[
    {"role": "user", "content": "Extraia nome, tamanho, preco: <description>...</description>"},
    {"role": "assistant", "content": "{"}  # Forca JSON direto
]
```

**Restricao:** Prefill nao pode terminar com whitespace.

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

**Fundamento:** Claude tem janelas de contexto grandes — 1M tokens (default, sem beta header) em Fable 5.1, Opus 5.5 e Sonnet 5; 200K no Haiku 4.5. Posicionamento e estrutura dos dados impactam qualidade da resposta em ate 30%, e essa sensibilidade aumenta quanto maior o contexto.

> **Nota tokenizer:** Opus 5.5 e Fable 5.1 usam o tokenizer introduzido no Opus 4.7 (1.0x-1.35x mais tokens que os modelos anteriores a ele). O **Sonnet 5 tem tokenizer novo, ~30% mais tokens que o Sonnet 4.6** — o preco por token caiu, mas o custo por tarefa nao cai na mesma proporcao. Re-conte tokens no modelo alvo em vez de reaproveitar contagens antigas.

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
3. **Guie o tom pelo prompt:** `temperature=0` funcionava em modelos antigos. **Em todo modelo a partir do Opus 4.7 (inclui Fable 5.1, Opus 5.5, Sonnet 5), `temperature`/`top_p`/`top_k` nao-default retornam HTTP 400** — e o SDK Python v1.0+ nem aceita esses parametros (`TypeError`). So o Haiku 4.5 ainda aceita `temperature` ou `top_p` (um de cada vez). Use instrucoes explicitas e POSITIVAS como "Responda usando apenas fatos verificaveis; se faltar evidencia, diga 'nao sei'."

---

## 10. Adaptive Thinking e Effort (familia Claude 5)

**Fundamento:** Adaptive Thinking permite que Claude "pense mais" em tarefas complexas, decidindo sozinho quando e quanto pensar. O **`effort` e o lever primario** de profundidade (e de custo); guiar o pensamento por prompt verbal e secundario. Extended Thinking classico (`thinking: {type: "enabled", budget_tokens: N}`) **retorna 400** em Fable 5.1, Opus 5.5 e Sonnet 5 — so o Haiku 4.5 ainda usa esse modo.

**Thinking por modelo (set/2026):**

| Modelo | Thinking | Pode desligar? | Effort default |
|--------|----------|----------------|----------------|
| Fable 5.1 | Adaptive, sempre ligado | Nao (`disabled` = 400) | `high` |
| Opus 5.5 | Adaptive, sempre ligado | Nao (`disabled` = 400) | **`medium`** |
| Sonnet 5 | Adaptive, ligado por default | Sim (`{type: "disabled"}`) | `high` |
| Haiku 4.5 | Extended manual (`budget_tokens`), desligado por default | — | sem effort |

```python
# Padrao atual (Opus 5.5)
client.messages.create(
    model="claude-opus-5-5",
    max_tokens=64000,               # cobre thinking + resposta; em xhigh/max comece em 64k+
    output_config={"effort": "medium"},  # low | medium | high | xhigh | max — SETE EXPLICITO
    messages=[{"role": "user", "content": "..."}],
)
# Nao precisa mandar `thinking`: no Opus 5.5 e no Fable 5.1 ele esta sempre ligado.
```

**Effort levels (tabela geral da doc):**

| Level | Uso tipico |
|-------|-----------|
| `low` | Tarefas simples, latencia/custo baixos, **subagentes** |
| `medium` | Equilibrio — **default do Opus 5.5** |
| `high` | Raciocinio complexo, coding dificil, agentes — default dos demais modelos |
| `xhigh` | Tarefas agenticas longas (>30 min) com orcamento de milhoes de tokens |
| `max` | Capacidade maxima sem limite de gasto; na pratica, reservar para ganho medido |

> **Os nomes nao equivalem entre modelos.** O `medium` do Opus 5.5 empata ou supera o `high` do Opus 5; o `medium` do Sonnet 5 ~ `high` do Sonnet 4.6; o `low` do Fable 5.1 costuma competir em custo por tarefa com Opus/Sonnet em effort mais alto. A recomendacao "`xhigh` para coding" valia para Opus 4.7/4.8 — **nao carregue esse habito para a familia 5**: comece no default, sete explicito e faca um sweep nos seus evals.

> **Ressalva de campo:** no lancamento, `max` no Opus 5.5 bateu no teto de 128K de output ainda pensando (Simon Willison, 2 de 2 tentativas). Reserve `xhigh`/`max` para onde voce mediu ganho.

**Diferenca de CoT estruturado:**

| Aspecto | CoT Estruturado | Adaptive Thinking |
|---------|----------------|-------------------|
| Controle | Voce define os passos | Claude decide como pensar, guiado por `effort` |
| Visibilidade | Pensamento no texto da resposta | Blocos `thinking`; `display` default `"omitted"` (vazios) — use `"summarized"` para ler |
| Uso | Modelos sem thinking nativo | Toda a familia Claude 5 |

**Restricoes importantes (Fable 5.1 / Opus 5.5 / Sonnet 5):**
- **Prefill** do assistant retorna 400 — use `output_config.format` / structured outputs (§6, §11)
- **`temperature`/`top_p`/`top_k`** nao-default retornam 400
- **`tool_choice` forcado** (`{type: "any"}` ou `{type: "tool"}`) retorna 400 em **Opus 5.5 e Fable 5.1** (Sonnet 5 ainda aceita). Use `auto` + instrucao explicita + tools com `strict: true`, ou structured outputs
- **A resposta pode comecar com blocos `thinking`** antes do texto: codigo que le `content[0].text` quebra — selecione blocos por `type`. Em loops de tool use, devolva os blocos `thinking` **inalterados**
- **Texto entre tool calls** (Opus 5.5, Fable 5.1) vem em blocos `thinking`, vazios por default — interfaces que mostram progresso ficam "mudas"; use `display: "updates"` (beta) ou `"summarized"`
- **Historico append-only** (Opus 5.5, Fable 5.1): editar turnos anteriores, o `system` ou as `tools` invalida os thinking blocks seguintes (400 em contas criadas a partir de 31/08/2026). Mudancas no meio da sessao vao em mensagens `role: "system"` no meio do array
- **`max_tokens` cobre thinking + resposta**, e tokens de thinking sao cobrados mesmo quando nao exibidos

**O que NAO colocar no prompt (familia 5):**
- "Pense com cuidado antes de responder" em system prompt de chat — atrasa o primeiro token sem ganho medido (doc do Opus 5.5). Quer mais ou menos raciocinio? Mude o `effort`
- "Escreva seu raciocinio na resposta" — pode ser recusado (`reasoning_extraction`). Leia os blocos com `display: "summarized"`
- Plano passo a passo escrito a mao para "ajudar a pensar" — *"Prefer general instructions over prescriptive steps"*

**Quando baixar a profundidade sem baixar o effort** (ex.: latencia em chat), uma linha no system ajuda — meça a qualidade depois:
```
Answer directly without deliberating.
```

**Mudar effort no meio da conversa sem perder cache (beta):** em Fable 5.1, Opus 5.5 e Opus 5, uma mensagem `{"role": "system", "content": [], "output_config": {"effort": "low"}}` (header `mid-conversation-output-config-2026-07-01`) vale do proximo turno em diante. Mudar o `effort` top-level entre requests invalida o prompt cache.

**Task budgets (beta):** para loops agenticos longos, `task_budget` (header `task-budgets-2026-03-13`, minimo 20k tokens) diz ao modelo quantos tokens ele tem para o loop inteiro:

```python
output_config={
    "effort": "medium",
    "task_budget": {"type": "tokens", "total": 128000},
}
```

**Quando preferir CoT estruturado sobre Adaptive Thinking:**
- Modelo alvo nao tem thinking nativo (Haiku 4.5 sem extended thinking, modelos nao-Claude, Notion Custom AI, OpenClaw)
- Nos modelos Claude 5, para auditoria do raciocinio, use `display: "summarized"` em vez de CoT no texto

**Migrando de codigo antigo:**
- Remover `budget_tokens` e `thinking: {type: "disabled"}` (este ultimo so continua valido no Sonnet 5)
- Controlar profundidade por `output_config: {effort: "<level>"}`; fazer sweep em vez de mapear 1:1
- Trocar prefill e `tool_choice` forcado (ver restricoes acima)
- Ler resposta por `type`; rever `max_tokens`
- `/claude-api migrate this project to claude-opus-5-5` no Claude Code automatiza o refactor e gera checklist

---

## 11. Structured Outputs e Stop Sequences

**Fundamento:** Garantir formato de output e economizar tokens. Nos modelos atuais sao o **substituto do prefilling** (que retorna 400).

### Structured Outputs

**O que e:** Feature da API (`output_config.format`) que garante output em JSON valido seguindo um schema especifico, validando a estrutura automaticamente.

**Como garantir formato nos modelos atuais:**

| Cenario | Usar | Justificativa |
|---------|------|---------------|
| JSON com schema rigido | Structured Outputs | Garantia de validacao |
| JSON simples | Structured Outputs | Prefill `{` retorna 400 em Fable 5.1/Opus 5.5/Sonnet 5 |
| Output que nao e JSON | XML output tags + instrucao no system + stop sequence | Sem prefill disponivel |
| Chamada de tool obrigatoria | `tool_choice: auto` + instrucao explicita + `strict: true` | `tool_choice` forcado retorna 400 em Opus 5.5/Fable 5.1 |
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
# Prompt: "Extraia o email e responda so com ele dentro de <email></email>."
stop_sequences=["</email>"]
# Para ao fechar a tag, sem texto adicional
```

**Combinacao — XML + instrucao + Stop (substitui o antigo XML + Prefill + Stop):**

```python
system="Responda apenas com <classificacao><categoria>...</categoria></classificacao>, sem preambulo."
messages=[{"role": "user", "content": "Classifique: <texto>...</texto>"}]
stop_sequences=["</classificacao>"]
# Leia o bloco de type "text" — a resposta pode comecar com blocos "thinking".
```

Para classificacao com valores fechados, Structured Outputs com `enum` e mais robusto.

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
- Effort acima do default (`high`/`xhigh`) so se o eval mostrar ganho — na familia 5 o default ja e forte

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
| Role + effort adequado (Claude 5) / Role + CoT (sem thinking nativo) | Raciocinio complexo (math, logica) | Muito Alta |
| Structured Outputs (ou XML + Stop Sequences) | Pipelines de extracao estruturada | Muito Alta |
| Few-Shot + Output Format | Classificacao e categorizacao | Alta |
| CoT + Anti-alucinacao | Q&A baseado em documentos | Muito Alta |
| Role + Few-Shot + instrucao de formato no system | Chatbots e agentes conversacionais | Alta |

**Hierarquia de prioridade para troubleshooting:**
1. Clareza → 2. Exemplos → 3. Effort (Claude 5) / CoT (sem thinking nativo) → 4. XML → 5. Role → 6. Formato (Structured Outputs) → 7. Chaining → 8. Long Context

Quando algo nao funciona, trabalhe esta lista em ordem.

---

## 14. Ajustes para a familia Claude 5

Fontes: [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices), [Prompting Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5), [Prompting Fable 5.1](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1), [Prompting Fable 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5), [Prompting Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5), [Prompting Sonnet 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5). Verificado em 2026-09-27.

**Principio geral:** prompts e skills escritos para modelos anteriores tendem a ser **prescritivos demais**. A doc do Fable 5 e direta: *"Skills developed for prior models are often too prescriptive for Claude Fable 5 and can degrade output quality."* Ao MELHORAR um prompt antigo, **remova** instrucoes antes de acrescentar.

### Parar de fazer

| Padrao antigo | Por que sai | Modelo |
|---------------|------------|--------|
| Plano passo a passo escrito a mao para "guiar o raciocinio" | Instrucao geral + objetivo + porque rende mais | Toda a familia 5 |
| Regras anti-formatacao ("nao use bullets/negrito/headers") | O Fable 5.1 ja formata pouco; a regra empurra para prosa densa. Troque por regra de *quando* formatar | Fable 5.1 |
| "Guarde todos os achados para a resposta final" | Suprime as atualizacoes de progresso uteis | Fable 5.1, Opus 5.5 |
| "Revise duas vezes" / "faca uma verificacao final" | O modelo ja verifica sozinho; a instrucao gera over-verification. Remover, nao reescrever | Opus 5 / 5.5 |
| "Pense com cuidado antes de responder" (chat) | Atrasa o primeiro token sem ganho medido; profundidade e o `effort` | Opus 5.5 |
| "Escreva seu raciocinio na resposta" | Pode ser recusado (`reasoning_extraction`) | Opus 5.5, Fable 5.1 |
| "Seja conservador" em harness de revisao | O Sonnet 5 obedece ao pe da letra e perde recall | Sonnet 5 |
| "Evite o visual generico de IA" (frontend) | So troca um estilo default por outro | Opus 5.5 |

### Comecar a fazer

- **Diga o que deixar de fora.** O Fable 5.1 tende a entregar mais que o pedido (corrige codigo vizinho, estende comportamento). Uma instrucao de escopo reduz os extras sem perder sucesso:
  ```
  Se encontrar um bug pre-existente ou algo que a tarefa nao menciona, nao corrija nem estenda nesta mudanca, a menos que o pedido nao funcione sem isso; reporte como follow-up no resumo.
  ```
- **Sonnet 5 e literal:** ele nao generaliza uma instrucao de um item para os outros. Se a regra vale para todos, diga "para todos os itens".
- **Tarefas autonomas longas:** Opus 5.5 e Fable 5.1 as vezes encerram o turno anunciando o proximo passo ("Next, I'll...") ou pedindo permissao ("Shall I apply this?") para algo ja pedido. Nomeie essas paradas indesejadas e as desejadas (so parar quando nada avanca sem o usuario, ou para acao destrutiva). A doc do Opus 5.5 traz um paragrafo pronto (secao "Unattended agentic runs").
- **Prosa "mannered" (Fable 5.1):** frases longas e metaforas no lugar de afirmacao direta. `Please remove all mannered prose.` funciona.
- **Agentes multi-app:** antes de agir, mandar explorar (emails, planilhas, registros) inclusive fontes que a tarefa nao citou — melhora mensuravel no Opus 5.5.
- **Texto colado pelo usuario:** envolver em `<pasted_content id="...">` com uma nota no system melhora a resistencia a injecao (Opus 5.5).
- **Frontend:** listar os padroes concretos a evitar ("fundo creme, rotulos 01/02/03, botoes pill") em vez de pedir "nao generico".
- **Multiagente:** um sinal de tempo (`elapsed 340s / 1200s`) no fim de cada mensagem faz o time paralelizar e terminar antes; o agente lider nao deve ficar parado esperando subagente.
- **Loops de tool (Fable 5.1):** uma frase pedindo para agrupar tool calls independentes evita uma chamada por turno.

### Escolha de modelo (para recomendar ao usuario)

| Uso | Modelo | Effort inicial |
|-----|--------|----------------|
| Maioria dos casos (default da doc) | Opus 5.5 (`claude-opus-5-5`, $4/$20) | `medium` |
| Raciocinio exigente, agentes de horas, pesquisa com entregavel longo | Fable 5.1 (`claude-fable-5-1`, $10/$50) | `high` |
| Dia a dia com velocidade (codigo, analise, conteudo) | Sonnet 5 (`claude-sonnet-5`, $2/$10) | `high` (ou `medium`) |
| Volume, latencia, subagentes simples | Haiku 4.5 (`claude-haiku-4-5`, $1/$5) | sem effort |

