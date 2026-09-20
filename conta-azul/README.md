# conta-azul

Plugin para usar o ERP **Conta Azul** (API v2) no Claude Code e no Cowork. O MCP roda **na sua máquina**:
credenciais e tokens nunca saem do seu computador e não passam por serviço de terceiros.

**Versão 0.1.1.** Pergunte em português, como "como está o financeiro de setembro?", "o que vence essa semana?" ou
"quanto temos em conta hoje?". O Claude consulta a API e responde com número real.

## O que vem no plugin

| Componente | O que faz |
|---|---|
| **Servidor MCP** (38 tools) | **Leitura:** resumo financeiro do período, contas a receber e a pagar, parcelas e baixas, saldos, categorias, DRE, centros de custo, transferências, vendas, orçamentos, contratos, pessoas, produtos, serviços, NF-e, NFS-e, GET genérico. **Escrita opcional:** lançamentos, baixas, alterar parcela, pessoas, vendas, cobranças. Ver [docs/ferramentas.md](docs/ferramentas.md) |
| **Skill `conta-azul`** | Qual tool responde cada pergunta e como ler o número (competência × vencimento × pagamento) |
| **Skill `conta-azul-setup`** | Configura credenciais e conecta a empresa sem segredo no chat |
| **Skill `conta-azul-escrita`** | Liga e desliga a escrita |

## Instalação

**Claude Code:**

```bash
/plugin marketplace add fercosnt/fernando-claude-marketplace
/plugin install conta-azul@fernando-claude-marketplace
```

**Cowork (Claude Desktop):** Settings → Plugins → marketplace `fercosnt/fernando-claude-marketplace` → `conta-azul`.

Reinicie o Claude e diga "configura a Conta Azul" (ou `/conta-azul-setup`).

Requisito: Node 18 ou superior. O servidor é um único arquivo, sem dependências para instalar.

## Credenciais: onde colocar

No arquivo **`~/.conta-azul-mcp.json`**, no seu Mac (permissão 600):

```json
{
  "escrita": false,
  "client_id": "...",
  "client_secret": "...",
  "redirect_uri": "exatamente a URL cadastrada no Portal",
  "empresas": [ { "nome": "Beauty Smile" } ]
}
```

Os três valores vêm do Portal do Desenvolvedor → Minhas aplicações → aplicação de **Produção**.
Os tokens o servidor grava sozinho em `~/.conta-azul-mcp/tokens/`. Detalhes, conexão e troca de computador estão em
[docs/credenciais.md](docs/credenciais.md).

## Segurança

- **Leitura sempre; escrita desligada por padrão.** Com a escrita ligada, toda alteração tem dois passos:
  primeiro a prévia (`confirmar=false`, nada é enviado), depois o envio (`confirmar=true`), que só acontece com o
  seu ok. A trava fica no servidor, não depende do modelo lembrar.
- Escritas **nunca** são repetidas automaticamente, porque a API não é idempotente.
- Credenciais e tokens com permissão 600. `contaazul_status` não expõe segredo.

## O detalhe que quebra integrações com a Conta Azul

O `refresh_token` é **rotativo**: cada renovação invalida o anterior. Se dois processos renovam ao mesmo tempo
(Claude Desktop e Claude Code abertos), um recebe `invalid_grant` e a conexão cai. O servidor grava o token novo
antes de usá-lo (escrita atômica) e usa uma trava de arquivo para que só um processo renove por vez. Isso foi testado
com dois servidores simultâneos.

## Validação

- **Estrutura:** `claude plugin validate` passou.
- **Servidor:** 45 testes contra uma API simulada.
- **API real:** conectada e consultada na conta da Beauty Smile em 20/09/2026. As três correções da 0.1.1 saíram
  desse teste (ver [CHANGELOG.md](CHANGELOG.md)).
- **Skill:** 3 iterações de evals do skill-creator, 7 casos, 100% de acerto. Com a skill, o modelo chega à resposta
  com metade das chamadas de API em relação à skill antiga ou a nenhuma skill.

Detalhes em [docs/testes.md](docs/testes.md) e `evals/benchmark-iteracao-*.md`.

## Estrutura

```
conta-azul/
├── .claude-plugin/plugin.json
├── .mcp.json                     # sobe servers/conta-azul-mcp.js via node
├── servers/conta-azul-mcp.js     # bundle pronto (gerado de server/src)
├── server/src/                   # fonte TypeScript: auth, client, tools
├── skills/conta-azul/            # skill principal + references/endpoints.md
├── skills/conta-azul-setup/
├── skills/conta-azul-escrita/
├── docs/                         # credenciais, ferramentas, testes
├── evals/                        # evals.json, harness, benchmark
└── test/                         # testes do servidor + API simulada
```

## Desenvolvimento

```bash
cd server && npm install && npm run build   # gera servers/conta-azul-mcp.js
cd ../test && ln -sf ../server/node_modules node_modules && node run.mjs
```

Variáveis para teste: `CONTAAZUL_CONFIG_FILE`, `CONTAAZUL_STATE_DIR`, `CONTAAZUL_BASE_URL`, `CONTAAZUL_TOKEN_URL`,
`CONTAAZUL_AUTHORIZE_URL`, `CONTAAZUL_ESCRITA=X`.

## Fontes

- OpenAPI oficiais em developers.contaazul.com (changelog até 2026-09-15). Os endpoints estão em
  `skills/conta-azul/references/endpoints.md`.
- Armadilhas mapeadas por github.com/augustotecnos/claude-skill-conta-azul. Aquela skill ainda usa os endereços
  antigos de OAuth: a Conta Azul mudou para `login.contaazul.com` e `api-v2.contaazul.com/oauth/token` em agosto
  de 2026.
