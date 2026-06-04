#!/usr/bin/env python3
"""F1b tests — `captcha_page_disguised` bucket + resolver.

Scenarios:
    - diff_engine pulls captcha-titled NBM sources into the new bucket
    - captcha-page sources are removed from `orphans`
    - captcha-page sources are removed from `duplicates` groups; group
      shrinking to <2 disappears entirely
    - `in_manifest` flag reflects whether the canonical_key exists in manifest
    - resolver dry-run: emits plan, no delete/readd
    - resolver apply: deletes each captcha, re-adds URLs via sci_fetch,
      and calls mark_deleted for in-manifest canonical_keys
    - resolver apply with delete failure → any_failure=True
    - noop_count ignores canonical_keys whose only source is captcha-page

Run: python3 evals/test_captcha_page_disguised.py
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_SKILL = _HERE.parent
sys.path.insert(0, str(_SKILL / "scripts"))
sys.path.insert(0, str(Path.home() / ".claude/skills/deep-research/scripts"))

import auditor  # noqa: E402
import notebook_manifest as manifest  # noqa: E402
from diff_engine import compute_diff  # noqa: E402


NOTEBOOK_ID = "nb-f1b"


def _fake_manifest(tmp: Path, sources: list[dict]) -> Path:
    p = tmp / "_notebook-manifest.json"
    data = {
        "version": 1,
        "notebooks": {
            NOTEBOOK_ID: {
                "title": "F1b Fixture",
                "added_at": "2026-03-01T00:00:00+00:00",
                "updated_at": "2026-03-01T00:00:00+00:00",
                "sources": sources,
            }
        },
    }
    p.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return p


def _expected_from_manifest(ms: list[dict], slugs: set[str]) -> dict:
    expected = {}
    for entry in ms:
        if entry.get("status") == "deleted":
            continue
        slug = entry.get("origin_pesquisa")
        if slug not in slugs:
            continue
        ck = entry["canonical_key"]
        expected[ck] = {
            "title": entry.get("title", ""),
            "type": entry.get("type", "article"),
            "origin_pesquisas": [slug],
            "manifest_entry": entry,
            "last_known_status": entry.get("status", "ok"),
        }
    return expected


# ---------------------------------------------------------------------------
# diff_engine coverage
# ---------------------------------------------------------------------------

def test_f1b_captcha_page_lands_in_dedicated_bucket_not_orphans():
    """A captcha-titled NBM source without a manifest entry used to surface
    as orphan. F1b pulls it into captcha_page_disguised instead."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        mpath = _fake_manifest(tmp, [
            {"canonical_key": "pmid:111", "status": "ok", "origin_pesquisa": "p1",
             "ingest_method": "url_direct", "title": "Paper A"},
        ])
        current = [
            {"id": "ok1", "title": "Paper A", "url": "https://pubmed.ncbi.nlm.nih.gov/111/",
             "added_at": "2026-03-01T10:00:00Z"},
            {"id": "cap1", "title": "Checking your browser before accessing",
             "url": "https://www.sciencedirect.com/something", "added_at": "2026-03-10T10:00:00Z"},
        ]
        expected = _expected_from_manifest(
            [{"canonical_key": "pmid:111", "status": "ok", "origin_pesquisa": "p1",
              "ingest_method": "url_direct", "title": "Paper A"}],
            {"p1"},
        )
        diff = compute_diff(
            current_sources=current, expected_sources=expected,
            manifest_path=mpath, notebook_id=NOTEBOOK_ID, max_retry=3,
        )
        assert len(diff["captcha_page_disguised"]) == 1
        cap = diff["captcha_page_disguised"][0]
        assert cap["source_id"] == "cap1"
        assert cap["in_manifest"] is False  # not known to manifest
        # It must NOT show up in orphans anymore.
        orphan_ids = {o["source_id"] for o in diff["orphans"]}
        assert "cap1" not in orphan_ids
        # noop counts just the real paper.
        assert diff["noop_count"] == 1


def test_f1b_in_manifest_flag_reflects_manifest_membership():
    """If a captcha-titled source's canonical_key is already in the manifest,
    in_manifest=True so the resolver can mark_deleted it later."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        # Manifest knows pmid:222 as an ok source.
        mpath = _fake_manifest(tmp, [
            {"canonical_key": "pmid:222", "status": "ok", "origin_pesquisa": "p1",
             "ingest_method": "url_direct", "title": "Paper B"},
        ])
        # NBM has the same canonical_key but a captcha title (someone replaced
        # the original add with a wall page). F1b still detects it via title.
        current = [
            {"id": "cap1", "title": "Access Denied",
             "url": "https://pubmed.ncbi.nlm.nih.gov/222/", "added_at": "2026-03-10T10:00:00Z"},
        ]
        expected = _expected_from_manifest(
            [{"canonical_key": "pmid:222", "status": "ok", "origin_pesquisa": "p1",
              "ingest_method": "url_direct", "title": "Paper B"}],
            {"p1"},
        )
        diff = compute_diff(
            current_sources=current, expected_sources=expected,
            manifest_path=mpath, notebook_id=NOTEBOOK_ID, max_retry=3,
        )
        assert len(diff["captcha_page_disguised"]) == 1
        cap = diff["captcha_page_disguised"][0]
        assert cap["source_id"] == "cap1"
        assert cap["in_manifest"] is True
        assert cap["derived_canonical_key"] == "pmid:222"


def test_f1b_captcha_excluded_from_duplicates_group():
    """Two sources resolve to the same canonical_key (e.g. both point to
    the same PubMed ID). One has a real title, the other has a captcha
    title. The captcha one must leave the duplicate group; the remaining
    group has <2 members so duplicates ends up empty."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        mpath = _fake_manifest(tmp, [
            {"canonical_key": "pmid:333", "status": "ok", "origin_pesquisa": "p1",
             "ingest_method": "url_direct", "title": "Paper C"},
        ])
        current = [
            {"id": "real", "title": "Paper C legit", "url": "https://pubmed.ncbi.nlm.nih.gov/333/",
             "added_at": "2026-03-01T10:00:00Z"},
            {"id": "cap", "title": "Cloudflare", "url": "https://pubmed.ncbi.nlm.nih.gov/333/",
             "added_at": "2026-03-02T10:00:00Z"},
        ]
        expected = _expected_from_manifest(
            [{"canonical_key": "pmid:333", "status": "ok", "origin_pesquisa": "p1",
              "ingest_method": "url_direct", "title": "Paper C"}],
            {"p1"},
        )
        diff = compute_diff(
            current_sources=current, expected_sources=expected,
            manifest_path=mpath, notebook_id=NOTEBOOK_ID, max_retry=3,
        )
        # Captcha lives in its own bucket.
        assert [c["source_id"] for c in diff["captcha_page_disguised"]] == ["cap"]
        # Duplicates empty because removing the captcha shrinks the group to 1.
        assert diff["duplicates"] == []
        # noop counts the surviving real source as conformant.
        assert diff["noop_count"] == 1


def test_f1b_noop_not_credited_when_only_source_is_captcha():
    """A canonical_key that matches expected but whose only NBM source is a
    captcha page should NOT count toward noop — the conformant source is
    effectively missing until the resolver runs."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        mpath = _fake_manifest(tmp, [
            {"canonical_key": "pmid:444", "status": "ok", "origin_pesquisa": "p1",
             "ingest_method": "url_direct", "title": "Paper D"},
        ])
        current = [
            {"id": "cap", "title": "403 Forbidden", "url": "https://pubmed.ncbi.nlm.nih.gov/444/",
             "added_at": "2026-03-01T10:00:00Z"},
        ]
        expected = _expected_from_manifest(
            [{"canonical_key": "pmid:444", "status": "ok", "origin_pesquisa": "p1",
              "ingest_method": "url_direct", "title": "Paper D"}],
            {"p1"},
        )
        diff = compute_diff(
            current_sources=current, expected_sources=expected,
            manifest_path=mpath, notebook_id=NOTEBOOK_ID, max_retry=3,
        )
        assert len(diff["captcha_page_disguised"]) == 1
        assert diff["noop_count"] == 0


# ---------------------------------------------------------------------------
# resolver coverage
# ---------------------------------------------------------------------------

class _FakeState:
    def __init__(self):
        self.deleted: list[str] = []
        self.readd_calls: list[dict] = []
        self.delete_should_fail_for: set[str] = set()

    def cli_delete(self, notebook_id: str, sid: str) -> bool:
        if sid in self.delete_should_fail_for:
            return False
        self.deleted.append(sid)
        return True

    def delegate(self, **kw):
        self.readd_calls.append({"urls": list(kw["urls"]), "slug": kw["pesquisa_slug"]})
        return {"ok": True, "auto_uploaded": len(kw["urls"]), "manual_required": 0, "skipped_duplicate": 0}


def _patch_resolver(state: _FakeState):
    auditor._cli_delete = state.cli_delete
    auditor._delegate_sci_fetch = state.delegate


def test_f1b_resolver_dry_run_lists_without_side_effects():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        mpath = _fake_manifest(tmp, [])
        state = _FakeState()
        _patch_resolver(state)
        items = [
            {"source_id": "cap1", "title": "Cloudflare", "url": "https://x.com/a",
             "derived_canonical_key": "doi:10.1/abc", "in_manifest": False},
        ]
        action, failed = auditor.resolve_captcha_page_disguised(
            items=items, notebook_id=NOTEBOOK_ID,
            manifest_path=mpath, pesquisas_root=tmp, pesquisa_slugs=["p1"],
            dry_run=True,
        )
        assert failed is False
        assert state.deleted == []
        assert state.readd_calls == []
        assert len(action["results"]) == 1
        assert "dry-run" in action["results"][0]["status"]


def test_f1b_resolver_apply_deletes_and_readds_and_marks_history():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        # Seed manifest with one source that we expect to be marked deleted.
        ms = [
            {"canonical_key": "pmid:555", "status": "ok", "origin_pesquisa": "p1",
             "ingest_method": "url_direct", "title": "Paper E",
             "added_at": "2026-03-01T00:00:00Z"},
        ]
        mpath = _fake_manifest(tmp, ms)
        state = _FakeState()
        _patch_resolver(state)

        items = [
            # Known in manifest — resolver must call mark_deleted.
            {"source_id": "cap1", "title": "Access Denied",
             "url": "https://pubmed.ncbi.nlm.nih.gov/555/",
             "derived_canonical_key": "pmid:555", "in_manifest": True},
            # Orphan-by-birth — delete only, no manifest mutation.
            {"source_id": "cap2", "title": "Cloudflare",
             "url": "https://wiley.com/some-paper",
             "derived_canonical_key": "url:wiley.com/some-paper", "in_manifest": False},
        ]
        action, failed = auditor.resolve_captcha_page_disguised(
            items=items, notebook_id=NOTEBOOK_ID,
            manifest_path=mpath, pesquisas_root=tmp, pesquisa_slugs=["p1"],
            dry_run=False,
        )
        assert failed is False
        # Both sources must have been deleted via the CLI.
        assert sorted(state.deleted) == ["cap1", "cap2"]
        # sci_fetch delegated exactly once with both URLs.
        assert len(state.readd_calls) == 1
        assert sorted(state.readd_calls[0]["urls"]) == [
            "https://pubmed.ncbi.nlm.nih.gov/555/",
            "https://wiley.com/some-paper",
        ]
        assert state.readd_calls[0]["slug"] == "p1"
        # Manifest must have the in-manifest source flipped to deleted.
        after = manifest.lookup_source(mpath, NOTEBOOK_ID, "pmid:555")
        assert after is not None
        assert after["status"] == "deleted"
        assert after["deletion_reason"] == "captcha_page_detected"
        # Orphan captcha was not in the manifest → no entry gets created.
        assert manifest.lookup_source(mpath, NOTEBOOK_ID, "url:wiley.com/some-paper") is None


def test_f1b_resolver_apply_propagates_delete_failure():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        mpath = _fake_manifest(tmp, [])
        state = _FakeState()
        state.delete_should_fail_for = {"cap_bad"}
        _patch_resolver(state)
        items = [
            {"source_id": "cap_bad", "title": "Cloudflare", "url": "https://x.com/a",
             "derived_canonical_key": None, "in_manifest": False},
        ]
        action, failed = auditor.resolve_captcha_page_disguised(
            items=items, notebook_id=NOTEBOOK_ID,
            manifest_path=mpath, pesquisas_root=tmp, pesquisa_slugs=["p1"],
            dry_run=False,
        )
        assert failed is True
        assert state.deleted == []
        # Nothing was readd'd because the only URL came from a failed delete.
        assert state.readd_calls == []
        assert action["results"][0]["status"] == "delete_failed"


def test_f1b_resolver_empty_input_is_fast_noop():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        mpath = _fake_manifest(tmp, [])
        state = _FakeState()
        _patch_resolver(state)
        action, failed = auditor.resolve_captcha_page_disguised(
            items=[], notebook_id=NOTEBOOK_ID,
            manifest_path=mpath, pesquisas_root=tmp, pesquisa_slugs=["p1"],
            dry_run=False,
        )
        assert failed is False
        assert action["results"] == []
        assert state.deleted == []
        assert state.readd_calls == []


# ---------------------------------------------------------------------------
# Entry
# ---------------------------------------------------------------------------
TESTS = [
    test_f1b_captcha_page_lands_in_dedicated_bucket_not_orphans,
    test_f1b_in_manifest_flag_reflects_manifest_membership,
    test_f1b_captcha_excluded_from_duplicates_group,
    test_f1b_noop_not_credited_when_only_source_is_captcha,
    test_f1b_resolver_dry_run_lists_without_side_effects,
    test_f1b_resolver_apply_deletes_and_readds_and_marks_history,
    test_f1b_resolver_apply_propagates_delete_failure,
    test_f1b_resolver_empty_input_is_fast_noop,
]


def main() -> int:
    import importlib
    passed = failed = 0
    for t in TESTS:
        importlib.reload(__import__("auditor"))
        globals()["auditor"] = sys.modules["auditor"]
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
