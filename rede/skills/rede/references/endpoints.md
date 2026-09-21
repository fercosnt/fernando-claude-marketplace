# Mapa tool → rota da Rede

Base da API: `https://rl7-sandbox-api.useredecloud.com.br` (sandbox) ou
`https://api.userede.com.br/redelabs` (producao). Todas as rotas sao `GET`.

Coluna "PV onde": onde o numero do Ponto de Venda e colocado pela tool.

## Gestao de Vendas — valor bruto

| Tool | Rota | PV onde | Janela | Notas |
|---|---|---|---|---|
| `rede_vendas` | `/merchant-statement/v2/sales` (padrao) ou `/v1/sales` | query `parentCompanyNumber` + `subsidiaries` (a v2 leva tambem `parentMerchantId`) | 62 dias | `statusType` e `modalityProducts` so existem na v2. **O swagger diz que a v2 usa `parentMerchantId`, mas producao exige `parentCompanyNumber`** |
| `rede_vendas_resumo` | `/v2/sales/{merchantId}/summary` ou `/v1/sales/{companyNumber}/summary` | path | 62 dias | v1 e a unica que aceita `groupBy` (MAIUSCULO) e `terminals` |
| `rede_vendas_por_nsu` | `/v1/sales/{companyNumber}/daily` | path | 62 dias | filtros `nsu`, `device`, `tid`. No sandbox a doc aponta outra base — ver `base_nsu` |
| `rede_parcelas_da_venda` | `/v2/payments/installments/{merchantId}` | path | — | exige `saleDate` **e** `nsu` |
| `rede_vendas_parceladas` | `/v1/sales/installments` | query `parentCompanyNumber` + `subsidiaries` | **30 dias** | janela pela data da venda |
| `rede_parcelas_do_pagamento` | `/v2/payments/installments/{parentCompanyNumber}/{paymentId}` | path | — | abre o pacote de um deposito |
| `rede_parcelas_gravame` | `/v3/payments/installments/central-merchant-id/{id}/payment-id-hash/{hash}` | path | — | campos de negociacao de recebiveis |

## Gestao de Pagamentos — valor liquido

| Tool | Rota | PV onde | Janela | Notas |
|---|---|---|---|---|
| `rede_pagamentos` | `/v1/payments` | query + `subsidiaries` | **30 dias** | `status` aqui so aceita PENDING, PAID, REJECTED |
| `rede_pagamentos_diario` | `/v2/payments/daily` | query `parentCompanyNumber` | sem limite | `types` abreviado: CRE, DEB, ANT |
| `rede_pagamentos_resumo` | `/v2/payments/summary` | **header `Merchant-Id`** | sem limite | `groupBy` minusculo, 9 opcoes; resposta muda por agrupamento |
| `rede_pagamento` | `/v1/payments/{parentCompanyNumber}/{paymentId}` | path | — | |
| `rede_pagamento_esperado` | `/v1/payments/expected/{parentCompanyNumber}/{paymentId}` | path | — | compare com o pago |
| `rede_ordens_de_credito` | `/v1/payments/credit-orders` | query + `subsidiaries` | **30 dias** | **unica rota de pagamento com `saleSummaryNumber`** |
| `rede_debitos_do_pagamento` | `/v1/payments/charges/{paymentId}` | **header `Merchant-Id`** | — | explica desconto no deposito |
| `rede_cashbacks_do_pagamento` | `/v1/payments/cashbacks/{paymentId}` | **header `Merchant-Id`** | — | |
| `rede_bloqueios_resumo` | `/v1/blocks/summary` | query `parentCompanyNumber` | sem limite | `groupBy` so aceita `day` |
| `rede_bloqueios_do_pagamento` | `/v1/blocks/{parentCompanyNumber}/{paymentId}` | path | — | traz bloqueios e liberacoes |

## Gestao de Recebiveis — o que ainda vai cair

| Tool | Rota | PV onde | Janela | Notas |
|---|---|---|---|---|
| `rede_recebiveis_resumo` (v3, padrao) | `/v3/receivables/summary` | **header `Merchant-Id`** | sem limite | `groupBy` minusculo; `status` SCHEDULED/IN_TRANSIT |
| `rede_recebiveis_resumo` (v2) | `/v2/receivables/summary` | query `parentCompanyNumber` | sem limite | `groupBy` MAIUSCULO |
| `rede_recebiveis_resumo` (v1) | `/v1/receivables/summary` | query + `subsidiaries` | **30 dias** | so `types` DAY/MONTH |
| `rede_recebiveis_calendario` | `/v1/receivables/calendar` | query `parentCompanyNumber` | **60 dias** | blocos `daily` e `mouthly` (sic) |
| `rede_recebiveis_diario` | `/v1/receivables/daily` | **header `Merchant-Id`** | sem limite | detalhe por entrada |
| `rede_recebiveis_parcelas` | `/v1/receivables/installments` | **header `Merchant-Id`** | sem limite | **`brands` obrigatorio** |

## Gestao de Debitos

| Tool | Rota | PV onde | Janela |
|---|---|---|---|
| `rede_debitos` | `/v1/charges` | query + `subsidiaries` | **30 dias** |
| `rede_debitos_resumo` | `/v1/charges/summary` | query + `subsidiaries` | **30 dias** |
| `rede_tipos_de_ajuste` | `/v1/charges/adjustment-types` | — | — |

## Utilitarios (nao chamam a Rede, exceto `rede_get`)

| Tool | O que faz |
|---|---|
| `rede_status` | Config, ambiente, PVs e validade do token |
| `rede_conectar` | Faz o login e confirma com uma consulta real |
| `rede_conciliar` | Cruza vendas x ordens de credito pelo `saleSummaryNumber` |
| `rede_dominios` | Tabelas de codigo, consulta local |
| `rede_get` | GET livre em qualquer rota |

## Paginacao

Rotas de lista devolvem `cursor.hasNextKey` e `cursor.nextKey`. Passe `nextKey` como `page_key`
na proxima chamada, ou use `paginar_tudo: true` e deixe a tool seguir o cursor (teto de 20 paginas,
`size` maximo 100 por pagina). Se parar no teto, a resposta traz `completo: false` e o
`proximo_page_key` para continuar.

## Autenticacao

`POST /oauth/token` com `Authorization: Basic base64(client_id:client_secret)` e corpo
`application/x-www-form-urlencoded`:

- primeiro login: `grant_type=password&username=<usuario>&password=<senha>`
- renovacao: `grant_type=refresh_token&refresh_token=<token>`

O `access_token` dura cerca de 40 minutos (a doc manda renovar a cada 24) e o `refresh_token`,
24 horas. Passadas as 24h o plugin refaz o login com usuario e senha sozinho.
