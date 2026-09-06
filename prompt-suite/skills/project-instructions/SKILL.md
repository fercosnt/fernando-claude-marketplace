---
name: project-instructions
description: Escreve, audita e melhora as INSTRUCOES de projetos do Claude — tanto Projects do chat (claude.ai / Claude Desktop) quanto Projects do Claude Cowork. Roteia cada regra para a camada certa (perfil global, instrucao do projeto, knowledge, memoria, skill) em vez de empilhar tudo num texto so. Inclui modo auditoria de instrucao existente e montagem do pacote completo do projeto (arquivos, pastas, links, connectors, skills). Ativar quando o usuario pedir para escrever instrucoes de projeto, custom instructions, project instructions, instrucao do Cowork, global instructions, configurar um projeto do Claude, "o que colocar nas instrucoes", "meu projeto do Claude nao obedece", "montar um projeto pro time", "revisar as instrucoes do projeto", ou colar uma instrucao existente pedindo melhoria. Tambem ativar ao mencionar Cowork, project knowledge, "instrucoes pro Claude", ou projeto compartilhado com o time.
intent: >
  Instrucao de projeto nao e prompt. E a camada de contexto duravel de um espaco de trabalho —
  e a maior parte do que as pessoas escrevem nela deveria morar em outro lugar (knowledge, skill,
  memoria, ou no proprio chat). Esta skill existe para decidir ONDE cada regra vai antes de
  redigir, porque instrucao inchada compete por janela de contexto e regra morta ensina o Claude
  a ignorar o resto. Cobre dois alvos com modelos mentais opostos: Chat Project (conversacional,
  governa como a resposta sai) e Cowork Project (agentico, governa o que e feito, onde salva e
  o que e "pronto"). Escrita para instrucoes que o time do Fernando vai usar — logo, explicitas,
  com dono e data, sem contexto tacito.
effort: high
references:
  - references/chat-project.md
  - references/cowork-project.md
  - references/auditoria.md
  - references/pacote.md
---

# project-instructions

Escreve e audita instrucoes de projeto do Claude. Dois alvos, dois modelos mentais opostos — a skill nunca trata os dois igual.

## 1. Deteccao de alvo

Antes de qualquer coisa, descubra para onde vai o texto.

| Sinal no pedido | Alvo | Reference |
|---|---|---|
| "projeto do Claude", claude.ai, "conversa", "anexei uns arquivos", "ele responde errado" | **Chat Project** | `references/chat-project.md` |
| "Cowork", "pasta", "arquivo local", "ele roda sozinho", "tarefa agendada", "gera a planilha", "entregavel" | **Cowork Project** | `references/cowork-project.md` |
| "instrucoes pro Claude" em Settings, "vale pra tudo", "toda conversa" | **Camada de perfil** (nao e projeto) | secao 2 abaixo |
| Ambos, ou nenhum sinal claro | **Pergunte** | — |

> Se o usuario disser "os dois", **nao escreva um texto so**. Escreva dois, e diga por que sao diferentes: a instrucao de Chat governa a resposta, a de Cowork governa o trabalho. Copiar uma na outra produz um projeto que fala bonito e nao entrega, ou que entrega e ignora o tom.

## 2. As camadas — o roteador

Esta e a parte que mais muda o resultado. **Antes de redigir, roteie cada regra levantada.** Uma regra na camada errada ou nao dispara, ou dispara sempre e vira ruido.

### Chat Project (claude.ai / Claude Desktop)

| Camada | O que mora aqui | Escopo |
|---|---|---|
| Organization instructions | Politica da empresa. Teto de **3.000 caracteres**. Vence conflito com instrucao individual | Toda a org (Team/Enterprise) |
| "Instructions for Claude" (perfil, em Settings) | Quem VOCE e, jargao que usa, formato/tamanho de resposta que prefere | Todas as suas conversas |
| **Project instructions** | Contexto e regras **daquele** projeto: papel, o que produzir, o que evitar, quando perguntar | So os chats do projeto |
| Project knowledge (arquivos) | FATOS. Documentos, tabelas de preco, guias de marca, transcricoes | Consultado sob demanda; planos pagos ativam RAG |
| Memoria do projeto | O que o Claude aprendeu sozinho ao longo dos chats. Memoria e por projeto | Automatico, nao se escreve |
| Skills | Processo repetivel de **uma** tarefa, invocavel | Sob demanda |

### Cowork Project

| Camada | O que mora aqui | Escopo |
|---|---|---|
| Global instructions (Settings > Cowork) | Quem VOCE e: papel, siglas, formato e tom preferidos. **Mantenha enxuto** — carrega em toda sessao | Toda sessao do Cowork, inclusive tarefas agendadas |
| **Project instructions** | O TRABALHO: proposito, workflow, definicao de pronto, onde salvar, o que nunca fazer sem perguntar | So aquele projeto |
| Folder instructions | Regras daquela pasta especifica. **O proprio Claude pode reescreve-las durante a sessao** | So aquela pasta |
| Description do projeto | Uma frase de para que serve. O **Dispatch le isso** ao escolher o projeto de uma tarefa — nao deixe generica | Roteamento |
| Folders / Links / Projects from Chat | Onde estao os arquivos, docs de referencia, knowledge de projeto do chat | Acesso |
| Memory | Store proprio do projeto, persiste entre sessoes | Automatico |
| Skills / Connectors / Plugins (Customize) | Capacidade. **Cowork nao le `~/.claude`** — o que existe so la precisa ser adicionado em Customize | Sob demanda |

### Teste de permanencia

Uma regra so entra na instrucao do projeto se passar nos tres:

1. **Duravel** — vale em pelo menos 8 de 10 conversas/tarefas do projeto. Se vale numa, e prompt de chat, nao instrucao.
2. **Nao-obvia** — sem ela o Claude erraria. "Seja claro e util" nao passa.
3. **Sem casa melhor** — nao e fato (→ knowledge), nao e processo de uma tarefa so (→ skill), nao e preferencia sua geral (→ perfil/global).

Regra que reprova: diga em qual camada ela deveria estar, nao apenas corte.

## 3. Deteccao de modo

| Sinal | Modo |
|---|---|
| "criar", "escrever", "montar", projeto novo, nao existe instrucao ainda | **CRIAR** |
| Usuario cola uma instrucao existente; "melhorar", "revisar", "nao obedece", "ta ignorando" | **AUDITAR** |
| "montar o projeto", "o que colocar", "que arquivos", "que connector", projeto inteiro | **PACOTE** |

Os modos se combinam. CRIAR normalmente termina em PACOTE. AUDITAR de um projeto que nao funciona quase sempre revela problema de PACOTE, nao de texto.

## 4. Modo CRIAR

### Passo 1 — Entrevista (maximo 7 perguntas, em blocos)

Nao pergunte tudo. Pergunte o que voce nao consegue inferir do que o usuario ja disse, e agrupe.

1. **Trabalho** — o que esse projeto produz, repetidamente? (peca um exemplo real de tarefa)
2. **Entregavel** — como o resultado bom se parece? Formato, tamanho, onde vai parar.
3. **Publico** — quem le/recebe o que sai dali.
4. **Fontes** — que documentos, dados ou sistemas o Claude precisa consultar.
5. **Erros conhecidos** — o que o Claude erra hoje nesse tipo de tarefa? (pergunta de maior retorno — cada erro citado vira uma regra que passa no teste de nao-obviedade)
6. **Fronteira** — o que ele nunca deve fazer sozinho / quando deve parar e perguntar.
7. **Vocabulario** — siglas, nomes internos, termos que so o time usa.

Se o usuario ja deu material (briefing, projeto existente, conversa anterior), **extraia dali e confirme** em vez de perguntar do zero.

### Passo 2 — Rotear

Monte a lista de regras levantadas e passe cada uma pelo teste de permanencia (secao 2). Mostre o roteamento ao usuario numa tabela curta: `regra → camada`. Isso e o que impede a instrucao de inchar.

### Passo 3 — Redigir

Regras de redacao (valem para os dois alvos):

- **Prosa curta em blocos rotulados.** Nao despeje XML de 6 secoes. Tags XML so quando houver 3+ blocos distintos ou exemplos colados dentro.
- **Regra positiva com substituto.** "Nao seja prolixo" nao ensina nada; "resposta padrao em ate 5 bullets; texto corrido so se eu pedir" ensina.
- **Tom sempre com exemplo.** Uma linha de amostra vale mais que tres adjetivos.
- **Nomeie o gatilho.** "Quando eu colar uma transcricao, faca X" > "seja proativo".
- **Orcamento.** Chat Project: mire **1.500–2.500 caracteres**; acima de ~3.500 pare e pergunte o que vai pro knowledge. Cowork global: mais enxuto ainda, so sobre voce.
- **Sem contexto tacito.** Time vai usar: nada de "como sempre fazemos". Escreva o que e.

**Cabecalho de time** — toda instrucao que o time vai usar comeca com duas linhas:

```
Dono: [nome] · Revisar em: [data]
Para que serve: [uma frase]
```

### Passo 4 — Validar

Rode o checklist da secao 6 e entregue o texto **em bloco de codigo, pronto pra colar**, seguido de: onde colar, o que ficou de fora e em que camada foi parar.

## 5. Modo AUDITAR

Leia `references/auditoria.md` para o catalogo completo de falhas. Fluxo:

1. **Conte** — caracteres, numero de regras, quantas passam no teste de permanencia.
2. **Classifique** cada trecho: `manter` / `reescrever` / `mover para [camada]` / `cortar`.
3. **Nomeie a falha** de cada problema (instrucao-curriculo, regra morta, enciclopedia, conflito silencioso, negativa orfa, Cowork conversacional...). Nomear e o que faz o usuario nao repetir.
4. **Reescreva** a versao nova inteira, nao so os trechos.
5. **Diga o que testar** — 2 ou 3 pedidos concretos que devem se comportar diferente agora.

Se o sintoma for "ele ignora as instrucoes", suspeite primeiro de: instrucao longa demais, regras em conflito entre si, ou regra que na verdade precisava de knowledge/skill. Diga isso — nao apenas reescreva mais bonito.

## 6. Checklist antes de entregar

- [ ] Alvo correto identificado (Chat vs Cowork) e o texto usa o modelo mental daquele alvo
- [ ] Toda regra passa nos 3 testes de permanencia; as reprovadas foram roteadas, nao apenas cortadas
- [ ] Nenhum fato que deveria estar no knowledge/folder foi colado dentro da instrucao
- [ ] Toda negativa tem substituto positivo
- [ ] Tom tem pelo menos um exemplo concreto
- [ ] Siglas e nomes internos definidos (o time vai ler)
- [ ] Cabecalho com dono e data de revisao
- [ ] Dentro do orcamento de caracteres
- [ ] Entregue em bloco de codigo + onde colar + o que foi para outras camadas
- [ ] Se Cowork: definicao de pronto, onde salvar e fronteira de permissao estao explicitos
- [ ] Se Cowork e o time vai usar: alertado que projeto Cowork **e local e nao compartilha** — a instrucao precisa de arquivo-fonte versionado

## 7. Fatos de plataforma (verificados)

- Project instructions do chat **consomem janela de contexto**; a orientacao oficial e manter conciso e deixar o especifico de tarefa para o chat.
- Limite de caracteres de project instructions: **nao publicado** pela Anthropic. O unico limite oficial e o de **organization instructions: 3.000**. Nao afirme outro numero.
- Precedencia documentada: **organization > individual**. Entre project instructions, perfil, memoria e skills a Anthropic **nao documenta** quem vence — nao invente ordem; escreva sem depender de conflito.
- Contexto **nao e compartilhado entre chats** do mesmo projeto a menos que va para o knowledge base.
- RAG do project knowledge (ate 10x mais capacidade) e **so plano pago**.
- Cowork empilha **global → projeto → pasta**; instrucoes de pasta podem ser reescritas pelo proprio Claude durante a sessao.
- Cowork **nao le `~/.claude`** — skills e plugins locais do Claude Code precisam ser adicionados em Customize.
- Projeto Cowork vive **so na maquina**: nao sincroniza nem compartilha. Projeto do chat e compartilhavel apenas em Team/Enterprise.
- Cowork le arquivos individuais de ate **50 MB**.
