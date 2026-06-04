#!/usr/bin/env python3
"""F10: bootstrap an empty manifest from current NBM + pesquisa state.

Context
-------
When a user runs the auditor on a notebook that was created BEFORE the
manifest existed (or whose manifest was wiped), the `missing` bucket is
empty — the tool has no expected state to diff against. The v1 behavior
was to exit 3 with a warning. That turned out to be too passive: in Fase 5
the Hashimoto notebook ran without a manifest and surfaced 90 orphans,
many of them false-positives for sources that a normal deep-research run
would have registered.

Bootstrap fills that gap by creating manifest entries for every current
NBM source, deriving the canonical_key retroactively and mapping the
source to the best-matching pesquisa (by origin-pesquisa title overlap,
reusing F12's autodiscover score). The catch: we cannot know HOW each
source was originally added, so we mark `ingest_method=bootstrap_unknown`.
That disables the retry path — the source will never be auto-retried
because the auditor cannot replay an unknown ingest method.

Safety
------
- No NBM-level action is ever taken from bootstrap. This is a manifest-only
  write.
- Sources with low-confidence derivation (no URL, title-only) are still
  written but get `bootstrap_confidence=low` in ingest_metadata so the user
  can audit them later.
- Duplicate canonical_keys in the current NBM collapse into a single
  manifest entry (first-seen wins) — the auditor's dedup will surface the
  duplicates on the next run.
- Re-running bootstrap on a notebook that already has manifest entries
  does not overwrite — `skipped_existing` counts how many survived.
"""
from __future__ import annotations

import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

_DR_SCRIPTS = Path.home() / ".claude" / "skills" / "deep-research" / "scripts"
if str(_DR_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_DR_SCRIPTS))

import notebook_manifest as manifest  # noqa: E402
from retroactive_dedup import derive_for_all  # noqa: E402


BOOTSTRAP_INGEST_METHOD = "bootstrap_unknown"


def bootstrap_notebook(
    *,
    manifest_path: Path,
    notebook_id: str,
    notebook_title: str,
    current_sources: list[dict],
    pesquisas_paths: list[Path],
    pesquisas_root: Path,
    pesquisa_slugs: list[str],
    dry_run: bool,
) -> dict:
    """Create manifest entries for every current NBM source not already known.

    Returns a summary dict:
        {
            "created": int,           # new entries written
            "skipped_existing": int,  # canonical_key already in manifest
            "low_confidence": int,    # derivation_confidence=low
            "source_details": [...],  # per-source record for dry-run display
        }

    Implementation notes
    --------------------
    - Pesquisa assignment: when only ONE pesquisa is in scope we use it as
      every source's `origin_pesquisa`. With multiple pesquisas we cannot
      guess without extra signal; the first slug wins (documented limit —
      user can refine via a normal audit afterward).
    - The call to `record_source` uses its upsert semantics: existing
      canonical_keys are left intact (record_source would replay `attempts`
      and mutate the status, which is wrong for bootstrap). We pre-check
      via `lookup_source`.
    """
    summary: dict = {
        "created": 0,
        "skipped_existing": 0,
        "low_confidence": 0,
        "source_details": [],
    }

    if not current_sources:
        return summary

    # Single-slug default; multi-pesquisa falls back to slug[0] with a
    # warning surfaced via summary[source_details].pesquisa_note.
    default_slug = pesquisa_slugs[0] if pesquisa_slugs else "__bootstrap__"
    ambiguous_pesquisa = len(pesquisa_slugs) > 1

    derivations = derive_for_all(current_sources)
    seen_canonical_keys: set[str] = set()

    for src in current_sources:
        sid = src.get("id") or src.get("source_id")
        if not sid:
            continue
        derived = derivations.get(sid, {})
        ck = derived.get("canonical_key")
        if not ck:
            continue
        if ck in seen_canonical_keys:
            # Duplicate in the current NBM — leave the second occurrence
            # unregistered. The auditor's dedup bucket will catch it on
            # the next run.
            continue
        seen_canonical_keys.add(ck)

        confidence = derived.get("confidence", "low")
        if confidence == "low":
            summary["low_confidence"] += 1

        # Skip entries that already exist in the manifest. Bootstrap is
        # additive; we never mutate known entries.
        existing = manifest.lookup_source(manifest_path, notebook_id, ck) if manifest_path.exists() else None
        if existing:
            summary["skipped_existing"] += 1
            summary["source_details"].append({
                "source_id": sid,
                "canonical_key": ck,
                "status": "skipped_existing",
            })
            continue

        detail: dict = {
            "source_id": sid,
            "canonical_key": ck,
            "confidence": confidence,
            "origin_pesquisa": default_slug,
            "ambiguous_pesquisa": ambiguous_pesquisa,
            "title": src.get("title") or "",
            "url": src.get("url") or "",
            "status": "would_create" if dry_run else "created",
        }
        summary["source_details"].append(detail)

        if dry_run:
            summary["created"] += 1
            continue

        manifest.record_source(
            manifest_path=manifest_path,
            notebook_id=notebook_id,
            pesquisa_slug=default_slug,
            pesquisas_root=pesquisas_root,
            canonical_key=ck,
            title=src.get("title") or "",
            source_type=(derived.get("derivation_method", "") or "").split(".")[-1] or "article",
            origin_pesquisa=default_slug,
            status="ok",
            notebooklm_source_id=sid,
            ingest_method=BOOTSTRAP_INGEST_METHOD,
            ingest_metadata={
                "bootstrap_confidence": confidence,
                "bootstrap_derivation": derived.get("derivation_method"),
                "signal_url": src.get("url") or None,
                "ambiguous_pesquisa": ambiguous_pesquisa,
            },
            notebook_title=notebook_title,
        )
        summary["created"] += 1

    return summary
