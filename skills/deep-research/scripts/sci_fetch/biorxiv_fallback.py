#!/usr/bin/env python3
"""bioRxiv / medRxiv preprint fallback for paywalled DOIs (stdlib only).

Endpoints (queried in order):
    https://api.biorxiv.org/details/biorxiv/{doi}
    https://api.biorxiv.org/details/medrxiv/{doi}

When Unpaywall says is_oa=false but a preprint exists in bioRxiv/medRxiv,
this client surfaces the open preprint as a fallback source.

Returns most-recent version when multiple exist:
    {
      "preprint_doi":    "10.1101/2024.01.15.123456",
      "pdf_url":         "https://www.biorxiv.org/content/10.1101/.../v1.full.pdf",
      "preprint_server": "bioRxiv" | "medRxiv",
      "version":         1,
      "posted_date":     "2024-01-15",
      "title":           "..."
    }

PDF URL is HEAD-validated before returning (avoids dead links propagating).

Cache TTL: 30d (preprints can have new versions; refresh monthly).
"""
from __future__ import annotations

import json
import sys
from typing import Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from _cache import (
    cache_get_json,
    cache_put,
    cache_get_error,
    cache_put_error,
    TTL_DEFAULTS,
)
from _http import fetch_with_retry, make_user_agent
from _token_bucket import get_bucket


API_BASE = "https://api.biorxiv.org/details"
SERVERS = ("biorxiv", "medrxiv")


def _safe_doi_key(doi: str) -> str:
    return doi.replace("/", "_").replace(":", "_")


def _head(url: str, timeout: int = 10) -> int:
    """Minimal HEAD request returning HTTP status code; -1 on network error."""
    try:
        req = Request(url, method="HEAD", headers={"User-Agent": make_user_agent()})
        with urlopen(req, timeout=timeout) as resp:
            return resp.status
    except HTTPError as e:
        return e.code
    except (URLError, TimeoutError):
        return -1


def _query_server(server: str, doi: str) -> Optional[list[dict]]:
    """Query one preprint server. Returns list of versions or None on miss/error."""
    get_bucket("biorxiv").acquire()
    url = f"{API_BASE}/{server}/{doi}"
    try:
        status, body, _ = fetch_with_retry(url, timeout=20, bucket="biorxiv")
    except HTTPError as e:
        if e.code == 404:
            return None
        raise
    if status != 200:
        return None
    try:
        data = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None

    collection = data.get("collection") or []
    if not collection:
        # bioRxiv API uses "messages" with status="no posts found" on miss.
        return None
    return collection


def _build_pdf_url(server: str, doi: str, version: int) -> str:
    return f"https://www.{server}.org/content/{doi}v{version}.full.pdf"


def find_preprint(doi: str, *, use_cache: bool = True, validate_pdf: bool = True) -> Optional[dict]:
    """Find a bioRxiv/medRxiv preprint for the given DOI.

    validate_pdf: HEAD-check the PDF URL before returning. Set False in tests
    or when network is constrained.

    Returns most-recent version if found, None otherwise.
    """
    if not doi:
        raise ValueError("empty doi")
    key = _safe_doi_key(doi)

    if use_cache:
        cached = cache_get_json("biorxiv", key, ttl_days=TTL_DEFAULTS["biorxiv"])
        if cached is not None:
            # Cached "no preprint" sentinel: {"preprint_server": null}
            if cached.get("preprint_server") is None:
                return None
            return cached
        err = cache_get_error("biorxiv", key)
        if err is not None and err.get("status") == "not_found":
            return None

    for server in SERVERS:
        try:
            collection = _query_server(server, doi)
        except Exception as e:
            print(f"[warn] biorxiv_fallback {server}/{doi}: {e}", file=sys.stderr)
            continue
        if not collection:
            continue

        # Most recent version wins. bioRxiv `version` field is a string.
        def _ver(entry: dict) -> int:
            try:
                return int(entry.get("version") or 0)
            except (TypeError, ValueError):
                return 0

        latest = max(collection, key=_ver)
        version = _ver(latest)
        if version <= 0:
            continue

        preprint_doi = latest.get("doi") or doi
        pdf_url = _build_pdf_url(server, preprint_doi, version)
        if validate_pdf:
            head_status = _head(pdf_url)
            # 200 OK or 302/301 redirects to the PDF are both acceptable.
            if head_status not in (200, 301, 302):
                # Try v{version} without .full suffix as a last resort.
                alt_url = f"https://www.{server}.org/content/{preprint_doi}v{version}.pdf"
                if _head(alt_url) in (200, 301, 302):
                    pdf_url = alt_url
                else:
                    continue

        result = {
            "preprint_doi": preprint_doi,
            "pdf_url": pdf_url,
            "preprint_server": "bioRxiv" if server == "biorxiv" else "medRxiv",
            "version": version,
            "posted_date": latest.get("date"),
            "title": latest.get("title"),
        }
        if use_cache:
            cache_put("biorxiv", key, result)
        return result

    if use_cache:
        # Negative result: cache as "no preprint" sentinel (TTL 30d via biorxiv kind),
        # plus an error record so we don't keep pinging both endpoints back-to-back.
        cache_put_error("biorxiv", key, "not_found", extra={"via": "biorxiv_fallback"})
    return None


def _main(argv: list[str]) -> int:
    use_cache = "--no-cache" not in argv
    skip_head = "--no-validate" in argv
    args = [a for a in argv[1:] if a not in ("--no-cache", "--no-validate")]
    if not args:
        print(
            "usage: biorxiv_fallback.py <DOI> [--no-cache] [--no-validate]",
            file=sys.stderr,
        )
        return 1
    try:
        result = find_preprint(args[0].strip(), use_cache=use_cache, validate_pdf=not skip_head)
    except Exception as e:
        print(f"[error] {args[0]}: {e}", file=sys.stderr)
        return 1
    if result is None:
        print(f"[info] {args[0]}: no preprint found in bioRxiv/medRxiv", file=sys.stderr)
        return 2
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
