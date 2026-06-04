# Nano Banana Pro - JSON Templates e Instrucoes de API

Templates JSON para a API Gemini, sistema de referencia por imagem e instrucoes tecnicas.

---

## Indice

1. [Regras Fundamentais da API](#regras-fundamentais-da-api)
2. [Sistema de Referencia de Imagens por Nome](#sistema-de-referencia-de-imagens-por-nome)
3. [JSON Templates (A, B, C)](#json-templates)
4. [Como Converter Imagem para Base64](#como-converter-imagem-para-base64)

---

## Regras Fundamentais da API

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
