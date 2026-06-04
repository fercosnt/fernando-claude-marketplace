#!/usr/bin/env python3
"""Unit tests for sci_fetch/_token_bucket.py (stdlib only).

Run: python3 evals/test_token_bucket.py
Exit 0 = pass, 1 = fail.
"""
from __future__ import annotations

import os
import sys
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO / "scripts" / "sci_fetch"))


def test_initial_burst_fills_capacity():
    from _token_bucket import TokenBucket, reset_buckets
    reset_buckets()
    b = TokenBucket(rate_per_sec=10.0, capacity=5, name="burst")
    t0 = time.monotonic()
    for _ in range(5):
        b.acquire()
    elapsed = time.monotonic() - t0
    assert elapsed < 0.1, f"initial burst should be near-instant, got {elapsed:.3f}s"


def test_throttle_after_burst():
    from _token_bucket import TokenBucket
    b = TokenBucket(rate_per_sec=10.0, capacity=5, name="throttle")
    # drain burst
    for _ in range(5):
        b.acquire()
    # next 5 should take ~0.5s
    t0 = time.monotonic()
    for _ in range(5):
        b.acquire()
    elapsed = time.monotonic() - t0
    assert 0.3 < elapsed < 0.8, f"throttle: expected ~0.5s, got {elapsed:.3f}s"


def test_penalize_freezes_bucket():
    from _token_bucket import TokenBucket
    b = TokenBucket(rate_per_sec=100.0, name="pen")
    b.penalize(0.3)
    t0 = time.monotonic()
    b.acquire()
    elapsed = time.monotonic() - t0
    assert 0.25 < elapsed < 0.5, f"penalty should block ~0.3s, got {elapsed:.3f}s"


def test_penalize_does_not_shrink_existing_penalty():
    from _token_bucket import TokenBucket
    b = TokenBucket(rate_per_sec=100.0, name="pen2")
    b.penalize(1.0)
    b.penalize(0.1)  # smaller → must not shrink
    stats = b.stats()
    assert stats["penalty_remaining"] > 0.5, f"penalty was shrunk: {stats}"


def test_concurrent_respects_rate():
    """20 threads, rate=10/s, capacity=1 → min ~1.9s, window never exceeds rate+jitter."""
    from _token_bucket import TokenBucket, reset_buckets
    reset_buckets()
    b = TokenBucket(rate_per_sec=10.0, capacity=1, name="concurrent")
    times: list[float] = []

    def worker():
        b.acquire()
        times.append(time.monotonic())

    threads = [threading.Thread(target=worker) for _ in range(20)]
    t0 = time.monotonic()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    total = time.monotonic() - t0

    assert 1.7 < total < 2.5, f"20 tokens @ 10/s expected ~2s, got {total:.3f}s"

    # Sliding 1s window: max 12 (10 + 1 capacity + 1 scheduler jitter)
    times.sort()
    max_in_window = 0
    for i, ti in enumerate(times):
        window = sum(1 for tj in times[i:] if tj - ti < 1.0)
        max_in_window = max(max_in_window, window)
    assert max_in_window <= 12, f"rate violation: {max_in_window}/sec"


def test_singleton_factory():
    from _token_bucket import get_bucket, reset_buckets
    reset_buckets()
    os.environ.pop("NCBI_API_KEY", None)
    b = get_bucket("ncbi")
    assert b.rate == 3.0, f"no NCBI_API_KEY → 3/s, got {b.rate}"
    assert get_bucket("ncbi") is b, "factory should return singleton"


def test_ncbi_key_raises_rate():
    from _token_bucket import get_bucket, reset_buckets
    reset_buckets()
    os.environ["NCBI_API_KEY"] = "fake-key-for-test"
    try:
        b = get_bucket("ncbi")
        assert b.rate == 10.0, f"with NCBI_API_KEY → 10/s, got {b.rate}"
    finally:
        del os.environ["NCBI_API_KEY"]


def test_unknown_bucket_raises():
    from _token_bucket import get_bucket
    try:
        get_bucket("no_such_api")
    except ValueError:
        return
    assert False, "unknown bucket should raise ValueError"


def test_handle_429_unknown_is_noop():
    """handle_429 on unknown bucket must not crash."""
    from _token_bucket import handle_429
    handle_429("not_a_real_bucket", 5.0)  # should not raise


def test_all_preconfigured_buckets_valid():
    from _token_bucket import get_bucket, reset_buckets
    reset_buckets()
    for name in ("ncbi", "unpaywall", "semantic_scholar", "openalex", "biorxiv"):
        b = get_bucket(name)
        assert b.rate > 0, f"{name} has invalid rate: {b.rate}"


def run_all():
    tests = [
        test_initial_burst_fills_capacity,
        test_throttle_after_burst,
        test_penalize_freezes_bucket,
        test_penalize_does_not_shrink_existing_penalty,
        test_concurrent_respects_rate,
        test_singleton_factory,
        test_ncbi_key_raises_rate,
        test_unknown_bucket_raises,
        test_handle_429_unknown_is_noop,
        test_all_preconfigured_buckets_valid,
    ]
    failures = 0
    for t in tests:
        try:
            t()
            print(f"  ok   {t.__name__}")
        except Exception as e:
            failures += 1
            print(f"  FAIL {t.__name__}: {e}")
    print(f"\n{len(tests) - failures}/{len(tests)} passed")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(run_all())
