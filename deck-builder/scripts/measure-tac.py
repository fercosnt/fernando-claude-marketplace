#!/usr/bin/env python3
"""
measure-tac.py — mede cobertura de tinta (TAC) de PDFs e imagens.

TAC = media por pixel da soma dos 4 canais CMYK normalizados, escala 0-400%.

AVISO METODOLOGICO (repetido no output, de proposito):
    A conversao CMYK e a ingenua do Pillow, SEM perfil ICC. O numero e um
    PROXY COMPARATIVO — serve para dizer "esta pagina gasta 8x menos que
    aquela" — e NAO uma estimativa de consumo real de impressora.

Uso:
    measure-tac.py DOSSIE.pdf
    measure-tac.py original.pdf dossie.pdf        # compara dois
    measure-tac.py slides/*.png
    measure-tac.py DOSSIE.pdf --dpi 72 --json

Dependencias: Pillow, numpy.
Para PDF: pdftoppm (poppler-utils) OU pymupdf — o que estiver disponivel.
"""

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    import numpy as np
    from PIL import Image
except ImportError as e:
    sys.exit(
        f"ERRO: dependencia Python ausente ({e.name}).\n"
        "  Instale com: pip install Pillow numpy\n"
        "  Ou rode ./check-print-deps.sh para o diagnostico completo."
    )

Image.MAX_IMAGE_PIXELS = None  # paginas grandes em DPI alto nao sao ataque


def tac_da_imagem(caminho: Path) -> float:
    """TAC de uma imagem, em porcentagem 0-400."""
    with Image.open(caminho) as im:
        cmyk = im.convert("CMYK")
        arr = np.asarray(cmyk, dtype=np.float32)
    # soma dos 4 canais / 255 * 100 -> 0..400% por pixel; media sobre os pixels
    return float(arr.sum(axis=2).mean() / 255.0 * 100.0)


def _rasterizar_pymupdf(pdf: Path, dpi: int, destino: Path) -> list[Path] | None:
    """Fallback sem binario de sistema. None se PyMuPDF nao estiver instalado."""
    try:
        import pymupdf                      # nome moderno
    except ImportError:
        try:
            import fitz as pymupdf          # nome legado (<1.24)
        except ImportError:
            return None
    paginas = []
    with pymupdf.open(pdf) as doc:
        for i, pag in enumerate(doc, 1):
            destino_png = destino / f"pag-{i:03d}.png"
            pag.get_pixmap(dpi=dpi).save(destino_png)
            paginas.append(destino_png)
    return paginas or None


def rasterizar_pdf(pdf: Path, dpi: int, destino: Path) -> list[Path]:
    """Rasteriza um PDF em PNGs. Prefere pdftoppm; cai para PyMuPDF."""
    if not shutil.which("pdftoppm"):
        via_py = _rasterizar_pymupdf(pdf, dpi, destino)
        if via_py:
            return via_py
        sys.exit(
            "ERRO: nao ha como rasterizar PDF — 'pdftoppm' ausente e PyMuPDF nao instalado.\n"
            "  Opcao A (sem binario de sistema):  python3 -m pip install pymupdf\n"
            "  Opcao B (binario):  macOS: brew install poppler | Debian: sudo apt install poppler-utils\n"
            "  (imagens PNG/JPG funcionam sem qualquer das duas)"
        )
    prefixo = destino / "pag"
    r = subprocess.run(
        ["pdftoppm", "-png", "-r", str(dpi), str(pdf), str(prefixo)],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        sys.exit(f"ERRO: pdftoppm falhou em {pdf}:\n{r.stderr.strip()}")
    paginas = sorted(destino.glob("pag*.png"))
    if not paginas:
        sys.exit(f"ERRO: nenhuma pagina extraida de {pdf} — arquivo vazio ou corrompido?")
    return paginas


def medir(caminho: Path, dpi: int) -> dict:
    """Mede um arquivo (PDF ou imagem). Retorna dict com paginas e media."""
    if caminho.suffix.lower() == ".pdf":
        with tempfile.TemporaryDirectory() as tmp:
            paginas = rasterizar_pdf(caminho, dpi, Path(tmp))
            valores = [tac_da_imagem(p) for p in paginas]
    else:
        valores = [tac_da_imagem(caminho)]
    media = sum(valores) / len(valores)
    return {
        "arquivo": str(caminho),
        "paginas": len(valores),
        "tac_por_pagina": [round(v, 1) for v in valores],
        "tac_medio": round(media, 1),
        # produto paginas x cobertura — a metrica que o piloto usou para dizer "30x"
        "produto": round(media * len(valores), 0),
    }


AVISO = (
    "TAC via conversao CMYK ingenua do Pillow, sem perfil ICC. "
    "Proxy comparativo, NAO estimativa de consumo real de impressora."
)


def relatorio_texto(resultados: list[dict], alvo: float) -> str:
    linhas = []
    for r in resultados:
        linhas.append(f"\n=== {r['arquivo']} ===")
        linhas.append(f"{'pag':>5}  {'TAC':>7}")
        for i, v in enumerate(r["tac_por_pagina"], 1):
            linhas.append(f"{i:>5}  {v:>6.1f}%")
        status = "OK" if r["tac_medio"] <= alvo else f"ACIMA DO ALVO ({alvo:.0f}%)"
        linhas.append(f"{'—' * 16}")
        linhas.append(f"{r['paginas']} paginas · TAC medio {r['tac_medio']:.1f}%  [{status}]")
        linhas.append(f"produto (paginas x cobertura): {r['produto']:.0f}")

    if len(resultados) == 2:
        antes, depois = resultados
        if depois["produto"] > 0:
            fator = antes["produto"] / depois["produto"]
            linhas.append(
                f"\n>>> REDUCAO: {antes['produto']:.0f} → {depois['produto']:.0f} "
                f"— aproximadamente {fator:.0f}x menos tinta."
            )
    linhas.append(f"\nNota: {AVISO}")
    return "\n".join(linhas)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Mede cobertura de tinta (TAC) de PDFs e imagens.",
        epilog=AVISO,
    )
    ap.add_argument("arquivos", nargs="+", type=Path,
                    help="PDF(s) ou imagem(ns). Com exatamente 2, compara original vs dossie.")
    ap.add_argument("--dpi", type=int, default=100,
                    help="DPI de rasterizacao do PDF (default: 100)")
    ap.add_argument("--alvo", type=float, default=25.0,
                    help="TAC medio alvo em %%, para o status (default: 25)")
    ap.add_argument("--json", action="store_true", help="Saida em JSON")
    args = ap.parse_args()

    faltando = [a for a in args.arquivos if not a.exists()]
    if faltando:
        sys.exit("ERRO: arquivo(s) nao encontrado(s): " + ", ".join(map(str, faltando)))

    resultados = [medir(a, args.dpi) for a in args.arquivos]

    if args.json:
        print(json.dumps({"resultados": resultados, "alvo": args.alvo, "aviso": AVISO},
                         ensure_ascii=False, indent=2))
    else:
        print(relatorio_texto(resultados, args.alvo))

    # exit 1 se algum arquivo passou do alvo — util em eval/CI
    return 1 if any(r["tac_medio"] > args.alvo for r in resultados) else 0


if __name__ == "__main__":
    sys.exit(main())
