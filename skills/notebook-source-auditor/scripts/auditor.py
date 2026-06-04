#!/usr/bin/env python3
"""Main entry point for notebook-source-auditor.

Usage:
    python auditor.py \\
        --notebook <url_or_id> \\
        --pesquisas <path1>[,<path2>,...] \\
        [--dry-run | --apply] \\
        [--skip-orphans] [--skip-duplicates] \\
        [--interactive] [--max-retry N] \\
        [--audits-dir <path>]

Exits:
    0  success (diffs resolved OR dry-run listed them)
    2  invalid invocation (bad flags, notebook not reachable)
    3  partial — notebook absent from manifest (bootstrap recommended)
    4  apply-mode: at least one destructive action failed
    5  manifest lock / corruption / auth error
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# --- path plumbing: sibling scripts + deep-research helpers ---
_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

_DR_SCRIPTS = Path.home() / ".claude" / "skills" / "deep-research" / "scripts"
if str(_DR_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_DR_SCRIPTS))

import notebook_manifest as manifest  # noqa: E402

from url_extract import extract_notebook_id  # noqa: E402
from diff_engine import compute_diff, load_expected_from_pesquisas  # noqa: E402
from orphan_handler import handle_orphan  # noqa: E402
from report_writer import write_report  # noqa: E402
from captcha_patterns import filter_captcha_sources  # noqa: E402
from env_loader import boot as boot_env  # noqa: E402
from manifest_backup import create_backup, rollback_latest, write_log_event  # noqa: E402
from bootstrap import bootstrap_notebook  # noqa: E402


# F11 convergence guard: fix-captcha runs at most this many dedupe rounds
# after re-add before giving up. Observed in Phase 5: 2 rounds usually
# suffice; a 3rd catches corner cases where upload_to_nblm re-added both
# MD and PDF formats.
FIX_CAPTCHA_MAX_ROUNDS = 3


# F13: stderr prints get a no-op replacement when --quiet is active so
# launchd/cron invocations emit only the single-line summary JSON.
_QUIET = False


def _log(msg: str) -> None:
    """Stderr message gated on --quiet (F13). The ONLY channel cron/launchd
    parses is stdout JSON from `emit_summary`; everything else routes here
    so it vanishes when the user opts into quiet mode."""
    if not _QUIET:
        print(msg, file=sys.stderr)


# ---------------- CLI ----------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="notebook-source-auditor",
        description="Reconcile NotebookLM state with manifest and pesquisa folders.",
    )
    p.add_argument("--notebook", required=True, help="notebook URL or bare id")
    p.add_argument(
        "--pesquisas",
        required=True,
        help="comma-separated list of pesquisa folder paths",
    )
    # Dry-run is default TRUE in v1 per PRD. `--apply` flips it.
    p.add_argument("--dry-run", dest="dry_run", action="store_true", default=True)
    p.add_argument(
        "--apply",
        dest="dry_run",
        action="store_false",
        help="execute destructive actions (default: dry-run)",
    )
    p.add_argument("--skip-orphans", action="store_true")
    p.add_argument("--skip-duplicates", action="store_true")
    p.add_argument("--interactive", action="store_true")
    p.add_argument("--max-retry", type=int, default=3)
    p.add_argument(
        "--audits-dir",
        default=None,
        help="override default _audits/ location under pesquisas_root",
    )
    p.add_argument(
        "--fix-captcha",
        action="store_true",
        help="F7: composite mode — pull NBM, detect captcha-page sources via "
             "regex (captcha_patterns), bulk-delete, re-add their URLs via "
             "sci_fetch with --skip-dupe, then run dedupe up to "
             f"{FIX_CAPTCHA_MAX_ROUNDS} rounds. Requires --apply to execute; "
             "with --dry-run reports what would happen.",
    )
    p.add_argument(
        "--quiet",
        action="store_true",
        help="F13: suppress stderr progress and emit one JSON summary on "
             "stdout at the end. Designed for launchd/cron — the summary is "
             "machine-parseable and exit code stays informative.",
    )
    p.add_argument(
        "--bootstrap",
        action="store_true",
        help="F10: when the manifest has no entry for this notebook, "
             "populate it from the current NBM + pesquisa state instead of "
             "exiting 3. Bootstrapped sources are marked "
             "ingest_method=bootstrap_unknown so they never auto-retry "
             "without user confirmation.",
    )
    p.add_argument(
        "--rollback",
        action="store_true",
        help="F14: restore the most recent manifest snapshot and exit. "
             "Does NOT undo notebooklm source delete calls — the CLI has "
             "no undo. Re-adds that failed mid-run reappear as "
             "status=failed in the restored manifest.",
    )
    return p


# ---------------- NotebookLM I/O ----------------

class AuthError(Exception):
    pass


def list_notebook_sources(notebook_id: str) -> dict:
    """Pull current state from NotebookLM. Retries once on transient failure."""
    for attempt in (1, 2):
        result = subprocess.run(
            ["notebooklm", "source", "list", "-n", notebook_id, "--json"],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode == 0:
            try:
                data = json.loads(result.stdout)
            except json.JSONDecodeError as e:
                raise RuntimeError(f"CLI returned malformed JSON: {e}") from e
            return data
        stderr_lc = result.stderr.lower()
        if "authentication" in stderr_lc or "login" in stderr_lc:
            raise AuthError("Run: notebooklm login")
        if attempt == 2:
            raise RuntimeError(
                f"notebooklm source list failed (rc={result.returncode}): "
                f"{result.stderr.strip() or '(no stderr)'}"
            )


def _cli_add_url(notebook_id: str, url: str) -> dict:
    result = subprocess.run(
        ["notebooklm", "source", "add", url, "-n", notebook_id, "--json"],
        capture_output=True, text=True, timeout=60,
    )
    if result.returncode != 0:
        return {"ok": False, "error": result.stderr.strip() or "non-zero exit"}
    try:
        payload = json.loads(result.stdout) if result.stdout.strip() else {}
    except json.JSONDecodeError:
        payload = {}
    return {"ok": True, "source_id": payload.get("id") or payload.get("source_id")}


def _cli_add_file(notebook_id: str, file_path: Path) -> dict:
    result = subprocess.run(
        ["notebooklm", "source", "add", str(file_path), "-n", notebook_id, "--json"],
        capture_output=True, text=True, timeout=120,
    )
    if result.returncode != 0:
        return {"ok": False, "error": result.stderr.strip() or "non-zero exit"}
    try:
        payload = json.loads(result.stdout) if result.stdout.strip() else {}
    except json.JSONDecodeError:
        payload = {}
    return {"ok": True, "source_id": payload.get("id") or payload.get("source_id")}


def _cli_delete(notebook_id: str, source_id: str) -> bool:
    result = subprocess.run(
        ["notebooklm", "source", "delete", source_id, "-n", notebook_id, "-y"],
        capture_output=True, text=True, timeout=30,
    )
    return result.returncode == 0


# ---------------- Resolvers ----------------

def resolve_missing(
    *,
    missing: list[dict],
    notebook_id: str,
    pesquisas_root: Path,
    dry_run: bool,
) -> dict:
    """Delegate missing sources to sci_fetch/upload_to_nblm.py, one call per
    pesquisa slug (upload_to_nblm requires a single slug per invocation)."""
    results = []
    manual_required = []
    if not missing:
        return {"results": results, "summary_note": "0 items", "manual_required": manual_required}

    # Group URLs/canonical_keys by their first origin_pesquisa so we can
    # invoke upload_to_nblm.py per slug.
    by_slug: dict[str, list[dict]] = {}
    for item in missing:
        expected = item["expected"]
        origins = expected.get("origin_pesquisas") or []
        slug = origins[0] if origins else "unknown"
        by_slug.setdefault(slug, []).append(item)

    if dry_run:
        for slug, items in by_slug.items():
            for it in items:
                results.append({
                    "canonical_key": it["canonical_key"],
                    "status": f"dry-run: would delegate to sci_fetch (pesquisa={slug})",
                })
        return {"results": results, "summary_note": f"dry-run: {len(missing)} would be delegated",
                "manual_required": manual_required}

    upload_script = _DR_SCRIPTS / "sci_fetch" / "upload_to_nblm.py"
    if not upload_script.exists():
        for it in missing:
            results.append({"canonical_key": it["canonical_key"], "status": "error: upload_to_nblm.py missing"})
        return {"results": results, "summary_note": "upload script missing", "manual_required": manual_required}

    for slug, items in by_slug.items():
        urls = []
        for it in items:
            expected = it["expected"]
            signal = expected.get("signal_url")
            manifest_entry = expected.get("manifest_entry") or {}
            ingest_md = manifest_entry.get("ingest_metadata") or {}
            url = signal or manifest_entry.get("url") or ingest_md.get("signal_url")
            if url:
                urls.append((it["canonical_key"], url))
            else:
                manual_required.append({
                    "canonical_key": it["canonical_key"],
                    "reason": "missing_url",
                    "instruction": "Add URL to the pesquisa or the manifest entry, then re-run.",
                })

        if not urls:
            continue

        tmp = Path(f"/tmp/auditor-missing-{notebook_id}-{slug}.txt")
        tmp.write_text("\n".join(u for _, u in urls), encoding="utf-8")

        proc = subprocess.run(
            [
                sys.executable,
                str(upload_script),
                "--urls", str(tmp),
                "--notebook", notebook_id,
                "--pesquisa", slug,
                "--pesquisas-root", str(pesquisas_root),
                "--from-auditor",
            ],
            capture_output=True, text=True, timeout=600,
        )

        if proc.returncode != 0:
            for ck, _ in urls:
                results.append({"canonical_key": ck, "status": f"error: sci_fetch rc={proc.returncode}"})
            continue

        # sci_fetch writes the manifest itself; we just record the outcome.
        for ck, _ in urls:
            results.append({"canonical_key": ck, "status": "delegated_to_sci_fetch"})

    return {
        "results": results,
        "summary_note": f"{len(results)} delegated",
        "manual_required": manual_required,
    }


def resolve_retryable(
    *,
    retryable: list[dict],
    notebook_id: str,
    manifest_path: Path,
    pesquisas_root: Path,
    dry_run: bool,
) -> dict:
    results = []
    manual_required = []
    for item in retryable:
        ck = item["canonical_key"]
        entry = item["manifest_entry"]
        method = item["ingest_method"]

        if dry_run:
            results.append({"canonical_key": ck, "status": f"dry-run: would retry via {method}"})
            continue

        if method == "url_direct":
            url = (entry.get("ingest_metadata") or {}).get("signal_url") or entry.get("url")
            if not url:
                manual_required.append({
                    "canonical_key": ck,
                    "reason": "url_direct missing URL in manifest",
                    "instruction": "Delete the manifest entry and re-add via deep-research.",
                })
                results.append({"canonical_key": ck, "status": "skipped_no_url"})
                continue
            out = _cli_add_url(notebook_id, url)
        elif method == "pdf_upload":
            pdf_path_str = (entry.get("ingest_metadata") or {}).get("pdf_local_path")
            pdf_path = Path(pdf_path_str) if pdf_path_str else None
            if not pdf_path or not pdf_path.exists():
                manifest.record_source(
                    manifest_path=manifest_path,
                    notebook_id=notebook_id,
                    pesquisa_slug=entry.get("origin_pesquisa") or "unknown",
                    pesquisas_root=pesquisas_root,
                    canonical_key=ck,
                    title=entry.get("title") or "",
                    source_type=entry.get("type") or "article",
                    origin_pesquisa=entry.get("origin_pesquisa") or "unknown",
                    status="failed",
                    ingest_method=method,
                    error="pdf_not_found",
                )
                results.append({"canonical_key": ck, "status": "failed_pdf_not_found"})
                continue
            out = _cli_add_file(notebook_id, pdf_path)
        else:
            results.append({"canonical_key": ck, "status": f"skipped_method:{method}"})
            continue

        if out.get("ok"):
            manifest.record_source(
                manifest_path=manifest_path,
                notebook_id=notebook_id,
                pesquisa_slug=entry.get("origin_pesquisa") or "unknown",
                pesquisas_root=pesquisas_root,
                canonical_key=ck,
                title=entry.get("title") or "",
                source_type=entry.get("type") or "article",
                origin_pesquisa=entry.get("origin_pesquisa") or "unknown",
                status="ok",
                notebooklm_source_id=out.get("source_id"),
                ingest_method=method,
            )
            results.append({"canonical_key": ck, "status": "ok"})
        else:
            manifest.record_source(
                manifest_path=manifest_path,
                notebook_id=notebook_id,
                pesquisa_slug=entry.get("origin_pesquisa") or "unknown",
                pesquisas_root=pesquisas_root,
                canonical_key=ck,
                title=entry.get("title") or "",
                source_type=entry.get("type") or "article",
                origin_pesquisa=entry.get("origin_pesquisa") or "unknown",
                status="failed",
                ingest_method=method,
                error=out.get("error"),
            )
            results.append({"canonical_key": ck, "status": f"failed:{out.get('error', '')[:40]}"})

    return {"results": results, "summary_note": f"{len(results)} processed", "manual_required": manual_required}


def resolve_duplicates(
    *,
    duplicates: list[dict],
    notebook_id: str,
    manifest_path: Path,
    dry_run: bool,
) -> tuple[dict, bool]:
    """Returns (result_dict, any_failure_bool)."""
    results = []
    any_failure = False
    for grp in duplicates:
        ck = grp["canonical_key"]
        to_delete = grp.get("delete", [])

        if dry_run:
            results.append({
                "canonical_key": ck,
                "status": f"dry-run: would delete {len(to_delete)} source(s), keep {grp.get('keep')}",
            })
            continue

        all_ok = True
        for sid in to_delete:
            if not _cli_delete(notebook_id, sid):
                all_ok = False

        if all_ok:
            manifest.mark_deleted(
                manifest_path=manifest_path,
                notebook_id=notebook_id,
                canonical_key=ck,
                reason=f"duplicate_of:{grp.get('keep')}",
            )
            results.append({"canonical_key": ck, "status": "merged"})
        else:
            any_failure = True
            results.append({"canonical_key": ck, "status": "partial_failure"})

    return ({"results": results, "summary_note": f"{len(results)} groups"}, any_failure)


def resolve_stale_manifest(
    *,
    stale: list[dict],
    notebook_id: str,
    manifest_path: Path,
    dry_run: bool,
) -> dict:
    results = []
    for item in stale:
        ck = item["canonical_key"]
        if dry_run:
            results.append({"canonical_key": ck, "status": "dry-run: would mark deleted"})
            continue
        updated = manifest.mark_deleted(
            manifest_path=manifest_path,
            notebook_id=notebook_id,
            canonical_key=ck,
            reason="deleted_from_nbm_externally",
        )
        results.append({
            "canonical_key": ck,
            "status": "marked_deleted" if updated else "not_found_in_manifest",
        })
    return {"results": results, "summary_note": f"{len(results)} processed"}


def resolve_captcha_page_disguised(
    *,
    items: list[dict],
    notebook_id: str,
    manifest_path: Path,
    pesquisas_root: Path,
    pesquisa_slugs: list[str],
    dry_run: bool,
) -> tuple[dict, bool]:
    """F1b: delete each captcha page and re-add its URL via sci_fetch.

    Mirrors the F7 steps 2–3 (delete + readd) without the convergence loop —
    the standard audit only handles first-pass detection. Users who want
    dedupe-until-converged should invoke `--fix-captcha` explicitly.

    Returns (result_dict, any_failure_bool).

    Manifest history: if the captcha source's canonical_key exists in the
    manifest, we call mark_deleted(reason=captcha_page_detected). If it
    does not (the common case: the deep-research never registered it
    because it thought the add had failed), we only delete from the NBM —
    there is nothing to mark.
    """
    results: list[dict] = []
    any_failure = False

    if not items:
        return ({"results": results, "summary_note": "0 items"}, False)

    if dry_run:
        for it in items:
            results.append({
                "source_id": it["source_id"],
                "status": "dry-run: would delete + re-add via sci_fetch",
            })
        return (
            {"results": results, "summary_note": f"dry-run: {len(items)} would be delete+readd"},
            False,
        )

    # Step 1: delete each captcha source from the NBM.
    urls_to_readd: list[str] = []
    for it in items:
        sid = it["source_id"]
        url = (it.get("url") or "").strip()
        ok = _cli_delete(notebook_id, sid)
        if not ok:
            any_failure = True
            results.append({"source_id": sid, "status": "delete_failed"})
            continue

        # Step 1b: mark manifest history when possible. `in_manifest=True`
        # means the manifest already knew about this canonical_key, so
        # flipping status to `deleted` preserves audit history.
        ck = it.get("derived_canonical_key")
        if it.get("in_manifest") and ck:
            manifest.mark_deleted(
                manifest_path=manifest_path,
                notebook_id=notebook_id,
                canonical_key=ck,
                reason="captcha_page_detected",
            )

        if url:
            urls_to_readd.append(url)
        results.append({"source_id": sid, "status": "deleted"})

    # Step 2: re-add the surviving URLs via sci_fetch (--skip-dupe guards
    # against re-introducing anything the NBM still has).
    if urls_to_readd and pesquisa_slugs:
        slug = pesquisa_slugs[0]
        readd = _delegate_sci_fetch(
            urls=urls_to_readd,
            notebook_id=notebook_id,
            pesquisa_slug=slug,
            pesquisas_root=pesquisas_root,
            skip_dupe=True,
        )
        if not readd.get("ok"):
            any_failure = True
            results.append({
                "source_id": "(batch)",
                "status": f"readd_failed: {readd.get('error', '')[:80]}",
            })
        else:
            results.append({
                "source_id": "(batch)",
                "status": (
                    f"readd_summary: uploaded={readd.get('auto_uploaded', 0)}, "
                    f"manual={readd.get('manual_required', 0)}, "
                    f"skipped_dupe={readd.get('skipped_duplicate', 0)}"
                ),
            })

    return (
        {"results": results, "summary_note": f"{len(items)} processed"},
        any_failure,
    )


def resolve_orphans(
    *,
    orphans: list[dict],
    notebook_id: str,
    manifest_path: Path,
    pesquisas_root: Path,
    pesquisa_slugs: list[str],
    interactive: bool,
    dry_run: bool,
) -> dict:
    results = []
    if not interactive:
        for orph in orphans:
            results.append({"source_id": orph["source_id"], "action": "listed_only"})
        return {"results": results, "summary_note": f"{len(results)} listed (non-interactive)"}

    # Interactive path — prompt per orphan.
    for orph in orphans:
        decision = handle_orphan(
            orphan=orph,
            notebook_id=notebook_id,
            pesquisa_slugs=pesquisa_slugs,
            pesquisas_root=pesquisas_root,
            manifest_path=manifest_path,
            dry_run=dry_run,
        )
        results.append({"source_id": orph["source_id"], **decision})
    return {"results": results, "summary_note": f"{len(results)} interactively reviewed"}


# ---------------- Orchestration ----------------

def collect_manual_required(diff: dict) -> list[dict]:
    """captcha_bypass_flow_v1 retries from the manifest that the auditor
    refuses to automate. Reported in the audit as `manual required`."""
    manual = []
    for item in diff.get("retryable", []):
        if item.get("ingest_method") == "captcha_bypass_flow_v1":
            manual.append({
                "canonical_key": item["canonical_key"],
                "reason": "captcha_bypass_flow_v1",
                "instruction": "Open URL → download PDF → drag into the notebook via the UI.",
            })
    return manual


def _delegate_sci_fetch(
    *,
    urls: list[str],
    notebook_id: str,
    pesquisa_slug: str,
    pesquisas_root: Path,
    skip_dupe: bool = True,
    timeout: int = 900,
) -> dict:
    """Write URLs to a temp file and invoke upload_to_nblm.py.

    F7 uses this to re-add captcha URLs after delete; the upload_to_nblm
    script writes the manifest itself (single source of truth). skip_dupe=True
    triggers F8 inside the upload script — a second F7 run on the same NBM
    adds zero sources because everything is already present.
    """
    upload_script = _DR_SCRIPTS / "sci_fetch" / "upload_to_nblm.py"
    if not upload_script.exists():
        return {"ok": False, "error": f"upload_to_nblm.py missing at {upload_script}"}

    tmp = Path(f"/tmp/auditor-fix-captcha-{notebook_id}-{pesquisa_slug}.txt")
    tmp.write_text("\n".join(urls), encoding="utf-8")
    cmd = [
        sys.executable, str(upload_script),
        "--urls", str(tmp),
        "--notebook", notebook_id,
        "--pesquisa", pesquisa_slug,
        "--pesquisas-root", str(pesquisas_root),
        "--from-auditor",
    ]
    if skip_dupe:
        cmd.append("--skip-dupe")
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if proc.returncode != 0:
        return {"ok": False, "error": f"sci_fetch rc={proc.returncode}: {proc.stderr.strip()[:400]}"}
    try:
        summary = json.loads(proc.stdout) if proc.stdout.strip() else {}
    except json.JSONDecodeError:
        summary = {"raw_stdout": proc.stdout[:400]}
    summary["ok"] = True
    return summary


def _dedupe_one_round(
    *,
    notebook_id: str,
    manifest_path: Path,
    pesquisas_paths: list[Path],
    max_retry: int,
    dry_run: bool,
) -> tuple[int, int]:
    """Run a single dedupe round. Returns (groups_detected, groups_merged)."""
    try:
        nbm = list_notebook_sources(notebook_id)
    except Exception as e:  # noqa: BLE001
        print(f"[warn] dedupe round: list_notebook_sources failed: {e}", file=sys.stderr)
        return (0, 0)
    current = nbm.get("sources") or nbm.get("data") or []
    expected = load_expected_from_pesquisas(
        pesquisas_paths=pesquisas_paths,
        manifest_path=manifest_path,
        notebook_id=notebook_id,
    )
    diff = compute_diff(
        current_sources=current,
        expected_sources=expected,
        manifest_path=manifest_path,
        notebook_id=notebook_id,
        max_retry=max_retry,
    )
    groups = diff.get("duplicates", [])
    if dry_run:
        return (len(groups), 0)
    _action, any_failure = resolve_duplicates(
        duplicates=groups,
        notebook_id=notebook_id,
        manifest_path=manifest_path,
        dry_run=False,
    )
    merged = sum(1 for r in _action["results"] if r["status"] == "merged")
    if any_failure:
        print("[warn] dedupe round had partial failures", file=sys.stderr)
    return (len(groups), merged)


def run_fix_captcha(
    *,
    notebook_id: str,
    notebook_title: str,
    pesquisas_paths: list[Path],
    pesquisas_root: Path,
    pesquisa_slugs: list[str],
    manifest_path: Path,
    audits_dir: Path,
    current_sources: list[dict],
    dry_run: bool,
    max_retry: int,
    max_rounds: int = FIX_CAPTCHA_MAX_ROUNDS,
) -> tuple[int, dict]:
    """F7 composite mode. Returns (exit_code, report_dict).

    Steps (skipped in dry-run after detection):
        1. Detect captcha-page sources via F15 regex on current NBM state
        2. Bulk-delete them via notebooklm CLI
        3. Re-add their URLs via sci_fetch/upload_to_nblm.py --skip-dupe
        4. Run dedupe rounds until convergence (F11: max_rounds cap)
        5. Write audit report at _audits/<nb>-fix-captcha-<date>.md
    """
    detected = filter_captcha_sources(current_sources)
    report: dict[str, Any] = {
        "mode": "dry-run" if dry_run else "apply",
        "detected_count": len(detected),
        "detected": [
            {"source_id": s.get("id"), "title": s.get("title", ""), "url": s.get("url", "")}
            for s in detected
        ],
        "deletions": [],
        "readd_summary": None,
        "dedupe_rounds": [],
        "converged": None,
    }
    print(f"[fix-captcha] detected {len(detected)} captcha-page source(s)", file=sys.stderr)

    if not detected:
        report["converged"] = True
        _write_fix_captcha_report(
            notebook_id=notebook_id, notebook_title=notebook_title,
            pesquisa_slugs=pesquisa_slugs, report=report, audits_dir=audits_dir,
        )
        return (0, report)

    if dry_run:
        print(
            f"[fix-captcha] dry-run: would delete {len(detected)}, "
            f"re-add via sci_fetch (skip-dupe), and dedupe up to {max_rounds} rounds",
            file=sys.stderr,
        )
        _write_fix_captcha_report(
            notebook_id=notebook_id, notebook_title=notebook_title,
            pesquisa_slugs=pesquisa_slugs, report=report, audits_dir=audits_dir,
        )
        return (0, report)

    # Step 2: delete. Any failure here counts as a destructive-action failure.
    deletion_failures = 0
    urls_to_readd: list[str] = []
    for src in detected:
        sid = src.get("id")
        url = (src.get("url") or "").strip()
        if not sid:
            continue
        ok = _cli_delete(notebook_id, sid)
        report["deletions"].append({"source_id": sid, "url": url, "ok": ok})
        if ok and url:
            urls_to_readd.append(url)
        elif not ok:
            deletion_failures += 1
    print(
        f"[fix-captcha] deleted {len(report['deletions']) - deletion_failures}/{len(detected)} "
        f"({deletion_failures} failed)",
        file=sys.stderr,
    )

    # Step 3: re-add. Use the first pesquisa slug as the upload target — this
    # is the same convention the `missing` resolver uses. F8 skip-dupe prevents
    # re-introducing anything the NBM still has.
    if urls_to_readd:
        slug = pesquisa_slugs[0]
        print(f"[fix-captcha] re-adding {len(urls_to_readd)} URL(s) via sci_fetch (slug={slug})", file=sys.stderr)
        readd = _delegate_sci_fetch(
            urls=urls_to_readd,
            notebook_id=notebook_id,
            pesquisa_slug=slug,
            pesquisas_root=pesquisas_root,
            skip_dupe=True,
        )
        report["readd_summary"] = readd
        if not readd.get("ok"):
            print(f"[fix-captcha] sci_fetch failed: {readd.get('error')}", file=sys.stderr)

    # Step 4: F11 convergence guard — up to max_rounds of dedupe until a
    # round finds zero duplicate groups.
    for round_idx in range(1, max_rounds + 1):
        detected_groups, merged = _dedupe_one_round(
            notebook_id=notebook_id,
            manifest_path=manifest_path,
            pesquisas_paths=pesquisas_paths,
            max_retry=max_retry,
            dry_run=False,
        )
        report["dedupe_rounds"].append({
            "round": round_idx,
            "detected_groups": detected_groups,
            "merged": merged,
        })
        print(
            f"[fix-captcha] dedupe round {round_idx}: "
            f"{detected_groups} group(s) detected, {merged} merged",
            file=sys.stderr,
        )
        if detected_groups == 0:
            report["converged"] = True
            break
    else:
        report["converged"] = False
        print(
            f"[error] did not converge after {max_rounds} rounds: "
            f"{report['dedupe_rounds'][-1]['detected_groups']} residual duplicate group(s)",
            file=sys.stderr,
        )

    # Step 5: write report. Exit non-zero when destructive actions failed or
    # convergence guard tripped.
    _write_fix_captcha_report(
        notebook_id=notebook_id, notebook_title=notebook_title,
        pesquisa_slugs=pesquisa_slugs, report=report, audits_dir=audits_dir,
    )
    if deletion_failures:
        return (4, report)
    if report["converged"] is False:
        return (4, report)
    return (0, report)


def _write_fix_captcha_report(
    *,
    notebook_id: str,
    notebook_title: str,
    pesquisa_slugs: list[str],
    report: dict,
    audits_dir: Path,
) -> Path:
    audits_dir.mkdir(parents=True, exist_ok=True)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    md_path = audits_dir / f"{notebook_id}-fix-captcha-{today}.md"
    lines: list[str] = []
    lines.append(f"# Fix-captcha report — {notebook_title}")
    lines.append("")
    lines.append(f"- Notebook ID: `{notebook_id}`")
    lines.append(f"- Mode: `{report['mode']}`")
    lines.append(f"- Pesquisas: {', '.join(pesquisa_slugs)}")
    lines.append(f"- Captcha-pages detected: **{report['detected_count']}**")
    if report["mode"] == "apply":
        deleted = sum(1 for d in report.get("deletions", []) if d["ok"])
        lines.append(f"- Deleted: **{deleted}/{report['detected_count']}**")
        if report.get("readd_summary"):
            rs = report["readd_summary"]
            lines.append(
                f"- Re-added via sci_fetch: auto_uploaded={rs.get('auto_uploaded', 0)}, "
                f"manual_required={rs.get('manual_required', 0)}, "
                f"skipped_duplicate={rs.get('skipped_duplicate', 0)}"
            )
        rounds = report.get("dedupe_rounds", [])
        if rounds:
            lines.append("")
            lines.append("## Dedupe rounds")
            for r in rounds:
                lines.append(f"- Round {r['round']}: detected={r['detected_groups']}, merged={r['merged']}")
        lines.append("")
        lines.append(f"- Converged: **{report['converged']}**")
    if report["detected"]:
        lines.append("")
        lines.append("## Detected captcha-page sources")
        for d in report["detected"]:
            lines.append(f"- `{d['source_id']}` — {d['title'][:80]}  ({d['url']})")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    json_path = audits_dir / "raw" / f"{notebook_id}-fix-captcha-{today}.json"
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[ok] fix-captcha report: {md_path}", file=sys.stderr)
    return md_path


def emit_summary(summary: dict) -> None:
    """F13: stdout is the machine channel. Print a single JSON line so
    launchd/cron can pipe it to a log dashboard or a watchdog script."""
    print(json.dumps(summary, ensure_ascii=False), flush=True)


def run(argv: list[str] | None = None) -> int:
    # F9: merge ~/.claude/skills/notebook-source-auditor/.env into os.environ
    # before any subprocess spawns, so NCBI/Unpaywall/OpenAlex keys reach
    # the sci_fetch delegate. Shell exports still win (override=False).
    boot_env()

    args = build_parser().parse_args(argv)
    global _QUIET
    _QUIET = bool(getattr(args, "quiet", False))

    # --- Resolve notebook id ---
    try:
        notebook_id = extract_notebook_id(args.notebook)
    except ValueError as e:
        print(f"[error] {e}", file=sys.stderr)
        return 2

    # --- Resolve pesquisas paths ---
    # F10a bootstrap w/ empty pesquisas: `--bootstrap` is allowed with an
    # empty --pesquisas because the user may want to snapshot the current
    # NBM into the manifest without any expected state. That is rare but
    # useful when first registering a legacy notebook. When --bootstrap is
    # NOT set, we still require at least one pesquisa (same as Fase A/B).
    pesquisas_paths = [Path(p.strip()) for p in args.pesquisas.split(",") if p.strip()]
    if not pesquisas_paths and not getattr(args, "bootstrap", False):
        print("[error] --pesquisas must include at least one path", file=sys.stderr)
        return 2
    for path in pesquisas_paths:
        if not path.exists():
            print(f"[error] pesquisa path does not exist: {path}", file=sys.stderr)
            return 2
        if path.is_dir() and not any(path.glob("PESQUISA-*.md")) and not any(path.glob("*.md")):
            _log(
                f"[warn] pesquisa folder has no .md files: {path} "
                f"— continuing but expected state will rely on manifest only"
            )

    # Derive common parent (pesquisas_root). For folders we use the parent;
    # for direct .md file paths we use the file's parent (so the manifest
    # lives next to the file). All paths must resolve to the same root —
    # otherwise the manifest they share would differ.
    def _root_of(p: Path) -> Path:
        rp = p.resolve()
        return rp.parent if rp.is_file() else rp.parent
    if pesquisas_paths:
        parents = {_root_of(p) for p in pesquisas_paths}
        if len(parents) != 1:
            print(
                "[error] all pesquisas must live under the same parent directory "
                "(for a shared manifest). Got: "
                + ", ".join(str(p) for p in parents),
                file=sys.stderr,
            )
            return 2
        pesquisas_root = next(iter(parents))
    else:
        # F10 empty-pesquisa bootstrap: default manifest root to the skill's
        # logs dir so the bootstrap output has a home. User can override via
        # --audits-dir or by passing a single pesquisa with the desired root.
        pesquisas_root = _HERE.parent
    manifest_path = pesquisas_root / "_notebook-manifest.json"
    audits_dir = Path(args.audits_dir) if args.audits_dir else pesquisas_root / "_audits"
    logs_dir = _HERE.parent / "logs"
    # Slug = folder name OR file stem (so "hashimoto-reference.md" → "hashimoto-reference").
    pesquisa_slugs = [
        (p.stem if p.is_file() else p.name) for p in pesquisas_paths
    ]

    # F14 --rollback: short-circuit before any destructive work. We only
    # need `manifest_path` resolved to act; the pesquisa validation above
    # stays in place so users get a clear error if they pass garbage.
    if getattr(args, "rollback", False):
        restored = rollback_latest(manifest_path)
        if restored is None:
            print(
                f"[error] no backups found for {manifest_path.name} under {manifest_path.parent}",
                file=sys.stderr,
            )
            return 2
        _log(f"[ok] restored manifest from {restored.name}")
        _log(
            "[info] NotebookLM source deletions are NOT reversed by "
            "rollback; re-adds failing mid-run reappear as status=failed "
            "on next audit."
        )
        write_log_event(logs_dir, {
            "event": "rollback",
            "notebook_id": notebook_id,
            "restored_from": restored.name,
        })
        if _QUIET:
            emit_summary({
                "event": "rollback",
                "notebook_id": notebook_id,
                "restored_from": restored.name,
                "exit_code": 0,
            })
        return 0

    mode = "dry-run" if args.dry_run else "apply"
    _log(f"[info] notebook={notebook_id} mode={mode} pesquisas={pesquisa_slugs}")

    # --- Pull current state ---
    try:
        nbm = list_notebook_sources(notebook_id)
    except AuthError as e:
        print(f"[error] {e}", file=sys.stderr)
        return 5
    except Exception as e:  # noqa: BLE001
        print(f"[error] {e}", file=sys.stderr)
        return 2
    current_sources = nbm.get("sources") or nbm.get("data") or []
    notebook_title = nbm.get("title") or nbm.get("notebook_title") or notebook_id

    # --- Build expected state ---
    # F10: if the user opted into --bootstrap, seed the manifest from the
    # current NBM + pesquisa state and exit 0 BEFORE the diff/resolver
    # pipeline. Bootstrap is deliberately a separate mode — mixing it with
    # a destructive audit could delete sources the user meant to keep.
    if getattr(args, "bootstrap", False):
        summary = bootstrap_notebook(
            manifest_path=manifest_path,
            notebook_id=notebook_id,
            notebook_title=notebook_title,
            current_sources=current_sources,
            pesquisas_paths=pesquisas_paths,
            pesquisas_root=pesquisas_root,
            pesquisa_slugs=pesquisa_slugs,
            dry_run=args.dry_run,
        )
        _log(
            f"[bootstrap] {summary['created']} entry/entries created, "
            f"{summary['skipped_existing']} already present, "
            f"{summary['low_confidence']} low-confidence source(s)"
        )
        if not args.dry_run:
            write_log_event(logs_dir, {
                "event": "bootstrap",
                "notebook_id": notebook_id,
                "created": summary["created"],
                "skipped_existing": summary["skipped_existing"],
                "low_confidence": summary["low_confidence"],
            })
        if _QUIET:
            emit_summary({
                "event": "bootstrap",
                "notebook_id": notebook_id,
                "mode": "dry-run" if args.dry_run else "apply",
                "created": summary["created"],
                "skipped_existing": summary["skipped_existing"],
                "low_confidence": summary["low_confidence"],
                "exit_code": 0,
            })
        return 0

    partial_bootstrap = False
    if not manifest_path.exists():
        _log(
            f"[info] manifest absent at {manifest_path} — "
            f"missing bucket will be empty; bootstrap recommended (pass --bootstrap)."
        )
        # Create an empty manifest so lock helpers can run.
        manifest_path.write_text('{"version": 1, "notebooks": {}}', encoding="utf-8")
        partial_bootstrap = True

    # F14: snapshot the manifest right before anything destructive runs.
    # We skip backup in dry-run because nothing will mutate the manifest —
    # a backup would just clutter the directory.
    backup_path: Path | None = None
    if not args.dry_run and manifest_path.exists():
        try:
            backup_path = create_backup(manifest_path)
            if backup_path:
                _log(f"[backup] snapshot: {backup_path.name}")
        except OSError as e:
            # Not fatal — but the user deserves to know their safety net
            # is missing for this run.
            _log(f"[warn] could not snapshot manifest: {e}")

    # --- F7 fix-captcha composite mode branches here — independent of the
    #     standard 5-bucket flow because its bucket semantics differ (the
    #     captcha sources are deliberately deleted, not kept as orphans). ---
    if getattr(args, "fix_captcha", False):
        exit_code, _report = run_fix_captcha(
            notebook_id=notebook_id,
            notebook_title=notebook_title,
            pesquisas_paths=pesquisas_paths,
            pesquisas_root=pesquisas_root,
            pesquisa_slugs=pesquisa_slugs,
            manifest_path=manifest_path,
            audits_dir=audits_dir,
            current_sources=current_sources,
            dry_run=args.dry_run,
            max_retry=args.max_retry,
        )
        if not args.dry_run:
            write_log_event(logs_dir, {
                "event": "fix_captcha",
                "notebook_id": notebook_id,
                "detected": len(_report.get("detected", [])),
                "converged": _report.get("converged"),
                "exit_code": exit_code,
                "backup": backup_path.name if backup_path else None,
            })
        if _QUIET:
            emit_summary({
                "event": "fix_captcha",
                "notebook_id": notebook_id,
                "mode": "dry-run" if args.dry_run else "apply",
                "detected": len(_report.get("detected", [])),
                "converged": _report.get("converged"),
                "exit_code": exit_code,
            })
        return exit_code

    expected = load_expected_from_pesquisas(
        pesquisas_paths=pesquisas_paths,
        manifest_path=manifest_path,
        notebook_id=notebook_id,
    )

    # --- Compute diff ---
    diff = compute_diff(
        current_sources=current_sources,
        expected_sources=expected,
        manifest_path=manifest_path,
        notebook_id=notebook_id,
        max_retry=args.max_retry,
    )

    if args.skip_duplicates:
        diff["duplicates"] = []
    if args.skip_orphans:
        diff["orphans"] = []

    # Print a compact summary to stderr so the user sees progress.
    _log(
        f"[diff] missing={len(diff['missing'])} retryable={len(diff['retryable'])} "
        f"duplicates={len(diff['duplicates'])} "
        f"captcha_page_disguised={len(diff.get('captcha_page_disguised', []))} "
        f"orphans={len(diff['orphans'])} "
        f"stale_manifest={len(diff['stale_manifest'])} noop={diff['noop_count']}"
    )

    # --- Apply resolvers ---
    actions: dict[str, Any] = {}
    any_failure = False

    missing_action = resolve_missing(
        missing=diff["missing"],
        notebook_id=notebook_id,
        pesquisas_root=pesquisas_root,
        dry_run=args.dry_run,
    )
    actions["missing"] = missing_action

    retryable_action = resolve_retryable(
        retryable=[i for i in diff["retryable"] if i.get("ingest_method") != "captcha_bypass_flow_v1"],
        notebook_id=notebook_id,
        manifest_path=manifest_path,
        pesquisas_root=pesquisas_root,
        dry_run=args.dry_run,
    )
    actions["retryable"] = retryable_action

    duplicates_action, dup_failed = resolve_duplicates(
        duplicates=diff["duplicates"],
        notebook_id=notebook_id,
        manifest_path=manifest_path,
        dry_run=args.dry_run,
    )
    actions["duplicates"] = duplicates_action
    any_failure = any_failure or dup_failed

    stale_action = resolve_stale_manifest(
        stale=diff["stale_manifest"],
        notebook_id=notebook_id,
        manifest_path=manifest_path,
        dry_run=args.dry_run,
    )
    actions["stale_manifest"] = stale_action

    captcha_action, captcha_failed = resolve_captcha_page_disguised(
        items=diff.get("captcha_page_disguised", []),
        notebook_id=notebook_id,
        manifest_path=manifest_path,
        pesquisas_root=pesquisas_root,
        pesquisa_slugs=pesquisa_slugs,
        dry_run=args.dry_run,
    )
    actions["captcha_page_disguised"] = captcha_action
    any_failure = any_failure or captcha_failed

    orphans_action = resolve_orphans(
        orphans=diff["orphans"],
        notebook_id=notebook_id,
        manifest_path=manifest_path,
        pesquisas_root=pesquisas_root,
        pesquisa_slugs=pesquisa_slugs,
        interactive=args.interactive,
        dry_run=args.dry_run,
    )
    actions["orphans"] = orphans_action

    manual = collect_manual_required(diff)
    manual.extend(missing_action.get("manual_required", []))
    manual.extend(retryable_action.get("manual_required", []))
    actions["manual_required"] = manual

    # --- Write report ---
    paths = write_report(
        notebook_id=notebook_id,
        notebook_title=notebook_title,
        pesquisa_slugs=pesquisa_slugs,
        diff=diff,
        actions=actions,
        mode=mode,
        audits_dir=audits_dir,
    )
    _log(f"[ok] report: {paths['md']}")

    if partial_bootstrap:
        exit_code = 3
    elif any_failure and not args.dry_run:
        exit_code = 4
    else:
        exit_code = 0

    # F14: structured event log for dashboards/cron. Dry-run logs are
    # suppressed — they would double the log volume without useful signal.
    if not args.dry_run:
        write_log_event(logs_dir, {
            "event": "audit",
            "notebook_id": notebook_id,
            "mode": mode,
            "diff": {
                "missing": len(diff["missing"]),
                "retryable": len(diff["retryable"]),
                "duplicates": len(diff["duplicates"]),
                "captcha_page_disguised": len(diff.get("captcha_page_disguised", [])),
                "orphans": len(diff["orphans"]),
                "stale_manifest": len(diff["stale_manifest"]),
                "noop": diff["noop_count"],
            },
            "exit_code": exit_code,
            "backup": backup_path.name if backup_path else None,
        })

    # F13: cron/launchd summary — stdout JSON with the metrics a scheduler
    # can alert on.
    if _QUIET:
        emit_summary({
            "event": "audit",
            "notebook_id": notebook_id,
            "mode": mode,
            "diff": {
                "missing": len(diff["missing"]),
                "retryable": len(diff["retryable"]),
                "duplicates": len(diff["duplicates"]),
                "captcha_page_disguised": len(diff.get("captcha_page_disguised", [])),
                "orphans": len(diff["orphans"]),
                "stale_manifest": len(diff["stale_manifest"]),
                "noop": diff["noop_count"],
            },
            "exit_code": exit_code,
        })

    return exit_code


if __name__ == "__main__":
    sys.exit(run())
