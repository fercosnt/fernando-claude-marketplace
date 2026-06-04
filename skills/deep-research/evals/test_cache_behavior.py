#!/usr/bin/env python3
"""Unit tests for sci_fetch/_cache.py (stdlib only).

Run: python3 evals/test_cache_behavior.py
Exit 0 = pass, 1 = fail.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO / "scripts" / "sci_fetch"))


def _isolate_cache() -> Path:
    tmp = Path(tempfile.mkdtemp(prefix="drsci_cache_"))
    os.environ["DR_SCI_CACHE_ROOT"] = str(tmp)
    os.environ.pop("DR_SCI_NO_CACHE", None)
    return tmp


def _reset_module():
    # _cache has no state, but clear any test leftovers between tests.
    pass


def test_hit_miss():
    _isolate_cache()
    from _cache import cache_put, cache_get
    assert cache_get("pmid", "42") is None, "empty should miss"
    cache_put("pmid", "42", "abstract content")
    assert cache_get("pmid", "42") == "abstract content"


def test_json_roundtrip():
    _isolate_cache()
    from _cache import cache_put, cache_get_json
    payload = {"is_oa": True, "oa_pdf_url": "https://example.com/x.pdf", "host_type": "repository"}
    cache_put("doi", "10.1234/abc", payload)
    got = cache_get_json("doi", "10.1234/abc")
    assert got == payload, f"roundtrip mismatch: {got}"


def test_binary_roundtrip():
    _isolate_cache()
    from _cache import cache_put, cache_get
    blob = b"%PDF-1.7\n\x00\x01\x02 binary content"
    cache_put("pdf", "deadbeef", blob, binary=True)
    got = cache_get("pdf", "deadbeef", binary=True)
    assert got == blob


def test_ttl_expiration(monkey_mtime=True):
    root = _isolate_cache()
    from _cache import cache_put, cache_get, cache_path
    cache_put("pmid", "33567185", "fresh content")
    # ttl_days=-1 forces expired semantics
    assert cache_get("pmid", "33567185", ttl_days=-1) is None, "neg ttl should be expired"
    # simulate aged file by setting mtime to past
    p = cache_path("pmid", "33567185")
    old = time.time() - 400 * 86400  # 400 days ago
    os.utime(p, (old, old))
    assert cache_get("pmid", "33567185", ttl_days=365) is None, "400d > 365d TTL"
    assert cache_get("pmid", "33567185", ttl_days=500) == "fresh content", "500d TTL still fresh"


def test_safe_key_encoding():
    _isolate_cache()
    from _cache import cache_put, cache_get, cache_path
    key = "10.1089/thy.2014.0028"
    cache_put("doi", key, {"x": 1})
    p = cache_path("doi", key)
    assert "/" not in p.name, f"path contains slash: {p.name}"
    assert p.exists(), "file should exist"


def test_error_cache():
    _isolate_cache()
    from _cache import cache_put_error, cache_get_error
    cache_put_error("doi", "10.1/paywalled", "not_oa", extra={"reason": "publisher"})
    err = cache_get_error("doi", "10.1/paywalled")
    assert err is not None
    assert err["status"] == "not_oa"
    assert err["reason"] == "publisher"
    assert "cached_at" in err


def test_bypass_via_env():
    _isolate_cache()
    from _cache import cache_put, cache_get
    cache_put("pmid", "stored", "value")
    os.environ["DR_SCI_NO_CACHE"] = "1"
    try:
        assert cache_get("pmid", "stored") is None, "bypass should miss"
        # put becomes no-op too
        cache_put("pmid", "new_key", "x")
    finally:
        del os.environ["DR_SCI_NO_CACHE"]
    # outside bypass: stored is still there, new_key is not
    assert cache_get("pmid", "stored") == "value"
    assert cache_get("pmid", "new_key") is None


def test_corrupt_json_recovery():
    root = _isolate_cache()
    from _cache import cache_get_json, cache_path
    # write garbage directly, skipping cache_put
    p = cache_path("doi", "corrupted")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("this is not { valid json }")
    assert cache_get_json("doi", "corrupted") is None, "corrupt should miss"
    # original file should be renamed, original slot gone
    assert not p.exists(), "corrupt file should be renamed"
    corrupt_files = list(p.parent.glob(f"{p.name}.corrupt-*"))
    assert corrupt_files, "corrupt file should have been renamed"


def test_atomic_write_no_partial():
    """Simulate no .tmp leftover after successful put."""
    _isolate_cache()
    from _cache import cache_put, cache_path
    cache_put("pmid", "atomic", "ok")
    p = cache_path("pmid", "atomic")
    assert p.exists()
    assert not p.with_suffix(p.suffix + ".tmp").exists(), "tmp should be renamed away"


def test_concurrent_write_no_corruption():
    _isolate_cache()
    from _cache import cache_put, cache_get_json

    errors: list[Exception] = []

    def writer(i: int):
        try:
            cache_put("doi", "concurrent", {"writer": i, "payload": "x" * 500})
        except Exception as e:
            errors.append(e)

    threads = [threading.Thread(target=writer, args=(i,)) for i in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors, f"writer errors: {errors}"
    final = cache_get_json("doi", "concurrent")
    assert final is not None, "should have a valid final value"
    assert 0 <= final["writer"] < 10, f"malformed final: {final}"


def test_clear():
    _isolate_cache()
    from _cache import cache_put, cache_get, cache_clear
    cache_put("pmid", "1", "a")
    cache_put("pmid", "2", "b")
    cache_put("doi", "x", {"k": "v"})
    removed = cache_clear(kinds=["pmid"])
    assert removed == 2, f"should remove 2 pmid files, got {removed}"
    assert cache_get("pmid", "1") is None
    from _cache import cache_get_json
    assert cache_get_json("doi", "x") == {"k": "v"}, "doi should survive"


def test_clear_before_date():
    _isolate_cache()
    from _cache import cache_put, cache_clear, cache_path
    cache_put("pmid", "old", "a")
    p_old = cache_path("pmid", "old")
    past = time.time() - 100 * 86400
    os.utime(p_old, (past, past))

    cache_put("pmid", "new", "b")

    cutoff = time.time() - 50 * 86400
    removed = cache_clear(before_date=cutoff, kinds=["pmid"])
    assert removed == 1, f"should remove only 'old': {removed}"


def run_all():
    tests = [
        test_hit_miss,
        test_json_roundtrip,
        test_binary_roundtrip,
        test_ttl_expiration,
        test_safe_key_encoding,
        test_error_cache,
        test_bypass_via_env,
        test_corrupt_json_recovery,
        test_atomic_write_no_partial,
        test_concurrent_write_no_corruption,
        test_clear,
        test_clear_before_date,
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
