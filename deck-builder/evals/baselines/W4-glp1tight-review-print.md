# W4 — GLP1TIGHT v4 · baseline de regressao do `deck-review-print`

> **Nao e um STORYBOARD.** E o registro do resultado de uma execucao real da skill
> `deck-review-print`, usado como baseline de regressao. O
> `lint-storyboard-schema.sh` **nao se aplica a este arquivo** — ele valida apenas
> fixtures de storyboard (W1-W3 + BAD).

| | |
|---|---|
| **Origem** | Canva `DAHKNdTNVwI` — GLP1TIGHT®_Apresentacaov4 |
| **Marca** | Fotona |
| **Dimensoes** | 17 slides, 1920x1080 |
| **Executado em** | 2026-08-12, modo `revisao` |
| **Piloto manual anterior** | 2026-08-10 — 6 paginas / 16,8% TAC (contava 3 tabelas) |

## Baseline — o que uma execucao correta produz

| Metrica | Valor | Tolerancia |
|---------|-------|-----------|
| Entradas no dossie | **17** (01..17) | exato — D18 |
| Paginas do PDF | **7** | <= 7 |
| TAC medio do dossie | **17,1%** | <= 25% |
| TAC medio do original | **193%** | +/- 3 p.p. |
| Produto original (pag x cobertura) | 3.281 | referencia |
| Produto do dossie | 120 | referencia |
| Reducao | **~27x** | >= 20x |
| Tabelas transcritas | **4** | exato |
| Divergencias aritmeticas | **1** | exato |
| Slides sem nenhum pixel | **1** (slide 10) | exato |

## TAC por slide do original — metrica de tinta, NAO classificador (D24)

| Slide | TAC | Slide | TAC | Slide | TAC |
|-------|-----|-------|-----|-------|-----|
| 01 | 224% | 07 | 261% | 13 | 256% |
| 02 | 261% | 08 | 253% | 14 | 222% |
| 03 | 191% | 09 | 37% | 15 | 266% |
| 04 | 66% | 10 | 65% | 16 | 25% |
| 05 | 266% | 11 | 270% | 17 | 273% |
| 06 | 89% | 12 | 257% | — | — |

**Mediana 253% · P75-P25 = 173 p.p. · media 193%**

> Este deck e a evidencia que derrubou as duas primeiras versoes do D24. Fotos
> medem **65%** (slide 10) e **273%** (slide 17); conteudo mede **37%** (slide 09)
> e **266%** (slide 05). O TAC nao separa em direcao nenhuma. Qualquer versao
> futura da skill que volte a classificar por TAC falha este fixture.

## Classificacao de referencia

| Tipo | Slides |
|------|--------|
| `conteudo` | 02, 04, 05, 06, 09, 16 |
| `tabela` | **07**, 12, 13, 15 |
| `foto` | 03, 08, 10, 11 |
| `misto` | 01, 14, 17 |

O slide **07** e comparativo em duas colunas e **conta como tabela** — o Apendice B
do PRD nao o contava, por isso o piloto registrou 3 e a execucao real achou 4.

## Divergencia aritmetica conhecida — slide 13

Linha *Massa muscular (StarFormer)*, programa masculino:

```
celulas:  8X  8X  6X  2X  2X  2X   soma = 28
total declarado:                          27X
```

As colunas fecham em 68 e o total geral esta correto; so a celula de total da
linha diverge. Somando os totais de linha da 67, nao 68.

**Comportamento esperado:** marcar `[DIVERGE: soma da linha = 28, total declarado
= 27X]`, **transcrever 27X** (o valor do slide), e comunicar explicitamente. O
dossie reproduz o original, nao o corrige.

**Controles de falso positivo:**

- Slide 12 (feminino) fecha nos dois eixos: 6+9+5+6+6+36 = 68 · 14+14+14+9+8+9 = 68
- Slide 15 (financeiro) fecha nas colunas derivadas: 180k x 4 = 720k · 720k x 12 = 8,64M

## Privacidade — slide 10

Grade de antes/depois de pacientes reais. Em modo `revisao` entra como moldura
tracejada, **sem nenhum pixel**, mantendo o numero 10 (D18 + RNF-06, CFO 196/2019
e LGPD). Uma execucao que reproduza a imagem falha este fixture.

## Divergencia entre deck e storyboard

O deck escreve **"ATP Reboost"** (slides 12 e 13); o storyboard registra
*"ATP Rebound"*. Um dos dois esta errado — registrado, nao resolvido.

## Como reproduzir

```bash
# 1) dependencias
./scripts/check-print-deps.sh          # espera NUCLEO OK

# 2) skill, com o MCP do Canva conectado
/deck-review-print https://www.canva.com/d/zuGnNQqRyXwQNs2

# 3) medicao
./.venv/bin/python scripts/measure-tac.py "$DECKS_DIR"/*/DOSSIE-glp1tight-*.pdf
```

## Falhas que este fixture pega

1. Classificacao voltar a depender de TAC (D24)
2. Perder o slide 07 na contagem de tabelas
3. Nao detectar a divergencia do slide 13 (checklist nao executado)
4. Reproduzir a imagem de paciente do slide 10 (RNF-06)
5. Renumerar ou compactar entradas (D18)
6. Reportar TAC sem a ressalva metodologica
7. Passar de 7 paginas ou de 25% TAC medio
