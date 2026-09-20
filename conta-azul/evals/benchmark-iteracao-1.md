# Skill Benchmark: conta-azul

**Model**: <model-name>
**Date**: 2026-09-20T03:57:12Z
**Evals**: 1, 2, 3, 4, 5 (3 runs each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% ± 0% | 100% ± 0% | +0.00 |
| Time | 42.8s ± 8.4s | 60.3s ± 36.5s | -17.6s |
| Tokens | 80869 ± 4056 | 86698 ± 6768 | -5829 |
## Leitura

- As 16 assercoes passaram nas duas configuracoes: nesta bateria elas nao distinguem uma da outra. As regras que a skill ensina (criterio de data, previa antes de escrever, checar parcela quitada) tambem estao nas descricoes das tools e nas instrucoes do servidor MCP, entao o modelo acerta mesmo sem a skill.
- A seguranca de escrita vem do servidor, nao da skill: no eval 4 o baseline chamou contaazul_baixar_parcela sem 'confirmar' e o servidor devolveu so a previa. Nenhuma das 10 execucoes enviou escrita a API.
- Onde a skill fez diferenca foi na eficiencia: -29% de tempo e -7% de tokens em media. No eval 5, sem a skill, o modelo fez 26 chamadas (6 com erro, a maioria filtro sem vencimento, que e obrigatorio) contra 8 com a skill, levando 84s contra 56s.
- Proxima iteracao: casos mais dificeis, que as tools sozinhas nao resolvem (rateio em varias categorias, periodo com mais de 10 mil parcelas, reconexao apos invalid_refresh_token).
