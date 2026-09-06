---
name: mkt-resultados-conteudo
description: Registra os resultados das peças de conteúdo publicadas do MKT da Fotona no Notion — lista as peças com link de post e sem métrica, pede os números (alcance, engajamento, cliques/leads) do painel nativo, grava só esses três campos com a fonte citada, e lê o que performou por pilar e canal no período contra a própria série. Use sempre que alguém falar em "resultados dos posts", "métricas do conteúdo", "atualiza o alcance", "como foram os posts da quinzena", "o que performou melhor", "preenche as métricas no Notion", "insights do Instagram/LinkedIn", ou colar números de posts — mesmo sem pedir para gravar. Não use para métricas de tráfego pago ou de campanha (isso é o relatório mensal do PMO) nem para peça ainda não publicada.
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
publicado é o link, não o status. Classe 3 do `contrato-de-escrita.md`. Os valores são **os que a
pessoa colou**, com a fonte citada ("Instagram, colado pela Bia em 06/09"). Número que você não leu
de nenhuma fonte não entra: estimativa de métrica é o jeito mais rápido de o relatório mensal mentir.

**Não existe fonte automática hoje** (testado em 06/09/2026): o conector do GHL não devolve métrica
por post — a única operação de analytics dele é agregada por conta e por período, e as contas nem
sincronizam os posts publicados fora do Social Planner. Se alguém pedir "puxa do GHL", diga isso em
uma linha em vez de tentar. A via automática depende da Meta Graph direto e ainda não existe.

Peça sem `Link do post` → não grava; diga que a peça consta como não publicada e que o link é o que
a marca como publicada. Não mexe em nenhum outro campo.

## O fluxo

### 1. Ache o que falta

Consulta **Q12** (publicadas no período — padrão: os últimos 15 dias; a pessoa pode pedir o mês) e
filtre: métrica vazia, ou métrica com mais de 14 dias desde `Publicado em` (a janela de 7–14 dias é
quando o número estabiliza). Liste por data: peça · canal · pilar · link · o que falta.

### 2. Pegue os números

**A pessoa cola** — é a única fonte hoje. Aceite em qualquer formato razoável ("carrossel GLP1 —
4.2k alcance, 310 eng, 18 cliques"); repita de volta em tabela com o que entendeu antes de gravar.
`Engajamento` = curtidas + comentários + salvamentos; se a pessoa colar separado, some e diga a soma.
Peça os números do painel nativo (Instagram → Insights do post; LinkedIn → analytics do post), e
registre de onde vieram.

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

Não grava métrica de tráfego pago nem de campanha. Não muda status, data, pilar ou dono da peça.
Não compara a performance de pessoas (a peça tem dono; a leitura é por pilar e canal). Não puxa da
Meta direto — isso é a v3, quando o coletor existir.
