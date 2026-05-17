# Fundraising Deck Checklist

Checklist final aplicado pelo `deck-fundraising` antes de finalizar o STORYBOARD. Tambem usado pelo `deck-reviewer` como referencia de qualidade.

## Estrutura

- [ ] STORYBOARD bate com schema §10.2 (SHARED.md)
- [ ] Numero correto de slides para o modo:
  - `padrao`: 12-15 slides
  - `sponsorship`: 10 + 3-4 (bloco contrapartidas)
  - `demo-day`: 7-8 slides
- [ ] `## Meta` completo (objetivo, audiencia, duracao, formato, Big Idea, marca, modo, framework, ID)
- [ ] `max_ctas: 1` no Meta (regra padrao global, sem override pra fundraising)
- [ ] Storyboard ID com slug + timestamp

## Narrativa (Sequoia + Raskin)

- [ ] Slide 1 (Capa): hook curto, NAO produto, NAO mission statement vago
- [ ] Slide 2 (Problema): Big Change in the world — NUNCA comeca com produto/solucao
- [ ] Slide 3 (Comparativo): Winners & Losers explicitos com exemplo concreto
- [ ] Slide 4 (Conceitual): **Big Idea (U5) verbatim ou ≥70% overlap** como Promised Land
- [ ] Slide 5 (Demo): produto como Magic Gift (ferramenta), NAO lista de features
- [ ] Slide 6 (Why Now): 2-3 tailwinds com fonte
- [ ] Slide 7 (Mercado): **TAM bottom-up** (N clientes × ticket × frequencia) — NUNCA top-down
- [ ] Slide 8 (Business Model): unit economics (LTV/CAC/payback) — Kupor/a16z desde seed
- [ ] Slide 9 (Tracao): 3 numeros principais em destaque + 1 case
- [ ] Slide 11 (Equipe): responde "por que ESSE time" com insight de dominio, NAO currículo
- [ ] Slide 12 (Ask): tripartido — valor + uso 3-buckets com % + timeline com milestone

## Action titles

- [ ] Todos os slides tem action title (NAO titulo descritivo tipo "Mercado")
- [ ] Action title e frase declarativa de 5-9 palavras
- [ ] Action titles formam narrativa linear (horizontal logic test)
- [ ] 1 ideia por slide (NAO 3 bullet points concorrentes)

## Ask (slide critico — NUNCA vago)

- [ ] Valor + estrutura clara (R$X em SAFE/equity/CCB com cap/discount/maturity)
- [ ] Uso de capital com % em 3-4 buckets (ex: Produto 40% / GTM 35% / G&A 25%)
- [ ] Timeline com milestone explicito (12-24m ate X)
- [ ] Milestone destrava algo concreto (proxima rodada / breakeven / atingir M&A)

## Compliance & Disclaimers

- [ ] Disclaimer slide separado (penultimo ou ultimo) com texto canonico
- [ ] Footnote "Projecoes; ver disclaimer" em slides com numeros futuros
- [ ] NDA mencionado se "confidencial" reclamado
- [ ] Auto-detect marca aplicada (Beauty Smile/Fotona/Carnaval 360)
- [ ] Compliance tags da marca injetadas:
  - Beauty Smile → `odontologia-br`, `cfo-cfm` (footnote em claims clinicos)
  - Fotona → `anvisa-laser-classe-iii`, `cfo-laser` (slide produto com numero RDC + responsavel tecnico)
  - Carnaval 360 → `[]` (sem compliance regulatorio)
- [ ] Se sponsorship cultural → numero PRONAC + Lei 8.313/91 ou estadual/municipal citados

## Image prompts (whitelist D5)

Slides com `**Prompt de imagem:**` preenchido (deck-image-prompts invocada):
- [ ] Slide 1 (capa)
- [ ] Slide 2 (problema)
- [ ] Slide 3 (comparativo)
- [ ] Slide 4 (conceitual/Promised Land)
- [ ] Slide 5 (demo)
- [ ] Slide 9 (prova-social) — tracao
- [ ] Slide 11 (equipe) — variant prova-social com retratos

Slides com `**Prompt de imagem:** —` (skip default):
- [ ] Slide 6 (dados — Why Now)
- [ ] Slide 7 (dados — TAM)
- [ ] Slide 8 (financeiro)
- [ ] Slide 10 (dados — roadmap)
- [ ] Slide 12 (CTA)
- [ ] Slide 13 (disclaimer)

## Anti-padroes (BLOQUEAR — 🔴)

- [ ] **NAO** tem "Retorno garantido" ou similar
- [ ] **NAO** tem "Nao temos concorrentes" + magic quadrant onde startup e #1
- [ ] **NAO** tem slide de exit (red flag Hunter Walk no seed)
- [ ] **NAO** tem vanity metrics (downloads/MAUs) sem MRR/receita
- [ ] **NAO** tem hockey stick sem mecanismo explicado
- [ ] **NAO** tem produto no slide 1 (inverte ordem narrativa vencedora)
- [ ] **NAO** tem team slide currículo-only
- [ ] **NAO** tem TAM top-down ("1% de R$1tri")

## Para modo `padrao` especifico

- [ ] 13 slides (12-15 OK)
- [ ] Sequoia + Raskin overlay completo
- [ ] Slide 4 = Promised Land com Big Idea
- [ ] Slide 9 = Evidence com tracao real (F3)

## Para modo `sponsorship` especifico

- [ ] 10 + bloco contrapartida (3-4 slides extras)
- [ ] Big Idea = visao do EVENTO (nao do patrocinador)
- [ ] Slide niveis com 4 tiers (bronze/silver/gold/master) + valores
- [ ] Slide contrapartidas master detalhado (4-6 contrapartidas concretas)
- [ ] Slide ROI patrocinador com metodologia explicita
- [ ] Ask com mecanismo fiscal (Rouanet se cultural)
- [ ] Disclaimer Rouanet com PRONAC + Lei especifica

## Para modo `demo-day` especifico

- [ ] 7-8 slides totais
- [ ] Tempo total ≤ 3-5min (somar tempo estimado por slide)
- [ ] Big Idea sandwich (slide 1 + frase final CTA)
- [ ] Tracao no slide 4 (early, antes de equipe)
- [ ] Ask tripartido condensado

## Output final

- [ ] Path correto: `$DECKS_DIR/{YYYY-MM}/STORYBOARD-{slug}-{HHmm}.md`
- [ ] Slug max 30 chars kebab-case
- [ ] Versao explicita (v1, v2 se revisao)
- [ ] Apendice opcional listado (competitive landscape, financial model, cap table)
- [ ] Storyboard de Imagens (handoff `deck-image-prompts`) preenchido
- [ ] Checklist de Revisao (handoff `deck-reviewer`) anotado
- [ ] Compliance & Disclaimers (3 tiers 🔴/🟡/✅) preenchido

## Validacao final

Antes de devolver para usuario:
1. Re-ler slide 12 (Ask) — tripartido?
2. Re-ler slide 4 — Big Idea presente verbatim?
3. Re-ler slide 7 — TAM bottom-up?
4. Slide disclaimer presente?
5. Compliance tags aplicadas?
6. Action titles em todos os slides?

Se qualquer "nao" → voltar e corrigir antes de finalizar.
