#!/usr/bin/env python3
"""Unit tests for Unpaywall-first DOI handling in upload_to_nblm._handle_doi.

Uses monkey-patching to avoid hitting the real Unpaywall / publisher APIs.
Run: python3 evals/test_doi_unpaywall.py
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
sys.path.insert(0, str(REPO / "scripts"))


def _isolate_cache() -> Path:
    tmp = Path(tempfile.mkdtemp(prefix="drsci_doitest_"))
    os.environ["DR_SCI_CACHE_ROOT"] = str(tmp)
    os.environ.pop("DR_SCI_NO_CACHE", None)
    os.environ["UNPAYWALL_EMAIL"] = "test@example.com"
    return tmp


def _patch(upload_to_nblm, *, unpaywall_return, pdf_fetch_raises=None, biorxiv_return=None):
    """Swap unpaywall_resolver.resolve, open_access_pdf.fetch, and
    biorxiv_fallback.find_preprint on the module so tests don't hit network.

    biorxiv_return defaults to None (no preprint found) so the v2 bioRxiv
    fallback in _handle_doi takes the "no preprint" path without a real call.
    """
    def fake_resolve(doi, email, *, use_cache=True):
        if callable(unpaywall_return):
            return unpaywall_return(doi)
        return unpaywall_return

    def fake_fetch(url, out_path, **kwargs):
        if pdf_fetch_raises is not None:
            raise pdf_fetch_raises
        Path(out_path).write_bytes(b"%PDF-1.7\n<fake-pdf-body>")
        return out_path

    def fake_biorxiv(doi, *, use_cache=True, validate_pdf=True):
        if callable(biorxiv_return):
            return biorxiv_return(doi)
        return biorxiv_return

    upload_to_nblm.unpaywall_resolver.resolve = fake_resolve
    upload_to_nblm.open_access_pdf.fetch = fake_fetch
    upload_to_nblm.biorxiv_fallback.find_preprint = fake_biorxiv


def test_oa_doi_returns_pdf():
    _isolate_cache()
    import upload_to_nblm
    _patch(upload_to_nblm, unpaywall_return={
        "doi": "10.1/oa", "is_oa": True,
        "oa_pdf_url": "https://example.com/paper.pdf",
        "oa_landing_url": "https://example.com/paper",
        "host_type": "repository",
    })
    work = Path(tempfile.mkdtemp(prefix="doitest_oa_"))
    cls = {"type": "doi", "metadata": {"doi": "10.1/oa"}}
    path, canonical, meta = upload_to_nblm._handle_doi("https://doi.org/10.1/oa", cls, work)
    assert path is not None, f"expected Path, got {path}"
    assert canonical == "doi:10.1/oa"
    assert meta["unpaywall_host_type"] == "repository"
    assert meta["unpaywall_pdf_url"] == "https://example.com/paper.pdf"
    assert path.exists() and path.read_bytes().startswith(b"%PDF")


def test_not_oa_returns_manual():
    _isolate_cache()
    import upload_to_nblm
    _patch(upload_to_nblm, unpaywall_return={
        "doi": "10.1/closed", "is_oa": False,
        "oa_pdf_url": None, "oa_landing_url": None, "host_type": None,
    })
    work = Path(tempfile.mkdtemp(prefix="doitest_closed_"))
    cls = {"type": "doi", "metadata": {"doi": "10.1/closed"}}
    path, canonical, meta = upload_to_nblm._handle_doi("https://doi.org/10.1/closed", cls, work)
    assert path is None
    assert canonical == "doi:10.1/closed"
    assert "nao-OA" in meta["reason"] or "not-OA" in meta["reason"] or "DOI nao-OA" in meta["reason"]
    assert meta.get("unpaywall_checked") is True


def test_is_oa_true_but_pdf_url_missing():
    _isolate_cache()
    import upload_to_nblm
    _patch(upload_to_nblm, unpaywall_return={
        "doi": "10.1/weird", "is_oa": True,
        "oa_pdf_url": None, "oa_landing_url": "https://example.com/landing", "host_type": "publisher",
    })
    work = Path(tempfile.mkdtemp(prefix="doitest_weird_"))
    cls = {"type": "doi", "metadata": {"doi": "10.1/weird"}}
    path, canonical, meta = upload_to_nblm._handle_doi("https://doi.org/10.1/weird", cls, work)
    assert path is None
    assert "reason" in meta


def test_unpaywall_error_falls_back_to_manual():
    _isolate_cache()
    import upload_to_nblm
    def boom(doi):
        raise RuntimeError("simulated network failure")
    _patch(upload_to_nblm, unpaywall_return=boom)
    work = Path(tempfile.mkdtemp(prefix="doitest_err_"))
    cls = {"type": "doi", "metadata": {"doi": "10.1/err"}}
    path, canonical, meta = upload_to_nblm._handle_doi("https://doi.org/10.1/err", cls, work)
    assert path is None
    assert "Unpaywall error" in meta["reason"]


def test_oa_but_pdf_is_html_returns_manual():
    _isolate_cache()
    import upload_to_nblm
    from open_access_pdf import NotAPDFError
    _patch(
        upload_to_nblm,
        unpaywall_return={
            "doi": "10.1/html", "is_oa": True,
            "oa_pdf_url": "https://example.com/paper", "oa_landing_url": "...", "host_type": "publisher",
        },
        pdf_fetch_raises=NotAPDFError("https://example.com/paper", "/tmp/fallback.html"),
    )
    work = Path(tempfile.mkdtemp(prefix="doitest_html_"))
    cls = {"type": "doi", "metadata": {"doi": "10.1/html"}}
    path, canonical, meta = upload_to_nblm._handle_doi("https://doi.org/10.1/html", cls, work)
    assert path is None
    assert "HTML fallback" in meta["reason"] or "nao retornou PDF" in meta["reason"]


def test_missing_unpaywall_email():
    _isolate_cache()
    os.environ.pop("UNPAYWALL_EMAIL", None)
    try:
        import upload_to_nblm
        _patch(upload_to_nblm, unpaywall_return={"is_oa": True})
        work = Path(tempfile.mkdtemp(prefix="doitest_noenv_"))
        cls = {"type": "doi", "metadata": {"doi": "10.1/env"}}
        path, canonical, meta = upload_to_nblm._handle_doi("https://doi.org/10.1/env", cls, work)
        assert path is None
        assert "UNPAYWALL_EMAIL" in meta["reason"]
    finally:
        os.environ["UNPAYWALL_EMAIL"] = "test@example.com"


def test_biorxiv_fallback_succeeds_when_unpaywall_paywalled():
    """v2 F6/T6.3: when Unpaywall says paywalled but bioRxiv has a preprint,
    we fetch the preprint PDF and surface preprint metadata in the manifest."""
    _isolate_cache()
    import upload_to_nblm
    _patch(
        upload_to_nblm,
        unpaywall_return={
            "doi": "10.1/paywalled", "is_oa": False,
            "oa_pdf_url": None, "oa_landing_url": None, "host_type": None,
        },
        biorxiv_return={
            "preprint_doi": "10.1101/2024.01.01.99999",
            "pdf_url": "https://www.biorxiv.org/content/10.1101/2024.01.01.99999v2.full.pdf",
            "preprint_server": "bioRxiv",
            "version": 2,
            "posted_date": "2024-01-15",
        },
    )
    work = Path(tempfile.mkdtemp(prefix="doitest_biorxiv_"))
    cls = {"type": "doi", "metadata": {"doi": "10.1/paywalled"}}
    path, canonical, meta = upload_to_nblm._handle_doi("https://doi.org/10.1/paywalled", cls, work)
    assert path is not None, f"expected preprint PDF Path, got None (meta={meta})"
    assert meta.get("preprint_fallback") is True
    assert meta.get("preprint_server") == "bioRxiv"
    assert meta.get("preprint_version") == 2
    assert path.exists() and path.read_bytes().startswith(b"%PDF")


def test_biorxiv_disabled_falls_back_to_manual():
    """When enable_biorxiv_fallback=False, paywalled DOI still goes to manual
    even if a preprint exists (preserves opt-out behavior for --skip-biorxiv-fallback)."""
    _isolate_cache()
    import upload_to_nblm
    _patch(
        upload_to_nblm,
        unpaywall_return={
            "doi": "10.1/paywalled2", "is_oa": False,
            "oa_pdf_url": None, "oa_landing_url": None, "host_type": None,
        },
        biorxiv_return={"pdf_url": "https://x/y.pdf", "preprint_server": "bioRxiv", "version": 1,
                        "preprint_doi": "10.1101/x"},
    )
    work = Path(tempfile.mkdtemp(prefix="doitest_biorxiv_off_"))
    cls = {"type": "doi", "metadata": {"doi": "10.1/paywalled2"}}
    path, canonical, meta = upload_to_nblm._handle_doi(
        "https://doi.org/10.1/paywalled2", cls, work,
        enable_biorxiv_fallback=False,
    )
    assert path is None
    assert "DOI nao-OA" in meta["reason"]
    assert "biorxiv_checked" not in meta  # path was disabled


def run_all():
    tests = [
        test_oa_doi_returns_pdf,
        test_not_oa_returns_manual,
        test_is_oa_true_but_pdf_url_missing,
        test_unpaywall_error_falls_back_to_manual,
        test_oa_but_pdf_is_html_returns_manual,
        test_missing_unpaywall_email,
        test_biorxiv_fallback_succeeds_when_unpaywall_paywalled,
        test_biorxiv_disabled_falls_back_to_manual,
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
