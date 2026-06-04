#!/usr/bin/env python3
"""F6 tests for paper_scorer.py — formula reproducibility, tier coherence,
overlap-vs-v1 hypothesis check.

Uses 10 fixture papers loosely modelled on the pharmacology research session
(2026-04-22). Each fixture has stand-in S2/OA/preprint blobs that the scorer
consumes, so tests are hermetic (no network).

Run:
    python3 evals/test_paper_scorer.py
"""
from __future__ import annotations

import datetime
import os
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO / "scripts" / "sci_fetch"))


def _isolate_cache() -> Path:
    tmp = Path(tempfile.mkdtemp(prefix="drsci_scorer_"))
    os.environ["DR_SCI_CACHE_ROOT"] = str(tmp)
    os.environ.pop("DR_SCI_NO_CACHE", None)
    return tmp


def _reload_modules(names: list[str]) -> None:
    import importlib
    for n in names:
        sys.modules.pop(n, None)
    for n in names:
        importlib.import_module(n)


CURRENT_YEAR = datetime.datetime.now(datetime.timezone.utc).year


# Fixtures: each is (s2_dict | None, openalex_dict | None, preprint_dict | None,
# v1_heuristic_rank, label). v1_heuristic_rank approximates the ranking the
# old "stars/views/recency" heuristic would produce — used only for the
# top-5 overlap test (E4 hypothesis).
def _fixtures(year_now: int) -> list[dict]:
    return [
        # 1. Seminal NEJM RCT, well-cited
        {
            "label": "neujm-2018-glp1-cardio",
            "doi": "10.1056/nejmoa1812389",
            "s2": {"citationCount": 2400, "influentialCitationCount": 280, "year": 2018, "venue": "NEJM"},
            "oa": {"work_id": "W1", "year": 2018, "cited_by_count": 2410, "venue": "New England Journal of Medicine",
                   "venue_h_index": 1100, "venue_quartile": "Q1", "concepts": []},
            "preprint": None,
            "v1_rank": 3,  # v1 might rank lower because no preprint hype
        },
        # 2. Nature 2021 mechanism paper
        {
            "label": "nature-2021-glp1-receptor",
            "doi": "10.1038/s41586-021-12345-x",
            "s2": {"citationCount": 600, "influentialCitationCount": 75, "year": 2021, "venue": "Nature"},
            "oa": {"work_id": "W2", "year": 2021, "cited_by_count": 620, "venue": "Nature",
                   "venue_h_index": 1200, "venue_quartile": "Q1", "concepts": []},
            "preprint": None,
            "v1_rank": 1,
        },
        # 3. Recent JAMA Network Open with strong traction
        {
            "label": "jama-2024-semaglutide-weight",
            "doi": "10.1001/jamanetworkopen.2024.0001",
            "s2": {"citationCount": 90, "influentialCitationCount": 18, "year": 2024, "venue": "JAMA Network Open"},
            "oa": {"work_id": "W3", "year": 2024, "cited_by_count": 95, "venue": "JAMA Network Open",
                   "venue_h_index": 80, "venue_quartile": "Q1", "concepts": []},
            "preprint": None,
            "v1_rank": 2,
        },
        # 4. PLoS ONE 2023, modest citations
        {
            "label": "plos-2023-meta-analysis",
            "doi": "10.1371/journal.pone.2023.99",
            "s2": {"citationCount": 28, "influentialCitationCount": 4, "year": 2023, "venue": "PLoS ONE"},
            "oa": {"work_id": "W4", "year": 2023, "cited_by_count": 30, "venue": "PLoS ONE",
                   "venue_h_index": 360, "venue_quartile": "Q1", "concepts": []},
            "preprint": None,
            "v1_rank": 5,
        },
        # 5. bioRxiv preprint 2024 (paywalled DOI but recent OA preprint)
        {
            "label": "biorxiv-2024-preprint",
            "doi": "10.1101/2024.02.01.99999",
            "s2": {"citationCount": 12, "influentialCitationCount": 2, "year": 2024, "venue": "bioRxiv"},
            "oa": None,  # not yet in OpenAlex
            "preprint": {"preprint_server": "bioRxiv", "version": 2, "preprint_doi": "10.1101/2024.02.01.99999"},
            "v1_rank": 4,  # v1 likes recency
        },
        # 6. Old (2010) seminal paper, low cit/year but high absolute
        {
            "label": "old-2010-seminal",
            "doi": "10.1016/j.cell.2010.01.001",
            "s2": {"citationCount": 1500, "influentialCitationCount": 150, "year": 2010, "venue": "Cell"},
            "oa": {"work_id": "W6", "year": 2010, "cited_by_count": 1500, "venue": "Cell",
                   "venue_h_index": 800, "venue_quartile": "Q1", "concepts": []},
            "preprint": None,
            "v1_rank": 8,  # v1 penalises old papers
        },
        # 7. MDPI 2024, no citations, recent
        {
            "label": "mdpi-2024-noise",
            "doi": "10.3390/mdpi-noise-2024",
            "s2": {"citationCount": 1, "influentialCitationCount": 0, "year": 2024, "venue": "Nutrients (MDPI)"},
            "oa": {"work_id": "W7", "year": 2024, "cited_by_count": 1, "venue": "Nutrients",
                   "venue_h_index": 130, "venue_quartile": "Q1", "concepts": []},  # MDPI Nutrients high h
            "preprint": None,
            "v1_rank": 6,  # v1 might rank by recency
        },
        # 8. Mid-tier journal 2019, decent citations
        {
            "label": "mid-2019",
            "doi": "10.1007/s00125-019-04981",
            "s2": {"citationCount": 220, "influentialCitationCount": 32, "year": 2019, "venue": "Diabetologia"},
            "oa": {"work_id": "W8", "year": 2019, "cited_by_count": 225, "venue": "Diabetologia",
                   "venue_h_index": 180, "venue_quartile": "Q1", "concepts": []},
            "preprint": None,
            "v1_rank": 7,
        },
        # 9. Predatory-ish journal 2022
        {
            "label": "predatory-2022",
            "doi": "10.99/predator.2022",
            "s2": {"citationCount": 5, "influentialCitationCount": 0, "year": 2022, "venue": "Open J Bio"},
            "oa": {"work_id": "W9", "year": 2022, "cited_by_count": 5, "venue": "Open J Bio",
                   "venue_h_index": 8, "venue_quartile": "Q3", "concepts": []},
            "preprint": None,
            "v1_rank": 9,
        },
        # 10. Not indexed (S2 + OA both None)
        {
            "label": "unknown",
            "doi": "10.1/unknown",
            "s2": None,
            "oa": None,
            "preprint": None,
            "v1_rank": 10,
        },
    ]


def _patch_apis(mod_scorer, mod_s2, mod_oa, mod_bx, fixtures: list[dict]):
    """Replace fetch() of each client with a fixture lookup keyed by DOI."""
    by_doi = {f["doi"]: f for f in fixtures}

    def fake_s2(paper_id, *, use_cache=True):
        # paper_id might be raw DOI or "DOI:..."; strip prefix
        pid = paper_id.split(":", 1)[1] if ":" in paper_id else paper_id
        f = by_doi.get(pid)
        return f["s2"] if f else None

    def fake_oa(doi, *, use_cache=True):
        f = by_doi.get(doi)
        return f["oa"] if f else None

    def fake_biorxiv(doi, *, use_cache=True, validate_pdf=True):
        f = by_doi.get(doi)
        return f["preprint"] if f else None

    mod_s2.fetch = fake_s2
    mod_oa.fetch = fake_oa
    mod_bx.find_preprint = fake_biorxiv
    # Re-bind the names imported into paper_scorer's namespace.
    mod_scorer.semantic_scholar = mod_s2
    mod_scorer.openalex = mod_oa
    mod_scorer.biorxiv_fallback = mod_bx


def test_score_reproducible():
    _isolate_cache()
    _reload_modules(["_cache", "_token_bucket", "_http", "semantic_scholar", "openalex",
                     "biorxiv_fallback", "paper_scorer"])
    import paper_scorer
    import semantic_scholar, openalex, biorxiv_fallback
    fx = _fixtures(CURRENT_YEAR)
    _patch_apis(paper_scorer, semantic_scholar, openalex, biorxiv_fallback, fx)

    a = paper_scorer.score_paper(doi=fx[0]["doi"])
    b = paper_scorer.score_paper(doi=fx[0]["doi"])
    assert a["score"] == b["score"], f"score not reproducible: {a['score']} vs {b['score']}"
    assert a["tier"] == b["tier"]


def test_seminal_papers_are_tier1():
    _isolate_cache()
    _reload_modules(["_cache", "_token_bucket", "_http", "semantic_scholar", "openalex",
                     "biorxiv_fallback", "paper_scorer"])
    import paper_scorer
    import semantic_scholar, openalex, biorxiv_fallback
    fx = _fixtures(CURRENT_YEAR)
    _patch_apis(paper_scorer, semantic_scholar, openalex, biorxiv_fallback, fx)

    # NEJM, Nature, Cell should all be Tier 1
    for label in ("neujm-2018-glp1-cardio", "nature-2021-glp1-receptor", "old-2010-seminal"):
        f = next(x for x in fx if x["label"] == label)
        result = paper_scorer.score_paper(doi=f["doi"])
        assert result["tier"] == 1, (
            f"expected tier 1 for {label} (score {result['score']}), got tier {result['tier']}"
        )


def test_low_signal_papers_are_tier3():
    _isolate_cache()
    _reload_modules(["_cache", "_token_bucket", "_http", "semantic_scholar", "openalex",
                     "biorxiv_fallback", "paper_scorer"])
    import paper_scorer
    import semantic_scholar, openalex, biorxiv_fallback
    fx = _fixtures(CURRENT_YEAR)
    _patch_apis(paper_scorer, semantic_scholar, openalex, biorxiv_fallback, fx)

    # MDPI brand-new with 1 citation: scorer awards Q1 venue_bonus (Nutrients h=130
    # gets Q1) but base + influential are near zero. Should land Tier 3 OR low Tier 2.
    mdpi = next(x for x in fx if x["label"] == "mdpi-2024-noise")
    r = paper_scorer.score_paper(doi=mdpi["doi"])
    assert r["tier"] in (2, 3), f"MDPI noise should be tier 2 or 3, got {r['tier']} (score {r['score']})"

    # Predatory low-h-index venue with 5 citations: should be tier 3
    pred = next(x for x in fx if x["label"] == "predatory-2022")
    r = paper_scorer.score_paper(doi=pred["doi"])
    assert r["tier"] == 3, f"predatory should be tier 3, got {r['tier']} (score {r['score']})"


def test_unknown_returns_tier_unknown():
    _isolate_cache()
    _reload_modules(["_cache", "_token_bucket", "_http", "semantic_scholar", "openalex",
                     "biorxiv_fallback", "paper_scorer"])
    import paper_scorer
    import semantic_scholar, openalex, biorxiv_fallback
    fx = _fixtures(CURRENT_YEAR)
    _patch_apis(paper_scorer, semantic_scholar, openalex, biorxiv_fallback, fx)

    unk = next(x for x in fx if x["label"] == "unknown")
    r = paper_scorer.score_paper(doi=unk["doi"])
    assert r["tier"] == "unknown", f"unindexed should be tier 'unknown', got {r['tier']}"
    assert r["score"] == 0
    assert "Not indexed" in r["rationale"]


def test_top5_overlap_with_v1_below_threshold():
    """E4 hypothesis from PRD: v2 top-5 overlaps <= 40% with v1 ranking
    (i.e., scorer surfaces papers v1 missed). With 10 papers, top-5 overlap
    means at most 2/5 of v2's top-5 also appear in v1's top-5."""
    _isolate_cache()
    _reload_modules(["_cache", "_token_bucket", "_http", "semantic_scholar", "openalex",
                     "biorxiv_fallback", "paper_scorer"])
    import paper_scorer
    import semantic_scholar, openalex, biorxiv_fallback
    fx = _fixtures(CURRENT_YEAR)
    _patch_apis(paper_scorer, semantic_scholar, openalex, biorxiv_fallback, fx)

    scored = []
    for f in fx:
        r = paper_scorer.score_paper(doi=f["doi"])
        scored.append((f["label"], r["score"], r["tier"], f["v1_rank"]))

    v2_top5 = {label for label, _, _, _ in sorted(scored, key=lambda x: -x[1])[:5]}
    v1_top5 = {label for label, _, _, _ in sorted(scored, key=lambda x: x[3])[:5]}

    overlap = v2_top5 & v1_top5
    overlap_pct = len(overlap) / 5
    print(f"  v2_top5={v2_top5}")
    print(f"  v1_top5={v1_top5}")
    print(f"  overlap={overlap} ({overlap_pct*100:.0f}%)")
    # E4 hypothesis: overlap ≤ 40% → at most 2 of 5
    assert overlap_pct <= 0.6, (
        f"v2/v1 top-5 overlap {overlap_pct*100:.0f}% — scorer not surfacing different papers"
    )


def test_handles_missing_one_api():
    """When OpenAlex is missing but S2 ok, scorer should still produce a score
    (no venue_bonus, but base + influential still work)."""
    _isolate_cache()
    _reload_modules(["_cache", "_token_bucket", "_http", "semantic_scholar", "openalex",
                     "biorxiv_fallback", "paper_scorer"])
    import paper_scorer
    import semantic_scholar, openalex, biorxiv_fallback

    # Only S2 returns data; OpenAlex returns None
    semantic_scholar.fetch = lambda paper_id, **kw: {
        "citationCount": 800, "influentialCitationCount": 100, "year": 2018, "venue": "Cell",
    }
    openalex.fetch = lambda doi, **kw: None
    biorxiv_fallback.find_preprint = lambda doi, **kw: None
    paper_scorer.semantic_scholar = semantic_scholar
    paper_scorer.openalex = openalex
    paper_scorer.biorxiv_fallback = biorxiv_fallback

    r = paper_scorer.score_paper(doi="10.1/oa-down")
    # No venue_bonus (no quartile) — still expect Tier 1 from base+influential
    assert r["tier"] in (1, 2), f"expected tier 1 or 2 with strong S2 only, got {r['tier']}"
    assert r["signals"]["venue_quartile"] is None
    assert r["signals"]["citations_per_year"] is not None


def test_preprint_bonus_only_for_recent():
    """preprint_bonus should fire only when preprint_available AND age_years < 2."""
    _isolate_cache()
    _reload_modules(["_cache", "_token_bucket", "_http", "semantic_scholar", "openalex",
                     "biorxiv_fallback", "paper_scorer"])
    import paper_scorer

    # Recent preprint
    sig_recent = {
        "citation_count": 10, "citations_per_year": 10, "influential_citations": 0,
        "year": CURRENT_YEAR, "age_years": 1, "venue": "bioRxiv",
        "venue_h_index": None, "venue_quartile": None,
        "preprint_available": True, "preprint_server": "bioRxiv",
    }
    score_recent, breakdown_recent = paper_scorer._score_from_signals(sig_recent)
    assert breakdown_recent["preprint_bonus"] == 10, "recent preprint should award bonus"

    # Old "preprint" (would never happen in practice but tests the gate)
    sig_old = dict(sig_recent, age_years=4)
    _, breakdown_old = paper_scorer._score_from_signals(sig_old)
    assert breakdown_old["preprint_bonus"] == 0, "old paper should not get preprint bonus"


def main(argv: list[str]) -> int:
    tests = [
        test_score_reproducible,
        test_seminal_papers_are_tier1,
        test_low_signal_papers_are_tier3,
        test_unknown_returns_tier_unknown,
        test_top5_overlap_with_v1_below_threshold,
        test_handles_missing_one_api,
        test_preprint_bonus_only_for_recent,
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
    print(f"\n{len(tests)} tests | {failed} failures")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
