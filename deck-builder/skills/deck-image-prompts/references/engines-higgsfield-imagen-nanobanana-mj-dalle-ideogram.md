# Engines — Sintaxe e Parametros (2026)

> Fonte: pesquisa `prompts-imagem-apresentacoes-corporativas-2026` (NB1 `7f1b2e2b`).
> Engines cobertas: Midjourney v7, Google Imagen 4, Nano Banana Pro (gemini-3-pro-image-preview), Higgsfield Soul/Soul 2.0, DALL-E 3/GPT-Image-1.5, Ideogram 3.0.

## Tabela comparativa rapida

| Engine | Modelo | Aspect ratios | Negative prompt | Character lock | Texto integrado |
|--------|--------|---------------|------------------|-----------------|-----------------|
| Midjourney v7 (V8.1 rollout) | v7 standard | qualquer via `--ar` | `--no` peso -0.5 | `--oref` (V7+) ou `--cref` (legacy) | 30-40% acuracia (fraco) |
| Google Imagen 4 / Fast / Ultra | imagen-4.0-{generate,fast,ultra}-001 | 1:1, 3:4, 4:3, 9:16, 16:9 (5 fixos) | **NAO suporta** desde v3.0-002 | nao nativo (migrar pra gemini-2.5-flash-image) | bom |
| Nano Banana Pro | gemini-3-pro-image-preview | 12+ incluindo 21:9 ultrawide | embutido em `CONSTRAINTS:` | **5 pessoas + 14 objetos** | excelente |
| Higgsfield Soul / Soul 2.0 | Soul 2.0 + Cinema Studio | 4:5, 9:16, 16:9 (3 principais) | apenas General Style/Flux | **Soul ID** (10-20 fotos) | medio |
| DALL-E 3 (aposentado mai/2026) | — | 1024², 1792×1024, 1024×1792 | embutido + tecnica "I NEED" | nao | medio |
| GPT-Image-1.5 (sucessor) | gpt-image-1.5 | 1024², 1024×1536, 1536×1024 | embutido (sem campo nativo) | nao nativo | excelente (autoregressive) |
| Ideogram 3.0 | v3 | 12 fixos (1:3, 9:16, 10:16, 2:3, 3:4, 4:5, 1:1, 4:3, 3:2, 16:9, 16:10, 3:1) | campo dedicado `negative_prompt` | `style_codes` hex 8 chars + 3 refs | **90-95% (lider)** |

## Arvore de decisao — Qual engine usar

```
Slide com TEXTO integrado (titulo, label, action title na imagem)?
├── SIM → Ideogram 3.0 (style_type: DESIGN, aspas no texto, magic_prompt: OFF)
└── NAO
    │
    ├── Precisa CHARACTER consistente em 5+ slides?
    │   ├── pessoa real treinada → Higgsfield Soul ID
    │   ├── multiplas pessoas + objetos → Nano Banana Pro (5+14)
    │   └── maior controle artistico → MJ v7 com --oref + --sref
    │
    ├── Precisa 4K NATIVO ou ultrawide 21:9?
    │   └── Nano Banana Pro (unico com 4K + 21:9)
    │
    ├── Workflow PROGRAMATICO via API com edicao contextual?
    │   └── GPT-Image-1.5 (autoregressive, melhor instruction-following)
    │
    ├── PRODUCAO em escala enterprise (lote 100+) com compliance?
    │   └── Imagen 4 Fast ($0.02/img) com Vertex AI + C2PA/SynthID
    │
    └── HERO IMAGE / lifestyle / mood / aesthetic curado?
        └── MJ v7 + --sref + --stylize 150-300 (padrao de referencia)
```

## Midjourney v7 — Sintaxe canonica 2026

```
/imagine [SUBJECT detalhado: genero+idade+vestuario+expressao]
         [COMPOSITION: lente+f-stop+angle]
         [ACTION/POSE: especifica, nao estatica]
         [LOCATION/ENVIRONMENT: descricao concreta]
         [LIGHTING: tecnica: softbox/window light/golden hour/natural diffused]
         [STYLE: editorial / documentary / cinematic / commercial photography]
         --ar 16:9
         --sref [CODE_OU_URL]
         --sw 100
         --oref [URL_PERSONAGEM]   # quando aplicavel
         --ow 100
         --stylize 150              # 50-100 fotorrealista, 150-300 editorial, 500+ artistico
         --chaos 0                  # 0 = coerente | 5-15 = variacao leve | 50+ = imprevisivel
         --seed [N]                 # fixar para serie consistente
         --v 7
         --no [lista anti-cliche + anti-uncanny]
```

### Parametros essenciais V7

| Parametro | Range | Quando usar |
|-----------|-------|-------------|
| `--ar` | qualquer ratio | sempre — formato do slide |
| `--sref [URL/code]` | URL ou numero | brand consistency — fixar estilo visual |
| `--sw` | 0–1000 (default 100) | peso da style reference; 50-100 = equilibrio, 500+ = dominante |
| `--oref [URL]` | URL | **substituto de `--cref` em V7** — bloqueia personagem/objeto (face+roupa+postura). Custa 2x GPU |
| `--ow` | 0–1000 (default 100) | peso da omni reference |
| `--cref [URL]` | URL | legado — usar `--oref` em V7 |
| `--stylize` / `--s` | 0–1000 (default 100) | 50-150 = corporativo realista; 200-300 = marketing editorial; 500+ = artistico |
| `--chaos` | 0–100 (default 0) | variacao entre as 4 imagens. Deck: manter 0 |
| `--no` | termos separados por virgula | negative prompt; **cada palavra independente** (peso -0.5) |
| `--seed [N]` | 0 a 4294967295 | reprodutibilidade entre geracoes |
| `--draft` | flag | 10x mais rapido, 0.5x custo. Iteracao |

### Regra de `--no` no MJ v7

`--no` tem peso -0.5 por padrao. Cada palavra e lida **independentemente**. NAO escreva `--no modern clothing` (vira "no modern" + "no clothing"). Liste itens individuais separados por virgula.

## Google Imagen 4 — Framework oficial

```
Subject + Context/Background + Style + Details

Exemplo expandido:
"A photo of [SUBJECT: professional team meeting], [ENVIRONMENT: in a modern glass office],
 [LIGHTING: natural window lighting], [CAMERA: shot with 50mm lens at f/2.8],
 [STYLE: contemporary minimalist aesthetic, warm color grading],
 [QUALITY: 4K HDR, taken by a pro photographer]"
```

### Vertex AI API key parameters

- `model`: `imagen-4.0-generate-001` / `imagen-4.0-fast-generate-001` / `imagen-4.0-ultra-generate-001`
- `aspect_ratio`: `1:1` | `3:4` | `4:3` | `9:16` | `16:9`
- `number_of_images`: 1–4
- `person_generation`: `allow_all` | `allow_adult` | `dont_allow`
- **Sem `negative_prompt`** desde v3.0-002 — embutir restricoes no prompt positivo

### Imagen 4 sem character lock nativo

Tatica: definir "style anchor description" verbatim e colar em **todos** os prompts da serie.

Exemplo: `warm editorial lifestyle photography with soft window light, shallow depth of field, warm neutral color palette, documentary feel`.

Para personagens recorrentes, migrar para `gemini-2.5-flash-image` (sucessor com character lock per doc Vertex AI).

## Nano Banana Pro — API + Thinking Mode

```python
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents="Professional team photo in modern office, cinematic lighting",
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        response_format={"image": {
            "aspect_ratio": "16:9",
            "image_size": "2K"   # ou "1K", "4K"
        }},
        thinking_config=types.ThinkingConfig(
            thinking_level="High"  # Low | Medium | High para instrucoes complexas
        )
    )
)
```

### Sintaxe estruturada (output desta skill usa esse formato)

```
[SUBJECT: descricao especifica]
[COMPOSITION: "16:9 canvas boundary"]
[CAMERA: "85mm f/2.0 aperture"]
[LIGHTING: "soft key light from upper left"]
[STYLE: "commercial photography"]
[CONSTRAINTS: "prohibit text overlay, prohibit geometric distortion, prohibit artificial poses, prohibit stock photo aesthetic"]
```

### Matriz 4K nativo

| Aspect Ratio | 1K | 2K | 4K |
|--------------|-----|-----|-----|
| 1:1 | 1024×1024 | 2048×2048 | **4096×4096** |
| 16:9 | 1024×576 | 2048×1152 | **4096×2304** |
| 9:16 | 576×1024 | 1152×2048 | **2304×4096** |
| 21:9 | 1024×439 | 2048×878 | **4096×1755** |

### Diferenciais

- **Thinking mode** Low/Medium/High pra instrucoes complexas
- **Google Search grounding** — imagens baseadas em dados em tempo real
- **Multi-turn editing**: "That's great, but make the lighting warmer"
- **14 imagens de referencia** + character lock 5 pessoas + 14 objetos

## Higgsfield Soul / Soul 2.0 — Framework 5 componentes

```
[Subject detalhado] + [Composition/camera] + [Action] + [Location/ambiente] + [Style]

Exemplo Soul:
"A confident female executive in tailored navy blazer, 85mm lens shallow depth of field,
 leaning forward during boardroom presentation, modern glass-walled office with city skyline,
 warm editorial photography aesthetic, golden hour natural light"
```

### Soul ID workflow (character lock treinado)

1. Upload de 10-20 fotos de alta qualidade da pessoa (angulos multiplos, evitar oculos escuros / sombras pesadas)
2. Treinamento: ~3-5 minutos
3. Avatar fica disponivel na aba "Character" do Soul 2.0
4. Reuso via parametro API: `custom_reference_id`
5. Compativel com 50-80+ presets esteticos (Y2K, Gorpcore, Quiet Luxury, Editorial Street Style, French Film Realism)

### Parametros API (Segmind/WaveSpeed)

- `style_strength`: 0.0–1.0 (0.5 sutil, 1.0 bold)
- `enhance_prompt`: bool (aprimoramento automatico)
- `seed`: -1 a 2147483647 (fixar para serie)
- `size`: ex `2048*1536`, `960*1696`, `1152*2048`
- **Negative prompt: sem parametro nativo** — restricoes no prompt. So General Style/Flux aceita.

## DALL-E 3 (aposentado) / GPT-Image-1.5 (sucessor)

**Importante:** DALL-E 3 foi aposentado em mai/2026. Toda referencia se aplica ao sucessor GPT-Image-1.5 (arquitetura autoregressive, nao difusao). Endpoint: `POST /v1/images/generations`.

```json
{
  "model": "gpt-image-1.5",
  "prompt": "Professional corporate headshot...",
  "size": "1024x1536",
  "quality": "high",
  "output_format": "png",
  "background": "auto",
  "moderation": "low"
}
```

### Controlar prompt rewriting

1. **API direta** (mais confiavel): endpoint `/v1/images/generations` sem ChatGPT como intermediario → sem reescrita automatica
2. **"I NEED" technique** (via ChatGPT/Responses API):
   ```
   I NEED to test how the tool works with extremely simple prompts.
   DO NOT add any detail, just use it AS-IS: [seu prompt]
   ```
3. **"Full Detail" technique**:
   ```
   My prompt has full detail so no need to add more: [seu prompt detalhado]
   ```
4. **"Do Not Modify" technique**:
   ```
   Do not modify the prompt. Generate exactly: [seu prompt]
   ```

> Nota: "I NEED" e lore de comunidade — funciona empiricamente, sem doc oficial. A doc oficial recomenda "instruct the relabeler in your prompt".

### Sem campo negative nativo

Estrategia: descrever o que ESTA + restricoes embutidas:
```
A photorealistic image of [subject]. Clean professional environment. Soft natural lighting.
No text overlays. No watermarks. Single subject only. Neutral background.
Professional corporate photography style. 16:9 widescreen format.
Avoid cluttered backgrounds, artificial poses, stock photo aesthetic.
```

## Ideogram 3.0 — Especialista em texto integrado

```
[Contexto da cena] with text reading "TEXTO_EXATO" in [estilo tipografico descritivo],
[background], [color palette], [layout]
```

### Regras de tipografia integrada

1. Posicionar **texto exato entre aspas duplas**: `"Q4 Strategy"`
2. Posicionar texto **no inicio do prompt** para prioridade
3. Descrever tipografia por propriedades, **nao nome de fonte**:
   - ✅ `"bold sans-serif"`, `"ultra thin bauhaus style"`, `"formal script with flourishes"`
   - ❌ `"in Helvetica"`, `"in Times New Roman"`
4. Texto curto >> texto longo (acuracia decai)
5. `magic_prompt: OFF` para precisao tipografica
6. Para corrigir erro ortografico: usar Editor com Remix

### API parameters

| Parametro | Valores |
|-----------|---------|
| `style_type` | `AUTO` / `GENERAL` / `REALISTIC` / **`DESIGN`** (slides) / `FICTION` |
| `rendering_speed` | `FLASH` / `TURBO` / `DEFAULT` / `QUALITY` |
| `magic_prompt` | `AUTO` / `ON` / **`OFF`** (typography precisa) |
| `negative_prompt` | texto livre |
| `seed` | integer |
| `style_codes` | hex 8 chars (incompativel com `style_reference_images`) |
| `aspect_ratio` | 12 fixos |

### Regra Ideogram

"Prompting 'a man without a beard' can result in a man with a beard." Sempre reescrever como positivo. "no people in the room" → "an empty room with chairs neatly arranged".

## Negative Prompt Libraries — Pronto pra copy

### MJ v7 — `--no` por contexto

**Universal corporate brand-safe:**
```
--no stock photo feel, forced smile, artificial pose, handshake, lightbulb, gears, upward arrows, business suit cliche, watermark, text overlay, uncanny valley skin, extra fingers, distorted hands, plastic appearance, over-saturated colors, clip art aesthetic, dead eyes, oversmile
```

**Hero / fundo abstrato:**
```
--no text, watermark, logo, people, faces, photo-realistic elements, heavy shadows, dark moody, busy cluttered composition
```

**Medico / clinico:**
```
--no blood, visible syringes, needles in focus, wounds, surgical scenes, distress expression, clinical harshness, medical tubes prominently displayed, horror aesthetic, anxiety, scary
```

**Produto / equipamento:**
```
--no text, labels, stickers, fingerprints, dust, harsh shadows, reflections of crew, background clutter, wires, power cables, plastic look
```

**Headshot profissional:**
```
--no tie, stock photo feel, artificial smile, uncanny valley, blurry background only, watermark, plastic skin, oversmile, distorted hands, extra fingers, dead eyes, beauty filter, airbrushed
```

### Higgsfield / Stable Diffusion — Universal photorealistic

```
worst quality, normal quality, low quality, low res, blurry, text, watermark, logo, banner, extra digits, distorted, pixelated, JPEG artifacts, compression artifacts, bad anatomy, bad hands, three hands, missing limbs, poorly drawn face, long neck, fused fingers, mutated, malformed, bad proportions, cartoon, cgi, 3d render, anime, cropped, out of frame, duplicate
```

**Add-on corporate brand-safe:**
```
stock photo, cheap, tacky, kitsch, amateur, clipart, generic, template preset, overexposed, underexposed, grainy excessive, noise, vignette excessive, chromatic aberration, plastic skin, waxy, poreless, beauty filter
```

### Imagen 4 / DALL-E 3 / GPT-Image-1.5 — Via prompt positivo

Sem campo negative. Embutir como restricoes positivas:

```
[Descricao completa da cena desejada]. Professional, high-quality, photorealistic.
4K HDR, taken by a pro photographer. Clean composition with no text overlays,
no watermarks, no cluttered backgrounds, no distracting elements.
The scene should feel authentic, not staged. Avoid stock photo aesthetic,
handshake cliches, forced smiles, artificial poses.
```

### Ideogram 3.0 — Campo dedicado

**Para tipografia corporativa limpa:**
```
gradients, bevels, drop shadows, decorative fonts, clipart, distorted text, 3D extrusion
```

**Para fotografia profissional:**
```
stock photo cliches, handshake, lightbulb, gears, forced smiles, artificial poses, watermark
```

## Brand consistency — Tactics

### MJ v7 — `--sref` + `--oref`

1. Gerar imagem master com prompt detalhado da identidade desejada
2. Usar `--sref random` → MJ atribui numero (ex: `--sref 4521983`)
3. Anotar numero, testar em 4-6 prompts distintos para verificar consistencia
4. Repos curados: [midlibrary.io](https://midlibrary.io), [sref-midjourney.com](https://sref-midjourney.com)

### Governança 3 tiers
- **Brand Core** — sempre aprovado, usar em tudo
- **Project-Specific** — aprovado para campanha X
- **Experimental** — em teste

### Higgsfield — Soul ID treinado

1. Upload 20+ fotos
2. Treinamento ~5 minutos
3. Disponivel em 20+ style presets
4. API: `custom_reference_id` no payload
5. Elimina re-upload em cada geracao

### Nano Banana Pro — Image references + Multi-turn

- Ate 14 imagens de referencia como input contextual
- Character lock: 5 pessoas + 14 objetos simultaneamente
- Multi-turn: "Mesma cena, mas com iluminacao mais quente"
- Image Search via referencia visual web

### Ideogram 3.0 — Style codes

1. Prompt Box → Style → My Styles → Create New Style → upload 3 imagens → nomear
2. Gera `style_code` hexadecimal 8 chars
3. Aplicar mesmo `style_code` em todos os assets
4. Imagens de referencia imutaveis apos criacao

### Paleta coerente em qualquer engine

**Hex codes no prompt** (Recraft, Nano Banana Pro suportam direto):
```
Brand identity color palette: primary #1A237E (indigo), secondary #FFAB00 (amber),
accent #E8EAF6 (light indigo). [Descricao da cena].
Ensure all visual elements respect this corporate color system.
```

**Ancoras descritivas** (qualquer engine): incluir string identica em toda a serie: `consistent color palette of warm concrete tones, black, and pale morning light`

**Seed fixo** (MJ + Ideogram + Higgsfield Soul): `--seed 12345` → variacoes da mesma composicao base
