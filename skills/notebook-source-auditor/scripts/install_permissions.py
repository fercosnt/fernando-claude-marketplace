#!/usr/bin/env python3
"""F13a: Install harness permission rules for the notebook-source-auditor.

During Phase 5 (2026-04-23) the Claude Code harness hook blocked bulk delete
operations twice even after the user gave generic authorization ("pode seguir").
The hook required per-target approval, forcing the user to run the delete loop
manually in a terminal.

This script patches `~/.claude/settings.json` to add wildcard allow-rules for
the exact notebooklm CLI commands that the auditor drives. Idempotent:
re-running does nothing. Creates a timestamped `.bak` before modifying.

Usage:
    python install_permissions.py                  # patch + backup
    python install_permissions.py --dry-run        # show diff, don't write
    python install_permissions.py --settings PATH  # override settings location
    python install_permissions.py --uninstall      # remove the rules

Exit codes:
    0  patched OR already in place (both success)
    2  invalid invocation / settings file not writable
    3  settings.json exists but is not valid JSON (human must fix first)
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


# Rules added by F13a. All three are needed for full-auto auditor + fix-captcha:
#   - list: reading NBM state
#   - add : re-adding URLs after captcha delete (via sci_fetch subprocess)
#   - delete: bulk-deleting captcha pages / duplicates
REQUIRED_RULES = [
    "Bash(notebooklm source list:*)",
    "Bash(notebooklm source add:*)",
    "Bash(notebooklm source delete:*)",
]


def _now_slug() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _default_settings_path() -> Path:
    return Path.home() / ".claude" / "settings.json"


def _load_settings(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as e:
        raise SystemExit(f"[error] cannot read {path}: {e}")
    if not raw.strip():
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise SystemExit(
            f"[error] {path} is not valid JSON ({e}). Fix manually before re-running."
        )


def _ensure_allow_list(settings: dict) -> list[str]:
    perms = settings.setdefault("permissions", {})
    allow = perms.setdefault("allow", [])
    if not isinstance(allow, list):
        raise SystemExit(
            f"[error] settings.permissions.allow must be a list; found {type(allow).__name__}."
        )
    return allow


def _backup(path: Path) -> Path | None:
    """Copy the current settings file to a timestamped .bak. Skipped when the
    file doesn't exist yet."""
    if not path.exists():
        return None
    bak = path.with_suffix(path.suffix + f".bak-{_now_slug()}")
    bak.write_bytes(path.read_bytes())
    return bak


def patch(settings_path: Path, *, dry_run: bool = False, uninstall: bool = False) -> int:
    settings = _load_settings(settings_path)
    allow = _ensure_allow_list(settings)
    before = list(allow)

    if uninstall:
        after = [r for r in allow if r not in REQUIRED_RULES]
        action = "uninstall"
    else:
        # Preserve existing order; only append rules not already present.
        missing = [r for r in REQUIRED_RULES if r not in allow]
        after = list(allow) + missing
        action = "install"

    if before == after:
        print(f"[ok] already {action}ed — nothing to do ({len(REQUIRED_RULES)} rules in place)")
        return 0

    # Replace the list reference so the mutation is visible to the parent dict.
    settings["permissions"]["allow"] = after

    if dry_run:
        print(f"[dry-run] would {action} in {settings_path}")
        print("  before:", json.dumps(before, indent=2))
        print("  after :", json.dumps(after, indent=2))
        return 0

    bak = _backup(settings_path)
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    settings_path.write_text(
        json.dumps(settings, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"[ok] {action}ed {len(REQUIRED_RULES)} rule(s) in {settings_path}")
    if bak:
        print(f"[ok] backup: {bak}")
    return 0


def _main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="notebook-source-auditor-install-permissions",
        description="Patch ~/.claude/settings.json to allow the auditor to run "
                    "notebooklm source list/add/delete without per-target prompts.",
    )
    p.add_argument("--settings", default=None, help="override settings.json path")
    p.add_argument("--dry-run", action="store_true", help="show diff, don't write")
    p.add_argument("--uninstall", action="store_true", help="remove the rules instead")
    args = p.parse_args(argv)

    path = Path(args.settings).expanduser() if args.settings else _default_settings_path()
    try:
        return patch(path, dry_run=args.dry_run, uninstall=args.uninstall)
    except SystemExit as e:
        if isinstance(e.code, str):
            print(e.code, file=sys.stderr)
            return 3 if "not valid JSON" in e.code else 2
        return int(e.code or 1)


if __name__ == "__main__":
    sys.exit(_main())
