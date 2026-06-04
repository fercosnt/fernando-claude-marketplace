#!/usr/bin/env python3
"""F5 tests for the v3 academic-graph API clients (semantic_scholar, openalex,
biorxiv_fallback). Mocked by default (no network); pass --live to run a single
real-API smoke test per client to catch upstream schema breakage.

Run:
    python3 evals/test_v3_apis.py
    python3 evals/test_v3_apis.py --live    # opt-in live smoke
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO / "scripts" / "sci_fetch"))


def _isolate_cache() -> Path:
    tmp = Path(tempfile.mkdtemp(prefix="drsci_v3apis_"))
    os.environ["DR_SCI_CACHE_ROOT"] = str(tmp)
    os.environ.pop("DR_SCI_NO_CACHE", None)
    return tmp


def _reload_modules(names: list[str]) -> None:
    import importlib
    for n in names:
        sys.modules.pop(n, None)
    for n in names:
        importlib.import_module(n)


def _patch_http(module, *, status: int = 200, body: bytes = b"{}", raises=None):
    """Replace the module's fetch_with_retry with a fake. raises wins over status."""
    calls = {"n": 0}

    def fake_fetch(url, **kwargs):
        calls["n"] += 1
        if raises is not None:
            raise raises
        return status, body, {}

    module.fetch_with_retry = fake_fetch
    return calls


def _patch_bucket(module):
    """No-op the token bucket so tests don't sleep."""
    class _NoOpBucket:
        def acquire(self, tokens: int = 1) -> None: pass
        def penalize(self, seconds: float) -> None: pass
    module.get_bucket = lambda name: _NoOpBucket()


# ---------------------------------------------------------------------------
# semantic_scholar
# ---------------------------------------------------------------------------
def test_s2_normalize_id():
    _isolate_cache()
    _reload_modules(["_cache", "_token_bucket", "_http", "semantic_scholar"])
    import semantic_scholar as s2
    assert s2._normalize_id("10.1089/thy.2014.0028") == "DOI:10.1089/thy.2014.0028"
    assert s2._normalize_id("33567185") == "PMID:33567185"
    assert s2._normalize_id("DOI:10.1/x") == "DOI:10.1/x"
    assert s2._normalize_id("PMID:1") == "PMID:1"
    assert s2._normalize_id("PMCID:PMC123") == "PMCID:PMC123"


def test_s2_fetch_success_then_cache_hit():
    _isolate_cache()
    _reload_modules(["_cache", "_token_bucket", "_http", "semantic_scholar"])
    import semantic_scholar as s2
    body = json.dumps({
        "citationCount": 156,
        "influentialCitationCount": 23,
        "year": 2015,
        "venue": "Thyroid",
        "title": "Magnesium supplementation",
    }).encode()
    calls = _patch_http(s2, status=200, body=body)
    _patch_bucket(s2)

    first = s2.fetch("10.1089/thy.2014.0028")
    assert first is not None
    assert first["citationCount"] == 156
    assert calls["n"] == 1

    second = s2.fetch("10.1089/thy.2014.0028")
    assert second is not None and second["venue"] == "Thyroid"
    assert calls["n"] == 1, f"expected 1 API call after cache hit, got {calls['n']}"


def test_s2_404_returns_none_and_caches_error():
    _isolate_cache()
    _reload_modules(["_cache", "_token_bucket", "_http", "semantic_scholar"])
    import semantic_scholar as s2
    from urllib.error import HTTPError
    err = HTTPError("u", 404, "Not Found", {}, None)
    calls = _patch_http(s2, raises=err)
    _patch_bucket(s2)

    out = s2.fetch("10.1/missing")
    assert out is None
    assert calls["n"] == 1

    # Second call hits error cache → no API call
    out2 = s2.fetch("10.1/missing")
    assert out2 is None
    assert calls["n"] == 1


def test_s2_500_raises():
    _isolate_cache()
    _reload_modules(["_cache", "_token_bucket", "_http", "semantic_scholar"])
    import semantic_scholar as s2
    from urllib.error import HTTPError
    _patch_http(s2, raises=HTTPError("u", 500, "Server Error", {}, None))
    _patch_bucket(s2)
    try:
        s2.fetch("10.1/error")
    except RuntimeError as e:
        assert "500" in str(e)
    else:
        raise AssertionError("expected RuntimeError on 500")


# ---------------------------------------------------------------------------
# openalex
# ---------------------------------------------------------------------------
def test_oa_quartile_thresholds():
    _isolate_cache()
    _reload_modules(["_cache", "_token_bucket", "_http", "openalex"])
    import openalex as oa
    assert oa._quartile(60) == "Q1"
    assert oa._quartile(50) == "Q2"  # boundary: > 50 = Q1, == 50 = Q2
    assert oa._quartile(20) == "Q2"
    assert oa._quartile(19) == "Q3"
    assert oa._quartile(5) == "Q3"
    assert oa._quartile(4) == "Q4"
    assert oa._quartile(None) is None


def test_oa_parse_extracts_venue_and_concepts():
    _isolate_cache()
    _reload_modules(["_cache", "_token_bucket", "_http", "openalex"])
    import openalex as oa
    raw = {
        "id": "https://openalex.org/W2057382412",
        "doi": "https://doi.org/10.1089/thy.2014.0028",
        "title": "Magnesium and thyroid",
        "publication_year": 2015,
        "cited_by_count": 234,
        "primary_location": {
            "source": {"display_name": "Thyroid", "h_index": 68},
        },
        "concepts": [
            {"display_name": "Hashimoto disease", "score": 0.89},
            {"display_name": "Magnesium",         "score": 0.85},
            {"display_name": "Thyroiditis",       "score": 0.72},
            {"display_name": "Endocrinology",     "score": 0.40},  # filtered (<0.7)
        ],
    }
    parsed = oa._parse(raw)
    assert parsed["work_id"] == "W2057382412"
    assert parsed["doi"] == "10.1089/thy.2014.0028"
    assert parsed["venue_h_index"] == 68
    assert parsed["venue_quartile"] == "Q1"
    assert len(parsed["concepts"]) == 3
    assert parsed["concepts"][0]["display_name"] == "Hashimoto disease"


def test_oa_fetch_404_returns_none():
    _isolate_cache()
    _reload_modules(["_cache", "_token_bucket", "_http", "openalex"])
    import openalex as oa
    from urllib.error import HTTPError
    calls = _patch_http(oa, raises=HTTPError("u", 404, "Not Found", {}, None))
    _patch_bucket(oa)
    out = oa.fetch("10.1/missing")
    assert out is None
    assert calls["n"] == 1
    out2 = oa.fetch("10.1/missing")
    assert out2 is None
    assert calls["n"] == 1  # error cache prevented re-fetch


def test_oa_fetch_success_caches():
    _isolate_cache()
    _reload_modules(["_cache", "_token_bucket", "_http", "openalex"])
    import openalex as oa
    body = json.dumps({
        "id": "https://openalex.org/W1",
        "doi": "https://doi.org/10.1/x",
        "title": "Test",
        "publication_year": 2020,
        "cited_by_count": 50,
        "primary_location": {"source": {"display_name": "Nature", "h_index": 100}},
        "concepts": [],
    }).encode()
    calls = _patch_http(oa, status=200, body=body)
    _patch_bucket(oa)
    out1 = oa.fetch("10.1/x")
    assert out1["venue_quartile"] == "Q1"
    assert calls["n"] == 1
    out2 = oa.fetch("10.1/x")
    assert out2["venue"] == "Nature"
    assert calls["n"] == 1


# ---------------------------------------------------------------------------
# biorxiv_fallback
# ---------------------------------------------------------------------------
def test_biorxiv_picks_latest_version():
    _isolate_cache()
    _reload_modules(["_cache", "_token_bucket", "_http", "biorxiv_fallback"])
    import biorxiv_fallback as bx
    body = json.dumps({
        "collection": [
            {"doi": "10.1101/2024.01.15.123456", "version": "1", "date": "2024-01-15", "title": "T"},
            {"doi": "10.1101/2024.01.15.123456", "version": "2", "date": "2024-02-20", "title": "T"},
        ]
    }).encode()
    _patch_http(bx, status=200, body=body)
    _patch_bucket(bx)

    out = bx.find_preprint("10.1101/2024.01.15.123456", validate_pdf=False)
    assert out is not None
    assert out["version"] == 2
    assert out["preprint_server"] == "bioRxiv"
    assert "v2.full.pdf" in out["pdf_url"]


def test_biorxiv_no_preprint_returns_none_and_caches():
    _isolate_cache()
    _reload_modules(["_cache", "_token_bucket", "_http", "biorxiv_fallback"])
    import biorxiv_fallback as bx
    from urllib.error import HTTPError
    calls = _patch_http(bx, raises=HTTPError("u", 404, "Not Found", {}, None))
    _patch_bucket(bx)

    out = bx.find_preprint("10.1/no-preprint", validate_pdf=False)
    assert out is None
    # Both bioRxiv and medRxiv tried → 2 calls.
    assert calls["n"] == 2

    # Second invocation: error cache short-circuits → 0 new calls.
    out2 = bx.find_preprint("10.1/no-preprint", validate_pdf=False)
    assert out2 is None
    assert calls["n"] == 2


def test_biorxiv_empty_collection_falls_through_to_medrxiv():
    _isolate_cache()
    _reload_modules(["_cache", "_token_bucket", "_http", "biorxiv_fallback"])
    import biorxiv_fallback as bx

    # First call (biorxiv) → empty; second call (medrxiv) → has data.
    seq = [
        (200, json.dumps({"collection": []}).encode()),
        (200, json.dumps({
            "collection": [
                {"doi": "10.1101/med", "version": "1", "date": "2024-03-01", "title": "MedT"},
            ]
        }).encode()),
    ]
    state = {"i": 0}

    def fake_fetch(url, **kw):
        i = state["i"]
        state["i"] += 1
        return seq[i][0], seq[i][1], {}

    bx.fetch_with_retry = fake_fetch
    _patch_bucket(bx)

    out = bx.find_preprint("10.1101/med", validate_pdf=False)
    assert out is not None
    assert out["preprint_server"] == "medRxiv"
    assert out["version"] == 1


# ---------------------------------------------------------------------------
# Live smoke (opt-in via --live)
# ---------------------------------------------------------------------------
def smoke_live_s2():
    _isolate_cache()
    _reload_modules(["_cache", "_token_bucket", "_http", "semantic_scholar"])
    import semantic_scholar as s2
    out = s2.fetch("10.1089/thy.2014.0028")
    assert out is not None, "S2 returned None for known DOI — schema may have changed"
    assert "citationCount" in out, f"missing citationCount: {out.keys()}"
    print(f"[live] S2 OK: cit={out.get('citationCount')}, venue={out.get('venue')}")


def smoke_live_oa():
    _isolate_cache()
    _reload_modules(["_cache", "_token_bucket", "_http", "openalex"])
    import openalex as oa
    out = oa.fetch("10.1089/thy.2014.0028")
    assert out is not None, "OA returned None for known DOI"
    assert out.get("cited_by_count") is not None
    print(f"[live] OA OK: cited={out['cited_by_count']}, venue={out.get('venue')}, h_idx={out.get('venue_h_index')}")


def smoke_live_biorxiv():
    _isolate_cache()
    _reload_modules(["_cache", "_token_bucket", "_http", "biorxiv_fallback"])
    import biorxiv_fallback as bx
    # A known recent bioRxiv preprint — DOI prefix 10.1101 is the bioRxiv namespace.
    # We don't assert it's found; we just assert the call doesn't crash.
    try:
        out = bx.find_preprint("10.1101/2020.02.07.20021154", validate_pdf=False)
    except Exception as e:
        raise AssertionError(f"biorxiv live call raised: {e}")
    print(f"[live] bioRxiv reachable; preprint_found={out is not None}")


def main(argv: list[str]) -> int:
    live = "--live" in argv
    tests = [
        test_s2_normalize_id,
        test_s2_fetch_success_then_cache_hit,
        test_s2_404_returns_none_and_caches_error,
        test_s2_500_raises,
        test_oa_quartile_thresholds,
        test_oa_parse_extracts_venue_and_concepts,
        test_oa_fetch_404_returns_none,
        test_oa_fetch_success_caches,
        test_biorxiv_picks_latest_version,
        test_biorxiv_no_preprint_returns_none_and_caches,
        test_biorxiv_empty_collection_falls_through_to_medrxiv,
    ]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
        except AssertionError as e:
            print(f"FAIL  {t.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"ERROR {t.__name__}: {type(e).__name__}: {e}")
            failed += 1

    if live:
        print("--- live smoke ---")
        for fn in (smoke_live_s2, smoke_live_oa, smoke_live_biorxiv):
            try:
                fn()
                print(f"PASS  {fn.__name__}")
            except Exception as e:
                print(f"FAIL  {fn.__name__}: {type(e).__name__}: {e}")
                failed += 1

    print(f"\n{len(tests)} mocked tests | {failed} failures")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
