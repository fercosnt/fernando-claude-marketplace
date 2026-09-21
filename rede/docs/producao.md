# Como sair do sandbox e usar na conta real

Levantado em 2026-09-20 das documentações oficiais de **Autenticação** (atualizada 21/03/2024) e
**Gestão de Acessos** (21/03/2024), mais o que foi confirmado testando.

## Primeiro: você provavelmente não precisa de "login e senha"

O PDF de Gestão de Vendas que circula (15/02/2023) manda usar `grant_type=password` com um usuário e
uma senha enviados por e-mail. **Isso está desatualizado.** A documentação de Autenticação, mais
recente, descreve o `client_credentials` como o fluxo — só `client_id` e `client_secret`, sem
usuário nem senha. Foi o que funcionou no teste, com o escopo correto.

Então o que você precisa obter não é um login: é **um par de credenciais de produção** e **a
liberação dos seus PVs**. São duas coisas separadas, e a segunda é a que costuma travar.

## Passo 1 — Credenciais de produção

Sandbox é self-service (você já gerou, em *Meus Projetos*). Produção não: é por e-mail.

**Para quem enviar:** `ecommerce@userede.com.br` se você for varejo ou não souber seu segmento. Se
for cliente do atacado, para o seu Box da Linha Direta.

**O que informar** (a lista é literal da documentação):

1. Nome da Empresa/Organização parceira que usará as APIs
2. CNPJ da Empresa/Organização
3. E-mail da Empresa/Organização
4. Telefone da Empresa/Organização
5. Segmento da Empresa/Organização (banco, credenciadora, subcredenciador etc.)
6. Nome do Cliente
7. E-mail do Cliente
8. API(s) que deseja acessar

No seu caso, "Empresa parceira" e "Cliente" são a mesma pessoa jurídica — você não é um
conciliador atendendo terceiros, é o próprio estabelecimento. Vale dizer isso no e-mail para evitar
idas e vindas.

Em "API(s) que deseja acessar", peça explicitamente:

- **Gestão de Vendas** (`merchant-statement`) — é o que este plugin usa
- **Gestão de Acessos** — necessária para o passo 2, se você quiser liberar PVs por API
- **Link de Pagamento** — só se for fazer a cobrança por link (projeto e credencial **separados**)

> **Pré-requisito declarado:** *"Para utilizar a API em Produção, primeiramente a Rede precisará
> certificar o parceiro em ambiente de Sandbox."* Na prática, a homologação no sandbox já está
> feita — o plugin roda contra ele e as evidências estão em [testes.md](testes.md).

Cadastro de **novo usuário** (mesmo canal): CNPJ, nome e e-mail do usuário.
Cadastro de **nova aplicação**: e-mail do usuário e as APIs desejadas.

## Passo 2 — Liberar os seus PVs (o que realmente trava)

Ter credencial de produção **não** dá acesso a nenhum estabelecimento. Cada PV precisa ser liberado,
e o erro típico é `401`/`403` em toda consulta com o token funcionando — foi justamente o cenário
que o plugin aprendeu a diagnosticar.

Existem dois caminhos.

### Pelo portal (mais simples)

O parceiro solicita e **o próprio PV aprova**: ao logar na área do lojista no Portal Rede, aparece
uma mensagem avisando que há uma solicitação pendente; basta clicar e aceitar. Como o PV é seu, você
solicita e você mesmo aprova.

### Pela API de Gestão de Acessos

Três operações, base igual à das outras APIs:

| Operação | Rota |
|---|---|
| Solicitar acesso | `POST /partner/v1/organizations/requests/features/merchant-statement` |
| Consultar solicitação | `GET /partner/v1/organizations/requests/{requestId}/features/merchant-statement` |
| Cancelar | `POST /partner/v1/organizations/requests/{requestId}/features/merchant-statement/cancel` |

Corpo da solicitação:

| Campo | Obrigatório | O que é |
|---|---|---|
| `requestCompanyNumber` | sim | O PV (matriz, filial ou autônomo) |
| `requestType` | sim | `I` individual, `P` parcial (matriz + filiais escolhidas), `T` total (matriz + todas as filiais, automático) |
| `companyNumbers` | só se `P` | Lista das filiais |
| `permissions` | sim | Nível de acesso |

Regras que evitam retrabalho:

- Enquanto houver **solicitação pendente** para um PV, não dá para pedir outra — devolve `409`.
- Solicitações **não expiram**; ficam pendentes até serem aprovadas ou reprovadas.
- A aprovação é do PV, pelo portal. A API só cria e acompanha o pedido.
- Se a clínica tem matriz e filiais, `T` resolve tudo de uma vez.

### O que se vê quando o PV ainda não foi liberado

Confirmado em produção em 2026-09-21, com o login funcionando:

- `403 Partner not allowed for this company number.` — nas rotas de vendas
- `401 Partner not allowed for this merchant` (código 1001) — nos recebíveis v3
- `401 Insufficient access level to access this feature.` — no resumo de pagamentos v2

As três somem com a liberação. A credencial de Gestão de Vendas também alcança a API de Gestão de
Acessos, então a solicitação pode ser criada por API sem pedir nada à Rede.

## Passo 3 — Configurar o plugin

Trocar duas linhas no `~/.rede-mcp.json`:

```json
{
  "ambiente": "producao",
  "client_id": "<o de produção>",
  "client_secret": "<o de produção>",
  "pvs": [
    { "nome": "Clínica", "numero": "<PV real>" }
  ]
}
```

O plugin troca a base sozinho (`https://api.userede.com.br/redelabs`) e guarda o token de produção
**separado** do de sandbox, então dá para alternar sem embaralhar sessão.

Depois: `rede_conectar`. Ele mostra o escopo do token — se não vier `merchant-statement`, a
credencial é do projeto errado e nenhuma consulta vai funcionar.

## Onde achar o número do seu PV

O PV (Ponto de Venda) é o número do estabelecimento na Rede — aparece na área do lojista no Portal
Rede, no extrato e nos comprovantes da maquininha. Tem até 9 dígitos. Se a clínica tem mais de uma
maquininha ou mais de uma unidade, provavelmente há mais de um PV, e cada um precisa entrar na lista
`pvs`.

## Diferenças de produção que valem saber antes

- **Sem os limites artificiais do sandbox.** As rotas que respondem `403 "Requisição inválida"` no
  sandbox (v2 de vendas, resumos, recebíveis, bloqueios) devem funcionar em produção, se o pacote
  contratado as incluir. O fallback automático de v2 para v1 continua valendo como rede de proteção.
- **`details` do Link de Pagamento devolve dado real** (no sandbox é mockado), e o `cancel`, que
  está quebrado no sandbox, só poderá ser testado lá.
- **Dados de verdade.** Vale começar por um período curto e conferir um número contra o extrato do
  portal antes de confiar em relatório automático.
- **Janelas de data continuam valendo**: 62 dias em vendas, 30 em pagamentos e débitos.

## Checklist

- [ ] E-mail enviado ao canal certo com os 8 itens
- [ ] Credenciais de produção recebidas (Gestão de Vendas)
- [ ] Credencial separada de Link de Pagamento, se for usar
- [ ] PV(s) da clínica identificados
- [ ] Solicitação de acesso criada (portal ou API)
- [ ] Solicitação **aprovada** na área logada do PV
- [ ] `~/.rede-mcp.json` com `ambiente: "producao"` e os PVs reais
- [ ] `rede_conectar` com escopo `merchant-statement`
- [ ] Um número conferido contra o extrato do portal
