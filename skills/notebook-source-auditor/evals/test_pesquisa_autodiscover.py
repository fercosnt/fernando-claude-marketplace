#!/usr/bin/env python3
"""F12 tests — pesquisa_autodiscover module + router.resolve_pesquisas.

Scenarios (pesquisa_autodiscover):
    - tokenize removes stopwords, short tokens, preserves accented chars
    - jaccard is 0 on empty sets and symmetric
    - scan_pesquisas picks folders with PESQUISA-*.md, folders without it
      (as fallback), and standalone .md files; skips hidden and _-prefixed
    - extract_title_from_md pulls first H1, falls back to file stem
    - match_pesquisas: high-overlap title → auto tier
    - match_pesquisas: mid-overlap → ambiguous
    - match_pesquisas: zero overlap → no_match
    - autodiscover end-to-end on a fake tree

Scenarios (router.resolve_pesquisas):
    - explicit --pesquisas bypasses autodiscover
    - auto-match returns paths without prompting
    - ambiguous invokes prompt_fn; picks propagate
    - ambiguous with no picks → exit 6
    - no_match → exit 6
    - empty notebook_title → exit 6

Run: python3 evals/test_pesquisa_autodiscover.py
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_SKILL = _HERE.parent
sys.path.insert(0, str(_SKILL / "scripts"))
sys.path.insert(0, str(Path.home() / ".claude/skills/deep-research/scripts"))

import pesquisa_autodiscover as pad  # noqa: E402
import router  # noqa: E402


# ---------------------------------------------------------------------------
# tokenize + jaccard
# ---------------------------------------------------------------------------

def test_f12_tokenize_removes_stopwords_and_short_tokens():
    got = pad.tokenize("The study of Hashimoto's thyroiditis")
    # "the", "of", "study" are stopwords. "s" is below min length.
    assert "hashimoto" in got
    assert "thyroiditis" in got
    assert "the" not in got
    assert "of" not in got
    assert "study" not in got


def test_f12_tokenize_preserves_accented_chars():
    got = pad.tokenize("análise de hipertensão")
    assert "análise" in got
    assert "hipertensão" in got


def test_f12_jaccard_empty_sets_returns_zero():
    assert pad.jaccard(set(), set()) == 0.0
    assert pad.jaccard({"a"}, set()) == 0.0
    assert pad.jaccard(set(), {"a"}) == 0.0


def test_f12_jaccard_identical_sets_returns_one():
    a = {"hashimoto", "thyroiditis"}
    assert pad.jaccard(a, a) == 1.0


def test_f12_jaccard_partial_overlap():
    a = {"hashimoto", "thyroiditis", "autoimmune"}
    b = {"hashimoto", "graves", "autoimmune"}
    # intersection={hashimoto, autoimmune}=2, union={hashimoto, thyroiditis,
    # autoimmune, graves}=4
    assert pad.jaccard(a, b) == 0.5


# ---------------------------------------------------------------------------
# scan_pesquisas
# ---------------------------------------------------------------------------

def _write_pesquisa(root: Path, slug: str, h1: str) -> Path:
    d = root / slug
    d.mkdir(parents=True, exist_ok=True)
    (d / "PESQUISA-main.md").write_text(f"# {h1}\n\nbody here\n", encoding="utf-8")
    return d


def test_f12_scan_finds_folder_pesquisas_with_h1_title():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        _write_pesquisa(tmp, "hashimoto", "Hashimoto Thyroiditis Review")
        _write_pesquisa(tmp, "glp1", "GLP-1 Receptor Agonists")
        got = pad.scan_pesquisas(tmp)
        got_by_slug = {c.slug: c for c in got}
        assert set(got_by_slug) == {"hashimoto", "glp1"}
        assert got_by_slug["hashimoto"].title == "Hashimoto Thyroiditis Review"
        assert got_by_slug["glp1"].title == "GLP-1 Receptor Agonists"


def test_f12_scan_skips_hidden_and_underscore_folders():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        _write_pesquisa(tmp, "real-one", "Real Pesquisa")
        (tmp / "_audits").mkdir()
        (tmp / ".git").mkdir()
        got = pad.scan_pesquisas(tmp)
        assert {c.slug for c in got} == {"real-one"}


def test_f12_scan_folder_without_pesquisa_file_uses_slug_as_title():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "lonely-folder").mkdir()  # no PESQUISA-*.md inside
        got = pad.scan_pesquisas(tmp)
        assert len(got) == 1
        assert got[0].slug == "lonely-folder"
        assert got[0].title == "lonely folder"  # hyphens to spaces


def test_f12_scan_picks_up_standalone_md_files():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "legacy-pesquisa.md").write_text(
            "# Legacy Pesquisa Title\n\nnotes", encoding="utf-8",
        )
        got = pad.scan_pesquisas(tmp)
        assert len(got) == 1
        assert got[0].slug == "legacy-pesquisa"
        assert got[0].title == "Legacy Pesquisa Title"


def test_f12_scan_missing_root_returns_empty():
    assert pad.scan_pesquisas(Path("/does/not/exist/at-all")) == []


# ---------------------------------------------------------------------------
# match_pesquisas
# ---------------------------------------------------------------------------

def _fake_candidate(slug: str, title: str) -> pad.PesquisaCandidate:
    return pad.PesquisaCandidate(path=Path("/tmp") / slug, slug=slug, title=title)


def test_f12_match_auto_tier_for_high_overlap():
    cands = [
        _fake_candidate("hashimoto", "Hashimoto Thyroiditis Review"),
        _fake_candidate("graves", "Graves Disease Mechanism"),
    ]
    result = pad.match_pesquisas(
        notebook_title="Hashimoto Thyroiditis",
        candidates=cands,
    )
    assert result.has_auto is True
    assert [c.slug for c in result.auto] == ["hashimoto"]
    assert result.no_match is False


def test_f12_match_ambiguous_when_overlap_is_middling():
    # Overlap token: {"hashimoto"}. Candidate adds other tokens that push
    # jaccard below 0.8 but still above 0.5.
    cands = [
        _fake_candidate("hashimoto-trials", "Hashimoto Trials"),
    ]
    result = pad.match_pesquisas(
        notebook_title="Hashimoto",  # only 1 token after stopword filtering
        candidates=cands,
        auto_threshold=0.8,
        ambiguous_min=0.5,
    )
    # jaccard = |{hashimoto}| / |{hashimoto, trials}| = 0.5
    assert result.has_auto is False
    assert len(result.ambiguous) == 1
    assert result.no_match is False
    assert result.needs_prompt is True


def test_f12_match_no_match_when_scores_below_floor():
    cands = [
        _fake_candidate("totally-unrelated", "Machine Learning in Finance"),
        _fake_candidate("also-unrelated", "Kubernetes Networking"),
    ]
    result = pad.match_pesquisas(
        notebook_title="Hashimoto Thyroiditis Autoimmune",
        candidates=cands,
    )
    assert result.no_match is True
    assert result.has_auto is False
    assert result.ambiguous == []


def test_f12_match_auto_tier_caps_at_max_auto():
    # 5 candidates whose slug+title tokens identically cover the notebook
    # title tokens → jaccard 1.0 for all. max_auto=3 caps the auto tier.
    # Using slug tokens that coincide with title tokens avoids the slug
    # contributing a unique token that would dilute the score.
    cands = [_fake_candidate(f"shared-topic-{i}", "Shared Topic") for i in range(5)]
    result = pad.match_pesquisas(
        notebook_title="Shared Topic",
        candidates=cands,
        max_auto=3,
    )
    # Every candidate scores 1.0, so the cap should fire regardless of order.
    assert len(result.auto) == 3
    assert all(c.score == 1.0 for c in result.auto)


def test_f12_match_scoring_is_deterministic_and_sorted():
    # "alpha" adds a unique slug token that dilutes the score, while
    # "alpha-beta" reuses title tokens → higher jaccard for alpha-beta.
    cands = [
        _fake_candidate("alpha", "Alpha Beta"),             # adds {alpha, beta}; score ≈ 1.0
        _fake_candidate("garbage", "Unrelated Foo Bar"),    # disjoint; score ≈ 0
    ]
    result = pad.match_pesquisas(
        notebook_title="Alpha Beta",
        candidates=cands,
    )
    # Best-first ordering — and the first auto-match must be the high scorer.
    assert len(result.auto) == 1
    assert result.auto[0].slug == "alpha"


# ---------------------------------------------------------------------------
# autodiscover wrapper
# ---------------------------------------------------------------------------

def test_f12_autodiscover_end_to_end_on_fake_tree():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        _write_pesquisa(tmp, "hashimoto-trials", "Hashimoto Trials and Review")
        _write_pesquisa(tmp, "glp1", "GLP-1 Agonists")
        result = pad.autodiscover(notebook_title="Hashimoto Trials", root=tmp)
        assert result.scan_root == tmp
        assert result.scanned_count == 2
        assert len(result.auto) == 1
        assert result.auto[0].slug == "hashimoto-trials"


# ---------------------------------------------------------------------------
# router.resolve_pesquisas
# ---------------------------------------------------------------------------

def test_f12_router_explicit_pesquisas_skips_autodiscover():
    paths, rc = router.resolve_pesquisas(
        notebook_title="anything",
        pesquisas_flag="/tmp/one,/tmp/two",
        pesquisas_root=None,
    )
    assert rc == 0
    assert paths == [Path("/tmp/one"), Path("/tmp/two")]


def test_f12_router_auto_match_returns_paths_without_prompt():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        _write_pesquisa(tmp, "hashimoto", "Hashimoto Thyroiditis")
        # Prompt must NOT be called when we already have auto-matches.
        def fail_prompt(result):  # noqa: ARG001
            raise AssertionError("prompt called despite auto-match existing")
        paths, rc = router.resolve_pesquisas(
            notebook_title="Hashimoto Thyroiditis",
            pesquisas_flag=None,
            pesquisas_root=tmp,
            prompt_fn=fail_prompt,
        )
        assert rc == 0
        assert len(paths) == 1
        assert paths[0].name == "hashimoto"


def test_f12_router_ambiguous_invokes_prompt_and_uses_picks():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        # Title shares 1 token with pesquisa, so jaccard ~ 0.5 → ambiguous.
        _write_pesquisa(tmp, "hashimoto-trials", "Hashimoto Trials")
        captured = {}
        def prompt(result):
            captured["result"] = result
            return [result.ambiguous[0].path]
        paths, rc = router.resolve_pesquisas(
            notebook_title="Hashimoto",
            pesquisas_flag=None,
            pesquisas_root=tmp,
            prompt_fn=prompt,
        )
        assert rc == 0
        assert len(paths) == 1
        assert captured["result"].needs_prompt is True


def test_f12_router_ambiguous_with_no_picks_exits_6():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        _write_pesquisa(tmp, "hashimoto-trials", "Hashimoto Trials")
        paths, rc = router.resolve_pesquisas(
            notebook_title="Hashimoto",
            pesquisas_flag=None,
            pesquisas_root=tmp,
            prompt_fn=lambda result: [],
        )
        assert rc == 6
        assert paths == []


def test_f12_router_no_match_exits_6_without_prompting():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        _write_pesquisa(tmp, "totally-different", "Machine Learning in Finance")
        def fail_prompt(result):  # noqa: ARG001
            raise AssertionError("prompt called despite no-match")
        paths, rc = router.resolve_pesquisas(
            notebook_title="Hashimoto Thyroiditis Autoimmune",
            pesquisas_flag=None,
            pesquisas_root=tmp,
            prompt_fn=fail_prompt,
        )
        assert rc == 6
        assert paths == []


def test_f12_router_empty_notebook_title_exits_6():
    paths, rc = router.resolve_pesquisas(
        notebook_title="",
        pesquisas_flag=None,
        pesquisas_root=None,
    )
    assert rc == 6
    assert paths == []


# ---------------------------------------------------------------------------
# Entry
# ---------------------------------------------------------------------------
TESTS = [
    test_f12_tokenize_removes_stopwords_and_short_tokens,
    test_f12_tokenize_preserves_accented_chars,
    test_f12_jaccard_empty_sets_returns_zero,
    test_f12_jaccard_identical_sets_returns_one,
    test_f12_jaccard_partial_overlap,
    test_f12_scan_finds_folder_pesquisas_with_h1_title,
    test_f12_scan_skips_hidden_and_underscore_folders,
    test_f12_scan_folder_without_pesquisa_file_uses_slug_as_title,
    test_f12_scan_picks_up_standalone_md_files,
    test_f12_scan_missing_root_returns_empty,
    test_f12_match_auto_tier_for_high_overlap,
    test_f12_match_ambiguous_when_overlap_is_middling,
    test_f12_match_no_match_when_scores_below_floor,
    test_f12_match_auto_tier_caps_at_max_auto,
    test_f12_match_scoring_is_deterministic_and_sorted,
    test_f12_autodiscover_end_to_end_on_fake_tree,
    test_f12_router_explicit_pesquisas_skips_autodiscover,
    test_f12_router_auto_match_returns_paths_without_prompt,
    test_f12_router_ambiguous_invokes_prompt_and_uses_picks,
    test_f12_router_ambiguous_with_no_picks_exits_6,
    test_f12_router_no_match_exits_6_without_prompting,
    test_f12_router_empty_notebook_title_exits_6,
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
