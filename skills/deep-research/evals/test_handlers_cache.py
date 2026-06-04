#!/usr/bin/env python3
"""F3 integration tests: verify cache hits/miss on the NCBI + OA handlers
without hitting the real network. Uses monkey-patching of `fetch_with_retry`
and an isolated cache root.

Run: python3 evals/test_handlers_cache.py
"""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO / "scripts" / "sci_fetch"))


def _isolate_cache() -> Path:
    tmp = Path(tempfile.mkdtemp(prefix="drsci_handlers_"))
    os.environ["DR_SCI_CACHE_ROOT"] = str(tmp)
    os.environ.pop("DR_SCI_NO_CACHE", None)
    return tmp


def _reload_modules(names: list[str]) -> None:
    """Drop then reimport modules so they pick up the new cache root env."""
    import importlib
    for n in names:
        if n in sys.modules:
            del sys.modules[n]
    for n in names:
        importlib.import_module(n)


def test_pubmed_abstract_cache_hit():
    _isolate_cache()
    _reload_modules(["_http", "_cache", "pubmed_abstract"])
    import pubmed_abstract
    import _http as http_mod

    calls = {"n": 0}
    sample = "A" * 500  # >100 chars → success path

    def fake_fetch(url, **kwargs):
        calls["n"] += 1
        return 200, sample.encode("utf-8"), {}

    http_mod.fetch_with_retry = fake_fetch
    pubmed_abstract.fetch_with_retry = fake_fetch
    pubmed_abstract.ncbi_throttle = lambda: None

    first = pubmed_abstract.fetch_abstract("33567185")
    assert first == sample
    assert calls["n"] == 1

    second = pubmed_abstract.fetch_abstract("33567185")
    assert second == sample
    assert calls["n"] == 1, f"expected 1 API call after cache hit, got {calls['n']}"


def test_pubmed_abstract_short_is_error_cached():
    _isolate_cache()
    _reload_modules(["_http", "_cache", "pubmed_abstract"])
    import pubmed_abstract
    import _http as http_mod

    calls = {"n": 0}
    http_mod.fetch_with_retry = pubmed_abstract.fetch_with_retry = (
        lambda url, **kw: (calls.__setitem__("n", calls["n"] + 1) or (200, b"tiny", {}))
    )
    pubmed_abstract.ncbi_throttle = lambda: None

    raw = pubmed_abstract.fetch_abstract("99999")
    assert raw == "tiny"
    # Second call should raise CachedEmptyAbstractError without bumping calls.
    try:
        pubmed_abstract.fetch_abstract("99999")
    except pubmed_abstract.CachedEmptyAbstractError:
        pass
    else:
        raise AssertionError("expected CachedEmptyAbstractError on 2nd call")
    assert calls["n"] == 1, f"should not refetch empty abstract, got {calls['n']}"


def test_pubmed_no_cache_flag_bypasses():
    _isolate_cache()
    _reload_modules(["_http", "_cache", "pubmed_abstract"])
    import pubmed_abstract
    import _http as http_mod

    calls = {"n": 0}
    sample = "B" * 500
    http_mod.fetch_with_retry = pubmed_abstract.fetch_with_retry = (
        lambda url, **kw: (calls.__setitem__("n", calls["n"] + 1) or (200, sample.encode(), {}))
    )
    pubmed_abstract.ncbi_throttle = lambda: None

    pubmed_abstract.fetch_abstract("111", use_cache=False)
    pubmed_abstract.fetch_abstract("111", use_cache=False)
    assert calls["n"] == 2, f"--no-cache should refetch; got calls={calls['n']}"


def test_pmc_fulltext_cache_hit():
    _isolate_cache()
    _reload_modules(["_http", "_cache", "pmc_fulltext"])
    import pmc_fulltext
    import _http as http_mod

    calls = {"n": 0}
    # Build minimal HTML with <title> tag and plenty of body text.
    title = "Study X"
    body_text = "Cohort results " * 1000  # ensures len(text) >= MIN_CONTENT_CHARS
    html_body = f"<html><head><title>{title}</title></head><body><p>{body_text}</p></body></html>"

    def fake_fetch(url, **kwargs):
        calls["n"] += 1
        return 200, html_body.encode("utf-8"), {}

    http_mod.fetch_with_retry = fake_fetch
    pmc_fulltext.fetch_with_retry = fake_fetch

    t1, txt1 = pmc_fulltext.fetch_fulltext("PMC12345")
    assert t1 == title
    assert len(txt1) >= pmc_fulltext.MIN_CONTENT_CHARS
    assert calls["n"] == 1

    t2, txt2 = pmc_fulltext.fetch_fulltext("PMC12345")
    assert (t2, txt2) == (t1, txt1)
    assert calls["n"] == 1, f"expected cache hit on 2nd call, got {calls['n']}"


def test_pmc_fulltext_captcha_error_cached():
    _isolate_cache()
    _reload_modules(["_http", "_cache", "pmc_fulltext"])
    import pmc_fulltext
    import _http as http_mod

    calls = {"n": 0}
    # Short HTML → triggers captcha/redirect path.
    http_mod.fetch_with_retry = pmc_fulltext.fetch_with_retry = (
        lambda url, **kw: (calls.__setitem__("n", calls["n"] + 1) or (200, b"<html><body>short</body></html>", {}))
    )

    # 1st call: succeeds with short text + writes error cache.
    _title, text = pmc_fulltext.fetch_fulltext("PMC99999")
    assert len(text) < pmc_fulltext.MIN_CONTENT_CHARS
    assert calls["n"] == 1

    # 2nd call: should short-circuit with CachedCaptchaError.
    try:
        pmc_fulltext.fetch_fulltext("PMC99999")
    except pmc_fulltext.CachedCaptchaError:
        pass
    else:
        raise AssertionError("expected CachedCaptchaError on 2nd call")
    assert calls["n"] == 1


def test_pmid_to_pmc_batch_filters_cached():
    _isolate_cache()
    _reload_modules(["_http", "_cache", "pmid_to_pmc"])
    import pmid_to_pmc
    import _http as http_mod

    # Seed the cache for PMID 111 → PMC1.
    from _cache import cache_put
    cache_put("pmc_link", "111", {"pmcid": "PMC1"})

    fetched_ids: list[str] = []

    def fake_fetch(url, **kwargs):
        # The URL contains ids= followed by comma-separated IDs.
        import re as _re
        m = _re.search(r"[?&]id=([^&]+)", url)
        ids = m.group(1).split(",") if m else []
        fetched_ids.extend(ids)
        body = ""
        for pid in ids:
            body += (
                f"<LinkSet><IdList><Id>{pid}</Id></IdList>"
                f"<LinkSetDb><LinkName>pubmed_pmc</LinkName>"
                f"<Link><Id>999{pid}</Id></Link></LinkSetDb></LinkSet>"
            )
        return 200, body.encode("utf-8"), {}

    http_mod.fetch_with_retry = pmid_to_pmc.fetch_with_retry = fake_fetch
    pmid_to_pmc.ncbi_throttle = lambda: None

    result = pmid_to_pmc._resolve_batch(["111", "222", "333"])

    # Only the cache-miss ids should have been fetched from elink.
    assert set(fetched_ids) == {"222", "333"}, f"expected only cache-miss ids, got {fetched_ids}"
    assert result["111"] == "PMC1"  # from cache
    assert result["222"] == "PMC999222"
    assert result["333"] == "PMC999333"


def test_open_access_pdf_cache_hit():
    _isolate_cache()
    _reload_modules(["_http", "_cache", "open_access_pdf"])
    import open_access_pdf
    import _http as http_mod

    pdf_bytes = b"%PDF-1.7\n" + b"x" * 2048
    calls = {"n": 0}

    def fake_fetch(url, **kwargs):
        calls["n"] += 1
        return 200, pdf_bytes, {}

    http_mod.fetch_with_retry = open_access_pdf.fetch_with_retry = fake_fetch

    tmp = Path(tempfile.mkdtemp(prefix="drsci_pdftest_"))
    out1 = tmp / "a.pdf"
    out2 = tmp / "b.pdf"
    url = "https://example.com/paper.pdf"

    open_access_pdf.fetch(url, str(out1))
    open_access_pdf.fetch(url, str(out2))

    assert out1.read_bytes() == pdf_bytes
    assert out2.read_bytes() == pdf_bytes
    assert calls["n"] == 1, f"2nd fetch should hit cache; got {calls['n']}"


def test_open_access_pdf_no_cache_bypasses():
    _isolate_cache()
    _reload_modules(["_http", "_cache", "open_access_pdf"])
    import open_access_pdf
    import _http as http_mod

    pdf_bytes = b"%PDF-1.7\nbypass"
    calls = {"n": 0}
    http_mod.fetch_with_retry = open_access_pdf.fetch_with_retry = (
        lambda url, **kw: (calls.__setitem__("n", calls["n"] + 1) or (200, pdf_bytes, {}))
    )

    tmp = Path(tempfile.mkdtemp(prefix="drsci_pdftest_nocache_"))
    out = tmp / "x.pdf"
    url = "https://example.com/paper.pdf"
    open_access_pdf.fetch(url, str(out), use_cache=False)
    open_access_pdf.fetch(url, str(out), use_cache=False)
    assert calls["n"] == 2


def run_all():
    tests = [
        test_pubmed_abstract_cache_hit,
        test_pubmed_abstract_short_is_error_cached,
        test_pubmed_no_cache_flag_bypasses,
        test_pmc_fulltext_cache_hit,
        test_pmc_fulltext_captcha_error_cached,
        test_pmid_to_pmc_batch_filters_cached,
        test_open_access_pdf_cache_hit,
        test_open_access_pdf_no_cache_bypasses,
    ]
    failures = 0
    for t in tests:
        try:
            t()
            print(f"  ok   {t.__name__}")
        except Exception as e:
            failures += 1
            import traceback
            print(f"  FAIL {t.__name__}: {e}")
            traceback.print_exc()
    print(f"\n{len(tests) - failures}/{len(tests)} passed")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(run_all())
