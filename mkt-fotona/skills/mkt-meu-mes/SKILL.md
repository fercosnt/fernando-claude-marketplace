---
name: mkt-meu-mes
description: Gera o relatório individual do mês da própria pessoa no sistema de MKT da Fotona (Notion) — o que entregou, o que está com ela, aging dos itens dela, quanto veio de demanda extra, o que travou esperando outra pessoa — em absoluto, contra a série dela mesma, sem comparar com ninguém; entrega em markdown, PDF ou HTML e registra no Log do PMO. Use sempre que alguém pedir "meu mês", "como foi meu mês", "o que eu entreguei", "meu relatório", "meus números", "resumo do que fiz em setembro", "quero levar pro meu 1:1", ou qualquer pedido da pessoa sobre o próprio trabalho no período. Recuse o mês de outra pessoa ("mostra o mês da fulana", "compara comigo"): isso é o PMO da coordenação, não este plugin.
---

# Meu mês

O sistema mede por fase e por dono, mas ninguém do time tinha uma leitura do próprio mês — a
coordenação via, a pessoa não. Esta skill devolve isso a quem trabalhou. É o mesmo relatório do
escopo Pessoa do `pmo-relatorio-mensal`, com uma diferença de entrada: **só a própria pessoa, sobre
ela mesma.**

Leia `../../CONTEXTO.md` e carregue o contexto. O template é `assets/template-meu-mes.md`; o formato
da resposta segue `formato-de-saida.md` (dado bruto → leitura → uma pergunta); pontos, aging e
sinal de prazo vêm de `formulas-espelho.md` — a API não devolve fórmula, recalcule.

## A regra que não se negocia

**`Responsável` = quem está pedindo, e só.** Pergunte o nome no início ("é o seu mês, certo? me
confirma seu nome como está no Notion") e confira no banco 👥 Time. Se o pedido for o mês de outra
pessoa, ou "compara com o fulano", ou "quem entregou mais" — recuse em duas linhas: este relatório
existe para o 1:1 da pessoa, não para comparação; leitura do time é do PMO, com a coordenação. Não
mostre nem um número de outra pessoa, mesmo que a consulta os tenha trazido (a fixture, por
exemplo, pode trazer colegas — ignore).

O motivo não é sigilo: é que número individual ao lado de outro vira ranking, ranking vira gaming, e
o sistema perde o que tem de melhor, que é medir fluxo e não pessoa. Creators (PJ) não têm
relatório — não são medidos pelo sistema.

## O fluxo

### 1. Leia o mês da pessoa — e os dois anteriores

Consultas **Q11** (concluídas no período), **Q2** (abertas), **Q8** (em produção), **Q5** (em
aprovação com a pessoa como aprovadora), filtradas por `Responsável` = a pessoa. Exclua
contêineres (`Subtarefas` não vazio). Repita para os dois meses anteriores — a leitura é contra a
**própria série**, então sem série não há leitura, só contagem.

Recalcule: entregues (contagem e pontos, P=1 · M=3 · G=8), no prazo desejado, abertos/atrasados/em
produção no fim do mês, aging máximo (`Idade em produção`), reativo × planejado (`Tipo de trabalho`),
aprovações paradas com ela. **Some antes de escrever**: se abertos por status não fecham com o total,
escreva a discrepância como dado.

`Motivo do bloqueio`: só existe/não existe. Nunca o texto — é o campo mais sensível do sistema.

### 2. Escreva no template

`assets/template-meu-mes.md`: **O que li** (números, com os dois meses anteriores entre parênteses) →
**Leitura** (um parágrafo, descritivo: o que mudou em relação aos meses anteriores desta pessoa, onde
o fluxo travou, o que ficou esperando outro) → **O que travou fora do seu alcance** (item, esperando o
quê, desde quando) → **Uma pergunta para o 1:1**.

Sem adjetivo ("produtiva", "lenta"), sem "bom"/"ruim", sem %, sem colega. "Setembro teve 14
entregas contra 9 em agosto, metade vinda de demanda extra" é leitura; "mês forte" é opinião. O
relatório descreve carga e fluxo; quem julga é a conversa do 1:1.

Cabe em uma página.

### 3. Entregue e registre

Formatos: markdown na conversa (sempre) · **PDF** (padrão, quando a pessoa quiser levar) · HTML.
Para PDF/HTML, use a skill `pdf` ou gere HTML simples a partir do markdown — sem gráfico de
comparação, no máximo a série da própria pessoa (3 meses).

Grave no 🤖 Log do PMO: `Tipo = Relatório individual`, `Rito = Mensal`, `Dado observado` = o bloco
"O que li", `Sugestão` = a pergunta do 1:1, `Confiança`, `Status do fato = Hipótese`, `Decidido por`
= a pessoa. Em **modo fixture**, descreva o registro em vez de gravar.

## O que esta skill não faz

Não mostra o mês de ninguém além de quem pede. Não compara, não ranqueia, não calcula % de
utilização nem "capacidade". Não muda nada no Notion além do registro no Log. Se a pessoa quiser
discutir carga com a coordenação, o relatório é o material para o 1:1 — a skill não o envia a
ninguém.
