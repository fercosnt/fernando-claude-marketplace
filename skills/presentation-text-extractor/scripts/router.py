"""Heuristica de roteamento por pagina.

Para cada pagina do PDF, decide qual engine usar:
- text_native: extracao direta via PyMuPDF (gratis)
- claude_vision_full: pagina inteira renderizada para PNG (scanned/keynote)
- hybrid: texto direto + vision em imagens embarcadas individuais
- + upgrade Haiku --> Sonnet 4.6 se detecta padrao de formula
"""

import re
from dataclasses import dataclass
from pathlib import Path

import pymupdf

TEXT_THRESHOLD = 100
IMAGE_AREA_THRESHOLD = 0.95
TEXT_HEAVY_AREA_THRESHOLD = 0.5
MIN_IMAGE_DIM = 100
BACKGROUND_IMAGE_THRESHOLD = 0.8

FORMULA_PATTERNS = [
    r"\$[^$]+\$",
    r"\\(?:frac|sum|int|sqrt|alpha|beta|gamma|delta|lambda|mu|sigma|omega)",
    r"\b\d+\s*[Jj]/cm[2²]",
    r"\bEr:YAG\b|\bNd:YAG\b|\bCO[2₂]\b",
    r"\b\d+(?:\.\d+)?\s*(?:nm|mJ|kHz|MHz|GHz|ms|us|ns|fs)\b",
    r"\b(?:fluencia|fluence|irradiance|wavelength|duty\s*cycle)\b",
]
FORMULA_RE = re.compile("|".join(FORMULA_PATTERNS), re.IGNORECASE)


@dataclass
class PageDecision:
    page_num: int
    method: str
    use_sonnet: bool
    text_len: int
    image_area_ratio: float
    images_to_ocr: list

    def estimated_cost_usd(self) -> float:
        if self.method == "text_native":
            per_image = 0.0008 if not self.use_sonnet else 0.005
            return len(self.images_to_ocr) * per_image
        if self.method == "claude_vision_full":
            return 0.005 if not self.use_sonnet else 0.012
        if self.method == "hybrid":
            base = 0.005 if not self.use_sonnet else 0.012
            per_image = 0.0008 if not self.use_sonnet else 0.005
            return base + len(self.images_to_ocr) * per_image
        return 0.0


def detect_formula(text: str) -> bool:
    """Retorna True se o texto contem padroes de formula cientifica/matematica."""
    return bool(FORMULA_RE.search(text))


def analyze_page(page) -> PageDecision:
    """Decide engine + modelo para uma pagina."""
    text = page.get_text().strip()
    text_len = len(text)

    page_area = page.rect.width * page.rect.height
    images_info = page.get_images(full=True)
    image_area_total = 0.0
    images_to_ocr = []

    for img_index, img in enumerate(images_info):
        xref = img[0]
        rects = page.get_image_rects(xref)
        for rect in rects:
            area = rect.width * rect.height
            image_area_total += area
            if rect.width < MIN_IMAGE_DIM or rect.height < MIN_IMAGE_DIM:
                continue
            # Skip imagem "background" (cobre quase a pagina inteira E ja temos texto nativo).
            # Tipico em PDFs exportados de PowerPoint onde cada slide vira 1 imagem raster.
            if text_len >= TEXT_THRESHOLD and page_area > 0 and (area / page_area) >= BACKGROUND_IMAGE_THRESHOLD:
                continue
            images_to_ocr.append({
                "xref": xref,
                "rect": (rect.x0, rect.y0, rect.x1, rect.y1),
                "width": rect.width,
                "height": rect.height,
            })

    image_area_ratio = image_area_total / page_area if page_area > 0 else 0.0

    if text_len >= TEXT_THRESHOLD and image_area_ratio < TEXT_HEAVY_AREA_THRESHOLD:
        method = "text_native"
    elif text_len < TEXT_THRESHOLD and image_area_ratio >= IMAGE_AREA_THRESHOLD:
        method = "claude_vision_full"
        images_to_ocr = []
    else:
        method = "hybrid"

    use_sonnet = detect_formula(text)

    return PageDecision(
        page_num=page.number + 1,
        method=method,
        use_sonnet=use_sonnet,
        text_len=text_len,
        image_area_ratio=image_area_ratio,
        images_to_ocr=images_to_ocr,
    )


def route_pdf(pdf_path: Path) -> list[PageDecision]:
    """Analisa o PDF inteiro e retorna decisoes por pagina."""
    decisions = []
    with pymupdf.open(pdf_path) as doc:
        for page in doc:
            decisions.append(analyze_page(page))
    return decisions


def collapse_ranges(numbers: list[int]) -> list:
    """Colapsa lista de inteiros em ranges contiguos: [3,4,5,7,9,10] -> [(3,5), 7, (9,10)]."""
    if not numbers:
        return []
    sorted_nums = sorted(set(numbers))
    result = []
    start = sorted_nums[0]
    end = start
    for n in sorted_nums[1:]:
        if n == end + 1:
            end = n
        else:
            result.append((start, end) if start != end else start)
            start = n
            end = n
    result.append((start, end) if start != end else start)
    return result


def format_ranges(numbers: list[int]) -> str:
    """Formata lista para legibilidade: [3,4,5,7,9,10] -> '3-5, 7, 9-10'."""
    parts = []
    for item in collapse_ranges(numbers):
        if isinstance(item, tuple):
            parts.append(f"{item[0]}-{item[1]}")
        else:
            parts.append(str(item))
    return ", ".join(parts)
