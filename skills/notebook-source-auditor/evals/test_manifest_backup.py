#!/usr/bin/env python3
"""F14 tests — manifest snapshot, rollback, JSONL logging.

Scenarios:
    - create_backup: writes a copy with the `.backup-<stamp>.json` suffix
    - create_backup: no-op when the manifest does not exist
    - create_backup: prunes old backups beyond MAX_BACKUPS_KEPT
    - list_backups: sorted newest-first by filename (ISO timestamp)
    - rollback_latest: restores the most recent backup atomically
    - rollback_latest: no-op (returns None) when no backups exist
    - write_log_event: appends one JSON dict per line to logs/auditor-<date>.jsonl
    - write_log_event: fails silently when logs dir is not writable (no crash)
    - CLI: `manifest_backup.py backup|list|rollback <path>` exit codes

Run: python3 evals/test_manifest_backup.py
"""
from __future__ import annotations

import json
import os
import stat
import sys
import tempfile
import time
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_SKILL = _HERE.parent
sys.path.insert(0, str(_SKILL / "scripts"))

import manifest_backup  # noqa: E402


# ---------------------------------------------------------------------------
# create_backup
# ---------------------------------------------------------------------------

def test_f14_create_backup_writes_copy_with_timestamp_suffix():
    with tempfile.TemporaryDirectory() as tmp:
        m = Path(tmp) / "_notebook-manifest.json"
        m.write_text('{"version": 1, "notebooks": {"abc": {}}}', encoding="utf-8")
        bk = manifest_backup.create_backup(m)
        assert bk is not None
        assert bk.exists()
        assert bk.name.startswith("_notebook-manifest.backup-")
        assert bk.name.endswith(".json")
        # Backup contents match the source byte-for-byte.
        assert bk.read_text(encoding="utf-8") == m.read_text(encoding="utf-8")


def test_f14_create_backup_missing_manifest_is_silent_noop():
    with tempfile.TemporaryDirectory() as tmp:
        m = Path(tmp) / "_notebook-manifest.json"
        # Do NOT create the file. create_backup should return None, not raise.
        bk = manifest_backup.create_backup(m)
        assert bk is None


def test_f14_create_backup_prunes_beyond_max_kept():
    original_max = manifest_backup.MAX_BACKUPS_KEPT
    try:
        manifest_backup.MAX_BACKUPS_KEPT = 3  # type: ignore[assignment]
        with tempfile.TemporaryDirectory() as tmp:
            m = Path(tmp) / "_notebook-manifest.json"
            m.write_text("{}", encoding="utf-8")
            # Write 5 snapshots with distinct timestamps. Sleep is required
            # because the stamp has 1-second resolution.
            for _ in range(5):
                manifest_backup.create_backup(m)
                time.sleep(1.1)
            remaining = manifest_backup.list_backups(m)
            # After the 5th create_backup the pruner has already removed
            # the two oldest — only 3 remain.
            assert len(remaining) == 3
    finally:
        manifest_backup.MAX_BACKUPS_KEPT = original_max  # type: ignore[assignment]


# ---------------------------------------------------------------------------
# list_backups / rollback_latest
# ---------------------------------------------------------------------------

def test_f14_list_backups_sorted_newest_first():
    with tempfile.TemporaryDirectory() as tmp:
        parent = Path(tmp)
        # Construct three backups with increasing timestamps.
        for stamp in ("20260101-000000", "20260201-000000", "20260301-000000"):
            (parent / f"_notebook-manifest.backup-{stamp}.json").write_text("{}")
        backups = manifest_backup.list_backups(parent / "_notebook-manifest.json")
        assert [b.name for b in backups] == [
            "_notebook-manifest.backup-20260301-000000.json",
            "_notebook-manifest.backup-20260201-000000.json",
            "_notebook-manifest.backup-20260101-000000.json",
        ]


def test_f14_rollback_latest_restores_most_recent():
    with tempfile.TemporaryDirectory() as tmp:
        m = Path(tmp) / "_notebook-manifest.json"
        m.write_text('{"version": 1, "tag": "original"}', encoding="utf-8")
        bk1 = manifest_backup.create_backup(m)
        # Mutate the manifest.
        time.sleep(1.1)
        m.write_text('{"version": 1, "tag": "mutated"}', encoding="utf-8")
        bk2 = manifest_backup.create_backup(m)
        # More mutation — to confirm rollback restores bk2, not bk1.
        m.write_text('{"version": 1, "tag": "broken"}', encoding="utf-8")
        restored = manifest_backup.rollback_latest(m)
        assert restored == bk2
        data = json.loads(m.read_text(encoding="utf-8"))
        assert data["tag"] == "mutated"
        # Oldest backup still exists on disk — rollback does not delete.
        assert bk1.exists()


def test_f14_rollback_latest_no_backups_returns_none():
    with tempfile.TemporaryDirectory() as tmp:
        m = Path(tmp) / "_notebook-manifest.json"
        m.write_text("{}", encoding="utf-8")
        restored = manifest_backup.rollback_latest(m)
        assert restored is None


# ---------------------------------------------------------------------------
# write_log_event
# ---------------------------------------------------------------------------

def test_f14_write_log_event_appends_one_json_per_line():
    with tempfile.TemporaryDirectory() as tmp:
        logs_dir = Path(tmp) / "logs"
        # Two events — both should end up on the same day's file as
        # distinct lines.
        manifest_backup.write_log_event(logs_dir, {"event": "audit", "n": 1})
        manifest_backup.write_log_event(logs_dir, {"event": "audit", "n": 2})
        files = list(logs_dir.glob("auditor-*.jsonl"))
        assert len(files) == 1
        lines = files[0].read_text(encoding="utf-8").splitlines()
        assert len(lines) == 2
        recs = [json.loads(ln) for ln in lines]
        assert [r["n"] for r in recs] == [1, 2]
        # Both records carry the `ts` field added by write_log_event.
        for r in recs:
            assert "ts" in r


def test_f14_write_log_event_does_not_crash_on_bad_path():
    # Pass a path inside a file (not a directory) — mkdir will fail.
    with tempfile.TemporaryDirectory() as tmp:
        blocker = Path(tmp) / "not-a-dir"
        blocker.write_text("", encoding="utf-8")
        result = manifest_backup.write_log_event(blocker / "nested", {"x": 1})
        # We want silent failure, not crash. Return None is acceptable.
        assert result is None


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def test_f14_cli_backup_missing_manifest_exits_2():
    with tempfile.TemporaryDirectory() as tmp:
        rc = manifest_backup._main(["backup", str(Path(tmp) / "_notebook-manifest.json")])
        assert rc == 2


def test_f14_cli_rollback_no_backups_exits_2():
    with tempfile.TemporaryDirectory() as tmp:
        rc = manifest_backup._main(["rollback", str(Path(tmp) / "_notebook-manifest.json")])
        assert rc == 2


def test_f14_cli_list_empty_returns_0():
    with tempfile.TemporaryDirectory() as tmp:
        rc = manifest_backup._main(["list", str(Path(tmp) / "_notebook-manifest.json")])
        # Empty list is not an error — cron pipelines want exit 0.
        assert rc == 0


def test_f14_cli_list_shows_backups_newest_first():
    # Capture stdout to confirm the filename ordering.
    import io
    from contextlib import redirect_stdout
    with tempfile.TemporaryDirectory() as tmp:
        parent = Path(tmp)
        for stamp in ("20260101-000000", "20260201-000000"):
            (parent / f"_notebook-manifest.backup-{stamp}.json").write_text("{}")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = manifest_backup._main(["list", str(parent / "_notebook-manifest.json")])
        assert rc == 0
        lines = [ln for ln in buf.getvalue().splitlines() if ln.strip()]
        assert lines[0] == "_notebook-manifest.backup-20260201-000000.json"
        assert lines[1] == "_notebook-manifest.backup-20260101-000000.json"


TESTS = [
    test_f14_create_backup_writes_copy_with_timestamp_suffix,
    test_f14_create_backup_missing_manifest_is_silent_noop,
    test_f14_create_backup_prunes_beyond_max_kept,
    test_f14_list_backups_sorted_newest_first,
    test_f14_rollback_latest_restores_most_recent,
    test_f14_rollback_latest_no_backups_returns_none,
    test_f14_write_log_event_appends_one_json_per_line,
    test_f14_write_log_event_does_not_crash_on_bad_path,
    test_f14_cli_backup_missing_manifest_exits_2,
    test_f14_cli_rollback_no_backups_exits_2,
    test_f14_cli_list_empty_returns_0,
    test_f14_cli_list_shows_backups_newest_first,
]


def main() -> int:
    passed = failed = 0
    for t in TESTS:
        try:
            t()
        except AssertionError as e:
            failed += 1
            print(f"[FAIL] {t.__name__}: {e}")
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"[ERR ] {t.__name__}: {type(e).__name__}: {e}")
        else:
            passed += 1
            print(f"[PASS] {t.__name__}")
    print(f"\n{passed}/{passed + failed} tests passed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
