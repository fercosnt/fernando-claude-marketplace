---
name: conta-azul
description: Use quando a pergunta precisar de dados reais do ERP Conta Azul — contas a receber ou a pagar, o que vence, o que esta atrasado, quanto entrou ou saiu, saldo das contas, fluxo de caixa, resultado do mes, DRE, categorias, centros de custo, vendas, orcamentos, contratos, clientes/fornecedores, notas fiscais (NF-e, NFS-e) — ou para lancar, quitar ou alterar algo no financeiro. Frases como "quanto a Beauty Smile tem a receber", "o que vence essa semana", "fechamento de setembro", "lanca essa despesa", "da baixa nessa parcela". Aplica-se quando as tools contaazul_* estao disponiveis.
---

# Conta Azul

As tools `contaazul_*` falam com a API v2 da Conta Azul. Esta skill e o julgamento: qual tool
responde cada pergunta e como ler o numero sem errar.

## Antes de tudo

- Qualquer erro de conexao ou duvida de setup → `contaazul_status`. Nao configurado → skill `conta-azul-setup`.
- Datas sempre `YYYY-MM-DD`. "Setembro" = `2026-09-01` a `2026-09-30`. Converta antes de chamar.
- Nunca invente UUID. Pessoa, conta financeira, categoria e centro de custo saem das tools de listagem.

## Qual tool responde o que

| Pergunta | Tool | Cuidado |
|---|---|---|
| "Como esta o financeiro do mes?" / fechamento | `contaazul_resumo_financeiro` | Traz dois blocos: `por_vencimento` (o que vence no mes) e `caixa_no_periodo` (o que entrou e saiu de fato). Diga qual numero e qual. |
| "Quanto entrou/saiu de fato no mes?" (caixa) | `contaazul_resumo_financeiro` → `caixa_no_periodo`, ou `contaazul_contas_receber` / `_pagar` com `pagamento_de/ate` **e** um vencimento amplo | Leia `pago_no_periodo_de_pagamento`, **nunca** `totais.pago`: `pago` e o acumulado da parcela, e parcela paga em partes ao longo de meses inflaria o mes. O vencimento e obrigatorio na API: use janela larga. |
| "O que esta atrasado / vencido?" | `contaazul_contas_receber` / `_pagar` com `somente_vencidas=true` | **Nao filtre so por `status=ATRASADO`**: na API real esse status atrasa, e parcela vencida ha dias continua `EM_ABERTO` na busca. O servidor calcula pela data (`vencida`, `dias_atraso`, `vencido_nao_pago`). |
| "O que vence essa semana?" | `contaazul_contas_pagar` ou `_receber` com o intervalo da semana | Diga o intervalo de datas que considerou. |
| "Quanto faturamos / gastamos por categoria?" | `contaazul_resumo_financeiro` → `por_categoria` | Ja vem pelo rateio real: pode somar. |
| Saldo em conta | `contaazul_contas_financeiras` | Saldo **atual**, nao historico. |
| Detalhe de uma parcela, rateio, quem pagou | `contaazul_parcela` (`incluir_baixas`) | |
| Vendas do periodo | `contaazul_vendas` | Os `totais` ja vem por situacao — use-os em vez de somar a pagina. |
| DRE / categorias | `contaazul_categorias_dre`, `contaazul_categorias` | |
| Notas de servico | `contaazul_notas_servico` | Janela de 15 dias e quebrada sozinha. |
| O que mudou desde X | `contaazul_alteracoes_financeiras` | Nao existe webhook. |
| Endpoint sem tool | `contaazul_get` | So GET, caminho `/v1/...` |

## Como ler os numeros

- **Competencia × vencimento × pagamento** sao datas diferentes. Sempre diga qual foi usada.
  Resultado contabil do mes = competencia; fluxo de caixa = pagamento; agenda de cobranca = vencimento.
- `total` = valor da parcela; `pago` = quanto ja entrou/saiu; `nao_pago` = saldo em aberto.
  Parcela `RECEBIDO_PARCIAL` tem as duas coisas.
- Em contas a pagar a API tambem usa o status `RECEBIDO` para quitado — traduza para "pago".
- `por_status_da_api` e informativo; para atraso use `vencido_nao_pago`, que e pela data.
- `por_categoria` distribui cada parcela pelo rateio do lancamento; descontos incondicionais tem valor zero e
  nao aparecem. Se surgir `(rateio nao consultado)`, parte do valor nao foi detalhada — diga isso.
- `pago + nao_pago` pode diferir de `total` por juros, multa, desconto ou taxa na baixa. E normal; nao "corrija".
- Se a resposta vier com `aviso` de truncado, os totais sao parciais — diga e reduza o periodo.
- Apresente em R$ com separador brasileiro, e mostre o dado bruto antes da interpretacao.

## Escrita

Tools marcadas **ESCRITA** so funcionam com a escrita ligada (skill `conta-azul-escrita`) e sempre em dois passos:

1. Chame com `confirmar=false` (padrao). Nada e enviado; volta a **previa** exata e avisos
   (duplicidade de CPF, parcela ja quitada...).
2. Mostre a previa em linguagem de gente: quem, quanto, quando, qual conta, qual categoria.
3. So com o "pode" explicito da pessoa, repita **os mesmos argumentos** com `confirmar=true`.

Regras:
- Antes de lancar, confirme os ids pela listagem (pessoa, conta, categoria). Se houver ambiguidade
  ("Itau" com duas contas), pergunte.
- Antes de dar baixa, olhe a parcela: se ja esta quitada, pare.
- Criar conta a receber/pagar e **assincrono**: volta um protocolo. Se ficar `PENDING`, consulte
  depois com `contaazul_protocolo` — **nunca recrie** o lancamento.
- Falha de rede numa escrita: a API pode ter aplicado. Confira antes de tentar de novo.
