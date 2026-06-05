#!/usr/bin/env python3
"""Regression tests for the Firecrawl fetch-fallback tier (2026-06-05).

Feature: `--firecrawl-fallback` lets cloudflare_known URLs try `firecrawl scrape`
(JS render + Cloudflare bypass) before falling into the NotebookLM manual bucket.

These tests are hermetic — they mock `subprocess.run`, so they never touch the
network or spend Firecrawl credits. They cover:
    - _firecrawl_scrape gate (no key), CLI-missing, non-zero exit, thin output,
      still-blocked output, and the happy path.
    - _worker_generic backward-compat (no flag → manual), gated flag (flag but no
      key → manual), happy path (flag + scrape → file upload), and that the flag
      does not affect non-cloudflare generic URLs.

Run: python3 evals/test_firecrawl_fallback.py
"""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO / "scripts" / "sci_fetch"))
sys.path.insert(0, str(REPO / "scripts"))

import upload_to_nblm as m  # noqa: E402

KEY = "FIRECRAWL_API_KEY"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
class _FakeProc:
    def __init__(self, returncode: int = 0):
        self.returncode = returncode
        self.stdout = ""
        self.stderr = ""


class _Sentinel:
    """Raises if subprocess.run is called — proves the gate short-circuited."""
    def __init__(self):
        self.called = False

    def __call__(self, *a, **k):
        self.called = True
        raise AssertionError("subprocess.run should not have been called")


def _fake_run(*, write_text: str | None = None, returncode: int = 0, raise_exc=None):
    def _run(cmd, capture_output=True, text=True, timeout=None):
        if raise_exc is not None:
            raise raise_exc
        # cmd == ["firecrawl", "scrape", url, "--only-main-content", "-o", outpath]
        out = Path(cmd[cmd.index("-o") + 1])
        if write_text is not None and returncode == 0:
            out.write_text(write_text, encoding="utf-8")
        return _FakeProc(returncode)
    return _run


class _patch_run:
    """Context manager: swap m.subprocess.run, restore on exit."""
    def __init__(self, fn):
        self.fn = fn

    def __enter__(self):
        self._orig = m.subprocess.run
        m.subprocess.run = self.fn
        return self.fn

    def __exit__(self, *exc):
        m.subprocess.run = self._orig


class _env_key:
    """Context manager: set/clear FIRECRAWL_API_KEY, restore on exit."""
    def __init__(self, value: str | None):
        self.value = value

    def __enter__(self):
        self._orig = os.environ.get(KEY)
        if self.value is None:
            os.environ.pop(KEY, None)
        else:
            os.environ[KEY] = self.value

    def __exit__(self, *exc):
        if self._orig is None:
            os.environ.pop(KEY, None)
        else:
            os.environ[KEY] = self._orig


def _wd() -> Path:
    return Path(tempfile.mkdtemp(prefix="dr_fcfb_"))


def _cf_item(url="https://www.mdpi.com/journal/cancers"):
    cls = m.classify(url)
    assert cls["type"] == "cloudflare_known", f"fixture must be cloudflare_known, got {cls['type']}"
    return {"url": url, "cls": cls, "url_norm": m.manifest.normalize_url(url)}


_REAL_MD = "# Cancers\n\n" + ("Real article body with plenty of substance. " * 60)


# ---------------------------------------------------------------------------
# _firecrawl_scrape
# ---------------------------------------------------------------------------
def test_scrape_gate_no_key_returns_none_without_calling_cli():
    sentinel = _Sentinel()
    with _env_key(None), _patch_run(sentinel):
        assert m._firecrawl_scrape("https://www.mdpi.com/x", _wd()) is None
    assert sentinel.called is False


def test_scrape_cli_missing_returns_none():
    with _env_key("fc-test"), _patch_run(_fake_run(raise_exc=FileNotFoundError())):
        assert m._firecrawl_scrape("https://www.mdpi.com/x", _wd()) is None


def test_scrape_timeout_returns_none():
    import subprocess as _sp
    exc = _sp.TimeoutExpired(cmd="firecrawl", timeout=120)
    with _env_key("fc-test"), _patch_run(_fake_run(raise_exc=exc)):
        assert m._firecrawl_scrape("https://www.mdpi.com/x", _wd()) is None


def test_scrape_nonzero_exit_returns_none():
    with _env_key("fc-test"), _patch_run(_fake_run(write_text=None, returncode=1)):
        assert m._firecrawl_scrape("https://www.mdpi.com/x", _wd()) is None


def test_scrape_thin_output_rejected_and_file_removed():
    wd = _wd()
    with _env_key("fc-test"), _patch_run(_fake_run(write_text="tiny", returncode=0)):
        assert m._firecrawl_scrape("https://www.mdpi.com/x", wd) is None
    # The thin file must be cleaned up so it can't be mistaken for a real source.
    assert list(wd.glob("firecrawl-*.md")) == []


def test_scrape_still_blocked_output_rejected():
    blocked = "Just a moment...\nChecking your browser before accessing." + ("x" * 800)
    with _env_key("fc-test"), _patch_run(_fake_run(write_text=blocked, returncode=0)):
        assert m._firecrawl_scrape("https://www.mdpi.com/x", _wd()) is None


def test_scrape_happy_path_returns_markdown_file():
    wd = _wd()
    with _env_key("fc-test"), _patch_run(_fake_run(write_text=_REAL_MD, returncode=0)):
        fp = m._firecrawl_scrape("https://www.mdpi.com/journal/cancers", wd)
    assert fp is not None and fp.exists()
    assert fp.read_text(encoding="utf-8").startswith("# Cancers")


# ---------------------------------------------------------------------------
# _worker_generic
# ---------------------------------------------------------------------------
def test_worker_no_flag_keeps_manual_bucket():
    """Backward-compat: without the flag, cloudflare_known still goes manual."""
    sentinel = _Sentinel()
    with _patch_run(sentinel):  # must not even attempt a scrape
        t = m._worker_generic(_cf_item(), _wd(), enable_firecrawl_fallback=False)
    assert t.file_path is None
    assert t.manual_required_reason and "Cloudflare" in t.manual_required_reason
    assert sentinel.called is False


def test_worker_flag_but_no_key_falls_back_to_manual():
    with _env_key(None), _patch_run(_fake_run(write_text=_REAL_MD, returncode=0)):
        t = m._worker_generic(_cf_item(), _wd(), enable_firecrawl_fallback=True)
    # Gate (no key) inside _firecrawl_scrape → None → manual bucket.
    assert t.file_path is None
    assert t.manual_required_reason is not None


def test_worker_flag_with_scrape_produces_upload_task():
    wd = _wd()
    with _env_key("fc-test"), _patch_run(_fake_run(write_text=_REAL_MD, returncode=0)):
        t = m._worker_generic(_cf_item(), wd, enable_firecrawl_fallback=True)
    assert t.manual_required_reason is None, "should not be manual when scrape succeeds"
    assert t.file_path is not None and t.file_path.exists()
    assert t.ingest_method == "pdf_upload"
    assert t.metadata_meta.get("fetch_method") == "firecrawl_scrape"


def test_worker_flag_does_not_touch_generic_web():
    """A normal generic_web URL is uploaded url-direct regardless of the flag."""
    url = "https://example.com/some-article"
    cls = m.classify(url)
    assert cls["type"] in ("generic_web", "blog_or_news", "gov_or_guideline")
    item = {"url": url, "cls": cls, "url_norm": m.manifest.normalize_url(url)}
    sentinel = _Sentinel()
    with _patch_run(sentinel):  # firecrawl must not be invoked for non-cloudflare
        t = m._worker_generic(item, _wd(), enable_firecrawl_fallback=True)
    assert t.file_path is None
    assert t.manual_required_reason is None
    assert t.ingest_method == "url_direct"
    assert sentinel.called is False


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
TESTS = [
    test_scrape_gate_no_key_returns_none_without_calling_cli,
    test_scrape_cli_missing_returns_none,
    test_scrape_timeout_returns_none,
    test_scrape_nonzero_exit_returns_none,
    test_scrape_thin_output_rejected_and_file_removed,
    test_scrape_still_blocked_output_rejected,
    test_scrape_happy_path_returns_markdown_file,
    test_worker_no_flag_keeps_manual_bucket,
    test_worker_flag_but_no_key_falls_back_to_manual,
    test_worker_flag_with_scrape_produces_upload_task,
    test_worker_flag_does_not_touch_generic_web,
]


def main() -> int:
    passed = failed = 0
    for t in TESTS:
        try:
            t()
        except AssertionError as e:
            failed += 1
            print(f"[FAIL] {t.__name__}: {e}")
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"[ERR ] {t.__name__}: {type(e).__name__}: {e}")
        else:
            passed += 1
            print(f"[PASS] {t.__name__}")
    print(f"\n{passed}/{passed + failed} tests passed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
