# IMRAD + GRADE — framework principal

> Coluna vertebral de TODOS os modos do `deck-scientific`. IMRAD organiza a narrativa; GRADE qualifica a evidencia.

## IMRAD (Introduction → Methods → Results → Discussion)

Estrutura canonica do paper cientifico, adaptada para apresentacao.

### Introduction (Por que importa?)

3 movimentos (Swales' CARS — Create A Research Space):
1. **Establish the territory** — contexto + relevancia clinica
2. **Establish the niche** — gap na literatura
3. **Occupy the niche** — research question / hipotese / objetivo

Aplicacao por modo:
- `oral-short` → 1 slide (60s) com 3 frases (uma por movimento)
- `oral-long` → 3 slides (background / gap / research question)
- `keynote` → Ato 1 inteiro (10-12 min)
- `poster` → Painel esquerdo (2-3 paragrafos)

### Methods (Como foi feito?)

Componentes obrigatorios (mais reproducibilidade = melhor):
- **Design** — RCT / cohort / case-control / cross-sectional / case series / case report / systematic review / meta-analise
- **Sample** — n, criterios inclusao/exclusao, recrutamento, calculo de poder
- **Interventions / Exposicoes** — descricao operacional reproduzivel
- **Outcomes** — primario operacionalizado + secundarios; tempo de seguimento
- **Analise estatistica** — testes, software, controle de confundimento
- **Reporting guideline** citado (CONSORT/STROBE/PRISMA/CARE conforme tipo)
- **Ethics approval** — comite + numero

Aplicacao por modo:
- `oral-short` → 1 slide (60s) — design + sample + outcome + analise (uma frase cada)
- `oral-long` → 4 slides expandidos
- `keynote` → 1 slide methods por estudo apresentado (no Ato 2)
- `poster` → Painel inferior esquerdo (small, conciso)

### Results (O que aconteceu?)

Regras:
- **Numeros sempre com unidade e denominador** — "40% (n=20/50)" e nao "40%"
- **p-value contextualizado** — junto com effect size e IC95%
- **Tabelas e figuras autossuficientes** — legenda completa, sem precisar do texto
- **Tufte aplicado** — data-ink ratio alto, sem chartjunk (ver `framework-tufte-doumont.md`)
- **Multiplos outcomes** → tabela ou small multiples; nunca slide separado para cada

Aplicacao por modo:
- `oral-short` → 2 slides (1 figura/tabela por slide, 90-120s total)
- `oral-long` → 4 slides
- `keynote` → 2-3 slides results por estudo apresentado
- `poster` → Painel direito (1-2 figuras + tabela)

### Discussion (E daí?)

4 movimentos:
1. **Restatement** — recapitular achado principal em 1 frase
2. **Comparison** — comparacao com literatura existente
3. **Limitations** — internas (viés, confundimento) + externas (generalizabilidade)
4. **Implications** — significado clinico + proximos passos

**Erro tipo II** — se outcome primario nao-significativo, discutir poder estatistico (ex: "poder = 0.65 para detectar diferenca de 10%; estudo subdimensionado").

Aplicacao por modo:
- `oral-short` → 1 slide discussion + 1 slide limitacoes/futuro
- `oral-long` → 3 slides
- `keynote` → Ato 3 inteiro (8-10 min)
- `poster` → Painel inferior direito + rodape

## GRADE — qualificacao da evidencia

GRADE classifica a qualidade da evidencia em 4 niveis:

| Nivel | Significado |
|-------|-------------|
| **High** | Confianca alta — improvavel que pesquisa futura mude a estimativa |
| **Moderate** | Confianca moderada — pesquisa futura pode mudar a estimativa |
| **Low** | Confianca baixa — pesquisa futura provavelmente mudara a estimativa |
| **Very Low** | Qualquer estimativa e altamente incerta |

### Como aplicar em apresentacao

- **Cada outcome ganha um GRADE level explicito** — nao so o primario
- **Razao do downgrade** quando aplicavel (risco de vies / inconsistencia / indireto / imprecisao / vies de publicacao)
- **Razao do upgrade** quando aplicavel (efeito grande / gradiente dose-resposta / confundimento residual oposto ao efeito)

### Exemplo (slide Results)

```
Outcome primario: reducao profundidade bolsa periimplantar
  - Effect size: -1.8 mm (IC95% -2.3 a -1.3)
  - p < 0.001
  - GRADE: Moderate
  - Downgrade: risco de vies (alocacao nao-cega em 3/8 estudos)
```

### GRADE por tipo de estudo (ponto de partida)

| Tipo de estudo | GRADE inicial |
|----------------|---------------|
| RCT | High |
| Cohort / case-control | Low |
| Case series / case report | Very Low |
| Meta-analise | herda do nivel mais baixo dos estudos incluidos |

A partir do ponto de partida, sobe ou desce conforme criterios GRADE.

## Cross-refs

- Tufte / Doumont aplicado em Results → `framework-tufte-doumont.md`
- Reporting guidelines (CONSORT/STROBE/PRISMA/CARE) → `compliance-consort-strobe-prisma-coi.md`
- NB2 Densas (101 sources cientificos) — pasta `apresentacoes-cientificas-congressos-saude`
