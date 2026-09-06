# Chat Project — instrucoes para projetos do claude.ai / Claude Desktop

Alvo conversacional. A instrucao governa **como a resposta sai**: o que o Claude assume, o que produz, em que forma, e quando para pra perguntar. Ele nao executa nada, nao tem pasta, nao salva arquivo.

## 1. Mecanica

| Item | Fato |
|---|---|
| Onde fica | Painel do projeto, lado direito, "Set project instructions" |
| Escopo | Todos os chats daquele projeto |
| Custo | **Consome janela de contexto.** Cada caractere e menos espaco pra knowledge e conversa |
| Limite de caracteres | Nao publicado pela Anthropic. Nao afirme numero. (O unico limite oficial e organization instructions: 3.000) |
| Companheiros | Project knowledge (arquivos), memoria do projeto, skills |
| Contexto entre chats | **Nao passa.** O que precisa sobreviver entre conversas vai pro knowledge |
| Compartilhamento | So Team/Enterprise |

Consequencia pratica: instrucao longa nao e "mais completa", e mais cara. Cada regra disputa espaco com o material que o Claude precisa ler pra acertar.

## 2. Estrutura recomendada

Cinco blocos, nessa ordem. **Pule os que nao se aplicam** — projeto simples usa tres.

1. **Cabecalho** — dono, data de revisao, uma frase de proposito.
2. **Contexto** — quem e o usuario/time, que negocio e esse, vocabulario interno.
3. **O trabalho** — o que esse projeto produz, e a forma do resultado bom.
4. **Regras** — o que fazer, o que evitar (sempre com substituto), quando parar e perguntar.
5. **Fontes** — o que esta no knowledge e quando consultar.

Prosa curta em blocos rotulados. Tags XML so se houver 3+ blocos distintos ou exemplos colados dentro — caso contrario e peso morto.

## 3. Template comentado

```
Dono: [nome] · Revisar em: [data]
Para que serve: [uma frase — o que esse projeto produz]

CONTEXTO
[Quem somos, o que fazemos, quem le o que sai daqui.]
[Vocabulario: sigla = significado. Uma linha cada.]

O TRABALHO
Neste projeto voce [verbo + entregavel principal].
Resultado bom se parece com: [formato, tamanho, estrutura].
[Se houver exemplo curto, cole aqui — vale mais que adjetivo.]

REGRAS
- [Gatilho concreto] → [acao esperada].
- Prefira [X] a [Y], porque [motivo em meia linha].
- Quando [condicao de incerteza], pergunte antes de seguir.

FONTES
- [arquivo.md] = [o que tem dentro]. Consulte antes de [situacao].
- Nao invente [tipo de dado]; se nao estiver nas fontes, diga que nao tem.
```

## 4. Exemplo enxuto (~900 caracteres)

Projeto de revisao de textos clinicos antes de publicar.

```
Dono: Fernando · Revisar em: 2027-03-01
Para que serve: revisar textos clinicos da Beauty Smile antes de publicar.

CONTEXTO
Clinica odontologica. Quem le o texto final e paciente leigo, nao dentista.

O TRABALHO
Voce revisa o texto que eu colar e devolve a versao corrigida, seguida de
uma lista curta do que mudou e por que.

REGRAS
- Trate promessa de resultado como erro: reescreva pra expectativa realista.
- Termo tecnico so entra se vier explicado na mesma frase.
- Nao mude o sentido clinico pra melhorar a leitura. Se o texto disser algo
  que parece errado, aponte e pergunte — nao corrija por conta.
- Devolva o texto inteiro, nunca so os trechos alterados.

FONTES
- guia-de-marca.pdf = tom de voz e termos proibidos. Consulte sempre.
```

Repare no que **nao** esta ali: nenhum "voce e um revisor senior", nenhum "seja claro e profissional", nenhum fato clinico colado — isso e knowledge.

## 5. Exemplo completo (projeto de time)

Projeto compartilhado de propostas comerciais.

```
Dono: Fernando · Revisar em: 2027-01-15
Para que serve: escrever e revisar propostas comerciais de equipamento.

CONTEXTO
Vendemos equipamento a laser pra clinicas. Quem le a proposta e o dono da
clinica — decide por retorno financeiro, nao por especificacao tecnica.
Vocabulario: TCO = custo total em 5 anos. Payback = meses pra se pagar.
"Peer-facing" = material pra dentista. "Patient-facing" = pra paciente.

O TRABALHO
Voce produz a proposta a partir do briefing que eu colar.
Estrutura fixa: problema da clinica → o que o equipamento resolve →
numeros (TCO, payback, 3 cenarios) → proximo passo.
Resultado bom: 2 a 3 paginas, numero sempre com a premissa ao lado.

REGRAS
- Todo numero financeiro vem com a premissa que o gerou. Numero solto,
  corte.
- Cenario sempre em tres: conservador, provavel, otimista. Nunca um so.
- Prefira "reduz X em N meses" a "aumenta a eficiencia" — beneficio
  mensuravel, nao adjetivo.
- Nao cite estudo, registro Anvisa ou dado de mercado que nao esteja nas
  fontes. Faltou dado, escreva [FALTA: o que] e siga.
- Se o briefing nao disser o porte da clinica, pergunte antes de escrever —
  muda todos os numeros.

FONTES
- catalogo-precos.xlsx = preco e configuracao vigentes.
- casos-clinicas.md = resultados reais ja documentados, com nome do caso.
- guia-de-marca.pdf = tom e termos proibidos.
Se a informacao nao esta nesses tres, ela nao existe pra esta proposta.
```

## 6. O que nunca colocar

| Nao coloque | Por que | Onde vai |
|---|---|---|
| Tabela de precos, dados, estudos | Fato ocupa contexto em toda conversa | Knowledge |
| "Voce e um especialista com 20 anos..." | Nao muda comportamento, gasta espaco | Lixo |
| Processo detalhado de uma tarefa so | So dispara as vezes | Skill |
| Preferencia sua geral (tom, tamanho de resposta) | Vale em todo projeto seu | "Instructions for Claude" no perfil |
| Instrucao pra salvar arquivo, rodar script, acessar pasta | Chat nao faz isso | Cowork |
| Uma tarefa especifica ("escreva o post de outubro") | Instrucao e permanente | Prompt do chat |

## 7. Orcamento

- Mire **1.500–2.500 caracteres**.
- Acima de ~3.500: pare e pergunte o que pode virar knowledge.
- Projeto simples resolve em 600–1.000. Nao encha pra parecer completo.
- Metrica melhor que contagem: **quantas regras disparam de fato**. Instrucao de 10 regras onde 3 disparam funciona pior que 3 regras que sempre disparam — porque ensina o Claude a tratar o bloco como decorativo.
