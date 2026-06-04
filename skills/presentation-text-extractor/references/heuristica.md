# Heuristica de roteamento — detalhes

A heuristica decide, para cada pagina do PDF, qual engine usar para extrair conteudo. Implementada em [scripts/router.py](../scripts/router.py).

## Por que ter heuristica

O custo de processar um PDF de 30 slides varia em 100x dependendo da escolha de engine:

| Estrategia | Custo |
|---|---|
| Texto direto (PyMuPDF) em tudo | $0.00 |
| Apple Vision em tudo (fallback) | $0.00 |
| Claude Haiku 4.5 em todas as paginas | ~$0.15 |
| Claude Sonnet 4.6 em todas as paginas | ~$0.36 |
| **Hibrido inteligente (skill default)** | **~$0.009-0.028** |

A heuristica garante que so se paga Claude vision quando ha ganho real (slide com imagem informativa ou pagina escaneada).

## Os 3 estados de uma pagina

Para cada pagina o router classifica em um dos 3 tipos:

### 1. `text_native`

**Quando**: `len(texto_extraido) >= 100` E `area_imagem / area_pagina < 0.5`.

Pagina text-based normal de slide. PyMuPDF extrai o texto direto (gratis, ~1ms).

Se a pagina tem imagens >= 100x100px (graficos, fotos, diagramas), elas sao OCR'adas via Apple Vision (primeira tentativa, gratis) ou Claude vision (fallback se confianca baixa).

### 2. `claude_vision_full`

**Quando**: `len(texto_extraido) < 100` E `area_imagem / area_pagina >= 0.95`.

Pagina escaneada (foto/scan) ou keynote-style (slide so com titulo + imagem ocupando 95% da area). PyMuPDF nao tem texto util.

Acao: renderizar a pagina inteira como PNG 1568px e mandar pra Claude.

### 3. `hybrid`

**Quando**: nem `text_native` nem `claude_vision_full` se aplicam.

Pagina mista (slide com texto + imagem grande). Faz as duas coisas: texto direto via PyMuPDF + vision nas imagens grandes individualmente.

## Upgrade Haiku --> Sonnet

Independente do tipo de pagina, se o **texto extraido contem padroes de formula cientifica**, fazemos upgrade do modelo Claude:

- `claude-haiku-4-5` (default) --> `claude-sonnet-4-6`

Padroes detectados (regex em [router.py](../scripts/router.py)):
- LaTeX inline: `$...$`
- Comandos LaTeX: `\frac`, `\sum`, `\sqrt`, `\alpha`, etc
- Unidades fisicas: `J/cm²`, `mJ`, `nm`, `Hz`, `ms`
- Laser/fisica medica: `Er:YAG`, `Nd:YAG`, `CO2`, `fluencia`, `irradiance`, `wavelength`, `duty cycle`

Justificativa: Sonnet 4.6 preserva LaTeX e notacao tecnica significativamente melhor que Haiku 4.5 (testado pelo sub-agente de best-practices). Custo extra ~3x ($0.005 vs $0.0013 por slide) so onde compensa.

## Thresholds — por que esses numeros

### `TEXT_THRESHOLD = 100`

Cobre slides "keynote-style" com so titulo (40-80 chars tipico). Original era 50 mas perdia slides keynote. Calibrado pelo plano antigo `/fotona-doc-to-md`.

### `IMAGE_AREA_THRESHOLD = 0.95`

Pagina onde imagens ocupam >= 95% da area e provavelmente escaneada ou full-bleed image. 90% pegaria slides com banner grande mas com texto util embaixo.

### `TEXT_HEAVY_AREA_THRESHOLD = 0.5`

Se imagens ocupam menos de 50% e ha texto >=100 chars, tratamos como text-native (extracao direta + vision so nas imagens grandes).

### `MIN_IMAGE_DIM = 100`

Imagens com menos de 100x100px sao ignoradas (provavelmente icone, logo, decoracao). Reduz falsos positivos e custo.

### `BACKGROUND_IMAGE_THRESHOLD = 0.8`

Adicionado em v1.0.1. Pula imagens que cobrem >= 80% da pagina **quando ja temos texto nativo extraivel** (>= 100 chars).

Caso real: PDFs exportados de PowerPoint geralmente embedam cada slide como UMA imagem raster grande cobrindo a pagina inteira. Sem esse filtro, Apple Vision (ou Claude) OCR'a essa imagem e retorna texto duplicado (mesmo que ja foi extraido nativamente). Resultado: callouts `> [!image]` poluem o markdown com transcricao redundante.

Com o filtro: se texto nativo >= 100 chars E imagem cobre >= 80% da pagina, considera background/page-as-image e pula o OCR dessa imagem (mas mantem as menores que sao conteudo real — graficos, logos, fotos).

Trade-off: pode perder uma imagem grande que e legitimamente conteudo unico (raro em slides comerciais). Override via `--force-ocr` se precisar.

### Legado (v1.0.0)

Antes do filtro BACKGROUND_IMAGE_THRESHOLD, OCR de page-as-image duplicava texto. Removido em v1.0.1 apos teste com Apresentacao Comercial Spectro Fotona — reduziu ~7 callouts redundantes para 0 mantendo descricoes uteis (graficos, logos, fotos).

### `APPLE_VISION_CONFIDENCE_THRESHOLD = 0.5`

Definido em [vision_client.py](../scripts/vision_client.py). Se confianca media do Apple Vision em uma imagem fica abaixo de 0.5, faz fallback para Claude.

## Quando a heuristica vai falhar

- **PDFs com encoding quebrado**: texto extraivel mas e gibberish. Use `--force-ocr`.
- **Slides com texto sobre imagem com baixo contraste**: PyMuPDF extrai parcial. Edge case que ainda precisamos validar no spike.
- **Apple Vision em ingles tecnico denso**: pode dar confianca baixa demais e cair pra Claude desnecessariamente. Mitigacao: `--engine claude` forca direto.

## Modo dry-run para auditoria

Para entender o que a heuristica decidiria sem rodar a extracao:

```
python scripts/extract.py deck.pdf --dry-run
```

Mostra a tabela do passo 2 (Plano) e sai sem chamar APIs.
