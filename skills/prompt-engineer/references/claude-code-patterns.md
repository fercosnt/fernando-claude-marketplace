# Padroes para Claude Code — Skills, Hooks, Commands, Subagents

## Indice

1. [Anatomia de uma Skill](#1-anatomia-de-uma-skill)
2. [Principios de Persuasao para Prompts de Agente](#2-principios-de-persuasao)
3. [Padroes para Hooks](#3-padroes-para-hooks)
4. [Padroes para CLAUDE.md](#4-padroes-para-claudemd)
5. [Padroes para Subagents](#5-padroes-para-subagents)
6. [Graus de Liberdade](#6-graus-de-liberdade)
7. [Anti-Patterns em Claude Code](#7-anti-patterns)

---

## 1. Anatomia de uma Skill

### Estrutura de Arquivos

```
skill-name/
├── SKILL.md           (obrigatorio — max ~500 linhas)
├── references/        (documentacao sob demanda)
├── scripts/           (codigo executavel reutilizavel)
└── assets/            (templates, imagens, fonts)
```

### SKILL.md — Frontmatter

```yaml
---
name: nome-da-skill
description: >
  [O QUE faz] + [QUANDO usar]. A description e o mecanismo de trigger.
  Inclua todos os sinais de ativacao aqui, NAO no body.
  Ex: "Cria X. Use quando usuario pedir Y, Z, ou W."
---
```

**Regra critica:** A `description` e o UNICO campo que Claude le para decidir se ativa a skill. Seja claro e exaustivo nos triggers.

### Principio de Progressive Disclosure

1. **Metadata (name + description)** — Sempre em contexto (~100 palavras)
2. **SKILL.md body** — Quando skill ativa (<5K palavras)
3. **References** — Sob demanda, quando Claude decide que precisa

**Implicacao:** Mantenha SKILL.md enxuto. Mova detalhes para references/. Referencie explicitamente: "Para detalhes de X, consulte `references/x.md`".

### Escrita de SKILL.md

- Use forma imperativa: "Faca X", nao "Voce deveria fazer X"
- Claude ja e inteligente — so adicione o que ele NAO sabe
- Desafie cada paragrafo: "Isso justifica o custo em tokens?"
- Prefira exemplos concisos a explicacoes verbosas

---

## 2. Principios de Persuasao

LLMs respondem aos mesmos principios de persuasao que humanos. Use para garantir que praticas criticas sejam seguidas.

**Base cientifica:** Meincke et al. (2025) — tecnicas de persuasao mais que dobraram taxas de compliance (33% → 72%).

### Principios Uteis para Skills/Hooks

| Principio | Como usar | Quando usar |
|-----------|----------|-------------|
| **Autoridade** | "VOCE DEVE", "NUNCA", "Sem excecoes" | Skills que exigem disciplina (TDD, verificacao) |
| **Compromisso** | "Anuncie que esta usando a skill", TodoWrite | Garantir que skills sejam seguidas |
| **Escassez** | "ANTES de prosseguir", "IMEDIATAMENTE apos" | Verificacoes urgentes, dependencias temporais |
| **Prova Social** | "TODA VEZ", "X sem Y = falha" | Estabelecer normas universais |
| **Unidade** | "Somos colegas", "nosso codebase" | Workflows colaborativos |

### Principios a EVITAR

| Principio | Por que evitar |
|-----------|---------------|
| **Reciprocidade** | Parece manipulativo, raramente necessario |
| **Afeicao (Liking)** | Cria sycophancy, conflita com feedback honesto |

### Exemplos Concretos

```markdown
# BOM — Autoridade + Compromisso
Escreveu codigo antes do teste? Delete. Recomece. Sem excecoes.
Quando encontrar uma skill aplicavel, ANUNCIE: "Usando [Skill] para [proposito]"

# RUIM — Vago, sem forca
Considere escrever testes primeiro quando possivel.
Talvez voce queira avisar qual skill esta usando.
```

### Tabela de Combinacoes por Tipo de Prompt

| Tipo de Prompt | Usar | Evitar |
|---------------|------|--------|
| Disciplina (TDD, code review) | Autoridade + Compromisso + Prova Social | Afeicao, Reciprocidade |
| Guia/Tecnica | Autoridade moderada + Unidade | Autoridade pesada |
| Colaborativo | Unidade + Compromisso | Autoridade, Afeicao |
| Referencia pura | Apenas clareza | Todos os principios |

---

## 3. Padroes para Hooks

Hooks sao shell commands que executam em resposta a eventos do Claude Code.

### Estrutura Eficaz de Hook Prompt

```markdown
# [Nome do Hook]

[Proposito em 1 linha]

## Trigger
[Evento que dispara: tool call, completion, etc.]

## Acao
[O que o hook faz — especifico, deterministico]

## Regras
- [Regra 1] — porque [justificativa]
- [Regra 2] — para [resultado]
```

### Principios para Hooks

- **Deterministico:** Hooks devem ter comportamento previsivel
- **Rapido:** Hooks bloqueiam a execucao — minimize latencia
- **Falha segura:** Se o hook falhar, Claude deve poder continuar
- **Feedback claro:** Mensagens de sucesso/falha devem ser inequivocas

---

## 4. Padroes para CLAUDE.md

CLAUDE.md e o arquivo de instrucoes do projeto que Claude Code le automaticamente.

### Estrutura Recomendada

```markdown
# CLAUDE.md

## Contexto do Projeto
[O que e este projeto, stack, arquitetura basica]

## Comandos
[Comandos essenciais: build, test, lint, deploy]

## Convencoes
[Padroes de codigo, naming, estrutura de pastas]

## Regras Inviolaveis
[O que NUNCA fazer — seguranca, patterns proibidos]
```

### Principios

- Trate como onboarding de dev senior no primeiro dia
- Inclua APENAS o que Claude nao pode inferir do codigo
- Comandos exatos > descricoes vagas
- Atualize quando convencoes mudarem

---

## 5. Padroes para Subagents

Subagents sao agentes especializados lancados via Task tool.

### Prompt Eficaz para Subagent

```markdown
## Objetivo
[Tarefa especifica e clara]

## Contexto
[Informacoes necessarias que o subagent nao tem]

## Restricoes
- [Limite 1]
- [Limite 2]

## Output Esperado
[Formato exato do resultado]

## NAO faca
- [Anti-pattern 1]
- [Anti-pattern 2]
```

### Principios para Subagents

- **Autonomia:** Subagent deve completar a tarefa sem voltar para perguntar
- **Contexto completo:** Forneca TUDO que precisa — ele nao tem historico da conversa
- **Output preciso:** Especifique formato exato do resultado
- **Scope limitado:** Uma tarefa por subagent

---

## 6. Graus de Liberdade

Calibre o nivel de especificidade conforme fragilidade da operacao:

### Alta Liberdade (instrucoes textuais)
Quando multiplas abordagens sao validas, decisoes dependem de contexto.
```markdown
## Code Review
1. Analise estrutura e organizacao
2. Verifique bugs potenciais
3. Sugira melhorias de legibilidade
```

### Media Liberdade (pseudocodigo com parametros)
Quando existe padrao preferido mas variacao e aceitavel.
```markdown
## Gerar Relatorio
Use este template, customize conforme necessario:
def generate_report(data, format="markdown", include_charts=True):
    ...
```

### Baixa Liberdade (scripts exatos)
Quando operacao e fragil, consistencia e critica, sequencia deve ser exata.
```markdown
## Migracao de Banco
Execute EXATAMENTE este comando:
python scripts/migrate.py --verify --backup
NAO modifique o comando ou adicione flags.
```

**Analogia:** Claude explorando um caminho:
- Ponte estreita com precipicios → guardrails exatos (baixa liberdade)
- Campo aberto → direcao geral (alta liberdade)

---

## 7. Anti-Patterns em Claude Code

| Anti-Pattern | Problema | Solucao |
|-------------|---------|---------|
| Skill com >500 linhas | Consome contexto desnecessariamente | Mova detalhes para references/ |
| Description vaga no frontmatter | Skill nunca e ativada | Liste TODOS os triggers na description |
| Instrucoes sem PORQUE | Claude nao generaliza | "Faca X — porque Y" |
| README.md dentro da skill | Arquivo inutil para o agente | Remova. Skill e para AI, nao humanos |
| Hook que bloqueia por muito tempo | Degrada UX | Max 5s por hook |
| Subagent sem contexto completo | Faz perguntas ou hallucina | Forneca TODO contexto necessario |
| CLAUDE.md com obviedades | Desperdia tokens | So inclua o que Claude nao pode inferir |

---

## 8. Features Avancadas do Claude Code

### EnterPlanMode

Ferramenta para entrar em modo de planejamento antes de implementacao complexa.

**Quando usar:**
- Tarefas que afetam multiplos arquivos
- Refatoracoes significativas
- Novas features com decisoes arquiteturais
- Quando usuario pode querer aprovar abordagem antes de executar

**Exemplo de instrucao:**
```markdown
Para tarefas complexas (3+ arquivos ou decisoes arquiteturais), use EnterPlanMode
antes de implementar. Apresente o plano e aguarde aprovacao.
```

### TodoWrite

Ferramenta para gerenciar lista de tarefas durante execucao.

**Quando usar:**
- Tarefas com multiplos passos
- Manter usuario informado do progresso
- Garantir que nenhum passo seja esquecido

**Exemplo de instrucao:**
```markdown
Use TodoWrite para:
1. Criar lista de tarefas no inicio
2. Marcar cada tarefa como in_progress quando iniciar
3. Marcar como completed IMEDIATAMENTE apos finalizar
4. Manter apenas UMA tarefa in_progress por vez
```

### Task Tool com Subagents Especializados

O Task tool lanca subagents com tipos especificos para tarefas especializadas.

**Tipos de subagent disponiveis:**
- `Explore` — Explorar codebase, buscar arquivos
- `Plan` — Planejar implementacao
- `Bash` — Executar comandos
- `general-purpose` — Tarefas gerais

**Exemplo de instrucao:**
```markdown
Para explorar o codebase, use Task tool com subagent_type=Explore.
Forneca contexto completo — subagent nao tem historico da conversa.
```

### run_in_background para Agents Paralelos

Permite executar subagents em background enquanto continua trabalhando.

**Quando usar:**
- Tarefas independentes que podem rodar em paralelo
- Operacoes longas que nao bloqueiam proximo passo

**Exemplo de instrucao:**
```markdown
Para tarefas independentes, use run_in_background=true no Task tool.
Use TaskOutput para verificar resultado quando necessario.
```

---

## 9. Modelo de Permissoes (Hooks)

Hooks podem BLOQUEAR tool calls antes de executar.

### Tipos de Hooks

| Tipo | Quando executa | Pode bloquear? |
|------|---------------|----------------|
| PreToolCall | Antes de tool call | SIM |
| PostToolCall | Apos tool call | NAO |
| Notification | Em eventos especificos | NAO |

### Mensagens de Bloqueio

Quando um hook bloqueia, Claude recebe mensagem. Skills devem:
1. Interpretar a mensagem de bloqueio
2. Ajustar comportamento conforme feedback
3. Nao tentar burlar o bloqueio

**Exemplo de instrucao:**
```markdown
Se um hook bloquear sua acao:
1. Leia a mensagem de bloqueio
2. Ajuste sua abordagem conforme indicado
3. Se nao puder ajustar, pergunte ao usuario

NUNCA tente burlar hooks — eles existem para proteger o usuario.
```

### Configuracao de Hooks em Skills

Skills podem sugerir hooks uteis:

```markdown
## Hooks Recomendados

Para garantir qualidade, configure estes hooks:

PreToolCall (Bash): Bloquear `rm -rf` sem confirmacao
PostToolCall (Edit): Rodar linter apos edicoes
```
