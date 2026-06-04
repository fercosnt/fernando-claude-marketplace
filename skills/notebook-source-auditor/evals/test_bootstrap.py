#!/usr/bin/env python3
"""F10 tests — bootstrap an empty manifest from current NBM + pesquisas.

Scenarios:
    - bootstrap_notebook: creates manifest entries for every current source
    - bootstrap_notebook: dry-run does not mutate the manifest
    - bootstrap_notebook: skips canonical_keys that already exist in manifest
    - bootstrap_notebook: collapses duplicate canonical_keys in current NBM
                          (first-seen wins; dedupe bucket catches the rest)
    - bootstrap_notebook: flags low-confidence derivations (title-only sources)
    - bootstrap_notebook: marks every created entry with
                          ingest_method=bootstrap_unknown
                          (disables the retryable bucket — we don't know
                          the original ingest method)
    - bootstrap_notebook: empty current_sources → no-op summary
    - auditor.run --bootstrap exit 0 (replaces the old exit 3 flow)

Run: python3 evals/test_bootstrap.py
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

_HERE = Path(__file__).resolve().parent
_SKILL = _HERE.parent
sys.path.insert(0, str(_SKILL / "scripts"))
sys.path.insert(0, str(Path.home() / ".claude/skills/deep-research/scripts"))

import bootstrap  # noqa: E402
import notebook_manifest as manifest  # noqa: E402


def _make_empty_manifest(tmp: Path) -> Path:
    m = tmp / "_notebook-manifest.json"
    m.write_text('{"version": 1, "notebooks": {}}', encoding="utf-8")
    return m


def test_f10_creates_entries_for_every_current_source():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        m = _make_empty_manifest(tmp)
        (tmp / "hashimoto-farmacologia").mkdir()
        current = [
            {"id": "nbm-1", "title": "Paper A", "url": "https://pubmed.ncbi.nlm.nih.gov/12345/"},
            {"id": "nbm-2", "title": "Paper B", "url": "https://doi.org/10.1000/abc"},
        ]
        summary = bootstrap.bootstrap_notebook(
            manifest_path=m,
            notebook_id="nb-abcdefgh",
            notebook_title="Hashimoto",
            current_sources=current,
            pesquisas_paths=[tmp / "hashimoto-farmacologia"],
            pesquisas_root=tmp,
            pesquisa_slugs=["hashimoto-farmacologia"],
            dry_run=False,
        )
        assert summary["created"] == 2, summary
        data = json.loads(m.read_text(encoding="utf-8"))
        entries = data["notebooks"]["nb-abcdefgh"]["sources"]
        assert len(entries) == 2
        for e in entries:
            assert e["ingest_method"] == "bootstrap_unknown"
            assert e["status"] == "ok"


def test_f10_dry_run_does_not_mutate_manifest():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        m = _make_empty_manifest(tmp)
        (tmp / "hashimoto-farmacologia").mkdir()
        original_text = m.read_text(encoding="utf-8")
        summary = bootstrap.bootstrap_notebook(
            manifest_path=m,
            notebook_id="nb-abcdefgh",
            notebook_title="Hashimoto",
            current_sources=[
                {"id": "nbm-1", "title": "Paper A", "url": "https://pubmed.ncbi.nlm.nih.gov/12345/"},
            ],
            pesquisas_paths=[tmp / "hashimoto-farmacologia"],
            pesquisas_root=tmp,
            pesquisa_slugs=["hashimoto-farmacologia"],
            dry_run=True,
        )
        assert summary["created"] == 1
        # File content must be byte-identical to before.
        assert m.read_text(encoding="utf-8") == original_text


def test_f10_skips_canonical_keys_already_present():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "hashimoto-farmacologia").mkdir()
        m = _make_empty_manifest(tmp)
        # Seed the manifest with one source already known via record_source.
        manifest.record_source(
            manifest_path=m,
            notebook_id="nb-abcdefgh",
            pesquisa_slug="hashimoto-farmacologia",
            pesquisas_root=tmp,
            canonical_key="pmid:12345",
            title="Paper A",
            source_type="pubmed",
            origin_pesquisa="hashimoto-farmacologia",
            status="ok",
            ingest_method="url_direct",
        )
        summary = bootstrap.bootstrap_notebook(
            manifest_path=m,
            notebook_id="nb-abcdefgh",
            notebook_title="Hashimoto",
            current_sources=[
                {"id": "nbm-1", "title": "Paper A", "url": "https://pubmed.ncbi.nlm.nih.gov/12345/"},
                {"id": "nbm-2", "title": "Paper B", "url": "https://doi.org/10.1000/abc"},
            ],
            pesquisas_paths=[tmp / "hashimoto-farmacologia"],
            pesquisas_root=tmp,
            pesquisa_slugs=["hashimoto-farmacologia"],
            dry_run=False,
        )
        assert summary["created"] == 1, summary
        assert summary["skipped_existing"] == 1, summary
        # The pre-existing entry still has ingest_method=url_direct.
        entry = manifest.lookup_source(m, "nb-abcdefgh", "pmid:12345")
        assert entry is not None
        assert entry["ingest_method"] == "url_direct"


def test_f10_collapses_duplicates_in_current_nbm():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "hashimoto-farmacologia").mkdir()
        m = _make_empty_manifest(tmp)
        # Two sources resolving to the same canonical_key. Bootstrap should
        # register only one — the dedup bucket catches the duplicate.
        current = [
            {"id": "nbm-1", "title": "Paper A", "url": "https://pubmed.ncbi.nlm.nih.gov/12345/"},
            {"id": "nbm-2", "title": "Paper A (copy)", "url": "https://pubmed.ncbi.nlm.nih.gov/12345/"},
        ]
        summary = bootstrap.bootstrap_notebook(
            manifest_path=m,
            notebook_id="nb-abcdefgh",
            notebook_title="Hashimoto",
            current_sources=current,
            pesquisas_paths=[tmp / "hashimoto-farmacologia"],
            pesquisas_root=tmp,
            pesquisa_slugs=["hashimoto-farmacologia"],
            dry_run=False,
        )
        assert summary["created"] == 1, summary
        data = json.loads(m.read_text(encoding="utf-8"))
        entries = data["notebooks"]["nb-abcdefgh"]["sources"]
        assert len(entries) == 1
        # notebooklm_source_id records the FIRST source seen — the dedup
        # bucket on the next run decides the final keeper.
        assert entries[0]["notebooklm_source_id"] == "nbm-1"


def test_f10_flags_low_confidence_sources():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "hashimoto-farmacologia").mkdir()
        m = _make_empty_manifest(tmp)
        # A source with no URL → derive_canonical_key falls back to title
        # with confidence=low.
        summary = bootstrap.bootstrap_notebook(
            manifest_path=m,
            notebook_id="nb-abcdefgh",
            notebook_title="Hashimoto",
            current_sources=[
                {"id": "nbm-1", "title": "Anonymous paper", "url": ""},
            ],
            pesquisas_paths=[tmp / "hashimoto-farmacologia"],
            pesquisas_root=tmp,
            pesquisa_slugs=["hashimoto-farmacologia"],
            dry_run=False,
        )
        assert summary["created"] == 1
        assert summary["low_confidence"] == 1
        entry = json.loads(m.read_text(encoding="utf-8"))["notebooks"]["nb-abcdefgh"]["sources"][0]
        assert entry["ingest_metadata"]["bootstrap_confidence"] == "low"


def test_f10_empty_current_sources_is_noop():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "p").mkdir()
        m = _make_empty_manifest(tmp)
        summary = bootstrap.bootstrap_notebook(
            manifest_path=m,
            notebook_id="nb-abcdefgh",
            notebook_title="Empty",
            current_sources=[],
            pesquisas_paths=[tmp / "p"],
            pesquisas_root=tmp,
            pesquisa_slugs=["p"],
            dry_run=False,
        )
        assert summary == {
            "created": 0,
            "skipped_existing": 0,
            "low_confidence": 0,
            "source_details": [],
        }


def test_f10_marks_ambiguous_pesquisa_when_multi_slug():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "slug-a").mkdir()
        (tmp / "slug-b").mkdir()
        m = _make_empty_manifest(tmp)
        summary = bootstrap.bootstrap_notebook(
            manifest_path=m,
            notebook_id="nb-abcdefgh",
            notebook_title="X",
            current_sources=[
                {"id": "nbm-1", "title": "Paper A", "url": "https://pubmed.ncbi.nlm.nih.gov/1/"},
            ],
            pesquisas_paths=[tmp / "slug-a", tmp / "slug-b"],
            pesquisas_root=tmp,
            pesquisa_slugs=["slug-a", "slug-b"],
            dry_run=True,
        )
        detail = summary["source_details"][0]
        assert detail["ambiguous_pesquisa"] is True
        # Default slug = first one; user can refine afterwards.
        assert detail["origin_pesquisa"] == "slug-a"


def test_f10_auditor_bootstrap_flag_returns_0_and_populates():
    """End-to-end: run() with --bootstrap must exit 0 (not 3) and write
    manifest entries for the current NBM sources."""
    import auditor
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "hashimoto-farmacologia").mkdir()
        # Deliberately leave the manifest absent — auditor must create it.
        fake_nbm = {
            "title": "Hashimoto",
            "sources": [
                {"id": "nbm-1", "title": "Paper A", "url": "https://pubmed.ncbi.nlm.nih.gov/12345/"},
                {"id": "nbm-2", "title": "Paper B", "url": "https://doi.org/10.1000/abc"},
            ],
        }
        with patch("auditor.list_notebook_sources", return_value=fake_nbm):
            rc = auditor.run([
                "--notebook", "nb-abcdefgh",
                "--pesquisas", str(tmp / "hashimoto-farmacologia"),
                "--bootstrap",
                "--apply",
            ])
        assert rc == 0
        m = tmp / "_notebook-manifest.json"
        assert m.exists()
        data = json.loads(m.read_text(encoding="utf-8"))
        sources = data["notebooks"]["nb-abcdefgh"]["sources"]
        assert len(sources) == 2
        for s in sources:
            assert s["ingest_method"] == "bootstrap_unknown"


TESTS = [
    test_f10_creates_entries_for_every_current_source,
    test_f10_dry_run_does_not_mutate_manifest,
    test_f10_skips_canonical_keys_already_present,
    test_f10_collapses_duplicates_in_current_nbm,
    test_f10_flags_low_confidence_sources,
    test_f10_empty_current_sources_is_noop,
    test_f10_marks_ambiguous_pesquisa_when_multi_slug,
    test_f10_auditor_bootstrap_flag_returns_0_and_populates,
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
