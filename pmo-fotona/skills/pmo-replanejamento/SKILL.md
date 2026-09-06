---
name: pmo-replanejamento
description: Propõe o replanejamento de um projeto ou campanha atrasada (ou em 🔴) do MKT da Fotona — lê as tarefas abertas, dependências, prazos e carga dos responsáveis no Notion, pede primeiro o palpite de quem decide, e só então apresenta 2 a 3 cenários (cortar escopo nomeado · empurrar prazo · redistribuir) com quem é afetado, risco e um premortem cada. Nunca aplica: entrega o cenário escolhido como lista de mudanças para a coordenação. Use sempre que a coordenação disser "o projeto estourou", "não vai dar tempo", "o que eu corto", "replaneja o X", "como salvo o congresso", "precisa empurrar", "redistribui isso", "o que faço com o atraso de Y", ou qualquer pedido de decidir o que fazer com algo atrasado — mesmo sem a palavra replanejamento.
---

# Replanejamento — cenários, nunca proposta única

Quando um projeto estoura, a tentação é entregar "o plano". A evidência de campo (Eisenhardt, Nutt)
e o framework de Decision Quality dizem o contrário: decisão com **2–3 alternativas e trade-off
explícito** sai melhor do que proposta única — e o medo de "muitas opções" não se sustenta
(meta-análise de 50 estudos, efeito ≈ 0). E a única intervenção com evidência consistente contra
aceitar a proposta por inércia é fazer a pessoa **dizer o próprio palpite antes de ver a
recomendação** — custa um pouco de satisfação, e vale.

Esta skill segue isso à risca. Ela é a mais "de julgamento" do PMO, e é justamente por isso que
não aplica nada.

Leia `../../CONTEXTO.md` e carregue o contexto.

## 1. Resolva o alvo e leia

Projeto ou campanha, por nome aproximado (Q13; pergunte se ambíguo). Depois:

- **Tarefas abertas** do alvo (Q14): status, prazo, estimativa, responsável, `Bloqueada por` /
  `Bloqueia`, aging (`formulas-espelho`).
- **A data que importa**: `Prazo` do projeto (ou a data do evento / `Período` da campanha).
- **Carga dos responsáveis envolvidos** (Q9, em absoluto; creators fora): o que mais cada um tem
  aberto além deste projeto.
- **Dependências**: o que trava o quê (`Bloqueada por`), e o que está parado em aprovação (Q5).
- **Memória**: o 🤖 Log do PMO sobre este alvo — o que já foi apontado, o que foi decidido antes.

Todo número vem de consulta. `Motivo do bloqueio` só como existe/não existe.

## 2. Mostre o dado e **peça o palpite antes de qualquer cenário**

```
📌 <Alvo> — o que li
• Data-alvo: <data> (faltam N dias úteis)
• Abertas: N (P pontos) · atrasadas: N · em aprovação: N · travadas: N
• Cadeia crítica: <A → B → C> (o que precisa acontecer em ordem)
• Quem está nisso e o que mais tem aberto: <pessoa: N pontos neste projeto / M no total>
• O que o PMO já disse: <registro + desfecho — ou "sem registro">
• Não consegui ler: <ou "tudo lido">

❓ Antes de eu propor: o que você faria? (uma frase — corta, empurra, redistribui, outra coisa)
```

**Pare aqui e espere.** Não mostre cenário nenhum antes da resposta. Se a pessoa disser "me mostra
logo", explique em uma frase por que pergunta antes (é o que reduz aceitação por inércia) e
pergunte de novo — mas não insista uma terceira vez. Grave o palpite no Log como `Dado observado`
adicional ("palpite prévio: …").

## 3. Apresente 2 a 3 cenários, com trade-off e premortem

Sempre entre estes três, adaptados ao caso (às vezes um deles não faz sentido — diga por quê e
mostre dois):

| | Cortar escopo | Empurrar prazo | Redistribuir |
|---|---|---|---|
| **O que muda** | quais entregas **nomeadas** saem ou viram v2 | nova data-alvo e o que ela custa (evento, campanha, promessa) | quem assume o quê, e o que essa pessoa deixa de fazer |
| **Quem é afetado** | solicitante / marca / evento | os mesmos + quem depende da data | as pessoas que recebem **e** as que perdem o item |
| **Risco** | a entrega cortada era a que importava? | a data nova também estoura? | sobrecarrega quem já está no limite? |
| **Premortem** (1 frase) | "Falhou porque…" | "Falhou porque…" | "Falhou porque…" |

Regras do cenário:

- **Sacrifício nomeado, nunca "horas".** "Sai o folder impresso e o vídeo de bastidores" — não "20
  horas de criação". A evidência de intake é clara: recusa com escopo nomeado é o que funciona.
- **Redistribuição cita carga em absoluto** ("a designer tem 11 pontos abertos; a produtora, 24") e
  nunca compara desempenho. Creators não recebem redistribuição.
- **Cada cenário tem um preço explícito.** Se um cenário parece de graça, falta um custo.
- **Não escolha por eles.** Pode dizer qual parece menos arriscado e por quê (com confiança
  declarada), mas a recomendação vem depois dos três, não no lugar deles.
- ≤ 400 palavras para os três cenários juntos.

Termine com **uma pergunta**: "qual dos três — ou uma mistura?".

## 4. Entregue o escolhido como lista de mudanças — e não aplique

Quando a pessoa escolher, devolva a **lista de mudanças** concreta: tarefa por tarefa, o que muda
(prazo, dono, status para Cancelada/Arquivada, projeto). Diga que **não aplicou nada**: quem aplica
é a coordenação, na UI — ou, item a item com confirmação, o `pmo-triagem` para as tarefas que
voltam à fila. Se pedirem "aplica o cenário 2", recuse em uma linha e entregue a lista.

Grave no 🤖 Log do PMO um registro `Tipo = Replanejamento`, `Rito = Sob demanda`: `Dado observado`
= bloco 📌 + palpite prévio; `Sugestão` = os cenários e o escolhido; `Confiança`; `Decidido por`;
`Desfecho` = o que a pessoa escolheu; `Status do fato = Hipótese`, `Válido até` = a nova data-alvo.
Feche pedindo `Sugestão procedente?` em uma palavra.

## O que esta skill não faz

Não muda prazo, dono, status ou RAG de nada. Não fala com o solicitante nem com o time. Não faz a
leitura geral da semana (é `pmo-status-semana`) nem o briefing rápido (é `pmo-briefing` — que, ao
detectar estouro, manda para cá).
