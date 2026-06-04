# Stack tecnico + Setup

## Dependencias Python

Instalar via pip:

```bash
pip install -r scripts/requirements.txt
```

| Pacote | Para que | Por que esse |
|---|---|---|
| `pymupdf` | Parser base + extracao de imagens | ~10x mais rapido que pdfplumber, wheels ARM nativos, zero deps |
| `pillow` | Redimensionar imagens para 1568px | Required pela API Claude vision (cap de tamanho) |
| `anthropic` | SDK Claude vision | Oficial Anthropic, suporta Haiku 4.5 e Sonnet 4.6 |
| `langdetect` | Auto-detect idioma do deck | Pacote leve, suporta pt/en/es |
| `ocrmac` | Wrapper Apple Vision | macOS only, gratis, ~150ms/img |

Sem dependencias de sistema (brew). PyMuPDF tem wheels ARM completos sem precisar de `poppler` ou `cairo`.

## Variaveis de ambiente

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

A skill faz `os.environ.get("ANTHROPIC_API_KEY")` em [vision_client.py](../scripts/vision_client.py). Sem essa env var, todas as chamadas Claude falham com `RuntimeError`.

Se voce so quer usar Apple Vision (sem custo, sem Claude), passe `--engine apple` — a skill nao vai ler a env var.

## Apple Vision via ocrmac

`ocrmac` e um wrapper Python fino sobre o framework Apple Vision via PyObjC. Caracteristicas:

- **Velocidade**: 130-207ms por imagem no M1/M2/M3
- **Qualidade PT-BR**: boa para texto corrido
- **Qualidade tecnica**: ruim para formulas LaTeX e notacao cientifica (Er:YAG, Nd:YAG, fluencias em J/cm²) — Apple Vision e OCR classico, nao entende contexto semantico

A skill usa Apple Vision como **primeira tentativa** para imagens com texto simples. Se confianca media < 0.5 ou texto contem padrao de formula, faz fallback para Claude.

### Troubleshooting ocrmac

Erro `ImportError: ocrmac` no Linux/Windows: esperado. `ocrmac` so funciona em macOS. A skill detecta e roda 100% via Claude vision.

Erro `Vision framework not available`: macOS muito antigo (<10.15). Update sistema.

## Decisao v1: PyMuPDF sem docling

O BRIEF.md original sugeria `docling` (IBM, MIT) como engine base. Decisao tomada na implementacao v1: usar `pymupdf` direto.

**Razoes**:
- `docling` adiciona ~500MB de modelos baixados na primeira execucao
- `docling` e otimizado para papers cientificos densos (multi-coluna, tabelas complexas)
- Slides PDF tem layout muito mais simples — PyMuPDF cobre 95% dos casos com 10x menos overhead
- Menos dependencias = menos modos de falha

**Quando reintroduzir `docling` (v1.1)**:
- Se houver demanda para PDFs hibridos (slide + paginas de paper anexadas)
- Como flag opcional `--engine docling` para casos com tabelas complexas

## Modelo Claude — qual usar

Default: `claude-haiku-4-5` (referenciado em [vision_client.py](../scripts/vision_client.py)).

Upgrade automatico para `claude-sonnet-4-6` quando o texto da pagina contem padroes de formula. Detalhes em [heuristica.md](heuristica.md).

Override manual:
- `--model haiku`: forca Haiku 4.5 em tudo
- `--model sonnet`: forca Sonnet 4.6 em tudo

Custo aproximado por slide (1568px PNG, prompt OCR + ~500 tokens output):
- Haiku 4.5: ~$0.0013
- Sonnet 4.6: ~$0.005

## Prompt de OCR

Definido como constante `OCR_PROMPT` em [vision_client.py](../scripts/vision_client.py):

```
Transcribe ALL text from this presentation slide image exactly as it appears.

Return as markdown:
- Use # for slide title, ## for subtitle
- Use bullet lists for bullets
- Use markdown table syntax for tables
- For mathematical/chemical formulas, use LaTeX inline ($...$) or block ($$...$$)
- For charts/diagrams/photos with no extractable text, output a one-sentence
  description prefixed with [DESCRIPTION:]

Do not interpret or summarize. Transcribe verbatim. Preserve layout order
(top-to-bottom, left-to-right).
```

Pontos chave:
- "Transcribe verbatim" evita o modelo sumarizar ou parafrasear
- Convencao `[DESCRIPTION:]` para imagens sem texto e detectada no parse e vira callout `> [!image]`
- LaTeX explicito preserva formulas para downstream (laser-physics consome bem)
- Layout order top-to-bottom evita confusao em slides multi-coluna

## Performance esperada

Por deck de 30 slides em M3 Pro:

| Cenario | Tempo |
|---|---|
| 100% text-native (so PyMuPDF) | ~2s |
| Hibrido com 5 imagens Apple Vision | ~5s |
| Hibrido com 5 imagens Claude Haiku | ~15-25s (depende latencia API) |
| Vision-only Sonnet (`--force-ocr`) | ~60-90s |

Modo `--batch` com 4 workers paraleliza por arquivo — N decks em paralelo, nao N slides.
