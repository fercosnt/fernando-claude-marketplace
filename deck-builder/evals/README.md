# Evals — deck-builder plugin

Fixtures sintéticas + lint runner para validar o schema §10.2 do `storyboard-schema.md`.

## Estrutura

```
evals/
├── README.md                                    # este arquivo
└── fixtures/
    ├── W1-beauty-smile-pitch-anjo.md            # walkthrough 1 — deck-fundraising (13 slides)
    ├── W2-aula-eryag-fotona.md                  # walkthrough 2 — deck-teaching (14 slides)
    ├── W3-politica-viagens-ceo.md               # walkthrough 3 — deck-internal (9 slides)
    └── BAD-incomplete-meta.md                   # fixture proposital INVÁLIDA (deve FAIL)
```

## Como rodar

```bash
# Lint nos 3 walkthroughs válidos (deve dar TODOS PASS, exit 0)
./scripts/lint-storyboard-schema.sh evals/fixtures/W*.md

# Lint na fixture inválida (deve dar FAIL, exit 1)
./scripts/lint-storyboard-schema.sh evals/fixtures/BAD-*.md

# Lint em tudo (deve dar 3 PASS + 1 FAIL, exit 1)
./scripts/lint-storyboard-schema.sh evals/fixtures/*.md
```

## Resultado esperado (referência v1.0.0)

| Fixture | Esperado | Validações |
|---------|----------|------------|
| W1-beauty-smile-pitch-anjo.md | PASS | Meta 12/12, 11 tipos distintos, 13 action titles, compliance 3 tiers |
| W2-aula-eryag-fotona.md | PASS | Meta 12/12, 10 tipos distintos, 14 action titles, compliance 3 tiers |
| W3-politica-viagens-ceo.md | PASS | Meta 12/12, 5 tipos distintos, 9 action titles, compliance 3 tiers |
| BAD-incomplete-meta.md | **FAIL** | 8 campos Meta faltando, 1 tipo não-canônico, compliance incompleto |

## Por que fixtures sintéticas (não outputs reais)

O plugin gera `STORYBOARD.md` apenas em resposta a `/deck` no Claude Code/Cowork. Outputs reais variam por sessão (depende das respostas U1-U6 do usuário). Fixtures sintéticas:

1. **Determinísticas** — mesma entrada, mesmo output, lint reproduzível em CI
2. **Cobrem os 3 walkthroughs §12 documentados no README** — não inventam casos
3. **Incluem fixture inválida** para garantir que o lint **detecta** problemas (não só passa silenciosamente)

Cada fixture é uma "amostra de output esperada" que um run real do walkthrough deveria gerar — desvios apontam regressão no schema.

## Cross-references

- `../scripts/lint-storyboard-schema.sh` — runner shell+grep (QA-3)
- `../shared/storyboard-schema.md` — schema canônico §10.2
- `../README.md` — descrição dos 3 walkthroughs
