#!/usr/bin/env python3
"""F11b: audit many notebooks in one invocation.

Motivation
----------
Fernando runs the auditor on multiple notebooks (Hashimoto, GLP1, Beauty
Smile Tech, Willian Celso, Posicionamento). Invoking the router once per
notebook works but wastes attention — preflight + autodiscover + log
interleaving is hard to skim.

This module drives the router in parallel:
    --all                  audit every notebook present in the manifest
    --batch <file>         audit notebooks listed in <file> (one URL/id per line)

Design
------
- ThreadPoolExecutor capped at 3 workers. The manifest file lock is
  shared with deep-research; three concurrent writers is the validated
  ceiling from Fase 5 (file lock is polled, not held-until-done).
- Each notebook runs in its own subprocess so a hard crash in one does
  not take down the batch. Stdout/stderr are captured and routed to the
  per-notebook summary dict — we never interleave raw output.
- Exit codes are aggregated: worst-case wins. A single exit=4 among 10
  runs surfaces as batch exit=4 so cron/launchd alerts fire correctly.
- On --quiet: one JSON line per notebook on stdout (not one per batch)
  so downstream log tooling can bucket results per notebook.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

_DR_SCRIPTS = Path.home() / ".claude" / "skills" / "deep-research" / "scripts"
if str(_DR_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_DR_SCRIPTS))

ROUTER_PY = _HERE / "router.py"

# Conservative: the manifest file lock handles contention but three
# concurrent notebooklm CLI invocations is the Fase 5 validated ceiling.
DEFAULT_WORKERS = 3


def load_targets_from_manifest(manifest_path: Path) -> list[str]:
    """Return every notebook_id present in the manifest. `--all` uses this."""
    if not manifest_path.exists():
        return []
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    notebooks = data.get("notebooks", {})
    # Sort for determinism across runs (useful for cron diff tooling).
    return sorted(notebooks.keys())


def load_targets_from_file(batch_path: Path) -> list[str]:
    """Parse a batch file: one URL or id per line, blank/`#` lines ignored."""
    if not batch_path.exists():
        return []
    lines = batch_path.read_text(encoding="utf-8").splitlines()
    out: list[str] = []
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        out.append(line)
    return out


def _run_one(*, target: str, passthrough: list[str], quiet: bool) -> dict:
    """Invoke the router for a single notebook. Returns a summary dict.

    When --quiet is set we capture the router's stdout summary JSON so
    the batch-level report can splice it into its per-notebook section.
    Otherwise we let stderr stream through so the user sees progress.
    """
    cmd = [sys.executable, str(ROUTER_PY), target, *passthrough]
    # F13: pass --quiet through so each subprocess emits its stdout summary.
    if quiet and "--quiet" not in cmd:
        cmd.append("--quiet")

    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=1800,  # 30 min per notebook (fix-captcha rounds take time)
    )

    parsed_summary: dict | None = None
    if proc.stdout.strip():
        try:
            parsed_summary = json.loads(proc.stdout.splitlines()[-1])
        except (json.JSONDecodeError, IndexError):
            parsed_summary = None

    return {
        "target": target,
        "exit_code": proc.returncode,
        "summary": parsed_summary,
        "stderr_tail": proc.stderr.splitlines()[-5:] if proc.stderr else [],
    }


def run_batch(
    *,
    targets: list[str],
    passthrough: list[str],
    workers: int = DEFAULT_WORKERS,
    quiet: bool = False,
) -> dict:
    """Run router across every target. Returns {overall_exit_code, results}."""
    if not targets:
        return {"overall_exit_code": 2, "results": []}

    results: list[dict] = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        future_map = {
            ex.submit(_run_one, target=t, passthrough=passthrough, quiet=quiet): t
            for t in targets
        }
        for fut in as_completed(future_map):
            try:
                res = fut.result()
            except Exception as e:  # noqa: BLE001
                res = {
                    "target": future_map[fut],
                    "exit_code": 5,
                    "summary": None,
                    "stderr_tail": [f"batch driver error: {e}"],
                }
            results.append(res)
            if quiet:
                # Each run's summary as a standalone JSON line. Downstream
                # tooling buckets by `target`.
                print(json.dumps({
                    "event": "batch_item",
                    "target": res["target"],
                    "exit_code": res["exit_code"],
                    "summary": res["summary"],
                }, ensure_ascii=False), flush=True)
            else:
                tail = " | ".join(res["stderr_tail"][-2:]) if res["stderr_tail"] else ""
                print(
                    f"[batch] target={res['target']} exit={res['exit_code']} {tail}",
                    file=sys.stderr,
                )

    overall = max((r["exit_code"] for r in results), default=0)
    return {"overall_exit_code": overall, "results": results}


def _main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="batch_runner",
        description="F11b: audit multiple notebooks in parallel via the router.",
    )
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument(
        "--all",
        action="store_true",
        help="audit every notebook present in the shared manifest",
    )
    src.add_argument(
        "--batch",
        type=Path,
        help="audit every notebook listed in FILE (one URL/id per line)",
    )
    p.add_argument(
        "--manifest-path",
        type=Path,
        default=Path.home() / ".claude" / "skills" / "deep-research" / "pesquisas" / "_notebook-manifest.json",
        help="manifest to read when --all is used (default: deep-research pesquisas)",
    )
    p.add_argument(
        "--workers",
        type=int,
        default=DEFAULT_WORKERS,
        help=f"parallel router processes (default {DEFAULT_WORKERS}, respects manifest file lock)",
    )
    p.add_argument(
        "--quiet",
        action="store_true",
        help="emit one JSON line per notebook on stdout; suppress progress stderr",
    )
    # Passthrough flags forwarded to the router. We do not attempt to
    # validate them — the router does its own argparse.
    known, passthrough = p.parse_known_args(argv)

    if known.all:
        targets = load_targets_from_manifest(known.manifest_path)
        if not targets:
            print(
                f"[error] --all: no notebooks in manifest {known.manifest_path}",
                file=sys.stderr,
            )
            return 2
    else:
        targets = load_targets_from_file(known.batch)
        if not targets:
            print(f"[error] --batch: no targets in {known.batch}", file=sys.stderr)
            return 2

    if not known.quiet:
        print(f"[batch] {len(targets)} target(s), workers={known.workers}", file=sys.stderr)

    outcome = run_batch(
        targets=targets,
        passthrough=passthrough,
        workers=known.workers,
        quiet=known.quiet,
    )

    if known.quiet:
        print(json.dumps({
            "event": "batch_complete",
            "total": len(targets),
            "overall_exit_code": outcome["overall_exit_code"],
        }, ensure_ascii=False), flush=True)
    else:
        print(
            f"[batch] done — overall exit={outcome['overall_exit_code']} "
            f"({len([r for r in outcome['results'] if r['exit_code'] == 0])}/{len(targets)} clean)",
            file=sys.stderr,
        )

    return outcome["overall_exit_code"]


if __name__ == "__main__":
    sys.exit(_main())
