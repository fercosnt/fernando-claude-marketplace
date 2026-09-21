# Credenciais da Rede

## O que você precisa

| Item | De onde vem |
|---|---|
| `client_id` e `client_secret` | Portal do Desenvolvedor → **Meus Projetos** → projeto do pacote *APIs de Conciliação* |
| `usuario` e `senha` | **Opcionais.** E-mail do time de Integrações da Rede (**não** é o login do portal) |
| Números de PV | Sandbox: `13381369`, `22523510` e `1254405` (só NSU). Produção: os PVs reais, liberados por estabelecimento |

### O pacote do projeto decide tudo

Credencial de um projeto de **Payment Link** autentica sem erro, mas o token sai com
`"scope": "payment-link"` e **toda** rota `/merchant-statement/*` responde `401 Unauthorized`.
O projeto tem de ser do pacote **APIs de Conciliação**, cujo token traz
`"scope": "merchant-statement feature_merchant_statement"`.

`rede_conectar` imprime o escopo e emite `ALERTA` quando ele não contém `merchant-statement`.

Para obter acesso de produção, a Rede pede por e-mail (`ecommerce@userede.com.br` no varejo, ou a
caixa da Linha Direta no atacado): razão social, CNPJ, e-mail, telefone e nicho da organização,
nome e e-mail do cliente, e quais APIs você quer acessar. A homologação no sandbox vem antes.

## Onde guardar

`~/.rede-mcp.json`, com `chmod 600`:

```json
{
  "ambiente": "sandbox",
  "client_id": "...",
  "client_secret": "...",
  "usuario": "...",
  "senha": "...",
  "pvs": [{ "nome": "Loja Centro", "numero": "13381369" }]
}
```

Campo opcional `base_nsu`: só se `rede_vendas_por_nsu` devolver 404. A documentação do sandbox
aponta `https://payments-apisandbox.useredecloud.com.br` para essa rota específica.

Os tokens ficam em `~/.rede-mcp/tokens/<ambiente>.json`, também com permissão 600, escritos pelo
servidor. Não edite à mão: apague o arquivo ou rode `rede_conectar` com `recomecar: true`.

## Regras

1. Nunca cole `client_secret`, senha ou token no chat — fica no histórico da conversa.
2. Se colar por engano, troque o valor no portal depois.
3. O plugin nunca imprime segredo: `rede_status` mostra só os últimos 6 caracteres do `client_id`.

## Como o token funciona

```
POST /oauth/token
Authorization: Basic base64(client_id:client_secret)
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials          # sem usuario/senha (padrão)
grant_type=password&username=…&password=…   # quando o par foi enviado pela Rede
```

**A documentação oficial só descreve o grant `password`**, mas o sandbox aceita
`client_credentials` com apenas client_id/secret e devolve token com o escopo correto — verificado
em 2026-09-20. O plugin escolhe o grant sozinho conforme o arquivo; o campo `grant` força um dos dois.

O `access_token` dura 1440 segundos (24 minutos, exatamente o que a doc manda renovar); o
`refresh_token`, 24 horas. Enquanto o refresh vive, a
renovação usa `grant_type=refresh_token`. Quando ele morre, o plugin refaz o login com usuário e
senha sozinho — você não precisa reconectar nada. Se dois clientes Claude estiverem abertos, uma
trava de arquivo impede que os dois renovem ao mesmo tempo e invalidem o token um do outro.

## Erros de credencial

| Mensagem | Causa |
|---|---|
| `Bad credentials` | `client_id`/`client_secret` errados, iguais entre si, ou de outro ambiente |
| `invalid_grant` | `usuario`/`senha` errados |
| Login ok, consulta 401 ou 403 | falta liberação do PV para este usuário na gestão de acessos da Rede |
