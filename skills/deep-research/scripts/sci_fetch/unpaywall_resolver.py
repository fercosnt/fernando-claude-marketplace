#!/usr/bin/env python3
"""Resolve a DOI to its open-access PDF/landing URL via Unpaywall.

Usage:
    python unpaywall_resolver.py <DOI>

Requires env var UNPAYWALL_EMAIL (API is free but requires email).

Output: JSON {doi, is_oa, oa_pdf_url, oa_landing_url, host_type}
Exit codes: 0 OA found, 1 error, 2 paywall / not OA.
"""
from __future__ import annotations

import json
import os
import sys

from _http import fetch_with_retry
from _cache import cache_get_json, cache_put, cache_get_error, cache_put_error, TTL_DEFAULTS
from _token_bucket import get_bucket


UNPAYWALL = "https://api.unpaywall.org/v2/{doi}?email={email}"


def _not_oa(doi: str, *, from_cache: str | None = None) -> dict:
    out = {
        "doi": doi,
        "is_oa": False,
        "oa_pdf_url": None,
        "oa_landing_url": None,
        "host_type": None,
    }
    if from_cache:
        out["from_cache"] = from_cache
    return out


def resolve(doi: str, email: str, *, use_cache: bool = True) -> dict:
    """Resolve DOI via Unpaywall, with local cache + error cache.

    use_cache: bypass cache entirely when False (e.g., --no-cache flag).
               Positive responses cached 30d; is_oa=false cached 7d via error cache
               (so we don't re-hit the API 3x in the same session).
    """
    if use_cache:
        cached = cache_get_json("doi", doi, ttl_days=TTL_DEFAULTS["doi"])
        if cached is not None:
            cached = dict(cached)
            cached["from_cache"] = "hit"
            return cached
        err = cache_get_error("doi", doi)
        if err is not None and err.get("status") == "not_oa":
            return _not_oa(doi, from_cache="error")

    get_bucket("unpaywall").acquire()
    url = UNPAYWALL.format(doi=doi, email=email)
    status, body, _ = fetch_with_retry(url, timeout=30, bucket="unpaywall")
    if status != 200:
        raise RuntimeError(f"Unpaywall HTTP {status} for {doi}")
    data = json.loads(body.decode("utf-8"))

    is_oa = bool(data.get("is_oa"))
    locations = data.get("oa_locations") or []
    # Prefer repository (preprint) over publisher.
    locations.sort(
        key=lambda loc: (
            0 if loc.get("host_type") == "repository" else 1,
            0 if loc.get("url_for_pdf") else 1,
        )
    )
    best = locations[0] if locations else None

    result = {
        "doi": doi,
        "is_oa": is_oa,
        "oa_pdf_url": (best or {}).get("url_for_pdf"),
        "oa_landing_url": (best or {}).get("url"),
        "host_type": (best or {}).get("host_type"),
    }

    if use_cache:
        if is_oa and result["oa_pdf_url"]:
            cache_put("doi", doi, result)
        else:
            cache_put_error("doi", doi, "not_oa", extra={"via": "unpaywall"})

    return result


def _main(argv: list[str]) -> int:
    use_cache = True
    args = [a for a in argv[1:] if a != "--no-cache"]
    if "--no-cache" in argv:
        use_cache = False

    if not args:
        print("usage: unpaywall_resolver.py <DOI> [--no-cache]", file=sys.stderr)
        return 1

    email = os.environ.get("UNPAYWALL_EMAIL")
    if not email:
        print("[error] env UNPAYWALL_EMAIL not set", file=sys.stderr)
        return 1

    doi = args[0].strip()
    # Accept full URLs too.
    if doi.startswith("http"):
        from urllib.parse import urlparse

        p = urlparse(doi)
        doi = p.path.lstrip("/")
        if doi.startswith("doi/"):
            doi = doi[4:]

    try:
        result = resolve(doi, email, use_cache=use_cache)
    except Exception as e:
        print(f"[error] {doi}: {e}", file=sys.stderr)
        return 1

    json.dump(result, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0 if result["is_oa"] else 2


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
