#!/usr/bin/env python3
"""F13a tests for install_permissions.py.

Coverage:
    - Fresh settings file (does not exist): creates one with the 3 rules
    - Existing settings with other rules: appends without touching them
    - Idempotent: running twice leaves exit=0 and no extra backup writes
    - Corrupted settings.json: exits 3 with clear error
    - --uninstall removes the rules but leaves siblings intact
    - --dry-run never writes to disk
    - Preserves unrelated top-level settings keys (env, hooks, model, etc.)

Run: python3 evals/test_install_permissions.py
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_SKILL = _HERE.parent
sys.path.insert(0, str(_SKILL / "scripts"))

import install_permissions as ip  # noqa: E402


REQUIRED = ip.REQUIRED_RULES


def test_fresh_file_gets_all_rules():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "settings.json"
        rc = ip.patch(p, dry_run=False)
        assert rc == 0
        data = json.loads(p.read_text())
        assert data["permissions"]["allow"] == REQUIRED


def test_existing_rules_appended_not_replaced():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "settings.json"
        p.write_text(json.dumps({"permissions": {"allow": ["Bash(git:*)", "Bash(npm:*)"]}}))
        rc = ip.patch(p, dry_run=False)
        assert rc == 0
        allow = json.loads(p.read_text())["permissions"]["allow"]
        # order preserved: original first, then the new rules
        assert allow[:2] == ["Bash(git:*)", "Bash(npm:*)"]
        assert set(allow[2:]) == set(REQUIRED)


def test_idempotent_second_run_no_backup_and_exit0():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "settings.json"
        ip.patch(p, dry_run=False)  # first run creates + backs up (nothing to back up on fresh)
        baks_after_first = list(Path(tmp).glob("settings.json.bak-*"))
        rc = ip.patch(p, dry_run=False)
        assert rc == 0
        baks_after_second = list(Path(tmp).glob("settings.json.bak-*"))
        assert baks_after_first == baks_after_second, (
            "second run must not create another backup — it's a no-op"
        )


def test_corrupted_json_exits_3():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "settings.json"
        p.write_text("this is {{{{ not json")
        # We call _main instead of patch directly so the top-level exit-code
        # routing exercises the JSON decode error branch.
        rc = ip._main(["--settings", str(p)])
        assert rc == 3, rc


def test_uninstall_preserves_siblings():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "settings.json"
        p.write_text(json.dumps({"permissions": {"allow": ["Bash(git:*)"] + REQUIRED}}))
        rc = ip.patch(p, dry_run=False, uninstall=True)
        assert rc == 0
        assert json.loads(p.read_text())["permissions"]["allow"] == ["Bash(git:*)"]


def test_dry_run_does_not_write():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "settings.json"
        rc = ip.patch(p, dry_run=True)
        assert rc == 0
        assert not p.exists(), "dry-run must not create the file"


def test_preserves_unrelated_top_level_keys():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "settings.json"
        p.write_text(json.dumps({
            "env": {"FOO": "bar"},
            "model": "opus",
            "hooks": {"PostToolUse": [{"matcher": "Edit", "hooks": []}]},
            "permissions": {"allow": ["Bash(git:*)"]},
        }))
        ip.patch(p, dry_run=False)
        data = json.loads(p.read_text())
        assert data["env"] == {"FOO": "bar"}
        assert data["model"] == "opus"
        assert "hooks" in data
        assert data["permissions"]["allow"][0] == "Bash(git:*)"
        assert set(data["permissions"]["allow"][1:]) == set(REQUIRED)


def test_backup_created_when_file_exists():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "settings.json"
        p.write_text(json.dumps({"env": {"A": "1"}}))
        ip.patch(p, dry_run=False)
        baks = list(Path(tmp).glob("settings.json.bak-*"))
        assert len(baks) == 1, baks
        assert json.loads(baks[0].read_text())["env"] == {"A": "1"}


TESTS = [
    test_fresh_file_gets_all_rules,
    test_existing_rules_appended_not_replaced,
    test_idempotent_second_run_no_backup_and_exit0,
    test_corrupted_json_exits_3,
    test_uninstall_preserves_siblings,
    test_dry_run_does_not_write,
    test_preserves_unrelated_top_level_keys,
    test_backup_created_when_file_exists,
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
