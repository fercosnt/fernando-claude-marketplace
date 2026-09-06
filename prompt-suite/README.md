# prompt-suite

As tres superficies onde se escreve instrucao para o Claude — e um orquestrador que decide qual delas e a sua.

## A pergunta que o plugin responde

> **Onde esse texto vai morar, e por quanto tempo?**

| Onde mora | Duracao | Superficie | Skill |
|---|---|---|---|
| Arquivo no repositorio (`CLAUDE.md`, `.claude/`) | Enquanto o repo existir | Claude Code | `claude-md-generator` |
| Campo de instrucoes de um projeto (chat ou Cowork) | Enquanto o projeto existir | Project | `project-instructions` |
| Uma mensagem, um system prompt, um node | Aquela execucao | Prompt avulso | `prompt-engineer` |

Escolher errado custa caro, e o erro e silencioso: `CLAUDE.md` nao existe num Chat Project; instrucao de Cowork colada num chat manda salvar arquivo em pasta que nao ha; prompt avulso congelado numa instrucao permanente vira regra que nunca dispara — e regra morta ensina o modelo a tratar o bloco inteiro como decorativo.

## As quatro skills

### `prompt-suite` — entrypoint

Classifica e roteia. **Nao redige.** Se o sinal do pedido nao bastar, faz no maximo duas perguntas: se vale para toda conversa daqui pra frente, e se voce trabalha pelo terminal ou pelo app. Passa o contexto ja apurado para a skill de destino, para nao repetir entrevista. Tambem cobre os casos que precisam de mais de uma skill, na ordem certa.

### `project-instructions` — Projects do chat e do Cowork

Dois alvos com modelos mentais opostos: **Chat Project** governa como a resposta sai; **Cowork Project** governa o trabalho, a definicao de pronto e onde salva. O centro e um **roteador de camadas** com teste de permanencia (duravel / nao-obvia / sem casa melhor), que decide onde cada regra mora antes de redigir. Tres modos: CRIAR, AUDITAR (9 falhas nomeadas, tabela sintoma→causa, reescrita completa e testes concretos) e PACOTE (knowledge, folders, connectors com os 3 modos de permissao, skills, memoria e o pacote replicavel de time).

### `claude-md-generator` — Claude Code

Cria ou audita `CLAUDE.md` e a estrutura `.claude/` inteira: hooks, commands, subagents, settings. Principios de concisao e posicionamento aplicados de pesquisa de 60+ fontes.

### `prompt-engineer` — prompt avulso e outras plataformas

System prompt, N8N, Notion Custom AI, OpenClaw. Tecnicas oficiais da Anthropic (XML, Chain of Thought, Few-Shot, Role, Chaining), scorecard de qualidade em 4 dimensoes, e modos criar / melhorar / analisar.

## Alguns fatos que as skills respeitam

Verificados contra a documentacao oficial — e a suite se recusa a inventar o que a Anthropic nao publica.

- Project instructions **consomem janela de contexto**; a orientacao oficial e manter conciso.
- **Nao existe limite de caracteres publicado** para project instructions. O unico limite oficial e o de organization instructions: 3.000.
- A unica precedencia documentada e **organization > individual**. Entre project instructions, perfil, memoria e skills a Anthropic nao documenta ordem.
- Cowork empilha **global → projeto → pasta**, e instrucao de pasta pode ser reescrita pelo proprio Claude durante a sessao.
- Cowork **nao le `~/.claude`**: skill que so existe la precisa ser adicionada em Customize.
- **Projeto Cowork e local — nao sincroniza nem compartilha.** Nao existe "mandar o projeto" pro time; existe arquivo-fonte versionado mais checklist de setup.

## Fora do escopo

**Prompt de imagem nao esta aqui.** A tese e outra: descreve cena para modelo de difusao, nao instrui agente. Use `deck-image-prompts` (plugin `deck-builder`).

## Instalacao

```
/plugin marketplace add fercosnt/fernando-claude-marketplace
/plugin install prompt-suite@fernando-claude-marketplace
```

> Se voce ja tem `project-instructions`, `prompt-engineer` ou `claude-md-generator` soltas em `~/.claude/skills/`, remova as copias soltas depois de instalar — senao a mesma skill aparece duas vezes no seletor.

## Uso

```
/prompt-suite
```

Ou em linguagem natural: "escreve as instrucoes do meu projeto do Cowork", "meu CLAUDE.md ta enorme e ele ignora", "melhora esse system prompt do meu agente do N8N", "monta isso pro meu time".

## Estrutura

```
prompt-suite/
├── .claude-plugin/plugin.json
└── skills/
    ├── prompt-suite/            entrypoint — classifica e roteia
    ├── project-instructions/    Chat Project e Cowork Project (4 references)
    ├── claude-md-generator/     CLAUDE.md e .claude/ (4 references)
    └── prompt-engineer/         prompt avulso, N8N, Notion, OpenClaw (8 references)
```
