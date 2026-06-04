#!/usr/bin/env python3
"""Fetch PMC full-text HTML, strip tags, and emit plain text.

Usage:
    python pmc_fulltext.py <PMCID> [--out <file>]

PMCID may be 'PMC1234567' or '1234567' (prefix added).
Exit codes: 0 ok, 1 error, 2 content too short (likely captcha / redirect).
"""
from __future__ import annotations

import html
import re
import sys

from _http import fetch_with_retry
from _cache import (
    cache_get_json,
    cache_put,
    cache_get_error,
    cache_put_error,
    TTL_DEFAULTS,
)


PMC_URL = "https://pmc.ncbi.nlm.nih.gov/articles/{pmcid}/"
PUBMED_FROM_PMC_URL = "https://pubmed.ncbi.nlm.nih.gov/?term={pmcid}"

MIN_CONTENT_CHARS = 5000


class CachedCaptchaError(RuntimeError):
    """Previous fetch tripped PMC captcha/redirect; cached as error for 7d."""
TAG_RE = re.compile(r"<[^>]+>", re.DOTALL)
SCRIPT_STYLE_RE = re.compile(
    r"<(script|style|noscript|nav|footer|header|aside)[^>]*>.*?</\1>",
    flags=re.IGNORECASE | re.DOTALL,
)
WHITESPACE_RE = re.compile(r"\n{3,}")
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.IGNORECASE | re.DOTALL)


def strip_html(raw_html: str) -> str:
    # Remove script/style/nav/footer blocks entirely.
    cleaned = SCRIPT_STYLE_RE.sub(" ", raw_html)
    # Replace block-level tags with newlines so paragraphs survive.
    cleaned = re.sub(
        r"</(?:p|div|section|article|h[1-6]|li|tr|br)\s*>",
        "\n",
        cleaned,
        flags=re.IGNORECASE,
    )
    cleaned = re.sub(r"<br\s*/?>", "\n", cleaned, flags=re.IGNORECASE)
    # Strip remaining tags.
    cleaned = TAG_RE.sub("", cleaned)
    cleaned = html.unescape(cleaned)
    # Collapse whitespace.
    cleaned = WHITESPACE_RE.sub("\n\n", cleaned)
    return cleaned.strip()


def extract_title(raw_html: str) -> str:
    m = TITLE_RE.search(raw_html)
    if not m:
        return ""
    return html.unescape(m.group(1).strip())


def fetch_fulltext(pmcid: str, *, use_cache: bool = True) -> tuple[str, str]:
    """Returns (title, stripped_text).

    With use_cache=True (default): consults the local cache (TTL 365d for success,
    7d for captcha/redirect errors) before hitting NCBI. Callers that need to
    force-refresh can pass use_cache=False.
    """
    if not pmcid.startswith("PMC"):
        pmcid = f"PMC{pmcid}"

    if use_cache:
        cached = cache_get_json("pmcid", pmcid, ttl_days=TTL_DEFAULTS["pmcid"])
        if cached is not None:
            return cached.get("title", ""), cached.get("text", "")
        err = cache_get_error("pmcid", pmcid)
        if err and err.get("status") == "captcha_or_redirect":
            raise CachedCaptchaError(
                f"{pmcid}: cached captcha/redirect (retry after {err.get('ttl_days', 7)}d)"
            )

    url = PMC_URL.format(pmcid=pmcid)
    # PMC does NOT block stdlib user-agent, but rotating to Chrome is safer.
    headers = {
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.9",
    }
    status, body, _ = fetch_with_retry(
        url, headers=headers, timeout=60, as_browser=True
    )
    if status != 200:
        raise RuntimeError(f"PMC HTTP {status} for {pmcid}")
    raw = body.decode("utf-8", errors="replace")
    title = extract_title(raw)
    text = strip_html(raw)

    if use_cache:
        if len(text) < MIN_CONTENT_CHARS:
            cache_put_error("pmcid", pmcid, "captcha_or_redirect", ttl_days=7)
        else:
            cache_put("pmcid", pmcid, {"title": title, "text": text})
    return title, text


def format_output(pmcid: str, title: str, text: str) -> str:
    if not pmcid.startswith("PMC"):
        pmcid = f"PMC{pmcid}"
    url = PMC_URL.format(pmcid=pmcid)
    header = (
        f"# FULL-TEXT: {pmcid}\n\n"
        f"{title}\n\n"
        f"Source: {url}\n"
        f"PubMed: {PUBMED_FROM_PMC_URL.format(pmcid=pmcid)}\n\n"
        f"---\n\n"
    )
    return header + text + "\n"


def _main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: pmc_fulltext.py <PMCID> [--out <file>] [--no-cache]", file=sys.stderr)
        return 1

    use_cache = "--no-cache" not in argv
    positional = [a for a in argv[1:] if a not in ("--no-cache",)]
    if not positional:
        print("usage: pmc_fulltext.py <PMCID> [--out <file>] [--no-cache]", file=sys.stderr)
        return 1

    pmcid = positional[0].strip()
    out_path = None
    if "--out" in positional:
        idx = positional.index("--out")
        if idx + 1 < len(positional):
            out_path = positional[idx + 1]

    try:
        title, text = fetch_fulltext(pmcid, use_cache=use_cache)
    except Exception as e:
        print(f"[error] {pmcid}: {e}", file=sys.stderr)
        return 1

    if len(text) < MIN_CONTENT_CHARS:
        print(
            f"[warn] {pmcid}: content {len(text)} chars < {MIN_CONTENT_CHARS} — likely captcha/redirect",
            file=sys.stderr,
        )
        return 2

    formatted = format_output(pmcid, title, text)
    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(formatted)
    else:
        sys.stdout.write(formatted)
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
