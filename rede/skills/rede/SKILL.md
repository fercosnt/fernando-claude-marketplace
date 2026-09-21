---
name: rede
description: Use quando a pergunta precisar de dados reais da Rede (adquirente de cartao, a maquininha) — vendas no credito e no debito, quanto foi vendido no periodo, ticket medio, taxa MDR cobrada, quando cai o dinheiro, quanto ja caiu, recebiveis futuros, parcelas de uma venda, um deposito especifico, bloqueios, chargebacks, debitos e ajustes descontados, cashbacks, ou conciliar venda com pagamento. Frases como "quanto vendi na maquininha em setembro", "quando cai a venda de ontem", "por que caiu menos do que eu esperava", "o que a Rede me cobrou esse mes", "essa venda ja foi paga". Aplica-se quando as tools rede_* estao disponiveis.
---

# Rede — Gestao de Vendas

As tools `rede_*` falam com as APIs de Gestao de Vendas da Rede. **Tudo e leitura**: a API nao
altera nada do estabelecimento. Esta skill e o julgamento — qual tool responde cada pergunta e
como ler o numero sem errar.

## Antes de tudo

- Erro de conexao ou duvida de setup → `rede_status`. Nao configurado → skill `rede-setup`.
- Datas sempre `YYYY-MM-DD`. "Setembro" = `2026-09-01` a `2026-09-30`. Converta antes de chamar.
- **Cada rota tem um limite de janela** (62, 60 ou 30 dias). As tools barram antes de chamar e o
  erro ja diz como fatiar. Nao tente contornar: a Rede devolve 422.
- Os codigos ja vem traduzidos na resposta (`brandCode: 14` vem com `bandeira: "Elo"`). A tabela
  completa esta em `rede_dominios`, que e consulta local e nao gasta chamada.
- Um PV (Ponto de Venda) e um estabelecimento. Se houver mais de um configurado, sempre diga qual
  voce consultou ao responder.

## Os tres conceitos que nao podem ser confundidos

Errar isso e a causa de praticamente toda resposta errada sobre maquininha.

| Conceito | O que e | Data que manda | Tool |
|---|---|---|---|
| **Venda** | Valor **bruto** da compra, sem desconto de MDR | data da venda | `rede_vendas` |
| **Recebivel** | O que **ainda vai** cair, ja liquido | data prevista de credito | `rede_recebiveis_resumo` |
| **Pagamento** | O deposito que **efetivamente** caiu, liquido de MDR e debitos | data do repasse | `rede_pagamentos` |

Quando o dinheiro cai:

- **Debito** → D+1 (proximo dia util apos a venda).
- **Credito a vista** → D+30.
- **Credito parcelado** → 30, 60, 90 dias... uma parcela por mes, inclusive no parcelado com juros
  (quem financia e o emissor; o lojista recebe como se fosse a vista em 30 dias).

**Consequencia pratica:** venda e pagamento quase nunca estao no mesmo periodo. "Vendi R$ 10 mil em
setembro" e "recebi R$ 10 mil em setembro" sao perguntas diferentes e respostas diferentes. Se a
pessoa nao deixou claro qual quer, pergunte ou responda as duas dizendo qual e qual.

Um pagamento e um **pacote**: agrupa parcelas de varias vendas diferentes. Nao existe "o pagamento
desta venda" — existe "o pagamento que contem a parcela desta venda".

## Qual tool responde o que

| Pergunta | Tool | Cuidado |
|---|---|---|
| "Quanto vendi no periodo?" (total) | `rede_vendas_resumo` | Leia **`total_do_periodo`**. A lista `resposta.content.sales` vem **um item por dia com venda** — o primeiro item e so o dia mais recente, nao o total. Use antes de listar transacao a transacao. |
| "Quanto vendi por dia/semana/mes?" | `rede_vendas_resumo` com `agrupar_por` | `DAY`, `WEEK`, `MONTH` — **maiusculo** nesta rota. Cai na v1 automaticamente. |
| "Lista das vendas" / auditar transacoes | `rede_vendas` | Janela de 62 dias. Use `paginar_tudo` para juntar as paginas. |
| "Essa venda especifica" (tenho o NSU) | `rede_vendas_por_nsu` | Filtra tambem por terminal e TID de e-commerce. |
| "Quando cai essa venda?" / "ja foi paga?" | `rede_parcelas_da_venda` | Exige data da venda **e** NSU. Devolve vencimento, status e o `paymentId` de cada parcela. |
| "Quanto tenho a receber?" | `rede_recebiveis_resumo` | v3 por padrao, sem limite de janela. `agrupar_por` aqui e **minusculo**. |
| "Calendario de entrada de caixa" | `rede_recebiveis_calendario` | Blocos diario e mensal juntos. Janela de 60 dias. |
| "Quanto caiu na conta?" | `rede_pagamentos` | Janela de 30 dias, pela data do **pagamento**. |
| "Resumo dos depositos" (por dia, banco, bandeira...) | `rede_pagamentos_resumo` | 9 agrupamentos, **minusculo**. O corpo da resposta muda conforme o agrupamento. |
| "Detalhe do dia, com pendentes e suspensos" | `rede_pagamentos_diario` | A visao mais rica de pagamento. Sem limite de janela. |
| "O que tem dentro deste deposito?" | `rede_parcelas_do_pagamento` | Abre o pacote: NSU, resumo de venda e valores de cada parcela. |
| "Por que caiu menos do que eu esperava?" | `rede_debitos_do_pagamento` + `rede_pagamento_esperado` | Compare esperado x pago e veja os ajustes descontados. |
| "O que a Rede me cobrou este mes?" | `rede_debitos_resumo` | Somado por tipo de ajuste. Janela de 30 dias. Os nomes dos tipos saem de `rede_tipos_de_ajuste`. |
| "Meu dinheiro esta preso/bloqueado" | `rede_bloqueios_resumo`, `rede_bloqueios_do_pagamento` | Tipos: SUSPENDED, PAWNED (gravame), RETAINED. O evento diz se foi BLOCK ou RELEASE. |
| "Essa venda caiu em qual deposito?" (em lote) | `rede_conciliar` | Ver a skill `rede-conciliacao`. |
| Recebiveis dados em garantia / gravame | `rede_parcelas_gravame`, `rede_recebiveis_diario` | Campos de cessao, cessionario e ordem de credito. |
| Rota sem tool dedicada | `rede_get` | Ultimo recurso — nao valida janela nem posiciona o PV. |

## Armadilhas reais desta API

1. **O PV viaja em tres lugares diferentes.** Query (`parentCompanyNumber`/`parentMerchantId`),
   path (`{merchantId}`) ou header (`Merchant-Id`), conforme a rota. As tools resolvem isso; se voce
   usar `rede_get`, e por sua conta — rotas v2 `payments/summary`, v3 `receivables` e
   `charges`/`cashbacks` exigem o header.
2. **`groupBy` muda de caixa.** `DAY`/`WEEK`/`MONTH` maiusculo no resumo de vendas v1; `day`, `brand`,
   `accountNumber` minusculo em pagamentos v2, recebiveis v3 e bloqueios. As tools validam.
3. **`SCHEDULLED` x `SCHEDULED`.** Parcela de venda tem dois L; recebivel tem um. Nao e erro de
   digitacao — sao rotas diferentes.
4. **Bandeira em rota detalhada.** A doc declara uma bandeira por chamada nas rotas detalhadas e
   lista separada por virgula nos resumos. Se a API recusar varias, repita uma por vez.
5. **`rede_recebiveis_parcelas` exige bandeira.** Sem ela a Rede recusa.
6. **204 nao e erro.** Significa "consulta ok, nenhum registro". A resposta vem com `vazio: true` —
   diga "nao houve movimento no periodo", nunca "deu erro".
7. **403 e 401 quase sempre sao permissao de PV**, nao credencial errada. A liberacao por
   estabelecimento e feita pela Rede (gestao de acessos), nao no codigo.
8. **Vendas por NSU no sandbox roda em outra base.** Se der 404, preencha `base_nsu` no
   `~/.rede-mcp.json` — a skill `rede-setup` explica.
9. **`401` em TODAS as rotas = projeto do pacote errado**, nao PV sem permissao. Um projeto de
   Payment Link no Portal da Rede autentica, mas o token sai com escopo `payment-link` e nenhuma
   rota de extrato abre. `rede_conectar` mostra o escopo e alerta.
10. **`403 "Requisicao invalida"` = rota nao habilitada** para o aplicativo. No sandbox e a resposta
    normal da v2 de vendas, dos resumos, dos recebiveis e dos bloqueios — `rede_vendas` cai
    sozinha na v1 nesse caso e avisa.
11. **O swagger erra o nome do PV na v2 de vendas.** Diz `parentMerchantId`; producao exige
    `parentCompanyNumber` e responde 422 sem ele. As tools mandam os dois. Se usar `rede_get` na v2,
    mande `parentCompanyNumber`.
12. **`Partner not allowed` = PV nao liberado**, seja 403 ("for this company number") ou 401
    ("for this merchant", codigo 1001). O login esta certo; falta a solicitacao de acesso e a
    aprovacao do lojista. Ver `docs/producao.md`.
13. **A v1 de vendas devolve campos fora do swagger**, como `ard` (numero de referencia do
    adquirente). Nao invente significado para campo que a doc nao descreve; mostre o valor como veio.

## Como responder

- Sempre diga **qual periodo e qual data** voce usou (data de venda ou data de pagamento).
- Valores em reais, com o bruto e o liquido separados quando os dois existirem.
- Se paginou e parou no teto, diga que o numero e parcial — a resposta traz `completo: false`.
- Nao some valores de rotas diferentes sem checar a data-base: somar venda de setembro com pagamento
  de setembro nao da nada que exista no mundo real.

## Referencias

- `references/endpoints.md` — mapa tool → rota da Rede, parametros e limite de janela de cada uma.
- `references/dominios.md` — tabelas de codigos (bandeiras, status, produtos, tipos de ajuste).
