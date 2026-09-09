---
name: mkt-resultados-conteudo
description: Registra os resultados das peças de conteúdo publicadas do MKT da Fotona no Notion nos três ciclos do sistema (D+7, D+15 e D+30 depois da publicação) — lista as peças que estão no ciclo devido, busca alcance, interações, curtidas, comentários, salvamentos, compartilhamentos, visualizações e seguidores por publicação no Reportei (casando pelo link do post) ou aceita os números colados do painel nativo, grava os campos de métrica com o ciclo e a fonte citada, e lê o que performou por pilar e canal no período contra a própria série. Use sempre que alguém falar em "resultados dos posts", "métricas do conteúdo", "atualiza o alcance", "como foram os posts da quinzena", "o que performou melhor", "preenche as métricas no Notion", "insights do Instagram/LinkedIn", "ciclo D+7/D+15/D+30", ou colar números de posts — mesmo sem pedir para gravar. Não use para métricas de tráfego pago ou de campanha (isso é o relatório mensal do PMO) nem para peça ainda não publicada.
---

# Resultados de conteúdo

Alcance, interações e os componentes do engajamento são campos manuais na peça — digitação dupla
que ninguém sustenta, e por isso o sistema não sabe o que funcionou. Esta skill faz a parte chata
(achar as peças que estão no ciclo certo, gravar os números) e devolve a leitura que interessa ao
social media: o que performou, por pilar e por canal, contra o que a própria casa costuma fazer.

Leia `../../CONTEXTO.md` e carregue o contexto. Métricas, ciclos e fontes estão em `conteudo.md`.

## A regra dos três ciclos (decisão do diretor, 08/09/2026)

Cada peça tem as métricas lidas **três vezes**, contadas a partir de `Publicado em`: **D+7**, **D+15**
e **D+30**. Depois do D+30 ninguém atualiza mais — o histórico fica no Reportei, e o número do
Notion é o "retrato de 30 dias" que o relatório mensal compara. O campo `Ciclo de métricas` diz em
que ciclo a peça está; `Métricas atualizadas em` diz quando foi a última leitura.

O ciclo **devido** hoje é: D+30 se `Publicado em` ≤ hoje−30 · senão D+15 se ≤ hoje−15 · senão D+7 se
≤ hoje−7 · senão **nenhum** (a peça ainda não completou 7 dias — não leia; o número dos primeiros
dias ainda está subindo e só polui). Uma peça precisa de leitura quando o ciclo devido é **maior**
que o `Ciclo de métricas` gravado (vazio conta como "nenhum"). Peça já em D+30 **nunca** é regravada,
mesmo que a pessoa peça — explique a regra e ofereça o Reportei para o histórico.

Por que isso importa: sem a regra, cada leitura sobrescreve a anterior em dia aleatório e o
relatório compara uma peça lida em D+3 com outra lida em D+40. Com três ciclos fixos, "alcance"
significa a mesma coisa em todas as peças.

## O que esta skill escreve

Em peça com `Link do post` preenchido — publicado é o link, não o status — e no ciclo devido:
`Alcance` · `Engajamento` (total de interações) · `Curtidas` · `Comentários` · `Salvamentos` ·
`Compartilhamentos` · `Visualizações` · `Seguidores ganhos` · `Cliques/Leads` (só quando alguém
informar) · e **sempre junto** `Ciclo de métricas` (o ciclo que está sendo lido) e `Métricas
atualizadas em` (hoje). Classe 3 do `contrato-de-escrita.md`. Todo número gravado tem **fonte
citada** ("Reportei · Instagram · lido em 06/09 14:10" ou "colado pela social media do painel do
Instagram"). Número que você não leu de nenhuma fonte não entra: estimativa de métrica é o jeito
mais rápido de o relatório mensal mentir. Campo que a fonte não trouxe fica como estava — não
zere.

O **GHL não serve** e não vale tentar (testado em 06/09/2026): a analytics dele é agregada por conta
e por período, e as contas não sincronizam os posts publicados fora do Social Planner. Se alguém
pedir "puxa do GHL", diga isso em uma linha.

Peça sem `Link do post` → não grava; diga que a peça consta como não publicada e que o link é o que
a marca como publicada. Não mexe em nenhum outro campo.

## O fluxo

### 1. Ache o que está no ciclo

Consulta **Q12** (publicadas — padrão: as que têm `Publicado em` nos últimos 45 dias; a pessoa pode
pedir o mês) e classifique cada peça: ciclo devido × ciclo gravado. Liste em três grupos, por data:

- **Para ler agora** — ciclo devido > ciclo gravado (diga qual: "D+15, estava em D+7").
- **Ainda não** — menos de 7 dias de publicada, ou já lida no ciclo devido (diga a próxima data).
- **Fechadas** — em D+30; não voltam a entrar.

Só o primeiro grupo segue. Se ele estiver vazio, diga isso e pule para a leitura do período (§4).

### 2. Pegue os números — Reportei primeiro, colagem depois

**Fonte 1: o Reportei** (conector MCP), quando houver projeto para a empresa da peça. O caminho é
`list_projects` → `list_integrations` (achar o `instagram_business` daquela empresa) →
`get_metrics_data` com a métrica **`ig:media_datatable`**, no período que cubra `Publicado em` das
peças. Passe o objeto da métrica exatamente como o `list_metrics` devolve.

Cada linha é uma publicação: o primeiro elemento traz `url` (o **permalink**) e `error`; depois vêm,
nesta ordem, `type`, `reach`, `views`, `total_interactions`, `post_interactions_rate`, `likes`,
`comments`, `saved`, `follows`, `profile_visits`, `shares`, `created_at`. **Case pelo `url` com o
`Link do post` da peça** (ignore `?igsh=`, barra final e `www.`) — é o casamento confiável. Só use a
data e a legenda como desempate quando o link no Notion estiver encurtado ou diferente, e diga que
casou por aproximação.

O mapeamento é direto:

| Reportei | Campo no Notion |
|---|---|
| `reach` | `Alcance` |
| `total_interactions` | `Engajamento` (use como veio, não a soma dos componentes) |
| `likes` · `comments` · `saved` · `shares` · `views` | `Curtidas` · `Comentários` · `Salvamentos` · `Compartilhamentos` · `Visualizações` |
| `follows` | `Seguidores ganhos` (só quando vier número) |

**`Cliques/Leads` não vem do Reportei** — o Instagram não expõe cliques em post orgânico. Deixe como
está ou peça à pessoa.

Duas armadilhas do dado real, e as duas fariam o relatório mentir:

- Linha com o campo `error` preenchido (por exemplo *"Posted before the convertion to business
  account"*) vem com **tudo zerado**. Isso é **ausência de dado, não zero**. Não grave; liste como
  "sem métrica disponível" e diga o motivo.
- `follows` e `profile_visits` vêm `-` em reels. Campo com `-` é vazio, não zero.

Reels e IGTV têm tabelas próprias (`ig:reels_datatable`, `ig:igtv_datatable`) quando você precisar
de detalhe por formato; a `ig:media_datatable` já cobre o essencial.

**Fonte 2: a pessoa cola** — quando não há projeto no Reportei para aquela empresa, quando a peça
não é do Instagram, ou quando o dado ainda não sincronizou. Aceite em qualquer formato razoável
("carrossel GLP1 — 4.2k alcance, 310 interações, 18 cliques"); repita de volta em tabela com o que
entendeu antes de gravar. Se vierem só curtidas, comentários e salvamentos, some para
`Engajamento` e diga a soma; grave os componentes que vieram e deixe os outros como estão.

Em qualquer das duas, mostre a tabela por peça **com a fonte e o ciclo** e pergunte "gravo?" antes
de escrever.

Se uma peça não tiver número em nenhuma fonte, fica como está e aparece na lista de pendentes — não
invente, e não avance o `Ciclo de métricas` de uma peça que não recebeu número.

### 3. Grave, item confirmado

Uma peça por vez ou em bloco explícito ("grava as cinco como estão"). Antes de gravar, confira que a
página tem `Link do post` e que não mudou desde que você leu (`last_edited_time`). Em cada gravação
vão os números **mais** `Ciclo de métricas` = o ciclo lido e `Métricas atualizadas em` = hoje.

### 4. Leia o período

Depois de gravar (ou se não havia nada para ler), a leitura, em absoluto: por **pilar** e por
**canal**, alcance e interações somados e medianos; **a peça-destaque** (maiores interações) e as
que ficaram **abaixo da mediana da própria série** (a série é o que a casa publicou nos últimos 2–3
meses no mesmo canal — se não houver série, diga que ainda não há base). Compare só peça no mesmo
ciclo (D+7 com D+7): um D+30 sempre "ganha" de um D+7 e a comparação mente. Uma frase do que se
repete: pilar que costuma puxar, canal onde o formato X rende, dia da semana se houver padrão com
contagem. Sem "bom"/"ruim"; sem benchmark de mercado (não veio da consulta).

Termine com **uma pergunta** para a pauta do próximo período ("o educativo rendeu 2× a mediana
em três das quatro peças — vale subir de 1 a cada 3 para 1 a cada 2?").

### 5. Registre

🤖 Log do PMO: `Tipo = Resultados de conteúdo`, `Rito = Sob demanda`, `Dado observado` = a tabela
por pilar/canal com os ciclos, `Sugestão` = a pergunta, `Status do fato = Hipótese`, `Decidido por` =
a pessoa. Em **modo fixture**, descreva o registro e as gravações em vez de executar.

## O que esta skill não faz

Não grava métrica de tráfego pago nem de campanha (o Reportei traz Ads, mas isso é leitura do
relatório mensal, não da peça). Não muda status, data, pilar ou dono da peça. Não compara a
performance de pessoas (a peça tem dono; a leitura é por pilar e canal). Não cria projeto nem
integração no Reportei — se faltar projeto para a empresa da peça, diga isso e siga pela colagem.
Não relê peça fechada em D+30. Quando a Onda B do n8n estiver no ar (leitura automática diária
pelos mesmos ciclos), esta skill vira o caminho manual para o que o robô não casou — a regra é a
mesma nas duas superfícies.
