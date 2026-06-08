---
name: whatsapp-formatter
description: Formata mensagens pro WhatsApp com a sintaxe nativa, removendo Markdown que quebra (asterisco duplo, #, links). Use ao pedir texto/mensagem pro WhatsApp ou zap, formatar, ou converter pro zap.
intent: Skill que produz mensagens prontas para copiar e colar no WhatsApp usando exclusivamente a sintaxe nativa do app (negrito com asterisco simples, italico com underscore, listas, citacoes). Resolve a falha recorrente em que o Claude gera Markdown (`**negrito**`, `# titulo`, `[texto](url)`) que aparece cru na tela porque o WhatsApp nao tem renderizador Markdown. Garante o resultado com um passo obrigatorio de auto-verificacao (lint) que varre a saida atras dos padroes que quebram, antes de entregar. Foco em avisos de equipe e mensagens pessoais. Roda identica no Claude Code e no Claude Desktop.
effort: high
---

# WhatsApp Formatter

Produz mensagens prontas pra colar no WhatsApp **sem nenhum simbolo de Markdown cru** aparecendo na tela.

## Por que esta skill existe

O Claude, por padrao, escreve em **Markdown** — `**negrito**`, `# titulo`, `[texto](url)` — porque assume que o destino tem um renderizador que transforma esses simbolos em formatacao. **O WhatsApp nao tem renderizador de Markdown.** Ele usa uma sintaxe propria e mais pobre. Quando voce cola Markdown la, os simbolos aparecem crus (`**`, `#`, colchetes) e a mensagem fica feia. Por isso "nunca da certo".

A correcao nao e "lembrar melhor" — o erro `**` -> `*` e automatico demais. A garantia vem do **passo de lint** no fim (secao "Verificacao obrigatoria"): antes de entregar, voce varre a propria saida atras dos padroes que quebram e os reescreve.

## Como acionar (4 modos de input)

Detecte o modo pelo que o usuario manda. Todos produzem o mesmo entregavel: **uma** mensagem formatada pro WhatsApp.

| Modo | Sinal | O que fazer |
|------|-------|-------------|
| **Formatar texto cru** | Usuario cola um texto ja escrito | Aplicar a formatacao WhatsApp ideal. NAO reescrever o conteudo — so estruturar e formatar. |
| **Escrever + formatar** | Usuario descreve o que quer comunicar | Redigir a mensagem do zero, ja formatada. |
| **Converter Markdown** | Usuario cola algo em Markdown (ou output anterior do Claude) | Converter pra sintaxe nativa do WhatsApp. |
| **Reformatar a ultima mensagem** | "manda isso formatado pro zap", "formata a mensagem acima" | Pegar a ultima mensagem relevante da conversa e formatar pro WhatsApp. |

Se o modo nao estiver claro, assuma **Formatar texto cru** quando vier um bloco de texto, e **Escrever + formatar** quando vier uma instrucao. Nao pergunte se da pra inferir.

## Sintaxe nativa do WhatsApp (a unica permitida na saida)

Cada estilo usa **UM** caractere de cada lado, **colado** ao texto (sem espaco interno).

| Estilo | Sintaxe | Exemplo |
|--------|---------|---------|
| Negrito | `*` de cada lado | `*importante*` |
| Italico | `_` de cada lado | `_observacao_` |
| Tachado | `~` de cada lado | `~cancelado~` |
| Monoespacado inline | `` ` `` (1 crase) | `` `codigo` `` |
| Bloco monoespacado | 3 crases | ` ```bloco``` ` |
| Lista com marcador | `-` + espaco, inicio de linha | `- item` |
| Lista numerada | `1.` + espaco, inicio de linha | `1. passo` |
| Citacao | `>` + espaco, inicio de linha | `> destaque` |

Combinacoes funcionam aninhando: `*_negrito e italico_*`. **Excecao:** monoespacado (crases) cancela qualquer outro estilo no trecho — nao combine.

Detalhes finos, casos de borda e limites: veja [references/conversao.md](references/conversao.md).

## Regras de conversao Markdown -> WhatsApp

Estas sao as trocas que mais quebram. Aplique sempre:

| Markdown (errado no zap) | WhatsApp (certo) | Observacao |
|--------------------------|------------------|------------|
| `**negrito**` ou `__negrito__` | `*negrito*` | Asterisco **simples**. Erro nº 1. |
| `*italico*` (markdown) | `_italico_` | No WhatsApp, asterisco simples e NEGRITO. Italico = underscore. |
| `~~tachado~~` | `~tachado~` | Til simples. |
| `# Titulo`, `## Titulo` | `*TITULO*` + linha em branco | WhatsApp nao tem heading. Simule com negrito (caixa alta opcional). |
| `[texto](url)` | `texto: url` | WhatsApp nao tem link com ancora. So URL crua fica clicavel. |
| Tabela com `\|` | lista `*Campo:* valor` | Sem tabela nativa. |
| `---` (linha) | linha em branco ou `------` | Sem regua horizontal. |

Mapa completo de degradacao (imagens, footnotes, links de varios tipos): [references/conversao.md](references/conversao.md).

## Verificacao obrigatoria (lint) — NUNCA pule

Antes de entregar, leia sua propria mensagem e procure cada um destes padroes. Se achar, conserte. Eles sao exatamente o que faz a mensagem quebrar quando colada:

1. `**` ou `__` em qualquer lugar (negrito Markdown) -> trocar por `*`.
2. `#` no inicio de uma linha (heading) -> virar `*negrito*`.
3. `[...](...)` (link Markdown) -> virar `texto: url`.
4. `~~` (tachado duplo) -> trocar por `~`.
5. Estilo com espaco interno: `* texto *`, `_ texto _` -> colar o simbolo no texto.
6. `-`, `>` ou `1.` sem espaco depois -> nao formata; adicionar o espaco.
7. Italico escrito com asterisco simples quando a intencao era italico -> trocar por `_` (senao sai negrito).
8. `|` de tabela cru -> degradar pra lista.

Esse passo e a razao de a skill existir. Se voce entregar sem fazer o lint, provavelmente vai vazar Markdown.

## Legibilidade (mensagem que da gosto de ler)

WhatsApp e tela pequena. Estruture pra ser escaneavel:

- **Pseudo-titulo:** negrito na primeira linha (`*COMUNICADO — Reuniao de sexta*`), seguido de linha em branco.
- **Respire:** linha em branco entre blocos. Evite paredao de texto.
- **Uma ideia central** por mensagem. Se ficou muito longa, sugira quebrar em duas.
- **Emoji como rotulo**, com parcimonia: 📅 quando · 📍 onde · ✅ acao. Nao encha de emoji — polui.
- **`>` pro que e critico** (prazo, decisao).
- Sem CAIXA ALTA em excesso (so em pseudo-titulo curto).

**Default sobrio — decore com proposito, nao por enfeite.** A mensagem boa e enxuta, nao uma "moldura". O criterio e dose, nao proibicao:

- **Divisoria (`━━━` ou `------`): use so pra separar 2-3 BLOCOS grandes** que o leitor precisa distinguir de relance (ex: CHEGADAS x SAIDAS numa lista longa). Uma divisoria entre os macro-blocos ajuda; uma divisoria em cada dia/subsecao vira ruido — nesse caso basta negrito + linha em branco.
- **Evite** titulo-geral redundante (ex: "✈️ AGENDA" antes de uma lista que ja se explica) e emoji em toda linha/dia.
- Use negrito nos titulos de secao/dia, bullets com `-`, e emoji so nos macro-blocos.
- Quando varias listas tem a mesma estrutura (ex: chegadas e saidas por dia), agrupe do mesmo jeito pra dar consistencia.
- Va pra um estilo mais visual (mais divisorias, mais emoji) se o usuario pedir ("manda mais chamativo/decorado").

Regra de bolso: a divisoria existe pra responder "onde comeca a outra parte?". Se nao ha duas partes grandes pra separar, ela nao tem funcao.

Templates de aviso pra equipe e exemplos prontos: [references/legibilidade.md](references/legibilidade.md).

## O que o WhatsApp NAO faz (nao prometa)

Sem: heading real, link com texto-ancora, tabela com grade, cor, tamanho de fonte, sublinhado, alinhamento/centralizacao, imagem dentro do texto. Ao encontrar qualquer um, **degrade com substituto** (secao de conversao) — nunca prometa fidelidade ao original.

## Formato da saida

Entregue **uma** mensagem final, dentro de um bloco de codigo, pra o usuario copiar sem que o renderizador do chat coma os asteriscos.

- Use uma cerca de **4 crases** (````) ao redor da mensagem. Isso deixa os `*`, `_` e ate blocos de 3 crases do WhatsApp visiveis e copiaveis.
- Nada de comentario dentro do bloco — so a mensagem pura.
- Por padrao, **nao** ofereca variacoes nem explicacao. Uma mensagem, limpa, pronta. Se o usuario pedir alternativas, ai sim.

Exemplo de entrega:

````
*COMUNICADO — Reuniao de sexta*

Pessoal, alinhamento rapido sexta pra fechar o mes.

📅 Sexta, 14h
📍 Sala 2 / link no calendario

> Confirmem presenca ate quinta.

Qualquer duvida, chama aqui. 🙏
````

Depois do bloco, no maximo uma linha curta tipo "Pronto, e so copiar." — sem firula.

## References

| Arquivo | Quando ler |
|---------|------------|
| [references/conversao.md](references/conversao.md) | Casos de borda da sintaxe, mapa completo de degradacao, limites de caracteres |
| [references/legibilidade.md](references/legibilidade.md) | Templates de aviso/comunicado, padroes de estrutura, uso de emoji |
