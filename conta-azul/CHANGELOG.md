# Changelog

## 0.1.1 — 2026-09-20

Correções feitas a partir do primeiro teste com a conta real da Beauty Smile.

- **Caixa pelas baixas.** O campo `pago` da busca é o total já pago da parcela. Em parcela paga em partes ao longo
  de meses, somar esse campo inflava o mês: na conta real, R$ 244 mil apareciam como "pagos em setembro". Agora
  `contaazul_resumo_financeiro` (`caixa_no_periodo`) e `contaazul_contas_receber`/`_pagar` com filtro de pagamento
  (`pago_no_periodo_de_pagamento`) somam só as baixas com data dentro do período.
- **Atraso pela data.** O status ATRASADO da busca da API demora a atualizar: a parcela vencida continua
  EM_ABERTO na busca, embora o detalhe já mostre ATRASADO. O atraso agora é calculado pela data (`vencido_nao_pago`,
  `vencida`, `dias_atraso`), e há um parâmetro novo, `somente_vencidas`. O status da API continua visível em
  `por_status_da_api`.
- **Categoria pelo rateio.** A busca informa quais categorias uma parcela tem, mas não quanto vai para cada uma.
  O valor por categoria agora sai do rateio do lançamento, e descontos incondicionais (valor zero) não inflam mais o ranking.
- **Resumo em dois critérios.** `por_vencimento` (com `saldo_previsto`) e `caixa_no_periodo`. O campo
  `resultado_realizado`, que confundia, foi removido.
- A data de "hoje" passa a seguir o fuso de São Paulo.
- Skill `conta-azul` atualizada com as três regras. Testes: 45 no servidor e 3 iterações de evals (ver `evals/`).

## 0.1.0 — 2026-09-20

- Primeira versão: 38 tools, OAuth local com refresh token rotativo protegido por trava, escrita desligada por
  padrão com prévia antes de enviar, e as skills `conta-azul`, `conta-azul-setup` e `conta-azul-escrita`.
