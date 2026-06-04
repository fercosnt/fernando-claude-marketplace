#!/usr/bin/env python3
"""Replays evals/test_scenarios.json against diff_engine.compute_diff().

Each scenario specifies inputs (current_sources + manifest_sources) and
expected counts per bucket. We synthesize a temp manifest, call the diff,
and assert counts match. Pure-function regression — no NotebookLM CLI.
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

from diff_engine import compute_diff  # noqa: E402


NOTEBOOK_ID = "fixture-nb"


def _fake_manifest(tmp_root: Path, manifest_sources: list[dict]) -> Path:
    path = tmp_root / "_notebook-manifest.json"
    data = {
        "version": 1,
        "notebooks": {
            NOTEBOOK_ID: {
                "title": "Fixture",
                "added_at": "2026-03-01T00:00:00+00:00",
                "updated_at": "2026-03-01T00:00:00+00:00",
                "sources": manifest_sources,
            }
        },
    }
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return path


_PASSED_SLUGS = {"p1"}


def _expected_state_from_manifest(manifest_sources: list[dict]) -> dict:
    """Use manifest entries as the expected state, but only those whose
    origin_pesquisa is in the passed-slug scope (mirrors what
    load_expected_from_pesquisas does in the real auditor).

    Entries from out-of-scope pesquisas (e.g. renamed_old_pesquisa) drop
    out of expected and become candidates for the stale_manifest bucket
    when NBM also doesn't have them.
    """
    expected: dict = {}
    for entry in manifest_sources:
        if entry.get("status") == "deleted":
            continue
        slug = entry.get("origin_pesquisa")
        if slug not in _PASSED_SLUGS:
            continue
        ck = entry["canonical_key"]
        expected[ck] = {
            "title": entry.get("title", ""),
            "type": entry.get("type", "article"),
            "origin_pesquisas": [slug],
            "manifest_entry": entry,
            "last_known_status": entry.get("status", "ok"),
            "signal_url": (entry.get("ingest_metadata") or {}).get("signal_url"),
        }
    return expected


def run_one(scenario: dict, tmp_root: Path) -> tuple[bool, list[str]]:
    inputs = scenario["inputs"]
    expected_diff = scenario["expected_diff"]
    manifest_sources = inputs.get("manifest_sources", [])
    current_sources = inputs["current_sources"]

    manifest_path = _fake_manifest(tmp_root, manifest_sources)
    expected_state = _expected_state_from_manifest(manifest_sources)

    diff = compute_diff(
        current_sources=current_sources,
        expected_sources=expected_state,
        manifest_path=manifest_path,
        notebook_id=NOTEBOOK_ID,
        max_retry=3,
    )

    failures: list[str] = []
    for key in ("missing", "retryable", "duplicates", "orphans", "stale_manifest"):
        got = len(diff.get(key, []))
        want = expected_diff.get(f"{key}_count", 0)
        if got != want:
            failures.append(f"{key}: got {got}, want {want}")

    want_noop = expected_diff.get("noop_count", 0)
    got_noop = diff.get("noop_count", 0)
    if got_noop != want_noop:
        failures.append(f"noop_count: got {got_noop}, want {want_noop}")

    if "duplicates_keep" in expected_diff and diff.get("duplicates"):
        keep = diff["duplicates"][0].get("keep")
        if keep != expected_diff["duplicates_keep"]:
            failures.append(f"duplicates_keep: got {keep}, want {expected_diff['duplicates_keep']}")

    return (not failures, failures)


def main() -> int:
    fixture_path = _HERE / "test_scenarios.json"
    fixtures = json.loads(fixture_path.read_text())["scenarios"]

    passed = 0
    failed = 0
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        for sc in fixtures:
            sub = td_path / f"sc-{sc['id']}"
            sub.mkdir()
            ok, fails = run_one(sc, sub)
            tag = "PASS" if ok else "FAIL"
            print(f"  [{tag}] #{sc['id']} {sc['name']}")
            if not ok:
                for f in fails:
                    print(f"        - {f}")
                failed += 1
            else:
                passed += 1

    print(f"\n{passed}/{passed + failed} fixtures passed.")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
