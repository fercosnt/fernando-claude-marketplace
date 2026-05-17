---
name: deck-internal
description: STORYBOARD para apresentacoes internas (pitch CEO, all-hands, estrategia, concept reveal). 4 modos com Pyramid/BLUF, Raskin, Sparkline, Sinek e 6-pager Amazon. concept-reveal consome cenografia (D3).
intent: action
effort: high
nb_ids:
  - 7f1b2e2b-4ba4-40de-ba56-ca2f55e2c0da  # NB1 Core (sempre)
  - 5a0aaabb-78c1-4d03-a400-e9ce1973737b  # NB3 Comerciais (Pyramid Minto transversal)
references:
  - references/framework-pyramid-raskin-sparkline.md
  - references/framework-working-backwards-amazon.md
  - references/pipeline-cenografia-handoff.md
  - references/eval-cases-internal.md
assets:
  - assets/templates/storyboard-skeleton-pitch-leadership.md
  - assets/templates/storyboard-skeleton-strategy.md
  - assets/templates/storyboard-skeleton-concept-reveal.md
  - assets/templates/storyboard-skeleton-all-hands.md
  - assets/templates/amazon-6pager-skeleton.md
  - assets/checklists/internal-checklist.md
---

# deck-internal

Skill vertical 8/8 do plugin **deck-builder**. Cria STORYBOARD.md para apresentacoes **internas** — pitch executivo, all-hands, estrategia, concept reveal. Quatro modos com frameworks distintos.

## Quando ativa

**Triggers diretos (orchestrator roteia sem perguntar):**
- "pitch interno", "apresentar pro CEO", "all-hands", "estrategia mkt", "concept reveal", "expert meeting"
- "politica viagens", "business case interno", "estrutura organizacional", "Q1/Q2/Q3/Q4 review"
- "alinhamento de time", "kickoff trimestre", "expert meeting Fotona/La&HA"

**Trigger especial concept-reveal (D3 — pipeline cenografia):**
- "apresentar conceito da sala VIP", "concept reveal Carnaval 360", "vender o booth pro board"
- Detectar PALAVRA-CHAVE `conceito` + (`sala` | `booth` | `camarote` | `ativacao` | `experiencia`) → modo `concept-reveal`

**Modo encadeado (default — invocada pelo `deck-orchestrator`):**
Orchestrator detecta keywords e roteia direto. Esta skill recebe o contexto e roda entrevista universal + vertical.

**Modo standalone:**
`/deck-internal` ou `/deck preciso pitchar pro CEO...` — roda interview completo.

## Fronteira (LOCKED — D3)

**NAO projeta espaco/cenografia.** Modo `concept-reveal` CONSOME artefatos prontos de `skill-cenografia` (renders + mood + layouts + JSON Nano Banana Pro). Esta skill APRESENTA o conceito ao board/CEO; NAO desenha a sala.

**Pipeline correto:**
1. Usuario invoca `skill-cenografia` PRIMEIRO → gera artefatos em `./cenografia/<projeto>/`
2. Depois invoca `deck-internal concept-reveal` → carrega artefatos como visuais nos slides 3-6 do STORYBOARD

Detalhes em [references/pipeline-cenografia-handoff.md](references/pipeline-cenografia-handoff.md).

## Modos (4)

| Modo | Quando | Estrutura | Slides | Framework |
|------|--------|-----------|--------|-----------|
| `pitch-to-leadership` | Pitch interno 1:1 ou small group (CEO/board/diretoria) | BLUF + Pyramid + ask especifico + 6-pager anexo | 8-10 | Pyramid Minto + Raskin |
| `strategy-presentation` | Apresentacao de estrategia para time/diretoria | Pyramid + 3 Horizontes McKinsey | 12-15 | Pyramid + SCR + McKinsey 3H |
| `concept-reveal` (D3) | Apresentar conceito de espaco/ativacao consumindo cenografia | Sparkline Duarte experiencial + visuais cenografia | 6-8 | Sparkline Duarte |
| `all-hands` | Apresentacao empresa toda (40+ pessoas) | Why-How-What + visao + Kotter visibilizado | 10-12 | Sinek + Raskin + Kotter |

**Algoritmo de selecao de modo (apos U1-U6):**
1. Keywords `CEO` + `aprovar`/`decidir`/`board` → `pitch-to-leadership`
2. Keywords `conceito` + (`sala`/`booth`/`camarote`/`ativacao`) → `concept-reveal` (e checa artefatos cenografia)
3. Keywords `empresa toda`/`all-hands`/`time todo` + audiencia ≥30 → `all-hands`
4. Keywords `estrategia`/`Q1`/`trimestre`/`horizontes` → `strategy-presentation`
5. Ambiguo → AskUserQuestion com 2 modos mais provaveis

## Entrevista (Universal §10.1 + Vertical I1-I5)

Apos U1-U6 do SHARED.md, rodar vertical:

- **I1:** Quem na audiencia decide o resultado? (1 pessoa / time / board / empresa toda)
- **I2:** Voce esta pedindo (a) aprovacao formal, (b) buy-in, (c) alinhamento, (d) inspirar/mobilizar?
- **I3:** Ask especifico (recurso $, headcount, decisao formal, mudanca de processo, alinhamento sem ask)
- **I4:** Existe business case interno com numeros? (ROI, payback, NPV, custo de inacao)
- **I5:** Maior resistencia politica antecipada (CFO ve como burocracia? Time ve como ameaca? Board ve como risco?)

**Modo `concept-reveal` ganha 2 perguntas adicionais:**
- **C1:** Path absoluto da pasta com artefatos `skill-cenografia` (default tentativa: `./cenografia/<slug>/`)
- **C2:** Big Idea sensorial em 1 frase (ex: "imersao VIP com IA hospedeira que muda o que e ser VIP em evento")

**Modo `all-hands` ganha 1 pergunta adicional:**
- **A1:** Ha mudanca organizacional ou crise no contexto? (ajusta tom + adiciona Kotter)

## Frameworks (resumo — detalhe em references)

### Pyramid Minto (BLUF) — pitch-to-leadership

- **Slide 2 = BLUF** (Bottom Line Up Front) em 1 sentenca: recomendacao + investimento + retorno + prazo + ask
- Argumentos top-down MECE (Mutuamente Exclusivos, Coletivamente Exaustivos)
- Evidencia depois, apendice por ultimo
- SCQA antes do BLUF: Situation → Complication → Question → Answer

### Andy Raskin — pitch-to-leadership + all-hands

- Status Quo (mundo atual) → New World (mundo apos a mudanca)
- Big Idea = ponte entre os dois mundos
- "A historia da empresa E a estrategia" (Horowitz)

### Sparkline Duarte — concept-reveal

- Oscilacao entre "what is" (status quo desconfortavel) vs "what could be" (visao)
- Minimo 2 oscilacoes ANTES do reveal (Jobs mostrou "telefones ruins" antes do iPhone)
- Reveal nao na primeira secao — pico emocional so funciona apos vales
- Cliene New Bliss (estado futuro desejavel)

### Sinek Golden Circle (Why → How → What) — all-hands

- Comeca pelo proposito (Why), depois processo (How), depois resultado (What)
- "What" sozinho ativa neocortex; "Why" ativa limbico (decisao + emocao)
- Slide visao no centro do deck (nao no fim)

### McKinsey 3 Horizontes — strategy-presentation

- H1 (core, defender): 70% budget/esforco
- H2 (emergente, cultivar): 20%
- H3 (futuro, semear): 10%
- Sequencia recomendada: H1 → H3 → H2 (familiar → visao → ponte)

### Working Backwards Amazon 6-pager — ANEXO em pitch-to-leadership

- Memorando narrativo 6 paginas, prosa densa, ZERO bullets, ZERO slides
- 30 min de leitura silenciosa no inicio da reuniao ("study hall")
- Apendice ilimitado para dados
- Detalhe completo em [references/framework-working-backwards-amazon.md](references/framework-working-backwards-amazon.md)
- Asset: [assets/templates/amazon-6pager-skeleton.md](assets/templates/amazon-6pager-skeleton.md)

## Estrutura por modo

### Modo `pitch-to-leadership` (8-10 slides)

Template: [assets/templates/storyboard-skeleton-pitch-leadership.md](assets/templates/storyboard-skeleton-pitch-leadership.md)

1. **Capa** — action title assertivo (NAO descritivo)
2. **BLUF** (Pyramid Minto — OBRIGATORIO slide 2) — recomendacao + investimento + retorno + prazo + ask em 1 sentenca
3. **Problema/Status Quo** (Raskin) — custo de inacao quantificado
4. **Solucao proposta** — 1 slide, especifica, nao vaga
5. **Business case** — numeros, ROI, payback (I4)
6. **Friccao mitigada** — objecao antecipada (I5)
7. **Ask especifico** (I3) — valor + timeline + sponsor + decisao requerida AGORA
8-10. **Proximos passos + Q&A backup + Apendice**

**ANEXO OBRIGATORIO:** 6-pager Amazon-style em PDF separado (assets/templates/amazon-6pager-skeleton.md). 6-pager NAO substitui slides — anexa.

**Adaptacao Brasil (Hofstede 69 distancia poder + 76 aversao incerteza):** Pyramid puro pode soar arrogante no Brasil. Solucao: 30s de abertura relacional + situacao compartilhada ANTES do BLUF slide 2. Slide 1 e capa relacional; BLUF e slide 2.

### Modo `strategy-presentation` (12-15 slides)

Template: [assets/templates/storyboard-skeleton-strategy.md](assets/templates/storyboard-skeleton-strategy.md)

- BLUF + Pyramid em cascata
- SCR (Situation → Complication → Resolution)
- 3 Horizontes McKinsey (now / next / later)
- Hipoteses testaveis por horizonte
- Alocacao de recursos regra 70/20/10
- KPIs por horizonte
- Riscos e dependencias criticas
- Proximos passos + owners

**SCR direction:** audiencia resistente → S→C→R (consenso gradual); audiencia alinhada → R→S→C (reforca conviccao).

### Modo `concept-reveal` (6-8 slides — D3 pipeline cenografia)

Template: [assets/templates/storyboard-skeleton-concept-reveal.md](assets/templates/storyboard-skeleton-concept-reveal.md)

1. **Capa mood** (Sparkline — atmosfera, NAO titulo descritivo)
2. **Big Idea sensorial** (U5/C2) — 1 frase poderosa
3. **What is** (status quo experiencial — sala VIP generica, evento sem alma, etc)
4. **What could be** (visao com render principal da cenografia)
5-6. **Detalhes do conceito** (mood + materiais + experiencia 1ª pessoa — usa renders + mood boards de cenografia)
7. **Ask executivo** (aprovar conceito + budget + cronograma)
8. **Proximos passos**

**Pipeline obrigatorio:**
1. Validar que pasta `./cenografia/<slug>/` (ou C1) existe com artefatos
2. Listar artefatos disponiveis (renders.png, mood-board.png, layout.json, prompts.json)
3. Slides 3-6 referenciam paths ABSOLUTOS dos artefatos no campo `Visual:` do schema §10.2
4. Campo `Prompt de imagem:` copia o prompt ja gerado por cenografia (NAO regera)
5. Se faltar artefato → emite WARN e sugere rodar `skill-cenografia` primeiro

Detalhe do handoff em [references/pipeline-cenografia-handoff.md](references/pipeline-cenografia-handoff.md).

### Modo `all-hands` (10-12 slides)

Template: [assets/templates/storyboard-skeleton-all-hands.md](assets/templates/storyboard-skeleton-all-hands.md)

1. **Abertura energizante** (video / musica / CEO ao vivo — NAO bullets)
2. **Visao + proposito** (Sinek WHY) — reafirmacao da missao
3. **Estado do negocio** (qualitativo do CEO — honestidade)
4. **Metricas-chave** (3-5 KPIs consistentes vs meta)
5. **Celebracoes Q anterior** (multiplos apresentadores — NAO so CEO)
6. **Tópico estrategico 1** (Sinek HOW) — o que esta mudando
7. **Tópico estrategico 2** (se aplicavel)
8. **Reconhecimento individual** (peer shoutouts)
9. **Prioridades Q seguinte** (Sinek WHAT)
10. **Q&A aberto** (perguntas anonimas pre-coletadas)
11. **Proximos passos + encerramento**

**Sinek Why-How-What estrutural:**
- Slide 2 (Visao) = WHY
- Slides 6-7 (Topicos estrategicos) = HOW
- Slide 9 (Prioridades) = WHAT

**Se A1 = "ha mudanca organizacional":** adicionar Kotter visibilizado (urgencia + coalizao + visao) entre slides 3-5. Lewin "unfreeze-change-refreeze" para mudancas discretas.

**Arco emocional:** Energia alta → Sobriedade factual → Calor humano → Relevancia estrategica → Conexao pessoal → Abertura → Clareza final.

**Proporcao:** 30% factual / 70% engajamento, reconhecimento, significado.

**max_ctas:** 2 (override SHARED.md — all-hands pode ter ask de prioridades + ask de Q&A engagement).

## Protocolo de execucao

1. **Auto-detect marca** (§10.5 SHARED.md). Se Beauty Smile → carregar `beauty-smile-design-system`. Se Fotona/Carnaval 360 → tokens declarados.
2. **Entrevista universal** (U1-U6) — pular se orchestrator ja roteou com 2+ keywords.
3. **Entrevista vertical** (I1-I5) — sempre rodar. Modo concept-reveal: +C1-C2. Modo all-hands: +A1.
4. **Selecionar modo** pelo algoritmo acima ou via AskUserQuestion se ambiguo.
5. **Consultar NB1 + NB3** com query especifica:
   ```bash
   notebooklm use 7f1b2e2b-4ba4-40de-ba56-ca2f55e2c0da
   notebooklm ask "Pyramid Minto BLUF estrutura para pitch CEO {Big Idea} {marca}" --max-citations 5
   notebooklm use 5a0aaabb-78c1-4d03-a400-e9ce1973737b
   notebooklm ask "Working Backwards 6-pager Amazon para business case {ask especifico}" --max-citations 5
   ```
   Falha de NB NAO bloqueia — degrade com warning.
6. **Gerar STORYBOARD.md** seguindo schema §10.2 SHARED.md + template do modo escolhido.
7. **Se modo `pitch-to-leadership`:** gerar tambem 6-pager anexo a partir do `amazon-6pager-skeleton.md` em arquivo separado `STORYBOARD-{slug}-{HHmm}.6pager.md`.
8. **Se modo `concept-reveal`:** validar paths cenografia + copiar prompts ja gerados + referenciar absolute paths nos campos Visual:.
9. **Whitelist `deck-image-prompts` D5** — preencher slides whitelisted (capa, problema, conceitual, comparativo, demo, prova-social); skip outros. Modo concept-reveal: cenografia ja forneceu imagens, deck-image-prompts so para capa adicional se faltar.
10. **Output:** `$DECKS_DIR/{YYYY-MM}/STORYBOARD-{slug}-{HHmm}.md` (+ `.6pager.md` se pitch-to-leadership).
11. **Sugerir `/deck review`** para passar pelo `deck-reviewer` (opt-in mas fortemente recomendado para decks de alta consequencia — pitches CEO especialmente).

## Guardrails

### Anti-padroes (banir — fonte: pesquisa anti-modelos-pitch-corporativo)

- **Ask invisivel** (Twitter/Musk Nov 2022): toda apresentacao pitch-to-leadership PRECISA de Ask especifico slide 7. NAO "avancar com a exploracao" — SIM "aprovar R$80k para Q3, decisao hoje".
- **Business case sem numeros** (rejeitado em 15min): se I4 = sem business case, AVISAR usuario antes de gerar pitch-to-leadership.
- **All-hands sem visao** (Twitter pos-aquisicao Musk): all-hands SEM slide visao = briefing disfarcado. Slide 2 OBRIGATORIO Sinek WHY.
- **Concept-reveal sem problema** (Spotify Squad Model copiado cegamente): NAO abrir com o conceito. Minimo 2 vales Sparkline ANTES do reveal.
- **Death by PowerPoint** (NASA Columbia — 7 mortos): NAO bullet hell. Action titles + 1 ideia por slide.
- **Enterrar o lede** (formato academico — contexto antes da resposta): em pitch-to-leadership, BLUF e slide 2, NAO slide 8.
- **Delegacao a proxy** (Yahoo Mayer 2013): mudanca grande precisa do dono comunicando. NAO delegar all-hands de mudanca a HR.

### Adaptacao Brasil (Hofstede)

- Pyramid puro pode soar arrogante. Solucao: capa relacional slide 1 + BLUF slide 2.
- Payback domina sobre NPV em grandes empresas BR. Business case: mencionar BOTH mas LIDERAR com payback.
- Hierarquia: respeitar abertura relacional antes da resposta. Adicionar 30-60s de "agradecer + situar" antes do BLUF.

### Compliance

- Beauty Smile (compliance_tags `odontologia-br` `cfo-cfm`): se pitch envolve protocolo clinico interno → adicionar `🟡 Verificar antes` Compliance & Disclaimers no STORYBOARD.
- Fotona (`anvisa-laser-classe-iii`): se pitch envolve venda de equipamento ou claims clinicos → bloqueio 🔴.
- Numeros financeiros sem `provisional`/`projecao` marker em pitch externo → 🔴.

### Falha graceful

- **NB indisponivel:** segue com defaults canonicos (Minto + Raskin estruturais) — emite warning `<!-- NB1/NB3 indisponivel; defaults aplicados -->`.
- **`skill-cenografia` artefatos ausentes em modo concept-reveal:** PARA e sugere `Rode skill-cenografia primeiro em ./cenografia/<slug>/, depois invoque deck-internal concept-reveal novamente`.
- **`beauty-smile-design-system` nao instalado:** segue sem tokens — emite warning.

## Output STORYBOARD

Schema §10.2 SHARED.md. **`max_ctas: 1`** default (override `all-hands` = 2 com justificativa).

Path: `$DECKS_DIR/{YYYY-MM}/STORYBOARD-{slug}-{HHmm}.md`

Modo `pitch-to-leadership` tem anexo: `STORYBOARD-{slug}-{HHmm}.6pager.md` no mesmo diretorio.

Cabecalho `## Meta`:
```yaml
- Skill geradora: deck-internal
- Framework principal: {Pyramid Minto + Raskin | SCR + 3H McKinsey | Sparkline Duarte | Sinek + Raskin + Kotter}
- Modo: {pitch-to-leadership | strategy-presentation | concept-reveal | all-hands}
- max_ctas: {1 | 2 se all-hands}
- Anexo 6-pager: {sim se pitch-to-leadership | nao}
- Artefatos cenografia (se concept-reveal): {path absoluto}
```

## Limites

- NAO gera slides finais (PPTX/Gamma/Figma) — so STORYBOARD.md.
- NAO projeta espaco/cenografia — D3 LOCKED, delega `skill-cenografia`.
- NAO renderiza imagens — `deck-image-prompts` faz prompts.
- NAO faz post de redes sociais — delega `/copy`.
- NAO busca dados em tempo real — usuario fornece I4.
- NAO substitui consultoria estrategica — modo strategy-presentation estrutura, NAO inventa estrategia.

## Eval cases (3 — detalhe em [references/eval-cases-internal.md](references/eval-cases-internal.md))

1. **Case 1: Politica viagens corp Beauty Smile (Walkthrough 3 §12)** — modo `pitch-to-leadership`, 9 slides, BLUF slide 2, anexo 6-pager, ask R$80k aprovacao
2. **Case 2: Concept reveal "Sala VIP Carnaval 360 com IA hospedeira"** — modo `concept-reveal` D3 pipeline, 8 slides Sparkline, consome artefatos cenografia em path absoluto, NAO duplica trabalho
3. **Case 3: All-hands Q1 Beauty Smile com mudanca organizacional** — modo `all-hands`, 11 slides Sinek Why-How-What + Kotter visibilizado, max_ctas 2

## Referencias

- [references/framework-pyramid-raskin-sparkline.md](references/framework-pyramid-raskin-sparkline.md) — Minto BLUF, Raskin Strategic Narrative, Sparkline Duarte (oscilacao what-is/what-could-be), Sinek Golden Circle, McKinsey 3 Horizontes
- [references/framework-working-backwards-amazon.md](references/framework-working-backwards-amazon.md) — 6-pager Amazon estrutura + regras de escrita + PR/FAQ method + protocolo de reuniao study hall
- [references/pipeline-cenografia-handoff.md](references/pipeline-cenografia-handoff.md) — schema D3 do handoff cenografia → concept-reveal, paths absolutos, validacao de artefatos, exemplos
- [references/eval-cases-internal.md](references/eval-cases-internal.md) — 3 eval cases com inputs e expected outputs detalhados
- [assets/templates/storyboard-skeleton-pitch-leadership.md](assets/templates/storyboard-skeleton-pitch-leadership.md) — skeleton 9 slides Pyramid + BLUF + 6-pager
- [assets/templates/storyboard-skeleton-strategy.md](assets/templates/storyboard-skeleton-strategy.md) — skeleton 13 slides SCR + 3H McKinsey
- [assets/templates/storyboard-skeleton-concept-reveal.md](assets/templates/storyboard-skeleton-concept-reveal.md) — skeleton 8 slides Sparkline + handoff cenografia
- [assets/templates/storyboard-skeleton-all-hands.md](assets/templates/storyboard-skeleton-all-hands.md) — skeleton 11 slides Sinek + Kotter
- [assets/templates/amazon-6pager-skeleton.md](assets/templates/amazon-6pager-skeleton.md) — 6-pager skeleton anexo
- [assets/checklists/internal-checklist.md](assets/checklists/internal-checklist.md) — checklist final por modo

## v1.1 — Adendo: `modo_entrega` + `[VERIFICAR]` + Layout sugerido

A partir de v1.1 do plugin, esta skill aplica 4 disciplinas adicionais ao gerar STORYBOARD. Detalhes canônicos em `../../shared/storyboard-schema.md` e `../../shared/verificar-flag.md`.

**1. `modo_entrega` adapta densidade do slide** (regra 7 do schema):
- `apresentado-ao-vivo` (U4=1/2): slides minimalistas (2-3 bullets) + speaker notes RICOS
- `enviado-para-leitura` (U4=3): slides DENSOS (4-6 bullets + dados inline + 1 quote curto) + speaker notes opcionais ou curtos
- `hibrido` (U4=4): meio-termo, ambos preenchidos

Preencher bloco `Conteúdo do slide (visível na projeção)` em cada slide, calibrado ao `modo_entrega`.

**2. `Layout sugerido` em cada slide** (regra 8 do schema): grid + tipografia + componentes visuais + animação. Sem isso, designer/Gamma/Claude Design/PowerPoint recebe o deck "no escuro".

**3. `[VERIFICAR]` em dados fabricados** (regra 9 do schema + `verificar-flag.md`): todo R$/%/n=/RCT/NPS/GRADE/CFO/Anvisa que a skill **inferir** (não veio do usuário; não é público canonicamente conhecido) recebe `[VERIFICAR: descrição]` inline ou em footnote. Lint v1.1 emite WARN quando ausente. Reviewer converte em 🟡 ou 🔴 no segundo passe.

**4. Bold opcional nos rótulos:** preferir `**Tipo:**`, `**Action title:**`, `**Mensagem-chave:**` para facilitar leitura visual. Lint aceita ambos formatos.

**Checklist v1.1 ao gerar cada slide:**
- [ ] `**Tipo:**`, `**Action title:**`, `**Mensagem-chave:**` em bold
- [ ] Bloco `Conteúdo do slide (visível na projeção)` preenchido com densidade adaptada ao `modo_entrega`
- [ ] Bloco `Layout sugerido` com grid + tipografia + componentes
- [ ] Dados específicos inferidos marcados com `[VERIFICAR: ...]`
- [ ] `Imagens sugeridas` no formato v1.1 (Quantidade explícita + variações em blocos separados)
