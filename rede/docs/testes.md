# Testes

## Offline (não tocam na API)

```bash
node test/run.mjs
```

54 verificações que sobem o servidor MCP de verdade, com uma configuração temporária, e checam:

- **Registro** — as 29 tools aparecem em `tools/list`.
- **Status** — lê a configuração, identifica o ambiente e a base certa, e **não vaza** `client_secret`
  nem senha na resposta.
- **Domínios** — as tabelas resolvem (bandeira 1 = Mastercard, 14 = Elo), o `group_by` por rota está
  exposto e tabela inexistente devolve a lista de opções.
- **Janelas de data** — 62 dias barrado em vendas, 30 em débitos, data final antes da inicial,
  formato fora de `YYYY-MM-DD`, data que não existe no calendário (31 de fevereiro), e o erro
  sugerindo as fatias.
- **Regras por rota** — bandeira obrigatória em parcelas de recebíveis, `groupBy` inválido listando
  os aceitos e avisando que a caixa importa, filtro exclusivo da v2 barrado na v1, bandeira
  desconhecida explicada.
- **Resolução de PV** — dois PVs sem escolher pede qual; PV inexistente lista os disponíveis.

Rode com `VERBOSE=1` para ver o stderr do servidor.

## Integração contra a API simulada

```bash
node test/integracao.mjs
```

65 verificações que sobem o servidor MCP contra o mock de [test/mock.mjs](../test/mock.mjs),
apontado por `REDE_BASE_URL`/`REDE_TOKEN_URL`. Cobrem as 29 tools com dados coerentes e provam o
que o sandbox da Rede **não** permite provar:

- **O cruzamento da conciliação** — 2 resumos conciliados, 1 divergente em R$ 27,50, 1 venda sem
  pagamento (vendida em 28/09, crédito em D+30) e 1 pagamento cuja venda é anterior ao período.
  No sandbox isso é impossível: os `saleSummaryNumber` das vendas (`1749152…`) e os das ordens de
  crédito (`29649108…`) são conjuntos disjuntos, fixtures independentes.
- **As rotas que o sandbox não habilita** — v2 de vendas, resumos, recebíveis (v1/v2/v3),
  calendário, diário e bloqueios.
- **A renovação de token** — o mock esquece os tokens, a consulta seguinte leva 401, o servidor
  renova e a chamada passa.
- **O 204 virando "sem registro"** em vez de erro.
- **O header `Merchant-Id`** chegando só nas rotas que o exigem.
- **A tradução de códigos**, incluindo `SCHEDULLED` (parcela, dois L) e `SCHEDULED` (recebível, um L).

## Validado contra a API real (2026-09-20)

Sandbox da Rede, credencial do pacote *APIs de Conciliação*, PV `13381369`, novembro de 2022:

| Rota | Resultado |
|---|---|
| `/oauth/token` com `client_credentials` | **OK** — escopo `merchant-statement feature_merchant_statement`, `expires_in` 1440 |
| `/v1/sales` | **OK** — 30 vendas, tradução correta (Mastercard, Aprovada, Parcelado sem juros) |
| `/v1/sales/installments` | **OK** |
| `/v1/payments` | **OK apenas com filtro** do roteiro (`size` 1/5/10, `status`, `brands`, `types`); sem filtro devolve 400 *"This scenario is not available in the sandbox"* |
| `/v1/payments/credit-orders` | **OK** — 20 ordens |
| `/v1/charges`, `/v1/charges/summary`, `/v1/charges/adjustment-types` | **OK** |
| `/v1/sales/{pv}/daily` | **OK** só no PV `1254405`, de `2022-11-22` a `2022-11-28` |
| `/v2/sales`, resumos de venda | **403 "Requisição inválida"** — não habilitados |
| recebíveis (v1/v2/v3), calendário, bloqueios | **403 "Requisição inválida"** |

Descobertas que não estão no swagger nem no PDF:

1. `client_credentials` funciona e dispensa usuário/senha — a doc só descreve `password`.
2. Credencial de projeto *Payment Link* autentica, mas o escopo `payment-link` fecha todas as rotas
   de extrato com 401.
3. `403 "Requisição inválida"` significa rota não habilitada para o aplicativo, não filtro errado.
4. `400 "This scenario is not available in the sandbox"` é um formato de erro não documentado.
5. A v1 de vendas devolve o campo `ard` (referência do adquirente), ausente do swagger.

## Produção (2026-09-21)

Credenciais de produção, PVs 96504463 e 106119095:

| Verificação | Resultado |
|---|---|
| Login `client_credentials` | **OK** — escopo `feature_merchant_statement merchant-statement` |
| `/v1/charges/adjustment-types` | **OK** — 56 tipos de ajuste |
| Vendas, resumos, pagamentos, recebíveis — **antes** da liberação | `Partner not allowed` (403, ou 401 código 1001) e `Insufficient access level` |
| Solicitação de acesso por API (Total, Leitura) | **Criada** às 15:39 e **aprovada** às 16:02 pela área do lojista |
| Vendas v2, resumo v2, pagamentos v2, recebíveis v3 — **depois** | **OK** nas duas unidades |
| Resumo de vendas × lista detalhada | Batem centavo a centavo (Matriz R$ 95.750,00 / 11; Hirata R$ 20.000,00 / 3) |
| `rede_conciliar`, vendas de agosto | **Cruza de verdade**: 7 resumos conciliados na Matriz, 2 na Hirata |
| `/v2/sales` com `parentMerchantId` (como o swagger manda) | **422** `parentCompanyNumber: Missing data` — erro do swagger |
| `/v2/sales` com `parentCompanyNumber` | Passa a validação e chega na checagem de permissão |
| API de Gestão de Acessos | **Acessível** com a mesma credencial (consulta de id inexistente → 204) |

## Sequência mínima de homologação

1. `rede_conectar` — prova o OAuth e **mostra o escopo do token**.
2. `rede_tipos_de_ajuste` — rota sem parâmetro; separa problema de credencial de problema de filtro.
3. `rede_vendas` num PV do sandbox, período de novembro de 2022.
4. `rede_pagamentos` com `tamanho: 5`.
5. `rede_ordens_de_credito` e `rede_debitos_resumo`.
6. `rede_conciliar` — roda ponta a ponta, mas no sandbox não concilia (ver acima).

## Build

```bash
cd server && npm install && npm run build
```

`npm run build` roda `tsc --noEmit` antes de empacotar: erro de tipo derruba o build. O artefato é
`servers/rede-mcp.js`, um arquivo único sem dependências.
