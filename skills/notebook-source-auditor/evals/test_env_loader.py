#!/usr/bin/env python3
"""F9 tests — dotenv loader for ~/.claude/skills/notebook-source-auditor/.env.

Scenarios:
    - parse_env_file: KEY=VALUE, export KEY=VALUE, quoted values, comments,
      blank lines, missing-equals lines
    - apply_env_file: merges into os.environ, skips keys already set
    - apply_env_file: override=True actually overwrites existing values
    - apply_env_file: silent no-op when file is missing
    - ensure_restrictive_perms: chmod 600 when world/group readable
    - boot(): loads from DEFAULT_ENV_PATH (monkeypatched) and returns keys
    - auditor.run() + router._main() pick up env file at entry

Run: python3 evals/test_env_loader.py
"""
from __future__ import annotations

import os
import stat
import sys
import tempfile
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_SKILL = _HERE.parent
sys.path.insert(0, str(_SKILL / "scripts"))
sys.path.insert(0, str(Path.home() / ".claude/skills/deep-research/scripts"))

import env_loader  # noqa: E402


# ---------------------------------------------------------------------------
# parse_env_file
# ---------------------------------------------------------------------------

def test_f9_parse_simple_key_value():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / ".env"
        p.write_text("FOO=bar\nBAZ=qux\n", encoding="utf-8")
        got = env_loader.parse_env_file(p)
        got.pop("__warnings__", None)
        assert got == {"FOO": "bar", "BAZ": "qux"}


def test_f9_parse_strips_export_prefix():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / ".env"
        p.write_text("export NCBI_API_KEY=abc123\nexport UNPAYWALL_EMAIL=a@b.co\n", encoding="utf-8")
        got = env_loader.parse_env_file(p)
        got.pop("__warnings__", None)
        assert got == {"NCBI_API_KEY": "abc123", "UNPAYWALL_EMAIL": "a@b.co"}


def test_f9_parse_strips_matching_quotes():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / ".env"
        p.write_text('''FOO="bar baz"\nBAR='q u x'\nNOQUOTE="unclosed\n''', encoding="utf-8")
        got = env_loader.parse_env_file(p)
        got.pop("__warnings__", None)
        assert got["FOO"] == "bar baz"
        assert got["BAR"] == "q u x"
        # Only matching outer quotes get stripped — unbalanced stays intact.
        assert got["NOQUOTE"] == '"unclosed'


def test_f9_parse_ignores_comments_and_blanks():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / ".env"
        p.write_text(
            "# leading comment\n"
            "\n"
            "FOO=ok\n"
            "# trailing comment\n"
            "\n"
            "BAR=also_ok\n",
            encoding="utf-8",
        )
        got = env_loader.parse_env_file(p)
        got.pop("__warnings__", None)
        assert got == {"FOO": "ok", "BAR": "also_ok"}


def test_f9_parse_malformed_line_goes_to_warnings():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / ".env"
        p.write_text("FOO=ok\nno_equals_here\nBAR=also\n", encoding="utf-8")
        got = env_loader.parse_env_file(p)
        assert got["FOO"] == "ok"
        assert got["BAR"] == "also"
        assert "__warnings__" in got
        assert "L2" in got["__warnings__"]


def test_f9_parse_missing_file_returns_empty():
    got = env_loader.parse_env_file(Path("/nonexistent/path/.env"))
    assert got == {}


# ---------------------------------------------------------------------------
# apply_env_file
# ---------------------------------------------------------------------------

def _clear_env(keys):
    for k in keys:
        os.environ.pop(k, None)


def test_f9_apply_sets_new_keys():
    keys = ["F9_TEST_FOO", "F9_TEST_BAR"]
    _clear_env(keys)
    try:
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / ".env"
            p.write_text("F9_TEST_FOO=aaa\nF9_TEST_BAR=bbb\n", encoding="utf-8")
            applied = env_loader.apply_env_file(p)
            assert sorted(applied) == sorted(keys)
            assert os.environ["F9_TEST_FOO"] == "aaa"
            assert os.environ["F9_TEST_BAR"] == "bbb"
    finally:
        _clear_env(keys)


def test_f9_apply_does_not_override_shell_export_by_default():
    """Shell exports always win — the caller's environment is the source of
    truth. This mirrors python-dotenv's default and the spec in env_loader.py."""
    keys = ["F9_TEST_EXPORT_WINS"]
    _clear_env(keys)
    os.environ["F9_TEST_EXPORT_WINS"] = "shell_value"
    try:
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / ".env"
            p.write_text("F9_TEST_EXPORT_WINS=dotenv_value\n", encoding="utf-8")
            applied = env_loader.apply_env_file(p)
            assert applied == []  # nothing actually changed
            assert os.environ["F9_TEST_EXPORT_WINS"] == "shell_value"
    finally:
        _clear_env(keys)


def test_f9_apply_override_true_replaces_existing():
    keys = ["F9_TEST_OVERRIDE"]
    _clear_env(keys)
    os.environ["F9_TEST_OVERRIDE"] = "old"
    try:
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / ".env"
            p.write_text("F9_TEST_OVERRIDE=new\n", encoding="utf-8")
            applied = env_loader.apply_env_file(p, override=True)
            assert applied == keys
            assert os.environ["F9_TEST_OVERRIDE"] == "new"
    finally:
        _clear_env(keys)


def test_f9_apply_missing_file_is_silent_no_op():
    applied = env_loader.apply_env_file(Path("/does/not/exist/.env"))
    assert applied == []


# ---------------------------------------------------------------------------
# ensure_restrictive_perms
# ---------------------------------------------------------------------------

def test_f9_chmod_600_when_world_readable():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / ".env"
        p.write_text("K=v\n", encoding="utf-8")
        # Make it world-readable.
        p.chmod(0o644)
        ok = env_loader.ensure_restrictive_perms(p)
        assert ok is True
        mode = stat.S_IMODE(p.stat().st_mode)
        # 0o600 is owner rw only — no bits set for group/world.
        assert mode & (stat.S_IRGRP | stat.S_IROTH | stat.S_IWGRP | stat.S_IWOTH) == 0


def test_f9_chmod_noop_when_already_restrictive():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / ".env"
        p.write_text("K=v\n", encoding="utf-8")
        p.chmod(0o600)
        ok = env_loader.ensure_restrictive_perms(p)
        assert ok is True
        mode = stat.S_IMODE(p.stat().st_mode)
        assert mode == 0o600


# ---------------------------------------------------------------------------
# boot() default path
# ---------------------------------------------------------------------------

def test_f9_boot_uses_default_env_path(monkeypatch_via_setattr=True):
    """boot() reads from env_loader.DEFAULT_ENV_PATH — redirecting the
    constant to a temp file should make the loader pick it up."""
    keys = ["F9_TEST_BOOT"]
    _clear_env(keys)
    original = env_loader.DEFAULT_ENV_PATH
    try:
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / ".env"
            p.write_text("F9_TEST_BOOT=yup\n", encoding="utf-8")
            env_loader.DEFAULT_ENV_PATH = p  # type: ignore[assignment]
            applied = env_loader.boot()
            assert applied == ["F9_TEST_BOOT"]
            assert os.environ["F9_TEST_BOOT"] == "yup"
    finally:
        env_loader.DEFAULT_ENV_PATH = original  # type: ignore[assignment]
        _clear_env(keys)


def test_f9_boot_no_file_returns_empty():
    """Fresh install: no .env file exists. boot() must not crash, must not
    touch os.environ, must return an empty list."""
    original = env_loader.DEFAULT_ENV_PATH
    try:
        env_loader.DEFAULT_ENV_PATH = Path("/absolutely/no/such/path/.env")  # type: ignore[assignment]
        applied = env_loader.boot()
        assert applied == []
    finally:
        env_loader.DEFAULT_ENV_PATH = original  # type: ignore[assignment]


# ---------------------------------------------------------------------------
# Entry
# ---------------------------------------------------------------------------
TESTS = [
    test_f9_parse_simple_key_value,
    test_f9_parse_strips_export_prefix,
    test_f9_parse_strips_matching_quotes,
    test_f9_parse_ignores_comments_and_blanks,
    test_f9_parse_malformed_line_goes_to_warnings,
    test_f9_parse_missing_file_returns_empty,
    test_f9_apply_sets_new_keys,
    test_f9_apply_does_not_override_shell_export_by_default,
    test_f9_apply_override_true_replaces_existing,
    test_f9_apply_missing_file_is_silent_no_op,
    test_f9_chmod_600_when_world_readable,
    test_f9_chmod_noop_when_already_restrictive,
    test_f9_boot_uses_default_env_path,
    test_f9_boot_no_file_returns_empty,
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
