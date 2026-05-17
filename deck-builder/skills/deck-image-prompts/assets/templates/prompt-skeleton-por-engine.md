# Prompt Skeletons por Engine — Copy-Paste

> Use como ponto de partida. Substituir `{placeholders}` com brief especifico do slide.

## Midjourney v7

### Capa / Hero (mood abstract)

```
/imagine Wide cinematic hero background for {marca} corporate presentation,
{descricao da metafora visual}, {paleta principal — ex: deep navy and gold},
editorial magazine aesthetic, premium brand feel
--ar 16:9 --s 200 --v 7
--no text, watermark, logo, people, faces, stock photo feel, busy cluttered composition
```

### Pessoa profissional (headshot/lifestyle)

```
/imagine Professional corporate {headshot/lifestyle} of {genero} {profissao}, {idade range},
wearing {vestuario}, {expressao precisa — ex: approachable yet authoritative},
shot with 85mm f/1.8 lens, soft window light from camera left,
{ambiente: modern minimalist office background with shallow depth of field bokeh},
clean color grading, LinkedIn profile quality
--ar 4:5 --s 150 --v 7
--no tie, stock photo feel, artificial smile, uncanny valley, blurry, watermark,
plastic skin, oversmile, distorted hands, extra fingers, dead eyes
```

### Conceitual / metafora

```
/imagine Visual metaphor for {conceito}, {descricao concreta — ex: a luminous castle with energy
shield moat protecting a glowing city of data nodes}, isometric view,
{paleta — ex: teal and deep blue}, cinematic lighting
--ar 16:9 --s 200 --v 7
--no text, generic icons, gears, lightbulb, clipart, handshake, upward arrows
```

### Medico/clinico — Profissional de saude

```
/imagine Professional healthcare portrait, friendly {genero} doctor in their 40s
wearing crisp white lab coat over navy scrubs, minimal jewelry, neat hairstyle,
soft diffused window light, modern outpatient clinic background with clean neutral walls,
warm and trustworthy mood, approachable professional expression, 85mm lens, shallow DoF
--ar 4:5 --s 150 --v 7
--no blood, wounds, syringes, medical equipment prominently displayed, distress,
pain expression, harsh lighting, uncanny, scary clinical environment
```

### Medico/clinico — Paciente sereno em tratamento

```
/imagine A relaxed {genero} in their {idade}s seated in a comfortable treatment chair
receiving {tratamento — ex: IV infusion}, modern wellness clinic with soft neutral colors
beige and taupe, soothing minimalist room, gentle natural light from window,
calm and trusting expression, healthcare professional partially visible in background,
lifestyle healthcare photography
--ar 16:9 --s 180 --v 7
--no blood, visible needles, medical tubes in focus, clinical harshness, anxiety expression, scary
```

### Tecnico / equipamento (hero product shot)

```
/imagine Professional studio hero shot of {equipamento},
{cor/acabamento — ex: clinical white and silver finish}, placed on clean white surface,
dramatic side lighting creating precise highlights on device edges,
subtle reflection on polished surface below, modern medical aesthetics,
technical product photography, sharp focus, three-point lighting setup
--ar 16:9 --s 200 --v 7
--no text, labels, wires, clutter, fingerprints, dust, plastic appearance
```

### Antes/depois (split screen)

Workflow: gerar 2 imagens com mesmo `--seed`, combinar em Figma.

```
# Painel ANTES
/imagine {descricao "antes" — ex: a cluttered chaotic urban office space, harsh fluorescent
lighting, paper stacks, stressful atmosphere}, editorial photography style
--ar 16:9 --s 150 --v 7 --seed 12345

# Painel DEPOIS (mesmo seed!)
/imagine {descricao "depois" — ex: the same space transformed into a modern minimalist
workspace, natural light, clean surfaces, calm productive atmosphere}, editorial photography style
--ar 16:9 --s 150 --v 7 --seed 12345
```

Disclaimer obrigatorio (rodar separado no Ideogram): `"Results may vary"` em sans-serif limpo.

### Brand consistency entre slides

Em TODOS os slides do mesmo deck, manter:
```
--sref [URL_da_master_image]  # mesmo codigo
--sw 100                       # mesmo peso
--seed [N_fixo]                # mesmo seed
--chaos 0                      # zero variacao
--v 7
```

## Google Imagen 4

### Hero/capa

```
Wide cinematic hero background for a {marca} corporate presentation,
soft gradient from {cor1} to {cor2}, abstract light rays emanating from center-left,
minimalist geometric shapes, 4K HDR, taken by a pro photographer,
photorealistic, professional and elegant mood. No text overlays, no watermarks,
clean composition, premium brand aesthetic.

aspect_ratio: 16:9
person_generation: dont_allow
```

### Pessoa profissional

```
Professional corporate headshot, {genero} executive in their {idade}s,
neutral light gray background, navy business attire, confident approachable expression,
studio lighting with large softbox from camera left, sharp focus on face,
f/2.8 depth of field, 85mm lens, 4K HDR, taken by a pro photographer,
realistic skin texture with natural pores, Kodak Portra 400 film stock aesthetic.

aspect_ratio: 9:16
person_generation: allow_adult
```

### Equipamento (especular)

```
Commercial product photography of a {equipamento}, pure white studio background,
three-point lighting setup, sharp focus on device details, reflections on glossy surface,
professional equipment photography aesthetic, 4K HDR, commercial advertising quality,
shot on Hasselblad X2D. No text overlays, no labels, no fingerprints, clean composition.

aspect_ratio: 16:9
```

### Style anchor verbatim (brand consistency)

Em **todos** os prompts da serie, colar identico:
```
warm editorial lifestyle photography with soft window light, shallow depth of field,
warm neutral color palette, documentary feel, premium brand aesthetic
```

## Nano Banana Pro (gemini-3-pro-image-preview)

### Hero abstract

```
SUBJECT: Abstract corporate hero composition with flowing light streams for {marca}
COMPOSITION: 16:9 canvas boundary, three-layer depth effect, focal point center-left
CAMERA: ultra-wide cinematic lens, depth of field at infinity
LIGHTING: ethereal volumetric light from upper left
STYLE: minimalist editorial, premium brand aesthetic, 4K resolution
CONSTRAINTS: prohibit text overlay, prohibit human figures, prohibit recognizable objects,
prohibit watermarks, prohibit stock photo aesthetic
```

### Headshot LinkedIn

```
SUBJECT: Professional LinkedIn headshot, {genero, idade, descritor de etnia},
wearing professional suit/blazer with crisp collar visible
COMPOSITION: head and shoulders framing with face taking 60% of frame,
rule of thirds composition
CAMERA: Canon EOS R5 85mm f/1.8
LIGHTING: even professional lighting with no harsh shadows, golden hour studio lighting
STYLE: clean solid light gray background NOT blurred, bokeh background, approachable confident demeanor
CONSTRAINTS: prohibit artificial smile, prohibit plastic skin, prohibit uncanny valley,
prohibit oversmile, prohibit beauty filter, prohibit watermarks
```

### Mockup brand-consistent

```
SUBJECT: {produto/cena} consistent with {marca} brand
COMPOSITION: 16:9 canvas, focal point as per rule of thirds, three-layer depth
CAMERA: {especificar lente e angle}
LIGHTING: {especificar}
STYLE: matching brand identity color palette: primary #{hex1}, secondary #{hex2},
accent #{hex3}. Premium brand aesthetic, editorial polish
CONSTRAINTS: prohibit text overlay (will be added in design tool),
prohibit stock photo cliches, prohibit artificial poses
REFERENCES: [up to 14 image refs for brand consistency]
```

## Higgsfield Soul / Soul 2.0

### Framework 5 componentes

```
[Subject detalhado] + [Composition/camera] + [Action] + [Location/ambiente] + [Style]
```

### Cinematic executive portrait

```
A confident {genero} executive in tailored navy blazer,
85mm lens shallow depth of field,
leaning forward during boardroom presentation,
modern glass-walled office with city skyline,
warm editorial photography aesthetic, golden hour natural light

style_strength: 0.8
seed: {fixar para serie}
size: 1152*2048
```

### Soul ID (character treinado — quando aplicavel)

```
{custom_reference_id treinado}, {acao + ambiente + estilo},
{preset estetico — ex: Quiet Luxury / Warm Ambient / French Film Realism}

custom_reference_id: {ID_treinado}
style_strength: 0.7
seed: {fixar}
```

## DALL-E 3 / GPT-Image-1.5

### Tecnica "Full Detail"

```
My prompt has full detail so no need to add more: A photorealistic image of {subject}.
{Ambiente detalhado}. {Luz tecnica}. {Composicao}. {Estilo}.
No text overlays, no watermarks, no stock photo aesthetic.
Single subject focus. Professional corporate photography style. 16:9 widescreen format.
Avoid cluttered backgrounds, artificial poses, handshake cliches.
```

### Tecnica "I NEED" (forca prompt as-is)

```
I NEED to test how the tool works with extremely simple prompts.
DO NOT add any detail, just use it AS-IS: {seu prompt detalhado completo}
```

### Tecnica "Do Not Modify"

```
Do not modify the prompt. Generate exactly: {seu prompt detalhado completo}
```

## Ideogram 3.0

### Slide com action title embutido

```
Conceptual corporate infographic with title "TEXTO EXATO" in bold sans-serif at top:
{descricao da cena}. Color palette: #{hex1} and #{hex2}.
Clean vector illustration, flat design.
```

Settings:
- `style_type: DESIGN`
- `magic_prompt: OFF`
- `aspect_ratio: 16:9`
- `negative_prompt: gradients, bevels, drop shadows, decorative fonts, clipart, distorted text, 3D extrusion`

### Disclaimer text (para antes/depois)

```
Clean minimalist banner reading "Results may vary" in elegant ultra-thin sans-serif,
centered alignment, neutral cream background, subtle texture, premium brand feel,
generous negative space around text.
```

Settings:
- `style_type: DESIGN`
- `magic_prompt: OFF`
- `aspect_ratio: 16:9`

### Hero com headline

```
Cinematic hero background for {marca} pitch deck with headline reading "BIG IDEA TEXT"
in bold modern sans-serif, positioned upper left third,
{descricao do background visual}, {paleta hex}, premium editorial aesthetic.
```

Settings:
- `style_type: DESIGN`
- `magic_prompt: OFF`
- `aspect_ratio: 16:9`
- `style_codes: {hex_8_chars_aprovado_pra_marca}`

## Tabela de aspect ratios

| Formato | MJ | Imagen 4 | Nano Banana Pro | Ideogram | Uso |
|---------|-----|----------|-----------------|----------|-----|
| 16:9 | `--ar 16:9` | ✅ | ✅ | ✅ (1312×736) | Keynote/Slides padrao |
| 4:3 | `--ar 4:3` | ✅ | ✅ | ✅ (1152×864) | Projetor legado/PDF |
| 9:16 | `--ar 9:16` | ✅ | ✅ | ✅ (736×1312) | Stories/TikTok |
| 1:1 | `--ar 1:1` | ✅ | ✅ | ✅ (1024×1024) | Avatar/thumbnail |
| 4:5 | `--ar 4:5` | ❌ | ✅ | ✅ (896×1120) | Headshot LinkedIn |
| 21:9 | `--ar 21:9` | ❌ | ✅ **unico** | ❌ | Banner ultra-wide |

## Combine engines — workflow deck completo

```
ETAPA 1 — IDENTIDADE VISUAL
  Brief: paleta hex, mood, fonte hint, formato
  Moodboard 5-8 imagens
  Master image MJ v7 — aprovar

ETAPA 2 — SISTEMA DE REFERENCIA
  MJ: --sref random + anotar codigo + validar em 4-6 testes
  Higgsfield: treinar Soul ID se personagem recorrente
  Ideogram: criar style_code + 3 imagens
  Documentar code + preview + uso

ETAPA 3 — POR TIPO DE SLIDE
  Capa/Hero       → MJ v7 + --sref + --s 200 + --ar 16:9
  Pessoa Profis.  → MJ v7 + --oref + --sref --ar 4:5 OU Higgsfield Soul ID
  Conceitual      → MJ v7 + --sref + --s 150
  Medico/Clinico  → MJ v7 + protocolo PMC11692014 (positivo + --no)
  Tecnico/Produto → MJ v7 (--s 160) OU Imagen 4 Ultra (especular)
  Antes/Depois    → MJ v7 com --seed fixo em 2 geracoes + Figma combine
  Lifestyle       → MJ v7 + --s 180 OU Imagen 4
  SLIDE COM TEXTO → Ideogram 3.0 DESIGN + aspas + magic_prompt: OFF

ETAPA 4 — CONSISTENCIA & FINISHING
  Verificar: paleta coerente em todos os slides
  Verificar: mesmo --sref code em todas as geracoes
  Verificar: anti-padroes cliche ausentes
  Pos-processamento: Photoshop para correcao de maos/dedos
  Disclaimers brand-safe via Ideogram

ETAPA 5 — EXPORT
  Upscale 2x quando necessario (MJ Subtle Upscaler)
  PNG 16:9 para Keynote/Google Slides
  Arquivar prompts em governanca
```
