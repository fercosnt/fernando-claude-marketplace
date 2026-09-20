# Testes e evals

## Testes do servidor (39 casos)

API Conta Azul simulada (`test/mock.mjs`), servidor real via MCP stdio:

```bash
cd server && npm install && npm run build
cd ../test && ln -sf ../server/node_modules node_modules && node run.mjs
```

Cobrem: configuração ausente ou com placeholder, link OAuth (host e scope oficiais), `state` forjado ou reutilizado,
token com permissão 600, paginação de 1234 parcelas, datas `DD/MM/AAAA` normalizadas, janelas de 15 dias da NFS-e,
nova tentativa em 429, **dois servidores renovando ao mesmo tempo (uma só renovação)**, renovação após 401,
refresh morto com mensagem útil, escrita desligada, prévia sem envio, soma de parcelas, POST com 500 **não** repetido,
checagem de CPF duplicado, versão da parcela no PATCH e nenhum segredo no `contaazul_status`.

## Evals da skill (skill-creator)

`evals/evals.json`: 5 casos com dados fictícios da Beauty Smile (hoje = 2026-09-20). Cada caso roda com a skill e
sem a skill, por subagentes que só acessam a Conta Azul pela CLI `evals/harness/ca.mjs` (servidor real + API simulada).
A nota vem do log de chamadas à API (nenhuma escrita pode sair) e da resposta final.

Resultado da iteração 1: `evals/benchmark-iteracao-1.md`.

```bash
cd evals/harness && ln -sf ../../server/node_modules node_modules
CA_RUN_DIR=/tmp/run1 node ca.mjs list
CA_RUN_DIR=/tmp/run1 CA_ESCRITA=1 node ca.mjs contaazul_resumo_financeiro '{"de":"2026-09-01","ate":"2026-09-30"}'
```
