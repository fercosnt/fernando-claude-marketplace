# Prompts de imagem — padrao visual Fotona

Guia para gerar imagens (Higgsfield, Midjourney, Flux, Imagen, DALL·E) que parecam feitas pelo mesmo time que produz o feed do @fotonalaser, o midia kit e as apresentacoes comerciais.

Fonte: analise de 6 apresentacoes do Canva (Midia Kit, Linha editorial, Fotona4GLOW, GLP1Tight × Dr. Luann Lobo, ATP Reboost, MelasmaRecovery, Meu Primeiro Fotona) e da grade do Instagram em set/2026. Cores medidas por amostragem dos slides.

---

## 1. A assinatura visual em uma frase

**Preto absoluto, carmesim profundo e um unico vermelho vivo, com luz de palco vermelha sobre equipamentos brancos e pessoas reais.** Sofisticado, cinematografico, quase editorial de moda; **nunca "clinica branca com azul"**.

## 2. Paleta medida nos materiais

| Papel | Hex | Onde aparece |
|-------|-----|--------------|
| Preto de fundo | `#000000` · `#0C0202` | 50–60% de todo slide escuro |
| Carmesim 900 | `#1F0003` | primeiro degrau do gradiente, cantos |
| Carmesim 800 | `#3A0009` | meio-tom do gradiente |
| Carmesim 700 | `#5F0503` | brilho do gradiente, esferas |
| Carmesim 600 | `#7D0000` | halos, luz de palco no chao |
| Carmesim 500 | `#9C130D` | ponto mais claro do gradiente, fumaca iluminada |
| Vermelho Fotona | `#ED1C24` | barra inferior de 24 px (1920 × 1080), pilulas, ponto do logo, palavra em destaque |
| Off-white | `#F5F4F1` | fundo dos slides claros (tabelas, antes/depois) |
| Branco | `#FFFFFF` | texto sobre escuro, equipamentos |

Gradiente padrao dos fundos escuros: `linear-gradient(135deg, #000000 0%, #1F0003 40%, #5F0503 75%, #9C130D 100%)`, quase sempre com um **halo radial** carmesim vindo de um canto ou de cima.

## 3. Os cinco cenarios que se repetem

1. **Equipamento no palco.** Aparelho Fotona (corpo branco/prata) centralizado sobre chao escuro refletivo, 1 a 3 cones de luz vermelha vindos de cima, nevoa vermelha baixa, fundo preto. As vezes sobre um podio/cilindro vermelho.
2. **Retrato cinematografico.** Paciente ou medica em fundo preto, luz principal vermelha lateral ou rim light vermelho, pele com brilho natural, expressao serena ou confiante, roupa preta, vermelha ou branca. Enquadramento de moda editorial.
3. **Esfera/lente de luz.** Grande esfera translucida vermelha com o wordmark "Fotona" dentro, brilho suave, fundo preto (slide de transicao). Variante: tecido de seda vermelha em movimento.
4. **Antes e depois.** Fundo off-white ou preto, duas fotos clinicas em molduras arredondadas lado a lado, pilulas "ANTES" e "DEPOIS", faixa vermelha lateral. **Fotos reais, nunca geradas.**
5. **Detalhe de corpo/pele.** Close de pele, maos, perna, abdomen com luz vermelha rasante e fundo escuro, sem rosto, tratamento fotografico e nao ilustrativo.

## 4. Prompt-base (ingles, funciona melhor nos modelos)

```
Cinematic editorial photograph, [SUJEITO], on a pure black background with a deep crimson gradient glow (#1F0003 to #9C130D) rising from one corner, dramatic red stage lighting from above, soft red haze on a dark reflective floor, subtle red rim light, high contrast chiaroscuro, luxury medical aesthetics brand, premium and restrained, sharp focus, 85mm lens, shallow depth of field, no text, no logo, no watermark
```

Sufixos por plataforma: `--ar 4:5` (feed), `--ar 9:16` (stories/reels), `--ar 16:9` (slides). Estilo fotografico realista sempre; nada de render 3D "de plastico" nem ilustracao.

**Prompt negativo** (quando o modelo aceitar):

```
blue light, purple gradient, teal, neon, cartoon, illustration, 3D render look, plastic skin, overexposed white clinic, stock photo smile, cluttered background, text, logo, watermark, emoji, competitor devices
```

## 5. Variacoes prontas

**Equipamento (cenario 1)**

```
Cinematic product photograph of a white medical laser device with a silver articulated arm and a touchscreen, standing centered on a dark reflective floor, three red spotlight beams from above cutting through thin red fog, pure black background fading into deep crimson (#5F0503) glow behind the device, red rim light on the edges, premium and dramatic, 50mm lens, no text
```

**Retrato de paciente (cenario 2)**

```
Editorial beauty portrait of a woman in her 40s with natural glowing skin, eyes closed, calm expression, black turtleneck, lit by a single deep red key light from the left against a pure black background, crimson glow fading behind her shoulder, high contrast, fine skin texture preserved, luxury dermatology brand campaign, 85mm, no text
```

**Medica / equipe**

```
Confident female doctor in a white coat, arms relaxed, photographed against a black background with a deep crimson gradient halo, subtle red rim light on the hair and shoulders, cinematic, premium medical brand, direct eye contact, 85mm, no text
```

**Esfera de transicao (cenario 3)**

```
Abstract giant translucent red glass sphere glowing from inside, deep crimson to black gradient background, soft volumetric light, tiny floating dust particles, minimal, cinematic, no text
```

**Detalhe de pele (cenario 5)**

```
Macro photograph of healthy glowing skin on a shoulder and collarbone, warm red grazing light from the side against a black background, fine texture visible, no face, cinematic and clean, luxury skincare campaign, no text
```

**Bastidor / evento (registro real do feed)**

```
Documentary photograph of a medical training room: a doctor explaining at a large screen, audience seen from behind, natural daylight mixed with red accent lights, candid, editorial, no text
```

## 6. O que nunca pedir

- Luz azul, roxa, teal ou neon: a marca e preto + vermelho
- Sorriso de banco de imagem, pose de propaganda generica
- Fundo branco "hospital", jaleco azul, estetoscopio
- Ilustracao, cartoon, render plastico, gradiente colorido
- Texto, logo ou marca d'agua gerados pelo modelo — **o wordmark Fotona entra depois, em vetor**
- Qualquer aparelho ou marca concorrente
- Rosto de paciente real ou antes/depois sintetico — antes/depois e sempre foto clinica cedida

## 7. Depois de gerar: como a arte final fica na marca

- Logo Fotona pequeno no canto superior esquerdo (positivo sobre claro, negativo sobre escuro).
- Barra vermelha `#ED1C24` de 24 px (em 1920 × 1080, ~2% da altura) rente a borda inferior nos slides.
- Titulo em Montserrat caixa alta, misturando peso 300 e 700 na mesma frase.
- Frase emocional em serifa italica + complemento em Montserrat bold no social.
- Nomes de protocolo em pilula com borda vermelha fina (GLP1Tight®, MelasmaRecovery®).
- Arcos finos vermelhos (quartos de circulo) como decoracao nos slides claros.
- **Um destaque vermelho por tela.** Se tudo e vermelho, nada e.

## 8. Aprendizados de teste (06/09/2026, Higgsfield · Nano Banana 2)

| Cenario | Ajuste que fez funcionar |
|---------|--------------------------|
| Equipamento no palco (16:9) | "medical laser device" **falhou** no modelo; descrever como **"sleek white and silver aesthetic laser platform on wheels"** passou |
| Retrato de paciente (4:5) | "Brazilian woman in her 40s" — luz vermelha lateral, gola preta, fundo preto, textura de pele preservada |
| Esfera de transicao (16:9) | Pedir **"placed left of center"** e **"empty dark space on the right"** quando o slide tera texto a direita |

Regra pratica: 4:5 para posts e 16:9 para slides saem no enquadramento certo sem recorte.
