# evals/baselines — registros de execucao real

Diferente de `evals/fixtures/`, que guarda **fixtures de STORYBOARD** validadas por
`scripts/lint-storyboard-schema.sh`, este diretorio guarda **baselines de execucao**:
o resultado medido de rodar uma skill sobre um caso real, usado para detectar
regressao.

**Por que em diretorio separado:** o linter de storyboard casa com `W*.md`. Um
baseline de `deck-review-print` colocado em `fixtures/` era capturado pelo glob e
reportado como FAIL, mudando o resultado do guardrail de 3 para 4 arquivos. Sao
tipos de artefato diferentes e nao devem dividir o mesmo diretorio.

| Arquivo | Skill | O que registra |
|---------|-------|----------------|
| `W4-glp1tight-review-print.md` | `deck-review-print` | 17 slides -> 7 paginas, 193% -> 17,1% TAC, 4 tabelas, 1 divergencia |
