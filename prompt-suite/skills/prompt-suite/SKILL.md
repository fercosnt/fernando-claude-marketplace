---
name: prompt-suite
description: Entrypoint do plugin prompt-suite. Classifica o pedido por SUPERFICIE (onde a instrucao vai morar) e roteia para a skill certa — claude-md-generator (Claude Code / CLAUDE.md / .claude/), project-instructions (Projects do chat e do Cowork) ou prompt-engineer (prompt avulso, system prompt, N8N, Notion Custom AI, OpenClaw). NAO escreve a instrucao sozinho. Ativar quando o usuario pedir ajuda para "escrever instrucoes pro Claude", "criar um prompt", "configurar meu projeto", "fazer o Claude se comportar assim", "melhorar minhas instrucoes", "montar isso pro meu time", ou quando pedir instrucao/prompt sem deixar claro para qual superficie. Tambem ativar quando o pedido envolver mais de uma superficie ao mesmo tempo (por exemplo, projeto de codigo que o time tambem usa no Cowork).
intent: >
  As tres skills do plugin respondem a mesma pergunta — o que escrever para mudar o comportamento
  do Claude — mas em superficies diferentes, e escolher errado custa caro: CLAUDE.md num Chat
  Project nao existe, instrucao de Cowork num chat manda salvar arquivo em pasta que nao ha,
  prompt avulso congelado numa instrucao permanente vira regra morta. Esta skill nao redige nada;
  ela faz a unica pergunta que resolve (onde isso vai morar, e por quanto tempo) e entrega o
  pedido pronto para a skill certa — ou para mais de uma, na ordem certa, quando o caso pede.
effort: medium
---

# prompt-suite

Entrypoint do plugin. **Classifica e roteia. Nao redige.**

## 1. A pergunta que resolve

Todo pedido deste plugin cai em uma de tres superficies. A pergunta que separa:

> **Onde esse texto vai morar, e por quanto tempo?**

| Onde mora | Duracao | Superficie | Skill |
|---|---|---|---|
| Arquivo no repositorio (`CLAUDE.md`, `.claude/`) | Enquanto o repo existir | **Claude Code** | `claude-md-generator` |
| Campo de instrucoes de um projeto (chat ou Cowork) | Enquanto o projeto existir | **Project** | `project-instructions` |
| Uma mensagem, um system prompt, um node | Aquela execucao | **Prompt avulso** | `prompt-engineer` |

## 2. Roteamento por sinal

| Sinal no pedido | Superficie | Rota |
|---|---|---|
| "CLAUDE.md", ".claude/", hook, subagent, slash command, "meu repo", "esse projeto de codigo", terminal | Claude Code | `claude-md-generator` |
| "projeto do Claude", "custom instructions", "project instructions", claude.ai, "anexei arquivos", "project knowledge" | Chat Project | `project-instructions` |
| "Cowork", "pasta local", "ele roda sozinho", "tarefa agendada", "gera a planilha", "entregavel", "global instructions" | Cowork Project | `project-instructions` |
| "prompt", "system prompt", "melhora esse prompt", "hook do N8N", "agente do N8N", "Notion Custom AI", "OpenClaw" | Prompt avulso | `prompt-engineer` |
| "prompt de imagem", Midjourney, Flux, Nano Banana, Higgsfield, Ideogram | **Fora do plugin** | Diga que nao e aqui e aponte `deck-image-prompts` |

**Precedencia quando ha mais de um sinal:** nome de arquivo (`CLAUDE.md`) vence nome de produto, que vence palavra generica ("prompt"). "Melhora o prompt do meu CLAUDE.md" → Claude Code, nao prompt avulso.

## 3. Quando o sinal nao resolve

No maximo **duas perguntas**, nesta ordem. Pare assim que a resposta bastar.

1. **"Isso vale para toda conversa daqui pra frente, ou e pra tarefa de agora?"**
   Toda conversa → superficie persistente (siga para a pergunta 2). Tarefa de agora → `prompt-engineer`.

2. **"Voce trabalha nisso pelo terminal/editor, ou pelo app do Claude?"**
   Terminal/editor → `claude-md-generator`. App do Claude → `project-instructions` (a propria skill separa Chat de Cowork).

Nunca faca as duas perguntas se o pedido ja respondeu uma. Nunca pergunte a superficie duas vezes de jeitos diferentes.

## 4. Pedidos que precisam de mais de uma skill

Existem e sao comuns. Nao escolha uma e ignore o resto — **diga a ordem e execute em sequencia.**

| Caso | Ordem |
|---|---|
| Projeto de codigo que o time tambem opera pelo Cowork | `claude-md-generator` primeiro (o repo e a fonte), depois `project-instructions` para o Cowork apontar para ele |
| "Meu prompt gigante vive colado em toda conversa" | `project-instructions` — o que e permanente vira instrucao de projeto; `prompt-engineer` so para o resto que sobrou |
| Instrucao de projeto que na verdade era um processo repetivel | `project-instructions` roteia a regra para virar skill; entao `skill-creator` (fora deste plugin) |
| Projeto novo do zero, sem nada escrito | `project-instructions` no modo PACOTE — ele cobre instrucao + knowledge + connectors + setup de time |

## 5. Como entregar o pedido para a skill de destino

Nao apenas anuncie a rota. **Passe o contexto ja apurado**, para a skill nao repetir entrevista:

- O que o usuario disse que quer produzir
- Para quem (so ele, time, cliente)
- O que ele ja tem escrito, se colou algo
- A superficie confirmada, e por que ela

Formato da passagem, uma linha antes de invocar:

> Superficie: [X], porque [sinal]. Contexto ja apurado: [resumo em uma frase]. Roteando para `[skill]`.

Se o usuario ja deu material suficiente, a skill de destino deve **confirmar e seguir**, nao perguntar do zero.

## 6. Limites

- Esta skill **nao redige instrucao, prompt nem CLAUDE.md**. Se voce se pegar escrevendo o texto final aqui, roteou errado — invoque a skill.
- Prompt de imagem nao pertence a este plugin. A tese e outra: descreve cena para modelo de difusao, nao instrui agente. Aponte `deck-image-prompts`.
- Se o pedido nao for sobre instruir um modelo (ex: "escreve o post", "revisa o contrato"), diga que nao e aqui e devolva sem rotear.
