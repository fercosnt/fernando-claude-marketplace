---
name: deck-reviewer
description: Revisa STORYBOARD de deck com 4 criticos adversariais (clareza/persuasao/SUCCESs Heath/VERIFICAR auditor v1.2) e gera issues BLOCKER/MAJOR/MINOR. Use ao pedir "/deck review", "revisa esse deck", "vamos criticar storyboard".
intent: action
effort: medium
nb_ids:
  - 7f1b2e2b-4ba4-40de-ba56-ca2f55e2c0da
references:
  - references/critico-clareza.md
  - references/critico-persuasao.md
  - references/critico-success-heath.md
  - references/critico-verificar.md
  - references/severidades-categoricas.md
assets:
  - assets/templates/review-skeleton.md
  - evals/reviewer-cases.md
---

# deck-reviewer

Skill auxiliar do plugin `deck-builder`. Revisa um STORYBOARD-{slug}-{HHmm}.md gerado por qualquer skill `deck-{vertical}` e devolve um relatorio paralelo `.review.md` com issues classificadas por severidade categorica.

> **Opt-in.** NAO roda automaticamente. NAO bloqueia geracao. Roda quando usuario explicitamente pede.

## Quando ativa

- `/deck review {path}` (com ou sem path — autodetecta ultimo STORYBOARD)
- "revisa esse deck", "vamos criticar", "manda critica nesse storyboard"
- Apos `deck-{vertical}` gerar um STORYBOARD em deck de alta consequencia (sugerir; nao executar sozinha)

## Fronteiras (LOCKED — SHARED.md §10.8)

- NAO reescreve o STORYBOARD original (gera arquivo paralelo `.review.md`)
- NAO emite score numerico 1-10 (D9 — risco "LLM rating theater")
- NAO gera slides finais (PPTX/Gamma/Figma) — so o review markdown
- NAO substitui revisao humana especializada (compliance juridica/clinica ainda precisa de profissional)
- NAO chama APIs pagas

## Output: arquivo paralelo (NUNCA sobrescreve original)

Para STORYBOARD em `$DECKS_DIR/2026-05/STORYBOARD-beauty-smile-anjo-1647.md`, o review vai em:

```
$DECKS_DIR/2026-05/STORYBOARD-beauty-smile-anjo-1647.review.md
```

Regra: mesmo diretorio, mesmo basename, sufixo `.review.md` antes da extensao. Se o arquivo `.review.md` ja existe, NAO sobrescrever — cria `.review-v2.md`, `.review-v3.md`, etc.

## Schema do output (v1.2 — 4 criticos)

Renderiza usando [assets/templates/review-skeleton.md](assets/templates/review-skeleton.md).

```markdown
# Review: {nome-deck}

## Meta
- STORYBOARD revisado: {basename original} (versao vN)
- Reviewer rodado em: {ISO date}
- Criticos aplicados: clareza + persuasao + SUCCESs + VERIFICAR (v1.2)
- max_ctas (lido da Meta): {N — default 1; teaching 4; scientific 3}
- modo_entrega (lido da Meta): {apresentado-ao-vivo | enviado-para-leitura | hibrido}
- [VERIFICAR] flags detectadas: {N total — {X 🔴} {Y 🟡} {Z 🟢}}

## Issues por severidade

### 🔴 BLOCKER (resolver ANTES de apresentar)
- **Slide N — Tipo:** {problema concreto e especifico}
  Sugestao: {acao concreta — texto reescrito, slide a adicionar, etc.}

### 🟡 MAJOR (resolver se sobrar tempo)
- ...

### 🟢 MINOR (pular se urgente)
- ...

## Audit [VERIFICAR] flags (Critico 4 — v1.2)

> Listagem dedicada das marcacoes [VERIFICAR: ...] encontradas no STORYBOARD,
> classificadas por slide afetado. Detalhes: references/critico-verificar.md.

🔴 BLOCKER — dados decisores nao podem ir sem confirmacao:
- **Slide N (tipo):** "{texto da flag}" → Sugestao: {acao concreta}
- ...

🟡 MAJOR — resolver antes de apresentar:
- ...

🟢 MINOR — resolver se sobrar tempo:
- ...

Total: {N} flags ({X 🔴} / {Y 🟡} / {Z 🟢})

## Recommended next action
{Uma frase considerando os 4 criticos: "Pronto pra ensaio" | "Resolver N blocker(s) antes de apresentar" | "Confirmar N dado(s) com fonte antes" | "Re-rodar deck-{vertical} v2 com correcoes"}
```

**NAO emitir:** score numerico (1-10, A-F, percentual, estrelas). D9 — captura sinal espurio. Severidades categoricas + recommended action sao suficientes.

## Workflow (4 passes sequenciais — v1.2)

```
1. PARSE        Le STORYBOARD + extrai Meta (vertical, max_ctas, modo_entrega, slides)
2. CRITICO 1    Clareza               → ver references/critico-clareza.md
3. CRITICO 2    Persuasao (/copy)     → ver references/critico-persuasao.md
4. CRITICO 3    SUCCESs (Heath)       → ver references/critico-success-heath.md
5. CRITICO 4    VERIFICAR auditor     → ver references/critico-verificar.md (v1.2)
6. CONSOLIDA    Agrega issues, classifica severidade, ordena por slide
7. ESCREVE      Renderiza review-skeleton.md no path paralelo (com bloco Audit [VERIFICAR])
```

Cada critico roda em sequencia (nao paralelo — eles compartilham contexto e o segundo precisa ver issues do primeiro pra nao duplicar). Critico 4 e independente dos outros 3 (so escaneia o STORYBOARD por marcacoes [VERIFICAR:]) mas roda no fim para usar contexto consolidado na classificacao de severidade.

### 1. Parse do STORYBOARD

Le o markdown e extrai:

| Campo | De onde |
|-------|---------|
| `nome_deck` | Linha `# Deck: ...` |
| `vertical` | `Skill geradora: deck-{vertical}` na Meta |
| `objetivo` | `Objetivo unico:` na Meta |
| `big_idea` | `Big Idea:` na Meta |
| `max_ctas` | `max_ctas:` na Meta — **se ausente, deriva da vertical** (ver §max_ctas abaixo) |
| `versao` | `Versao: vN` |
| `slides[]` | Cada bloco `## Slide N — Tipo` com seus campos |
| `checklist_revisao` | `## Checklist de Revisao` (pistas do que o deck declarou checar) |
| `compliance_section` | `## Compliance & Disclaimers` |

Se algum campo obrigatorio faltar (vertical, big_idea, slides), gera `🔴 BLOCKER: STORYBOARD malformado` e para. NAO chuta valores.

### 2. Pass 1 — Critico 1 (Clareza)

Le `references/critico-clareza.md` e aplica TODAS as checagens (action titles, 1 ideia/slide, horizontal logic, max_ctas, tempo balanceado). Para cada falha, registra:

```python
issue = {
  "slide_n": 4,
  "tipo_slide": "problema",
  "critico": "clareza",
  "severidade": "🟡",     # ver references/severidades-categoricas.md
  "problema": "Action title fraco: 'Mercado endodontia' nao afirma nada",
  "sugestao": "Reescrever para: 'Mercado de endodontia premium cresce 12%/ano com TAM R$2.4bi'"
}
```

### 3. Pass 2 — Critico 2 (Persuasao — invoca `/copy`)

Le `references/critico-persuasao.md`. Para o slide 1 (capa/abertura) E para o slide CTA, **invoca `/copy`** em modo de critica/refinamento. Ver §integracao-copy.

### 4. Pass 3 — Critico 3 (SUCCESs Heath)

Le `references/critico-success-heath.md` e aplica filtro SUCCESs (Simple/Unexpected/Concrete/Credible/Emotional/Stories) ao deck inteiro como narrativa, NAO slide-a-slide.

### 5. Pass 4 — Critico 4 (VERIFICAR Auditor — v1.2)

Le `references/critico-verificar.md`. Escaneia o STORYBOARD inteiro procurando padrao `[VERIFICAR:.*\]`:

```bash
grep -nE '\[VERIFICAR:[^]]+\]' "$STORYBOARD"
```

Para cada match:

1. Identifica `slide_n` (procura `## Slide N` mais proximo antes do match)
2. Identifica `tipo_slide` (procura `**Tipo:** X` ou `Tipo: X` mais proximo)
3. Extrai `texto_flag` (string entre `[VERIFICAR:` e `]`)
4. Classifica severidade segundo `references/critico-verificar.md` §classificacao:

| Tipo do slide | Severidade |
|---------------|------------|
| `CTA` / `disclaimer` | **🔴 BLOCKER** (decisor nao pode ir sem confirmacao) |
| `compliance` | **🔴 BLOCKER** |
| `dados` / `financeiro` / `prova-social` | **🟡 MAJOR** |
| `problema` / `comparativo` (com numero quantitativo) | **🟡 MAJOR** |
| `equipe` / `conceitual` / `contexto` / `capa` | **🟢 MINOR** |
| `apendice` / Storyboard de Imagens / Compliance & Disclaimers blocks | (ignorado — ja flagado pelo proprio bloco) |

5. Gera issue:

```python
flag = {
  "slide_n": 2,
  "tipo_slide": "problema",
  "critico": "verificar",
  "severidade": "🟡",
  "texto_flag": "fonte CFO ou ABO",
  "problema": "Dado fabricado sem fonte conferida (slide problema = gancho do deck)",
  "sugestao": "Confirmar fonte oficial CFO/ABO antes de apresentar — slide 2 e ponto escrutinado por anjo"
}
```

6. **Output bloco dedicado** `## Audit [VERIFICAR] flags` no review.md (alem de aparecer no bloco geral de severidade).

**Por que separar:** flags `[VERIFICAR]` vao para o bloco geral de severidade (🔴/🟡/🟢) E para o bloco dedicado `## Audit [VERIFICAR]`. Bloco dedicado da visibilidade clara de "todos os pontos que precisam confirmacao antes de apresentar" — util para usuario fazer auditoria sistematica.

**Se 0 flags encontradas:** bloco vira `## Audit [VERIFICAR] flags\n\nNenhuma flag encontrada. Verificar se skill geradora aplicou disciplina v1.1 (`shared/verificar-flag.md`).` — sinal de que dados podem estar over-claimed sem flag.

### 6. Consolidacao

- Deduplica issues que 2 criticos levantaram (mantem severidade mais alta)
- Ordena: 🔴 primeiro, depois 🟡, depois 🟢; dentro de cada bucket por numero de slide
- Calcula recommended action (regra abaixo)

### 7. Renderizacao

Usa `assets/templates/review-skeleton.md`, substitui placeholders, grava em `{path-paralelo}.review.md`. Em v1.2 o template inclui:

- Meta com `Criticos aplicados: clareza + persuasao + SUCCESs + VERIFICAR (v1.2)`
- Meta com `[VERIFICAR] flags detectadas: N (X 🔴 / Y 🟡 / Z 🟢)`
- Bloco `## Audit [VERIFICAR] flags` dedicado apos `## Issues por severidade`
- Recommended next action considerando os 4 criticos (ex: "Resolver 2 blockers + confirmar 18 dados antes de apresentar")

## Regra `max_ctas` com override por vertical (D14)

| Vertical | Default `max_ctas` | Override permitido? |
|----------|---:|---|
| fundraising | 1 | declarar `max_ctas: N` na Meta com justificativa |
| sales | 1 | declarar `max_ctas: N` na Meta |
| clinical | 1 | declarar na Meta |
| equipment | 1 | declarar na Meta |
| proposal | 1 | declarar na Meta |
| internal | 1 | declarar na Meta |
| **teaching** | **4** | objetivos pedagogicos multiplos (pratica + leitura + quiz + caso) |
| **scientific** | **3** | read paper / replicate / contact author |

**Algoritmo:**

```
1. Le `max_ctas` da Meta. Se ausente, usa default da tabela acima.
2. Conta slides do tipo `CTA` no STORYBOARD.
3. Se count > max_ctas:
     - Severidade: 🟡 MAJOR (NAO 🔴 — pode ser intencional)
     - Sugestao: "Reduzir para {max_ctas} CTAs OU aumentar `max_ctas: N` na Meta com justificativa"
4. Se count = 0 em vertical com CTA esperado (fundraising/sales/proposal):
     - Severidade: 🔴 BLOCKER
     - Sugestao especifica por vertical (ex: "Adicionar slide 'Ask' com valuation + ticket + timeline")
```

## Integracao com `/copy` (graceful fallback)

O Critico 2 (persuasao) chama `/copy` em sub-prompt para revisar:

1. **Hook do slide 1** (capa ou primeira frase impactante)
2. **CTA do slide final** (texto da chamada-a-acao)

### Detecao se `/copy` esta instalada

Antes de invocar:

```bash
ls ~/.claude/skills/copy/SKILL.md 2>/dev/null && echo "AVAILABLE" || echo "MISSING"
```

(Em Cowork Desktop, checar tambem `~/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/.../skills/copy/SKILL.md`.)

### Modo COM `/copy` instalada

Para o slide 1 e CTA, invoca `/copy` em modo critica:

```
/copy duvida Esse hook do slide 1 funciona pra audiencia {U2} com objetivo {U1}? Big Idea: {big_idea}. Hook atual: "{texto}". Devolva: (a) diagnostico em 2 linhas; (b) 2 variantes alternativas se hook fraco; (c) veredito mantem/ajusta/troca.
```

O resultado de `/copy` vira **insumo** das issues do reviewer — NAO sao incluidos verbatim no output, mas alimentam a `Sugestao:` do issue.

### Modo SEM `/copy` (graceful fallback)

Se `/copy` ausente, o Critico 2 NAO falha — degrada com warning na Meta do review:

```markdown
## Meta
...
- Criticos aplicados: clareza + persuasao (heuristico — /copy indisponivel) + SUCCESs
```

E aplica heuristica embutida em `references/critico-persuasao.md` §fallback (checa: hook tem numero/contraste/pergunta retorica? CTA tem verbo + objeto + prazo?). Resultado e menos refinado mas funcional.

## Consulta NB1 (transversal)

NB1 (`7f1b2e2b-4ba4-40de-ba56-ca2f55e2c0da`) cobre canonicos de critica: Resonate (Duarte), Made to Stick (Heath), Pitch Anything (Klaff), Story (Raskin).

Quando consultar:
- Critico 3 (SUCCESs) precisa de exemplos canonicos do framework Heath
- Critico 1 (clareza) precisa de criterios "action title" do Duarte/McKinsey

Como consultar (§10.6 SHARED.md):

```bash
notebooklm use 7f1b2e2b-4ba4-40de-ba56-ca2f55e2c0da
notebooklm ask "Critica de action titles vs titulos descritivos em pitch decks — quais sinais de fraqueza segundo Duarte/McKinsey? Big Idea do deck: {big_idea}" --max-citations 5
```

Falha de NB NAO bloqueia o review (degrada com warning).

## Recommended next action (regra de selecao — v1.2)

Considerando issues + flags `[VERIFICAR]` agregados dos 4 criticos:

| Situacao | Frase |
|----------|-------|
| 0 🔴 e 0 🟡 e 0 [VERIFICAR] | "Pronto pra ensaio." |
| 0 🔴 e 0 🟡 e 1+ [VERIFICAR] 🟡/🟢 | "Pronto pra ensaio apos confirmar {N} dado(s) com fonte." |
| 0 🔴 e 1-2 🟡 | "Resolver {N} major(es) antes de polir." |
| 0 🔴 e 3+ 🟡 | "Varias melhorias importantes — recomendado v2 antes de apresentar." |
| 1 🔴 (qualquer critico) | "Resolver 1 blocker antes de apresentar." |
| 2-3 🔴 | "Resolver {N} blockers — re-revisao apos correcao." |
| 1+ 🔴 do Critico 4 (VERIFICAR em CTA/disclaimer) | "Resolver {N} blocker(s) E confirmar dado(s) decisor(es) com fonte antes de apresentar." |
| 4+ 🔴 | "Re-rodar deck-{vertical} v2 — deck atual nao deve ser apresentado." |

🟢 minor NAO entra na decisao da recommended action.

**Caso especial:** se total `[VERIFICAR]` ≥ 10 E nenhuma e 🔴, ainda assim recomendar `"Confirmar {N} dados com fonte antes de apresentar — alta densidade de inferencias"` mesmo se issues clareza/persuasao/SUCCESs estiverem OK.

## Eval cases (v1.2 — 5 cases)

5 cases canonicos em [evals/reviewer-cases.md](evals/reviewer-cases.md):

1. Fundraising sem ask → 🔴 BLOCKER (CTA inexistente)
2. Clinical com promessa de cura → 🔴 BLOCKER (compliance CFO 196/2019)
3. Teaching 4h sem hands-on → 🟡 MAJOR (Andragogy violation; CTAs OK porque max=4)
4. Scientific oral-long com 4 CTAs → 🟡 MAJOR (excede max_ctas=3)
5. **(v1.2)** Beauty Smile pitch anjo v1.1 com 25 [VERIFICAR] flags → 2-3 🔴 (CTA SAFE structure, disclaimer Res. CVM 160/22, etc.) + 15-20 🟡 (problema 40%, NPS 91 metodologia, papers GRADE, etc.) + ~5 🟢 (bios equipe, nomes internacionais)

DoD §13.6 exige 3+ passando. Alvo v1.2: 5/5.

## DoD especifico (v1.2)

- Frontmatter §10.7 com `intent: action`, `effort: medium`, NB1 listado
- **5 eval cases passando** (v1.2 — case 5 e [VERIFICAR] auditor sobre W1 v1.1)
- **4 criticos como passes sequenciais** (clareza → persuasao → SUCCESs → VERIFICAR)
- `/copy` invocado para hook + CTA do Critico 2, com graceful fallback
- `max_ctas` lido da Meta com defaults por vertical (D14)
- **`modo_entrega` lido da Meta** (v1.1+) — registrado no review
- **Critico 4 (VERIFICAR) detecta padrao `[VERIFICAR:.*\]` + classifica severidade por tipo de slide**
- **Bloco `## Audit [VERIFICAR] flags` dedicado** no output do review (alem das issues por severidade)
- Output `STORYBOARD-{slug}-{HHmm}.review.md` paralelo (NUNCA sobrescreve)
- SEM score numerico — apenas 🔴🟡🟢 + recommended action
- Instalada em `~/.claude/skills/deck-reviewer/` + Cowork Desktop skills-plugin

## Referencias

- [critico-clareza.md](references/critico-clareza.md) — action titles + 1 ideia/slide + horizontal logic + max_ctas
- [critico-persuasao.md](references/critico-persuasao.md) — hook + CTA via `/copy` + fallback heuristico
- [critico-success-heath.md](references/critico-success-heath.md) — SUCCESs filter
- [critico-verificar.md](references/critico-verificar.md) — **(v1.2)** [VERIFICAR] auditor + classificacao severidade por tipo de slide
- [severidades-categoricas.md](references/severidades-categoricas.md) — guia de classificacao 🔴🟡🟢 por vertical
- [assets/templates/review-skeleton.md](assets/templates/review-skeleton.md) — template do output
- [evals/reviewer-cases.md](evals/reviewer-cases.md) — 5 eval cases (v1.2)
- [../../shared/verificar-flag.md](../../shared/verificar-flag.md) — disciplina anti-fabricacao v1.1
