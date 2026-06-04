#!/usr/bin/env python3
"""F14: manifest backup + rollback + structured JSONL logging.

Before any destructive action in `--apply` mode, we snapshot the manifest
to `_notebook-manifest.backup-<timestamp>.json` alongside the original.
`--rollback` restores the most recent snapshot.

Limitation: restoring the manifest does NOT undo `notebooklm source delete`
calls. The NotebookLM CLI has no undo — deleted sources are gone. After a
rollback, any re-adds that failed before the crash will reappear as
`status=failed` in the restored manifest; the next normal run picks them
up via the retryable bucket.

Logging: every backup/rollback/destructive event gets a line in
`logs/auditor-<YYYY-MM-DD>.jsonl`. One JSON dict per line, append-only.
Dashboards or grep tools can consume this without parsing the full audit
markdown. Log failures are warnings, never fatal — never let observability
block the operational path.
"""
from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


BACKUP_PREFIX = "_notebook-manifest.backup-"
BACKUP_SUFFIX = ".json"
# Kept per-manifest-root. Two notebooks sharing a pesquisas_root share the
# backup set — acceptable because the manifest itself is shared.
MAX_BACKUPS_KEPT = 10


def _now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def create_backup(manifest_path: Path) -> Path | None:
    """Copy `_notebook-manifest.json` to `_notebook-manifest.backup-<ts>.json`.

    Returns the backup path on success. Returns None when the manifest does
    not exist (there is nothing to back up — callers should treat this as
    a no-op, not an error, so bootstrap runs stay quiet).

    Older backups beyond MAX_BACKUPS_KEPT are pruned on success, oldest
    first. We never prune on failure — keeping whatever is there is safer
    than losing history.
    """
    manifest_path = Path(manifest_path)
    if not manifest_path.exists():
        return None
    stamp = _now_stamp()
    backup_path = manifest_path.with_name(f"{BACKUP_PREFIX}{stamp}{BACKUP_SUFFIX}")
    shutil.copy2(manifest_path, backup_path)
    _prune_old_backups(manifest_path)
    return backup_path


def list_backups(manifest_path: Path) -> list[Path]:
    """Return every backup file in the manifest's directory, newest first.

    Sorted by filename (the ISO-like timestamp is lexically sortable), not
    by mtime — mtime can drift if files get copied between machines.
    """
    manifest_path = Path(manifest_path)
    parent = manifest_path.parent
    if not parent.exists():
        return []
    backups = [
        p for p in parent.iterdir()
        if p.is_file()
        and p.name.startswith(BACKUP_PREFIX)
        and p.name.endswith(BACKUP_SUFFIX)
    ]
    backups.sort(key=lambda p: p.name, reverse=True)
    return backups


def rollback_latest(manifest_path: Path) -> Path | None:
    """Restore the most recent backup to the manifest path.

    Returns the backup path that was restored, or None when there are no
    backups. Overwrites the current manifest atomically (write to `.tmp`
    then rename) so a crash mid-copy never leaves a truncated manifest.
    """
    manifest_path = Path(manifest_path)
    backups = list_backups(manifest_path)
    if not backups:
        return None
    latest = backups[0]
    tmp = manifest_path.with_suffix(manifest_path.suffix + ".tmp")
    shutil.copy2(latest, tmp)
    tmp.replace(manifest_path)
    return latest


def _prune_old_backups(manifest_path: Path) -> None:
    """Drop backups beyond MAX_BACKUPS_KEPT. Silent on error — we never let
    pruning fail the operational path."""
    backups = list_backups(manifest_path)
    for stale in backups[MAX_BACKUPS_KEPT:]:
        try:
            stale.unlink()
        except OSError:
            pass


def write_log_event(logs_dir: Path, event: dict) -> Path | None:
    """Append one JSON object per line to `logs/auditor-<date>.jsonl`.

    `event` is merged with {ts, date}; callers control the rest (event
    type, notebook_id, counts, exit code). Any write failure is swallowed
    with a stderr warning — observability must not crash a destructive
    run.
    """
    logs_dir = Path(logs_dir)
    try:
        logs_dir.mkdir(parents=True, exist_ok=True)
        today = _today()
        log_path = logs_dir / f"auditor-{today}.jsonl"
        record = {"ts": datetime.now(timezone.utc).isoformat(), **event}
        with log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        return log_path
    except OSError as e:
        print(f"[warn] could not write log event: {e}", file=sys.stderr)
        return None


def _cli_rollback(manifest_path_str: str) -> int:
    manifest_path = Path(manifest_path_str).expanduser().resolve()
    if not manifest_path.parent.exists():
        print(f"[error] manifest directory does not exist: {manifest_path.parent}", file=sys.stderr)
        return 2
    restored = rollback_latest(manifest_path)
    if not restored:
        print(f"[error] no backups found for {manifest_path.name} in {manifest_path.parent}", file=sys.stderr)
        return 2
    print(f"[ok] restored manifest from {restored.name}", file=sys.stderr)
    print(
        "[info] NotebookLM source deletions are NOT reversed by rollback; "
        "re-adds failing mid-run will reappear as status=failed on next audit.",
        file=sys.stderr,
    )
    return 0


def _cli_list(manifest_path_str: str) -> int:
    manifest_path = Path(manifest_path_str).expanduser().resolve()
    backups = list_backups(manifest_path)
    if not backups:
        print("(no backups)", file=sys.stderr)
        return 0
    for p in backups:
        print(p.name)
    return 0


def _main(argv: list[str] | None = None) -> int:
    import argparse
    p = argparse.ArgumentParser(
        prog="manifest_backup",
        description="Backup/rollback helpers for _notebook-manifest.json (F14).",
    )
    sub = p.add_subparsers(dest="cmd", required=True)
    sp_bak = sub.add_parser("backup", help="snapshot the manifest now")
    sp_bak.add_argument("manifest_path")
    sp_rb = sub.add_parser("rollback", help="restore the most recent snapshot")
    sp_rb.add_argument("manifest_path")
    sp_ls = sub.add_parser("list", help="list every snapshot, newest first")
    sp_ls.add_argument("manifest_path")
    args = p.parse_args(argv)

    if args.cmd == "backup":
        m = Path(args.manifest_path).expanduser().resolve()
        bk = create_backup(m)
        if bk is None:
            print(f"[warn] manifest does not exist at {m} — nothing to back up", file=sys.stderr)
            return 2
        print(f"[ok] backup: {bk.name}")
        return 0
    if args.cmd == "rollback":
        return _cli_rollback(args.manifest_path)
    if args.cmd == "list":
        return _cli_list(args.manifest_path)
    return 2


if __name__ == "__main__":
    sys.exit(_main())
