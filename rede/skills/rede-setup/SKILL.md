---
name: rede-setup
description: Configura o acesso as APIs da Rede (maquininha de cartao) nesta maquina — ambiente sandbox ou producao, client_id, client_secret, usuario, senha e os Pontos de Venda — sem segredo no chat. Use quando a pessoa pedir para configurar, instalar ou conectar a Rede, perguntar onde colocar as credenciais, ou quando qualquer tool rede_* falhar por falta de configuracao, "Bad credentials", 401 ou 403.
---

Guie a pessoa na configuracao do acesso as **APIs de Gestao de Vendas da Rede** nesta maquina.

## Regras que nao podem ser quebradas

1. **Nunca peca para colar `client_secret`, senha ou token no chat.** Tudo que passa pela conversa
   fica no historico. Os segredos vao do portal direto para o arquivo local.
2. **Nunca imprima o conteudo de `~/.rede-mcp.json` nem da pasta `~/.rede-mcp/`.**
3. Se a pessoa colar um segredo no chat assim mesmo, avise que aquele valor deve ser considerado
   exposto e trocado no portal depois do teste.

## O arquivo

Fica em `~/.rede-mcp.json`, com permissao de leitura so para a pessoa:

```json
{
  "ambiente": "sandbox",
  "client_id": "...",
  "client_secret": "...",
  "pvs": [
    { "nome": "Loja Centro", "numero": "13381369" }
  ]
}
```

**`usuario` e `senha` sao opcionais.** A documentacao da Rede so descreve o grant `password`, mas
na pratica o sandbox aceita `client_credentials` com apenas `client_id` e `client_secret` — e o
token sai com o escopo certo (`merchant-statement`). O plugin escolhe sozinho: sem usuario e senha,
usa `client_credentials`; com os dois, usa `password`. Para forcar um dos dois, o campo `grant`.

Depois de criar: `chmod 600 ~/.rede-mcp.json`.

Campo opcional `base_nsu`: so preencha se `rede_vendas_por_nsu` devolver 404. A doc do sandbox
aponta `https://payments-apisandbox.useredecloud.com.br` para essa rota, diferente de todas as outras.

## De onde vem cada valor

**`client_id` e `client_secret`** — do Portal do Desenvolvedor da Rede
(`developer.userede.com.br`), menu **Meus Projetos**: crie um projeto associado ao pacote
**APIs de Conciliacao** e as credenciais de teste aparecem na tela do projeto. Sao dois valores
**diferentes**; se ficarem iguais no arquivo, foi o mesmo valor colado duas vezes e o plugin recusa
na largada.

**O pacote do projeto importa mais que tudo.** Um projeto criado no pacote **Payment Link** gera
credencial que autentica normalmente, mas o token sai com escopo `payment-link` e **toda** rota de
extrato responde `401 Unauthorized`. O projeto tem de ser do pacote **APIs de Conciliacao**, cujo
token traz `merchant-statement` no escopo. `rede_conectar` mostra o escopo e alerta quando esta
errado — e o primeiro lugar para olhar quando "o login funciona mas nada responde".

**`usuario` e `senha`** — opcionais, e nao sao o login do portal. Sao credenciais que o time de
Integracoes da Rede envia por e-mail quando cadastra a organizacao, o usuario e a aplicacao. Em
producao, o cadastro e pedido por e-mail (`ecommerce@userede.com.br` para varejo, ou a caixa da
Linha Direta para atacado) informando: razao social, CNPJ, e-mail, telefone, nicho, nome e e-mail
do cliente, e quais APIs quer acessar.

**`pvs`** — os Pontos de Venda (estabelecimentos) que a pessoa pode consultar. No sandbox existem
apenas dois, com dados fixos: **13381369** e **22523510**. Em producao sao os PVs reais, e cada um
precisa ser liberado para o usuario na gestao de acessos da Rede.

## Ambientes

| Ambiente | Base da API | Token |
|---|---|---|
| `sandbox` | `https://rl7-sandbox-api.useredecloud.com.br` | `.../oauth/token` |
| `producao` | `https://api.userede.com.br/redelabs` | `.../redelabs/oauth/token` |

Credencial de um ambiente **nao funciona** no outro. A Rede exige homologar no sandbox antes de
liberar producao. Cada ambiente guarda o proprio token, entao trocar o campo `ambiente` nao mistura
sessoes.

## Passo a passo

1. Pergunte qual ambiente (comece por `sandbox`).
2. Peca para a pessoa criar o arquivo e colar as credenciais **no editor, nao no chat**. Se ajudar,
   copie `credenciais.exemplo.json` do plugin como ponto de partida.
3. `chmod 600 ~/.rede-mcp.json`.
4. Rode `rede_status` — confirma que o arquivo foi lido, sem mostrar segredo.
5. Rode `rede_conectar` — faz o login de verdade e confirma com uma consulta real.
6. Teste util: `rede_vendas` num periodo curto do PV de sandbox.

## Quando der erro

| Sintoma | Causa provavel |
|---|---|
| `Bad credentials` no login | `client_id`/`client_secret` errados, iguais, ou de outro ambiente |
| `invalid_grant` | `usuario`/`senha` errados (so no grant password) |
| Login ok, **toda** rota da 401 | projeto do pacote errado no Portal. Rode `rede_conectar` e olhe o escopo: se vier `payment-link`, crie um projeto em *APIs de Conciliacao* |
| 401 so em algumas rotas | falta liberacao daquele PV para o usuario na gestao de acessos da Rede |
| 403 "Requisicao invalida" | rota nao habilitada para o aplicativo. No sandbox e a resposta normal de recebiveis, bloqueios, resumos de venda e da v2 de vendas |
| 400 "scenario is not available in the sandbox" | o ambiente de teste nao tem esse caso. Em `/v1/payments`, mande um filtro do roteiro: `size` 1, 5 ou 10, `status=PENDING`, `brands=1`, `types=DEBIT` |
| 404 so em `rede_vendas_por_nsu` | preencher `base_nsu` |
| 204 / `vazio: true` | nao e erro: a consulta funcionou e nao havia registro no periodo |

## O que o sandbox realmente responde

Testado em 2026-09-20 com credencial do pacote APIs de Conciliacao:

| Rota | Sandbox |
|---|---|
| `/v1/sales` | **OK**, dados de nov/2022 nos PVs 13381369 e 22523510 |
| `/v1/sales/installments` | **OK** |
| `/v1/payments` | **OK, mas so com filtro** do roteiro (`size` 1/5/10, `status`, `brands`, `types`) |
| `/v1/payments/credit-orders` | **OK** |
| `/v1/charges`, `/v1/charges/summary`, `/v1/charges/adjustment-types` | **OK** |
| `/v1/sales/{pv}/daily` | **OK** so no PV 1254405, de 2022-11-22 a 2022-11-28 |
| `/v2/sales` e os resumos de venda | 403 — nao habilitados |
| recebiveis (v1, v2, v3) e bloqueios | 403 — nao habilitados |

O periodo com dado e **novembro de 2022**. Fora dele a consulta volta vazia mesmo com tudo certo.

**A conciliacao nao da para validar no sandbox:** os `saleSummaryNumber` das vendas e os das ordens
de credito sao conjuntos disjuntos (fixtures independentes), entao `rede_conciliar` roda mas nao
concilia nada. O cruzamento e provado no teste de integracao contra a API simulada.

## Ir para producao

**Ao trocar para producao, remova `usuario` e `senha` do arquivo** (a nao ser que a Rede tenha
mandado um par de producao). Com os dois preenchidos o plugin usa o grant `password`; se forem os
de sandbox, o login de producao falha com `invalid_grant`. Sem eles, vale o `client_credentials`,
que e o fluxo documentado. O arquivo de producao fica so com `ambiente`, `client_id`,
`client_secret` e `pvs`.

O caminho completo — e-mail para pedir credenciais, os 8 itens que a Rede exige, e a liberacao dos
PVs (que e o passo que costuma travar) — esta em `docs/producao.md`. Dois pontos que economizam
tempo: o `grant_type=password` do PDF de 2023 esta desatualizado, e ter credencial de producao
**nao** da acesso a nenhum PV; cada um precisa de solicitacao e aprovacao na area logada do lojista.

## Instalar o plugin

O servidor ja vai compilado em `servers/rede-mcp.js` (bundle sem dependencias). Para rodar a partir
do codigo-fonte: `cd server && npm install && npm run build`. O teste offline, que nao toca na API,
e `node test/run.mjs`.
