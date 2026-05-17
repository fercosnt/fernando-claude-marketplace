# Skeleton STORYBOARD — Modo `concept-reveal` (D3 pipeline cenografia)

Aplica Sparkline Duarte (oscilacao what-is/what-could-be) + Raskin (ancorar conceito em mudanca real).

**Pre-requisito (D3 LOCKED):** `skill-cenografia` JA rodou e gerou artefatos em pasta dedicada. Esta skill CONSOME artefatos — NAO projeta espaco.

---

```markdown
# Deck: {slug}

## Meta
- Skill geradora: deck-internal
- Objetivo unico: {U1}
- Audiencia: {U2 — board/diretoria, 5-10 pessoas mix analitico+intuitivo}
- Duracao: {U3} min (tipicamente 20-45)
- Formato: {U4}
- Big Idea: {U5/C2 — sensorial em 1 frase}
- Marca: {U6}
- Framework principal: Sparkline Duarte
- Modo: concept-reveal
- max_ctas: 1
- Anexo 6-pager: nao
- Artefatos cenografia: {C1 — path absoluto da pasta cenografia/<slug>/}
- Gerado em: {ISO date}
- Versao: v1
- Storyboard ID: STORYBOARD-{slug}-{YYYYMMDD-HHmm}

## Estrutura Narrativa

Sparkline Duarte com 2 vales antes do reveal (Jobs iPhone padrao).
Big Idea sensorial slide 2 (NAO slide 1 — capa mood evita revelar conceito cedo demais).
Walk-through em 1ª pessoa no slide 4 (REVEAL) — imersao sensorial obrigatoria.
Renders + mood-boards de cenografia carregados como visuais slides 3-6 (paths absolutos).
NAO duplicar trabalho cenografia — apenas apresentar.

## Slide 1 — Capa mood
Tipo: capa
Action title: {pergunta poetica que abre tensao, NAO descritivo}
Mensagem-chave: {1 frase de abertura — atmosfera, NAO o conceito ainda}
Speaker notes: 30-60s — atmosfera, criar expectativa sem revelar conceito
Visual: {path absoluto de mood-board-iluminacao.png ou similar de cenografia}
Prompt de imagem:
> {copia verbatim de prompts/nano-banana-pro-prompts.json caso exista para mood; senao deck-image-prompts whitelist}
Tempo estimado: 30-60s

## Slide 2 — Big Idea sensorial
Tipo: conceitual
Action title: {Big Idea U5/C2 em 1 frase poderosa}
Mensagem-chave: nomear o conceito SEM revelar a execucao ainda
Speaker notes: 60s — entregar Big Idea sem detalhar; criar curiosidade
Visual: minimalista (so texto, eventualmente fundo escuro)
Prompt de imagem: — (skip, ou minimalista via deck-image-prompts)
Tempo estimado: 60s

## Slide 3 — What is (status quo desconfortavel — Sparkline vale 1)
Tipo: problema
Action title: {realidade desconfortavel em 1 frase}
Mensagem-chave: experiencia generica vigente — sem alma, sem diferenciacao
Speaker notes: 90-120s — descrever experiencia atual de quem participa (chip mais caro, mesma comida, dezenas de eventos identicos). Raskin Status Quo + perdedores.
Visual: contraste com visao futura — eventualmente sem imagem (so texto sobre fundo)
Prompt de imagem: {deck-image-prompts capa fake "evento generico" — cenografia nao tem render disso}
Tempo estimado: 90-120s

## Slide 4 — What could be (REVEAL — Sparkline pico)
Tipo: conceitual
Action title: {nome do conceito + verbo de mudanca radical}
Mensagem-chave: {walk-through 1a pessoa em 1 frase}
Speaker notes: 120-180s — narracao 1ª pessoa:
"Voce chega. {nome IA/anfitriao} te chama pelo nome. Ela sabe que voce e fa do {referencia}, que voce gosta de {preferencia}. {experiencia sensorial — luz, som, textura}. {acao que transforma o momento}."
Pausa dramatica antes de revelar o nome do conceito.
Visual: **{path absoluto de renders/render-hero-*.png de cenografia}** — render principal
Prompt de imagem:
> {prompt verbatim de prompts/nano-banana-pro-prompts.json — copiar tudo, NAO regerar}
Tempo estimado: 120-180s

## Slide 5 — Detalhes sensoriais (Sparkline subida)
Tipo: conceitual
Action title: {detalhe que ancora qualidade do conceito}
Mensagem-chave: {2-3 detalhes do conceito — iluminacao, textura, som}
Speaker notes: 90-120s — descricao sensorial 1ª pessoa continua. Justificar cada elemento (NAO Pinterest sem curadoria).
Visual: {path absoluto de renders/render-detalhe-iluminacao.png + mood/mood-board-textura.png}
Prompt de imagem:
> {prompts verbatim do JSON cenografia para os artefatos}
Tempo estimado: 90-120s

## Slide 6 — Aplicacoes do conceito (Sparkline new bliss)
Tipo: conceitual
Action title: {extensao do conceito a outros pontos de contato}
Mensagem-chave: como o conceito se aplica em bar / area foto / sinalizacao / brindes
Speaker notes: 90s — coerencia em multiplos toques; conceito como sistema, NAO unico ponto
Visual: {renders bar-vip.png + area-foto.png ou similar — paths absolutos}
Prompt de imagem:
> {prompts verbatim do JSON cenografia}
Tempo estimado: 90s

## Slide 7 — Ask executivo
Tipo: CTA
Action title: {decisao + budget + cronograma}
Mensagem-chave: "Aprovar conceito hoje + liberar R$ {valor} + cronograma {prazo}"
Speaker notes: 60s — ask especifico (NUNCA "vamos discutir"); criterio de execucao
Visual: tabela orcamento split por categoria
Prompt de imagem: — (skip — tipo CTA fora whitelist D5)
Tempo estimado: 60s

## Slide 8 — Proximos passos
Tipo: CTA (continuacao)
Action title: Cronograma de execucao
Mensagem-chave: {3-5 marcos com owners — contrato fornecedores, mockup fisico, soft-launch}
Speaker notes: 30s
Visual: timeline
Prompt de imagem: — (skip)
Tempo estimado: 30s

## Apendice (opcional)
- A1 — Planta baixa cenografia (path layout/planta-baixa.svg)
- A2 — Materiais e fornecedores
- A3 — Comparativo com edicoes anteriores (se aplicavel)

## Storyboard de Imagens (handoff pra deck-image-prompts)

**IMPORTANTE:** Modo concept-reveal recebe imagens prontas de cenografia. deck-image-prompts e usado SO para:
- Slide 1 (capa mood adicional, se cenografia nao tem mood especifico para abertura)
- Slide 3 (capa fake "evento generico" — cenografia nao tem render disso)

Demais slides (4, 5, 6) consomem renders de cenografia com prompts ja gerados.

## Artefatos cenografia consumidos (D3 handoff)
- {path absoluto}/renders/render-hero-sala-vip-v2.png → slide 4
- {path absoluto}/renders/render-detalhe-iluminacao.png → slide 5
- {path absoluto}/mood/mood-board-textura.png → slide 5
- {path absoluto}/renders/render-bar-vip.png → slide 6
- {path absoluto}/renders/render-area-foto.png → slide 6
- {path absoluto}/prompts/nano-banana-pro-prompts.json → prompts verbatim

## Checklist de Revisao (handoff pra deck-reviewer)
- [ ] Sparkline correto: 2 vales antes do reveal (slide 3 = vale 1; slide 4 = pico)
- [ ] Big Idea sensorial slide 2 (NAO slide 1)
- [ ] REVEAL NAO esta na primeira secao
- [ ] Walk-through 1ª pessoa no slide 4
- [ ] Paths absolutos dos renders cenografia nos campos Visual: dos slides 4, 5, 6
- [ ] Prompts copiados VERBATIM do JSON cenografia (NAO regerados)
- [ ] Slide 7 Ask ESPECIFICO (valor + cronograma + decisao)
- [ ] CTA unico (max_ctas: 1)
- [ ] Frontmatter Meta tem `Artefatos cenografia: {path}`
- [ ] Mood board justificado (NAO Pinterest aleatorio)
- [ ] Fechamento de loop com problema slide 3

## Compliance & Disclaimers
{aplicar 3 tiers — atencao especial para claims sensoriais NAO mensuraveis}

🟡 Verificar antes:
- Promessas experienciais devem ser realistas com o budget aprovado
- Renders sao simulacao — execucao final pode ter pequenas variacoes
```
