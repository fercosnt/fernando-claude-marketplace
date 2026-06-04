#!/usr/bin/env python3
"""Semantic Scholar Graph API client for academic signals (stdlib only).

Endpoint: https://api.semanticscholar.org/graph/v1/paper/{prefixed_id}
Public (no key): 1 req/s. With SEMANTIC_SCHOLAR_API_KEY env: 10 req/s.

Usage:
    python semantic_scholar.py "DOI:10.1089/thy.2014.0028"
    python semantic_scholar.py "PMID:33567185"
    python semantic_scholar.py "10.1089/thy.2014.0028"   # auto-prefix DOI

Returns JSON with citationCount, influentialCitationCount, year, venue, tldr, authors.

Behavior:
    - 200 OK              → returns dict
    - 404 (not indexed)   → returns None silently (paper just isn't in S2)
    - 429                 → bucket penalty + raises RuntimeError
    - other error         → raises RuntimeError

Cache: TTL 90d (citation counts move slowly). Errors (404) cached 7d so we
don't keep pinging S2 for the same un-indexed paper across runs.
"""
from __future__ import annotations

import json
import os
import sys
from typing import Optional
from urllib.error import HTTPError

from _cache import (
    cache_get_json,
    cache_put,
    cache_get_error,
    cache_put_error,
    TTL_DEFAULTS,
)
from _http import fetch_with_retry
from _token_bucket import get_bucket


API_BASE = "https://api.semanticscholar.org/graph/v1/paper"
FIELDS = (
    "citationCount,influentialCitationCount,year,venue,tldr,"
    "authors.name,authors.hIndex,externalIds,title"
)


def _normalize_id(paper_id: str) -> str:
    """Auto-prefix DOI: / PMID: when caller passes a bare identifier.

    Anything starting with "10." is treated as a DOI; pure digits as PMID.
    Already-prefixed IDs (DOI:..., PMID:..., PMCID:..., ARXIV:...) pass through.
    """
    pid = paper_id.strip()
    if not pid:
        raise ValueError("empty paper_id")
    upper = pid.upper()
    if any(
        upper.startswith(p)
        for p in ("DOI:", "PMID:", "PMCID:", "ARXIV:", "MAG:", "ACL:", "URL:", "CORPUSID:")
    ):
        return pid
    if pid.startswith("10."):
        return f"DOI:{pid}"
    if pid.isdigit():
        return f"PMID:{pid}"
    return pid


def _cache_key(prefixed_id: str) -> str:
    return prefixed_id.replace(":", "_").replace("/", "_")


def fetch(paper_id: str, *, use_cache: bool = True) -> Optional[dict]:
    """Fetch S2 paper metadata. Returns dict or None on 404."""
    prefixed = _normalize_id(paper_id)
    key = _cache_key(prefixed)

    if use_cache:
        cached = cache_get_json("s2", key, ttl_days=TTL_DEFAULTS["s2"])
        if cached is not None:
            return cached
        err = cache_get_error("s2", key)
        if err is not None and err.get("status") == "not_found":
            return None

    url = f"{API_BASE}/{prefixed}?fields={FIELDS}"
    api_key = os.environ.get("SEMANTIC_SCHOLAR_API_KEY")
    headers = {"Accept": "application/json"}
    if api_key:
        headers["x-api-key"] = api_key

    get_bucket("semantic_scholar").acquire()
    try:
        status, body, _ = fetch_with_retry(
            url, headers=headers, timeout=30, bucket="semantic_scholar"
        )
    except HTTPError as e:
        # urllib raises on 4xx; treat 404 as "not indexed"
        if e.code == 404:
            if use_cache:
                cache_put_error("s2", key, "not_found", extra={"via": "semantic_scholar"})
            return None
        raise RuntimeError(f"Semantic Scholar HTTP {e.code} for {prefixed}: {e}")

    if status == 404:
        if use_cache:
            cache_put_error("s2", key, "not_found", extra={"via": "semantic_scholar"})
        return None
    if status != 200:
        raise RuntimeError(f"Semantic Scholar HTTP {status} for {prefixed}")

    try:
        data = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Semantic Scholar returned invalid JSON for {prefixed}: {e}")

    if use_cache:
        cache_put("s2", key, data)
    return data


def _main(argv: list[str]) -> int:
    use_cache = "--no-cache" not in argv
    args = [a for a in argv[1:] if a != "--no-cache"]
    if not args:
        print(
            "usage: semantic_scholar.py <DOI|PMID|prefixed-id> [--no-cache]",
            file=sys.stderr,
        )
        return 1

    try:
        result = fetch(args[0], use_cache=use_cache)
    except Exception as e:
        print(f"[error] {args[0]}: {e}", file=sys.stderr)
        return 1
    if result is None:
        print(f"[info] {args[0]}: not indexed in Semantic Scholar (404)", file=sys.stderr)
        return 2
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
