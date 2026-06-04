#!/usr/bin/env python3
"""Derive canonical_keys retroactively for NotebookLM sources that predate
the manifest (RF-10).

Used by diff_engine.py. Given a source dict coming from
`notebooklm source list --json`, produce the best canonical_key we can with
explicit confidence, so the caller can decide whether to group it in
duplicates / promote it to manifest / leave it as orphan.

Confidence levels:
    high    — PMID / PMC / DOI matched by classify_url OR normalized URL
    medium  — URL normalized (lowercased scheme+host, no query)
    low     — fell back to title-based key (no URL available)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

# Resolve imports to deep-research scripts (notebook_manifest + classify_url).
_DR_SCRIPTS = Path.home() / ".claude" / "skills" / "deep-research" / "scripts"
if str(_DR_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_DR_SCRIPTS))
_SCI_FETCH = _DR_SCRIPTS / "sci_fetch"
if str(_SCI_FETCH) not in sys.path:
    sys.path.insert(0, str(_SCI_FETCH))

import notebook_manifest as manifest  # noqa: E402
from classify_url import classify  # noqa: E402


_TITLE_CLEAN_RE = re.compile(r"[^a-z0-9]+")


def _title_key(title: str) -> str:
    """Last-resort canonical_key derived from title only. Low confidence."""
    slug = _TITLE_CLEAN_RE.sub("-", title.lower()).strip("-")
    slug = slug[:80] or "untitled"
    return f"title:{slug}"


def derive_canonical_key(source: dict) -> dict:
    """Given a source from NotebookLM, derive the best canonical_key.

    Returns {canonical_key, confidence, derivation_method, source_signal}.
    Never returns None — worst case falls back to title-based key.
    """
    url = (source.get("url") or "").strip()
    title = (source.get("title") or "").strip() or "(untitled)"

    if url:
        cls = classify(url)
        ctype = cls.get("type")
        meta = cls.get("metadata") or {}

        if ctype == "pubmed" and meta.get("pmid"):
            return {
                "canonical_key": f"pmid:{meta['pmid']}",
                "confidence": "high",
                "derivation_method": "classify_url.pubmed",
                "source_signal": url,
            }
        pmcid = meta.get("pmcid") or meta.get("pmc_id")
        if ctype == "pmc" and pmcid:
            return {
                "canonical_key": f"pmc:{pmcid}",
                "confidence": "high",
                "derivation_method": "classify_url.pmc",
                "source_signal": url,
            }
        if ctype == "doi" and meta.get("doi"):
            return {
                "canonical_key": f"doi:{meta['doi'].lower()}",
                "confidence": "high",
                "derivation_method": "classify_url.doi",
                "source_signal": url,
            }

        # Fallback: normalize URL.
        try:
            normalized = manifest.normalize_url(url)
            return {
                "canonical_key": f"url:{normalized}",
                "confidence": "medium",
                "derivation_method": "manifest.normalize_url",
                "source_signal": url,
            }
        except Exception:  # noqa: BLE001 — normalize may raise on weird urls
            pass

    # No URL → title only. Low confidence, flag for user review.
    return {
        "canonical_key": _title_key(title),
        "confidence": "low",
        "derivation_method": "title_fallback",
        "source_signal": title,
    }


def derive_for_all(current_sources: list[dict]) -> dict[str, dict]:
    """Map source_id → {canonical_key, confidence, ...} for every source."""
    out: dict[str, dict] = {}
    for src in current_sources:
        sid = src.get("id") or src.get("source_id")
        if not sid:
            continue
        out[sid] = {
            **derive_canonical_key(src),
            "source_id": sid,
            "title": src.get("title") or "",
            "url": src.get("url") or "",
        }
    return out


def _main() -> int:
    """Smoke-test CLI: reads a single JSON source from stdin, prints derivation."""
    import json
    try:
        source = json.loads(sys.stdin.read())
    except Exception as e:  # noqa: BLE001
        print(f"[error] expected JSON on stdin: {e}", file=sys.stderr)
        return 1
    print(json.dumps(derive_canonical_key(source), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(_main())
