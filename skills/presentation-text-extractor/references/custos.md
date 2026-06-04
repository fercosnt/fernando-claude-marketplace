# Custos — calculo detalhado

## Premissas

- PNG 1568px no lado longo (cap de Claude vision)
- Resolucao tipica = ~1334-1568 tokens de imagem
- Output OCR ~ 500 tokens (texto extraido + estrutura markdown)

## Custo por imagem (USD)

| Modelo | Input (1334 tokens img) | Output (~500 tokens) | Total/imagem |
|---|---|---|---|
| Haiku 4.5 | $0.0013 | $0.0025 | **~$0.004** |
| Sonnet 4.6 | $0.0040 | $0.0075 | **~$0.012** |

Apple Vision: **$0.00** sempre (roda local).

## Custo por deck (30 slides, 5 imagens embarcadas)

| Cenario | Engine | Total |
|---|---|---|
| 100% texto extraivel + Apple Vision em imagens | Apple Vision | **$0.00** |
| Hibrido: 25 slides texto + 5 imagens OCR Haiku | Apple + Haiku | **~$0.020** |
| Hibrido: laser-physics (fórmulas detectadas) | Apple + Sonnet | **~$0.060** |
| Vision-only Haiku (`--force-ocr`) | Claude Haiku | **~$0.120** |
| Vision-only Sonnet (`--force-ocr --model sonnet`) | Claude Sonnet | **~$0.360** |

## Custo mensal estimado (volume Fernando)

Premissa: 15-20 decks/mes.

| Mix tipico | Custo/mes |
|---|---|
| 70% texto + 30% hibrido Haiku | **~$0.50** |
| 50% texto + 50% hibrido Haiku/Sonnet | **~$0.80** |
| Misto com 30% laser-physics (Sonnet) | **~$1.20** |

Range esperado: **$0.50 - $1.50/mes**.

## Hard cap (`--max-cost`)

Default: `$0.10/deck`.

Aborta antes de executar se a estimativa do passo 2 (Plano) exceder. Justificativa:
- Deck tipico (30 slides hibrido) cabe em $0.06 com Sonnet
- $0.10 da folga para decks de 50-60 slides
- Se voce esta fazendo `--force-ocr` ou processando deck de 100+ slides, eleve o limite explicitamente: `--max-cost 0.30`

Em modo `--batch`, o limite aplica **por arquivo** (nao para o lote inteiro). Lote com 12 PDFs e `--max-cost 0.10` pode gastar ate $1.20 total.

## Como auditar o gasto

A skill loga 3 numeros relevantes em stderr:

```
[2/4] Plano de extracao:
  ...
  TOTAL                                      ~$0.052          <-- estimativa
  Limite (--max-cost): $0.100  OK

[4/4] Gravando markdown...
  Custo real: $0.048 (estimado: $0.052)                       <-- real
  Output: ./deck.md
```

E grava no frontmatter do `.md` final:

```yaml
custo_real_usd: 0.048
```

Para auditoria mensal:

```bash
grep "^custo_real_usd:" ~/Downloads/decks/*.md | awk -F'[: ]+' '{sum += $2} END {print "Total: $" sum}'
```

## Calibracao do estimador

A funcao `PageDecision.estimated_cost_usd()` em [router.py](../scripts/router.py) usa as constantes:

```python
per_haiku_image = 0.0008    # input cap + output ~200 tok
per_sonnet_image = 0.005    # input cap + output ~500 tok
per_haiku_full_page = 0.005
per_sonnet_full_page = 0.012
```

Atualizar quando precos da API Anthropic mudarem. Em [stack.md](stack.md) ha a tabela mais recente da pesquisa.

## Reduzindo custo

Se voce processa volume alto:

1. **Use `--engine apple`** se a maior parte dos seus decks e PT-BR de texto simples (sem formulas). Custo cai pra zero, qualidade um pouco menor.
2. **Use `--model haiku`** sempre (mesmo em laser-physics). Custo cai 3x mas formulas LaTeX podem sair imperfeitas.
3. **`--max-cost 0.05`** para ser conservador e abortar antes de gastar em decks anomalos.
4. **Prompt caching** (futuro v1.1): chamadas Claude com mesmo system prompt fazem cache (90% off no input). Implementar se virar bottleneck.
