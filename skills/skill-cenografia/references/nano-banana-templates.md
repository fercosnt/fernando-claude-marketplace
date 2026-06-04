# Nano Banana Pro - Templates e JSON para Geracao de Imagens

Referencia principal do VISION para criar renders fotorealistas de espacos de eventos.

## Indice

1. [Regras Fundamentais](#regras-fundamentais)
2. [Sistema de Referencia de Imagens por Nome](#sistema-de-referencia-de-imagens-por-nome)
3. [Template Master - Categorias Cinematograficas](#template-master---categorias-cinematograficas)
4. [JSON Templates (A, B, C)](#json-templates)
5. [Templates de Prompt por Tipo de Evento](#templates-de-prompt-por-tipo-de-evento)
6. [Aspect Ratio por Uso](#aspect-ratio-por-uso)
7. [Dicas por Marca](#dicas-por-marca)
8. [Como Converter Imagem para Base64](#como-converter-imagem-para-base64)

---

## Regras Fundamentais

- Prompts SEMPRE em ingles — modelos de imagem tem training predominantemente em ingles, produzindo resultados mais fieis ao prompt
- Pedir "photorealistic photograph" (nunca "render" ou "3D") — termos como "render" ativam estilos de computacao grafica, produzindo resultados artificiais em vez de fotorrealistas
- Descrever cena narrativamente, nao listar keywords soltas — descricoes narrativas produzem composicoes mais coerentes porque o modelo entende relacoes espaciais e contexto
- Quanto mais especifico, melhor o resultado — detalhes como angulo de camera, lente e temperatura de cor reduzem ambiguidade e o modelo nao precisa "adivinhar"
- Ate 14 imagens de referencia total (6 objetos + 5 humanos) — limite da API Gemini para inline_data parts por request
- Image sizes: `"1K"`, `"2K"`, `"4K"` (UPPERCASE obrigatorio) — a API rejeita lowercase, gerando erro silencioso
- Aspect ratios: `"1:1"`, `"2:3"`, `"3:2"`, `"3:4"`, `"4:3"`, `"4:5"`, `"5:4"`, `"9:16"`, `"16:9"`, `"21:9"`
- Modelos: `gemini-2.5-flash-image` (velocidade) ou `gemini-3-pro-image-preview` (qualidade pro)
- responseModalities: `["TEXT", "IMAGE"]` — obrigatorio incluir ambos para que o modelo retorne tanto a imagem quanto descricao textual

---

## Sistema de Referencia de Imagens por Nome

Quando o usuario enviar imagens de referencia, cada uma deve ser referenciada pelo seu papel:

### Imagens de Espaco (ambiente base)
```
"Referencing the attached image of the event space [NOME_IMAGEM],
transform this venue into a [BRAND] [EVENT_TYPE] experience..."
```

### Imagens de Objetos (mobiliario, equipamentos, decoracao)
```
"Place the [OBJECT_NAME] shown in the attached reference image exactly
as depicted, maintaining its exact proportions, materials and colors.
Position it at [LOCATION] in the space."
```

### Imagens de Marca (logos, patterns)
```
"Integrate the [BRAND] logo from the attached reference image prominently
on [SURFACE], maintaining exact proportions and colors."
```

Cada imagem de referencia = um `inline_data` part separado no JSON.

---

## Template Master - Categorias Cinematograficas

Cada prompt segue esta estrutura de categorias. Selecionar opcoes adequadas ao projeto:

```
[SUBJECT & CONCEPT]
A photorealistic interior photograph of [descricao detalhada da cena]

[REFERENCE IMAGES]
- Space reference: [nome/descricao da imagem do espaco]
- Object references: [lista de objetos com instrucoes de posicionamento]
- Brand assets: [logos, patterns com instrucoes de integracao]

[SHOT TYPES]
Establishing wide shot | Medium shot | Close-up | Detail shot | Aerial/isometric | Panoramic

[CAMERA ANGLES]
Eye-level | Low angle (dramatico) | High angle (overview) | Bird's eye (top-down) |
Dutch angle (dinamico) | 3/4 elevated angle

[CAMERA & LENSES]
24mm wide-angle (espaco completo) | 35mm standard (equilibrado) |
50mm detail (foco medio) | 85mm vignette (bokeh)
f/1.8 (shallow DOF, bokeh) | f/5.6 (equilibrado) | f/11 (tudo nitido)

[COMPOSITIONS]
Rule of thirds | Center-weighted | Leading lines | Symmetry |
Natural framing | Golden ratio

[LIGHTING]
Natural daylight streaming through windows | Golden hour warm backlighting |
Three-point professional setup | Dramatic uplighting on walls |
Rim light separating subject from background | Backlit panels creating glow |
Neon accent lighting in brand colors | LED perimetral outlining structures |
Gobo projection of logos/patterns | Kinetic moving light elements |
Warm ambient 3000K | Cool corporate 5000K | Mixed temperatures

[COLOR GRADING]
Warm cinematic golden tones | Cool corporate blue undertones |
Muted luxury desaturated elegance | Vibrant festival saturated colors |
Kodak Portra 400 film warmth | Clean and bright editorial |
Desaturated premium quiet luxury | High contrast dramatic

[ENVIRONMENTS & SCENERY]
Indoor convention center | Outdoor beach resort | Indoor premium hotel ballroom |
Mixed open-air covered | Rooftop terrace | Community center | Industrial warehouse

[MATERIALS & TEXTURES]
Backlit white acrylic | Natural light wood (freijo, oak) | Brushed gold metal |
Cream velvet upholstery | Raw concrete | Tempered glass | Neon tubing |
Draped linen fabric | Marble with dramatic veins | Polished travertine

[WEATHER & TIME]
Golden hour (warm, long shadows) | Blue hour (cool, atmospheric) |
Night with designed artificial lighting | Midday diffused soft light |
Overcast even illumination | Sunset orange glow

[ACTIONS & MOVEMENTS]
Empty showcase (clean, catalog) | People networking casually |
Visitors exploring with curiosity | Medical treatment in progress |
Cocktail reception | Panel discussion | Wellness session

[EMOTIONS & EXPRESSIONS]
Premium relaxed sophistication | Engaged curious exploration |
Celebratory vibrant energy | Professional focused attention |
Intimate wellness calm | Community warmth and joy

[QUALITY & OUTPUT]
4K resolution, photorealistic, architectural photography, editorial quality,
magazine-worthy, professional interior photography
```

---

## JSON Templates

### Template A: Sem Imagem de Referencia

```json
{
  "contents": [
    {
      "parts": [
        {
          "text": "[PROMPT COMPLETO EM INGLES]"
        }
      ]
    }
  ],
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"],
    "imageConfig": {
      "aspectRatio": "16:9",
      "imageSize": "4K"
    }
  }
}
```

### Template B: Com Imagem do Espaco

```json
{
  "contents": [
    {
      "parts": [
        {
          "text": "[PROMPT REFERENCIANDO A IMAGEM DO ESPACO]"
        },
        {
          "inline_data": {
            "mime_type": "image/jpeg",
            "data": "<<< COLE BASE64 DA IMAGEM DO ESPACO AQUI >>>"
          }
        }
      ]
    }
  ],
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"],
    "imageConfig": {
      "aspectRatio": "16:9",
      "imageSize": "4K"
    }
  }
}
```

### Template C: Multiplas Referencias (espaco + objetos + marca)

```json
{
  "contents": [
    {
      "parts": [
        {
          "text": "[PROMPT REFERENCIANDO TODAS AS IMAGENS POR PAPEL]"
        },
        {
          "inline_data": {
            "mime_type": "image/jpeg",
            "data": "<<< BASE64: IMAGEM DO ESPACO >>>"
          }
        },
        {
          "inline_data": {
            "mime_type": "image/png",
            "data": "<<< BASE64: OBJETO 1 (ex: sofa, equipamento) >>>"
          }
        },
        {
          "inline_data": {
            "mime_type": "image/png",
            "data": "<<< BASE64: OBJETO 2 >>>"
          }
        },
        {
          "inline_data": {
            "mime_type": "image/png",
            "data": "<<< BASE64: LOGO DA MARCA >>>"
          }
        }
      ]
    }
  ],
  "generationConfig": {
    "responseModalities": ["TEXT", "IMAGE"],
    "imageConfig": {
      "aspectRatio": "16:9",
      "imageSize": "4K"
    }
  }
}
```

---

## Templates de Prompt por Tipo de Evento

### 1. Stand / Booth Design

```
[SUBJECT & CONCEPT]
A photorealistic interior photograph of a [BRAND] exhibition stand at a
[EVENT_TYPE] trade show event. The stand measures [W]m x [D]m x [H]m with
[N] open sides.

[REFERENCE IMAGES]
- Space reference: [venue/floor plan image]
- Object references: [specific furniture, equipment to place]
- Brand assets: [logo, branded materials]

[SHOT TYPES]
Establishing wide shot showing the complete stand within the exhibition hall

[CAMERA ANGLES]
3/4 elevated angle, capturing both the stand layout and the surrounding event context

[CAMERA & LENSES]
24mm wide-angle lens, f/5.6 for balanced sharpness across the stand

[COMPOSITIONS]
Rule of thirds with the main brand wall on the left third, reception area centered

[LIGHTING]
Professional exhibition lighting with LED perimetral outlining the stand structure,
backlit brand panels creating a warm halo effect, spot lighting on product displays,
warm ambient 3000-3500K throughout

[COLOR GRADING]
Clean and bright editorial with subtle warmth, premium corporate feel

[ENVIRONMENTS & SCENERY]
Indoor convention center with visible but soft-focus neighboring stands in background

[MATERIALS & TEXTURES]
[Brand-specific materials from fotona-brand.md or relevant brand]

[WEATHER & TIME]
Indoor artificial lighting, daytime event atmosphere

[ACTIONS & MOVEMENTS]
Visitors exploring the stand with curiosity, a few people at the reception counter,
soft-focus crowd in the background creating busy event atmosphere

[EMOTIONS & EXPRESSIONS]
Engaged curious exploration, professional focused attention

[QUALITY & OUTPUT]
4K resolution, photorealistic, architectural photography, trade show photography
style, editorial quality, magazine-worthy composition
```

### 2. Camarote / VIP Space

```
[SUBJECT & CONCEPT]
A photorealistic photograph of a premium VIP lounge/camarote for [BRAND]
at [EVENT_NAME]. Total area approximately [SIZE]m2, [OPEN/COVERED/MIXED].

[REFERENCE IMAGES]
- Space reference: [venue photo or floor plan]
- Object references: [specific furniture pieces, bar equipment]
- Brand assets: [logo for backdrop, branded items]

[SHOT TYPES]
Establishing wide shot capturing the full lounge atmosphere

[CAMERA ANGLES]
Eye-level perspective from the entrance, inviting the viewer into the space

[CAMERA & LENSES]
24mm wide-angle, f/2.8 for slight background softness while keeping foreground sharp

[COMPOSITIONS]
Leading lines from entrance through the lounge to the main backdrop

[LIGHTING]
Golden hour warm backlighting mixed with designed artificial lighting, neon accent
in brand colors, warm ambient uplighting on textured walls, soft LED strip lighting
under bar counter, ring light embedded near photo opportunity zone

[COLOR GRADING]
Warm cinematic with golden tones, premium evening atmosphere, Kodak Portra warmth

[ENVIRONMENTS & SCENERY]
[Indoor/outdoor/mixed] premium event venue, [beach/city/resort] context visible

[MATERIALS & TEXTURES]
[Brand-specific: velvet seating, gold accents, natural wood, draped fabric]

[WEATHER & TIME]
Golden hour transitioning to evening, warm natural light mixed with artificial

[ACTIONS & MOVEMENTS]
People enjoying cocktails in the lounge, a small group at the photo backdrop,
bartender preparing drinks, relaxed premium atmosphere

[EMOTIONS & EXPRESSIONS]
Premium relaxed sophistication, intimate social atmosphere

[QUALITY & OUTPUT]
4K resolution, photorealistic, event photography, editorial lifestyle quality
```

### 3. Brand Activation / Experiencia Imersiva

```
[SUBJECT & CONCEPT]
A photorealistic photograph of an immersive brand activation space for [BRAND]
themed "[CONCEPT_NAME]". The activation takes visitors through a [NARRATIVE]
journey from entrance to exit.

[REFERENCE IMAGES]
- Space reference: [venue image]
- Object references: [installations, interactive elements, equipment]
- Brand assets: [logo, patterns, brand colors reference]

[SHOT TYPES]
Medium shot capturing the immersive environment with a visitor interacting

[CAMERA ANGLES]
Low angle looking up for dramatic perspective, emphasizing scale and impact

[CAMERA & LENSES]
24mm wide-angle, f/2.8 for atmospheric depth

[COMPOSITIONS]
Center-weighted with the hero installation as focal point, framed by brand elements

[LIGHTING]
Dramatic theatrical lighting, color drenching the entire space in [BRAND_COLOR],
gobo projection of brand pattern on floor, neon signage as hero light source,
backlit translucent panels, strategic spotlights on interaction points

[COLOR GRADING]
High contrast dramatic with brand-dominant color, saturated and immersive

[ENVIRONMENTS & SCENERY]
[Venue type], fully transformed into brand universe, no original venue visible

[MATERIALS & TEXTURES]
[Brand-specific + special: LED screens, projection surfaces, interactive displays]

[WEATHER & TIME]
Controlled indoor environment, dramatic artificial lighting only

[ACTIONS & MOVEMENTS]
Visitors exploring with wonder, someone taking a selfie at the Instagram moment,
someone interacting with the brand installation

[EMOTIONS & EXPRESSIONS]
Engaged curious exploration, wow-factor excitement, discovery

[QUALITY & OUTPUT]
4K resolution, photorealistic, immersive experience photography, editorial quality
```

### 4. Before/After Transformation

```
[SUBJECT & CONCEPT]
Create a side-by-side before-and-after transformation of an event space.

BEFORE (left side):
- Empty [VENUE_TYPE] space, raw walls, basic floor, industrial ceiling
- No decoration or branding, neutral overhead lighting
- Keep the original attached reference image as base

AFTER (right side):
- Fully transformed [BRAND] event space with:
  [WALL_TREATMENT], [FLOORING], [FURNITURE], [BRAND_ELEMENTS],
  [LIGHTING_DESIGN], [DECORATIVE_ELEMENTS]

[SHOT TYPES]
Wide establishing shot, identical framing both sides

[CAMERA ANGLES]
Eye-level, same exact perspective in both images

[CAMERA & LENSES]
24mm, f/8 for uniform sharpness across the entire frame

[COMPOSITIONS]
Symmetrical split-screen, clean dividing line

[QUALITY & OUTPUT]
4K resolution, split-screen format, architectural before/after photography,
professional quality. The transformation should demonstrate dramatic impact.
Aspect ratio: 16:9
```

### 5. Detail Vignette (Close-Up)

```
[SUBJECT & CONCEPT]
A photorealistic close-up vignette of [SPECIFIC_ELEMENT] at a [BRAND] event space.
Focus on [detailed description of hero element and surrounding objects].

[REFERENCE IMAGES]
- Object references: [exact items to show in the vignette]
- Brand assets: [branded items visible: napkin, coaster, card]

[SHOT TYPES]
Close-up detail shot, product/styling photography

[CAMERA ANGLES]
Slightly elevated 3/4 angle, intimate perspective

[CAMERA & LENSES]
50mm or 85mm lens, f/1.8 for beautiful shallow depth of field with creamy bokeh

[COMPOSITIONS]
Rule of thirds with hero object at intersection point, natural framing

[LIGHTING]
Soft directional light from [DIRECTION], warm fill, gentle shadows creating depth

[COLOR GRADING]
Muted luxury desaturated elegance, intimate premium atmosphere

[MATERIALS & TEXTURES]
[Detailed: brushed gold tray, linen napkin, crystal glass, fresh flowers, etc.]

[WEATHER & TIME]
[Golden hour / soft evening / morning light] for warmth

[ACTIONS & MOVEMENTS]
Still life composition, no people, curated arrangement

[EMOTIONS & EXPRESSIONS]
Intimate, curated, luxurious, premium

[QUALITY & OUTPUT]
4K resolution, photorealistic, interior styling photography, editorial quality.
Aspect ratio: 1:1 (Instagram) or 4:5
```

### 6. Planta Baixa 3D / Vista Aerea

```
[SUBJECT & CONCEPT]
An isometric 3D architectural visualization of a [BRAND] event space layout
seen from above at a 45-degree angle. Space dimensions: [W]m x [D]m.

Zone layout from entrance:
1. [ZONE_1]: [position, size, key elements]
2. [ZONE_2]: [position, size, key elements]
3. [ZONE_3]: [position, size, key elements]

[SHOT TYPES]
Aerial/isometric view, architectural diagram style

[CAMERA ANGLES]
Bird's eye at 45-degree isometric angle

[CAMERA & LENSES]
Orthographic projection feel, 35mm equivalent, f/11 everything sharp

[COMPOSITIONS]
Center-weighted, full layout visible, clean edges

[LIGHTING]
Soft even illumination from above, gentle shadows for depth, no harsh contrasts

[COLOR GRADING]
Clean and bright, architectural visualization palette

[MATERIALS & TEXTURES]
Photorealistic materials but clean and readable: [wood floors, carpet zones,
wall colors matching brand palette]

[WEATHER & TIME]
Neutral daylight simulation, no dramatic shadows

[ACTIONS & MOVEMENTS]
Empty layout, clean catalog view showing spatial organization

[QUALITY & OUTPUT]
4K resolution, architectural visualization, clean white background,
isometric perspective, professional architectural rendering quality.
Aspect ratio: 4:3
```

---

## Aspect Ratio por Uso

| Uso | Aspect Ratio | Template |
|-----|-------------|----------|
| Vista geral panoramica | 16:9 | Stand, Camarote, Activation |
| Instagram feed | 1:1 ou 4:5 | Vignette, Detail |
| Instagram stories/reels | 9:16 | Qualquer template adaptado |
| Apresentacao/deck | 4:3 ou 16:9 | Stand, Planta, Before/After |
| Ultra-wide / banner | 21:9 | Panoramicas, headers |
| Before/After | 16:9 | Template 4 |
| Planta 3D | 4:3 | Template 6 |

---

## Dicas por Marca

### Fotona
Enfatizar: "premium", "sophisticated", "clean technology", "quiet luxury"
Iluminacao: warm golden accents, white dominant, backlit panels
Materiais: white acrylic, brushed gold, light wood, cream velvet
Atmosfera: "The space feels like walking into a premium wellness sanctuary"

### Beauty Smile
Enfatizar: "modern", "welcoming", "transformative", "innovative"
Iluminacao: turquoise+deep blue ambient, glass morphism effects
Materiais: glass, smooth surfaces, gradient lighting
Atmosfera: "A modern dental wellness experience with cutting-edge design"

### Carnaval 360
Enfatizar: "vibrant", "warm", "festive", "community", "dignified"
Iluminacao: warm saturated colors, red and yellow dominant
Materiais: colorful fabrics, organic textures, accessible furniture
Atmosfera: "A celebratory healthcare space that honors samba culture"

---

## Como Converter Imagem para Base64

Instrucoes para o usuario:

**Opcao 1 - Terminal (Mac/Linux):**
```bash
base64 -i imagem.jpg | pbcopy
```

**Opcao 2 - Python:**
```python
import base64
with open("imagem.jpg", "rb") as f:
    print(base64.b64encode(f.read()).decode())
```

**Opcao 3 - Online:**
Usar sites como base64-image.de ou base64.guru/converter/encode/image

Colar o resultado no campo `"data"` do `inline_data` correspondente no JSON.
