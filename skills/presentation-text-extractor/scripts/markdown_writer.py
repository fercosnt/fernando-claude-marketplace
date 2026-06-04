"""Geracao do .md final com frontmatter + headers por slide + callouts de imagem."""

import hashlib
from datetime import datetime, timezone
from pathlib import Path

from router import format_ranges


def compute_sha256(pdf_path: Path) -> str:
    h = hashlib.sha256()
    with pdf_path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def detect_lang(sample_text: str) -> str:
    """Retorna codigo ISO (pt-BR, en, es) ou 'unknown'."""
    try:
        from langdetect import detect

        code = detect(sample_text)
        if code == "pt":
            return "pt-BR"
        return code
    except Exception:
        return "unknown"


def detect_deck_title(first_slide_text: str) -> str:
    """Heuristica simples: primeira linha nao-vazia do slide 1, sem markdown headers."""
    for line in first_slide_text.splitlines():
        stripped = line.strip().lstrip("#").strip()
        if stripped:
            return stripped
    return "Untitled Deck"


def build_frontmatter(
    pdf_path: Path,
    slide_count: int,
    slides_data: list[dict],
    cost_real_usd: float,
) -> dict:
    """Monta o dict de frontmatter a partir das decisoes e dados extraidos."""
    methods_by_page = {s["page_num"]: s["method_used"] for s in slides_data}

    paginas_multimodal = [p for p, m in methods_by_page.items() if m != "text_native"]
    paginas_apple = [p for p, m in methods_by_page.items() if m == "apple_vision"]
    paginas_haiku = [p for p, m in methods_by_page.items() if m == "claude_haiku"]
    paginas_sonnet = [p for p, m in methods_by_page.items() if m == "claude_sonnet"]

    extraction_methods_count = len(set(methods_by_page.values()))
    if extraction_methods_count == 1:
        extracao_modo = next(iter(methods_by_page.values())).replace("claude_", "").replace("_full", "")
        if extracao_modo == "text_native":
            extracao_modo = "text"
        elif extracao_modo == "vision":
            extracao_modo = "multimodal"
    else:
        extracao_modo = "hybrid"

    first_slide_text = next((s["text"] for s in slides_data if s["page_num"] == 1), "")
    sample = "\n".join(s["text"] for s in slides_data[:5])

    return {
        "source": pdf_path.name,
        "source_sha256": compute_sha256(pdf_path),
        "slide_count": slide_count,
        "lang": detect_lang(sample),
        "extracted_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "extracao_modo": extracao_modo,
        "paginas_multimodal": format_ranges(paginas_multimodal) if paginas_multimodal else "",
        "paginas_apple_vision": format_ranges(paginas_apple) if paginas_apple else "",
        "paginas_claude_haiku": format_ranges(paginas_haiku) if paginas_haiku else "",
        "paginas_claude_sonnet": format_ranges(paginas_sonnet) if paginas_sonnet else "",
        "custo_real_usd": round(cost_real_usd, 4),
        "deck_title": detect_deck_title(first_slide_text),
        "generator": "presentation-text-extractor v1.0",
    }


def render_frontmatter(fm: dict) -> str:
    lines = ["---"]
    for key, value in fm.items():
        if value == "" or value is None:
            continue
        if isinstance(value, str) and (":" in value or value.startswith("[")):
            lines.append(f'{key}: "{value}"')
        else:
            lines.append(f"{key}: {value}")
    lines.append("---")
    return "\n".join(lines)


def render_slide(slide: dict) -> str:
    """Renderiza um slide com header + texto + notas + callouts de imagem."""
    parts = []
    title_line = slide.get("title") or f"Slide {slide['page_num']}"
    parts.append(f"## Slide {slide['page_num']} — {title_line}")
    parts.append("")

    if slide.get("text", "").strip():
        parts.append(slide["text"].strip())
        parts.append("")

    if slide.get("notes"):
        parts.append(f"> **Notas do palestrante:** {slide['notes']}")
        parts.append("")

    for img in slide.get("image_descriptions", []):
        engine_tag = img["engine"]
        parts.append(f"> [!image] Slide {slide['page_num']} ({engine_tag})")
        for line in img["description"].splitlines():
            parts.append(f"> {line}" if line.strip() else ">")
        parts.append("")

    return "\n".join(parts).rstrip() + "\n"


def write_markdown(
    pdf_path: Path,
    slides_data: list[dict],
    cost_real_usd: float,
    output_path: Path | None = None,
) -> Path:
    """Gera .md final ao lado do PDF (mesma pasta, mesmo nome + .md)."""
    if output_path is None:
        output_path = pdf_path.with_suffix(".md")

    frontmatter = build_frontmatter(pdf_path, len(slides_data), slides_data, cost_real_usd)
    deck_title = frontmatter["deck_title"]

    sections = [render_frontmatter(frontmatter), "", f"# {deck_title}", ""]
    for slide in sorted(slides_data, key=lambda s: s["page_num"]):
        sections.append(render_slide(slide))

    output_path.write_text("\n".join(sections), encoding="utf-8")
    return output_path
