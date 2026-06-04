#!/usr/bin/env python3
"""Composite academic scorer (Semantic Scholar + OpenAlex + bioRxiv).

Produces a 0-100 score and Tier 1/2/3 (or "unknown") with rule-based rationale.

Formula (RF-21 do PRD v2):
    age_years          = max(1, current_year - paper_year)
    citations_per_year = citation_count / age_years
    base               = min(50, citations_per_year * 3)
    influential_bonus  = min(20, influential_citations * 0.5)
    venue_bonus        = {Q1: 20, Q2: 10, Q3: 5, Q4: 0}[quartile]
    preprint_bonus     = 10 if (preprint_available and age_years < 2) else 0
    recency_bonus      = 10 if (age_years < 3 and citations_per_year > 5) else 0
    score              = min(100, sum_of_above)
    tier               = 1 if score >= 70 else (2 if score >= 40 else 3)

Handles missing data:
    - S2 404 + OA OK    → use OA (no influential_citations / S2 fields)
    - OA 404 + S2 OK    → use S2 (no venue quartile)
    - both 404          → tier="unknown", no error raised

Usage:
    python paper_scorer.py --doi "10.1089/thy.2014.0028"
    python paper_scorer.py --pmid 33567185
    python paper_scorer.py --doi 10.1/x --skip-biorxiv  # for paywalled-only check
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

import semantic_scholar
import openalex
import biorxiv_fallback


VENUE_BONUS = {"Q1": 20, "Q2": 10, "Q3": 5, "Q4": 0}
TIER_1_MIN = 70
TIER_2_MIN = 40


def _current_year() -> int:
    return datetime.datetime.now(datetime.timezone.utc).year


def _safe_int(v) -> Optional[int]:
    try:
        return int(v) if v is not None else None
    except (TypeError, ValueError):
        return None


def _gather_signals(
    s2: Optional[dict],
    oa: Optional[dict],
    preprint: Optional[dict],
) -> dict:
    """Reduce three API responses into a flat signals dict the scorer consumes."""
    citation_count = None
    influential = None
    year = None
    venue = None

    if s2:
        citation_count = _safe_int(s2.get("citationCount"))
        influential = _safe_int(s2.get("influentialCitationCount"))
        year = _safe_int(s2.get("year"))
        venue = s2.get("venue")

    if oa:
        # OpenAlex cited_by_count is generally close to S2 citationCount but
        # uses a different graph; prefer the larger of the two as a robustness
        # signal (papers are at least as cited as the smaller estimate).
        oa_cit = _safe_int(oa.get("cited_by_count"))
        if oa_cit is not None and (citation_count is None or oa_cit > citation_count):
            citation_count = oa_cit
        if year is None:
            year = _safe_int(oa.get("year"))
        if not venue:
            venue = oa.get("venue")

    quartile = oa.get("venue_quartile") if oa else None
    venue_h = oa.get("venue_h_index") if oa else None

    current = _current_year()
    age_years = max(1, current - year) if year else None
    cit_per_year = (
        round(citation_count / age_years, 2)
        if (citation_count is not None and age_years)
        else None
    )

    return {
        "citation_count": citation_count,
        "citations_per_year": cit_per_year,
        "influential_citations": influential,
        "year": year,
        "age_years": age_years,
        "venue": venue,
        "venue_h_index": venue_h,
        "venue_quartile": quartile,
        "preprint_available": bool(preprint),
        "preprint_server": preprint.get("preprint_server") if preprint else None,
    }


def _score_from_signals(sig: dict) -> tuple[int, dict]:
    """Returns (score 0-100, breakdown of each component contribution)."""
    cpy = sig.get("citations_per_year") or 0
    influential = sig.get("influential_citations") or 0
    quartile = sig.get("venue_quartile")
    age = sig.get("age_years")
    preprint = sig.get("preprint_available")

    base = min(50, cpy * 3)
    influential_bonus = min(20, influential * 0.5)
    venue_bonus = VENUE_BONUS.get(quartile, 0) if quartile else 0
    preprint_bonus = 10 if (preprint and age is not None and age < 2) else 0
    recency_bonus = 10 if (age is not None and age < 3 and cpy > 5) else 0

    breakdown = {
        "base_citations": round(base, 1),
        "influential_bonus": round(influential_bonus, 1),
        "venue_bonus": venue_bonus,
        "preprint_bonus": preprint_bonus,
        "recency_bonus": recency_bonus,
    }
    raw = sum(breakdown.values())
    score = min(100, max(0, int(round(raw))))
    return score, breakdown


def _tier_from_score(score: int) -> int:
    if score >= TIER_1_MIN:
        return 1
    if score >= TIER_2_MIN:
        return 2
    return 3


def _generate_rationale(sig: dict, breakdown: dict, tier) -> str:
    """1-2 sentence explanation of the dominant signals."""
    if tier == "unknown":
        return "Not indexed in academic graphs (Semantic Scholar / OpenAlex)."

    parts = []
    venue = sig.get("venue")
    quartile = sig.get("venue_quartile")
    cpy = sig.get("citations_per_year")
    influential = sig.get("influential_citations")
    age = sig.get("age_years")

    # Identify the dominant single contribution.
    dominant = max(breakdown.items(), key=lambda kv: kv[1])
    dom_name, dom_val = dominant

    if dom_name == "venue_bonus" and venue:
        parts.append(f"Top venue ({venue}, {quartile})")
    elif dom_name == "base_citations" and cpy:
        parts.append(f"High citation rate ({cpy:.1f}/yr)")
    elif dom_name == "influential_bonus" and influential:
        parts.append(f"{influential} influential citations (S2)")
    elif dom_name == "recency_bonus":
        parts.append(f"Recent ({age}y) and traction is building ({cpy:.1f}/yr)")
    elif dom_name == "preprint_bonus":
        server = sig.get("preprint_server") or "preprint server"
        parts.append(f"Available as {server} preprint (recent, age {age}y)")

    # Add a secondary signal if useful.
    secondary = []
    if dom_name != "venue_bonus" and venue and quartile:
        secondary.append(f"venue {venue} ({quartile})")
    if dom_name != "base_citations" and cpy and cpy >= 5:
        secondary.append(f"{cpy:.1f} citations/yr")
    if dom_name != "influential_bonus" and influential and influential >= 5:
        secondary.append(f"{influential} influential cit.")
    if not parts and not secondary:
        return f"Tier {tier} based on limited signal — {sum(breakdown.values()):.0f} pts total."
    head = " — ".join(parts) if parts else f"Tier {tier}"
    if secondary:
        head += f"; also {', '.join(secondary[:2])}"
    return head + "."


def score_paper(
    *,
    doi: Optional[str] = None,
    pmid: Optional[str] = None,
    use_cache: bool = True,
    fetch_preprint: bool = True,
) -> dict:
    """Score a paper. Returns dict with canonical_key, score, tier, signals, rationale.

    fetch_preprint: when False, skip the bioRxiv/medRxiv lookup (saves an API
    round-trip when the caller already knows there's no preprint to consider).
    """
    if not doi and not pmid:
        raise ValueError("score_paper: pass doi or pmid")

    canonical = f"doi:{doi}" if doi else f"pmid:{pmid}"
    paper_id = doi or pmid

    # Run the three lookups in parallel — they are independent.
    s2_data: Optional[dict] = None
    oa_data: Optional[dict] = None
    preprint_data: Optional[dict] = None
    errors: list[str] = []

    def _run_s2():
        try:
            return semantic_scholar.fetch(paper_id, use_cache=use_cache)
        except Exception as e:
            errors.append(f"semantic_scholar: {e}")
            return None

    def _run_oa():
        if not doi:
            return None  # OpenAlex DOI-only endpoint
        try:
            return openalex.fetch(doi, use_cache=use_cache)
        except Exception as e:
            errors.append(f"openalex: {e}")
            return None

    def _run_biorxiv():
        if not (doi and fetch_preprint):
            return None
        try:
            return biorxiv_fallback.find_preprint(doi, use_cache=use_cache, validate_pdf=False)
        except Exception as e:
            errors.append(f"biorxiv: {e}")
            return None

    with ThreadPoolExecutor(max_workers=3) as pool:
        s2_fut = pool.submit(_run_s2)
        oa_fut = pool.submit(_run_oa)
        bx_fut = pool.submit(_run_biorxiv)
        s2_data = s2_fut.result()
        oa_data = oa_fut.result()
        preprint_data = bx_fut.result()

    # All academic APIs returned nothing → tier unknown.
    if s2_data is None and oa_data is None:
        return {
            "canonical_key": canonical,
            "score": 0,
            "tier": "unknown",
            "signals": {
                "citation_count": None,
                "citations_per_year": None,
                "influential_citations": None,
                "year": None,
                "age_years": None,
                "venue": None,
                "venue_quartile": None,
                "preprint_available": bool(preprint_data),
                "preprint_server": (preprint_data or {}).get("preprint_server"),
            },
            "rationale": "Not indexed in academic graphs (Semantic Scholar / OpenAlex).",
            "errors": errors or None,
        }

    signals = _gather_signals(s2_data, oa_data, preprint_data)
    score, breakdown = _score_from_signals(signals)
    tier = _tier_from_score(score)
    rationale = _generate_rationale(signals, breakdown, tier)

    out = {
        "canonical_key": canonical,
        "score": score,
        "tier": tier,
        "signals": signals,
        "breakdown": breakdown,
        "rationale": rationale,
    }
    if errors:
        out["errors"] = errors
    return out


def _main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--doi")
    g.add_argument("--pmid")
    parser.add_argument("--no-cache", action="store_true")
    parser.add_argument("--skip-biorxiv", action="store_true")
    args = parser.parse_args(argv[1:])

    try:
        result = score_paper(
            doi=args.doi,
            pmid=args.pmid,
            use_cache=not args.no_cache,
            fetch_preprint=not args.skip_biorxiv,
        )
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        return 1
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
