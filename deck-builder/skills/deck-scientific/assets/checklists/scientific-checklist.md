# Scientific checklist — handoff para deck-reviewer

> Anexada ao final do STORYBOARD ou POSTER. Reviewer valida.

## Conformidade estrutural

- [ ] **Frontmatter §10.7** completo (name, description, intent, effort, nb_ids, references, assets)
- [ ] **Modo correto** identificado e bate com output:
  - [ ] `poster` → POSTER.md (D8 schema proprio)
  - [ ] `oral-short` / `oral-long` / `keynote` → STORYBOARD.md (§10.2 schema padrao)
- [ ] **`max_ctas: 3`** declarado na Meta (override scientific — D14)
- [ ] **Big Idea (U5)** aparece no slide 1, ultimo slide (take-home), ou centro do poster

## COI (regra inviolavel — slide 1 sempre)

- [ ] COI declarado slide 1 (modos oral/keynote) OU cabecalho+rodape (modo poster)
- [ ] Se nao ha COI: escrito "Nenhum COI a declarar" (omitir e proibido)
- [ ] Categorias relevantes citadas: financeiro direto / equity / consultoria / patente / financiamento / autoria / pessoal

## Reporting guideline (conforme tipo X2)

| Tipo de estudo (X2) | Guideline obrigatorio | Conferido? |
|---------------------|----------------------|------------|
| RCT | **CONSORT** 2010 | [ ] |
| Cohort / case-control / cross-sectional | **STROBE** | [ ] |
| Systematic review / meta-analise | **PRISMA** 2020 | [ ] |
| Case report / case series | **CARE** | [ ] |
| Diagnostic accuracy | **STARD** | [ ] |
| Animal preclinical | **ARRIVE** 2.0 | [ ] |
| Health economic | **CHEERS** | [ ] |

- [ ] Reporting guideline citado **explicitamente no slide Methods** (oral/keynote) ou painel inferior esquerdo (poster)
- [ ] Checklist completa disponivel via QR/OSF para peer-review

## Estatistica

- [ ] **p-value contextualizado** — NUNCA "p<0.05" solto
  - [ ] Effect size reportado junto
  - [ ] IC95% reportado junto
  - [ ] n reportado junto
- [ ] **GRADE level** explicito no outcome primario (High / Moderate / Low / Very Low)
- [ ] Razao do downgrade/upgrade GRADE citada quando aplicavel
- [ ] Outcomes secundarios tambem ganham GRADE
- [ ] Numeros sempre com **unidade e denominador** ("40% (n=20/50)" e nao "40%")
- [ ] **Erro tipo II discutido** se outcome primario nao-significativo (poder estatistico calculado e citado)
- [ ] Correcao para multiplos testes aplicada e citada se >5 outcomes testados (Bonferroni / Holm / FDR)

## Anti-cherry-picking

- [ ] Outcomes secundarios reportados na integra (sem omitir negativos)
- [ ] Pre-registration citado (OSF / ClinicalTrials.gov / PROSPERO)
- [ ] Funnel plot incluido em apendice (se meta-analise)
- [ ] Egger's test reportado (se meta-analise)
- [ ] Per protocol analysis declarada como tal (nao mascarando ITT)

## Visualizacao (Tufte)

- [ ] **Data-ink ratio alto** — sem gradientes 3D, sem dropshadow, sem chartjunk
- [ ] Sem pizza chart (Tufte)
- [ ] Eixos Y nao truncados sem aviso
- [ ] Cores com mapeamento perceptual (ColorBrewer ou paleta consistente)
- [ ] Legenda autossuficiente em cada figura
- [ ] Small multiples usados quando aplicavel (especialmente keynote multi-estudo)
- [ ] N por grupo explicito nas figuras

## Narrativa (Doumont)

- [ ] **Action titles** (assertivos) em todos os slides — NUNCA titulos descritivos
- [ ] **Tree (agenda visual)** no slide 2 — obrigatorio em oral-long e keynote
- [ ] **Map (voce esta aqui)** em slides de transicao — obrigatorio em keynote
- [ ] **Theorems** (afirmacao + evidencia) — padrao slide cientifico

## CTAs (max 3 — D14 override scientific)

- [ ] **max_ctas = 3** validado (sem extrapolar)
- [ ] CTA 1: Read paper (DOI ou QR code)
- [ ] CTA 2: Replicate (protocolo + dataset/codigo aberto — OSF / Zenodo / Figshare)
- [ ] CTA 3: Contact author (email ou ORCID)

## Image-prompts (D5 override)

**Modos oral/keynote:**
- [ ] **`--include-dados` flag passada** ao invocar `deck-image-prompts`
- [ ] Slides tipo `dados` (graficos cientificos) tem prompt de imagem preenchido
- [ ] Slides tipo `capa`, `conceitual`, `comparativo`, `problema` tem prompt preenchido (whitelist canonica)
- [ ] Slides tipo `CTA`, `disclaimer`, `agradecimento`, `apendice` ficam sem prompt (skip)

**Modo poster:**
- [ ] **`deck-image-prompts` NAO invocada** — figuras do poster sao referencias diretas ao paper

## Compliance bloco 3 tiers (D7)

- [ ] **🔴 Issues bloqueantes** preenchidas (vazio = nenhuma OK)
- [ ] **🟡 Verificar antes** preenchidas (checagens recomendadas)
- [ ] **✅ OK** preenchidas (confirmacoes positivas)

## Output convention

- [ ] Path bate com §10.4: `$DECKS_DIR/{YYYY-MM}/{STORYBOARD|POSTER}-{slug}-{HHmm}.md`
- [ ] Slug kebab-case ≤ 30 chars
- [ ] Versao declarada (v1 inicial)
- [ ] ID unico declarado (`STORYBOARD-{slug}-{YYYYMMDD-HHmm}` ou `POSTER-{slug}-{YYYYMMDD-HHmm}`)

## Modo poster — validacao Better Poster Morrison

(apenas modo `poster`)

- [ ] **Teste de 5 segundos** — key finding centralizado, ≥ 100 pt em A0
- [ ] **Teste de QR code** — link estavel ao paper completo
- [ ] **Teste de COI** — declarado e visivel sem zoom
- [ ] **Teste de GRADE** — outcome primario tem GRADE level explicito na tabela
- [ ] Layout 6 elementos: cabecalho, centro grande, esquerdo, inferior esquerdo, direito, inferior direito, rodape

---

## Como o reviewer usa esta checklist

`deck-reviewer` valida cada item. Output esperado:
- Resumo de itens marcados ✅ / ⚠️ / 🔴
- Detalhe das 🔴 com sugestao de correcao
- Detalhe das 🟡 com checagem recomendada

Skill original (`deck-scientific`) re-gera v2 do output ao receber feedback.
