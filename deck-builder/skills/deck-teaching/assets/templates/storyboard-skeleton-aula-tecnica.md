# Skeleton — modo `aula-tecnica`

Estrutura segmentada em chunks ≤7min (Mayer). Copia + preenche.

```markdown
# Deck: {nome-aula}

## Meta
- Skill geradora: deck-teaching
- Modo: aula-tecnica
- Objetivo unico: {U1}
- Audiencia: {U2}
- Duracao: {T1} min
- Formato: {U4}
- Big Idea: {U5}
- Marca: {U6}
- Framework principal: Backwards Design + Bloom + Mayer (12 principios)
- max_ctas: 4
- Verbo Bloom alvo: {T2}
- Chunks totais: {N — calc: duracao / 7min, arredondar pra cima}
- Hands-on totais: {T4}
- Avaliacao final: {T5}
- Gerado em: {ISO date}
- Versao: v1
- Storyboard ID: STORYBOARD-{slug}-{YYYYMMDD-HHmm}

## Estrutura Narrativa
Aula segmentada Mayer com {N} chunks de ≤7min. Cada chunk segue padrao 5min explicacao + 2min retrieval practice. Quiz formativo entre chunks. Hands-on intercalado(s). Avaliacao somativa no final + 4 CTAs acionaveis (override D14).

---

## Slide 1 — Capa
Tipo: capa
Action title: {Big Idea destilada}
Mensagem-chave: 1 frase
Speaker notes: 2-3 paragrafos contextualizando audiencia e relevancia (Andragogy: necessidade de saber)
Visual: {brief para deck-image-prompts}
Prompt de imagem: {preenchido pelo deck-image-prompts}
Tempo estimado: 30s

## Slide 2 — Objetivos (REGRA INVIOLAVEL: verbo Bloom em CAIXA ALTA)
Tipo: conceitual
Action title: Ao final desta aula voce vai {VERBO_BLOOM} {objeto}
Mensagem-chave: 3-5 objetivos mensuraveis
Bullets:
- {VERBO_BLOOM} {tarefa 1 mensuravel}
- {VERBO_BLOOM} {tarefa 2 mensuravel}
- {VERBO_BLOOM} {tarefa 3 mensuravel}
Speaker notes: explicar evidencia que comprova cada objetivo (Backwards Design)
Visual: minimal, lista visivel
Prompt de imagem: skip — tipo conceitual mas lista pura, sem necessidade de imagem
Tempo estimado: 60s

## Slide 3 — Pre-avaliacao rapida (diagnostico T3)
Tipo: conceitual
Action title: Quanto voce ja sabe sobre {tema}?
Mensagem-chave: 3-5 perguntas para autoavaliar conhecimento previo
Speaker notes: pause-and-discuss; sem gabarito visivel; instrutor calibra ritmo conforme respostas
Visual: perguntas com escala 1-5
Tempo estimado: 90s

---

## Chunk 1 — {Conceito A} (≤7min)

## Slide 4 — {Tipo}
Action title: {assertivo}
...
Tempo estimado: 90s

## Slide 5 — {Tipo}
...

## Slide 6 — {Tipo}
...

## Slide 7 — Quiz formativo chunk 1
Tipo: conceitual
Action title: Voce consegue {tarefa Bloom-aplicar simples} agora?
Mensagem-chave: 1-2 perguntas retrievel practice
Speaker notes: NAO mostrar gabarito; instrutor revela na fala apos audiencia tentar
Tempo estimado: 120s

---

## Chunk 2 — {Conceito B} (≤7min)
... mesma estrutura

## Slide N — Quiz formativo chunk 2
...

---

## Hands-on 1 (T4 — se aplicavel)

## Slide N — Briefing hands-on 1
Tipo: demo
Action title: Agora voce vai {tarefa hands-on}
Mensagem-chave: tarefa + tempo + criterio de sucesso
Speaker notes:
- Material necessario: {lista}
- Tempo: {min}
- Criterio de sucesso: {observavel}
- Worksheet impresso: ver apendice A
Visual: foto setup ou esquema
Prompt de imagem: {tipo demo na whitelist — deck-image-prompts preenche}
Tempo estimado: total {min} (split: 5min briefing + N min execucao + 5min debrief)

## Slide N — Debrief hands-on 1
Tipo: conceitual
Action title: O que voce notou ao {tarefa}?
Speaker notes: pause-and-discuss; coletar 2-3 observacoes da audiencia
Tempo estimado: 5min

---

(continuar chunks 3-N + hands-on 2 + ...)

---

## Slide N — Avaliacao somativa (T5)
Tipo: conceitual
Action title: Vamos consolidar
Mensagem-chave: quiz somativo {N} questoes Bloom-aplicar
Speaker notes:
- Formato: {quiz / projeto / observacao}
- Criterio de aprovacao: {ex: 70%}
- Gabarito: ver apendice B (NAO mostrar no slide)
Tempo estimado: 15min

---

## Slides N-1 e N — CTAs (max 4 — override D14)

## Slide N+1 — Proximos passos
Tipo: CTA
Action title: O que fazer ate a proxima aula
Mensagem-chave: 4 CTAs acionaveis e auto-direcionados (Andragogy)
Bullets:
- [PRATICA] Aplicar {tecnica} em {N casos proprios} ate {data}
- [LEITURA] {paper / capitulo} recomendado
- [QUIZ ONLINE] Banco de {N questoes} em {link}
- [PROXIMO MODULO] {tema seguinte} em {data}
Speaker notes: explicar por que esses 4 (auto-direcao — aluno escolhe combinacao)
Visual: lista clara, 4 itens
Prompt de imagem: skip — tipo CTA fora da whitelist (D5)
Tempo estimado: 60s

---

## Apendice
- A: Worksheet hands-on 1 (referencia externa)
- B: Gabarito avaliacao somativa (so instrutor)
- C: Bibliografia ampliada

## Storyboard de Imagens (handoff pra deck-image-prompts)
Slides whitelisted: 1 (capa), {N} (conceituais), {N} (demo hands-on)

## Checklist de Revisao (handoff pra deck-reviewer)
- [ ] Verbo Bloom CAIXA ALTA no slide 2
- [ ] Pre-avaliacao slide 3
- [ ] Cada chunk ≤7min
- [ ] Quiz formativo entre chunks
- [ ] Hands-on contado (T4 = {N}) e estruturado (tempo + material + criterio)
- [ ] Avaliacao somativa final (T5)
- [ ] 4 CTAs com tags [PRATICA] [LEITURA] [QUIZ] [PROXIMO]
- [ ] max_ctas: 4 declarado na Meta
- [ ] Cross-skill invocado se marca = Fotona (laser-physics) ou Beauty Smile (design-system)
- [ ] Sem stock cliche (Mayer coerencia)
- [ ] Speaker notes EXPANDEM o slide, nao repetem (Mayer redundancia)

## Compliance & Disclaimers
{conforme marca — compliance_tags do brands.yaml}
```
