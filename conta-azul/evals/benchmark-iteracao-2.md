# Skill Benchmark: conta-azul

**Model**: <model-name>
**Date**: 2026-09-20T04:45:08Z
**Evals**: 1, 2, 3, 4, 5, 6, 7 (3 runs each per configuration)

## Summary

| Metric | With Skill | Old Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% ± 0% | 100% ± 0% | +0.00 |
| Time | 45.3s ± 12.6s | 47.0s ± 19.0s | -1.6s |
| Tokens | 82465 ± 4754 | 86656 ± 9080 | -4192 |
## Leitura

- Iteracao 2 (plugin 0.1.1): regressao dos 5 casos com a skill nova — 16/16 assercoes. Dois casos novos vindos do teste com a conta real: status ATRASADO defasado na busca (eval 6) e receita por categoria com desconto no rateio (eval 7).
- Skill nova x skill antiga nos casos novos: 6/6 x 6/6. As correcoes estao no SERVIDOR (vencido pela data, categoria pelo rateio), entao ate a skill antiga acerta. A skill nova chegou ao mesmo resultado com metade das chamadas (eval 6: 2 x 4; eval 7: 5 x 10) e 32% menos tempo no eval 7 (41s x 60s).
- Nenhuma das 9 execucoes enviou escrita a API.
- A comparacao com skill x skill antiga nos evals 1-5 nao foi rodada; a comparacao com e sem skill desses casos esta na iteracao 1.
