# Padroes para Agentes Claude em N8N

## Indice

1. [Arquitetura de System Prompts para N8N](#1-arquitetura-de-system-prompts)
2. [Padroes por Tipo de Node AI](#2-padroes-por-tipo-de-node)
3. [Prompt Chaining entre Nodes](#3-prompt-chaining-entre-nodes)
4. [Gerenciamento de Memoria e Contexto](#4-gerenciamento-de-memoria)
5. [Tool Use e Function Calling](#5-tool-use-e-function-calling)
6. [Anti-Patterns em N8N](#6-anti-patterns)
7. [Templates Prontos](#7-templates-prontos)

---

## 1. Arquitetura de System Prompts para N8N

### Principio Central

Prompts em N8N devem ser **mais deterministicos e concisos** que em Claude Desktop. Motivos:
- Execucao automatizada sem supervisao humana
- Contexto limitado por custo/latencia
- Necessidade de output parseavel por nodes subsequentes

### Estrutura Base para System Prompt

```xml
<role>
Voce e [papel especifico] especializado em [dominio].
</role>

<objective>
Sua tarefa: [objetivo unico e claro].
</objective>

<rules>
SEMPRE:
- [Regra 1] — porque [justificativa]
- [Regra 2] — porque [justificativa]

NUNCA:
- [Restricao 1] — pois [consequencia]
- [Restricao 2] — pois [consequencia]
</rules>

<output_format>
Responda EXCLUSIVAMENTE no formato:
[formato exato — JSON, markdown, texto estruturado]

Nao inclua explicacoes, preambulos ou texto fora do formato.
</output_format>
```

### Principios para N8N

| Principio | Descricao |
|-----------|-----------|
| **Concisao** | Cada token custa dinheiro e tempo. Elimine redundancias. |
| **Determinismo** | Output deve ser parseavel. Especifique formato exato. |
| **Idempotencia** | Mesmo input = mesmo output. Evite aleatoriedade. |
| **Fail-safe** | Defina o que fazer quando input e inesperado. |
| **Sem ambiguidade** | Zero espaco para interpretacao. |

---

## 2. Padroes por Tipo de Node

### AI Agent Node

Para o node AI Agent com tools conectadas:

```xml
<role>
Voce e um agente [funcao] que tem acesso a estas ferramentas:
- [Tool 1]: [quando usar]
- [Tool 2]: [quando usar]
</role>

<decision_process>
Ao receber uma solicitacao:
1. Analise se precisa de informacao externa → use [tool]
2. Se ja tem dados suficientes → responda diretamente
3. Se dados sao ambiguos → use [tool] para clarificar
</decision_process>

<output_rules>
- Responda em [formato]
- Se usar tool, integre resultado na resposta
- Se tool falhar, responda: {"error": "[descricao]", "fallback": "[acao alternativa]"}
</output_rules>
```

### Basic LLM Chain Node

Para o node LLM Chain simples (sem tools):

```xml
<task>
[Instrucao direta e especifica]
</task>

<input>
Dados de entrada: {{ $json.campo }}
</input>

<output>
Responda APENAS com [formato].
Sem explicacoes adicionais.
</output>
```

### Classificador / Router Node

Para nodes que classificam e roteam:

```xml
<task>
Classifique o texto a seguir em UMA das categorias:
- VENDA: Pedido de compra, orcamento, negociacao
- SUPORTE: Problema tecnico, reclamacao, duvida
- INFORMACAO: Pergunta geral, consulta de status
- OUTRO: Nao se encaixa nas anteriores
</task>

<rules>
- Responda APENAS com o nome da categoria, nada mais
- Se houver duvida entre duas categorias, escolha a primeira listada
- "OUTRO" so quando nenhuma outra categoria se aplica
</rules>

<input>
{{ $json.message }}
</input>
```

### Sumarizador Node

```xml
<task>
Resuma o texto abaixo em exatamente 3 bullet points.
Cada bullet: 1 frase, maximo 20 palavras.
Foque em: [aspecto prioritario].
</task>

<format>
- [Bullet 1]
- [Bullet 2]
- [Bullet 3]
</format>

<input>
{{ $json.text }}
</input>
```

---

## 3. Prompt Chaining entre Nodes

### Padrao: Pipeline de Processamento

```
[Input] → [Classificacao] → [Switch] → [Processamento Especializado] → [Formatacao] → [Output]
```

**Prompt do node Classificacao:**
```
Classifique em: TIPO_A, TIPO_B, TIPO_C.
Responda APENAS com o tipo.
```

**Prompt do node Switch (baseado na classificacao):**
Cada rota tem seu prompt especializado.

### Padrao: Gerar + Revisar

```
[Input] → [Geracao] → [Revisao/QA] → [Condicional: aprovado?] → [Output ou Regeneracao]
```

**Prompt do node Geracao:**
```
Gere [conteudo] baseado em: {{ $json.input }}
Formato: [especificacao]
```

**Prompt do node Revisao:**
```
Avalie o texto a seguir em 3 criterios (nota 1-10 cada):
1. Precisao factual
2. Clareza
3. Completude

Se TODOS >= 7: responda "APROVADO"
Se algum < 7: responda "REPROVAR: [criterio]: [nota] - [motivo]"

Texto: {{ $json.generated_text }}
```

### Padrao: Enriquecimento Progressivo

```
[Input] → [Extracao de Entidades] → [Busca de Contexto] → [Geracao Enriquecida] → [Output]
```

Cada node adiciona dados ao payload JSON que nodes subsequentes usam.

---

## 4. Gerenciamento de Memoria e Contexto

### Window Memory

Para conversas com historico:

```xml
<role>
Voce e [papel]. Mantenha contexto da conversa.
</role>

<memory_rules>
- Referencie informacoes anteriores quando relevante
- Se o usuario contradizer algo anterior, pergunte: "Antes voce mencionou X. Mudou de ideia?"
- Nao repita informacoes ja fornecidas
</memory_rules>
```

### Summary Memory

Para conversas longas onde window memory estoura:

```xml
<context>
Resumo da conversa ate agora: {{ $json.summary }}
</context>

<rules>
- Use o resumo como base, nao peca ao usuario repetir informacoes
- Se o resumo for insuficiente, pergunte especificamente o que falta
</rules>
```

### Sem Memoria (Stateless)

Para operacoes isoladas:

```xml
<rules>
- Trate cada mensagem como independente
- Nao assuma contexto anterior
- Toda informacao necessaria esta na mensagem atual
</rules>
```

---

## 5. Tool Use e Function Calling

### Descricao de Tools para AI Agent

Quando conectar tools ao AI Agent, a descricao da tool e critica:

```
Nome: buscar_cliente
Descricao: Busca informacoes de um cliente no CRM pelo nome ou email.
Use quando: O usuario perguntar sobre dados de um cliente especifico.
NAO use quando: A pergunta for generica ou sobre politicas da empresa.

Parametros:
- query (string, obrigatorio): Nome ou email do cliente
```

### Principios para Tool Descriptions

- **Explicite QUANDO usar** — nao deixe o agente adivinhar
- **Explicite QUANDO NAO usar** — previna chamadas desnecessarias
- **Parametros claros** — tipo, obrigatoriedade, formato esperado
- **Exemplos de query** — "Ex: 'maria@email.com' ou 'Maria Silva'"

---

## 6. Anti-Patterns em N8N

| Anti-Pattern | Problema | Solucao |
|-------------|---------|---------|
| System prompt >500 tokens | Custo alto, resposta lenta | Condense. Cada token deve justificar seu custo |
| Output nao-parseavel | Node seguinte quebra | Especifique formato EXATO com exemplo |
| Nao definir fallback | Erro silencioso no workflow | "Se nao souber, responda: {\"error\": \"...\"}" |
| Prompt generico reutilizado | Resultados mediocres | Customize para cada node/funcao |
| Ignorar temperatura | Resultados aleatorios | temp=0 para classificacao, temp=0.7 para criacao |
| Contexto desnecessario | Desperdicar tokens | Inclua APENAS dados que o node precisa |
| Encadear sem validacao | Erros se propagam | Node de QA entre etapas criticas |

---

## 7. Templates Prontos

### Template: Atendimento ao Cliente

```xml
<role>
Voce e um atendente de suporte da [empresa], especializado em [area].
Tom: profissional, empatico, objetivo.
</role>

<rules>
SEMPRE:
- Cumprimente pelo nome se disponivel
- Responda em portugues
- Ofereca proximo passo concreto
- Limite: max 150 palavras

NUNCA:
- Prometa prazos que nao pode garantir
- Invente informacoes — diga "vou verificar" se nao souber
- Use jargao tecnico com cliente final
</rules>

<output_format>
[Saudacao]
[Resposta ao problema]
[Proximo passo]
[Encerramento]
</output_format>
```

### Template: Extracao de Dados

```xml
<task>
Extraia as seguintes informacoes do texto:
- nome_completo (string)
- email (string ou null)
- telefone (string ou null)
- assunto (string, max 50 caracteres)
- urgencia (alta/media/baixa)
</task>

<output_format>
Responda APENAS com JSON valido:
{
  "nome_completo": "",
  "email": "",
  "telefone": "",
  "assunto": "",
  "urgencia": ""
}
</output_format>

<rules>
- Se informacao nao estiver presente, use null
- Nao invente dados
- urgencia: "alta" se mencionar urgente/critico/ASAP; "media" se prazo definido; "baixa" se sem indicacao
</rules>

<input>
{{ $json.message }}
</input>
```

### Template: Gerador de Conteudo

```xml
<role>
Voce e um redator [especialidade] que escreve para [audience].
</role>

<task>
Crie [tipo de conteudo] sobre: {{ $json.topic }}

Requisitos:
- Tom: [tom]
- Tamanho: [X-Y palavras]
- Estrutura: [descricao]
- Incluir: [elementos obrigatorios]
</task>

<quality>
FACA:
- Usar dados concretos quando possivel
- Manter consistencia de tom
- Fechar com CTA claro

EVITE:
- Cliches e frases genericas
- Parágrafos > 3 frases
- Promessas exageradas
</quality>
```

---

## 8. Features Avancadas do N8N

### AI Agent com Sub-Agents

O node AI Agent pode orquestrar sub-agents para tarefas complexas.

**Estrutura de prompt para agent orquestrador:**

```xml
<role>
Voce e um agente orquestrador que coordena sub-agents especializados.
</role>

<sub_agents>
Voce tem acesso a estes sub-agents:
- pesquisador: Busca informacoes em bases de dados
- redator: Cria conteudo textual
- validador: Verifica qualidade e correcao

Use cada sub-agent para sua especialidade.
</sub_agents>

<orchestration_rules>
1. Decomponha tarefas complexas em subtarefas
2. Delegue cada subtarefa ao sub-agent apropriado
3. Sintetize resultados em resposta final
4. Se sub-agent falhar, tente alternativa ou reporte erro
</orchestration_rules>
```

### Structured Output Parser

Para garantir output parseavel, use o Structured Output Parser node.

**No system prompt, reforce o formato:**

```xml
<output_format>
Sua resposta DEVE ser JSON valido que segue este schema:
{
  "resultado": "string",
  "confianca": "number (0-1)",
  "metadata": {
    "fonte": "string",
    "timestamp": "ISO date"
  }
}

CRITICO: Nao inclua texto fora do JSON.
O node seguinte espera JSON puro para parsing.
</output_format>
```

**Configuracao do parser:**
- Defina schema JSON esperado
- Ative "Strict Mode" para rejeitar outputs invalidos
- Configure fallback para erros de parsing

### Integracao com MCP Servers

N8N pode integrar com MCP servers para expandir capacidades do AI Agent.

**Prompt com tools MCP:**

```xml
<role>
Voce e um agente com acesso a ferramentas externas via MCP.
</role>

<mcp_tools>
Ferramentas disponiveis:
- mcp_database_query: Consulta banco de dados
- mcp_api_call: Chama APIs externas
- mcp_file_read: Le arquivos do sistema

Cada tool tem parametros especificos — consulte descricao antes de usar.
</mcp_tools>

<mcp_rules>
- Prefira MCP tools quando disponivel — sao mais confiaveis que output textual
- Se MCP tool retornar erro, inclua na resposta: "Tool [nome] falhou: [erro]"
- Nao tente simular resultado de MCP tool
</mcp_rules>
```

---

## 9. Output Parsing e Validacao

### Padrao: JSON com Fallback

```xml
<output_rules>
Responda em JSON valido.

Se nao conseguir produzir JSON valido, responda:
{
  "error": true,
  "message": "[descricao do problema]",
  "partial_data": [dados que conseguiu extrair]
}

Isso permite que o workflow trate erros graciosamente.
</output_rules>
```

### Padrao: Validacao em Etapas

```
[Geracao] → [Parser JSON] → [Validacao Schema] → [Node de Erro ou Sucesso]
```

Node de validacao:
```javascript
// Code node para validar
const data = $json;
const required = ['nome', 'email', 'assunto'];

const missing = required.filter(f => !data[f]);
if (missing.length > 0) {
  return { valid: false, missing };
}
return { valid: true, data };
```

---

## 10. Boas Praticas de Performance

| Pratica | Impacto | Implementacao |
|---------|---------|---------------|
| Prompt conciso | -30% tokens, -20% latencia | Elimine redundancias. Cada token deve justificar custo. |
| Temperatura baixa | +50% consistencia | temp=0 para classificacao/extracao. temp=0.3-0.7 para criacao. |
| Cache de respostas | -70% custo em repeticoes | Use node Cache antes de LLM para queries frequentes. |
| Batch processing | -40% overhead | Agrupe itens antes de chamar LLM (max 10-20 por batch). |
| Early exit | -50% processamento | Use Switch apos classificacao para pular etapas desnecessarias. |
