# API de Link de Pagamento da Rede

Levantamento feito em 2026-09-20, combinando o swagger oficial, os quatro documentos do Portal do
Desenvolvedor e **teste real no sandbox** (um link foi criado de verdade). Ainda **não implementada**
no plugin — este documento é a base para implementar quando for a hora.

Fonte primária guardada em [referencia/payment-link-swagger.json](referencia/payment-link-swagger.json),
tirada de `https://developer.userede.com.br/dev-portal-swaggers/payment-link-api/swagger.json`.

## O que é

API que cria uma **página de pagamento hospedada pela Rede**. Você envia valor, vencimento e
condições; recebe uma URL para mandar ao cliente, que paga com cartão de crédito (até 12x) ou PIX.

Diferença essencial em relação à API de Gestão de Vendas, já implementada neste plugin: **aquela é
100% leitura; esta cria cobrança real**. Todo o desenho muda por causa disso.

São só três operações. **Não existe** listagem de links, estorno (aparece apenas como leitura em
`Refunds` + `Reversible`) nem webhook.

| Operação | Rota | Resposta |
|---|---|---|
| Criar | `POST /payment-link/v1/create` | `{ paymentLinkId, message, url }` |
| Consultar | `GET /payment-link/v1/details/{paymentLinkId}` | `{ Order, Billing, Transaction, Merchant, Refunds, Reversible }` |
| Cancelar | `PATCH /payment-link/v1/cancel/{paymentLinkId}` | `{ paymentLinkId, message }` |

## Bases e autenticação

| Ambiente | Base |
|---|---|
| Sandbox | `https://payments-apisandbox.useredecloud.com.br` |
| Produção | `https://payments-api.useredecloud.com.br` |

**Host diferente do de conciliação** (`rl7-sandbox-api…`), mas o token sai do mesmo emissor.

OAuth com `grant_type=client_credentials`, `Authorization: Basic base64(client_id:client_secret)`.
Obrigatório desde 05/01/2026. `access_token` dura 1440 s (24 minutos).

Sobre o endpoint de token há divergência na documentação da Rede — os docs dizem `/oauth2/token` e
o swagger diz `/oauth/token`. **Testado: os dois funcionam** e devolvem o mesmo escopo
(`payment-link`). O plugin de conciliação já usa `/oauth/token`.

O `client_id`/`client_secret` precisa ser de um projeto do pacote **Payment Link**. A credencial de
*APIs de Conciliação* **não** serve aqui, e vice-versa: cada uma autentica normalmente e recebe 401
nas rotas da outra. São dois projetos separados no portal.

## Cabeçalhos

Nas três rotas:

- `Authorization: Bearer <token>`
- `company-number` — o número do PV. **Vai no header**, não em query nem no corpo. Sem ele: 422.
- `Content-Type: application/json`

## Payload de criação

Obrigatórios: `amount`, `description`, `expirationDate`, `installments`, `paymentOptions`.

| Campo | Tipo | Regra |
|---|---|---|
| `amount` | number | Maior que zero. Abaixo de R$ 1,00 é recusado. Teto depende do contrato (no simulador, 20.000) |
| `description` | string | 1 a 50 caracteres, não pode ser vazia |
| `expirationDate` | string | **`MM/DD/YYYY`** — formato americano. De hoje até no máximo +15 dias |
| `installments` | int | 1 a 12 |
| `paymentOptions` | array | Só `"credit"` e/ou `"pix"`. Em produção depende das habilitações do PV |
| `createdBy` | string | Opcional. E-mail, até 65 caracteres |
| `comments` | string | Opcional, até 255 caracteres |

**Não existem** campos de cliente (nome, CPF, e-mail), callback/webhook nem split. `Billing.phone` e
`emailSubject` aparecem só na resposta e a documentação manda ignorá-los na v1.

Exemplo que funcionou no sandbox:

```json
{
  "amount": 149.90,
  "description": "Teste plugin Claude - consulta",
  "expirationDate": "10/05/2026",
  "installments": 3,
  "paymentOptions": ["credit", "pix"],
  "createdBy": "fulano@exemplo.com",
  "comments": "criado por automacao"
}
```

Resposta: `{"paymentLinkId": "33j36w0", "message": "Inserted Successfully", "url": "https://sandbox.userede.com.br/pagamentos/pt/33j36w0"}`

## Regras de negócio

- Validade máxima de **15 dias** a partir da criação.
- **Antifraude obrigatório e gratuito** em todo link criado por API (`fraudCheck: "Y"`). Não desliga.
- **5 tentativas** de pagamento por link (`failureThreshold`).
- Status possíveis: `CREATED`, `PAID`, `EXPIRED`, `CANCELED`, `REVERSED`, `REJECTED`.
- PIX devolve `Transaction.pix.emv` (o copia-e-cola) na consulta.
- O produto precisa estar habilitado e os termos aceitos no portal userede antes de integrar.
- **Migração de identificador:** desde 02/09/2026 a URL e o `paymentLinkId` usam o mesmo UUID. Use
  sempre o `paymentLinkId` devolvido na criação para consultar e cancelar — nunca o pedaço da URL.

## Sem webhook: só polling

A Rede é explícita — não há notificação automática, está previsto para o futuro. Para saber se o
link foi pago, é preciso consultar. Recomendação oficial: começar **5 minutos** após a criação e
repetir **a cada 1 minuto** até um status definitivo.

Isso define o custo de qualquer automação de "me avise quando pagar": ela é um laço de consultas,
não um push.

## Armadilhas confirmadas no teste

1. **`expirationDate` é `MM/DD/YYYY`.** Mandar `05/10/2026` pensando em "5 de outubro" faz a API ler
   10 de maio e recusar como data passada. Vale uma conversão explícita antes de qualquer chamada.
2. **Mensagem de erro enganosa em valor baixo.** R$ 0,50 responde
   `"Amount should be less than 20000. Provided amount: value"` — fala do teto quando o problema é o
   piso de R$ 1,00.
3. **`company-number` no header.** Sem ele, 422 com
   `"missing request header 'company-number'"`.
4. Erros de validação vêm em **dois formatos diferentes**: às vezes uma lista
   `[{"FailedField": "...", "Message": "..."}]`, às vezes um objeto `{"message": "..."}`. Quem for
   implementar precisa tratar os dois.

## Estado do sandbox (testado)

| Operação | Sandbox |
|---|---|
| `create` | **Funciona de verdade.** Gera link real e valida todas as regras acima |
| `details` | Responde 200, mas **com dados mockados**: campos literalmente `"example"`, `amount` fixo em 1000, `paymentOptions` sempre `["credit"]`. Só `paymentLinkId`, `url` e `status` refletem o link criado |
| `cancel` | **Quebrado.** O stub do WireMock está configurado esperando o header `authorization` *ausente*, mas o gateway exige o header — dá 404 com auth e 401 sem. Sem contorno do nosso lado |

O 404 do cancelamento vaza a configuração do stub no corpo da resposta, que foi como o problema
apareceu:

```
authorization [absent] : (absent)  |  authorization: Bearer eyJ...  <<<<< Header does not match
```

Consequência: `cancel` só poderá ser validado em produção, e `details` precisa ser testado em
produção antes de confiar no que ele devolve.

## O destino provável: n8n + CRM, não tools MCP

O caso de uso real é a clínica: consulta agendada no CRM dispara a cobrança e manda o link ao
paciente pelo WhatsApp. Isso é um workflow n8n, não uma conversa com o Claude — o link precisa sair
sozinho, sem ninguém pedindo. As tools MCP ficam como opção para o caso de alguém querer gerar uma
cobrança no meio de uma conversa.

### O que importa ao montar no n8n

**O token de 24 minutos resolve-se com credencial, não com nó.** O n8n tem credencial *OAuth2 API*
com grant *Client Credentials*, que renova sozinha — é o caminho limpo, em vez de um nó HTTP para
pegar token antes de cada chamada:

| Campo da credencial | Valor |
|---|---|
| Grant Type | Client Credentials |
| Access Token URL | `https://rl7-sandbox-api.useredecloud.com.br/oauth/token` (produção: `https://api.userede.com.br/redelabs/oauth/token`) |
| Client ID / Secret | os do projeto **Payment Link** |
| Authentication | Basic (envia as credenciais no header, que é o que a Rede espera) |

*A confirmar no ambiente:* não testei essa credencial dentro do n8n, só o fluxo OAuth direto. Se o
n8n insistir em mandar as credenciais no corpo em vez do header, cai-se no plano B: um nó HTTP
Request para o token seguido do nó de criação.

**A criação é um HTTP Request POST** para
`https://payments-apisandbox.useredecloud.com.br/payment-link/v1/create`, com header
`company-number` (o PV) e o JSON do payload.

**A data precisa de expressão.** Como o formato é `MM/DD/YYYY` e o limite é 15 dias:

```
{{ $now.plus({ days: 7 }).toFormat('MM/dd/yyyy') }}
```

Escrever a data à mão, ou reaproveitar um campo `DD/MM/YYYY` vindo do CRM, é o erro mais provável
desse workflow — e ele falha silenciosamente para dias menores que 13, virando um link com validade
errada em vez de um erro.

**Confirmar o pagamento custa polling.** Sem webhook, o desenho é um Schedule Trigger (ou um Wait em
laço) consultando `details` a cada minuto, começando 5 minutos depois da criação, até `PAID`,
`EXPIRED` ou `CANCELED`. Vale limitar o número de voltas: o link morre em 15 dias, mas ninguém quer
um laço de 15 dias.

**Tratar os dois formatos de erro**, porque a API alterna entre eles — ver a seção de armadilhas.

## Decisões de desenho já tomadas

Para quando (e se) for implementado como tool MCP:

- **Prévia obrigatória.** `criar` e `cancelar` nunca executam direto: primeira chamada devolve a
  prévia do que será criado, e só uma segunda chamada com `confirmar=true` envia. Mesmo padrão do
  plugin conta-azul. Vale nos dois ambientes — em sandbox o link é inofensivo, mas o hábito de
  confirmar é o que protege produção.
- **Segundo MCP server dentro do mesmo plugin `rede`**, com credenciais próprias no
  `~/.rede-mcp.json` (bloco separado), porque o projeto do portal e o escopo do token são outros.
- **Conversão de data explícita**: a tool aceita `YYYY-MM-DD` (o padrão do resto do plugin) e
  converte para `MM/DD/YYYY` na hora de chamar, validando o teto de 15 dias antes.
- Uma tool de **acompanhamento por polling** é opcional e deve ser explícita sobre o custo: sem
  webhook, cada verificação é uma chamada.

## Onde isso se conecta com o resto

O link pago vira venda na maquininha, que vira pagamento — e o `rede_conciliar`, já implementado
neste plugin, sabe cruzar os dois. O ciclo completo, com cada peça no lugar certo:

| Etapa | Onde roda |
|---|---|
| Consulta agendada gera a cobrança | n8n, disparado pelo CRM |
| Link enviado ao paciente | n8n → WhatsApp |
| Acompanhar até `PAID` | n8n, por polling |
| Conferir o depósito e conciliar | plugin `rede`, aqui no Claude |

Ou seja: o n8n cuida do que precisa acontecer sozinho, e o Claude cuida do que precisa de análise.
