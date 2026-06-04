#!/usr/bin/env python3
"""OpenAlex Works API client for venue h-index, citations, concepts.

Endpoint: https://api.openalex.org/works/doi:{doi}?mailto={OPENALEX_EMAIL}
Polite pool: 10 req/s when mailto= is set; anonymous works but rate-limited
more aggressively. Skill-level boot check warns if OPENALEX_EMAIL is missing.

Returns:
    {
      "work_id":         "W2057382412",
      "title":           "...",
      "doi":             "10.1089/thy.2014.0028",
      "year":            2015,
      "cited_by_count":  234,
      "venue":           "Thyroid",
      "venue_h_index":   68,
      "venue_quartile":  "Q1",
      "concepts":        [{"display_name": "Hashimoto disease", "score": 0.89}, ...]
    }

Quartile thresholds (calibratable in F11 future):
    Q1: h_index > 50
    Q2: 20 <= h_index <= 50
    Q3: 5  <= h_index < 20
    Q4: h_index < 5

Cache TTL: 90d (citation counts move slowly).
"""
from __future__ import annotations

import json
import os
import sys
from typing import Optional
from urllib.error import HTTPError
from urllib.parse import quote

from _cache import (
    cache_get_json,
    cache_put,
    cache_get_error,
    cache_put_error,
    TTL_DEFAULTS,
)
from _http import fetch_with_retry
from _token_bucket import get_bucket


API_BASE = "https://api.openalex.org/works"
CONCEPT_SCORE_MIN = 0.7
CONCEPT_TOP_N = 3


def _quartile(h_index: Optional[int]) -> Optional[str]:
    if h_index is None:
        return None
    if h_index > 50:
        return "Q1"
    if h_index >= 20:
        return "Q2"
    if h_index >= 5:
        return "Q3"
    return "Q4"


def _safe_doi_key(doi: str) -> str:
    return doi.replace("/", "_").replace(":", "_")


def _parse(data: dict) -> dict:
    """Extract the subset of fields we actually use downstream."""
    primary = data.get("primary_location") or {}
    source = (primary.get("source") or {}) if isinstance(primary, dict) else {}
    venue_name = source.get("display_name")
    # OpenAlex exposes venue h-index under different keys depending on shape;
    # `summary_stats.h_index` is per-work, but venue's h-index lives on the
    # source. Newer schema uses `h_index` directly on source.
    venue_h_index = source.get("h_index")
    if venue_h_index is None:
        # Try summary_stats fallback (some endpoints expose it there).
        ss = source.get("summary_stats") or {}
        venue_h_index = ss.get("h_index") if isinstance(ss, dict) else None

    concepts_raw = data.get("concepts") or []
    concepts = [
        {"display_name": c.get("display_name"), "score": c.get("score")}
        for c in sorted(concepts_raw, key=lambda c: c.get("score") or 0, reverse=True)
        if (c.get("score") or 0) > CONCEPT_SCORE_MIN
    ][:CONCEPT_TOP_N]

    doi_full = data.get("doi") or ""
    # OpenAlex returns DOIs as full URLs (https://doi.org/...); normalise.
    if doi_full.startswith("https://doi.org/"):
        doi_full = doi_full[len("https://doi.org/"):]

    return {
        "work_id": (data.get("id") or "").rsplit("/", 1)[-1] or None,
        "title": data.get("title") or data.get("display_name"),
        "doi": doi_full or None,
        "year": data.get("publication_year"),
        "cited_by_count": data.get("cited_by_count"),
        "venue": venue_name,
        "venue_h_index": venue_h_index,
        "venue_quartile": _quartile(venue_h_index),
        "concepts": concepts,
    }


def fetch(doi: str, *, use_cache: bool = True) -> Optional[dict]:
    """Fetch OpenAlex work metadata for a DOI. Returns None on 404."""
    if not doi:
        raise ValueError("empty doi")
    # OpenAlex accepts the bare DOI; URL-encode to be safe with weird suffixes.
    key = _safe_doi_key(doi)

    if use_cache:
        cached = cache_get_json("openalex", key, ttl_days=TTL_DEFAULTS["openalex"])
        if cached is not None:
            return cached
        err = cache_get_error("openalex", key)
        if err is not None and err.get("status") == "not_found":
            return None

    email = os.environ.get("OPENALEX_EMAIL")
    qs = f"?mailto={quote(email)}" if email else ""
    url = f"{API_BASE}/doi:{quote(doi, safe='/.:-')}{qs}"

    get_bucket("openalex").acquire()
    try:
        status, body, _ = fetch_with_retry(url, timeout=30, bucket="openalex")
    except HTTPError as e:
        if e.code == 404:
            if use_cache:
                cache_put_error("openalex", key, "not_found", extra={"via": "openalex"})
            return None
        raise RuntimeError(f"OpenAlex HTTP {e.code} for {doi}: {e}")

    if status == 404:
        if use_cache:
            cache_put_error("openalex", key, "not_found", extra={"via": "openalex"})
        return None
    if status != 200:
        raise RuntimeError(f"OpenAlex HTTP {status} for {doi}")

    try:
        raw = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        raise RuntimeError(f"OpenAlex returned invalid JSON for {doi}: {e}")

    parsed = _parse(raw)
    if use_cache:
        cache_put("openalex", key, parsed)
    return parsed


def _main(argv: list[str]) -> int:
    use_cache = "--no-cache" not in argv
    args = [a for a in argv[1:] if a != "--no-cache"]
    if not args:
        print("usage: openalex.py <DOI> [--no-cache]", file=sys.stderr)
        return 1

    if not os.environ.get("OPENALEX_EMAIL"):
        print(
            "[warn] OPENALEX_EMAIL not set — using anonymous pool (lower rate limit)",
            file=sys.stderr,
        )

    try:
        result = fetch(args[0].strip(), use_cache=use_cache)
    except Exception as e:
        print(f"[error] {args[0]}: {e}", file=sys.stderr)
        return 1
    if result is None:
        print(f"[info] {args[0]}: not indexed in OpenAlex (404)", file=sys.stderr)
        return 2
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
