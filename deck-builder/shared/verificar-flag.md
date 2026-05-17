# §10.9 [VERIFICAR] Flag — Disciplina anti-fabricação (v1.1)

> Contrato LOCKED v1.1 — todas as 8 skills verticais + auxiliares aplicam esta disciplina ao gerar STORYBOARD.

## Problema que isto resolve

LLMs (incluindo Opus 4.7) inventam números específicos e citações de papers com alta plausibilidade quando o STORYBOARD pede dados concretos. Exemplos reais observados nos walkthroughs v1.0:

- `40% das clinicas dentais premium em SP fecharam` — número plausível, sem fonte real, citado como CFO/ABO
- `Genova 2023`, `Tonetti 2024`, `ICOI consensus 2024` — papers fabricados que soam reais
- `NPS 91, n=131` — combinação plausível sem auditoria
- `GRADE moderate em RCTs piloto Er:YAG clareamento` — over-claiming da evidência real

Sem disciplina, o STORYBOARD vai pro designer / Gamma / PowerPoint com números que parecem auditados mas não são. **Risco para Fernando:** apresentar com claim que um revisor cuidadoso pode derrubar.

## Regra LOCKED v1.1

**Todo dado específico fabricado ou não-conferido pela skill DEVE ser marcado `[VERIFICAR: descrição]` ao lado.**

### Padrões que disparam obrigação de flag

| Padrão | Exemplo |
|--------|---------|
| Valor monetário com unidade | `R$500k`, `R$180k/mes`, `US$1M` |
| Percentual específico | `40% das clinicas`, `90% retencao`, `NPS 91` |
| Tamanho de amostra | `n=131`, `247 pacientes ativos` |
| Citação a paper / source | `Genova 2023`, `RCT Tonetti 2024`, `CFO 2024`, `IBGE PNAD 2024` |
| Score de evidência | `GRADE moderate`, `GRADE high para outcome X` |
| Margem / unit economics | `margem operacional 34%`, `LTV/CAC 8.3x` |
| Numero regulatório | `CFO Res. 196/2019`, `Anvisa Classe III nº 80312770005` |

### O que NÃO precisa flag

- Frameworks bem estabelecidos (Sequoia, Raskin, Pyramid Minto, Bloom, Andragogy)
- Nomes próprios genéricos (Beauty Smile, Fotona, LightWalker — auto-detect §10.5)
- Termos clínicos canônicos (Er:YAG, Nd:YAG, All-on-4, dosimetria, fluence)
- Valores fornecidos pelo usuário durante a entrevista (esses são responsabilidade do usuário)
- Numeração de slides, tempos de fala, quantidade de bullets (metadados estruturais)

## Como aplicar

### Opção 1 — Inline (preferido)

```markdown
Action title: Em 5 anos, 40% das clinicas dentais premium em SP fecharam [VERIFICAR: fonte CFO ou ABO]
```

### Opção 2 — Footnote

```markdown
Action title: NPS 91, n=131 [VERIFICAR: metodologia Bain padrao, calculo proprio Q1-Q3 2026]
```

### Opção 3 — Bloco de speaker notes

```markdown
Speaker notes: ... NPS 91 (autoreporte, metodologia Bain padrao, n=131 respondentes Jan-Mar 2026) [VERIFICAR: confirmar n + datas + metodologia documentada]
```

## O que o reviewer (`deck-reviewer`) faz com flags

`deck-reviewer` no segundo passe:

1. **Lista todos os `[VERIFICAR]` encontrados** no bloco final `🟡 Verificar antes`.
2. **Classifica severidade:**
   - Se número aparece em slide CTA / Ask / Compliance → eleva pra `🔴 BLOQUEANTE` (dado decisor não pode ir sem auditoria).
   - Demais → `🟡 VERIFICAR` (resolver antes de apresentar mas não bloqueia geração).
3. **Sugere ação concreta:**
   - "Slide N (action title) — confirmar fonte X antes de apresentar".

## O que o lint script faz

`lint-storyboard-schema.sh` v1.1:

1. Conta linhas com padrões suspeitos (R$/%/n=/RCT/NPS/GRADE/CFO/Anvisa).
2. Conta marcações `[VERIFICAR`.
3. Se `suspect_data ≥ 5` E `verified_flags = 0` → emite **WARN** (não FAIL — humano avalia).
4. Se `verified_flags ≥ 1` → emite **PASS** confirmando que skills aplicaram disciplina.

## Boa prática para skills verticais

Quando gerar STORYBOARD e estiver tentado a inventar um número específico, perguntar:

1. **O usuário forneceu este dado durante a entrevista?** → SIM = usar como está, sem flag.
2. **É um dado público canonicamente conhecido (ex: IBGE, CFO publicado)?** → SIM = citar fonte específica explicitamente, sem flag.
3. **É um número que parece plausível mas a skill está inferindo / extrapolando?** → SIM = inventar SE o tipo de slide exige (problema, prova-social), mas **marcar com `[VERIFICAR]`** explicitando o que precisa ser conferido.
4. **É um claim regulatório (CFO, CFM, Anvisa, GRADE)?** → SIM = sempre flag, mesmo que aparente confiança. Regulatorios mudam; melhor confirmar.

## Cross-references

- `storyboard-schema.md` — regra 9 (`[VERIFICAR]` em dados fabricados)
- `entrevista-universal-u1-u6.md` — dados fornecidos pelo usuário ficam isentos de flag
- `../scripts/lint-storyboard-schema.sh` — WARN automático quando flag está ausente
- `../skills/deck-reviewer/SKILL.md` — converte flags em 🟡 ou 🔴 no review pass
