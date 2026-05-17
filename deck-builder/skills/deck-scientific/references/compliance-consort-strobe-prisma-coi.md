# Compliance scientific — CONSORT / STROBE / PRISMA / CARE + COI

> Reporting guidelines obrigatorios + declaracao de conflito de interesse. 3 tiers (🔴/🟡/✅) — D7.

## Mapa tipo-de-estudo → reporting guideline

| Tipo de estudo (X2) | Guideline | Site |
|---------------------|-----------|------|
| RCT (Randomized Controlled Trial) | **CONSORT** 2010 | consort-statement.org |
| Cohort / case-control / cross-sectional | **STROBE** | strobe-statement.org |
| Systematic review / meta-analise | **PRISMA** 2020 | prisma-statement.org |
| Case report / case series | **CARE** | care-statement.org |
| Diagnostic accuracy | **STARD** | equator-network.org/reporting-guidelines/stard |
| Animal preclinical | **ARRIVE** 2.0 | arriveguidelines.org |
| Qualitative | **COREQ** ou **SRQR** | equator-network.org |
| Health economic | **CHEERS** | ispor.org/cheers |

**Regra:** se X2 nao mapeia em nenhum, consultar EQUATOR Network (equator-network.org).

## Por que citar reporting guideline

- **Reproducibilidade** — outros pesquisadores conseguem replicar
- **Peer-review** — editores cobram a checklist preenchida
- **Compliance ICMJE** — Vancouver group exige
- **Compliance de congresso** — AAOMS / ICOI / IADR aceitam abstracts com guideline citada

## Como citar em apresentacao

### Modo oral (oral-short / oral-long / keynote)

Slide de Methods inclui linha:
> "Reported per CONSORT 2010 (Schulz et al., BMJ 2010). Checklist disponivel via OSF: osf.io/abc123"

### Modo poster

Painel inferior esquerdo (Methods small) inclui linha:
> "STROBE-compliant. Full checklist: QR code rodape."

## COI — Conflito de interesse

### Categorias declaraveis

- **Financeiro direto** — salario, honorario palestra, royalty
- **Equity** — acoes/stock options da industria
- **Consultoria** — pagamento por advisory board
- **Patente** — inventor de tecnologia relacionada
- **Financiamento de pesquisa** — grant da industria para o estudo
- **Autoria** — livro/curso pago sobre o tema
- **Pessoal** — parente trabalha na industria

### Como declarar

**Sempre slide 1 da apresentacao** — independente de ter COI ou nao.

Formato sugerido:

Com COI:
> "COI: Dr. Costa Neto e consultor pago da Fotona Inc. e recebeu financiamento de pesquisa Fotona/Beauty Smile."

Sem COI:
> "COI: Nenhum a declarar."

**Aplicacao no poster:** rodape, junto com references e acknowledgments.

## p-value reportado corretamente

### 🔴 BLOCKER patterns

- **"p<0.05" sem effect size** — significancia sem magnitude e meio dado
- **"p=0.06 indicou tendencia significativa"** — p-value nao tem "tendencia"; ou e significante pelo threshold pre-registrado ou nao e
- **"p=NS (nao significativo)"** — reportar p exato + IC95%; "NS" e ambiguo
- **Multiplos testes sem correcao** — se >5 outcomes testados, aplicar Bonferroni / Holm / FDR e citar

### ✅ Padrao correto

```
Outcome primario: reducao profundidade bolsa periimplantar
  - Effect size (mean difference): -1.8 mm
  - IC95%: -2.3 a -1.3 mm
  - p < 0.001
  - n = 142 (grupo Er:YAG) vs n = 138 (controle)
  - GRADE: Moderate
  - Reporting per CONSORT 2010
```

### Erro tipo II (poder estatistico)

Se outcome primario nao-significativo:
- Reportar **poder estatistico** calculado
- Discutir se estudo foi subdimensionado
- Citar effect size detectavel com poder atual

Exemplo:
> "Poder = 0.65 para detectar diferenca de 10% (alpha=0.05). Estudo subdimensionado; meta-analise futura pode reverter conclusao."

## Cherry-picking (selecao seletiva)

### 🔴 BLOCKER

- Apresentar so outcome favoravel quando ha outcomes negativos relevantes
- Subgrupo analysis post-hoc apresentada como pre-especificada
- "Per protocol analysis" mascarando intencao de tratar
- Funnel plot ausente em meta-analise (esconde vies de publicacao)

### ✅ Como evitar

- Outcome primario sempre apresentado, mesmo se negativo
- Outcomes secundarios em tabela densa (Tufte) com todos os resultados
- Pre-registro (OSF / ClinicalTrials.gov / PROSPERO) citado em Methods
- Funnel plot + Egger's test em meta-analise

## Checklist 🔴/🟡/✅ aplicada no output

Bloco final do STORYBOARD ou POSTER:

```markdown
## Compliance & Disclaimers (3 tiers — D7)

🔴 Issues bloqueantes:
- [se aplicavel] {ex: "Slide 5 reporta p<0.05 sem effect size — adicionar IC95%"}
- [se aplicavel] {ex: "COI Fotona nao declarado slide 1"}

🟡 Verificar antes:
- [se aplicavel] {ex: "PRISMA flow diagram presente em apendice?"}
- [se aplicavel] {ex: "Funnel plot incluido em apendice?"}
- [se aplicavel] {ex: "Erro tipo II discutido (poder=0.65)?"}

✅ OK:
- COI declarado slide 1
- GRADE moderate citado outcome primario
- Reporting per CONSORT 2010 (slide Methods)
- p-value com IC95% + effect size + n
- Outcomes secundarios em tabela densa (nao cherry-picking)
```

## Cross-refs

- GRADE detalhado → `framework-imrad-grade.md` (secao GRADE)
- COI no slide 1 — regra inviolavel do SKILL.md
- NB2 cientifico (101 sources) cobre CONSORT/STROBE/PRISMA/CARE + GRADE
