#!/usr/bin/env python3
"""Fetch a PubMed abstract via NCBI E-utilities efetch.

Usage:
    python pubmed_abstract.py <PMID> [--out <file>]

Writes formatted text (header + abstract) to stdout or --out.
Exit codes: 0 ok, 1 error, 2 empty/short abstract.
"""
from __future__ import annotations

import re
import sys

from _http import fetch_with_retry, ncbi_throttle, ncbi_api_key_param
from _cache import (
    cache_get,
    cache_put,
    cache_get_error,
    cache_put_error,
    TTL_DEFAULTS,
)


EFETCH = (
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    "?db=pubmed&id={pmid}&rettype=abstract&retmode=text"
)


class CachedEmptyAbstractError(RuntimeError):
    """Abstract previously fetched was < 100 chars; we cache that so we don't retry for 7d."""


def fetch_abstract(pmid: str, *, use_cache: bool = True) -> str:
    if use_cache:
        cached = cache_get("pmid", pmid, ttl_days=TTL_DEFAULTS["pmid"])
        if cached is not None:
            return cached
        err = cache_get_error("pmid", pmid)
        if err and err.get("status") == "empty_abstract":
            raise CachedEmptyAbstractError(
                f"PMID {pmid}: cached empty_abstract (retry after {err.get('ttl_days', 7)}d)"
            )

    ncbi_throttle()
    url = EFETCH.format(pmid=pmid) + ncbi_api_key_param()
    status, body, _ = fetch_with_retry(url, timeout=30, bucket="ncbi")
    if status != 200:
        raise RuntimeError(f"efetch HTTP {status} for PMID {pmid}")
    text = body.decode("utf-8", errors="replace").strip()

    if use_cache:
        if len(text) < 100:
            # Short abstract = likely empty/retracted; don't re-bat the API every run.
            cache_put_error("pmid", pmid, "empty_abstract", ttl_days=7)
        else:
            cache_put("pmid", pmid, text)
    return text


def format_output(pmid: str, raw: str) -> str:
    # efetch text format already has title, authors, journal, abstract, etc.
    # Extract first non-empty line after metadata as title heuristic.
    lines = [line.rstrip() for line in raw.splitlines()]
    title = ""
    for line in lines:
        stripped = line.strip()
        if stripped and not re.match(r"^\d+\.\s", stripped) and not stripped.startswith("PMID:"):
            title = stripped
            break
    url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
    header = f"# PubMed {pmid}: {title}\n\nSource: {url}\n\n---\n\n"
    return header + raw + "\n"


def _main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: pubmed_abstract.py <PMID> [--out <file>] [--no-cache]", file=sys.stderr)
        return 1

    use_cache = "--no-cache" not in argv
    positional = [a for a in argv[1:] if a not in ("--no-cache",)]
    if not positional:
        print("usage: pubmed_abstract.py <PMID> [--out <file>] [--no-cache]", file=sys.stderr)
        return 1

    pmid = positional[0].strip()
    if not pmid.isdigit():
        print(f"invalid PMID: {pmid!r}", file=sys.stderr)
        return 1

    out_path = None
    if "--out" in positional:
        idx = positional.index("--out")
        if idx + 1 < len(positional):
            out_path = positional[idx + 1]

    try:
        raw = fetch_abstract(pmid, use_cache=use_cache)
    except Exception as e:
        print(f"[error] PMID {pmid}: {e}", file=sys.stderr)
        return 1

    if len(raw) < 100:
        print(f"[warn] PMID {pmid}: abstract < 100 chars ({len(raw)})", file=sys.stderr)
        return 2

    formatted = format_output(pmid, raw)
    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(formatted)
    else:
        sys.stdout.write(formatted)
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
