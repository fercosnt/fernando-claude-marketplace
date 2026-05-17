# Anti-Cliches Stock — 8 a Banir + Alternativas

> Estudo AAAS Science documentou que IA reproduz os mesmos 12 motivos genericos quando prompts sao vagos — "visual elevator music". Especificidade radical e o antidoto.
> Fonte: AAAS Science "When creating images, AI keeps remixing the same 12 stock-photo cliches".

## Os 8 anti-padroes obrigatorios

| # | Anti-padrao | Por que evitar | `--no` / restricao | Alternativa criativa |
|---|-------------|----------------|---------------------|----------------------|
| 1 | **Handshake generico** | Artificial, impessoal, exausta para "parceria" | `handshake, two people shaking hands, business deal` | "Dynamic duo working side-by-side at shared workstation, genuine collaborative moment" |
| 2 | **Lightbulb = ideia** | Metafora exausta desde os 90s | `lightbulb, glowing bulb, idea icon` | "A spark igniting a constellation of interconnected nodes, isometric view, teal and gold" |
| 3 | **Engrenagens = processo** | Mecanicista, sem calor humano, cliche pre-2010 | `gears, cogwheels, mechanical system` | "River of light flowing through interconnected transparent chambers, isometric 3D" |
| 4 | **Sorriso forcado em mesa de reuniao** | Posado, diversidade tokenista | `forced smile, business meeting cliche, diverse team meeting` | "Candid overhead view of team collaborating on printed materials and laptops, hands visible, genuine focus" |
| 5 | **Setas crescentes em grafico** | Banal, descontextualizado | `upward arrow, growth chart, financial graph` | "Timelapse-style visualization of sapling growing into robust tree inside digital frame" |
| 6 | **Pessoa no topo de montanha bracos abertos** | Overused para "sucesso" | `mountaintop, arms outstretched, achievement pose, sunrise vista` | "Candid victory expression of marathon runner crossing finish line, raw authentic emotion" |
| 7 | **Road sign "OPPORTUNITY"** | Literalismo preguicoso | `road sign, signpost, way forward, opportunity arrow` | "Intriguing half-open door revealing warm golden light from dark corridor" |
| 8 | **Touchscreen flutuante "futuro"** | Datado, futurismo preguicoso | `holographic screen, floating UI, futuristic interface, glasses with HUD` | "Photorealistic interior of near-future office with ambient computing surfaces, warm human-centered design" |

## Lista expandida (banlist sempre)

Adicionar SEMPRE ao `negative:` de qualquer prompt corporativo:

```
stock photo feel, forced smile, artificial pose, handshake, lightbulb, gears, upward arrows,
business suit cliche, watermark, text overlay, uncanny valley skin, extra fingers,
distorted hands, plastic appearance, over-saturated colors, clip art aesthetic, dead eyes,
oversmile, diverse team high-five, road sign OPPORTUNITY, mountaintop arms-open
```

## Anti-uncanny obrigatorio (pessoas)

| Categoria | ✅ Pedir | ❌ Banir |
|-----------|---------|---------|
| Lente | "85mm f/1.8", "Canon EOS R5", "medium format 120mm" | — |
| Luz | "large softbox from camera left", "soft window light", "three-point lighting" | "flat overhead lighting" |
| Pele | "natural skin texture, subtle pores, slight asymmetry" | "plastic skin, waxy, poreless, beauty filter, airbrushed" |
| Emocao | "approachable yet authoritative", "warm professional confidence", "thoughtful focus" | "smiling", "happy" (genericos) |
| Composicao | "rule of thirds", "shallow DoF", "subject on right third" | "centered, symmetrical" (look amador) |
| Maos/dedos | (nada — IA falha) | "extra fingers, distorted hands, fused fingers" |
| Olhar | "engaged gaze, authentic expression" | "dead eyes, vacant stare, glassy" |

## Cliches por contexto especifico

### Clinico/medico

- ❌ Banir: `blood, syringes in focus, wounds, surgical scenes, distress, clinical harshness, anxiety expression, scary, sterile horror, white-coat-only`
- ✅ Pedir: `serene, relaxed, comfortable treatment chair, modern wellness clinic, soft neutral colors, gentle natural light, warm trusting atmosphere`
- ✅ Profissional: `friendly female/male doctor in their 40s, crisp white lab coat over navy scrubs, minimal jewelry, neat hairstyle, soft diffused light`

Protocolo paper PMC11692014:
1. **Descrever o que ESTA presente** (calma, conforto, luz suave) ANTES de negar o que nao quer
2. Contornar filtros via reframing: `"red-stained handkerchief"` em vez de `"blood"`
3. **NAO usar IA para diagnostico visual** (ECG, raio-X, anatomia precisa falham)

### Produto/equipamento

- ❌ Banir: `text, labels, stickers, fingerprints, dust, harsh shadows, reflections of crew, background clutter, wires, power cables, plastic look`
- ✅ Pedir: `hero product shot, three-point lighting setup, pure white studio background, dramatic side lighting, sharp focus, commercial product photography precision`

### Hero/capa abstrato

- ❌ Banir: `text, watermark, logo, people, faces, photo-realistic elements, heavy shadows, dark moody, busy cluttered composition`
- ✅ Pedir: `wide cinematic composition, three-layer depth, focal point center-left, premium brand aesthetic, ethereal volumetric light`

### Headshot profissional

- ❌ Banir: `tie cliche, stock photo feel, artificial smile, uncanny valley, oversmile, plastic skin, beauty filter, dead eyes`
- ✅ Pedir: `professional corporate headshot, [genero+idade range], navy blazer/professional attire, 85mm f/1.8 lens, soft window light from camera left, shallow depth of field bokeh, approachable yet authoritative atmosphere`

## Regra de ouro

> **Especificidade radical vence teoria generica.** Prompts com camera real, film stock, iluminacao tecnica, e estado emocional preciso produzem 3x mais resultados utilizaveis que prompts genericos. Em vez de `"professional businesswoman"`, escrever `"confident female tech entrepreneur, early 40s, navy blazer, natural genuine smile, 85mm f/1.8, soft window light from camera left, modern minimalist office background, approachable yet authoritative atmosphere, LinkedIn profile quality"`.
