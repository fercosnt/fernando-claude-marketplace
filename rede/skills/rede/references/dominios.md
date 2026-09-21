# Tabelas de codigo da Rede

Tudo isto tambem esta disponivel em `rede_dominios`, que e consulta local e nao gasta chamada.
As respostas das tools ja chegam com os campos traduzidos ao lado do codigo original.

## Bandeiras (`brandCode`)

| Codigo | Bandeira | | Codigo | Bandeira | | Codigo | Bandeira |
|---|---|---|---|---|---|---|---|
| 1 | Mastercard | | 21 | VR | | 41 | Ok Cartoes |
| 2 | Visa | | 22 | Greencard | | 42 | Onecard |
| 3 | Diners | | 23 | Nutricash | | 43 | Sindplus |
| 4 | Cabal | | 24 | Planvale | | 44 | UauhBeneficios |
| 5 | Sicredi | | 25 | Verocheque | | 45 | Vale Shop |
| 6 | Sorocred | | 26 | Coopercard | | 46 | Vegas Card |
| 7 | Hipercard | | 27 | Abrapetite | | 47 | Visasoft Pay |
| 8 | CUP | | 28 | Bamex Beneficios | | 48 | Volus |
| 9 | Calcard | | 29 | Biq Beneficios | | 49 | Vscard |
| 10 | Construcard | | 30 | Bonuscred | | 50 | Up Brasil |
| 11 | Avista | | 31 | Convenios Card | | 51 | Verocard |
| 12 | Credsystem | | 32 | Credialimentacao | | 52 | Ticket |
| 13 | Amex | | 33 | Eucard | | 53 | VAN |
| 14 | Elo | | 34 | Facecard | | 54 | PL Itau FAI |
| 15 | Hiper | | 35 | Flex | | 55 | PL Bradesco |
| 16 | Alelo | | 36 | Goodcard | | 56 | PL Banco do Brasil |
| 20 | Sodexo | | 37 | Lecard | | 57 | PL Citibank |
| | | | 38 | Libercard | | 58 | PL Credsystem |
| | | | 39 | Maxxcard | | 59 | PL Porto Seguro |
| | | | 40 | Nutricard | | 60 | Pagamento de Fatura |
| 72 | Nova Bandeira | | 74 | Banescard | | 76 | JCB |
| 77 | Credz | | 999 | Outros | | | |

**Divergencia da doc:** a Rede escreve "Dinners" (3) em algumas tabelas e "Mais!" (12) em outras.
As tools aceitam as duas grafias na entrada.

## Modalidade (`modalityCode`)

| Codigo | Valor | Descricao |
|---|---|---|
| 1 | CREDIT | Credito |
| 2 | DEBIT | Debito |
| 3 | VAN | Voucher |

## Produto (`modalityProductCode`)

| Codigo | Valor | Descricao |
|---|---|---|
| 0 | NO_INSTALLMENTS_DEBIT | Debito a vista |
| 1 | NO_INSTALLMENTS | Credito a vista |
| 2 | IN_INSTALLMENTS_WITH_INTEREST | Parcelado com juros |
| 3 | IN_INSTALLMENTS_NO_INTEREST | Parcelado sem juros |
| 4 | CREDIT_PLAN | Crediario |
| 5 | PRE_DATED | Pre-datado |
| 6 | FUEL | Combustivel |
| 7 | FOOD | Alimentacao |
| 8 | AWARD | Premiacao |
| 9 | PRIVATE_LABEL | Private label |
| 10 | COVENANT | Convenio |
| 11 | MEAL | Refeicao |
| 12 | PREMIUM | Premium |
| 13 | MULT_BENEFITS | Multi beneficio |
| 14 | DRUGSTORE | Farmacia |
| 15 | FLEET | Gestao de frota |
| 16 | CULTURE | Cultura |
| 17 | AUTOMOBILE | Auto |
| 18 | GIFT | Gift |
| 19 | VOUCHER | Voucher |
| 99 | OTHERS | Outros |

Alem desses, os **resumos** usam agregados que nao sao produto de verdade: `TOTALS`,
`TOTAL_RECEIVABLES`, `TOTAL_ADJUSTMENTS_AND_CHARGES`, `TOTAL_HATES` (taxas MDR + Flex),
`IN_INSTALLMENTS_2_6`, `IN_INSTALLMENTS_7_12`, `IN_INSTALLMENTS_13_21` e os `RATES_*`.
Nao os some junto com os produtos: dariam contagem dupla.

## Status da venda

`APPROVED` (aprovada) e `CANCELLED` (cancelada).

`statusType` detalha (so na v2):

| Valor | Descricao |
|---|---|
| COMPLETE | Aprovada total |
| PARTIAL | Aprovada com cancelamento parcial |
| CHARGEBACK | Cancelamento total por chargeback |
| CANCELLATION | Cancelamento total |
| REVERSED | Estorno realizado |
| DENIED | Negada |
| UNDONE | Desfeita |
| IN_DISPUTE | Aprovada em disputa |
| IN_DISPUTE_PARTIAL | Parcialmente aprovada em disputa |
| PENDING_PAYMENT | Pagamento pendente |
| PAYMENT_REFUND | Pagamento reembolsado |

## Status do pagamento (`statusCode`)

| Codigo | Valor | Descricao |
|---|---|---|
| 1 | PENDING | Pagamento pendente |
| 2 | PAID | Pago |
| 3 | REJECTED | Rejeitado |
| 4 | EXPECTED | Esperado |
| 5 | RECEIVED | Recebido |
| 6 | FORETHOUGHT | Previsto |
| 7 | CANCELLED | Cancelado |
| 8 | SUSPENDED | Suspenso |
| 9 | PAWNED | Penhorado (gravame) |
| 10 | BLOCKED | Bloqueado |
| 11 | PAWNED_BLOCKED | Penhorado e bloqueado |
| 12 | RETAINED | Retido |
| 14 | CHARGED | Cobrado |

`/v1/payments` so aceita filtrar por PENDING, PAID e REJECTED. A lista completa vale para
`/v2/payments/daily`.

Tipo de pagamento: `CRE`/`CREDIT`, `DEB`/`DEBIT`, `ANT`/`ANTICIPATION`. Algumas rotas querem a
sigla de tres letras, outras o nome por extenso — as tools mandam a forma certa.

## Status de parcela e de recebivel

Parcela de **venda**: `SCHEDULLED` (dois L, agendada), `PAID`, `ANTICIPATED`, `UNBOOK`, `BLOCKED`.

**Recebivel** (v3): `SCHEDULED` (um L, agendado), `IN_TRANSIT` (enviado a CIP para pagamento).

## Bloqueio

| Codigo | Valor |
|---|---|
| 8 | SUSPENDED |
| 9 | PAWNED |
| 12 | RETAINED |

Evento: `BLOCK` (bloqueio) ou `RELEASE` (liberacao).

## Chargeback

| Valor | Descricao |
|---|---|
| CHARGEBACK_IN_DISPUTE | Em disputa |
| CHARGEBACK_SOLVED_DEBIT | Debito solucionado (impacta o cliente) |
| CHARGEBACK_SOLVED_CREDIT | Credito solucionado (impacta o cliente) |
| CHARGEBACK_SOLVED_NO_IMPACT | Solucionado (nao impacta o cliente) |

## Cobranca e negociacao

Tipo de cobranca: `NET` (desconta do repasse) e `NET_EXTERNO` (debita da conta bancaria).

Tipo de negociacao de recebiveis: `ENCUMBRANCE` (onus gravame), `ENCUMBRANCE_FIDUCIARY`
(cessao fiduciaria), `ENCUMBRANCE_PAWN` (penhor), `ALLOWANCE` (troca de titularidade),
`FREE`/`FREE_AMOUNT` (pagamento livre).

## Tipos de ajuste de debito

Nao tem lista fixa: mudam com o tempo e saem de `rede_tipos_de_ajuste`. Exemplos que aparecem
na doc: 1 Pacote eRede, 2 Consulta Decheques, 5 Tx Man Dotef, 18 cancelamento de vendas.

## `groupBy` aceito por rota (a caixa importa)

| Rota | Valores |
|---|---|
| Resumo de vendas v1 | `DAY`, `WEEK`, `MONTH` |
| Resumo de recebiveis v2 | `DAY`, `WEEK`, `MONTH` |
| Resumo de pagamentos v2 | `day`, `week`, `month`, `brand`, `status`, `type`, `bank`, `agency`, `accountNumber` |
| Resumo de recebiveis v3 | `day`, `week`, `month`, `brand`, `modality`, `terminal` |
| Bloqueios | `day` |
