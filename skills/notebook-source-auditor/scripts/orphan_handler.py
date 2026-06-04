#!/usr/bin/env python3
"""Interactive handling of orphan sources (RF-08).

Orphans default to non-destructive: the auditor lists them in the report
and moves on. When `--interactive` is set, each orphan prompts the user
for one of three actions:

    [k]eep    — mark source in manifest as origin_pesquisa='manual_keep'
                so future runs do not re-ask.
    [d]elete  — remove source from NotebookLM AND mark_deleted in manifest.
    [l]ink    — associate source with an existing pesquisa slug. Writes a
                record_source() entry so next audit classifies it as no-op.

With 5+ pesquisas the link choice becomes indexed multiple-choice
(user types a number).
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Callable

# Make deep-research helpers importable.
_DR_SCRIPTS = Path.home() / ".claude" / "skills" / "deep-research" / "scripts"
if str(_DR_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_DR_SCRIPTS))

import notebook_manifest as manifest  # noqa: E402


def _ask(prompt: str, reader: Callable[[str], str] = input) -> str:
    return reader(prompt).strip().lower()


def handle_orphan(
    *,
    orphan: dict,
    notebook_id: str,
    pesquisa_slugs: list[str],
    pesquisas_root: Path,
    manifest_path: Path,
    dry_run: bool,
    reader: Callable[[str], str] = input,
) -> dict:
    """Prompt the user interactively and return the action taken.

    Returns: {"action": "keep"|"delete"|"link"|"skip", "details": {...}}
    """
    title = orphan.get("title") or "(untitled)"
    url = orphan.get("url") or "(no url)"
    confidence = orphan.get("derivation_confidence", "unknown")

    print(f"\n🧩 Orphan: {title}")
    print(f"   URL: {url}")
    print(f"   Derived canonical_key: {orphan['derived_canonical_key']} ({confidence})")
    choice = _ask("   Action — [k]eep / [d]elete / [l]ink / [s]kip? ", reader)

    if choice == "s" or choice == "":
        return {"action": "skip", "details": {}}

    if choice == "k":
        if dry_run:
            return {"action": "keep", "details": {"dry_run": True}}
        src = manifest.record_source(
            manifest_path=manifest_path,
            notebook_id=notebook_id,
            pesquisa_slug="manual_keep",
            pesquisas_root=pesquisas_root,
            canonical_key=orphan["derived_canonical_key"],
            title=title,
            source_type=orphan.get("derivation_method", "orphan_keep"),
            origin_pesquisa="manual_keep",
            status="ok",
            notebooklm_source_id=orphan["source_id"],
            ingest_method="url_direct" if url != "(no url)" else "unknown",
            ingest_metadata={"signal_url": url if url != "(no url)" else None},
        )
        return {"action": "keep", "details": {"manifest_entry": src}}

    if choice == "d":
        if dry_run:
            return {"action": "delete", "details": {"dry_run": True}}
        ok = _cli_delete(notebook_id, orphan["source_id"])
        if ok:
            manifest.mark_deleted(
                manifest_path=manifest_path,
                notebook_id=notebook_id,
                canonical_key=orphan["derived_canonical_key"],
                reason="orphan_user_choice",
            )
        return {"action": "delete", "details": {"cli_ok": ok}}

    if choice == "l":
        slug = _pick_pesquisa(pesquisa_slugs, reader)
        if slug is None:
            return {"action": "skip", "details": {"reason": "link_cancelled"}}
        if dry_run:
            return {"action": "link", "details": {"slug": slug, "dry_run": True}}
        src = manifest.record_source(
            manifest_path=manifest_path,
            notebook_id=notebook_id,
            pesquisa_slug=slug,
            pesquisas_root=pesquisas_root,
            canonical_key=orphan["derived_canonical_key"],
            title=title,
            source_type=orphan.get("derivation_method", "orphan_link"),
            origin_pesquisa=slug,
            status="ok",
            notebooklm_source_id=orphan["source_id"],
            ingest_method="url_direct" if url != "(no url)" else "unknown",
            ingest_metadata={"signal_url": url if url != "(no url)" else None},
        )
        return {"action": "link", "details": {"slug": slug, "manifest_entry": src}}

    # Unrecognized input → skip for safety.
    return {"action": "skip", "details": {"reason": f"unknown_input:{choice}"}}


def _pick_pesquisa(slugs: list[str], reader: Callable[[str], str]) -> str | None:
    """Prompt the user for a pesquisa slug. Indexed multiple-choice when 5+."""
    if not slugs:
        return None
    if len(slugs) < 5:
        print("   Available pesquisas:", ", ".join(slugs))
        raw = reader("   Link to which? ").strip()
        if raw in slugs:
            return raw
        return None
    # Indexed mode.
    print("   Available pesquisas:")
    for i, slug in enumerate(slugs, start=1):
        print(f"     [{i}] {slug}")
    raw = reader("   Link to which number? ").strip()
    try:
        idx = int(raw)
    except ValueError:
        return None
    if 1 <= idx <= len(slugs):
        return slugs[idx - 1]
    return None


def _cli_delete(notebook_id: str, source_id: str) -> bool:
    result = subprocess.run(
        ["notebooklm", "source", "delete", source_id, "-n", notebook_id, "-y"],
        capture_output=True, text=True, timeout=30,
    )
    return result.returncode == 0
