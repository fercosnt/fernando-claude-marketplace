# Padroes de Skills Bem Construidas

Catalogo de boas praticas extraido de 17+ skills existentes e diretrizes oficiais (skill-creator, writing-skills do superpowers). Serve como baseline de referencia para o que "bom" significa ao analisar skills.

---

## Indice

1. Padroes Estruturais
2. Padroes de Instrucao
3. Padroes de Trigger
4. Padroes de Workflow
5. Padroes de Persuasao
6. Anti-Patterns Universais
7. Benchmarks Quantitativos

---

## 1. Padroes Estruturais

### 1.1 Progressive Disclosure (3 niveis)

Cada nivel carrega apenas o que e necessario naquele momento — tokens sao custo direto.

- **Nivel 1 - Metadata (name + description):** ~100 palavras, sempre no contexto do Claude. E o que o Claude le para decidir se ativa a skill. Deve conter triggers, nao workflow.
- **Nivel 2 - SKILL.md body (quando skill ativa):** < 5K palavras target. Contem todas as instrucoes necessarias para execucao. E carregado integralmente quando a skill e ativada.
- **Nivel 3 - References (sob demanda pelo Claude):** Sem limite de tamanho. Claude le apenas quando precisa de contexto adicional. Deve ser referenciado explicitamente no SKILL.md.

Principio: quanto mais tarde o conteudo e carregado, menor o custo por ativacao.

Exemplos de skills que aplicam bem:
- knowledge-optimizer: 152 linhas no SKILL.md + 3 references separados por dominio
- prompt-engineer: 408 linhas no SKILL.md + 7 references tematicos

### 1.2 Organizacao de References

- Um reference por dominio ou preocupacao, nao por tipo de arquivo
- Nomes descritivos: `anthropic-techniques.md` e melhor que `ref1.md`
- TOC interno para navegabilidade em arquivos com mais de 100 linhas
- Referenciado explicitamente no SKILL.md: "Consulte `references/X` para detalhes sobre Y"
- Nunca criar reference orfao — se nao e mencionado no SKILL.md, nao sera lido

Padroes encontrados:
- prompt-engineer: 5 references tematicos (tecnicas, plataformas, exemplos, rubrica, checklist)
- notion-meeting-intelligence: 7 templates organizados por tipo de reuniao

### 1.3 Scripts e Assets

- **Scripts:** usar apenas para operacoes deterministicas ou frageis onde desvio do Claude causaria erro. Baixa liberdade proposital.
- **Assets:** templates de output, nao prosa explicativa. Claude preenche variaveis, nao interpreta texto livre.

Exemplos:
- knowledge-optimizer: 2 scripts Python para calculo de metricas
- prompt-architect: 7 templates .txt com estrutura fixa de output

### 1.4 Arquivos Proibidos

Estes arquivos nao devem existir dentro de uma skill:

| Arquivo | Motivo da proibicao |
|---------|-------------------|
| README.md | Para humanos, nao para AI. Claude nao le READMEs por padrao |
| CHANGELOG.md | Historico nao e necessario para execucao da skill |
| QUICK_REFERENCE.md | Redundante com o body do SKILL.md |
| Arquivos nao referenciados | Orfaos que gastam espaco sem agregar valor |

Regra geral: se o SKILL.md nao menciona o arquivo, ele nao deveria existir.

---

## 2. Padroes de Instrucao

### 2.1 Forma Imperativa

Claude responde melhor a comandos claros e diretos. A forma imperativa e mais concisa e elimina ambiguidade.

| BOM (imperativo) | RUIM (passivo/condicional) |
|-------------------|--------------------------|
| "Leia todos os arquivos" | "Os arquivos devem ser lidos" |
| "Avalie cada dimensao" | "Cada dimensao deve ser avaliada" |
| "Pergunte ao usuario" | "Voce deveria perguntar ao usuario" |
| "Gere o relatorio" | "Um relatorio precisa ser gerado" |

Principio: forma imperativa reduz tokens e aumenta taxa de cumprimento.

### 2.2 Context > Configuration

Toda regra precisa de um PORQUE. Sem justificativa, Claude segue a regra cegamente e nao generaliza para edge cases.

- **Principios sobre numeros arbitrarios:** "Pare quando clareza >= 80%" e melhor que "Maximo 5 perguntas"
- **Quando usar numeros, justificar:** link com pesquisa, principio de UX, ou evidencia empirica
- **Contexto permite adaptacao:** Claude ajusta comportamento quando entende a razao

Exemplo da prompt-engineer:
> "Maximo 5 perguntas — alem disso, fadiga do usuario reduz qualidade das respostas (pesquisas de UX mostram queda apos 5 interacoes)"

Anti-exemplo:
> "Maximo 3 perguntas" (por que 3? por que nao 2 ou 4?)

### 2.3 Tabelas de Decisao

Tabelas sao o formato mais eficiente para regras condicionais. Claude processa tabelas melhor que prosa com multiplos "se/entao".

Tipos de tabela encontrados em skills de alta qualidade:

- **Mode detection:** "sinal no pedido do usuario -> modo de operacao -> acao inicial"
- **Selecao de tecnica:** "situacao identificada -> tecnica a aplicar -> referencia"
- **Prioridade de perguntas:** classificacao ESSENCIAL / IMPORTANTE / OPCIONAL

Exemplo: prompt-engineer utiliza 3 tabelas de deteccao (modo, plataforma, tecnicas aplicaveis).

### 2.4 Hierarquia Visual de Prioridade

Nem toda instrucao tem o mesmo peso. Separar por prioridade melhora escaneabilidade:

- **ESSENCIAIS (sempre fazer):** em negrito ou com marcador forte. Sao as regras inviolaveis.
- **IMPORTANTES (fazer se relevancia > 50%):** instrucoes que agregam valor na maioria dos casos.
- **OPCIONAIS (fazer se contexto sugerir):** melhorias incrementais para casos especificos.

Beneficio: em sessoes prolongadas, Claude prioriza corretamente mesmo quando o contexto e grande.

### 2.5 Secoes Curtas e Escaneabilidade

Paredes de texto fazem Claude perder instrucoes. Quanto mais longo o paragrafo, maior a chance de instrucoes no meio serem ignoradas.

Hierarquia de preferencia de formato:
1. Headers descritivos (nao "Secao 1" mas "Passo 1: Leitura da Skill")
2. Listas com bullet points
3. Tabelas para relacoes condicionais
4. Prosa curta (maximo 3 frases por paragrafo)

Regra pratica: uma ideia por paragrafo, um conceito por secao.

---

## 3. Padroes de Trigger (Description)

### 3.1 Anatomia de Description Eficaz

Formato comprovado: `[VERBO + O QUE FAZ] + "Ativar quando" + [lista exaustiva de triggers]`

Componentes:
- **Verbo primeiro:** "Analisa", "Cria", "Transforma", "Preenche"
- **Triggers cobrindo sinonimos:** analisar/avaliar/revisar/pontuar/diagnosticar
- **Limite:** under 1024 chars total (restricao tecnica)

Exemplo bom (prompt-engineer):
> "Engenheiro de prompts especialista... Ativar quando usuario pedir para criar prompt, melhorar prompt, criar skill, criar hook, criar system prompt, otimizar instrucoes..."

Exemplo ruim:
> "Esta skill ajuda com prompts" (vago, sem triggers, nao cobre sinonimos)

### 3.2 Keyword Coverage

A description precisa cobrir todas as formas que um usuario usaria para pedir a funcionalidade.

Checklist de cobertura:
- Verbos de acao no dominio (criar, gerar, construir, fazer)
- Nomes do dominio e suas variacoes (prompt, instrucao, system prompt)
- Sinonimos em portugues e ingles quando a skill e bilingue
- Termos tecnicos e termos leigos para o mesmo conceito

Teste mental: imaginar 5 pedidos diferentes de 5 usuarios diferentes. A description cobre todos?

### 3.3 Anti-Patterns de Description

| Anti-Pattern | Problema | Correcao |
|-------------|---------|---------|
| Descrever workflow na description | Description nao e lugar para "primeiro faz X, depois Y" | Focar em triggers e capacidades |
| Description curta demais (< 50 chars) | Faltam triggers, skill nao ativa | Expandir com sinonimos e casos de uso |
| Misturar linguas sem proposito | Confunde deteccao de contexto | Escolher lingua primaria, adicionar keywords na outra |
| Resumir capacidades em vez de quando usar | Claude nao sabe QUANDO ativar | Reformular como "Ativar quando..." |

---

## 4. Padroes de Workflow

### 4.1 Mode Detection

Skills robustas detectam automaticamente o modo de operacao a partir do pedido do usuario.

Estrutura padrao:
- Tabela mapeando sinais no pedido para modos de operacao
- Deteccao automatica quando o sinal e claro (nao perguntar o obvio)
- Fallback: perguntar quando ambiguo
- Limite recomendado: 1-4 modos por skill

Padrao exemplar — prompt-engineer:

| Sinal no pedido | Modo | Acao inicial |
|-----------------|------|-------------|
| "crie um prompt para..." | CRIAR | Entrevista adaptativa |
| "melhore este prompt:" | MELHORAR | Analise do prompt existente |
| "avalie este prompt" | ANALISAR | Rubrica de avaliacao |

### 4.2 Entrevista Adaptativa

A entrevista com o usuario deve se adaptar ao contexto, nao seguir script fixo.

Principios:
- **Perguntas por prioridade:** ESSENCIAL > IMPORTANTE > OPCIONAL
- **Limite com justificativa:** explicar por que aquele numero de perguntas
- **Adaptacao por complexidade:** tarefa simples = 2 perguntas, tarefa complexa = 5+
- **Criterio de parada:** clareza >= threshold definido, nao numero fixo de perguntas
- **Agrupar perguntas:** fazer 2-3 por vez em vez de uma por uma (reduz turnos)

### 4.3 Formato de Entrega

O output da skill deve ser consistente e profissional.

Elementos de um bom formato de entrega:
- **Metadata:** data, versao, plataforma-alvo, tecnicas utilizadas
- **Separacao clara:** output principal + metadata + instrucoes de uso
- **Templates pre-definidos:** garantem consistencia entre execucoes
- **Checklist de verificacao:** validacao pre-entrega para nao esquecer criterios

### 4.4 Passos Numerados

Quando o workflow tem etapas sequenciais, numerar explicitamente.

Regras para passos eficazes:
- Formato: "Passo N: [Verbo] [O que]" — nunca "Passo N: [Conceito abstrato]"
- Cada passo tem uma acao clara e verificavel
- Resultado esperado de cada passo documentado
- Condicoes de transicao entre passos explicitas

Exemplo bom: "Passo 3: Leia o SKILL.md e extraia a lista de instrucoes imperativas"
Exemplo ruim: "Passo 3: Analise estrutural"

---

## 5. Padroes de Persuasao (para Agentes)

Baseados em pesquisa de Meincke et al. (2025) sobre como LLMs respondem a tecnicas de persuasao em instrucoes.

### 5.1 Authority (Autoridade)

Atribuir um role especifico ativa conhecimento do dominio relevante no Claude.

- Quanto mais especifico, melhor o resultado
- Incluir credenciais contextuais quando relevante

| Nivel de especificidade | Exemplo | Eficacia |
|------------------------|---------|---------|
| Generico | "Voce e um analista" | Baixa |
| Especifico | "Voce e um auditor senior de QA para sistemas de AI" | Alta |
| Contextualizado | "...com experiencia em avaliar 50+ skills de producao" | Muito alta |

### 5.2 Commitment (Compromisso)

Palavras de compromisso reforcam regras criticas.

- "NUNCA", "SEMPRE", "OBRIGATORIO" — para regras inviolaveis
- "Sem excecoes" — reforcar que a regra nao tem bypass
- **Moderacao e essencial:** usar CAPS apenas para 2-3 regras verdadeiramente criticas por skill
- Overuse de CAPS dilui o efeito e torna tudo "importante" (ou seja, nada e importante)

### 5.3 Social Proof (Prova Social)

Referenciar padroes estabelecidos aumenta compliance.

- "Skills bem construidas fazem X" — apela para norma do grupo
- "Baseado em analise de 17+ skills" — evidencia empirica
- Funciona melhor quando combinado com Authority
- Cuidado: nao inventar numeros. Usar apenas dados reais.

### 5.4 Graus de Liberdade (Analogia da Ponte)

A quantidade de liberdade dada ao Claude deve variar conforme o tipo de tarefa.

| Grau | Formato | Quando usar | Exemplo |
|------|---------|-------------|---------|
| **Alta liberdade** | Instrucoes textuais | Decisoes onde multiplas abordagens sao validas | "Avalie considerando o contexto do usuario" |
| **Media liberdade** | Pseudocodigo | Processos que precisam de estrutura mas permitem adaptacao | "Para cada metrica: score = weighted_avg(subs)" |
| **Baixa liberdade** | Scripts exatos | Operacoes frageis onde desvio = erro | Script Python com outputs fixos |

Principio: quanto mais fragil a operacao, menor a liberdade. Quanto mais subjetiva, maior.

---

## 6. Anti-Patterns Universais

Problemas recorrentes encontrados nas skills analisadas, ordenados por frequencia:

| Anti-Pattern | Frequencia | Consequencia | Correcao |
|-------------|-----------|-------------|---------|
| Instrucoes sem PORQUE | 30% | Claude nao generaliza para edge cases, segue regra cegamente sem entender intencao | Adicionar justificativa para cada regra significativa |
| Exemplos placeholder ou ausentes | 25% | Nao demonstra o padrao esperado, Claude gera output generico | Substituir por exemplos concretos e completos |
| SKILL.md > 500 linhas sem references | 20% | Gasta tokens em toda ativacao; 100% do conteudo carregado mesmo quando so parte e necessario | Mover conteudo pesado para references/ |
| Parede de texto sem hierarquia | 20% | Claude perde instrucoes no meio, prioriza o que leu por ultimo (recency bias) | Quebrar em headers, listas e tabelas |
| Description descreve workflow | 15% | Skill nao ativa quando deveria; description consumida para fins errados | Reescrever focando em triggers e sinonimos |
| Inconsistencia interna | 15% | Confunde o Claude, produz output contraditorio | Auditar: a skill pratica o que ensina? |
| Role generico ou ausente | 10% | Nao ativa conhecimento especializado do dominio | Especificar dominio, senioridade e contexto |
| README.md dentro da skill | 10% | Arquivo para humanos que Claude ignora; tokens desperdicados | Remover e integrar conteudo util no SKILL.md |

---

## 7. Benchmarks Quantitativos

Metricas extraidas de 17+ skills analisadas. Usar como referencia, nao como regra rigida.

### 7.1 Tamanho e Estrutura

| Metrica | Mediana | Range Saudavel | Red Flag |
|---------|---------|---------------|----------|
| Linhas do SKILL.md | ~250 | 93-500 | > 800 sem references |
| Numero de references | 2 | 0-7 | > 10 (fragmentacao excessiva) |
| Linhas por reference | ~200 | 50-400 | > 600 (reference muito grande) |
| Total de linhas (skill completa) | ~500 | 200-1500 | > 2000 (complexidade excessiva) |

### 7.2 Description e Triggers

| Metrica | Mediana | Range Saudavel | Red Flag |
|---------|---------|---------------|----------|
| Caracteres na description | ~400 | 100-800 | < 50 (insuficiente) ou > 1000 (verbose) |
| Numero de triggers/sinonimos | ~8 | 3-15 | < 2 (skill nao ativa) |

### 7.3 Complexidade e Workflow

| Metrica | Mediana | Range Saudavel | Red Flag |
|---------|---------|---------------|----------|
| Numero de modos | 1-3 | 1-4 | > 5 (complexidade desnecessaria) |
| Exemplos concretos | 1-2 | 0-7 | 0 em skill complexa |
| Passos no workflow | 4-6 | 3-10 | > 12 (workflow muito longo) |
| Perguntas na entrevista | 3-5 | 2-7 | > 8 (fadiga do usuario) |

### 7.4 Como Interpretar os Benchmarks

- **Dentro do range saudavel:** nenhuma acao necessaria
- **Fora do range mas justificado:** aceitavel se ha razao documentada (ex: skill de dominio muito amplo pode ter > 500 linhas)
- **Red flag:** requer investigacao. Pode ser valido, mas precisa de justificativa forte
- **Multiplos red flags:** sinal claro de problema estrutural

---

## Notas Finais

Este catalogo e um documento vivo. Os padroes foram extraidos empiricamente e devem ser atualizados conforme novas skills de alta qualidade sao analisadas.

Prioridade ao usar este catalogo:
1. Padroes estruturais (secao 1) — impacto direto em custo e eficiencia
2. Padroes de instrucao (secao 2) — impacto direto em qualidade do output
3. Padroes de trigger (secao 3) — impacto direto em ativacao correta
4. Anti-patterns (secao 6) — identificacao rapida de problemas
5. Benchmarks (secao 7) — validacao quantitativa
