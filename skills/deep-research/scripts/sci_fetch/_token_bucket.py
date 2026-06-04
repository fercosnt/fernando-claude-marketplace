"""Thread-safe token bucket rate limiter for sci_fetch APIs (stdlib only).

Usage:
    from _token_bucket import get_bucket
    get_bucket("ncbi").acquire()
    # ... hit NCBI API ...

Buckets pre-configurados (criados lazily na 1a chamada):
    ncbi              3 req/s sem NCBI_API_KEY, 10 req/s com
    unpaywall         5 req/s
    semantic_scholar  1 req/s sem SEMANTIC_SCHOLAR_API_KEY, 10 req/s com
    openalex          10 req/s
    biorxiv           2 req/s

Chamar `bucket.penalize(seconds)` ao receber HTTP 429 congela o bucket
inteiro (nao so o worker afetado).
"""
from __future__ import annotations

import os
import threading
import time


class TokenBucket:
    """Thread-safe leaky-bucket rate limiter.

    rate_per_sec: tokens gerados por segundo
    capacity: teto de tokens acumulados (default: ceil(rate))
    """

    def __init__(
        self,
        rate_per_sec: float,
        capacity: int | None = None,
        *,
        name: str = "",
    ) -> None:
        if rate_per_sec <= 0:
            raise ValueError("rate_per_sec must be > 0")
        self.rate = float(rate_per_sec)
        self.capacity = float(capacity if capacity is not None else max(1, int(rate_per_sec + 0.999)))
        self.tokens = self.capacity  # start full (allow initial burst)
        self.last_refill = time.monotonic()
        self.penalty_until = 0.0
        self._lock = threading.Lock()
        self.name = name or "unnamed"

    def _refill_locked(self, now: float) -> None:
        elapsed = now - self.last_refill
        if elapsed > 0:
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
            self.last_refill = now

    def acquire(self, tokens: int = 1) -> None:
        """Block until `tokens` can be consumed, respecting rate + penalty."""
        if tokens < 1:
            return
        while True:
            with self._lock:
                now = time.monotonic()
                if now < self.penalty_until:
                    sleep_for = self.penalty_until - now
                else:
                    self._refill_locked(now)
                    if self.tokens >= tokens:
                        self.tokens -= tokens
                        return
                    deficit = tokens - self.tokens
                    sleep_for = deficit / self.rate
            # sleep outside the lock so other threads can progress
            time.sleep(max(0.001, sleep_for))

    def penalize(self, seconds: float) -> None:
        """Freeze the bucket for `seconds` (global backoff on 429)."""
        if seconds <= 0:
            return
        with self._lock:
            self.tokens = 0.0
            target = time.monotonic() + seconds
            if target > self.penalty_until:
                self.penalty_until = target

    def stats(self) -> dict:
        with self._lock:
            now = time.monotonic()
            self._refill_locked(now)
            return {
                "name": self.name,
                "rate_per_sec": self.rate,
                "capacity": self.capacity,
                "tokens": round(self.tokens, 2),
                "penalty_remaining": max(0.0, self.penalty_until - now),
            }


_BUCKETS: dict[str, TokenBucket] = {}
_BUCKETS_LOCK = threading.Lock()


def _default_rate(name: str) -> float:
    if name == "ncbi":
        return 10.0 if os.environ.get("NCBI_API_KEY") else 3.0
    if name == "unpaywall":
        return 5.0
    if name == "semantic_scholar":
        return 10.0 if os.environ.get("SEMANTIC_SCHOLAR_API_KEY") else 1.0
    if name == "openalex":
        return 10.0
    if name == "biorxiv":
        return 2.0
    raise ValueError(f"unknown bucket: {name}")


def get_bucket(name: str) -> TokenBucket:
    """Return (creating if needed) the singleton bucket for `name`."""
    with _BUCKETS_LOCK:
        b = _BUCKETS.get(name)
        if b is None:
            b = TokenBucket(rate_per_sec=_default_rate(name), name=name)
            _BUCKETS[name] = b
        return b


def reset_buckets() -> None:
    """Clear all singletons. Used by tests; not for production."""
    with _BUCKETS_LOCK:
        _BUCKETS.clear()


def handle_429(bucket_name: str, retry_after: float = 60.0) -> None:
    """Penalty hook for HTTP 429 responses."""
    try:
        get_bucket(bucket_name).penalize(retry_after)
    except ValueError:
        # Unknown bucket name — no-op rather than crash the pipeline.
        pass


def _main(argv: list[str]) -> int:
    """CLI: print current bucket stats as JSON."""
    import json
    import sys

    names = argv[1:] or ["ncbi", "unpaywall", "semantic_scholar", "openalex", "biorxiv"]
    out = {}
    for n in names:
        try:
            out[n] = get_bucket(n).stats()
        except ValueError as e:
            out[n] = {"error": str(e)}
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(_main(sys.argv))
