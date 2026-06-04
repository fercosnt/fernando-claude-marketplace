"""Entrypoint principal: workflow 4 passos automatico.

Uso:
  python extract.py deck.pdf
  python extract.py --batch ~/Downloads/decks/
  python extract.py --batch ~/Inbox/ --quiet --max-cost 0.20
"""

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict
from pathlib import Path

import pymupdf

from markdown_writer import write_markdown
from router import format_ranges, route_pdf
from vision_client import claude_vision_ocr, ocr_image

EXIT_OK = 0
EXIT_COST_EXCEEDED = 2
EXIT_BAD_INPUT = 3
EXIT_RUNTIME_ERROR = 4


def log(msg: str, quiet: bool = False, level: str = "info"):
    """Logs em stderr para cron-friendliness."""
    if quiet and level == "info":
        return
    prefix = {"info": "", "warn": "[warn] ", "error": "[error] "}[level]
    print(f"{prefix}{msg}", file=sys.stderr)


def render_image(page, rect_tuple, out_path: Path, dpi: int = 200):
    """Renderiza um retangulo de imagem da pagina como PNG."""
    rect = pymupdf.Rect(*rect_tuple)
    matrix = pymupdf.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=matrix, clip=rect)
    pix.save(str(out_path))


def render_full_page(page, out_path: Path, dpi: int = 200):
    matrix = pymupdf.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=matrix)
    pix.save(str(out_path))


def extract_slide_text(page) -> str:
    """Extracao direta de texto da pagina (sem OCR)."""
    return page.get_text().strip()


def extract_slide_title(text: str) -> str | None:
    """Heuristica simples: primeira linha curta (<80 chars) e nao bullet, sem markdown header."""
    for line in text.splitlines():
        stripped = line.strip().lstrip("#").strip()
        if not stripped:
            continue
        if stripped.startswith(("-", "*", "•", "·")):
            continue
        if len(stripped) <= 80:
            return stripped
        break
    return None


def process_page(page, decision, prefer_engine: str, tmpdir: Path) -> dict:
    """Processa uma pagina aplicando a decisao do router."""
    slide = {
        "page_num": decision.page_num,
        "text": "",
        "title": None,
        "notes": None,
        "image_descriptions": [],
        "method_used": decision.method,
        "cost_usd": 0.0,
    }

    if decision.method == "text_native":
        slide["text"] = extract_slide_text(page)
        slide["title"] = extract_slide_title(slide["text"])

        for img_idx, img_info in enumerate(decision.images_to_ocr):
            img_path = tmpdir / f"page{decision.page_num}_img{img_idx}.png"
            render_image(page, img_info["rect"], img_path)
            ocr = ocr_image(img_path, prefer_engine=prefer_engine, use_sonnet=decision.use_sonnet)
            slide["image_descriptions"].append({
                "engine": engine_tag(ocr.engine, ocr.model),
                "description": ocr.text or "[no text detected]",
            })
            slide["cost_usd"] += estimated_image_cost(ocr.engine, ocr.model)
            slide["method_used"] = upgrade_method(slide["method_used"], ocr.engine, ocr.model)

    elif decision.method == "claude_vision_full":
        img_path = tmpdir / f"page{decision.page_num}_full.png"
        render_full_page(page, img_path)
        ocr = claude_vision_ocr(img_path, use_sonnet=decision.use_sonnet)
        slide["text"] = ocr.text if not ocr.is_description else ""
        if ocr.is_description:
            slide["image_descriptions"].append({
                "engine": engine_tag(ocr.engine, ocr.model),
                "description": ocr.text,
            })
        slide["title"] = extract_slide_title(slide["text"]) if slide["text"] else None
        slide["cost_usd"] = 0.012 if decision.use_sonnet else 0.005
        slide["method_used"] = "claude_sonnet" if decision.use_sonnet else "claude_haiku"

    else:
        slide["text"] = extract_slide_text(page)
        slide["title"] = extract_slide_title(slide["text"])
        for img_idx, img_info in enumerate(decision.images_to_ocr):
            img_path = tmpdir / f"page{decision.page_num}_img{img_idx}.png"
            render_image(page, img_info["rect"], img_path)
            ocr = ocr_image(img_path, prefer_engine=prefer_engine, use_sonnet=decision.use_sonnet)
            slide["image_descriptions"].append({
                "engine": engine_tag(ocr.engine, ocr.model),
                "description": ocr.text or "[no text detected]",
            })
            slide["cost_usd"] += estimated_image_cost(ocr.engine, ocr.model)
        slide["method_used"] = "hybrid"

    return slide


def engine_tag(engine: str, model: str | None) -> str:
    if engine == "apple_vision":
        return "apple_vision"
    if model and "haiku" in model:
        return "claude_haiku"
    if model and "sonnet" in model:
        return "claude_sonnet"
    return engine


def estimated_image_cost(engine: str, model: str | None) -> float:
    if engine == "apple_vision":
        return 0.0
    if model and "sonnet" in model:
        return 0.005
    return 0.0008


def upgrade_method(current: str, engine: str, model: str | None) -> str:
    """Se ja era text_native e agora usou claude_*, upgrade para hybrid."""
    if engine == "claude_vision" and current == "text_native":
        return "hybrid"
    return current


def print_inventory(pdf_path: Path, decisions: list, quiet: bool):
    log(f"[1/4] Inventariando {pdf_path.name}...", quiet)
    log(f"  Paginas: {len(decisions)}", quiet)
    counts = {}
    for d in decisions:
        counts[d.method] = counts.get(d.method, 0) + 1
    summary = ", ".join(f"{v} {k}" for k, v in counts.items())
    log(f"  Tipos: {summary}", quiet)


def print_plan(decisions: list, quiet: bool, max_cost: float) -> float:
    log("", quiet)
    log("[2/4] Plano de extracao:", quiet)
    by_method = {}
    for d in decisions:
        key = d.method
        if d.use_sonnet and "claude" in d.method or d.method == "claude_vision_full":
            key = f"{d.method}_sonnet" if d.use_sonnet else d.method
        by_method.setdefault(key, {"pages": [], "cost": 0.0})
        by_method[key]["pages"].append(d.page_num)
        by_method[key]["cost"] += d.estimated_cost_usd()

    total = sum(group["cost"] for group in by_method.values())

    log("  Engine               | Slides            | Custo estimado", quiet)
    log("  ---------------------+-------------------+----------------", quiet)
    for method, group in sorted(by_method.items()):
        slides_str = format_ranges(group["pages"])[:35]
        log(f"  {method:<20} | {slides_str:<17} | ${group['cost']:.4f}", quiet)
    log("  ---------------------+-------------------+----------------", quiet)
    log(f"  TOTAL                                      ~${total:.4f}", quiet)
    log(f"  Limite (--max-cost): ${max_cost:.4f}  {'OK' if total <= max_cost else 'EXCEDIDO'}", quiet)

    return total


def extract_single(
    pdf_path: Path,
    max_cost: float,
    prefer_engine: str,
    model_override: str | None,
    force_ocr: bool,
    dry_run: bool,
    interactive: bool,
    quiet: bool,
) -> int:
    if not pdf_path.exists():
        log(f"Arquivo nao encontrado: {pdf_path}", level="error")
        return EXIT_BAD_INPUT
    if pdf_path.suffix.lower() != ".pdf":
        log(f"Apenas PDF suportado no v1: {pdf_path.suffix}", level="error")
        return EXIT_BAD_INPUT

    decisions = route_pdf(pdf_path)

    if force_ocr:
        for d in decisions:
            d.method = "claude_vision_full"

    if model_override == "sonnet":
        for d in decisions:
            d.use_sonnet = True
    elif model_override == "haiku":
        for d in decisions:
            d.use_sonnet = False

    print_inventory(pdf_path, decisions, quiet)
    total_estimated = print_plan(decisions, quiet, max_cost)

    if total_estimated > max_cost:
        log(
            f"Custo estimado ${total_estimated:.4f} > limite ${max_cost:.4f}. "
            f"Use --max-cost {total_estimated * 1.5:.2f} para liberar.",
            level="error",
        )
        return EXIT_COST_EXCEEDED

    if dry_run:
        log("(dry-run: nao executando extracao)", quiet)
        return EXIT_OK

    if interactive:
        try:
            answer = input("Continuar? [Y/n] ").strip().lower()
        except EOFError:
            answer = ""
        if answer == "n":
            log("Abortado pelo usuario.", level="warn")
            return EXIT_OK

    log("", quiet)
    log("[3/4] Extraindo...", quiet)

    slides_data = []
    cost_real = 0.0

    with tempfile.TemporaryDirectory() as tmp_str:
        tmpdir = Path(tmp_str)
        with pymupdf.open(pdf_path) as doc:
            for page, decision in zip(doc, decisions, strict=True):
                slide = process_page(page, decision, prefer_engine, tmpdir)
                slides_data.append(slide)
                cost_real += slide["cost_usd"]
                if not quiet:
                    log(f"  Slide {decision.page_num}/{len(decisions)}: {slide['method_used']} (${slide['cost_usd']:.4f})", quiet)

    log("", quiet)
    log("[4/4] Gravando markdown...", quiet)
    output = write_markdown(pdf_path, slides_data, cost_real)

    log(f"  Custo real: ${cost_real:.4f} (estimado: ${total_estimated:.4f})", quiet)
    log(f"  Output: {output}", quiet=False)

    print(str(output))
    return EXIT_OK


def extract_batch(
    dir_path: Path,
    max_cost: float,
    workers: int,
    prefer_engine: str,
    model_override: str | None,
    force_ocr: bool,
    dry_run: bool,
    quiet: bool,
    skip_existing: bool = False,
) -> int:
    if not dir_path.is_dir():
        log(f"Diretorio nao encontrado: {dir_path}", level="error")
        return EXIT_BAD_INPUT

    pdfs = sorted(dir_path.glob("*.pdf"))
    if not pdfs:
        log(f"Nenhum PDF em {dir_path}", level="error")
        return EXIT_BAD_INPUT

    if skip_existing:
        skipped = [p for p in pdfs if p.with_suffix(".md").exists()]
        pdfs = [p for p in pdfs if not p.with_suffix(".md").exists()]
        log(f"[BATCH] Pulando {len(skipped)} PDFs ja processados (--skip-existing)", quiet)
        if not pdfs:
            log("[BATCH] Nada a processar (todos PDFs ja tem .md)", quiet)
            return EXIT_OK

    log(f"[BATCH] {len(pdfs)} PDFs em {dir_path}", quiet)
    log(f"[BATCH] Spawning {workers} workers paralelos", quiet)

    script_path = Path(__file__).resolve()
    extra_args = []
    if quiet:
        extra_args.append("--quiet")
    if force_ocr:
        extra_args.append("--force-ocr")
    if dry_run:
        extra_args.append("--dry-run")
    extra_args.extend(["--max-cost", str(max_cost)])
    extra_args.extend(["--engine", prefer_engine])
    if model_override:
        extra_args.extend(["--model", model_override])

    failures = []
    successes = []

    def run_one(pdf: Path) -> tuple[Path, int, str]:
        result = subprocess.run(
            [sys.executable, str(script_path), str(pdf), *extra_args],
            capture_output=True,
            text=True,
        )
        return pdf, result.returncode, result.stderr

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(run_one, pdf): pdf for pdf in pdfs}
        for i, future in enumerate(as_completed(futures), 1):
            pdf, rc, stderr_output = future.result()
            if rc == EXIT_OK:
                successes.append(pdf)
                log(f"  [{i}/{len(pdfs)}] {pdf.name}: DONE", quiet)
            else:
                failures.append((pdf, rc, stderr_output.strip().splitlines()[-1] if stderr_output else "?"))
                log(f"  [{i}/{len(pdfs)}] {pdf.name}: FAILED (exit {rc})", level="warn")

    log("", quiet)
    log(f"[BATCH] {len(successes)}/{len(pdfs)} concluidos.", quiet)
    if failures:
        log(f"[BATCH] Falhas:", level="warn")
        for pdf, rc, reason in failures:
            log(f"  - {pdf.name}: exit {rc} ({reason})", level="warn")
        return EXIT_RUNTIME_ERROR

    return EXIT_OK


def main():
    parser = argparse.ArgumentParser(prog="presentation-text-extractor")
    parser.add_argument("input", nargs="?", help="PDF file path (ou use --batch)")
    parser.add_argument("--batch", metavar="DIR", help="Processa todos PDFs da pasta")
    parser.add_argument("--workers", type=int, default=4, help="Subprocessos paralelos em --batch (default 4)")
    parser.add_argument("--max-cost", type=float, default=0.10, help="Hard cap em USD (default $0.10)")
    parser.add_argument("--engine", choices=["auto", "claude", "apple"], default="auto")
    parser.add_argument("--model", choices=["haiku", "sonnet"], default=None, help="Forca modelo Claude")
    parser.add_argument("--force-ocr", action="store_true", help="Vision em tudo (ignora texto extraivel)")
    parser.add_argument("--dry-run", action="store_true", help="So passos 1+2, sem extracao")
    parser.add_argument("--interactive", action="store_true", help="Pergunta confirmacao apos passo 2")
    parser.add_argument("--quiet", action="store_true", help="So output final em stdout")
    parser.add_argument("--skip-existing", action="store_true", help="Em --batch, pula PDFs que ja tem .md ao lado")

    args = parser.parse_args()

    if args.batch:
        return extract_batch(
            dir_path=Path(args.batch).expanduser().resolve(),
            max_cost=args.max_cost,
            workers=args.workers,
            prefer_engine=args.engine,
            model_override=args.model,
            force_ocr=args.force_ocr,
            dry_run=args.dry_run,
            quiet=args.quiet,
            skip_existing=args.skip_existing,
        )

    if not args.input:
        parser.error("Forneca um PDF ou use --batch DIR")

    return extract_single(
        pdf_path=Path(args.input).expanduser().resolve(),
        max_cost=args.max_cost,
        prefer_engine=args.engine,
        model_override=args.model,
        force_ocr=args.force_ocr,
        dry_run=args.dry_run,
        interactive=args.interactive,
        quiet=args.quiet,
    )


if __name__ == "__main__":
    sys.exit(main())
