---
name: mkt-triagem
description: Processa a fila de triagem do sistema de MKT da Fotona no Notion — lê as tarefas em Status=Triagem, propõe dono, prazo, estimativa, área e tipo de trabalho para cada uma, e aplica em lote depois da confirmação. Use sempre que alguém falar em "triagem", "fila de triagem", "as solicitações que chegaram", "o que entrou no formulário", "processar os pedidos novos", "distribuir as tarefas novas", "quem pega o quê", ou pedir para dar dono e prazo a tarefas do Notion — mesmo sem usar a palavra triagem. Também use quando o pedido for revisar tarefas sem dono ou sem prazo.
---

# Triagem da fila de MKT

A triagem é o único ponto do sistema em que alguém olha a fila **inteira** antes de comprometer o
time. É por isso que ela não pode virar carimbo: se cada pedido for despachado isolado, ninguém vê
que três coisas caíram na mesma pessoa na mesma semana.

Esta skill faz o trabalho chato — ler tudo, montar o quadro, escrever no Notion — e deixa a decisão
com quem coordena.

Leia `../../shared/sistema-mkt.md` antes de consultar qualquer coisa: IDs, campos e as armadilhas de
SQL estão lá.

## O fluxo

### 1. Puxe a fila

Consulte ✅ Tarefas em modo SQL, `Status = 'Triagem'`, trazendo `url`, `Tarefa`,
`Objetivo / Por quê`, `Origem`, `Canal de entrada`, `Empresa`, `Categoria`, `Prioridade`,
`date:Data desejada:start`, `Links e referências`, `Responsável`, `Área`.

Fila vazia é uma boa notícia — diga isso em uma linha e pare. Não invente trabalho.

### 2. Carregue o contexto que torna a sugestão defensável

Sem isto a sugestão é chute com cara de análise. Puxe, em paralelo:

- **👥 Time** — quem existe, função, área principal, capacidade semanal.
- **Carga atual** — tarefas abertas por responsável (Status em A fazer/Em produção/Em aprovação/
  Parada, `Subtarefas IS EMPTY`), para não empilhar na pessoa que já está cheia.
- **🧭 Áreas** — para casar assunto com área.
- **🗂️ Projetos e 🚀 Campanhas ativos** — um pedido solto costuma pertencer a algo que já existe.

### 3. Proponha, item a item

Para cada tarefa da fila monte uma linha com: **dono · prazo · estimativa · área · tipo de trabalho ·
prioridade · projeto/campanha**, e uma frase curta dizendo **por que** — a justificativa é o que
permite discordar rápido.

Como decidir cada campo:

- **Dono:** a área do assunto define a função; entre pessoas da mesma função, quem tem menos carga.
  Diga a carga atual junto ("Luana, 11 pontos abertos" vs "Avinho, 24").
- **Prazo:** parta da `Data desejada`. Se ela não couber na carga da pessoa, proponha outra data e
  **diga que está renegociando** — silenciosamente aceitar uma data impossível é o começo do atraso.
  Sem data desejada, use o lead time do tipo de entrega (story 1d · post 3d · reel 5d · YouTube
  10–15d · blog 7d · e-mail 5d; +2 dias se exigir aprovação clínica).
- **Estimativa:** P = até meio dia · M = 1 a 2 dias · G = 3 dias ou mais. Na dúvida entre dois,
  escolha o maior e diga que escolheu — subestimar entope a semana de alguém.
- **Tipo de trabalho:** veio de um plano/campanha existente = Planejado. Apareceu do nada = Ad-hoc.
  Largou tudo = Fire-drill/P0. **Este campo se decide agora e não se muda depois** — é ele que mede
  quanto do mês foi reativo.
- **Prioridade:** P0 só para o que para o negócio. Se tudo é P1, nada é.

Quando faltar informação essencial (não dá para saber a área nem o objetivo), **não invente**:
marque o item como "precisa de resposta do solicitante" e diga qual é a pergunta. Um item mal
triado custa mais que um item que esperou um dia.

### 4. Mostre o quadro e espere

Apresente uma tabela com uma linha por tarefa e as colunas acima, seguida de:

- **Alerta de concentração:** se uma pessoa recebeu mais de ~40% da fila ou passou da capacidade
  semanal, diga isso explicitamente antes de qualquer outra coisa.
- **O que não dá para triar** e por quê.

Então pergunte, de forma que dê para responder rápido: aplicar tudo, aplicar com ajustes, ou revisar
item a item. **Não escreva no Notion antes da confirmação.**

### 5. Aplique

Depois do OK, para cada tarefa confirmada:

- Campos reais (`Responsável`, `Prazo`, `Estimativa`, `Área`, `Tipo de trabalho`, `Prioridade`,
  `Projeto`/`Campanha`) recebem **o que a pessoa confirmou** — e o `Status` vai para `A fazer`.
- `🤖 Sugestão de triagem (IA)` recebe o que você propôs e o porquê, mesmo quando foi aceito. É o
  registro de como a decisão foi tomada.
- `🤖 Resumo (IA)` recebe uma linha do que é a tarefa. `🤖 Analisado em` recebe hoje.

Se o dono confirmado não tiver conta no Notion, escreva o nome em `🤖 Sugestão de triagem (IA)`,
deixe `Responsável` vazio, mantenha o item em `Triagem` e avise. Tarefa em `A fazer` sem dono é
tarefa órfã com aparência de organizada — pior que a fila.

Ao final, diga em uma linha: quantas foram, quantas ficaram, e o link da view de Triagem.

## O que esta skill não faz

Não muda status de tarefa que já saiu da triagem, não repriorização geral do board, não fala com
o time. Se o pedido for "reorganiza o board todo", isso é replanejamento — trabalho de gestão,
não de triagem, e deve ser feito com quem coordena olhando junto.
