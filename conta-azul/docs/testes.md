# Testes e evals

## Testes do servidor (45 casos)

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
Desde a 0.1.1 também cobrem: categoria pelo rateio (desconto não entra), atraso pela data, `somente_vencidas` e caixa
somando só as baixas do período.

## Evals da skill (skill-creator)

`evals/evals.json`: 5 casos com dados fictícios da Beauty Smile (hoje = 2026-09-20). Cada caso roda com a skill e
sem a skill, por subagentes que só acessam a Conta Azul pela CLI `evals/harness/ca.mjs` (servidor real + API simulada).
A nota vem do log de chamadas à API (nenhuma escrita pode sair) e da resposta final.

| Iteração | O que mudou | Resultado |
|---|---|---|
| 1 (0.1.0) | 5 casos, com skill × sem skill | 16/16 × 16/16. A skill foi 29% mais rápida. As regras também estão nas descrições das tools. |
| 2 (0.1.1) | +2 casos da conta real (status de atraso defasado, desconto no rateio) e regressão dos 5 | 22/22 com a skill nova. Nos casos novos, a skill antiga também acertou (a correção está no servidor), mas precisou do dobro de chamadas. |
| 3 (0.1.1) | Caixa com parcela paga em partes ao longo de meses | 6/6. Skill nova com 3 chamadas × 13 da antiga. Somar `pago` daria R$ 43.300 em vez de R$ 23.300. |

Os detalhes de cada iteração estão em `evals/benchmark-iteracao-N.md`.

```bash
cd evals/harness && ln -sf ../../server/node_modules node_modules
CA_RUN_DIR=/tmp/run1 node ca.mjs list
CA_RUN_DIR=/tmp/run1 CA_ESCRITA=1 node ca.mjs contaazul_resumo_financeiro '{"de":"2026-09-01","ate":"2026-09-30"}'
```
