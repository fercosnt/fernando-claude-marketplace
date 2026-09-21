# rede

Plugin para usar as **APIs de Gestão de Vendas da Rede** (a maquininha de cartão) no Claude Code e no
Cowork. O MCP roda **na sua máquina**: credenciais e tokens nunca saem do seu computador.

**Versão 0.1.0.** Pergunte em português — "quanto vendi na maquininha em setembro?", "quando cai a
venda de ontem?", "por que caiu menos do que eu esperava?" — e o Claude consulta a API e responde
com número real.

A API da Rede é **somente leitura**: não existe rota que altere dado do estabelecimento. Por isso
este plugin não tem camada de escrita nem confirmação em dois passos.

## O que vem no plugin

| Componente | O que faz |
|---|---|
| **Servidor MCP** (29 tools) | Vendas detalhadas e sumarizadas, venda por NSU, parcelas de uma venda, pagamentos (CIP, diário, sumarizado, por id), ordens de crédito, débitos e cashbacks de um pagamento, bloqueios, recebíveis (resumo v1/v2/v3, calendário, diário, parcelas), débitos e tipos de ajuste, conciliação venda↔pagamento, tabelas de domínio e GET genérico. Ver [docs/ferramentas.md](docs/ferramentas.md) |
| **Skill `rede`** | Qual tool responde cada pergunta e como ler o número sem confundir venda, recebível e pagamento |
| **Skill `rede-setup`** | Configura credenciais e ambiente sem segredo no chat |
| **Skill `rede-conciliacao`** | O fluxo de fechamento: da venda ao depósito, e por que caiu menos |

## Instalação

**Claude Code:**

```bash
/plugin marketplace add fercosnt/fernando-claude-marketplace
/plugin install rede@fernando-claude-marketplace
```

**Cowork (Claude Desktop):** Settings → Plugins → marketplace `fercosnt/fernando-claude-marketplace` → `rede`.

Reinicie o Claude e diga "configura a Rede" (ou `/rede-setup`).

Requisito: Node 18 ou superior. O servidor é um único arquivo, sem dependências para instalar.

## Credenciais: onde colocar

No arquivo **`~/.rede-mcp.json`** (permissão 600):

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

- `client_id` e `client_secret` saem do projeto criado em **Meus Projetos** no
  [Portal do Desenvolvedor da Rede](https://developer.userede.com.br). **O projeto precisa ser do
  pacote *APIs de Conciliação*** — um projeto de *Payment Link* autentica normalmente, mas o token
  sai com escopo `payment-link` e toda rota de extrato responde 401.
- `usuario` e `senha` são **opcionais**. A doc da Rede só descreve o grant `password`, mas o sandbox
  aceita `client_credentials` com apenas client_id/secret, e o token vem com o escopo certo. O
  plugin escolhe sozinho; preencha o par só se o time de Integrações tiver enviado.
- `pvs` são os Pontos de Venda. No sandbox existem só dois com dados: `13381369` e `22523510`
  (mais `1254405`, exclusivo da consulta por NSU).
- `base_nsu` é opcional — preencha apenas se `rede_vendas_por_nsu` der 404.

Nunca cole o `client_secret` nem a senha no chat. Detalhes em [docs/credenciais.md](docs/credenciais.md).

## Os três conceitos

Confundir isto é a causa de quase toda resposta errada sobre maquininha:

| Conceito | O que é | Data que manda |
|---|---|---|
| **Venda** | valor bruto da compra, sem MDR | data da venda |
| **Recebível** | o que ainda vai cair, já líquido | data prevista de crédito |
| **Pagamento** | o depósito que caiu, líquido de MDR e débitos | data do repasse |

Débito cai em D+1, crédito em D+30, parcelado em 30/60/90. Venda e pagamento quase nunca estão no
mesmo período — e a conciliação entre eles passa pela cadeia
`venda → ordem de crédito → pagamento`, ligada pelo `saleSummaryNumber`. A tool `rede_conciliar`
faz esse cruzamento e o fatiamento de janelas sozinha.

## Ambientes

| Ambiente | Base da API |
|---|---|
| `sandbox` | `https://rl7-sandbox-api.useredecloud.com.br` |
| `producao` | `https://api.userede.com.br/redelabs` |

Credencial de um ambiente não funciona no outro, e a Rede exige homologar no sandbox antes de
liberar produção. Cada ambiente guarda o próprio token.

> **Retomando o trabalho?** [STATUS.md](STATUS.md) diz o que está pronto, o que falta e quais
> armadilhas já foram pagas. Para usar na conta real: [docs/producao.md](docs/producao.md).

## Estado da validação

Testado contra o sandbox real da Rede em 2026-09-20: login, tradução de códigos, paginação por
cursor, fallback de versão e as rotas de vendas, vendas parceladas, pagamentos, ordens de crédito e
débitos respondendo com dado real. O sandbox **não habilita** recebíveis, bloqueios, resumos de
venda nem a v2 de vendas (403), e suas fixtures de venda e de ordem de crédito são independentes —
por isso o cruzamento da conciliação é provado contra a API simulada. Detalhes em
[docs/testes.md](docs/testes.md).

## Desenvolvimento

```bash
cd server && npm install && npm run build   # gera servers/rede-mcp.js
node test/run.mjs                           # 54 testes offline
node test/integracao.mjs                    # 65 testes contra a API simulada
```

## Payment Link (mapeada, não implementada)

A Rede tem uma segunda API, de **Link de Pagamento**: cria uma página de cobrança hospedada por ela
(cartão em até 12x ou PIX). São três operações — criar, consultar e cancelar — e ela **cria cobrança
real**, ao contrário de tudo que este plugin faz hoje.

Foi levantada e testada no sandbox em 2026-09-20 (um link real foi criado), mas **não virou tool**:
o destino natural dela é um workflow n8n disparado pelo CRM, não uma conversa. Tudo o que é preciso
para implementar — endpoints, payload, regras, armadilhas e o que está quebrado no sandbox — está em
[docs/payment-link.md](docs/payment-link.md), com o swagger oficial em
[docs/referencia/](docs/referencia/payment-link-swagger.json).

Exige credencial de um projeto do pacote *Payment Link*, que é **outra** do que este plugin usa.

## Documentação

- [STATUS.md](STATUS.md) — o que está pronto, o que falta, decisões tomadas
- [docs/producao.md](docs/producao.md) — como obter credenciais de produção e liberar os PVs
- [docs/payment-link.md](docs/payment-link.md) — a API de Link de Pagamento, mapeada e testada
- [docs/ferramentas.md](docs/ferramentas.md) — as 29 tools, uma a uma
- [docs/credenciais.md](docs/credenciais.md) — como obter e onde guardar
- [docs/testes.md](docs/testes.md) — o que é testado e o que só dá para testar com credencial real
- [skills/rede/references/endpoints.md](skills/rede/references/endpoints.md) — mapa tool → rota
- [skills/rede/references/dominios.md](skills/rede/references/dominios.md) — tabelas de código
