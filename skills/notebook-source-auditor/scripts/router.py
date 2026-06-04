#!/usr/bin/env python3
"""F10a: natural-CLI wrapper around auditor.py.

Turns `/notebook-source-auditor <url_or_id> [--pesquisas X]` into the right
`auditor.py` invocation, picking the mode by inspecting the current NBM state:

    - any title matches F15 captcha regex → `--fix-captcha --dry-run`
    - otherwise                            → `--dry-run` (standard 6-bucket audit)

The dry-run default is deliberate in v2 Fase A (F16-adiado). User passes
`--apply` to actually execute destructive actions.

v2 Fase B (F12) added auto-discover: when `--pesquisas` is omitted, the
router pulls the notebook title and matches against subfolders of
`--pesquisas-root` (default `~/.claude/skills/deep-research/pesquisas/`)
using tokenized Jaccard overlap. Scores >= 0.8 auto-match; scores in the
ambiguous band (0.5–0.8) prompt the user via stdin; all below 0.5 exit 6.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

from url_extract import extract_notebook_id  # noqa: E402
from captcha_patterns import filter_captcha_sources  # noqa: E402
from env_loader import boot as boot_env  # noqa: E402
from pesquisa_autodiscover import (  # noqa: E402
    DEFAULT_PESQUISAS_ROOT,
    MatchResult,
    autodiscover,
)


AUDITOR_PY = _HERE / "auditor.py"


def preflight(notebook_id: str) -> tuple[bool, int, str]:
    """Pull NBM state, return (captcha_detected, total_sources, notebook_title).

    On CLI failure, treat as zero sources — auditor will surface the real
    error with better context. Title is returned so F12 autodiscover can
    match pesquisas against it without a second source-list call.
    """
    result = subprocess.run(
        ["notebooklm", "source", "list", "-n", notebook_id, "--json"],
        capture_output=True, text=True, timeout=30,
    )
    if result.returncode != 0:
        print(
            f"[warn] preflight source-list failed (rc={result.returncode}); "
            "defaulting to standard mode",
            file=sys.stderr,
        )
        return (False, 0, "")
    try:
        data = json.loads(result.stdout) if result.stdout.strip() else {}
    except json.JSONDecodeError:
        return (False, 0, "")
    if isinstance(data, dict):
        sources = data.get("sources") or data.get("data") or []
        title = data.get("title") or data.get("notebook_title") or ""
    else:
        sources = data
        title = ""
    captcha = filter_captcha_sources(sources)
    return (bool(captcha), len(sources), title)


def _prompt_ambiguous(result: MatchResult) -> list[Path]:
    """Render ambiguous candidates and ask the user which to include.

    Accepted replies:
        - blank / "n" / "none"   → no pesquisas selected (caller errors out)
        - "all"                  → include every ambiguous candidate
        - "1,3" / "1 3"          → 1-indexed picks
    """
    print("", file=sys.stderr)
    print("[autodiscover] no auto-match (score >= 0.8) but ambiguous candidates exist:", file=sys.stderr)
    for idx, c in enumerate(result.ambiguous, start=1):
        print(f"  [{idx}] {c.slug}  (score {c.score:.2f})  — {c.title[:60]}", file=sys.stderr)
    print(
        "[autodiscover] enter numbers to include (comma-separated), 'all', "
        "or blank to cancel:",
        file=sys.stderr,
    )
    try:
        raw = input("> ").strip().lower()
    except EOFError:
        raw = ""
    if not raw or raw in {"n", "no", "none"}:
        return []
    if raw == "all":
        return [c.path for c in result.ambiguous]
    picks: list[Path] = []
    for token in raw.replace(",", " ").split():
        try:
            idx = int(token)
        except ValueError:
            continue
        if 1 <= idx <= len(result.ambiguous):
            picks.append(result.ambiguous[idx - 1].path)
    return picks


def resolve_pesquisas(
    *,
    notebook_title: str,
    pesquisas_flag: str | None,
    pesquisas_root: Path | None,
    prompt_fn=_prompt_ambiguous,
) -> tuple[list[Path], int]:
    """Decide which pesquisa paths to pass to auditor.py.

    Returns (paths, exit_code). When exit_code != 0 the caller should abort
    with that code — paths will be empty.

    Exit codes:
        0 — paths resolved (explicit --pesquisas OR auto-match OR user picks)
        6 — autodiscover found zero candidates above the ambiguous floor
    """
    if pesquisas_flag:
        return ([Path(p.strip()) for p in pesquisas_flag.split(",") if p.strip()], 0)

    if not notebook_title:
        print(
            "[error] autodiscover needs the notebook title, but preflight "
            "returned empty. Pass --pesquisas explicitly.",
            file=sys.stderr,
        )
        return ([], 6)

    result = autodiscover(notebook_title=notebook_title, root=pesquisas_root)
    root_str = str(result.scan_root) if result.scan_root else "<unset>"
    print(
        f"[autodiscover] scanned {result.scanned_count} candidate(s) under {root_str}",
        file=sys.stderr,
    )

    if result.has_auto:
        picked = [c.path for c in result.auto]
        print(
            "[autodiscover] auto-matched: "
            + ", ".join(f"{c.slug} ({c.score:.2f})" for c in result.auto),
            file=sys.stderr,
        )
        return (picked, 0)

    if result.no_match:
        print(
            f"[error] autodiscover found no pesquisa with score >= "
            f"0.5 matching notebook title '{notebook_title}'. "
            f"Pass --pesquisas explicitly or add a pesquisa under {root_str}.",
            file=sys.stderr,
        )
        return ([], 6)

    # Needs user prompt.
    picks = prompt_fn(result)
    if not picks:
        print("[error] autodiscover cancelled; no pesquisas selected.", file=sys.stderr)
        return ([], 6)
    print(
        f"[autodiscover] user selected {len(picks)} pesquisa(s): "
        + ", ".join(p.name for p in picks),
        file=sys.stderr,
    )
    return (picks, 0)


def _main(argv: list[str] | None = None) -> int:
    # F9: apply dotenv before preflight so the NotebookLM CLI subprocess
    # inherits anything the user configured (e.g. custom paths, debug flags).
    boot_env()
    p = argparse.ArgumentParser(
        prog="/notebook-source-auditor",
        description="Natural wrapper: detects mode from NBM state and dispatches auditor.py",
    )
    p.add_argument("target", help="notebook URL or bare id")
    p.add_argument(
        "--pesquisas",
        default=None,
        help="comma-separated pesquisa paths. Omit to trigger F12 autodiscover "
             "from --pesquisas-root against the notebook title.",
    )
    p.add_argument(
        "--pesquisas-root",
        default=None,
        help=f"autodiscover scan root (default: {DEFAULT_PESQUISAS_ROOT})",
    )
    p.add_argument(
        "--apply",
        action="store_true",
        help="execute destructive actions (default: dry-run in v2 Fase A)",
    )
    p.add_argument(
        "--force-mode",
        choices=["standard", "fix-captcha"],
        help="bypass preflight detection and force a specific mode",
    )
    # Passthrough for advanced flags.
    p.add_argument("--audits-dir")
    p.add_argument("--skip-orphans", action="store_true")
    p.add_argument("--skip-duplicates", action="store_true")
    p.add_argument("--interactive", action="store_true")
    p.add_argument("--max-retry", type=int, default=3)
    # Fase C passthroughs — no routing logic, they just reach auditor.py.
    p.add_argument(
        "--quiet",
        action="store_true",
        help="F13: suppress stderr progress; emit stdout JSON summary (cron-friendly)",
    )
    p.add_argument(
        "--bootstrap",
        action="store_true",
        help="F10: populate an empty manifest from current NBM + pesquisas",
    )
    p.add_argument(
        "--rollback",
        action="store_true",
        help="F14: restore the most recent manifest backup and exit",
    )
    args = p.parse_args(argv)

    try:
        notebook_id = extract_notebook_id(args.target)
    except ValueError as e:
        print(f"[error] {e}", file=sys.stderr)
        return 2

    # F14 --rollback: no NBM call, no autodiscover. Users should still pass
    # --pesquisas to pin the manifest root; otherwise we fall back to
    # autodiscover's default root (deep-research/pesquisas). Either way,
    # preflight is skipped because rollback is a pure file-level operation.
    rollback_mode = bool(getattr(args, "rollback", False))
    if rollback_mode:
        captcha_found, total, notebook_title = (False, 0, "")
        mode = "standard"
    else:
        # Preflight runs even when --force-mode is set, because F12 autodiscover
        # needs the notebook_title that the same source-list call returns.
        captcha_found, total, notebook_title = preflight(notebook_id)
        if args.force_mode:
            mode = args.force_mode
            if not args.quiet:
                print(f"[router] forced mode: {mode}", file=sys.stderr)
        else:
            mode = "fix-captcha" if captcha_found else "standard"
            if not args.quiet:
                print(
                    f"[router] preflight: {total} source(s); captcha={captcha_found} → mode={mode}",
                    file=sys.stderr,
                )

    # F12: resolve --pesquisas either from the flag or via autodiscover.
    # For --rollback we skip autodiscover (no notebook_title) and require
    # the user to pin the manifest root with --pesquisas. Without one, the
    # rollback can't know which manifest file to restore.
    pesquisas_root = Path(args.pesquisas_root) if args.pesquisas_root else None
    if rollback_mode and not args.pesquisas:
        print(
            "[error] --rollback needs --pesquisas to pin the manifest root "
            "(pass any pesquisa under the target root so the manifest path "
            "can be derived).",
            file=sys.stderr,
        )
        return 2
    pesquisa_paths, rc = resolve_pesquisas(
        notebook_title=notebook_title,
        pesquisas_flag=args.pesquisas,
        pesquisas_root=pesquisas_root,
    )
    if rc != 0:
        return rc
    resolved_pesquisas = ",".join(str(p) for p in pesquisa_paths)

    cmd = [
        sys.executable, str(AUDITOR_PY),
        "--notebook", args.target,
        "--pesquisas", resolved_pesquisas,
        "--max-retry", str(args.max_retry),
    ]
    if args.audits_dir:
        cmd += ["--audits-dir", args.audits_dir]
    if args.skip_orphans:
        cmd.append("--skip-orphans")
    if args.skip_duplicates:
        cmd.append("--skip-duplicates")
    if args.interactive:
        cmd.append("--interactive")
    if mode == "fix-captcha":
        cmd.append("--fix-captcha")
    if args.apply:
        cmd.append("--apply")
    # Fase C passthroughs — each is a pure flag, no value.
    if args.quiet:
        cmd.append("--quiet")
    if args.bootstrap:
        cmd.append("--bootstrap")
    if args.rollback:
        cmd.append("--rollback")
    # else: dry-run is the default in auditor.py — no flag needed.

    if not args.quiet:
        print(f"[router] $ {' '.join(cmd)}", file=sys.stderr)
    return subprocess.run(cmd).returncode


if __name__ == "__main__":
    sys.exit(_main())
