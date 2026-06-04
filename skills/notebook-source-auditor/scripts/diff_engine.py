#!/usr/bin/env python3
"""Compute the 6-bucket diff between NotebookLM state, manifest, and
expected state derived from pesquisa folders (RF-03, RF-04, plus the
`stale_manifest` v1 bonus bucket from Q5 and the F1b `captcha_page_disguised`
bucket from v2 Fase B).

Buckets:
    missing                 — expected canonical_key is absent from the notebook
    retryable               — manifest marks source as captcha_pending|failed AND
                              ingest_method is auto-retryable AND attempts < max
    duplicates              — 2+ current sources resolve to the same canonical_key
                              (captcha-page sources are excluded — they belong to
                              `captcha_page_disguised` and get deleted, not merged)
    captcha_page_disguised  — F1b: current source whose title matches the F15
                              captcha regex. Pulled out of orphans and duplicates
                              because the only sane action is delete+readd via F7.
    orphans                 — current source has no manifest entry AND we cannot
                              confidently map it to an expected canonical_key AND
                              it is not a captcha page
    stale_manifest          — manifest has an `ok` entry but the source is not in
                              the notebook (user deleted it via the UI). Auto-handled
                              by flipping status to `deleted` with reason
                              `deleted_from_nbm_externally`.

Inputs are pure data — this module does no I/O. The orchestrator in
auditor.py loads manifest, fetches NBM state, builds pesquisa expected
state, and passes all three into compute_diff().
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

# Make sibling scripts importable.
_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

# Import deep-research helpers.
_DR_SCRIPTS = Path.home() / ".claude" / "skills" / "deep-research" / "scripts"
if str(_DR_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_DR_SCRIPTS))

import notebook_manifest as manifest  # noqa: E402

from captcha_patterns import is_captcha_title  # noqa: E402
from retroactive_dedup import derive_for_all  # noqa: E402


# ingest methods the auditor can auto-retry. captcha_bypass_flow_v1 is
# excluded by design — it requires human intervention.
_AUTO_RETRY_METHODS = {"url_direct", "pdf_upload"}

# PMID/PMC/DOI extraction for pesquisa .md files (fallback when manifest
# is missing an expected source).
_MD_URL_RE = re.compile(
    r"https?://[A-Za-z0-9._\-/%?=&#:+~]+",
    re.IGNORECASE,
)


def load_expected_from_pesquisas(
    pesquisas_paths: list[Path],
    manifest_path: Path,
    notebook_id: str,
) -> dict[str, dict]:
    """Collect expected canonical_keys from the pesquisa folders.

    Primary source: manifest entries whose notebook_id matches. For any
    source listed in a PESQUISA-*.md but not in the manifest, we best-effort
    derive a canonical_key from the URL so it still shows up in `missing`.

    Returns: {canonical_key: {title, type, origin_pesquisas: [slug], ...}}
    """
    expected: dict[str, dict] = {}
    manifest_data = manifest._load_or_bootstrap(manifest_path)  # noqa: SLF001
    nb = manifest_data.get("notebooks", {}).get(notebook_id, {})
    pesquisa_slugs_in_scope = {p.name for p in pesquisas_paths}

    # 1. Manifest entries scoped to this notebook + the pesquisas we audit.
    # Entries whose origin_pesquisa slug is NOT in scope fall through — the
    # stale_manifest bucket in compute_diff picks them up if NBM also does
    # not have them (the user either renamed the pesquisa or removed the
    # source from intent entirely).
    for src in nb.get("sources", []):
        # Skip sources already marked deleted — they are historical.
        if src.get("status") == "deleted":
            continue
        slug = src.get("origin_pesquisa")
        if slug not in pesquisa_slugs_in_scope:
            continue
        ck = src.get("canonical_key")
        if not ck:
            continue
        if ck not in expected:
            expected[ck] = {
                "canonical_key": ck,
                "title": src.get("title") or "",
                "type": src.get("type") or "",
                "origin_pesquisas": [slug] if slug else [],
                "manifest_entry": src,
                "last_known_status": src.get("status"),
            }
        else:
            if slug and slug not in expected[ck]["origin_pesquisas"]:
                expected[ck]["origin_pesquisas"].append(slug)

    # 2. Scan pesquisa .md files for URLs not yet in the manifest. Best-effort:
    # we classify; if classifiable we add with derived canonical_key.
    # Import here to avoid a circular scan on module load.
    from retroactive_dedup import derive_canonical_key  # noqa: PLC0415

    def _md_files_for(pesquisa_path: Path):
        # Direct .md file → that file is the only source.
        if pesquisa_path.is_file() and pesquisa_path.suffix.lower() == ".md":
            yield pesquisa_path
            return
        # Folder with PESQUISA-*.md (canonical layout).
        canonical = list(pesquisa_path.glob("PESQUISA-*.md"))
        if canonical:
            yield from canonical
            return
        # Fallback: any *.md in the folder, skipping leading-underscore meta files
        # (e.g. _audits/, _notebook-manifest.json siblings).
        for f in pesquisa_path.glob("*.md"):
            if not f.name.startswith("_"):
                yield f

    def _slug_for(pesquisa_path: Path) -> str:
        # File path → use stem; folder → use name.
        return pesquisa_path.stem if pesquisa_path.is_file() else pesquisa_path.name

    for pesquisa_path in pesquisas_paths:
        if not pesquisa_path.exists():
            continue
        slug = _slug_for(pesquisa_path)
        for md_file in _md_files_for(pesquisa_path):
            try:
                text = md_file.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            for url in _MD_URL_RE.findall(text):
                derived = derive_canonical_key({"url": url, "title": ""})
                ck = derived["canonical_key"]
                if ck in expected:
                    if slug not in expected[ck]["origin_pesquisas"]:
                        expected[ck]["origin_pesquisas"].append(slug)
                    continue
                # Only trust md-derived keys when classify_url says high
                # confidence (PMID/PMC/DOI). Medium-confidence raw URLs can
                # create spurious `missing` items if the pesquisa mentions
                # a URL in prose but never intended it as a source. Skip
                # those to avoid false positives.
                if derived["confidence"] != "high":
                    continue
                expected[ck] = {
                    "canonical_key": ck,
                    "title": "",
                    "type": derived["derivation_method"].split(".")[-1],
                    "origin_pesquisas": [slug],
                    "manifest_entry": None,
                    "last_known_status": None,
                    "derived_from_md": True,
                    "signal_url": url,
                }

    return expected


def compute_diff(
    *,
    current_sources: list[dict],
    expected_sources: dict[str, dict],
    manifest_path: Path,
    notebook_id: str,
    max_retry: int = 3,
) -> dict[str, Any]:
    """Compute the 5-bucket diff. Pure function — no I/O beyond reading
    the manifest once (for retryable bucket decisions).

    Returns a dict with keys: missing, retryable, duplicates, orphans,
    stale_manifest, noop_count.
    """
    # Retroactively derive canonical_keys for every current source so we
    # can group duplicates and match orphans against manifest.
    derivations = derive_for_all(current_sources)

    # Build reverse index: canonical_key -> list of sources that resolve to it.
    by_canonical: dict[str, list[dict]] = {}
    for src in current_sources:
        sid = src.get("id") or src.get("source_id")
        if not sid:
            continue
        derived = derivations.get(sid, {})
        ck = derived.get("canonical_key")
        if not ck:
            continue
        enriched = {
            **src,
            "source_id": sid,
            "derived_canonical_key": ck,
            "derivation_confidence": derived.get("confidence"),
            "derivation_method": derived.get("derivation_method"),
            "added_at": src.get("added_at") or src.get("created_at") or "",
        }
        by_canonical.setdefault(ck, []).append(enriched)

    current_canonical_keys = set(by_canonical.keys())
    expected_canonical_keys = set(expected_sources.keys())

    # Load manifest once to classify retryable sources.
    manifest_data = manifest._load_or_bootstrap(manifest_path)  # noqa: SLF001
    nb = manifest_data.get("notebooks", {}).get(notebook_id, {})
    manifest_sources_by_ck = {
        src["canonical_key"]: src
        for src in nb.get("sources", [])
        if src.get("canonical_key")
    }

    # --- Bucket: missing ---
    missing = []
    for ck in sorted(expected_canonical_keys - current_canonical_keys):
        entry = expected_sources[ck]
        missing.append({
            "canonical_key": ck,
            "expected": entry,
        })

    # --- Bucket: retryable ---
    # Only include canonical_keys that are still missing AND have a retry-able
    # manifest entry. Successful retries live alongside `missing`, so we
    # deduplicate by preferring the retryable bucket when both apply.
    retryable = []
    retryable_keys: set[str] = set()
    for ck, src in manifest_sources_by_ck.items():
        status = src.get("status")
        if status not in {"captcha_pending", "failed"}:
            continue
        ingest_method = src.get("ingest_method", "")
        if ingest_method not in _AUTO_RETRY_METHODS:
            continue
        attempts = int(src.get("attempts", 0))
        if attempts >= max_retry:
            continue
        if ck in current_canonical_keys:
            # Already in NBM — manifest is just stale on status; skip. Caller
            # can refresh status later.
            continue
        retryable.append({
            "canonical_key": ck,
            "manifest_entry": src,
            "ingest_method": ingest_method,
            "attempts": attempts,
        })
        retryable_keys.add(ck)

    # Strip retryable keys out of missing to avoid double-resolving them.
    missing = [m for m in missing if m["canonical_key"] not in retryable_keys]

    # --- Bucket: captcha_page_disguised (F1b) ---
    # Any current NBM source whose title matches the F15 regex is a captcha
    # page saved as a source (Cloudflare challenge, Sage wall, Access Denied
    # page, etc). Collect them before computing `duplicates` and `orphans` so
    # those buckets never double-classify the same source. The resolver in
    # auditor.py deletes them and (optionally) re-adds via sci_fetch — merging
    # two captcha pages as duplicates would be wrong (both are garbage).
    captcha_page_disguised: list[dict] = []
    captcha_source_ids: set[str] = set()
    for src in current_sources:
        sid = src.get("id") or src.get("source_id")
        if not sid:
            continue
        title = src.get("title") or ""
        if not is_captcha_title(title):
            continue
        captcha_source_ids.add(sid)
        derived = derivations.get(sid, {})
        manifest_entry = manifest_sources_by_ck.get(derived.get("canonical_key") or "")
        captcha_page_disguised.append({
            "source_id": sid,
            "title": title,
            "url": src.get("url") or "",
            "derived_canonical_key": derived.get("canonical_key"),
            "derivation_confidence": derived.get("confidence"),
            # True when the captcha page is known to the manifest — lets the
            # resolver call mark_deleted() with a canonical_key; False means
            # history can't be recorded (orphan-by-birth).
            "in_manifest": bool(manifest_entry),
        })

    # --- Bucket: duplicates ---
    duplicates = []
    for ck, group in by_canonical.items():
        # F1b: exclude captcha-page sources from duplicate grouping. Their
        # sole action is delete; merging them as `kept` would leave a
        # captcha page in the notebook.
        non_captcha_group = [s for s in group if s["source_id"] not in captcha_source_ids]
        if len(non_captcha_group) < 2:
            continue
        # Keep the source with the earliest added_at. `added_at` may be
        # absent on some NBM responses — fall back to source_id lexical
        # order to keep the result deterministic.
        group_sorted = sorted(non_captcha_group, key=lambda s: (s["added_at"] or "￿", s["source_id"]))
        keep = group_sorted[0]
        delete = group_sorted[1:]
        duplicates.append({
            "canonical_key": ck,
            "sources": group_sorted,
            "keep": keep["source_id"],
            "delete": [s["source_id"] for s in delete],
        })

    # --- Bucket: orphans ---
    # A current source is an orphan when its derived canonical_key is not
    # expected AND there is no manifest entry for it. Low-confidence
    # derivations are flagged for review. F1b: captcha-page sources are
    # excluded here because they land in captcha_page_disguised instead.
    orphans = []
    for ck, group in by_canonical.items():
        if ck in expected_canonical_keys:
            continue
        if ck in manifest_sources_by_ck:
            # Manifest knows about it but the user did not pass its pesquisa.
            # Not an orphan — surfaces in `noop` silently.
            continue
        # Every source in the group is technically orphan; report each so
        # the user can action them individually.
        for src in group:
            if src["source_id"] in captcha_source_ids:
                continue
            orphans.append({
                "source_id": src["source_id"],
                "title": src.get("title") or "",
                "url": src.get("url") or "",
                "derived_canonical_key": ck,
                "derivation_confidence": src.get("derivation_confidence"),
                "derivation_method": src.get("derivation_method"),
            })

    # --- Bucket: stale_manifest (bonus v1) ---
    # Manifest entry with status=ok but the source is not in NBM anymore.
    stale_manifest = []
    for ck, src in manifest_sources_by_ck.items():
        if src.get("status") != "ok":
            continue
        if ck in current_canonical_keys:
            continue
        # Also skip anything we already put in missing/retryable to avoid
        # acting twice (manifest may still consider it ok, but the expected
        # state says user WANTS it — those belong in missing/retryable).
        if ck in expected_canonical_keys:
            continue
        stale_manifest.append({
            "canonical_key": ck,
            "manifest_entry": src,
        })

    # Sources already in NBM AND in expected state AND no duplicate group →
    # no-op. Counted for the report summary. F1b: a canonical_key whose only
    # source is a captcha page does not count as conformant.
    noop_count = 0
    for ck in current_canonical_keys & expected_canonical_keys:
        group = by_canonical[ck]
        non_captcha = [s for s in group if s["source_id"] not in captcha_source_ids]
        if len(non_captcha) == 1:
            noop_count += 1

    return {
        "missing": missing,
        "retryable": retryable,
        "duplicates": duplicates,
        "captcha_page_disguised": captcha_page_disguised,
        "orphans": orphans,
        "stale_manifest": stale_manifest,
        "noop_count": noop_count,
        "totals": {
            "current_sources": len(current_sources),
            "expected_canonical_keys": len(expected_canonical_keys),
            "distinct_canonical_keys_current": len(current_canonical_keys),
        },
    }
