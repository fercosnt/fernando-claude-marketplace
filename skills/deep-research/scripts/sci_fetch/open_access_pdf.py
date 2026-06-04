#!/usr/bin/env python3
"""Download a PDF from an open-access URL with proper browser headers.

Usage:
    python open_access_pdf.py <url> --out <file>

Validates %PDF signature. If not a PDF, saves as .html fallback and exits 2.
Exit codes: 0 PDF ok, 1 error, 2 not-a-PDF fallback saved.
"""
from __future__ import annotations

import hashlib
import os
import sys
from urllib.parse import urlparse

from _http import fetch_with_retry
from _cache import cache_get, cache_put, TTL_DEFAULTS


MAX_SIZE_BYTES = 50 * 1024 * 1024  # 50 MB


class NotAPDFError(RuntimeError):
    """Raised by fetch() when the body is not a PDF; callers decide fallback."""

    def __init__(self, url: str, fallback_path: str) -> None:
        super().__init__(f"{url}: not a PDF (saved HTML fallback to {fallback_path})")
        self.url = url
        self.fallback_path = fallback_path


def _cache_key(url: str) -> str:
    """Short stable key derived from the URL; avoids 200-char filenames."""
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]


def fetch(url: str, out_path: str, *, use_cache: bool = True) -> str:
    """Download PDF to out_path.

    Returns the actual path written. Raises RuntimeError on HTTP errors /
    oversized bodies, NotAPDFError when the body is HTML (fallback saved).

    When use_cache=True (default) the raw PDF bytes are cached under
    ~/.cache/deep-research-sci/pdf/<sha256_16>.pdf with TTL 365d — cheap
    re-use across pesquisas/delta research. Cache hit just copies bytes to
    out_path without any network call.
    """
    if use_cache:
        key = _cache_key(url)
        cached = cache_get("pdf", key, ttl_days=TTL_DEFAULTS["pdf"], binary=True)
        if cached is not None:
            with open(out_path, "wb") as f:
                f.write(cached)
            return out_path

    host = urlparse(url).hostname or ""
    headers = {
        "Accept": "application/pdf,*/*;q=0.8",
        "Referer": f"https://{host}/",
        "Accept-Language": "en-US,en;q=0.9",
    }
    status, body, _ = fetch_with_retry(
        url, headers=headers, timeout=60, as_browser=True
    )
    if status != 200:
        raise RuntimeError(f"{url}: HTTP {status}")
    if len(body) > MAX_SIZE_BYTES:
        raise RuntimeError(f"{url}: size {len(body)} exceeds max {MAX_SIZE_BYTES}")

    if body.startswith(b"%PDF"):
        with open(out_path, "wb") as f:
            f.write(body)
        if use_cache:
            cache_put("pdf", _cache_key(url), body, binary=True)
        return out_path

    fallback_path = os.path.splitext(out_path)[0] + ".html"
    with open(fallback_path, "wb") as f:
        f.write(body)
    raise NotAPDFError(url, fallback_path)


def _main(argv: list[str]) -> int:
    use_cache = "--no-cache" not in argv
    args = [a for a in argv[1:] if a != "--no-cache"]
    if len(args) < 3 or args[1] != "--out":
        print("usage: open_access_pdf.py <url> --out <file> [--no-cache]", file=sys.stderr)
        return 1

    url = args[0]
    out_path = args[2]
    try:
        fetch(url, out_path, use_cache=use_cache)
        return 0
    except NotAPDFError as e:
        print(f"[warn] {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"[error] {url}: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
