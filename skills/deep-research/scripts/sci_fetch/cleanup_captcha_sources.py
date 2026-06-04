#!/usr/bin/env python3
"""Delete CAPTCHA / error sources from a NotebookLM notebook.

Usage:
    python cleanup_captcha_sources.py --notebook <NB_ID> [--dry-run]

Uses the `notebooklm` CLI (from notebooklm-py). Requires prior login.

Detects titles matching any of:
    - "Checking your browser"
    - "reCAPTCHA"
    - "Access denied"
    - "Just a moment"
    - "Cloudflare"
    - "Error 403"

Exit code: 0 (always, even if nothing to clean; failures logged to stderr).
"""
from __future__ import annotations

import json
import re
import subprocess
import sys


CAPTCHA_PATTERNS = re.compile(
    r"(checking your browser|recaptcha|access denied|just a moment|cloudflare|error\s*40[13]|forbidden)",
    re.IGNORECASE,
)


def list_sources(notebook_id: str) -> list[dict]:
    result = subprocess.run(
        ["notebooklm", "source", "list", "-n", notebook_id, "--json"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        print(f"[error] notebooklm source list failed: {result.stderr}", file=sys.stderr)
        return []
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print(f"[error] invalid JSON from notebooklm: {e}", file=sys.stderr)
        return []
    return data.get("sources", []) if isinstance(data, dict) else []


def delete_source(source_id: str, notebook_id: str, dry_run: bool) -> bool:
    if dry_run:
        print(f"[dry-run] would delete {source_id}")
        return True
    result = subprocess.run(
        ["notebooklm", "source", "delete", source_id, "-n", notebook_id, "-y"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        print(f"[error] delete {source_id}: {result.stderr}", file=sys.stderr)
        return False
    return True


def _main(argv: list[str]) -> int:
    if "--notebook" not in argv:
        print("usage: cleanup_captcha_sources.py --notebook <NB_ID> [--dry-run]", file=sys.stderr)
        return 1

    nb_id = argv[argv.index("--notebook") + 1]
    dry_run = "--dry-run" in argv

    sources = list_sources(nb_id)
    if not sources:
        print("[info] no sources returned (empty notebook or auth issue)", file=sys.stderr)
        return 0

    to_delete = [
        s for s in sources
        if s.get("title") and CAPTCHA_PATTERNS.search(s["title"])
    ]

    print(f"[info] {len(sources)} total sources; {len(to_delete)} match CAPTCHA patterns")
    deleted = 0
    for src in to_delete:
        sid = src.get("id")
        if not sid:
            continue
        if delete_source(sid, nb_id, dry_run):
            deleted += 1
            print(f"  - deleted: {src.get('title', '')[:80]}")

    print(f"[info] cleanup done: {deleted}/{len(to_delete)} deleted{' (dry run)' if dry_run else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
