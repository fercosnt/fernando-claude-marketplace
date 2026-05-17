---
name: deck-image-prompts
description: Gera prompts de imagem (MJ v7/Imagen 4/Nano Banana Pro/Higgsfield/DALL-E/Ideogram) para STORYBOARD em slides na whitelist D5. Plugin deck-builder ou direto via /deck-image-prompts.
intent: action
effort: medium
nb_ids:
  - 7f1b2e2b-4ba4-40de-ba56-ca2f55e2c0da
references:
  - references/engines-higgsfield-imagen-nanobanana-mj-dalle-ideogram.md
  - references/whitelist-por-tipo-slide.md
  - references/anti-cliches-stock.md
assets:
  - assets/templates/prompt-skeleton-por-engine.md
  - evals/image-prompts-cases.md
---

# deck-image-prompts

Skill auxiliar do plugin **deck-builder**. Gera prompts de imagem por engine (MJ v7, Google Imagen 4, Nano Banana Pro, Higgsfield Soul, DALL-E 3/GPT-Image-1.5, Ideogram 3.0) para preencher o campo `**Prompt de imagem:**` do STORYBOARD apenas em slides da whitelist (regra canonica D5).

## Quando ativa

**Modo encadeado (default — invocada por outra skill do plugin):**
Skills verticais (`deck-fundraising`, `deck-sales`, `deck-clinical`, `deck-equipment`, `deck-teaching`, `deck-proposal`, `deck-scientific`, `deck-internal`) chamam esta skill **depois** de gerar o STORYBOARD. Recebem uma lista de slides com tipo + brief + Big Idea e devolvem o bloco preenchido.

**Modo standalone (direto):**
`/deck-image-prompts` ou frases como "preciso de prompts pra capa do deck", "gera prompt MJ pra slide conceitual do Beauty Smile". Roda a entrevista IM1-IM5 abaixo.

## Whitelist por tipo de slide (D5 — regra canonica)

Detalhe e overrides em [references/whitelist-por-tipo-slide.md](references/whitelist-por-tipo-slide.md). Em uma frase:

- **Preencher prompt:** `capa` | `problema` | `conceitual` | `comparativo` | `demo` | `prova-social`
- **Skip por default:** `dados` | `financeiro` | `CTA` | `disclaimer` | `agradecimento` | `apendice`
- **Override `deck-scientific`:** inclui `dados` (graficos cientificos sao imagens)
- **Override usuario:** `--include-dados` ou `--exclude-prova-social`

**Quando o tipo cai em "Skip":** retornar exatamente `skip — tipo {tipo} fora da whitelist (D5)` e gravar `**Prompt de imagem:** —` no STORYBOARD. NAO inventar prompt.

## Engines suportadas

| Engine | Forte para | Aspect ratio default | Negative prompt |
|--------|-----------|---------------------|------------------|
| Midjourney v7 | hero / lifestyle / mood / character lock | 16:9 / 4:5 / 1:1 | `--no` (peso -0.5) |
| Google Imagen 4 | editorial / fotorealismo / escala | 16:9 / 9:16 / 1:1 / 4:3 / 3:4 | **NAO suporta nativo** — embutir restricoes no prompt positivo |
| Nano Banana Pro (gemini-3-pro-image-preview) | 4K nativo / 21:9 / mockup layout-aware / brand consistency / character lock 5+14 | 16:9 / 21:9 / 1:1 / 9:16 | bloco `CONSTRAINTS:` |
| Midjourney v7 com `--sref`/`--oref` | brand-safe recorrente | 16:9 / 4:5 | `--no` |
| DALL-E 3 / GPT-Image-1.5 (sucessor mai/2026) | brand-safe / didatico | 16:9 / 1:1 | **NAO suporta nativo** — restricoes embutidas + tecnica "I NEED" |
| Higgsfield Soul / Soul 2.0 | cinematic / motion / Soul ID character treinado | 16:9 / 4:5 / 9:16 | apenas em General Style/Flux — senao embutido |
| Ideogram 3.0 | type-in-image (action title embutido) / iconografia | 16:9 / 1:1 / 9:16 | campo dedicado `negative_prompt` |

Detalhes de sintaxe por engine em [references/engines-higgsfield-imagen-nanobanana-mj-dalle-ideogram.md](references/engines-higgsfield-imagen-nanobanana-mj-dalle-ideogram.md).

## Entrevista (so modo standalone)

Pular essas perguntas no modo encadeado — a skill que chama ja passou os dados.

- **IM1:** Tipo de slide (capa / problema / conceitual / comparativo / demo / prova-social / outro). Se "outro" cair em skip → retornar skip.
- **IM2:** Marca alvo (auto-detect §10.5 do SHARED.md). Se marca tiver `design_system_skill` declarado e instalado → carrega tokens (paleta hex, fontes implicitas, mood) e injeta nos prompts.
- **IM3:** Estilo desejado (cinematic / editorial / technical / minimal / organic / quiet-luxury / heritage). Default: editorial.
- **IM4:** Engine principal (1 obrigatorio + 2 opcionais como fallback). **Default quando nenhuma e nomeada:** Higgsfield + Imagen 4 + Nano Banana Pro.
- **IM5:** Aspect ratio (16:9 default; 4:5 headshot; 9:16 story; 21:9 banner — so Nano Banana Pro).

## Protocolo de execucao

1. **Receber input** — lista de slides {tipo, action_title, mensagem_chave, visual_brief, big_idea, marca} ou entrevista IM1-IM5.
2. **Filtrar pela whitelist D5** (incluindo override scientific e flags do usuario). Marcar SKIPs.
3. **Auto-detect marca** se nao recebida explicitamente. Se `design_system_skill` carregado, ler tokens.
4. **Consultar NB1** se houver duvida especifica sobre sintaxe de engine ou padrao para o tipo de slide. Query exemplo:
   ```bash
   notebooklm use 7f1b2e2b-4ba4-40de-ba56-ca2f55e2c0da
   notebooklm ask "Sintaxe MJ v7 cinematic editorial portrait pitch deck cover Big Idea = {U5}" --max-citations 5
   ```
   Se NB falhar → degrade com warning, NAO bloqueia.
5. **Gerar 3 versoes por slide whitelisted** — engines diferentes da matriz IM4, cada uma com:
   - Prompt detalhado (30-60 palavras), em ingles tecnico
   - Linha `negative:` (ou `constraints:` se engine nao suporta — sempre presente, mesmo que reescrita como positivo)
   - Aspect ratio explicito
   - Brand tokens injetados se marca tem design system
6. **Aplicar guardrails** (proxima secao) e disclaimers de contexto (clinico → TCLE, anvisa-laser → sem promessa de "cura").
7. **Devolver bloco Markdown** no formato do output (proxima secao) pronto pra colar no STORYBOARD.

## Formato de output (v1.1 — reformatado para clareza visual + handoff designer)

Por slide whitelisted, devolver bloco `**Imagens sugeridas:**` no formato abaixo. **Mudança v1.1:** cada variação fica em bloco markdown separado (não inline com `>`) com campos labeled (Engine / Aspect ratio / Estilo / Composição / Prompt / Negative / Mood ref). Quantidade declarada explicitamente no header.

```markdown
**Imagens sugeridas:**

> **Quantidade:** 1 imagem hero (3 variações para o designer escolher) | OU: N imagens distintas (uma para cada componente do slide)

**Variação A — Higgsfield Soul**
- Aspect ratio: 16:9
- Estilo: cinematic editorial
- Composição: rule-of-thirds, subject 1/3 esquerda, espaço negativo direita, lente 35mm
- Prompt: {prompt em ingles, 30-60 palavras com SUBJECT + ENVIRONMENT + LIGHTING + MOOD + brand color hex se aplicavel}
- Negative: stock-photo aesthetic, AI-look, generic faces, watermarks, plastic skin
- Mood ref (opcional): {link, painel mood ou descricao de mood ja conhecida}

**Variação B — Imagen 4**
- Aspect ratio: 16:9
- Estilo: editorial documental
- Composição: center, espaço negativo superior, lente 50mm
- Prompt: {prompt em ingles — incluir restricoes como positivo porque Imagen 4 nao tem negative nativo}
- Constraints (embutido — Imagen 4 nao tem negative): no text overlays, no watermarks, no stock photo aesthetic, no harsh fluorescent
- Mood ref (opcional): —

**Variação C — Nano Banana Pro** (recomendado quando há `design_system_skill` instalado)
- Aspect ratio: 16:9
- Estilo: mockup brand-aware
- Composição: full-bleed com overlay sutil para brand tokens (SUBJECT / COMPOSITION / CAMERA / LIGHTING / STYLE estruturado)
- Prompt: {prompt estruturado SUBJECT/COMPOSITION/CAMERA/LIGHTING/STYLE com brand tokens injetados se aplicavel}
- CONSTRAINTS: prohibit text overlay, prohibit artificial poses, prohibit cliche tech imagery
- Mood ref (opcional): {tokens de design_system_skill se carregado — paleta hex, fontes, mood}
```

**Regras invioláveis do output (v1.1):**
- **Header `Quantidade:` obrigatório** — declara explicitamente se são 3 variações da mesma imagem (default) OU N imagens distintas (raro, só quando slide pede composição multi-imagem).
- **Cada variação em bloco markdown separado** com `**Variação A/B/C — {Engine}**` como header — facilita o designer copiar pra ferramenta dele sem misturar config com prompt.
- **6 campos por variação:** Aspect ratio / Estilo / Composição / Prompt / Negative (ou Constraints) / Mood ref (pode ser "—").
- **Sempre 3 variações** (a menos que usuario peça menos via flag) com engines diferentes.
- **Negative/Constraints em TODAS as 3 versões**, mesmo quando a engine não tem campo nativo (reescrever como positivo ou listar como `constraints` embutidos).
- **Aspect ratio sempre explícito** em cada variação.
- **Composição com direção concreta** (rule-of-thirds, center, split-50, full-bleed, etc.) — NÃO genérico ("editorial restraint" sozinho não é composição).
- **Slides em skip:** linha única `**Imagens sugeridas:** — (slide sem imagem hero por whitelist D5)` + comentário HTML `<!-- skip — tipo {tipo} fora da whitelist (D5) -->`.

### Migração do formato v1.0 → v1.1

Formato v1.0 (deprecated mas ainda aceito pelo lint):
```markdown
**Prompt de imagem:**
> Higgsfield (cinematic, 16:9): {prompt}
>   negative: {...}
```

Formato v1.1 (recomendado — mais legível, melhor handoff):
```markdown
**Imagens sugeridas:**

> **Quantidade:** 1 imagem hero (3 variações)

**Variação A — Higgsfield Soul**
- Aspect ratio: 16:9
- Estilo: cinematic editorial
- Composição: rule-of-thirds
- Prompt: {prompt}
- Negative: {...}
```

Skills verticais v1.1 emitem o formato novo. Skill standalone aceita flag `--legacy-format` pra ainda emitir v1.0 se o usuário quiser.

## Guardrails

### Anti-cliches stock (lista completa em [references/anti-cliches-stock.md](references/anti-cliches-stock.md))

Banir em todos os prompts: handshake generico, lightbulb-as-idea, engrenagens-como-processo, equipe rindo em volta de mesa, setas crescentes em grafico, pessoa no topo de montanha bracos abertos, road sign "OPPORTUNITY", touchscreen flutuante "futuro". Sao 8 anti-padroes documentados pelo AAAS Science. Sempre incluir esses termos no `negative:` ou reescrever como alternativa criativa.

### Brand consistency entre slides do mesmo deck

Se o deck tem >1 slide whitelisted, usar o **mesmo** style anchor em todos:
- **MJ v7:** mesmo `--sref [URL/codigo]` + mesmo `--sw 100` + mesmo `--seed N` em toda a serie.
- **Higgsfield:** mesmo Soul ID treinado se ha personagem recorrente; senao mesmo preset estetico.
- **Nano Banana Pro:** mesma `image reference` ancora ou mesma string de estilo verbatim.
- **Imagen 4:** sem `--sref` nativo — colar "style anchor description" verbatim em todos os prompts.
- **Ideogram 3.0:** mesmo `style_code` (hex 8 chars) em toda a serie.

### Anti-uncanny (pessoas)

Sempre incluir lente real (`85mm f/1.8`, `Canon EOS R5`), luz tecnica (`large softbox from camera left`), emocao precisa (`approachable yet authoritative` — nao so "smiling"), e banir: `plastic skin, waxy, dead eyes, artificial smile, perfect symmetry, oversmile, extra fingers, distorted hands`.

### Compliance medico/clinico

Quando marca tem `compliance_tags` (ex: `anvisa-laser-classe-iii`, `cfo-cfm`, `odontologia-br`):
- **Sempre descrever positivo primeiro** (paciente sereno, ambiente acolhedor, luz suave) ANTES de banir o negativo. Protocolo PMC11692014.
- **Banir:** `blood, visible syringes, needles in focus, wounds, surgical scenes, distress expression, clinical harshness, anxiety, scary`.
- **Sem promessa visual de "cura"/resultado dramático** — preferir "tratamento sendo aplicado" a "antes vs depois super agressivo".
- **Antes/depois:** marcar `<!-- TCLE obrigatorio + disclaimer "Resultados podem variar" -->` no bloco e gerar disclaimer text no Ideogram quando aplicavel.

### Brand tokens (se design_system_skill instalado)

Se a marca tem `design_system_skill` declarado no `~/.config/deck-builder/brands.yaml` (ex: `beauty-smile-design-system`) e a skill esta instalada localmente:
- Ler tokens (paleta hex, fontes implicitas, mood).
- Injetar hex codes no prompt: `color palette: #{hex1}, #{hex2}, #{hex3}`.
- Injetar mood verbatim: `aesthetic: {mood}`.
- Marcar `<!-- brand tokens injetados de {design_system_skill} -->` no bloco.

### Falha graceful

- **NB indisponivel:** segue com defaults canonicos da pesquisa — emite warning `<!-- NB1 indisponivel; defaults aplicados -->`.
- **design_system_skill nao instalado:** segue sem tokens — emite warning `<!-- design system {nome} nao instalado; brand tokens pulados -->`.
- **Engine nomeada nao reconhecida:** cai pro default Higgsfield + Imagen 4 + Nano Banana Pro com warning.

## Defaults

- **Engines default** (quando nenhuma e nomeada): **Higgsfield + Imagen 4 + Nano Banana Pro**.
- **Aspect ratio default:** 16:9.
- **Estilo default:** editorial.
- **Numero de versoes:** 3 (sem flag pra reduzir nesta versao da skill).

## Templates pronto-para-copy

Skeletons por engine prontos em [assets/templates/prompt-skeleton-por-engine.md](assets/templates/prompt-skeleton-por-engine.md). Usar como ponto de partida e preencher com o brief do slide.

## Eval cases

4 cases em [evals/image-prompts-cases.md](evals/image-prompts-cases.md):
1. Capa pitch Beauty Smile (tipo `capa` whitelist) — 3 versoes + tokens design system
2. Demo clinico Fotona Er:YAG (tipo `demo` whitelist) — compliance anvisa-laser
3. Antes-e-depois clareamento (tipo `comparativo` whitelist) — TCLE + tom clinico
4. Slide financeiro fundraising (tipo `financeiro` SKIP) — retorna skip, nao gera prompt

## Limites

- NAO renderiza a imagem — so escreve o prompt.
- NAO valida output visual — funcao do `deck-reviewer`.
- NAO chama API paga.
- NAO altera o STORYBOARD fora do campo `**Prompt de imagem:**` por slide.
- NAO faz post de redes sociais (delega `/copy`).
- NAO projeta cenografia/espaco fisico (delega `skill-cenografia` — D3).
- Cita NB1 ate 3 hits maximos; falha de NB nao bloqueia.

## Referencias

- [references/engines-higgsfield-imagen-nanobanana-mj-dalle-ideogram.md](references/engines-higgsfield-imagen-nanobanana-mj-dalle-ideogram.md) — sintaxe + parametros das 6 engines (MJ v7, Imagen 4, Nano Banana Pro, GPT-Image-1.5, Higgsfield Soul, Ideogram 3.0).
- [references/whitelist-por-tipo-slide.md](references/whitelist-por-tipo-slide.md) — 14 tipos canonicos + override scientific + flags do usuario.
- [references/anti-cliches-stock.md](references/anti-cliches-stock.md) — 8 anti-padroes documentados + alternativas criativas.
- [assets/templates/prompt-skeleton-por-engine.md](assets/templates/prompt-skeleton-por-engine.md) — 6 skeletons copy-paste.
- [evals/image-prompts-cases.md](evals/image-prompts-cases.md) — 4 eval cases.
