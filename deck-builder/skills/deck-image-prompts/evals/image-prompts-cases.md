# Eval Cases — deck-image-prompts

> 4 cases (3 minimo DoD §13.6 + 1 do skip case financeiro). Cada case: input → esperado → criterios de PASS.

---

## Case 1 — Capa pitch Beauty Smile (tipo `capa` whitelist)

### Input

```yaml
modo: encadeado
slide:
  tipo: capa
  action_title: "Como provar que dentista premium escala como rede de butique"
  mensagem_chave: "Beauty Smile e a tese fundadora de odontologia premium escalavel"
  visual_brief: "interior de clinica boutique premium + portrait Dr. Fernando founder"
  big_idea: "Beauty Smile prova que dentista premium escala como rede de butique"
  marca: "Beauty Smile"
flags: {}
```

### Esperado

Bloco `**Prompt de imagem:**` com **3 versoes**, cada uma com `negative:` ou `constraints:`:

```markdown
**Prompt de imagem:**
> **Higgsfield Soul** (cinematic, 16:9): {prompt de interior boutique clinic + warm editorial cinematography aesthetic + Beauty Smile palette tokens}
>   negative: stock photo feel, plastic skin, harsh fluorescent lighting, sterile clinical look, AI-uncanny
> **Imagen 4** (editorial, 16:9): {prompt editorial portrait Dr. Fernando founder + 85mm + softbox + Kodak Portra 400}
>   constraints (embutido — Imagen 4 sem campo negative): no text overlays, no watermarks, no stock photo aesthetic, single subject focus
> **Nano Banana Pro** (mockup brand-consistent, 16:9): SUBJECT/COMPOSITION/CAMERA/LIGHTING/STYLE/CONSTRAINTS estruturado + paleta hex Beauty Smile (se design system instalado)
>   CONSTRAINTS: prohibit text overlay, prohibit cliche tech imagery, prohibit handshake, prohibit lightbulb
<!-- brand tokens injetados de beauty-smile-design-system | NB1 consultado: padrao MJ v7 editorial portrait -->
```

### Criterios de PASS

- [ ] 3 versoes geradas (Higgsfield + Imagen 4 + Nano Banana Pro)
- [ ] **Cada versao tem `negative:` ou `constraints:`** (mesmo Imagen 4 com restricoes embutidas)
- [ ] Cada versao especifica aspect ratio (16:9)
- [ ] Brand tokens da Beauty Smile injetados (paleta hex ou nota se design system nao instalado)
- [ ] Sem cliches stock (handshake, lightbulb, gears, etc.)
- [ ] Prompt MJ inclui `--ar 16:9 --s 200 --v 7 --no [lista]` ou skeleton equivalente
- [ ] Prompt Imagen 4 NAO tem campo `negative_prompt:` (engine nao suporta)
- [ ] Prompt Nano Banana Pro segue formato `SUBJECT:/COMPOSITION:/CAMERA:/LIGHTING:/STYLE:/CONSTRAINTS:`
- [ ] Comentario HTML `<!-- -->` indica origem dos tokens / NB consultado

---

## Case 2 — Demo clinico Fotona Er:YAG (tipo `demo` whitelist)

### Input

```yaml
modo: encadeado
slide:
  tipo: demo
  action_title: "Er:YAG nao queima, ablaciona — por isso paciente nao sente"
  mensagem_chave: "Demo de procedimento de clareamento com Er:YAG sem desconforto"
  visual_brief: "paciente sereno + equipamento LightWalker + dentista posicionando handpiece"
  big_idea: "Tratamentos a laser elevam a percepcao de premium do paciente"
  marca: "Fotona"
  compliance_tags: [anvisa-laser-classe-iii, cfo-laser]
flags: {}
```

### Esperado

```markdown
**Prompt de imagem:**
> **Imagen 4 Ultra** (editorial healthcare, 16:9): {paciente sereno em treatment chair + modern wellness clinic + soft neutral colors + dentist partially visible positioning handpiece + lifestyle healthcare photography}
>   constraints (embutido): no blood, no visible needles in focus, no clinical harshness, no anxiety expression, no scary aesthetic, no promise of "miraculous cure" visual
> **Midjourney v7** (lifestyle clinical, 16:9): /imagine A relaxed patient in their 40s seated in comfortable treatment chair receiving laser procedure, modern wellness clinic with soft neutral colors, gentle natural light, calm trusting expression, dentist partially visible in background positioning Fotona LightWalker handpiece, lifestyle healthcare photography --ar 16:9 --s 180 --v 7 --no blood, visible needles, medical tubes in focus, clinical harshness, anxiety expression, scary, dramatic before-after promise, "cure" implication
> **Nano Banana Pro** (mockup-aware, 16:9): SUBJECT/COMPOSITION/CAMERA/LIGHTING/STYLE/CONSTRAINTS estruturado com equipamento LightWalker em foco secundario
>   CONSTRAINTS: prohibit blood, prohibit visible needles, prohibit anxiety expression, prohibit "miraculous result" visual implication, prohibit clinical harshness, prohibit text overlay
<!-- compliance anvisa-laser-classe-iii aplicado: sem promessa visual de "cura" ou resultado dramatico | TCLE de imagem ilustrativa obrigatorio | NB1 consultado: protocolo PMC11692014 -->
```

### Criterios de PASS

- [ ] 3 versoes geradas com paciente sereno (NAO sofrendo)
- [ ] **Todas as 3 incluem ban explicito de `blood, syringes, distress, clinical harshness, anxiety`**
- [ ] Comentario HTML `<!-- -->` cita compliance `anvisa-laser-classe-iii`
- [ ] Comentario HTML inclui nota sobre TCLE obrigatorio
- [ ] Nenhuma versao usa linguagem de "cura miraculosa" ou "transformacao dramatica"
- [ ] Protocolo PMC11692014 aplicado: positivo primeiro, depois bane negativo

---

## Case 3 — Antes-e-depois clareamento (tipo `comparativo` whitelist)

### Input

```yaml
modo: encadeado
slide:
  tipo: comparativo
  action_title: "8 sessoes — sem aplicacao de quimica externa"
  mensagem_chave: "Antes vs depois de clareamento Er:YAG (8 sessoes)"
  visual_brief: "split-screen antes/depois de sorriso clareado"
  big_idea: "Tratamentos a laser elevam percepcao de premium"
  marca: "Fotona"
  compliance_tags: [anvisa-laser-classe-iii, cfo-laser]
flags: {}
```

### Esperado

```markdown
**Prompt de imagem:**
> **Imagen 4** (editorial split-screen, 16:9): {split-screen composition + left panel: pre-treatment smile with subtle yellowing + right panel: same patient post-treatment with naturally lighter smile + identical lighting and framing + divided by thin vertical line + clinical documentary photography + soft natural light}
>   constraints (embutido): no exaggerated bleaching white, no Hollywood smile, no perfect symmetry, no makeup-style filter, no "miraculous" implication, no text overlays (disclaimer rendered separately)
> **Midjourney v7** (split-screen, 16:9): /imagine Split-screen composition: left panel shows a natural smile with subtle dental yellowing, right panel shows the same patient post-treatment with naturally lighter smile, identical lighting and framing in both panels, divided by clean thin vertical line at center, clinical documentary photography style --ar 16:9 --s 150 --v 7 --seed 12345 --no exaggerated bleaching, Hollywood smile, perfect symmetry, makeup filter, watermark, "miracle" implication
> **DALL-E 3 / GPT-Image-1.5** (brand-safe, 16:9): My prompt has full detail so no need to add more: A photorealistic side-by-side comparison image. Left half: a natural patient smile with subtle dental yellowing in a clinical setting with soft window light. Right half: the same patient post-clareamento with naturally lighter smile, same lighting, same framing, same camera angle. Divided by a thin vertical white line. Editorial documentary photography style. No text overlays, no exaggerated bleaching, no Hollywood smile, no "miracle" implication. Clean professional dental documentation.
<!-- TCLE obrigatorio + disclaimer "Resultados podem variar" — gerar separado no Ideogram (style_type: DESIGN, magic_prompt: OFF) | compliance anvisa-laser + cfo-laser aplicado | NB1 consultado: split-screen workflow MJ com --seed fixo + Figma combine -->
```

### Criterios de PASS

- [ ] 3 versoes geradas (Imagen 4 + MJ + DALL-E/GPT-Image)
- [ ] **MJ usa `--seed [N]` fixo para garantir consistencia de iluminacao/enquadramento**
- [ ] Tom clinico (NAO cosmetico exagerado/Hollywood smile)
- [ ] **Comentario HTML cita TCLE + disclaimer "Resultados podem variar"** e indica gerar separado no Ideogram
- [ ] Nenhuma versao promete "cura" / resultado garantido / "miracle"
- [ ] Restricao explicita contra `exaggerated bleaching, Hollywood smile, makeup filter`
- [ ] Comentario cita compliance `anvisa-laser-classe-iii` e `cfo-laser`

---

## Case 4 — Slide financeiro fundraising (tipo `financeiro` SKIP)

### Input

```yaml
modo: encadeado
slide:
  tipo: financeiro
  action_title: "Use of funds: 60% expansao, 25% R&D protocolo, 15% S&M"
  mensagem_chave: "Allocacao do round R$500k"
  visual_brief: "—" # vertical sabe que nao pede prompt
  big_idea: "Beauty Smile prova que dentista premium escala como rede de butique"
  marca: "Beauty Smile"
flags: {}
```

### Esperado

```markdown
**Prompt de imagem:** —
<!-- skip — tipo financeiro fora da whitelist (D5) -->
```

**Comportamento adicional:** skill devolve mensagem `skip — tipo financeiro fora da whitelist (D5)` ao chamador (modo encadeado) ou ao usuario (modo standalone). A vertical (`deck-fundraising`) confirma o skip e cola `**Prompt de imagem:** —` no STORYBOARD.

### Criterios de PASS

- [ ] **NENHUM prompt gerado** (nao inventa imagem ilustrativa para slide financeiro)
- [ ] Linha exata `**Prompt de imagem:** —` no campo
- [ ] Comentario HTML explica o motivo (whitelist D5)
- [ ] Mensagem de retorno `skip — tipo financeiro fora da whitelist (D5)` enviada ao chamador
- [ ] NAO oferece "quer que eu gere mesmo assim?" — skip e definitivo (a menos que flag `--include-financeiro` venha no input)

---

## Validacao integrada

Apos os 4 cases passarem:

1. STORYBOARD do Walkthrough 1 (Beauty Smile pitch anjo, 13 slides Sequoia + Raskin) deve ter:
   - **Slides 1, 2, 4, 5, 11 (capa/problema/conceitual/equipe/CTA)** → bloco preenchido com 3 versoes
   - **Slide financeiro** → `**Prompt de imagem:** —`
2. Comentarios `<!-- -->` permitem auditoria do `deck-reviewer`.
3. Nenhum cliche stock aparece em nenhum prompt.
4. Brand tokens Beauty Smile aplicados de forma consistente entre slides.

## Cliche check (todos os cases)

Grep do output gerado contra anti-padroes proibidos (do `references/anti-cliches-stock.md`):

```bash
grep -iE "handshake|lightbulb|gear[s]?|upward arrow|growth chart|mountaintop|road sign OPPORTUNITY|holographic screen|forced smile|diverse team high-?five" output.md
```

Deve retornar **vazio** (ou apenas dentro de blocos `negative:` ou `--no` — onde eles devem aparecer banidos).
