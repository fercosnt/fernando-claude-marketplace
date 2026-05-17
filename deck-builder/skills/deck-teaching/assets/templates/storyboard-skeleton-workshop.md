# Skeleton — modo `workshop-hands-on`

Estrutura modulos + pratica intercalada (4-8h). Copia + preenche.

```markdown
# Deck: {nome-workshop}

## Meta
- Skill geradora: deck-teaching
- Modo: workshop-hands-on
- Objetivo unico: {U1}
- Audiencia: {U2}
- Duracao: {T1} min (tipicamente 240min = 4h ou 480min = 8h)
- Formato: {U4 — quase sempre presencial}
- Big Idea: {U5}
- Marca: {U6}
- Framework principal: Andragogy + Backwards Design + Bloom
- max_ctas: 4
- Verbo Bloom alvo: {T2 — quase sempre APLICAR}
- Modulos totais: 3-4
- Hands-on totais: {T4 — minimo 2 para validar tipo workshop}
- Avaliacao final: {T5 — quase sempre caso integrador}
- Gerado em: {ISO date}
- Versao: v1
- Storyboard ID: STORYBOARD-{slug}-{YYYYMMDD-HHmm}

## Estrutura Narrativa
Workshop {T1}min em 3-4 modulos conceituais alternados com {T4} hands-on supervisionados. Fecha com caso integrador onde aluno demonstra dominio da tarefa-alvo Bloom-APLICAR. Andragogy: relevancia imediata + experiencia previa ancorada + auto-direcao nos CTAs finais.

---

## Slide 1 — Capa
Tipo: capa
Action title: {Big Idea destilada}
Mensagem-chave: 1 frase + tempo total
Speaker notes: contextualizar workshop, materiais que cada aluno precisa, expectativas
Visual: setup hands-on real
Prompt de imagem: {deck-image-prompts preenche}
Tempo estimado: 2min (boas-vindas)

## Slide 2 — Objetivos (REGRA INVIOLAVEL: verbo Bloom em CAIXA ALTA)
Tipo: conceitual
Action title: Ao final deste workshop voce vai {VERBO_BLOOM} {tarefa}
Mensagem-chave: 3-5 objetivos terminais mensuraveis
Bullets:
- {VERBO_BLOOM} {tarefa hands-on 1}
- {VERBO_BLOOM} {tarefa hands-on 2}
- {VERBO_BLOOM} {tarefa integradora}
- {VERBO_BLOOM} {tarefa pos-workshop em campo real}
Speaker notes: amarrar cada objetivo ao hands-on/caso que comprova (Backwards Design)
Tempo estimado: 3min

## Slide 3 — Pre-avaliacao + agenda
Tipo: conceitual
Action title: Onde voce esta hoje + como vamos chegar la
Mensagem-chave: 3-4 perguntas diagnosticas + agenda visivel (modulos + hands-on + horarios)
Speaker notes: calibrar profundidade conforme respostas; agenda visivel REDUZ ansiedade adulto (Knowles)
Visual: timeline horizontal com 4 modulos + 2 hands-on marcados
Tempo estimado: 5min

---

## Modulo 1 — {Conceito fundacional} ({~60min})

## Slide 4-N — Conteudo conceitual
(varia conforme tema; pode usar mini-chunks ≤7min internos para temas densos)

## Slide N — Sintese modulo 1
Tipo: conceitual
Action title: 3 ideias-chave do modulo 1
Mensagem-chave: bullets resumo
Speaker notes: pause-and-discuss; aluno explica em voz alta (retrieval practice)
Tempo estimado: 5min

---

## Hands-on 1 ({~30min}) — {Tarefa supervisionada}

## Slide N — Briefing hands-on 1
Tipo: demo
Action title: Agora voce vai {tarefa pratica especifica}
Mensagem-chave: tarefa + tempo + criterio de sucesso
Speaker notes:
- Material necessario por aluno: {lista}
- Tempo: {min}
- Criterio de sucesso observavel: {ex: monta protocolo sem ajuda em <10min}
- Worksheet impresso: ver apendice A (NAO produzido pela skill — instrutor prepara)
- Instrutor circula: minimo 2 passagens por aluno
Visual: foto/esquema do setup
Prompt de imagem: {deck-image-prompts preenche — tipo demo whitelist}
Tempo estimado: 30min (5min briefing + 20min execucao + 5min debrief)

## Slide N — Debrief hands-on 1
Tipo: conceitual
Action title: O que cada um descobriu fazendo
Mensagem-chave: 2-3 padroes observados pelo instrutor
Speaker notes: coletar 3-4 falas da audiencia ANTES de comentar; nomear erros comuns sem expor aluno
Tempo estimado: 5min (incluso nos 30min hands-on)

---

## Modulo 2 — {Conceito avancado} ({~60min})
... (mesma estrutura modulo 1)

## Hands-on 2 ({~45min}) — {Caso integrador parcial OU tarefa mais complexa}
... (mesma estrutura hands-on 1, tempo maior, criterio mais exigente)

---

## Modulo 3 — {Casos clinicos / discussao} ({~30min})

## Slides N — 3-5 casos clinicos reais comentados
Tipo: prova-social
Action title: O que vimos na pratica clinica
Speaker notes: 1 caso por slide; perguntar audiencia antes de comentar; abrir espaco para casos da audiencia
Tempo estimado: 30min total

---

## Avaliacao final ({~15-30min}) — Caso integrador (T5)

## Slide N — Briefing caso integrador
Tipo: demo
Action title: Voce planeja {tarefa completa} sozinho
Mensagem-chave: caso real anonimizado + worksheet de planejamento
Speaker notes:
- Tempo individual: {N min}
- Apresentacao breve: cada aluno expoe seu planejamento em 2min
- Criterio: {checklist com X itens minimos}
- Feedback: instrutor + colegas
Tempo estimado: 15-30min

## Slide N — Sintese final + feedback coletivo
Tipo: conceitual
Action title: O que ficou claro + o que ainda precisa amadurecer
Speaker notes: nomear 2-3 padroes positivos + 2-3 areas de melhoria observadas; cada aluno escolhe seu proximo passo
Tempo estimado: 10min

---

## Slide N — CTAs (max 4 — override D14)
Tipo: CTA
Action title: O que fazer voltando pra clinica/escritorio
Mensagem-chave: 4 CTAs auto-direcionados
Bullets:
- [APLICAR] Fazer {tarefa} em paciente/caso proprio Tipo I (mais simples) em <30 dias e enviar relato
- [LEITURA] {livro / paper} cap {N}
- [FECHAR PRIMEIRO CASO] enviar planejamento pra revisao do instrutor antes de executar
- [PROXIMO NIVEL] workshop avancado em {N dias} (sequencia)
Speaker notes: explicar logica da progressao (Andragogy: auto-direcao + casos reais)
Tempo estimado: 5min

---

## Apendice
- A: Worksheet hands-on 1 + 2 (referencia — instrutor prepara impresso)
- B: Worksheet caso integrador
- C: Checklist criterio de aprovacao
- D: Bibliografia + workshops sequencia
- E: Lista de materiais por aluno (instrutor envia antes)

## Storyboard de Imagens (handoff pra deck-image-prompts)
Slides whitelisted: 1 (capa), demos de hands-on, casos clinicos (prova-social)

## Checklist de Revisao (handoff pra deck-reviewer)
- [ ] Verbo Bloom CAIXA ALTA no slide 2
- [ ] Pre-avaliacao + agenda visivel slide 3
- [ ] 3-4 modulos + minimo 2 hands-on (T4)
- [ ] Cada hands-on com tempo + material + criterio de sucesso explicito
- [ ] Caso integrador no final (T5)
- [ ] 4 CTAs com tags [APLICAR] [LEITURA] [FECHAR CASO] [PROXIMO]
- [ ] max_ctas: 4 declarado na Meta
- [ ] Worksheets referenciados em apendice (NAO produzidos pela skill)
- [ ] Cross-skill invocado se aplicavel
- [ ] Andragogy: agenda visivel + casos reais + auto-direcao nos CTAs

## Compliance & Disclaimers
{conforme marca}
```
