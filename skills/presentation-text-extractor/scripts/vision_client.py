"""Cliente unificado para Claude vision (Haiku/Sonnet) e Apple Vision (ocrmac).

Apple Vision e usado como primeira tentativa para imagens com texto simples
(zero custo, ~150ms). Se confianca baixa OU texto contem padrao de formula,
faz upgrade para Claude vision.
"""

import base64
import io
import os
from dataclasses import dataclass
from pathlib import Path

from PIL import Image

CLAUDE_MAX_LONG_EDGE = 1568
CLAUDE_HAIKU_MODEL = "claude-haiku-4-5"
CLAUDE_SONNET_MODEL = "claude-sonnet-4-6"
APPLE_VISION_CONFIDENCE_THRESHOLD = 0.5

OCR_PROMPT = """Transcribe ALL text from this presentation slide image exactly as it appears.

Return as markdown:
- Use # for slide title, ## for subtitle
- Use bullet lists for bullets
- Use markdown table syntax for tables
- For mathematical/chemical formulas, use LaTeX inline ($...$) or block ($$...$$)
- For charts/diagrams/photos with no extractable text, output a one-sentence description prefixed with [DESCRIPTION:]

Do not interpret or summarize. Transcribe verbatim. Preserve layout order (top-to-bottom, left-to-right)."""


@dataclass
class OCRResult:
    text: str
    engine: str
    model: str | None
    confidence: float
    is_description: bool = False


def resize_for_claude(image_path: Path) -> bytes:
    """Redimensiona imagem para max 1568px no lado longo (PNG, lossless)."""
    with Image.open(image_path) as img:
        img.load()
        max_edge = max(img.width, img.height)
        if max_edge > CLAUDE_MAX_LONG_EDGE:
            scale = CLAUDE_MAX_LONG_EDGE / max_edge
            new_size = (int(img.width * scale), int(img.height * scale))
            img = img.resize(new_size, Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="PNG", optimize=True)
        return buf.getvalue()


def apple_vision_ocr(image_path: Path) -> OCRResult:
    """OCR via Apple Vision (ocrmac). Retorna confianca baixa se falhar."""
    try:
        from ocrmac import ocrmac
    except ImportError:
        return OCRResult(text="", engine="apple_vision", model=None, confidence=0.0)

    try:
        annotations = ocrmac.OCR(str(image_path), language_preference=["pt-BR", "en-US"]).recognize()
    except Exception:
        return OCRResult(text="", engine="apple_vision", model=None, confidence=0.0)

    if not annotations:
        return OCRResult(text="", engine="apple_vision", model=None, confidence=0.0)

    texts = []
    confidences = []
    for ann in annotations:
        text, conf, _ = ann
        texts.append(text)
        confidences.append(conf)

    avg_conf = sum(confidences) / len(confidences) if confidences else 0.0
    return OCRResult(
        text="\n".join(texts),
        engine="apple_vision",
        model=None,
        confidence=avg_conf,
    )


def claude_vision_ocr(image_path: Path, use_sonnet: bool = False) -> OCRResult:
    """OCR via Claude vision (Haiku ou Sonnet)."""
    try:
        from anthropic import Anthropic
    except ImportError as exc:
        raise RuntimeError("anthropic SDK nao instalado. Rode: pip install anthropic") from exc

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY nao definida no ambiente")

    client = Anthropic(api_key=api_key)
    model = CLAUDE_SONNET_MODEL if use_sonnet else CLAUDE_HAIKU_MODEL

    image_bytes = resize_for_claude(image_path)
    image_b64 = base64.standard_b64encode(image_bytes).decode("utf-8")

    response = client.messages.create(
        model=model,
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {"type": "base64", "media_type": "image/png", "data": image_b64},
                },
                {"type": "text", "text": OCR_PROMPT},
            ],
        }],
    )

    text = response.content[0].text if response.content else ""
    is_description = text.strip().startswith("[DESCRIPTION:")
    if is_description:
        text = text.strip().removeprefix("[DESCRIPTION:").rstrip("]").strip()

    return OCRResult(
        text=text,
        engine="claude_vision",
        model=model,
        confidence=1.0,
        is_description=is_description,
    )


def ocr_image(image_path: Path, prefer_engine: str = "auto", use_sonnet: bool = False) -> OCRResult:
    """Roteia OCR de uma imagem: tenta Apple Vision primeiro, fallback Claude.

    prefer_engine: "auto" | "claude" | "apple"
    """
    if prefer_engine == "claude":
        return claude_vision_ocr(image_path, use_sonnet=use_sonnet)

    if prefer_engine == "apple":
        return apple_vision_ocr(image_path)

    apple_result = apple_vision_ocr(image_path)
    if apple_result.confidence >= APPLE_VISION_CONFIDENCE_THRESHOLD and not use_sonnet:
        return apple_result

    return claude_vision_ocr(image_path, use_sonnet=use_sonnet)
