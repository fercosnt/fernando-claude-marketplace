# Ferramentas do MCP conta-azul

Gerado a partir do servidor (v0.1.1). Datas sempre `YYYY-MM-DD`. O parâmetro `empresa` é opcional quando só há uma empresa configurada.


## Conexão

| Tool | O que faz | Parâmetros |
|---|---|---|
| `contaazul_status` | Mostra se o arquivo de configuracao esta ok, quais empresas estao configuradas, quais ja foram conectadas (e ate quando o token vale), e se a escrita esta ligada. | — |
| `contaazul_conectar` | Gera o link de autorizacao OAuth da Conta Azul. | — |
| `contaazul_concluir_conexao` | Recebe a URL para onde a Conta Azul redirecionou (ou so o code) e troca pelos tokens, gravando-os localmente. | `url_ou_codigo` |

## Financeiro

| Tool | O que faz | Parâmetros |
|---|---|---|
| `contaazul_contas_receber` | Lista as PARCELAS de contas a receber por intervalo de VENCIMENTO (obrigatorio), com filtros opcionais de status, competencia, pagamento, valor, categoria, centro de custo e conta financeira. | `vencimento_de`, `vencimento_ate`, `status`, `descricao`, `competencia_de`, `competencia_ate`, `pagamento_de`, `pagamento_ate`, `valor_de`, `valor_ate`, `ids_contas_financeiras`, `ids_categorias`, `ids_centros_de_custo`, `ids_clientes`, `somente_vencidas`, `limite`, `formato` |
| `contaazul_contas_pagar` | Lista as PARCELAS de contas a pagar por intervalo de VENCIMENTO (obrigatorio), com filtros opcionais de status, competencia, pagamento, valor, categoria, centro de custo e conta financeira. | `vencimento_de`, `vencimento_ate`, `status`, `descricao`, `competencia_de`, `competencia_ate`, `pagamento_de`, `pagamento_ate`, `valor_de`, `valor_ate`, `ids_contas_financeiras`, `ids_categorias`, `ids_centros_de_custo`, `somente_vencidas`, `limite`, `formato` |
| `contaazul_resumo_financeiro` | Visao consolidada de um periodo em uma chamada. | `de`, `ate`, `incluir_saldos`, `incluir_categorias` |
| `contaazul_parcela` | Detalhe de uma parcela (receber ou pagar): evento, rateio por categoria e centro de custo, composicao de valor, status, versao. | `id`, `incluir_baixas` |
| `contaazul_parcelas_do_evento` | Lista todas as parcelas de um evento financeiro (lancamento de receber ou pagar) pelo id_evento.. | `id_evento` |
| `contaazul_contas_financeiras` | Lista as contas financeiras (banco, caixa, cartao, cobrancas Conta Azul...) com id, tipo e, opcionalmente, o saldo atual de cada uma.. | `apenas_ativo`, `com_saldo`, `nome` |
| `contaazul_categorias` | Lista categorias de receita/despesa (id, nome, tipo, hierarquia). | `tipo`, `busca`, `apenas_filhos` |
| `contaazul_categorias_dre` | Categorias do DRE (Demonstracao do Resultado) com a hierarquia contabil usada pela empresa.. | — |
| `contaazul_centros_de_custo` | Lista centros de custo (id, codigo, nome, ativo).. | `busca`, `filtro` |
| `contaazul_transferencias` | Transferencias entre contas financeiras num periodo.. | `data_inicio`, `data_fim`, `ids_conta_financeira` |
| `contaazul_alteracoes_financeiras` | IDs dos eventos financeiros (receber/pagar) criados ou alterados entre duas datas-hora. | `data_inicio`, `data_fim` |
| `contaazul_protocolo` | Consulta o processamento de um lancamento criado (a criacao de contas a receber/pagar e assincrona e devolve um protocolo). | `id` |

## Cadastros e vendas

| Tool | O que faz | Parâmetros |
|---|---|---|
| `contaazul_empresa` | Dados da empresa conectada (razao social, CNPJ, id_empresa). | — |
| `contaazul_pessoas` | Busca pessoas por nome/documento e filtros. | `busca`, `tipo_perfil`, `tipo_pessoa`, `emails`, `documentos`, `com_endereco`, `pagina`, `tamanho_pagina` |
| `contaazul_pessoa` | Cadastro completo de uma pessoa (cliente/fornecedor) pelo UUID.. | `id` |
| `contaazul_vendas` | Busca vendas por periodo de emissao, cliente, situacao ou texto. | `data_inicio`, `data_fim`, `termo_busca`, `ids_clientes`, `ids_vendedores`, `situacoes`, `ordenar_por`, `crescente`, `pagina`, `tamanho_pagina` |
| `contaazul_venda` | Detalhe completo de uma venda, com os itens.. | `id`, `incluir_itens` |
| `contaazul_vendedores` | Lista vendedores cadastrados (id para filtrar vendas e orcamentos).. | — |
| `contaazul_orcamentos` | Busca orcamentos por periodo, cliente, situacao ou texto.. | `data_inicio`, `data_fim`, `termo_busca`, `ids_clientes`, `situacoes`, `pagina`, `tamanho_pagina` |
| `contaazul_orcamento` | Detalhe de um orcamento.. | `id` |
| `contaazul_contratos` | Lista contratos recorrentes num intervalo de datas (obrigatorio), com status e busca por nome.. | `data_inicio`, `data_fim`, `status`, `busca`, `pagina`, `tamanho_pagina` |
| `contaazul_contrato` | Detalhe de um contrato recorrente.. | `id` |
| `contaazul_produtos` | Lista produtos por nome/SKU/EAN, status e faixa de preco.. | `busca`, `status`, `pagina`, `tamanho_pagina` |
| `contaazul_servicos` | Lista servicos cadastrados (procedimentos, no caso de clinica) por nome, codigo ou descricao.. | `busca`, `pagina`, `tamanho_pagina` |

## Notas fiscais

| Tool | O que faz | Parâmetros |
|---|---|---|
| `contaazul_notas_fiscais` | NF-e emitidas num periodo (obrigatorio), com filtros por documento do tomador, numero ou venda.. | `data_inicial`, `data_final`, `documento_tomador`, `numero_nota`, `id_venda` |
| `contaazul_notas_servico` | NFS-e por periodo de competencia. | `de`, `ate`, `status`, `tipo_negociacao` |

## Genérico

| Tool | O que faz | Parâmetros |
|---|---|---|
| `contaazul_get` | Faz um GET em qualquer endpoint /v1/... | `caminho`, `params` |

## Escrita (desligada por padrão; sempre prévia antes de enviar)

| Tool | O que faz | Parâmetros |
|---|---|---|
| `contaazul_criar_conta_receber` | Cria um lancamento de contas a receber (evento financeiro) com uma ou mais parcelas. | `descricao`, `valor`, `data_competencia`, `id_contato`, `id_conta_financeira`, `id_categoria`, `id_centro_custo`, `data_vencimento`, `metodo_pagamento`, `parcelas`, `observacao`, `confirmar` |
| `contaazul_criar_conta_pagar` | Cria um lancamento de contas a pagar (evento financeiro) com uma ou mais parcelas. | `descricao`, `valor`, `data_competencia`, `id_contato`, `id_conta_financeira`, `id_categoria`, `id_centro_custo`, `data_vencimento`, `metodo_pagamento`, `parcelas`, `observacao`, `confirmar` |
| `contaazul_baixar_parcela` | Registra o recebimento/pagamento (total ou parcial) de uma parcela. | `id_parcela`, `data_pagamento`, `valor`, `id_conta_financeira`, `metodo_pagamento`, `juros`, `multa`, `desconto`, `taxa`, `observacao`, `nsu`, `confirmar` |
| `contaazul_atualizar_parcela` | Altera vencimento, valor, descricao, nota, metodo ou conta de uma parcela. | `id_parcela`, `vencimento`, `valor`, `descricao`, `nota`, `metodo_pagamento`, `id_conta_financeira`, `data_pagamento_esperado`, `confirmar` |
| `contaazul_criar_pessoa` | Cadastra pessoa (cliente, fornecedor ou transportadora). | `nome`, `tipo_pessoa`, `perfis`, `cpf`, `cnpj`, `email`, `telefone_celular`, `data_nascimento`, `nome_fantasia`, `observacao`, `endereco`, `confirmar` |
| `contaazul_atualizar_pessoa` | Atualiza campos do cadastro (PATCH — so o que for informado muda).. | `id`, `campos`, `confirmar` |
| `contaazul_criar_venda` | Cria uma venda. | `id_cliente`, `data_venda`, `situacao`, `itens`, `condicao`, `tipo_pagamento`, `id_conta_financeira`, `parcelas`, `id_categoria`, `id_centro_custo`, `id_vendedor`, `numero`, `desconto_valor`, `observacoes`, `confirmar` |
| `contaazul_gerar_cobranca` | Gera cobranca Conta Azul (BOLETO, PIX_COBRANCA ou LINK_PAGAMENTO) para uma parcela a receber. | `id_parcela`, `id_conta_bancaria`, `tipo`, `data_vencimento`, `descricao_fatura`, `maximo_parcelas`, `confirmar` |

Total: 38 tools.
