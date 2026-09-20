# Skill Benchmark: conta-azul

**Model**: <model-name>
**Date**: 2026-09-20T04:50:21Z
**Evals**: 1, 5 (3 runs each per configuration)

## Summary

| Metric | Old Skill | With Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% ± 0% | 100% ± 0% | +0.00 |
| Time | 62.0s ± 0.0s | 45.8s ± 17.1s | +16.2s |
| Tokens | 83385 ± 0 | 88390 ± 5218 | -5004 |
## Leitura

- Iteracao 3: caixa pelas baixas. Caso novo: parcela antiga paga em partes (R$ 30 mil acumulados, R$ 10 mil em setembro), o mesmo padrao encontrado na conta real.
- Skill nova e skill antiga chegaram a R$ 23.300, porque o servidor ja devolve pago_no_periodo_de_pagamento. A skill nova levou 3 chamadas e 34s; a antiga precisou de 13 chamadas e 62s, conferindo parcela por parcela.
- Somar o campo pago da busca daria R$ 43.300, que e o erro que a v0.1.0 cometeria.
