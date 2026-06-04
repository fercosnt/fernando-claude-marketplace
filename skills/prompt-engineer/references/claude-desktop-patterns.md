# Claude Desktop Patterns

Padroes e tecnicas para criar prompts otimizados para uso no Claude Desktop (web e app). Este reference cobre conversas diretas e Projects com Custom Instructions.

## Contexto do Claude Desktop

O Claude Desktop e uma interface conversacional projetada para humanos. Diferente de APIs ou Claude Code:

| Caracteristica | Claude Desktop | API/Claude Code |
|----------------|---------------|-----------------|
| Interacao | Bidirecional, iterativa | Programatica, one-shot |
| Feedback | Imediato, visual | Logs, outputs |
| Artifacts | Entrega principal | Menos relevante |
| Adaptive Thinking | Toggle/effort selector pelo usuario | Via `thinking: {type: "adaptive"}` + `effort` |
| Tools | web_search, computer_use, analysis_tool | MCP servers, Bash, etc. |
| Projects | Custom Instructions persistentes | CLAUDE.md, skills |

**Mindset:** Escreva para humanos em conversas reais, nao para parsers ou automacao.

---

## 1. Artifacts como Entrega Principal

Artifacts sao documentos interativos renderizados ao lado da conversa. Sao a forma preferida de entregar resultados substanciais no Desktop.

### Tipos de Artifacts

| Tipo | Quando Usar | Exemplos |
|------|------------|----------|
| `text/markdown` | Documentos, relatorios, analises | PRD, relatorio de pesquisa, plano de acao |
| `text/html` | Apps interativos, visualizacoes | Dashboard, formulario, calculadora |
| `application/vnd.ant.code` | Codigo para revisao/edicao | Scripts, componentes, configs |
| `application/vnd.ant.react` | Apps React completos | Ferramentas interativas, prototipos |
| `image/svg+xml` | Diagramas, ilustracoes | Fluxogramas, arquitetura, graficos |
| `application/vnd.ant.mermaid` | Diagramas de fluxo | Sequencias, estados, relacoes |

### Instrucoes para Artifacts de Qualidade

```xml
<artifact_guidelines>
Ao criar artifacts:

FACA:
- Inclua TODAS as features relevantes, nao apenas o minimo
- Adicione detalhes profissionais (hover states, transicoes, polish)
- Implemente funcionalidade completa, nao apenas estrutura
- Use design moderno e limpo
- Considere responsividade quando aplicavel

EVITE:
- Artifacts parciais que precisam de "continuacao"
- Placeholders ou TODOs dentro do artifact
- Codigo boilerplate excessivo sem funcionalidade real
- Design datado ou generio

QUANDO CRIAR ARTIFACT vs TEXTO:
- Artifact: resultado substancial que o usuario vai usar, salvar ou iterar
- Texto: explicacoes, discussoes, respostas curtas, perguntas
</artifact_guidelines>
```

### Template para Solicitar Artifact

```xml
Crie um artifact do tipo [tipo especifico] que:
- Inclua [elementos essenciais]
- Demonstre [qualidades desejadas]
- Seja [caracteristicas de usabilidade]

Nao economize em criatividade — mostre o que e possivel fazer.
```

---

## 2. Adaptive Thinking

Adaptive Thinking permite que Claude "pense mais" em tarefas complexas. E o unico modo de thinking no **Opus 4.7** (Extended Thinking classico com `budget_tokens` foi removido). No Desktop, a intensidade e controlada por um toggle/effort selector (low/medium/high/xhigh/max).

> **Nota:** em versoes mais antigas, essa feature chamava-se "Extended Thinking". Vasta parte da literatura online ainda usa esse nome — trate como sinonimo ao atualizar prompts antigos.

### Quando Recomendar Thinking (e qual effort)

| Situacao | Effort recomendado | Justificativa |
|----------|-------------------|---------------|
| Raciocinio multi-step complexo | `xhigh` / `max` | Melhora qualidade significativamente |
| Analise de trade-offs | `high` / `xhigh` | Permite exploracao mais profunda |
| Planejamento detalhado | `xhigh` | Considera mais opcoes |
| Codigo complexo com interdependencias | `xhigh` (default Claude Code Pro/Max) | Reduz bugs e inconsistencias |
| Perguntas factuais simples | `low` ou desligar | Overhead desnecessario |
| Tarefas criativas simples | `medium` | Depende da profundidade desejada |
| Formatacao ou conversao | `low` | Tarefa mecanica |

### Como Indicar no Prompt

Nao controle o Thinking em baixo nivel — instrua o comportamento desejado e, se relevante, sugira o effort:

```xml
<thinking_guidance>
Aborde esta tarefa de forma profunda e meticulosa. Pense cuidadosamente sobre:
- Multiplas abordagens possiveis e seus trade-offs
- Implicacoes e consequencias de cada decisao
- Como diferentes elementos se inter-relacionam

Nao se apresse — e melhor pensar profundamente e fornecer uma solucao robusta.

[Nota para o usuario: Esta tarefa se beneficia de effort alto. No Desktop, ative o toggle de thinking; no Claude Code, o default Pro/Max ja e xhigh.]
</thinking_guidance>
```

### Restricoes Importantes (Opus 4.7)

- **Prefilling nao e mais suportado** em mensagens assistant no Opus 4.7 (retorna 400). Use `output_config.format` ou estruture via XML no prompt.
- **`temperature`/`top_p`/`top_k` nao-default retornam 400** — sampling agora e guiado por prompting + effort level.
- Nao microgerencie o processo de pensamento — ajuste apenas o effort.
- `thinking.display` default mudou para `"omitted"` no 4.7: a UI nao mostra reasoning a menos que voce peca explicitamente `display: "summarized"`.
- No Desktop, o usuario controla a ativacao e o effort pelo toggle. No Claude Code, defina via `/effort` ou frontmatter de SKILL.md.
- Suportado no Opus 4.7 (unico modo), Sonnet 4.6, e via `effort` level configuravel no Claude Code v2.1.111+.

---

## 3. Tool Orchestration

O Claude Desktop tem acesso a ferramentas nativas que expandem suas capacidades.

### Ferramentas Disponiveis

| Ferramenta | Funcao | Quando Usar |
|------------|--------|-------------|
| `web_search` | Pesquisa na web em tempo real | Informacoes atualizadas, verificacao de fatos, pesquisa |
| `computer_use` | Execucao de codigo e scripts | Calculos, processamento de dados, automacao |
| `analysis_tool` | Analise de arquivos uploadados | PDFs, planilhas, imagens, documentos |
| `project_knowledge_search` | Busca no Project Knowledge | Documentos do projeto, contexto persistente |

### Padrao de Orchestration

```xml
<tool_orchestration>
Voce tem acesso a varias ferramentas. Use-as estrategicamente:

web_search:
- Use quando precisar de informacoes atualizadas (apos sua data de conhecimento)
- Use para verificar fatos ou encontrar fontes
- Use para pesquisar topicos especificos com profundidade

computer_use:
- Use para calculos complexos ou processamento de dados
- Use para executar scripts ou codigo
- Use para tarefas que requerem computacao real

analysis_tool:
- Use para analisar arquivos que o usuario fez upload
- Use para extrair informacoes de documentos
- Use para processar dados de planilhas

Estrategia geral:
1. Avalie quais ferramentas sao relevantes para a tarefa
2. Execute operacoes independentes em paralelo quando possivel
3. Sintetize resultados de multiplas fontes
4. Cite fontes quando usar informacoes de web_search
</tool_orchestration>
```

### Parallel Tool Execution

O Claude pode executar multiplas ferramentas simultaneamente quando nao ha dependencias:

```xml
<parallel_execution>
Quando possivel, execute operacoes independentes em paralelo para maxima eficiencia.

Exemplo: Ao pesquisar um topico amplo, faca multiplas web_searches simultaneas
explorando diferentes angulos (definicao, casos de uso, comparacoes, tendencias),
depois sintetize os resultados em uma visao coerente.

Exemplo: Ao analisar multiplos arquivos, processe-os em paralelo em vez de
sequencialmente, depois compare e contraste os resultados.
</parallel_execution>
```

---

## 4. Project Knowledge

Projects permitem armazenar documentos que Claude pode consultar em todas as conversas do projeto.

### Protocolo de Busca (5 Queries Obrigatorias)

Antes de criar prompts para Projects, execute TODAS estas buscas:

```xml
<search_sequence>
1. project_knowledge_search: "[tipo_tarefa] prompt template Claude Desktop"
2. project_knowledge_search: "[dominio] conversational guidelines"
3. project_knowledge_search: "artifacts examples [resultado_esperado]"
4. project_knowledge_search: "projects custom instructions [contexto]"
5. project_knowledge_search: "interactive prompts [categoria]"
</search_sequence>
```

### Integracao com Project Knowledge

```xml
<project_integration>
Se encontrar recursos relevantes:
- Template adequado: "Encontrei o template '[nome]' no Project Knowledge.
  Deseja que eu use como base?"
- Guidelines existentes: Mantenha 100% de consistencia com convencoes documentadas
- Exemplos similares: Reference e adapte padroes comprovados
- Custom Instructions: Integre com instrucoes persistentes do projeto

Documentacao obrigatoria:
- Cite todas as fontes: <source>documento_nome.md</source>
- Rastreie decisoes baseadas em documentacao existente
- Mantenha terminologia consistente com o projeto
</project_integration>
```

---

## 5. Custom Instructions para Projects

Custom Instructions definem comportamentos persistentes para todas as conversas de um Project.

### Template Completo

```xml
<project_custom_instructions_template>

<!-- PAPEL PERSISTENTE -->
<persistent_role>
Voce e [papel detalhado] trabalhando especificamente no contexto do [nome do projeto].

Este projeto foca em [objetivo/dominio do projeto], e voce deve:
- Manter consistencia com [padroes estabelecidos]
- Referenciar e utilizar [documentos chave do projeto]
- Seguir [guidelines especificos]
- Comunicar em [tom/estilo preferido]
</persistent_role>

<!-- CONHECIMENTO E CONTEXTO -->
<project_context>
**Documentacao Chave:**
[Liste documentos importantes no Project Knowledge]

**Terminologia e Padroes:**
[Defina termos especificos, convencoes, padroes de qualidade]

**Objetivos do Projeto:**
[Liste objetivos de alto nivel que devem guiar todas as interacoes]
</project_context>

<!-- COMPORTAMENTOS PADRAO -->
<default_behaviors>
Em todas as conversas neste projeto:

1. **[Comportamento 1]** — [contexto/justificativa]
   - [Detalhe ou sub-comportamento]

2. **[Comportamento 2]** — [contexto/justificativa]
   - [Detalhe ou sub-comportamento]

3. **[Comportamento 3]** — [contexto/justificativa]
   - [Detalhe ou sub-comportamento]

**Uso de Ferramentas:**
- Sempre consulte project_knowledge_search antes de responder sobre [topico]
- Use web_search quando [condicao]
- Crie artifacts por padrao para [tipo de solicitacao]
</default_behaviors>

<!-- ESTILO E TOM -->
<communication_style>
**Tom:** [descricao do tom]
**Formato preferido:** [estrutura de resposta]
**Nivel de detalhe:** [especificacao]

**Evite:**
- [Padrao indesejado]
- [Comportamento a evitar]

**Sempre:**
- [Padrao desejado]
- [Comportamento a manter]
</communication_style>

<!-- QUALIDADE E VALIDACAO -->
<quality_standards>
Todo output neste projeto deve:
- [Criterio de qualidade 1]
- [Criterio de qualidade 2]
- [Criterio de qualidade 3]

Quando nao tiver certeza sobre [aspecto especifico],
consulte [fonte/documento] ou peca clarificacao.
</quality_standards>

<!-- WORKFLOWS ESPECIFICOS (opcional) -->
<specific_workflows>
**Para [tipo de tarefa]:**
1. [Passo especifico]
2. [Passo especifico]
3. [Resultado esperado]

**Para [outro tipo de tarefa]:**
[Processo especifico]
</specific_workflows>

</project_custom_instructions_template>
```

---

## 6. Templates: Conversa Direta vs Projects

### Template para Conversas Diretas

Para prompts usados em conversas individuais, sem contexto persistente:

```xml
<conversational_prompt_template>

<!-- PAPEL E CONTEXTO -->
<role_and_context>
Voce e um [papel especifico ultra-detalhado] especializado em [dominio].

Seu contexto de trabalho:
[Descricao do cenario, audience, proposito]
</role_and_context>

<!-- OBJETIVO PRINCIPAL -->
<primary_objective>
Sua missao e [objetivo claro e especifico].

O sucesso sera medido por:
- [Criterio 1]
- [Criterio 2]
- [Criterio 3]

[Para tarefas complexas:] Pense profundamente sobre esta tarefa antes de comecar.
</primary_objective>

<!-- ABORDAGEM E PROCESSO -->
<approach>
Para alcancar este objetivo:

1. [Passo ou consideracao] — porque [justificativa]
2. [Passo ou consideracao] — para [resultado esperado]
3. [Passo ou consideracao] — garantindo [qualidade]

[Se usar ferramentas:]
Voce deve usar:
- web_search quando [condicao especifica]
- computer_use para [finalidade especifica]
- Artifacts para [tipo de entrega]
</approach>

<!-- FORMATO E ENTREGA -->
<output_format>
[Para artifacts:]
Crie um artifact do tipo [tipo especifico] que:
- Inclua [elementos essenciais]
- Demonstre [qualidades desejadas]
- Seja [caracteristicas de usabilidade]

[Para texto:]
Forneca sua resposta em [formato especifico]:
- [Caracteristica de formato]
- [Estilo de comunicacao]
- [Estrutura esperada]
</output_format>

<!-- EXEMPLOS (se disponiveis) -->
<examples>
<example type="ideal_case">
**Input:** [Exemplo de entrada]
**Output:** [Exemplo de saida exemplar]
**Por que e bom:** [Explicacao]
</example>
</examples>

<!-- DIRETRIZES DE QUALIDADE -->
<quality_guidelines>
FACA:
- [Comportamento desejado 1] porque [beneficio]
- [Comportamento desejado 2] para [resultado]

EVITE:
- [Anti-pattern 1] pois [problema]
- [Anti-pattern 2] que pode causar [issue]

VERIFIQUE antes de finalizar:
- [ ] [Criterio de validacao 1]
- [ ] [Criterio de validacao 2]
</quality_guidelines>

<!-- ITERACAO E FEEDBACK -->
<iteration_protocol>
Apos fornecer seu resultado inicial:
1. Peca feedback especifico sobre [aspecto 1] e [aspecto 2]
2. Esteja preparado para refinar baseado em [tipo de feedback]
3. Itere ate alcancar [criterio de satisfacao]
</iteration_protocol>

</conversational_prompt_template>
```

### Diferencas-Chave entre Templates

| Aspecto | Conversa Direta | Project Custom Instructions |
|---------|-----------------|----------------------------|
| Escopo | Unica conversa | Todas as conversas do projeto |
| Contexto | Deve ser completo no prompt | Pode referenciar Project Knowledge |
| Iteracao | Built-in no prompt | Implicita pelo relacionamento continuo |
| Persistencia | Nenhuma | Total dentro do projeto |
| Complexidade | Pode ser mais detalhado | Deve ser mais conciso (aplicado sempre) |

---

## 7. Principios de Design para Desktop

> **Nota:** Para Variacoes Estrategicas (Ultra-Conciso, Profundidade Maxima, Hiper-Interativo), consulte `references/anthropic-techniques.md` secao 12.

---

## 8. Principios de Design para Desktop

### Naturalidade > Tecnicidade

```xml
<principle name="Naturalidade">
Escreva para humanos, nao para parsers:
- Linguagem clara e direta
- Tom amigavel e colaborativo
- Evite jargao desnecessario
- Incentive iteracao e feedback
</principle>
```

### Conversacional > Programatico

```xml
<principle name="Conversacional">
O Desktop e uma conversa, nao um terminal:
- Permita flexibilidade na execucao
- Encoraje perguntas e clarificacoes
- Aceite que o usuario pode mudar de ideia
- Trate erros como oportunidades de refinamento
</principle>
```

### Context > Configuration

```xml
<principle name="Context">
Explique o PORQUE de cada instrucao:
- Forneca contexto suficiente para decisoes inteligentes
- Evite micro-gerenciamento
- Confie na inteligencia do modelo
- Permita adaptacao a situacoes imprevistas
</principle>
```

### Iteracao > Perfeicao Imediata

```xml
<principle name="Iteracao">
Projete para refinamento:
- Encoraje draft inicial + feedback
- Prepare para multiplas rodadas
- Estabeleca criterios de sucesso claros
- Inclua protocolo de iteracao explicito
</principle>
```

---

## Scorecard Desktop-Specific

Metricas adicionais para avaliar prompts de Desktop:

| Metrica | Peso | O que Avaliar |
|---------|------|--------------|
| Artifact Readiness | 3x | Prepara bem para criacao de artifacts? |
| Tool Use Strategy | 2.5x | Direciona uso apropriado de ferramentas? |
| Adaptive Thinking Guidance | 2x | Indica quando ativar e qual effort? Nao microgerencia? |
| Iteracao e Refinamento | 2x | Prepara para ciclos de feedback? |
| Usabilidade Imediata | 3x | Usuario pode usar sem modificacoes? |
| Project Integration | 2.5x | Se aplicavel, integra com Custom Instructions? |

**Thresholds:**
- Score minimo aceitavel: 7.5/10
- Score < 6.0 em Artifact Readiness (se aplicavel): bloqueio
- Score < 6.0 em Usabilidade: bloqueio

---

## Anti-Patterns Especificos do Desktop

| Anti-Pattern | Problema | Solucao |
|--------------|----------|---------|
| Prompt para API usado no Desktop | Ignora artifacts, tools, iteracao | Reescrever com foco conversacional |
| Micro-gerenciamento de thinking | Usuario controla apenas o effort do Adaptive Thinking | Remover instrucoes de thinking de baixo nivel; dar guidance geral + sugerir effort |
| Ignorar Project Knowledge | Perde contexto valioso | Adicionar instrucoes de busca explicitas |
| Artifact como afterthought | Resultado principal fica no texto | Projetar artifact como entrega principal |
| Sem protocolo de iteracao | Usuario nao sabe como refinar | Adicionar `<iteration_protocol>` |
| Linguagem de documentacao tecnica | Tom inadequado para conversa | Reescrever em linguagem natural |

---

## Checklist Final para Prompts Desktop

Antes de entregar um prompt para Claude Desktop:

```xml
<desktop_checklist>
Ambiente:
- [ ] Linguagem natural e conversacional
- [ ] Tom apropriado para audience
- [ ] Zero jargao desnecessario

Artifacts:
- [ ] Se aplicavel, artifact e a entrega principal
- [ ] Tipo de artifact especificado
- [ ] Features beyond basics incentivadas

Tools:
- [ ] web_search instruido quando relevante
- [ ] computer_use instruido quando relevante
- [ ] Parallel execution incentivado

Adaptive Thinking:
- [ ] Recomendacao de effort (`low`/`medium`/`high`/`xhigh`/`max`) quando relevante
- [ ] Sem micro-gerenciamento do processo
- [ ] Guidance de profundidade incluido

Project Integration:
- [ ] Project Knowledge search instruido (se Project)
- [ ] Consistencia com Custom Instructions
- [ ] Fontes citadas quando aplicavel

Iteracao:
- [ ] Protocolo de feedback incluido
- [ ] Criterios de sucesso claros
- [ ] Preparado para refinamento
</desktop_checklist>
```
