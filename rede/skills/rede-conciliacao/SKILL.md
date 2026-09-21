---
name: rede-conciliacao
description: Concilia as vendas na maquininha da Rede com os depositos que caem na conta — descobre se uma venda ja foi paga, em qual deposito ela caiu, por que caiu menos do que o esperado, e o que ficou para tras. Use quando a pessoa pedir conciliacao financeira, fechamento de maquininha, "bate o extrato da Rede com o banco", "essa venda ja caiu?", "por que recebi menos", "quanto a Rede descontou", ou quiser cruzar vendas com pagamentos em lote.
---

# Conciliacao Rede: da venda ao deposito

Conciliar maquininha e responder: **cada venda virou quanto de dinheiro, quando, e por que nao foi
o valor cheio.**

## Por que nao e trivial

A Rede nao tem uma rota "esta venda caiu em qual deposito". A ligacao existe, mas em tres pontas:

```
venda                     ordem de credito                    pagamento
saleSummaryNumber   -->   saleSummaryNumber + paymentId  -->  paymentId
(rede_vendas)             (rede_ordens_de_credito)            (rede_pagamentos)
```

A rota de vendas traz o `saleSummaryNumber` (numero do resumo de vendas). A rota de pagamentos
**nao traz**. A unica rota de pagamento que carrega os dois campos e a de **ordens de credito** —
por isso toda conciliacao passa por ela.

Caminho alternativo, de baixo para cima: `rede_parcelas_do_pagamento` abre um deposito e lista NSU
e resumo de venda de cada parcela dentro dele. Use quando a pergunta parte do extrato bancario
("o que e esse deposito de R$ 4.320?") em vez de partir da venda.

## A armadilha das datas

Venda e datada pela **compra**; pagamento, pelo **repasse**. Debito cai em D+1, credito em D+30,
parcelado em 30/60/90.

Conciliar setembro com setembro **perde quase tudo**: as vendas de setembro no credito so aparecem
como pagamento em outubro. Por isso a janela de pagamento tem de ser mais larga e deslocada para
frente. `rede_conciliar` ja faz isso por padrao (fim das vendas + 40 dias); so mexa se souber por que.

## O fluxo

1. **Panorama.** `rede_vendas_resumo` no periodo (bruto, liquido, quantidade) e
   `rede_pagamentos_resumo` na janela deslocada. Se a pessoa so quer ordem de grandeza, pode parar aqui.
2. **Cruzamento.** `rede_conciliar` com o periodo de venda. Ele fatia as janelas sozinho
   (62 dias para vendas, 30 para ordens de credito), cruza pelo `saleSummaryNumber` e devolve
   quatro grupos.
3. **Investigar o que nao bateu** — a tabela abaixo.
4. **Fechar com o banco.** `rede_pagamentos` ou `rede_pagamentos_diario` dao o valor liquido por
   data de credito, que e o numero comparavel ao extrato bancario.

## Lendo o resultado de `rede_conciliar`

| Grupo | O que costuma ser | Como confirmar |
|---|---|---|
| `conciliado` | venda paga, valores batem (tolerancia de 2 centavos de arredondamento) | nada a fazer |
| `parcelado_em_andamento` | **normal**: venda parcelada com parte das parcelas paga; as outras vencem uma por mes, depois da janela. O pago e multiplo exato da parcela | `parcelas_pagas` de `parcelas` e `falta_receber` ja vem calculados. Nao trate como problema |
| `sem_pagamento` | venda recente que ainda nao venceu, ou parcela bloqueada/suspensa | `rede_parcelas_da_venda` (data + NSU) mostra vencimento e status de cada parcela |
| `pago_sem_venda` | a venda e anterior ao periodo consultado | estique `venda_inicio` para tras e rode de novo |
| `ajuste_no_repasse` | diferenca **ja explicada** por um debito do deposito. `ajustes` diz qual (aluguel, estorno...). Se for estorno, `provavel_origem` aponta a venda estornada — que costuma ser de **outra data e outro resumo** | conte a historia. O **valor** do debito e fato; a **venda de origem** e deducao — ver abaixo |
| `valor_divergente` | o que sobrou **sem explicacao** nos debitos do deposito — esse sim merece olhar humano | `ajustes_no_pagamento` (se vier) mostra debitos que existem mas nao fecham a conta; confira `statusType` da venda e chargeback |

`detalhar: true` devolve a lista completa de resumos de venda em vez da amostra.

**Atencao aos totais:** `valor_liquido_pago` inclui parcelas de vendas **anteriores** ao periodo
(o grupo `pago_sem_venda`). Numa clinica com muito parcelado ele passa facilmente do valor vendido —
no primeiro teste real, agosto teve R$ 121 mil vendidos e R$ 265 mil pagos na janela. Nao compare
os dois totais diretamente; compare grupo a grupo.

### Como `rede_conciliar` explica sozinha

Para cada resumo divergente, ela consulta os debitos do deposito. Se o total (ou um debito so)
fecha a diferenca com tolerancia de 5 centavos, o resumo vira `ajuste_no_repasse`. Quando o ajuste e
estorno (codigo 18, "cancelamento de vendas"), ela procura nos 6 meses anteriores a venda com evento
`CANCELLED`/`PARTIAL_CANCELLED` na semana do deposito. Um candidato vira `provavel_origem`; varios
viram `candidatos_de_origem`. Parcelado de mais de 6x pode escapar dessa busca.

Caso real que originou o recurso: deposito R$ 526,32 menor numa venda a vista intacta de R$ 7.350.
Era o estorno de 90% de uma venda 10x de outra data, cuja 1a parcela ja tinha sido paga cheia.

**Como dizer a origem:** o debito da Rede **nao traz** o NSU da venda estornada; a ligacao e feita
por data de evento. Entao diga "o desconto e de um estorno; a venda que bate e a de 20/06 (NSU
111008), estornada em 13/08, dois dias antes do deposito — foi a unica encontrada no periodo".
Apresentar a origem como certeza e errado, mesmo quando ha um candidato so: pode haver estorno de
venda mais antiga que 6 meses, fora da busca.

## "Por que caiu menos do que eu esperava?"

Na ordem:

1. `rede_pagamento_esperado` x `rede_pagamento` — a diferenca entre previsto e pago.
2. `rede_debitos_do_pagamento` — o que foi descontado daquele deposito, por tipo de ajuste.
   Os nomes dos tipos saem de `rede_tipos_de_ajuste`.
3. `rede_bloqueios_do_pagamento` — se parte do valor foi suspensa, penhorada (gravame) ou retida,
   e se ja houve liberacao (`RELEASE`).
4. `rede_debitos_resumo` no mes — a visao geral do que a Rede cobrou e por que.

A conta que explica o dinheiro:

```
valor bruto da venda
  - MDR (mdrAmount)
  - taxa flex, quando houver (flexAmount)
  = valor liquido da venda
  - ajustes a debito do periodo (aluguel, cancelamentos, chargebacks)
  = deposito na conta
```

## Cuidados ao responder

- Diga sempre **qual janela de venda e qual de pagamento** voce usou. Sem isso o numero nao e
  auditavel.
- Nunca apresente "vendi X" e "recebi X" como se fossem a mesma coisa no mesmo mes.
- Se a paginacao parou no teto (`completo: false`), o total e **parcial** — diga isso antes do numero.
- Conciliacao de varios meses faz dezenas de chamadas e demora. Avise antes de disparar.
- Valor divergente de centavos costuma ser arredondamento de MDR por parcela, nao erro da Rede.
