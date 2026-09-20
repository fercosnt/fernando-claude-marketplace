---
name: conta-azul-escrita
description: Liga ou desliga as tools que alteram dados na Conta Azul (lancamentos, baixas, cadastros, vendas, cobrancas). Use quando a pessoa pedir para ligar/desligar/liberar a escrita, ou quando uma tool contaazul_* recusar dizendo que a escrita esta DESLIGADA e a pessoa quiser mesmo alterar dados.
---

Liga ou desliga a escrita na Conta Azul nesta maquina, editando o campo `escrita` de
`~/.conta-azul-mcp.json`.

## Regras que nao podem ser quebradas

1. **Nunca imprima o arquivo** — ele tem o client_secret.
2. **Nunca ligue sem a pessoa pedir explicitamente nesta conversa.**
3. **Backup antes, validacao depois.**

## Passos

1. Rode `contaazul_status` e diga o estado atual da escrita.
2. Se a intencao nao estiver clara, pergunte. Ao **ligar**, diga o que passa a ser possivel: criar contas a
   receber e a pagar, registrar baixas (quitar parcelas), alterar parcelas, cadastrar/editar pessoas, criar
   vendas e gerar cobrancas — dados reais, sem desfazer pela API. E que toda escrita continua em dois passos:
   o Claude mostra a previa e so envia depois do ok.
3. Se o estado pedido ja for o atual, diga e pare.
4. Copie o arquivo para `~/.conta-azul-mcp.json.bak`; carregue o JSON; troque **apenas** `escrita`
   para `true`/`false`; grave com indentacao 2 e `chmod 600`.
5. Valide sem imprimir: JSON faz parse; `client_id`, `client_secret`, `redirect_uri` continuam preenchidos;
   `empresas` tem o mesmo tamanho; `escrita` esta no estado pedido. Falhou → restaure o backup. Passou → apague o backup.
6. A escrita e lida **quando o servidor sobe** (de proposito). Peca para reiniciar o Claude e confira com
   `contaazul_status` — deve mostrar `LIGADA` ou `DESLIGADA`.
