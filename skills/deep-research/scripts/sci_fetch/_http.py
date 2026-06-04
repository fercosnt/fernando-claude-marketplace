"""Shared HTTP helpers for sci_fetch scripts (stdlib only).

Provides:
    fetch_with_retry(url, *, headers=None, timeout=60, retries=2, backoff=5)
    make_user_agent(tool="DeepResearchSkill/1.0")
    NCBI rate limit guard (decorator).
"""
from __future__ import annotations

import os
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def make_user_agent(tool: str = "DeepResearchSkill/1.0") -> str:
    email = os.environ.get("UNPAYWALL_EMAIL") or os.environ.get("USER_EMAIL") or "anonymous"
    return f"{tool} ({email})"


CHROME_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)


def fetch_with_retry(
    url: str,
    *,
    headers: dict | None = None,
    timeout: int = 60,
    retries: int = 2,
    backoff: int = 5,
    as_browser: bool = False,
    bucket: str | None = None,
) -> tuple[int, bytes, dict]:
    """Fetch URL. Returns (status_code, body_bytes, response_headers_dict).

    On final failure raises the last exception.
    Respects HTTP 429 / 503 with exponential backoff.

    bucket: optional token-bucket name (e.g., "ncbi"). When a 429 arrives,
            the entire bucket is penalized via handle_429() so every thread
            sharing that API backs off together, not just this call.
    """
    base_headers = {
        "User-Agent": CHROME_UA if as_browser else make_user_agent(),
        "Accept": "*/*",
    }
    if headers:
        base_headers.update(headers)

    last_err: Exception | None = None
    for attempt in range(retries + 1):
        try:
            req = Request(url, headers=base_headers)
            with urlopen(req, timeout=timeout) as resp:
                body = resp.read()
                return resp.status, body, dict(resp.headers)
        except HTTPError as e:
            last_err = e
            if e.code in (429, 503) and attempt < retries:
                # Honor server-provided Retry-After when present; else exponential backoff.
                retry_after_hdr = e.headers.get("Retry-After") if e.headers else None
                try:
                    sleep_s = int(retry_after_hdr) if retry_after_hdr else backoff * (2 ** attempt)
                except (TypeError, ValueError):
                    sleep_s = backoff * (2 ** attempt)
                if e.code == 429 and bucket:
                    try:
                        from _token_bucket import handle_429
                        handle_429(bucket, sleep_s)
                    except ImportError:
                        pass
                print(f"[warn] {url} HTTP {e.code}; sleep {sleep_s}s", file=sys.stderr)
                time.sleep(sleep_s)
                continue
            raise
        except (URLError, TimeoutError) as e:
            last_err = e
            if attempt < retries:
                time.sleep(backoff * (2 ** attempt))
                continue
            raise
    if last_err:
        raise last_err
    raise RuntimeError("unreachable")


# NCBI rate-limit guard. Delegates to the shared token bucket so parallel
# workers coordinate and 429 responses freeze everyone, not just the caller.
# Falls back to a single-threaded min-interval sleep if the bucket module is
# unavailable (kept for backward compat with standalone script invocation).
_last_ncbi_call = 0.0


def ncbi_throttle() -> None:
    try:
        from _token_bucket import get_bucket
        get_bucket("ncbi").acquire()
        return
    except (ImportError, ValueError):
        pass
    global _last_ncbi_call
    has_key = bool(os.environ.get("NCBI_API_KEY"))
    min_interval = 0.11 if has_key else 0.34  # 10/s or 3/s
    now = time.monotonic()
    delta = now - _last_ncbi_call
    if delta < min_interval:
        time.sleep(min_interval - delta)
    _last_ncbi_call = time.monotonic()


def ncbi_api_key_param() -> str:
    """Return '&api_key=...' suffix if NCBI_API_KEY env var is set, else ''."""
    key = os.environ.get("NCBI_API_KEY")
    return f"&api_key={key}" if key else ""
