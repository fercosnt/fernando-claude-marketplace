# Eval cases — deck-teaching

3 casos cobrindo os 3 modos. Usados para validar a skill.

---

## Case 1 — Aula 60min "Dosimetria laser Er:YAG" (modo `aula-tecnica`)

### Input
```
U1: "Dentistas pos-grad calculam fluence Er:YAG para clareamento + descontaminacao"
U2: dentistas pos-graduacao, mix iniciante/intermediario
U3: 60min (escolha 3)
U4: presencial
U5: "Fluence calculada vence o achismo do equipamento"
U6: Fotona (auto-detect via "Er:YAG")
T1: 60min
T2: Bloom APLICAR (calculo dosimetrico)
T3: medio (base laser, sem dosimetria solida)
T4: 2 hands-on (calculo + protocolo simulado)
T5: quiz somativo 8 questoes Bloom-aplicar
```

### Output esperado

STORYBOARD ~45-55 slides com:

- **Meta:** modo `aula-tecnica`, `max_ctas: 4`, verbo Bloom = APLICAR, duracao 60min, chunks totais 8, hands-on totais 2
- **Slide 1:** capa Fotona, Big Idea "Fluence calculada vence o achismo"
- **Slide 2:** objetivos visiveis — 3 bullets iniciando com APLICAR
- **Slide 3:** pre-avaliacao (T3) — 4 perguntas para diagnosticar base
- **Slides 4-8:** Chunk 1 (≤7min) — Fisica do laser Er:YAG (vocabulario: J/cm², spot size, pulse duration)
- **Slide 9:** Quiz formativo chunk 1 (2 perguntas retorica)
- **Slides 10-14:** Chunk 2 (≤7min) — Formula de fluence + variaveis
- **Slide 15:** Quiz formativo chunk 2
- **Slides 16-22:** **Hands-on 1 (15min)** — calcular fluence em 3 casos (cliente faz, instrutor circula)
- **Slides 23-27:** Chunk 3 (≤7min) — Clareamento (parametros recomendados)
- **Slide 28:** Quiz formativo chunk 3
- **Slides 29-33:** Chunk 4 (≤7min) — Descontaminacao endodontica (parametros)
- **Slide 34:** Quiz formativo chunk 4
- **Slides 35-42:** **Hands-on 2 (15min)** — montar protocolo completo para caso simulado
- **Slides 43-46:** Chunk 5 — Casos clinicos comentados (3 casos reais)
- **Slides 47-48:** Quiz somativo final (T5 — 8 questoes)
- **Slides 49-50:** CTAs (4 — override D14 max_ctas:4):
  1. Leitura: paper recomendado sobre dosimetria
  2. Quiz online: link para banco de 30 questoes
  3. Casos: 5 casos clinicos proprios para tentar antes da proxima aula
  4. Proximo modulo: Nd:YAG seguinte semana

### Validacoes esperadas

- [x] Cada chunk ≤7min com retrieval practice
- [x] Verbo APLICAR explicito no slide 2
- [x] Hands-on contado (2) e estruturado (tempo, materiais, criterio)
- [x] `max_ctas: 4` declarado na Meta
- [x] Invoca `laser-physics` para formulas (cross-skill Fotona)
- [x] Invoca `deck-image-prompts` para capa + slides conceituais (esquema absorcao Er:YAG)
- [x] SEM Sparkline Duarte (nao e keynote)
- [x] Reviewer passa: chunks ≤7min ✓, max_ctas=4 OK, verbo Bloom ✓, hands-on ≥2 ✓

---

## Case 2 — Workshop 4h "Implantodontia basica" (modo `workshop-hands-on`)

### Input
```
U1: "Dentistas saem aptos a planejar e executar primeiro implante simples"
U2: dentistas clinicos sem experiencia em implantodontia
U3: 60min+ (escolha 5)
U4: presencial
U5: "Primeiro implante mata o medo do segundo"
U6: generico (sem auto-detect)
T1: 240min (4h)
T2: Bloom APLICAR
T3: alto em clinica geral, baixo em implante
T4: 2 hands-on (modelo plastico + caso integrador)
T5: caso integrador final (planejamento completo de 1 implante)
```

### Output esperado

STORYBOARD ~30-40 slides com:

- **Meta:** modo `workshop-hands-on`, `max_ctas: 4`, verbo Bloom = APLICAR, duracao 240min, chunks totais nao aplicavel (modulos), hands-on totais 2
- **Slide 1:** capa
- **Slide 2:** objetivos visiveis — 4 bullets iniciando com APLICAR (planejar / posicionar / suturar / orientar pos-op)
- **Slide 3:** pre-avaliacao
- **Modulo 1 (60min) — Slides 4-15:** Anatomia + planejamento radiografico
- **Hands-on 1 (30min) — Slides 16-18:** Posicionamento em modelo plastico com guia simples (worksheet impresso referenciado em apendice)
- **Modulo 2 (60min) — Slides 19-28:** Tecnica cirurgica + suturas basicas
- **Hands-on 2 (45min) — Slides 29-31:** Caso integrador — planejar 1 implante completo (radiografia real anonimizada, cliente preenche worksheet)
- **Modulo 3 (30min) — Slides 32-37:** Casos clinicos comentados + pos-op
- **Avaliacao (15min) — Slides 38-39:** Caso integrador apresentado individualmente
- **Slides 40-41:** CTAs (4):
  1. Aplicar em paciente proprio (com critério de selecao — caso simples Tipo I)
  2. Leitura: livro recomendado capitulo 3
  3. Fechar primeiro caso real e enviar pra revisao do instrutor
  4. Workshop avancado em 60 dias (sequencia)

### Validacoes esperadas

- [x] 4 modulos + 2 hands-on + caso integrador (estrutura workshop)
- [x] Verbo APLICAR no slide 2 (4 bullets)
- [x] Hands-on contado (2) e estruturado (tempo, materiais, criterio de sucesso)
- [x] `max_ctas: 4` declarado na Meta
- [x] Worksheet impresso referenciado em apendice (NAO produzido pela skill — fora do escopo)
- [x] SEM chunks ≤7min rigidos (workshop opera em modulos)
- [x] SEM Sparkline (nao e keynote)
- [x] Reviewer passa: hands-on contado ✓, max_ctas=4 OK, verbo Bloom ✓, modulos balanceados ✓

---

## Case 3 — Keynote 18min "O futuro da odontologia premium" (modo `keynote-inspirational`)

### Input
```
U1: "Audiencia sai com nova visao sobre seu papel no futuro odonto premium"
U2: dentistas-proprietarios diversos niveis (alguns ja premium, alguns commodity)
U3: 15-20min (escolha 3)
U4: presencial em evento
U5: "Voce esta vendendo procedimento; o futuro vende transformacao"
U6: Beauty Smile (auto-detect)
T1: 18min
T2: Bloom AVALIAR (mudanca de perspectiva)
T3: alto em odonto, baixo em estrategia de marca
T4: nao
T5: nao
```

### Output esperado

STORYBOARD 15-18 slides Sparkline Duarte:

- **Meta:** modo `keynote-inspirational`, **`max_ctas: 1`** (override do override — keynote nao precisa 4), verbo Bloom = AVALIAR, duracao 18min, chunks N/A, hands-on N/A
- **Slide 1:** capa Beauty Smile + Big Idea "Voce esta vendendo procedimento; o futuro vende transformacao"
- **Slide 2:** hook narrativo — historia real (paciente trocou de clinica) — 60s
- **Slide 3:** contexto (what is) — "73% das clinicas competem por preco. Onde voce esta?" — 90s
- **Slide 4:** promessa (what could be) — "Existe um terceiro caminho que poucos ainda veem" — 60s
- **Slides 5-6:** tensao 1 — problema visivel (margem caindo, cadeira ociosa, churn) com numeros — 2min
- **Slides 7-8:** resolucao 1 (insight parcial) — "Primeiro shift: do volume ao valor percebido" + 1 caso — 90s
- **Slides 9-10:** tensao 2 (mais profunda) — problema invisivel ("voce vende procedimentos quando deveria vender transformacao") — 2min
- **Slides 11-13:** resolucao 2 (revelacao) — modelo Beauty Smile (experiencia + branding + outcome) — 3min
- **Slide 14:** Big Idea reforcada — slide 1 redesenhado, frase identica — 30s
- **Slides 15-16:** call provocativo UNICO — "Escolha hoje: lembranca daqui 10 anos ou consultorio que faz tratamento?" — 60s

### Validacoes esperadas

- [x] Sparkline Duarte aplicado (contexto → promessa → tensao 1 → resolucao 1 → tensao 2 → resolucao 2 → Big Idea → call)
- [x] Big Idea destilada em 1 frase poetica, repetida no inicio e fim
- [x] **`max_ctas: 1`** declarado na Meta (override do default teaching=4 — keynote pede 1 unico CTA provocativo)
- [x] Verbo AVALIAR explicito no slide 2 (objetivo de mudar perspectiva)
- [x] SEM chunks ≤7min (Sparkline ignora segmentacao Mayer)
- [x] SEM hands-on
- [x] SEM quiz
- [x] Tom narrativo nas speaker notes (NAO didatico)
- [x] Brand tokens Beauty Smile injetados via `beauty-smile-design-system` (se instalado)
- [x] Reviewer passa: Sparkline detectado ✓, Big Idea repetida ✓, 1 CTA ✓, tom narrativo ✓

---

## Resumo de cobertura

| Dimensao validada | Case 1 | Case 2 | Case 3 |
|-------------------|--------|--------|--------|
| Modo `aula-tecnica` | ✓ | — | — |
| Modo `workshop-hands-on` | — | ✓ | — |
| Modo `keynote-inspirational` | — | — | ✓ |
| Chunks ≤7min | ✓ | — | — |
| Hands-on contado | ✓ | ✓ | — |
| Sparkline Duarte | — | — | ✓ |
| Verbo Bloom slide 2 | APLICAR | APLICAR | AVALIAR |
| max_ctas | 4 | 4 | 1 |
| Pre-avaliacao slide 3 | ✓ | ✓ | — |
| Cross-skill `laser-physics` | ✓ | — | — |
| Cross-skill `beauty-smile-design-system` | — | — | ✓ |
| Auto-detect marca | Fotona | generico | Beauty Smile |
