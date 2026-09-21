# As 29 tools do plugin rede

Todas são leitura. Datas sempre `YYYY-MM-DD`. O parâmetro `pv` aceita o apelido ou o número do
Ponto de Venda e é opcional quando há só um configurado.

## Conexão

| Tool | Para quê |
|---|---|
| `rede_status` | Config, ambiente, PVs e validade do token. Não mostra segredo. |
| `rede_conectar` | Faz o login e confirma com uma consulta real. `recomecar: true` descarta o token em disco antes. |

## Vendas — valor bruto

| Tool | Parâmetros principais | Janela |
|---|---|---|
| `rede_vendas` | `data_inicio`, `data_fim`, `bandeiras`, `modalidade`, `status`, `status_tipo`*, `produto`*, `versao`, `paginar_tudo` | 62 dias |
| `rede_vendas_resumo` | `agrupar_por` (DAY/WEEK/MONTH), `bandeiras`, `modalidades`, `status`, `terminais` | 62 dias |
| `rede_vendas_por_nsu` | `nsu`, `terminal`, `tid`, filtros de venda | 62 dias |
| `rede_parcelas_da_venda` | `data_venda` + `nsu` (ambos obrigatórios) | — |
| `rede_vendas_parceladas` | período, paginação | **30 dias** |
| `rede_parcelas_do_pagamento` | `payment_id` | — |
| `rede_parcelas_gravame` | `pv_centralizador`, `payment_id_hash` | — |

\* só existem na v2.

`rede_vendas` usa a v2 por padrão. `versao: 1` existe para comparar com integrações antigas.
`rede_vendas_resumo` cai na v1 automaticamente quando você pede `agrupar_por` ou `terminais`,
porque a v2 não agrupa.

## Pagamentos — valor líquido

| Tool | Parâmetros principais | Janela |
|---|---|---|
| `rede_pagamentos` | `bandeiras`, `status` (PENDING/PAID/REJECTED), `tipo` | **30 dias** |
| `rede_pagamentos_diario` | `status` (13 valores), `tipo` (CRE/DEB/ANT), `contas_bancarias`, `payment_ids` | sem limite |
| `rede_pagamentos_resumo` | `agrupar_por` (9 opções, minúsculo), `status`, `tipo`, `bandeira` | sem limite |
| `rede_pagamento` | `payment_id` | — |
| `rede_pagamento_esperado` | `payment_id` | — |
| `rede_ordens_de_credito` | período, paginação | **30 dias** |
| `rede_debitos_do_pagamento` | `payment_id`, `tipos_de_ajuste` | — |
| `rede_cashbacks_do_pagamento` | `payment_id` | — |
| `rede_bloqueios_resumo` | `agrupar_por_dia` | sem limite |
| `rede_bloqueios_do_pagamento` | `payment_id` | — |

## Recebíveis — o que ainda vai cair

| Tool | Parâmetros principais | Janela |
|---|---|---|
| `rede_recebiveis_resumo` | `agrupar_por`, `bandeiras`, `contas_bancarias`*, `status`*, `tipo`**, `versao` (1/2/3, padrão 3) | v1: 30 dias; v2/v3: sem limite |
| `rede_recebiveis_calendario` | `tipo` (DAY/MONTH) | **60 dias** |
| `rede_recebiveis_diario` | período | sem limite |
| `rede_recebiveis_parcelas` | `bandeiras` (**obrigatório**), paginação | sem limite |

\* só na v3. \*\* só nas v1/v2.

## Débitos

| Tool | Parâmetros | Janela |
|---|---|---|
| `rede_debitos` | período, paginação | **30 dias** |
| `rede_debitos_resumo` | período | **30 dias** |
| `rede_tipos_de_ajuste` | nenhum | — |

## Utilitários

| Tool | Para quê |
|---|---|
| `rede_conciliar` | Cruza vendas × ordens de crédito pelo `saleSummaryNumber`. `venda_inicio`/`venda_fim` obrigatórios; janela de pagamento tem padrão deslocado em 40 dias. `detalhar: true` devolve tudo. |
| `rede_dominios` | Tabelas de código. Consulta local, não gasta chamada. |
| `rede_get` | GET livre. Não valida janela nem posiciona o PV — use as tools dedicadas quando existirem. |

## Paginação

Tools de lista aceitam `tamanho` (máx. 100), `page_key` e `paginar_tudo`. Com `paginar_tudo: true`
a tool segue o cursor até o fim ou até 20 páginas, e a resposta traz `completo` e, se parou no
teto, `proximo_page_key`.

## Comportamentos comuns

- **204** vira `{ vazio: true, mensagem: ... }` — consulta certa, período sem movimento.
- Respostas trazem os códigos **traduzidos** ao lado do original (`brandCode: 14` + `bandeira: "Elo"`).
- Erros de janela de data são barrados **antes** da chamada e o texto já sugere as fatias.
- Variáveis de ambiente: `REDE_CONFIG_FILE`, `REDE_STATE_DIR`, `REDE_TIMEOUT_MS`,
  `REDE_INTERVALO_MS`, `REDE_MAX_PAGINAS`.
