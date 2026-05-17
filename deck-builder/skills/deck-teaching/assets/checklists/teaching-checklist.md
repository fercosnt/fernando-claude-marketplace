# Teaching Checklist — auto-validacao deck-teaching

Aplicar APOS gerar STORYBOARD, ANTES de handoff pra deck-reviewer. Cobre os 3 modos.

---

## Universal (3 modos)

- [ ] Frontmatter SKILL.md com `intent: action`, `effort: high`, NB1
- [ ] Schema §10.2 do SHARED.md valido
- [ ] Meta declara `Modo: aula-tecnica | workshop-hands-on | keynote-inspirational`
- [ ] Meta declara `Verbo Bloom alvo:` (lembrar | compreender | aplicar | analisar | avaliar | criar)
- [ ] Meta declara `max_ctas: N` explicitamente (4 para aula/workshop, 1 para keynote)
- [ ] Slide 2 lista objetivos com verbo Bloom em **CAIXA ALTA** no inicio de cada bullet
- [ ] Action titles assertivos (NAO titulos descritivos do tipo "Sobre fluence")
- [ ] 1 ideia por slide (Mayer coerencia)
- [ ] Speaker notes EXPANDEM o slide, NAO repetem (Mayer redundancia)
- [ ] Visual brief evita stock cliche (handoff pra deck-image-prompts ja barra)
- [ ] Marca auto-detectada e cross-skill invocado quando aplicavel

---

## Modo `aula-tecnica` (specific)

- [ ] Slide 3 = pre-avaliacao rapida (T3 diagnostico)
- [ ] **Cada chunk ≤7min** (Mayer segmentacao) — listar chunks e somar tempo
- [ ] Cada chunk tem retrieval practice no final (quiz formativo, pause-and-discuss, ou pergunta retorica)
- [ ] Numero de chunks ≈ duracao / 7min, arredondado pra cima
- [ ] Hands-on contado (T4) e estruturado: tempo + materiais + criterio de sucesso observavel
- [ ] Avaliacao somativa final (T5)
- [ ] **4 CTAs** com tags [PRATICA] [LEITURA] [QUIZ] [PROXIMO] — confirma `max_ctas: 4`
- [ ] **SEM Sparkline Duarte** (proibido em aula tecnica)
- [ ] Cross-skill Fotona → `laser-physics` invocado para formulas

---

## Modo `workshop-hands-on` (specific)

- [ ] Slide 3 = pre-avaliacao + agenda visivel (reduz ansiedade Knowles)
- [ ] **3-4 modulos conceituais** alternados com **minimo 2 hands-on** (T4 ≥ 2)
- [ ] Cada hands-on estruturado: briefing + execucao + debrief
- [ ] Hands-on com tempo + materiais + criterio de sucesso observavel
- [ ] Worksheets impressos referenciados em apendice (NAO produzidos pela skill)
- [ ] Caso integrador no final (T5)
- [ ] **4 CTAs** com tags [APLICAR] [LEITURA] [FECHAR CASO] [PROXIMO] — confirma `max_ctas: 4`
- [ ] **SEM Sparkline Duarte**
- [ ] Andragogy: casos reais + auto-direcao nos CTAs

---

## Modo `keynote-inspirational` (specific)

- [ ] **Sparkline Duarte detectado**: capa+BigIdea → contexto → promessa → tensao 1 → resolucao 1 → tensao 2 → resolucao 2 → BigIdea reforcada → call
- [ ] **Big Idea no slide 1 e no slide penultimo com frase IDENTICA** (verbatim)
- [ ] Big Idea destilada em 1 frase poetica (se ocupa mais que 1 linha, NAO esta destilada — iterar)
- [ ] Verbo Bloom AVALIAR no slide 2 (ou raramente compreender/lembrar; aplicar/criar nao cabem em keynote)
- [ ] **`max_ctas: 1` declarado na Meta** (override do default teaching=4)
- [ ] 1 UNICO CTA provocativo (decisao de identidade, NAO acao operacional)
- [ ] **SEM chunks ≤7min** (Sparkline ignora segmentacao Mayer)
- [ ] SEM hands-on, SEM quiz, SEM pre-avaliacao
- [ ] Tom narrativo nas speaker notes (NAO didatico)
- [ ] Style anchor consistente em toda serie de imagens (brand consistency)
- [ ] Resolucao 2 NAO e pitch de produto (se for, vira deck-sales — refazer com vertical correta)
- [ ] Slides totais 12-20

---

## Falhas comuns

| Falha | Diagnostico | Correcao |
|-------|-------------|----------|
| Slide 2 sem verbo Bloom | Backwards Design quebrado — sem objetivo mensuravel | Reescrever cada bullet iniciando com verbo (LEMBRAR/COMPREENDER/APLICAR/ANALISAR/AVALIAR/CRIAR) |
| Aula tecnica com chunk de 12min | Violacao Mayer segmentacao | Quebrar em 2 chunks de 6min com retrieval practice no meio |
| Workshop sem hands-on (T4=0) | NAO e workshop, e aula longa | Mudar modo para `aula-tecnica` OU adicionar minimo 2 hands-on |
| Keynote com 4 CTAs | Confusao com default teaching | Cortar para 1 CTA provocativo; mover outros pra apendice ou deletar |
| Keynote com chunks ≤7min | Modo errado — Sparkline NAO segmenta | Remover marcacao de chunks; reorganizar em arco Sparkline |
| Aula tecnica com Sparkline | Modo errado — Sparkline so em keynote | Remover Sparkline; usar Backwards Design + Bloom + Mayer |
| Big Idea longa em keynote | Nao destilada | Oferecer 3 versoes curtas e poeticas, usuario escolhe |
| Resolucao 2 do keynote vira pitch | NAO e keynote — e venda | Refazer com `deck-sales` ou ajustar tom pra insight/perspectiva |

---

## Handoff pra deck-reviewer

Apos checklist passar, output do reviewer deve cobrir:
- max_ctas validado (4 ou 1 conforme modo)
- Verbo Bloom slide 2 ✓
- Modo-especifico: chunks ≤7min (aula) | hands-on contado (workshop) | Sparkline detectado (keynote)
- Action titles ✓
- 1 ideia/slide ✓
- Horizontal logic ✓
