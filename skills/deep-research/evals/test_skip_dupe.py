#!/usr/bin/env python3
"""F8 skip-dupe tests for upload_to_nblm.py.

Scenario driving the feature (Phase 5, 2026-04-23):
    - Notebook already has WEB_PAGE source for paper X (canonical=pmid:...)
    - sci_fetch runs again with the same URL list → tries to add MARKDOWN of X
    - Without skip-dupe: second source gets added → dedupe↔readd loop
    - With skip-dupe: task is skipped, no manifest write, no CLI call

Run: python3 evals/test_skip_dupe.py
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import threading
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO / "scripts" / "sci_fetch"))
sys.path.insert(0, str(REPO / "scripts"))


def _isolate_cache() -> Path:
    tmp = Path(tempfile.mkdtemp(prefix="drsci_skipdupe_"))
    os.environ["DR_SCI_CACHE_ROOT"] = str(tmp)
    os.environ.pop("DR_SCI_NO_CACHE", None)
    os.environ["UNPAYWALL_EMAIL"] = "test@example.com"
    return tmp


def _reload():
    import importlib
    for n in ("_cache", "_token_bucket", "_http", "classify_url",
              "pubmed_abstract", "pmc_fulltext", "pmid_to_pmc",
              "unpaywall_resolver", "open_access_pdf", "upload_to_nblm"):
        if n in sys.modules:
            del sys.modules[n]
    for n in ("_cache", "_token_bucket", "_http", "classify_url",
              "pubmed_abstract", "pmc_fulltext", "pmid_to_pmc",
              "unpaywall_resolver", "open_access_pdf", "upload_to_nblm"):
        importlib.import_module(n)


def _stub_upload_pipeline(already_present_canonicals: list[str]):
    """Stub NotebookLM + fetchers so tasks run end-to-end in memory.

    `already_present_canonicals` seeds the fake `_nblm_list_sources` with
    sources that would derive to those canonical_keys, so F8 skip-dupe
    can see them.
    """
    import upload_to_nblm

    # Fetchers return content long enough to trigger the file-write branch
    # in `_handle_pubmed` (>= 100 chars). Ensures the task carries file_path,
    # exercising the file upload path that F8 must short-circuit.
    upload_to_nblm.pubmed_abstract.fetch_abstract = lambda pmid, *, use_cache=True: "Abstract " * 50
    upload_to_nblm.pubmed_abstract.format_output = lambda pmid, raw: f"pmid:{pmid}\n\n{raw}"
    upload_to_nblm.pmc_fulltext.fetch_fulltext = lambda pmcid, *, use_cache=True: ("title", "body " * 400)
    upload_to_nblm.pmid_to_pmc._resolve_batch = lambda pmids, *, use_cache=True: {}
    upload_to_nblm.paper_scorer.score_paper = lambda **kw: None
    upload_to_nblm.biorxiv_fallback.find_preprint = lambda doi, **kw: None

    # Fake NBM state: each canonical in `already_present_canonicals` maps
    # to a source dict that, when passed through `_derive_canonical_for_source`,
    # yields that canonical. For pmid:N we emit a pubmed URL.
    fake_sources = []
    for ck in already_present_canonicals:
        if ck.startswith("pmid:"):
            pmid = ck.split(":", 1)[1]
            fake_sources.append({
                "id": f"src_{pmid}",
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                "title": f"Paper {pmid} (WEB_PAGE)",
            })
    upload_to_nblm._nblm_list_sources = lambda notebook_id: fake_sources

    # Record CLI attempts so we can assert skip-dupe *actually* skipped.
    cli_calls = {"add_file": [], "add_url": []}
    lock = threading.Lock()

    def fake_add_file(file_path, notebook_id):
        with lock:
            cli_calls["add_file"].append(str(file_path))
        return {"ok": True, "source_id": f"src_{Path(file_path).stem}", "error": None}

    def fake_add_url(url, notebook_id):
        with lock:
            cli_calls["add_url"].append(url)
        return {"ok": True, "source_id": f"url_{hash(url) & 0xffff}", "error": None}

    upload_to_nblm._nblm_add_file = fake_add_file
    upload_to_nblm._nblm_add_url = fake_add_url

    # Record manifest writes so skip-dupe's "no manifest write" guarantee is testable.
    manifest_writes = []
    def fake_record_source(**kw):
        manifest_writes.append(kw)
    upload_to_nblm.manifest.record_source = fake_record_source

    return {"cli_calls": cli_calls, "manifest_writes": manifest_writes}


def _pmid_url(n: int) -> str:
    return f"https://pubmed.ncbi.nlm.nih.gov/{n}/"


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
def test_skip_dupe_off_uploads_everything():
    """Baseline: without --skip-dupe, all tasks upload even if canonical exists.
    Proves the stubbing harness is live — nothing leaks from per-test state."""
    _isolate_cache()
    _reload()
    probe = _stub_upload_pipeline(already_present_canonicals=["pmid:111", "pmid:222"])
    import upload_to_nblm

    work_dir = Path(tempfile.mkdtemp(prefix="drsci_skipdupe_off_"))
    summary = upload_to_nblm.process(
        urls=[_pmid_url(111), _pmid_url(222), _pmid_url(333)],
        notebook_id="nb_test",
        pesquisa_slug="p",
        pesquisas_root=work_dir.parent,
        work_dir=work_dir,
        skip_upload=False,
        serial=True,
        skip_dupe=False,
    )
    total_upload_calls = len(probe["cli_calls"]["add_file"]) + len(probe["cli_calls"]["add_url"])
    assert total_upload_calls == 3, f"skip_dupe=False should upload all 3, got {total_upload_calls}"
    assert summary.get("skipped_duplicate", 0) == 0


def test_skip_dupe_on_skips_present_canonicals():
    """Core F8: when skip_dupe=True, tasks whose canonical is already in the
    NBM get skipped → no CLI call, no manifest write, tallied in skipped_duplicate."""
    _isolate_cache()
    _reload()
    probe = _stub_upload_pipeline(already_present_canonicals=["pmid:111", "pmid:222"])
    import upload_to_nblm

    work_dir = Path(tempfile.mkdtemp(prefix="drsci_skipdupe_on_"))
    summary = upload_to_nblm.process(
        urls=[_pmid_url(111), _pmid_url(222), _pmid_url(333)],
        notebook_id="nb_test",
        pesquisa_slug="p",
        pesquisas_root=work_dir.parent,
        work_dir=work_dir,
        skip_upload=False,
        serial=True,
        skip_dupe=True,
    )
    total_upload_calls = len(probe["cli_calls"]["add_file"]) + len(probe["cli_calls"]["add_url"])
    assert total_upload_calls == 1, (
        f"skip_dupe=True should upload only pmid:333, got {total_upload_calls} calls "
        f"(files={probe['cli_calls']['add_file']}, urls={probe['cli_calls']['add_url']})"
    )
    assert summary["skipped_duplicate"] == 2, summary
    # Skipped tasks must not write to the manifest.
    skipped_keys = {"pmid:111", "pmid:222"}
    written_keys = {w.get("canonical_key") for w in probe["manifest_writes"]}
    assert skipped_keys.isdisjoint(written_keys), (
        f"skip-dupe wrote manifest entries for {skipped_keys & written_keys}"
    )


def test_skip_dupe_idempotent_second_run():
    """Regression for the Phase 5 loop: run twice, second run must skip all
    (canonical set from NBM covers everything), → 0 new uploads + 0 new manifest
    writes. Without F8, the second run would add 3 new MARKDOWN sources."""
    _isolate_cache()
    _reload()
    # After the first run, all 3 canonicals are present in the NBM.
    probe = _stub_upload_pipeline(already_present_canonicals=["pmid:111", "pmid:222", "pmid:333"])
    import upload_to_nblm

    work_dir = Path(tempfile.mkdtemp(prefix="drsci_skipdupe_idem_"))
    summary = upload_to_nblm.process(
        urls=[_pmid_url(111), _pmid_url(222), _pmid_url(333)],
        notebook_id="nb_test",
        pesquisa_slug="p",
        pesquisas_root=work_dir.parent,
        work_dir=work_dir,
        skip_upload=False,
        serial=True,
        skip_dupe=True,
    )
    total_upload_calls = len(probe["cli_calls"]["add_file"]) + len(probe["cli_calls"]["add_url"])
    assert total_upload_calls == 0, f"re-run should add zero new sources, got {total_upload_calls}"
    assert summary["skipped_duplicate"] == 3
    assert summary["auto_uploaded"] == 0
    assert len(probe["manifest_writes"]) == 0, probe["manifest_writes"]


def test_compute_present_canonical_keys_derives_pmid():
    """_derive_canonical_for_source + compute_present_canonical_keys are the
    keystone of F8. Assert the derivation produces the same canonical format
    used by tasks (pmid:N, doi:x, url:normalized)."""
    _isolate_cache()
    _reload()
    import upload_to_nblm

    upload_to_nblm._nblm_list_sources = lambda nb: [
        {"id": "a", "url": "https://pubmed.ncbi.nlm.nih.gov/12345/", "title": "X"},
        {"id": "b", "url": "https://doi.org/10.1234/abc", "title": "Y"},
        {"id": "c", "url": "https://example.org/page", "title": "Z"},
        {"id": "d", "url": "", "title": "titlefallback"},
    ]
    got = upload_to_nblm.compute_present_canonical_keys("nb_x")
    assert "pmid:12345" in got, got
    assert "doi:10.1234/abc" in got, got
    # Generic URL falls back to url:normalized; exact form depends on normalize_url.
    assert any(k.startswith("url:") for k in got), got
    # Empty URL → None → not in set.
    assert len(got) == 3, got


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
TESTS = [
    test_skip_dupe_off_uploads_everything,
    test_skip_dupe_on_skips_present_canonicals,
    test_skip_dupe_idempotent_second_run,
    test_compute_present_canonical_keys_derives_pmid,
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
