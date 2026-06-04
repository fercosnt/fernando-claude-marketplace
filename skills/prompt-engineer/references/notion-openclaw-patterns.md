# Padroes para Notion Custom AI e OpenClaw

Estas plataformas tem restricoes significativas comparadas ao Claude Desktop/Code. Prompts devem ser model-agnostic, concisos e focados em instrucoes claras sem depender de features avancadas.

---

## 1. Notion Custom AI

### O que e

Custom AI do Notion permite criar "assistentes" dentro de pages/databases usando instrucoes personalizadas. O modelo subjacente varia (Claude, GPT, etc.) e o usuario nao controla parametros como temperatura ou tokens.

### Restricoes Criticas

| Restricao | Impacto no Prompt |
|-----------|------------------|
| Sem XML tags | Usar markdown (##, -, **bold**) para estrutura |
| Sem prefilling | Nao depender de pre-fill de resposta |
| Sem tools/MCP | Prompt deve ser auto-contido |
| Contexto limitado | Manter prompt curto (ideal < 500 palavras) |
| Modelo variavel | Tecnicas devem funcionar em qualquer LLM |
| Sem system prompt separado | Tudo vai nas "Custom Instructions" |
| Output em Notion blocks | Pensar em formatacao compativel com Notion |

### Padroes que Funcionam

**Estrutura recomendada:**

```markdown
## Papel
[Uma frase definindo quem o assistente e]

## Objetivo
[O que deve fazer quando acionado]

## Regras
- Regra 1
- Regra 2
- Regra 3

## Formato de Resposta
[Como estruturar o output — headings, bullet points, tabelas]

## Exemplo
**Input:** [exemplo de pergunta/contexto]
**Output:** [exemplo de resposta ideal]
```

**Por que essa estrutura:**
- Headings `##` criam separacao visual clara que qualquer modelo entende
- Bullet points sao parseados consistentemente por todos os LLMs
- Um exemplo concreto ancora o comportamento melhor que 10 regras abstratas
- Cabe em ~200-300 palavras, respeitando o contexto limitado

### Anti-Patterns no Notion

| Anti-Pattern | Problema | Alternativa |
|-------------|----------|-------------|
| `<xml_tags>` | Modelo pode nao entender | Usar `## Heading` |
| Prompt > 800 palavras | Estourar contexto, perder instrucoes finais | Comprimir para < 500 |
| "Pense passo a passo em tags" | Sem suporte a scratchpad | "Liste os passos antes de responder" |
| Multiplos exemplos longos | Gasta contexto precioso | 1 exemplo curto e anotado |
| Instrucoes condicionais complexas | Modelo perde track | Simplificar para if/then direto |
| Referencia a tools externas | Notion nao tem tools | Manter auto-contido |

### Exemplo Real: Assistente de Meeting Notes

```markdown
## Papel
Assistente de produtividade para reunioes.

## Objetivo
Ao receber notas de reuniao, gerar um resumo estruturado com action items.

## Regras
- Extrair decisoes tomadas (nao suposicoes)
- Cada action item deve ter: tarefa, responsavel, prazo
- Se prazo nao foi mencionado, marcar como "A definir"
- Tom profissional e conciso
- Maximo 300 palavras no resumo

## Formato
### Resumo
[3-5 bullet points com decisoes-chave]

### Action Items
| Tarefa | Responsavel | Prazo |
|--------|-------------|-------|
| ... | ... | ... |

### Pendencias
[Itens que ficaram em aberto]

## Exemplo
**Input:** "Reuniao com time de marketing. Maria vai atualizar o site ate sexta. Decidimos adiar o lancamento para marco. Joao precisa validar orcamento."

**Output:**
### Resumo
- Lancamento adiado para marco
- Atualizacao do site em andamento
- Orcamento pendente de validacao

### Action Items
| Tarefa | Responsavel | Prazo |
|--------|-------------|-------|
| Atualizar site | Maria | Sexta |
| Validar orcamento | Joao | A definir |

### Pendencias
- Motivo do adiamento nao documentado
```

---

## 2. OpenClaw

### O que e

OpenClaw e uma plataforma para criar e compartilhar prompts publicos. Prompts sao executados por diferentes modelos e usuarios, entao devem ser universais e auto-explicativos.

### Restricoes Criticas

| Restricao | Impacto no Prompt |
|-----------|------------------|
| Model-agnostic | Nao usar features especificas de um modelo |
| Sem system prompt dedicado | Tudo em um bloco de texto |
| Usuarios variados | Prompt deve ser claro para qualquer nivel |
| Sem tools | Auto-contido, sem dependencias externas |
| Publico | Nao incluir dados sensiveis ou contexto privado |
| Contexto limitado | Concisao e essencial |

### Padroes que Funcionam

**Estrutura recomendada:**

```markdown
# [Nome do Prompt]

## Contexto
[1-2 frases sobre o que este prompt faz e para quem]

## Instrucoes
Voce e [papel]. Sua tarefa e [objetivo].

Siga estas regras:
1. [Regra mais importante]
2. [Segunda regra]
3. [Terceira regra]

## Formato de Saida
[Especificar estrutura esperada]

## Variaveis
- {variavel_1}: [descricao]
- {variavel_2}: [descricao]

## Exemplo
[Input e output concretos]
```

**Por que essa estrutura:**
- `# Nome` identifica o prompt rapidamente na plataforma
- Variaveis com `{chaves}` permitem reutilizacao
- Regras numeradas dao prioridade clara
- Exemplo ancora o comportamento esperado

### Anti-Patterns no OpenClaw

| Anti-Pattern | Problema | Alternativa |
|-------------|----------|-------------|
| XML tags (`<role>`) | Muitos modelos ignoram | Usar markdown ou texto direto |
| Jargao tecnico de prompt eng | Usuarios variados nao entendem | Linguagem natural e clara |
| Prompt sem exemplo | Comportamento imprevisivel | Sempre incluir 1 exemplo |
| Hardcode de contexto especifico | Nao e reutilizavel | Usar variaveis `{empresa}`, `{produto}` |
| Instrucoes muito longas | Usuarios abandonam | Maximo 400 palavras |
| "Use extended/adaptive thinking" | Feature especifica de Claude (Opus 4.7 usa Adaptive Thinking) | Omitir ou usar "pense antes de responder" |

### Exemplo Real: Gerador de Copy para Redes Sociais

```markdown
# Gerador de Copy para Redes Sociais

## Contexto
Cria posts persuasivos para redes sociais com variantes para diferentes plataformas.

## Instrucoes
Voce e um copywriter digital especializado em {nicho}. Crie posts para promover {produto_ou_servico}.

Regras:
1. Tom {tom} (ex: profissional, casual, inspirador)
2. Incluir CTA claro em cada post
3. Adaptar tamanho para cada plataforma
4. Usar emojis com moderacao (max 3 por post)
5. Nunca fazer promessas absolutas ("garantido", "100%")

## Formato de Saida
### Instagram
- Legenda (max 150 palavras)
- 5 hashtags relevantes
- Sugestao de visual

### LinkedIn
- Post (max 200 palavras)
- Tom mais profissional

### Twitter/X
- Tweet (max 280 chars)
- Thread opcional (3 tweets)

## Variaveis
- {nicho}: Area de atuacao (ex: odontologia estetica)
- {produto_ou_servico}: O que promover (ex: lentes de contato dental)
- {tom}: Tom de comunicacao desejado

## Exemplo
**Input:** nicho=odontologia estetica, produto=clareamento dental, tom=profissional

**Output:**
### Instagram
Seu sorriso merece brilhar. O clareamento dental profissional pode transformar sua autoestima em apenas uma sessao.

Agende sua avaliacao e descubra o tom ideal para voce.

#ClareamentoDental #OdontologiaEstetica #SorrisoPerfeito #Estetica #DicasDeSaude

Visual: Foto antes/depois com iluminacao natural, foco no sorriso.
```

---

## 3. Adaptacao Cross-Platform

### Tabela de Decisao

| Situacao | Notion Custom AI | OpenClaw |
|----------|-----------------|----------|
| Estrutura | `## Heading` markdown | `# Titulo` + `## Secoes` |
| Tamanho ideal | < 500 palavras | < 400 palavras |
| Exemplos | 1 curto e anotado | 1 com input/output claro |
| Variaveis | Nao aplicavel (contexto fixo) | `{chaves}` para reutilizacao |
| Tom | Adaptar ao workspace | Universal e acessivel |
| CoT | "Liste os passos" (inline) | "Pense antes de responder" |
| Publico | Time/empresa especifica | Qualquer usuario |

### Checklist de Adaptacao

Ao criar prompt para estas plataformas:

- [ ] Sem XML tags — usar markdown puro
- [ ] Sem prefilling ou stop sequences
- [ ] Sem referencia a tools, MCP ou APIs
- [ ] Tamanho < 500 palavras (Notion) ou < 400 (OpenClaw)
- [ ] Pelo menos 1 exemplo concreto
- [ ] Instrucoes claras sem jargao tecnico
- [ ] Testavel mentalmente: "Se eu fosse o modelo, saberia o que fazer?"
- [ ] Para OpenClaw: variaveis com `{chaves}` onde aplicavel
- [ ] Para Notion: formato de output compativel com Notion blocks
