# Skeleton — modo `keynote-inspirational`

Sparkline Duarte (Nancy Duarte, *Resonate*). 12-20 slides. 12-20min. SO neste modo. Copia + preenche.

```markdown
# Deck: {nome-keynote}

## Meta
- Skill geradora: deck-teaching
- Modo: keynote-inspirational
- Objetivo unico: {U1 — mudanca de perspectiva da audiencia}
- Audiencia: {U2}
- Duracao: {T1} min (tipicamente 12-20min)
- Formato: presencial em evento
- Big Idea: {U5 — UMA frase poetica memoravel}
- Marca: {U6}
- Framework principal: Sparkline Duarte (what is ↔ what could be)
- max_ctas: 1   (override do default teaching=4 — keynote pede 1 unico CTA provocativo)
- Verbo Bloom alvo: {T2 — quase sempre AVALIAR}
- Chunks ≤7min: N/A (Sparkline ignora segmentacao Mayer)
- Hands-on: N/A
- Avaliacao final: N/A (objetivo e mudanca de perspectiva, nao demonstracao de tarefa)
- Gerado em: {ISO date}
- Versao: v1
- Storyboard ID: STORYBOARD-{slug}-{YYYYMMDD-HHmm}

## Estrutura Narrativa
Keynote {T1}min em arco Sparkline Duarte: contexto (what is) → promessa (what could be) → tensao 1 → resolucao 1 → tensao 2 (mais profunda) → resolucao 2 (revelacao) → Big Idea reforcada → call provocativo UNICO. Big Idea funciona como ponte entre o "is" e o "could be" e e repetida no slide 1 e no penultimo slide redesenhado.

Tom: narrativo, primeira pessoa, pausas marcadas nas speaker notes. NAO didatico, NAO segmentado, NAO pitch de produto.

---

## Slide 1 — Capa + Big Idea
Tipo: capa
Action title: {Big Idea — U5 destilada, 1 frase poetica}
Mensagem-chave: nenhuma — Big Idea sozinha ocupa o slide
Speaker notes: 2-3 paragrafos. Comecar com pausa de 3-5s antes de falar. Estabelecer presenca. Big Idea dita devagar.
Visual: cinematic, brand-safe, mood evocativo
Prompt de imagem: {deck-image-prompts preenche — Higgsfield Soul ou Imagen 4 cinematic, brand tokens}
Tempo estimado: 30s

## Slide 2 — Objetivos visiveis (verbo Bloom em CAIXA ALTA)
Tipo: conceitual
Action title: Ao final destes {T1}min voce vai AVALIAR {objeto}
Mensagem-chave: 1-2 objetivos de mudanca de perspectiva (NAO tarefa tecnica)
Bullets:
- AVALIAR sua posicao atual em relacao a {tema}
- (opcional) RECONSIDERAR a premissa que vinha guiando {decisao}
Speaker notes: explicar que isto NAO e uma aula — e um convite a repensar; sem prova de aprendizagem mensuravel, so reflexao
Visual: tipografia limpa
Prompt de imagem: skip — conceitual minimal
Tempo estimado: 60s

---

## Slide 3 — Contexto (what is)
Tipo: problema
Action title: {descrever o mundo atual da audiencia em 1 frase}
Mensagem-chave: dado/numero/observacao concreta que ressoa
Speaker notes: pintar a realidade da audiencia com precisao. "Voce esta neste lugar." Sem julgar.
Visual: editorial, retrato do status quo
Prompt de imagem: {deck-image-prompts preenche}
Tempo estimado: 90s

## Slide 4 — Promessa (what could be)
Tipo: conceitual
Action title: {visao futura em 1 frase}
Mensagem-chave: convite — "imagine este lugar"
Speaker notes: pintar a visao com mesma precisao. Sem prometer demais. Plantar duvida: "isso e possivel?"
Visual: contraste visual com slide 3 (mesma estetica, mood oposto)
Prompt de imagem: {deck-image-prompts preenche}
Tempo estimado: 60s

---

## Slides 5-6 — Tensao 1 (problema visivel)
Tipo: problema (2 slides)
Action title: {nome do problema visivel — numero/dado}
Mensagem-chave: o que a audiencia ja sente mas talvez nao tenha nomeado
Speaker notes: nomear o medo/duvida real. Concreto. Especifico. Pausa apos o numero.
Visual: 1 dado central por slide
Prompt de imagem: {se conceitual; se dados puros = skip}
Tempo estimado: 2min total

## Slides 7-8 — Resolucao 1 (insight parcial)
Tipo: conceitual + (opcional) prova-social
Action title: {primeiro shift — frase memoravel}
Mensagem-chave: insight inicial + 1 caso real curto
Speaker notes: oferecer perspectiva alternativa SEM resolver tudo ainda; preservar tensao para o proximo movimento
Visual: 1 ideia + 1 caso
Prompt de imagem: {deck-image-prompts — prova-social se houver caso}
Tempo estimado: 90s

---

## Slides 9-10 — Tensao 2 (mais profunda)
Tipo: problema
Action title: {o problema invisivel — atras do visivel}
Mensagem-chave: revelar a camada que poucos percebem
Speaker notes: aqui doe mais. Apontar para o erro de premissa, nao o erro de execucao. Pausa longa.
Visual: simbolico
Prompt de imagem: {deck-image-prompts preenche — conceitual ou problema}
Tempo estimado: 2min

## Slides 11-13 — Resolucao 2 (revelacao)
Tipo: conceitual (esquema novo)
Action title: {o modelo / framework / perspectiva que reorganiza tudo}
Mensagem-chave: 3 elementos ou 1 esquema que materializa a "what could be"
Speaker notes: aqui esta o coracao do keynote. Apresentar com clareza mas sem virar aula. Cada elemento ganha 1 slide.
Visual: esquema visual brand-safe, mesma estetica
Prompt de imagem: {deck-image-prompts preenche — tipo conceitual}
Tempo estimado: 3min

---

## Slide 14 — Big Idea reforcada (redesenho do slide 1)
Tipo: conceitual
Action title: {Big Idea identica ao slide 1, frase verbatim}
Mensagem-chave: nenhuma — Big Idea sozinha
Speaker notes: pausa antes de falar. Repetir a frase de abertura. Audiencia deve sair com essa frase na cabeca. Mostra que toda a jornada serviu pra dar peso a esta frase.
Visual: mesmo prompt da capa OU variacao consciente que ecoa
Prompt de imagem: {deck-image-prompts — variacao da capa, mesma serie}
Tempo estimado: 30s

---

## Slides 15-16 — Call provocativo (1 UNICO CTA)
Tipo: CTA
Action title: {pergunta provocativa que forca escolha — NAO instrucao operacional}
Mensagem-chave: 1 decisao binaria/trinaria que audiencia deve fazer hoje
Speaker notes:
- NAO e "compre", "acesse", "siga". E uma escolha de identidade.
- Ex: "Voce vai construir uma clinica que sera lembranca em 10 anos, ou um lugar que faz tratamento?"
- Pausa final de 5-8s antes de agradecer.
Visual: minimal, frase central
Prompt de imagem: skip — tipo CTA fora da whitelist (D5)
Tempo estimado: 60s

---

## Apendice (raro em keynote — usar so se evento pedir)
- A: Leitura recomendada (Resonate de Duarte; livros do tema)
- B: Contato/proximos passos (se aplicavel — discreto)

## Storyboard de Imagens (handoff pra deck-image-prompts)
Slides whitelisted: 1 (capa), 3 (problema), 4 (conceitual), 5-6 (problema), 7-8 (conceitual + prova-social), 9-10 (problema), 11-13 (conceitual), 14 (variacao da capa). Todos com MESMO style anchor para serie coesa (regra brand consistency).

## Checklist de Revisao (handoff pra deck-reviewer)
- [ ] Sparkline Duarte detectado: contexto → promessa → tensao 1 → resolucao 1 → tensao 2 → resolucao 2 → Big Idea → call
- [ ] Big Idea no slide 1 e no slide 14 (penultimo) com frase IDENTICA
- [ ] Verbo Bloom AVALIAR no slide 2
- [ ] **max_ctas: 1** declarado na Meta (override do default teaching=4)
- [ ] 1 UNICO CTA provocativo (decisao de identidade, nao acao operacional)
- [ ] SEM chunks ≤7min (regra Mayer NAO se aplica em keynote)
- [ ] SEM hands-on
- [ ] SEM quiz
- [ ] Tom narrativo nas speaker notes (NAO didatico)
- [ ] Style anchor consistente em toda a serie de imagens (brand consistency)
- [ ] Resolucao 2 NAO e pitch de produto (se for, vira deck-sales)
- [ ] Slides totais entre 12 e 20

## Compliance & Disclaimers
{conforme marca — keynote raramente tem disclaimers clinicos pois nao prescreve protocolo}
```
