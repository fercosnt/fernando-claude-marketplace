# Endpoints da API v2 Conta Azul

Gerado dos OpenAPI oficiais (developers.contaazul.com/_bundle/...yaml) em 2026-09-20.
Base: https://api-v2.contaazul.com. Campos de payload: https://developers.contaazul.com/llms.txt -> area.md -> endpoint.md

> A documentacao tem dois conjuntos para Financeiro e Produtos: `docs/financial-apis-openapi` (`/v1/financeiro/eventos-financeiros/...`, citado no changelog) e `open-api-docs/open-api-finance` (`/v1/financeiro/contas-a-receber`, ...). O servidor usa o primeiro. Se um endpoint do segundo for necessario, use `contaazul_get`.


## Baixas (`acquittance-apis-openapi`)

- `POST /v1/financeiro/eventos-financeiros/parcelas/{parcela_id}/baixa` — Criar uma nova baixa
- `GET /v1/financeiro/eventos-financeiros/parcelas/{parcela_id}/baixa` — Retornar as baixas pelo id da parcela
- `PATCH /v1/financeiro/eventos-financeiros/parcelas/baixa/{baixa_id}` — Atualizar parcialmente uma baixa por id
- `DELETE /v1/financeiro/eventos-financeiros/parcelas/baixa/{baixa_id}` — Deletar baixa por id
- `GET /v1/financeiro/eventos-financeiros/parcelas/baixa/{baixa_id}` — Retornar a baixa por id

## Cobranças (`charge-apis-openapi`)

- `GET /v1/financeiro/eventos-financeiros/contas-a-receber/cobranca/{id_cobranca}` — Retornar a cobrança por id
- `DELETE /v1/financeiro/eventos-financeiros/contas-a-receber/cobranca/{id_cobranca}` — Deletar cobrança por id
- `POST /v1/financeiro/eventos-financeiros/contas-a-receber/gerar-cobranca` — Criar uma nova cobrança

## Contratos (`contracts-apis-openapi`)

- `POST /v1/contratos` — Criar um novo contrato
- `GET /v1/contratos` — Retornar os contratos por filtro
- `GET /v1/contratos/proximo-numero` — Retornar o próximo número do contrato disponível

## Captura (`developer-platform-open-api-capture`)

- `POST /v1/captura/documentos` — Envia um documento para a captura e extração de dados
- `GET /v1/captura/documentos/status` — Consulta o status de documentos e das extrações (Captura)
- `GET /v1/captura/{id}` — Consulta os dados extraídos da captura do documento enviado
- `POST /v1/captura/{id}` — Aceita a prévia do evento financeiro da captura
- `DELETE /v1/captura/{id}` — Recusa a captura (rejeita o evento financeiro sugerido)

## Financeiro (`financial-apis-openapi`)

- `GET /v1/centro-de-custo` — Retornar os centros de custo por filtro
- `POST /v1/centro-de-custo` — Criar um novo centro de custo
- `GET /v1/financeiro/eventos-financeiros/{id_evento}/parcelas` — Retornar as parcelas pelo id do evento financeiro
- `GET /v1/categorias` — Retornar as categorias por filtro
- `GET /v1/categorias/configuracao-padrao` — Retornar a configuração de de-para de categorias
- `GET /v1/financeiro/categorias-dre` — Retornar as categorias DRE
- `GET /v1/conta-financeira` — Retornar as contas financeiras por filtro
- `GET /v1/conta-financeira/{id_conta_financeira}/saldo-atual` — Retornar o saldo atual pelo id da conta financeira
- `GET /v1/financeiro/transferencias` — Retornar as transferências entre contas financeiras por filtro
- `POST /v1/financeiro/eventos-financeiros/contas-a-receber` — Criar um novo evento financeiro de contas a receber
- `GET /v1/financeiro/eventos-financeiros/contas-a-receber/buscar` — Retornar as receitas por filtro
- `POST /v1/financeiro/eventos-financeiros/contas-a-pagar` — Criar um novo evento financeiro de contas a pagar
- `GET /v1/financeiro/eventos-financeiros/contas-a-pagar/buscar` — Retornar as despesas por filtro
- `GET /v1/financeiro/eventos-financeiros/parcelas/{id}` — Retornar a parcela por id
- `PATCH /v1/financeiro/eventos-financeiros/parcelas/{id}` — Atualizar parcialmente uma parcela por id
- `GET /v1/financeiro/eventos-financeiros/alteracoes` — Retornar os IDs dos eventos financeiros alterados em um período
- `GET /v1/financeiro/eventos-financeiros/saldo-inicial` — Retornar os saldos iniciais das contas financeiras

## Produto (`inventory-apis-openapi`)

- `GET /v1/produto/busca` — Obter produtos por filtro
- `POST /v1/produto` — Criar um novo produto
- `DELETE /v1/produto/{id}` — Excluir um produto existente
- `POST /v1/produto/desativar` — Desativar produtos

## Financeiro (`open-api-finance`)

- `GET /v1/financeiro/baixas` — Retornar as baixas pelo id da parcela
- `POST /v1/financeiro/baixas` — Criar uma nova baixa
- `GET /v1/financeiro/baixas/{id}` — Retornar a baixa por id
- `DELETE /v1/financeiro/baixas/{id}` — Deletar baixa por id
- `PATCH /v1/financeiro/baixas/{id}` — Atualizar parcialmente uma baixa por id
- `GET /v1/financeiro/categorias` — Retornar as categorias por filtro
- `GET /v1/financeiro/categorias-dre` — Retornar as categorias DRE
- `GET /v1/financeiro/categorias/configuracao-padrao` — Retornar a configuração de de-para de categorias
- `GET /v1/financeiro/categorias/{id}` — Retornar a categoria por id
- `GET /v1/financeiro/centros-de-custo` — Retornar os centros de custo por filtro
- `POST /v1/financeiro/centros-de-custo` — Criar um novo centro de custo
- `PATCH /v1/financeiro/centros-de-custo/{id}` — Atualizar parcialmente um centro de custo
- `POST /v1/financeiro/cobrancas` — Criar uma nova cobrança
- `GET /v1/financeiro/cobrancas/{id}` — Retornar a cobrança por id
- `DELETE /v1/financeiro/cobrancas/{id}` — Deletar cobrança por id
- `GET /v1/financeiro/contas-a-pagar` — Retornar as despesas por filtro
- `POST /v1/financeiro/contas-a-pagar` — Criar um novo evento financeiro de contas a pagar
- `GET /v1/financeiro/contas-a-receber` — Retornar as receitas por filtro
- `POST /v1/financeiro/contas-a-receber` — Criar um novo evento financeiro de contas a receber
- `GET /v1/financeiro/contas-financeiras` — Retornar as contas financeiras por filtro
- `GET /v1/financeiro/contas-financeiras/saldo-inicial` — Retornar os saldos iniciais das contas financeiras
- `GET /v1/financeiro/contas-financeiras/{id_conta_financeira}/saldo-atual` — Retornar o saldo atual pelo id da conta financeira
- `GET /v1/financeiro/eventos-financeiros/alteracoes` — Retornar os IDs dos eventos financeiros alterados em um período
- `GET /v1/financeiro/parcelas` — Retornar as parcelas pelo id do evento financeiro
- `GET /v1/financeiro/parcelas/{id}` — Retornar a parcela por id
- `PATCH /v1/financeiro/parcelas/{id}` — Atualizar parcialmente uma parcela por id
- `GET /v1/financeiro/transferencias` — Retornar as transferências entre contas financeiras por filtro

## Produtos (`open-api-inventory`)

- `GET /v1/produtos` — Retornar os produtos por filtro
- `POST /v1/produtos` — Criar um novo produto
- `GET /v1/produtos/categorias` — Retornar as categorias por filtro
- `GET /v1/produtos/cest` — Retornar os cests por filtro
- `GET /v1/produtos/ecommerce-categorias` — Retornar as categorias de e-commerce por filtro
- `GET /v1/produtos/ecommerce-marcas` — Retornar as marcas de ecommerce por filtro
- `GET /v1/produtos/ncm` — Retornar os ncms por filtro
- `GET /v1/produtos/unidades-medida` — Retornar as unidades de medida por filtro
- `GET /v1/produtos/{id}` — Retornar o produto por id
- `DELETE /v1/produtos/{id}` — Deletar produto por id
- `PATCH /v1/produtos/{id}` — Atualizar parcialmente um produto por id

## Notas fiscais (`open-api-invoice`)

- `GET /v1/notas-fiscais` — Retornar as notas fiscais por filtro
- `GET /v1/notas-fiscais-servico` — Retornar notas fiscais de serviço por filtros
- `POST /v1/notas-fiscais/vinculo-mdfe` — Vincular nota fiscal a mdfe
- `GET /v1/notas-fiscais/{chave}` — Retornar a nota fiscal por chave

## Pessoas (`open-api-person`)

- `GET /v1/pessoas` — Retornar as pessoas por filtro
- `POST /v1/pessoas` — Criar uma nova pessoa
- `POST /v1/pessoas/ativar` — Ativar pessoas em lote
- `GET /v1/pessoas/conta-conectada` — Retornar dados da empresa conectada
- `POST /v1/pessoas/excluir` — Excluir pessoas em lote
- `POST /v1/pessoas/inativar` — Desativar pessoas em lote
- `GET /v1/pessoas/legado/{id}` — Retornar a pessoa por legacyid
- `GET /v1/pessoas/{id}` — Retornar a pessoa por id
- `PUT /v1/pessoas/{id}` — Atualizar uma pessoa por id
- `PATCH /v1/pessoas/{id}` — Atualizar parcialmente uma pessoa por id

## Orçamentos (`open-api-proposal`)

- `GET /v1/orcamentos` — Retornar orçamentos por filtros
- `POST /v1/orcamentos` — Criar um orçamento
- `DELETE /v1/orcamentos` — Excluir orçamentos em lote
- `GET /v1/orcamentos/{id}` — Retornar o orçamento por ID

## Contratos (`open-api-scheduled-sales`)

- `GET /v1/contratos` — Retornar os contratos por filtro
- `POST /v1/contratos` — Criar um novo contrato
- `GET /v1/contratos/proximo-numero` — Retornar o próximo número do contrato disponível
- `GET /v1/contratos/{id}` — Retornar o contrato por id
- `DELETE /v1/contratos/{id}` — Remover um contrato
- `POST /v1/contratos/{id}/encerrar` — Encerrar um contrato

## Serviços (`open-api-service`)

- `GET /v1/servicos` — Retornar os serviços por filtro
- `POST /v1/servicos` — Criar um novo serviço
- `DELETE /v1/servicos` — Deletar serviços em lote
- `GET /v1/servicos/{id}` — Retornar o serviço por id
- `PATCH /v1/servicos/{id}` — Atualizar parcialmente um serviço por id

## Protocolos (`protocol-apis-openapi`)

- `GET /v1/protocolo/{id}` — Retornar o protocolo por id

## Vendas (`sales-apis-openapi`)

- `GET /v1/venda/vendedores` — Retornar os vendedores
- `GET /v1/venda/{id}` — Retornar a venda por id
- `PUT /v1/venda/{id}` — Atualizar uma venda por id
- `GET /v1/venda/busca` — Retornar as vendas por filtro
- `POST /v1/venda` — Criar uma nova venda
- `GET /v1/venda/{id}/imprimir` — Retornar o PDF de uma venda
- `POST /v1/venda/exclusao-lote` — Excluir vendas em lote
- `GET /v1/venda/{id_venda}/itens` — Retornar os itens de uma venda pelo id da venda
- `GET /v1/venda/proximo-numero` — Retornar o próximo número de venda disponível
