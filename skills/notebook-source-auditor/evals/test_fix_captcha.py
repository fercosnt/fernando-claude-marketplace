#!/usr/bin/env python3
"""F7 + F11 + F15 tests for the composite --fix-captcha mode.

Scenarios:
    - F15 regex catches all new patterns (Access Denied, Cloudflare, 403, ...)
    - run_fix_captcha dry-run: detects + reports but no destructive calls
    - run_fix_captcha apply: deletes captchas, re-adds via sci_fetch, converges
    - F11 convergence guard: stops after MAX_ROUNDS if dupes keep re-appearing
    - Empty notebook: no detection → 0-exit + early report

Run: python3 evals/test_fix_captcha.py
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
from captcha_patterns import is_captcha_title, filter_captcha_sources  # noqa: E402


# ---------------------------------------------------------------------------
# F15: expanded regex coverage
# ---------------------------------------------------------------------------
CAPTCHA_TITLES_YES = [
    "Checking your browser before accessing",
    "reCAPTCHA challenge",
    "Access Denied",
    "Just a moment...",
    "Cloudflare",
    "Attention Required! | Cloudflare",
    "Please Wait...",
    "Security Check",
    "Verify you are human",
    "403 Forbidden",
    "Error 403",
    "Sage Journals: Discover world-class research",
    "sage journals: discover world-class research and reviews",
]
CAPTCHA_TITLES_NO = [
    "A cohort study of levothyroxine dosing in Hashimoto's",
    "Hashimoto's thyroiditis: a review of pathogenesis",
    "Empty page",
    "",
    None,
    "403: the bookstore is at level 3",  # 403 standalone, not an error phrase
]


def test_f15_all_known_patterns_match():
    for title in CAPTCHA_TITLES_YES:
        assert is_captcha_title(title), f"expected captcha hit for: {title!r}"


def test_f15_no_false_positives_on_legitimate_titles():
    for title in CAPTCHA_TITLES_NO:
        assert not is_captcha_title(title), f"false positive: {title!r}"


def test_f15_filter_captcha_sources_preserves_shape():
    sources = [
        {"id": "a", "title": "Checking your browser", "url": "https://x.com"},
        {"id": "b", "title": "A real paper", "url": "https://y.com"},
        {"id": "c", "title": "Cloudflare", "url": "https://z.com"},
    ]
    got = filter_captcha_sources(sources)
    assert [s["id"] for s in got] == ["a", "c"], got


# ---------------------------------------------------------------------------
# F7 + F11 integration — stub NBM CLI + sci_fetch subprocess
# ---------------------------------------------------------------------------
class _StubState:
    """In-memory NBM state used to drive end-to-end F7 assertions."""
    def __init__(self, initial: list[dict]):
        self.sources: list[dict] = list(initial)
        self.delete_calls: list[str] = []
        self.readd_calls: list[dict] = []  # parsed sci_fetch invocations

    def list_sources(self, notebook_id: str) -> dict:
        return {"title": "Test NB", "sources": list(self.sources)}

    def cli_delete(self, notebook_id: str, sid: str) -> bool:
        self.delete_calls.append(sid)
        self.sources = [s for s in self.sources if s.get("id") != sid]
        return True


def _patch_auditor(state: _StubState, readd_side_effect=None):
    """Monkey-patch auditor's I/O shims. Returns the patched module state.

    `readd_side_effect(state, urls)` runs after each sci_fetch delegation and
    can append new fake sources to state.sources — simulating the real
    upload pipeline + post-readd state.
    """
    auditor.list_notebook_sources = state.list_sources
    auditor._cli_delete = state.cli_delete

    def fake_delegate(**kw):
        state.readd_calls.append({"urls": list(kw["urls"]), "slug": kw["pesquisa_slug"]})
        if readd_side_effect is not None:
            readd_side_effect(state, kw["urls"])
        return {
            "ok": True,
            "auto_uploaded": len(kw["urls"]),
            "manual_required": 0,
            "skipped_duplicate": 0,
        }

    auditor._delegate_sci_fetch = fake_delegate


def _seed_manifest(tmp: Path) -> Path:
    p = tmp / "_notebook-manifest.json"
    p.write_text('{"version": 1, "notebooks": {}}', encoding="utf-8")
    return p


def _seed_pesquisa(tmp: Path, slug: str) -> Path:
    d = tmp / slug
    d.mkdir(parents=True, exist_ok=True)
    (d / "PESQUISA-stub.md").write_text("# stub\n", encoding="utf-8")
    return d


def test_f7_no_captchas_detected_is_zero_exit():
    """Notebook without captcha sources → fix-captcha reports 0 detected, exits 0."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        p = _seed_pesquisa(tmp, "p1")
        mpath = _seed_manifest(tmp)
        state = _StubState([
            {"id": "s1", "title": "A real paper", "url": "https://pubmed.ncbi.nlm.nih.gov/1/"},
        ])
        _patch_auditor(state)
        code, report = auditor.run_fix_captcha(
            notebook_id="nb_x", notebook_title="Test",
            pesquisas_paths=[p], pesquisas_root=tmp,
            pesquisa_slugs=["p1"], manifest_path=mpath,
            audits_dir=tmp / "_audits",
            current_sources=state.sources,
            dry_run=False, max_retry=3,
        )
        assert code == 0, (code, report)
        assert report["detected_count"] == 0
        assert report["converged"] is True
        assert state.delete_calls == [] and state.readd_calls == []


def test_f7_dry_run_detects_but_no_writes():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        p = _seed_pesquisa(tmp, "p1")
        mpath = _seed_manifest(tmp)
        state = _StubState([
            {"id": "c1", "title": "Checking your browser", "url": "https://sage.com/a"},
            {"id": "c2", "title": "Cloudflare", "url": "https://wiley.com/b"},
            {"id": "s1", "title": "Real paper", "url": "https://pubmed.ncbi.nlm.nih.gov/1/"},
        ])
        _patch_auditor(state)
        code, report = auditor.run_fix_captcha(
            notebook_id="nb_x", notebook_title="Test",
            pesquisas_paths=[p], pesquisas_root=tmp,
            pesquisa_slugs=["p1"], manifest_path=mpath,
            audits_dir=tmp / "_audits",
            current_sources=state.sources,
            dry_run=True, max_retry=3,
        )
        assert code == 0
        assert report["detected_count"] == 2
        # dry-run must not delete or call sci_fetch.
        assert state.delete_calls == []
        assert state.readd_calls == []


def test_f7_apply_full_cycle_converges():
    """The golden path: captchas detected → deleted → re-added (via sci_fetch
    stub that simulates successful uploads, no new dupes) → dedupe rounds find
    nothing → converged=True, exit=0."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        p = _seed_pesquisa(tmp, "p1")
        mpath = _seed_manifest(tmp)
        state = _StubState([
            {"id": "c1", "title": "Checking your browser", "url": "https://sage.com/a"},
            {"id": "c2", "title": "Cloudflare", "url": "https://wiley.com/b"},
        ])

        # Simulate sci_fetch re-add: replace captchas with clean entries.
        def after_readd(st: _StubState, urls):
            for i, u in enumerate(urls):
                st.sources.append({"id": f"re_{i}", "title": "Recovered paper", "url": u})
        _patch_auditor(state, readd_side_effect=after_readd)

        code, report = auditor.run_fix_captcha(
            notebook_id="nb_x", notebook_title="Test",
            pesquisas_paths=[p], pesquisas_root=tmp,
            pesquisa_slugs=["p1"], manifest_path=mpath,
            audits_dir=tmp / "_audits",
            current_sources=state.sources,
            dry_run=False, max_retry=3,
        )
        assert code == 0, (code, report)
        assert state.delete_calls == ["c1", "c2"]
        # exactly 1 sci_fetch batch containing both URLs
        assert len(state.readd_calls) == 1
        assert sorted(state.readd_calls[0]["urls"]) == ["https://sage.com/a", "https://wiley.com/b"]
        assert report["converged"] is True
        # At least one dedupe round ran and found nothing.
        assert len(report["dedupe_rounds"]) >= 1
        assert report["dedupe_rounds"][0]["detected_groups"] == 0


def test_f11_convergence_guard_trips_on_persistent_dupes():
    """F11: stub dedupe to always report 1 residual group → after MAX_ROUNDS
    rounds, report['converged'] must be False and exit=4."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        p = _seed_pesquisa(tmp, "p1")
        mpath = _seed_manifest(tmp)
        state = _StubState([
            {"id": "c1", "title": "Access Denied", "url": "https://nature.com/a"},
        ])
        _patch_auditor(state)
        # Force dedupe to always see residual groups → never converge.
        auditor._dedupe_one_round = lambda **kw: (1, 0)

        code, report = auditor.run_fix_captcha(
            notebook_id="nb_x", notebook_title="Test",
            pesquisas_paths=[p], pesquisas_root=tmp,
            pesquisa_slugs=["p1"], manifest_path=mpath,
            audits_dir=tmp / "_audits",
            current_sources=state.sources,
            dry_run=False, max_retry=3,
            max_rounds=3,
        )
        assert code == 4, (code, report)
        assert report["converged"] is False
        assert len(report["dedupe_rounds"]) == 3


def test_f7_writes_audit_report_to_disk():
    """Report files (md + json) must end up under _audits/<today>."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        p = _seed_pesquisa(tmp, "p1")
        mpath = _seed_manifest(tmp)
        state = _StubState([
            {"id": "c1", "title": "Checking your browser", "url": "https://sage.com/a"},
        ])

        def after_readd(st, urls):
            st.sources.append({"id": "new1", "title": "Recovered", "url": urls[0]})
        _patch_auditor(state, readd_side_effect=after_readd)

        audits_dir = tmp / "_audits"
        code, _report = auditor.run_fix_captcha(
            notebook_id="nb_xyz", notebook_title="Test",
            pesquisas_paths=[p], pesquisas_root=tmp,
            pesquisa_slugs=["p1"], manifest_path=mpath,
            audits_dir=audits_dir,
            current_sources=state.sources,
            dry_run=False, max_retry=3,
        )
        assert code == 0
        md_files = list(audits_dir.glob("nb_xyz-fix-captcha-*.md"))
        json_files = list((audits_dir / "raw").glob("nb_xyz-fix-captcha-*.json"))
        assert len(md_files) == 1, md_files
        assert len(json_files) == 1, json_files
        loaded = json.loads(json_files[0].read_text())
        assert loaded["detected_count"] == 1
        assert loaded["converged"] is True


# ---------------------------------------------------------------------------
# Entry
# ---------------------------------------------------------------------------
TESTS = [
    test_f15_all_known_patterns_match,
    test_f15_no_false_positives_on_legitimate_titles,
    test_f15_filter_captcha_sources_preserves_shape,
    test_f7_no_captchas_detected_is_zero_exit,
    test_f7_dry_run_detects_but_no_writes,
    test_f7_apply_full_cycle_converges,
    test_f11_convergence_guard_trips_on_persistent_dupes,
    test_f7_writes_audit_report_to_disk,
]


def main() -> int:
    # Reset state each test (the patch monkeying sticks across tests).
    passed = failed = 0
    for t in TESTS:
        import importlib
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
