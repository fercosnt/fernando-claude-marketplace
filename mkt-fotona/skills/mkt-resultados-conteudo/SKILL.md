---
name: mkt-resultados-conteudo
description: Registra os resultados das peças de conteúdo publicadas do MKT da Fotona no Notion — lista as peças com link de post e sem métrica, busca alcance e engajamento por publicação no Reportei (casando pelo link do post) ou aceita os números colados do painel nativo, grava só esses três campos com a fonte citada, e lê o que performou por pilar e canal no período contra a própria série. Use sempre que alguém falar em "resultados dos posts", "métricas do conteúdo", "atualiza o alcance", "como foram os posts da quinzena", "o que performou melhor", "preenche as métricas no Notion", "insights do Instagram/LinkedIn", ou colar números de posts — mesmo sem pedir para gravar. Não use para métricas de tráfego pago ou de campanha (isso é o relatório mensal do PMO) nem para peça ainda não publicada.
---

# Resultados de conteúdo

Alcance, engajamento e cliques hoje são campos manuais na peça — digitação dupla que ninguém
sustenta, e por isso o sistema não sabe o que funcionou. Esta skill faz a parte chata (achar as
peças que faltam, gravar os números) e devolve a leitura que interessa ao social media: o que
performou, por pilar e por canal, contra o que a própria casa costuma fazer.

Leia `../../CONTEXTO.md` e carregue o contexto. Métricas, fórmula de engajamento e fontes estão em
`conteudo.md`.

## O que esta skill escreve

Só `Alcance`, `Engajamento` e `Cliques/Leads`, e só em peça com `Link do post` preenchido —
publicado é o link, não o status. Classe 3 do `contrato-de-escrita.md`. Todo número gravado tem
**fonte citada** ("Reportei · Instagram · lido em 06/09 14:10" ou "colado pela social media do
painel do Instagram"). Número que você não leu de nenhuma fonte não entra: estimativa de métrica é o
jeito mais rápido de o relatório mensal mentir.

O **GHL não serve** e não vale tentar (testado em 06/09/2026): a analytics dele é agregada por conta
e por período, e as contas não sincronizam os posts publicados fora do Social Planner. Se alguém
pedir "puxa do GHL", diga isso em uma linha.

Peça sem `Link do post` → não grava; diga que a peça consta como não publicada e que o link é o que
a marca como publicada. Não mexe em nenhum outro campo.

## O fluxo

### 1. Ache o que falta

Consulta **Q12** (publicadas no período — padrão: os últimos 15 dias; a pessoa pode pedir o mês) e
filtre: métrica vazia, ou métrica com mais de 14 dias desde `Publicado em` (a janela de 7–14 dias é
quando o número estabiliza). Liste por data: peça · canal · pilar · link · o que falta.

### 2. Pegue os números — Reportei primeiro, colagem depois

**Fonte 1: o Reportei** (conector MCP), quando houver projeto para a empresa da peça. O caminho é
`list_projects` → `list_integrations` (achar o `instagram_business` daquela empresa) →
`get_metrics_data` com a métrica **`ig:media_datatable`**, no período das peças. Passe o objeto da
métrica exatamente como o `list_metrics` devolve.

Cada linha é uma publicação e traz `url` (o **permalink**), `reach`, `total_interactions`, `likes`,
`comments`, `saved`, `shares`, `views` e `created_at`. **Case pelo `url` com o `Link do post` da
peça** — é o casamento confiável. Só use a data e a legenda como desempate quando o link no Notion
estiver encurtado ou diferente, e diga que casou por aproximação.

O mapeamento é direto: `reach` → **`Alcance`** · `total_interactions` → **`Engajamento`**. Use
`total_interactions` como veio, não a soma de curtidas + comentários + salvos: os dois quase batem,
mas o número do Instagram é o `total_interactions`. **`Cliques/Leads` não vem do Reportei** — o
Instagram não expõe cliques em post orgânico. Deixe vazio ou peça à pessoa.

Duas armadilhas do dado real, e as duas fariam o relatório mentir:

- Linha com o campo `error` preenchido (por exemplo *"Posted before the convertion to business
  account"*) vem com **tudo zerado**. Isso é **ausência de dado, não zero**. Não grave; liste como
  "sem métrica disponível" e diga o motivo.
- `follows` e `profile_visits` vêm `-` em reels. Campo com `-` é vazio, não zero.

Reels e IGTV têm tabelas próprias (`ig:reels_datatable`, `ig:igtv_datatable`) quando você precisar
de detalhe por formato; a `ig:media_datatable` já cobre o essencial.

**Fonte 2: a pessoa cola** — quando não há projeto no Reportei para aquela empresa, quando a peça
não é do Instagram, ou quando o dado ainda não sincronizou. Aceite em qualquer formato razoável
("carrossel GLP1 — 4.2k alcance, 310 eng, 18 cliques"); repita de volta em tabela com o que entendeu
antes de gravar. Aqui `Engajamento` = curtidas + comentários + salvamentos; se vier separado, some e
diga a soma.

Em qualquer das duas, mostre a tabela por peça **com a fonte** e pergunte "gravo?" antes de escrever.

Se uma peça não tiver número em nenhuma fonte, fica vazia e aparece na lista de pendentes — não
invente.

### 3. Grave, item confirmado

Uma peça por vez ou em bloco explícito ("grava as cinco como estão"). Antes de gravar, confira que a
página tem `Link do post` e que não mudou desde que você leu (`last_edited_time`).

### 4. Leia o período

Depois de gravar (ou se já estava tudo preenchido), a leitura, em absoluto: por **pilar** e por
**canal**, alcance e engajamento somados e medianos; **a peça-destaque** (maior engajamento) e as
que ficaram **abaixo da mediana da própria série** (a série é o que a casa publicou nos últimos 2–3
meses no mesmo canal — se não houver série, diga que ainda não há base). Uma frase do que se
repete: pilar que costuma puxar, canal onde o formato X rende, dia da semana se houver padrão com
contagem. Sem "bom"/"ruim"; sem benchmark de mercado (não veio da consulta).

Termine com **uma pergunta** para a pauta do próximo período ("o educativo rendeu 2× a mediana
em três das quatro peças — vale subir de 1 a cada 3 para 1 a cada 2?").

### 5. Registre

🤖 Log do PMO: `Tipo = Resultados de conteúdo`, `Rito = Sob demanda`, `Dado observado` = a tabela
por pilar/canal, `Sugestão` = a pergunta, `Status do fato = Hipótese`, `Decidido por` = a pessoa.
Em **modo fixture**, descreva o registro e as gravações em vez de executar.

## O que esta skill não faz

Não grava métrica de tráfego pago nem de campanha (o Reportei traz Ads, mas isso é leitura do
relatório mensal, não da peça). Não muda status, data, pilar ou dono da peça. Não compara a
performance de pessoas (a peça tem dono; a leitura é por pilar e canal). Não cria projeto nem
integração no Reportei — se faltar projeto para a empresa da peça, diga isso e siga pela colagem.
