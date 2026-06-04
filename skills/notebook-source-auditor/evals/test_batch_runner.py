#!/usr/bin/env python3
"""F11b tests — audit many notebooks via --all or --batch.

Scenarios:
    - load_targets_from_manifest: reads every notebook_id, sorted
    - load_targets_from_manifest: missing manifest returns empty list
    - load_targets_from_file: strips blanks and `#` comments
    - run_batch: aggregates exit codes (worst-case wins)
    - run_batch: exceptions in one target do not kill the batch
    - run_batch: --quiet emits per-target JSON summaries on stdout
    - CLI --all wires through manifest_path
    - CLI --batch forwards extra args to the router

Run: python3 evals/test_batch_runner.py
"""
from __future__ import annotations

import io
import json
import sys
import tempfile
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
from unittest.mock import patch

_HERE = Path(__file__).resolve().parent
_SKILL = _HERE.parent
sys.path.insert(0, str(_SKILL / "scripts"))

import batch_runner  # noqa: E402


# ---------------------------------------------------------------------------
# load_targets_from_manifest / _from_file
# ---------------------------------------------------------------------------

def test_f11b_load_manifest_returns_sorted_ids():
    with tempfile.TemporaryDirectory() as tmp:
        m = Path(tmp) / "_notebook-manifest.json"
        m.write_text(json.dumps({
            "version": 1,
            "notebooks": {
                "zzz-22222222": {},
                "aaa-11111111": {},
                "mmm-33333333": {},
            },
        }), encoding="utf-8")
        targets = batch_runner.load_targets_from_manifest(m)
        assert targets == ["aaa-11111111", "mmm-33333333", "zzz-22222222"]


def test_f11b_load_manifest_missing_file_returns_empty_list():
    with tempfile.TemporaryDirectory() as tmp:
        targets = batch_runner.load_targets_from_manifest(Path(tmp) / "missing.json")
        assert targets == []


def test_f11b_load_file_strips_blanks_and_comments():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "batch.txt"
        p.write_text(
            "# notebooks to audit\n"
            "abc-12345678\n"
            "\n"
            "  def-87654321  \n"
            "# inline comment line\n"
            "ghi-abcdefgh\n",
            encoding="utf-8",
        )
        targets = batch_runner.load_targets_from_file(p)
        assert targets == ["abc-12345678", "def-87654321", "ghi-abcdefgh"]


# ---------------------------------------------------------------------------
# run_batch
# ---------------------------------------------------------------------------

class _FakeProc:
    def __init__(self, *, returncode, stdout="", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def test_f11b_run_batch_worst_case_exit_wins():
    """Target A passes (0), target B fails destructive (4). Overall = 4."""
    results_map = {
        "abc-12345678": _FakeProc(returncode=0, stdout='{"exit_code":0}'),
        "def-87654321": _FakeProc(returncode=4, stdout='{"exit_code":4}'),
    }

    def fake_run(cmd, *a, **kw):
        target = cmd[2]  # router is invoked as: python router.py <target> ...
        return results_map[target]

    with patch("batch_runner.subprocess.run", side_effect=fake_run):
        err = io.StringIO()
        with redirect_stderr(err):
            outcome = batch_runner.run_batch(
                targets=list(results_map),
                passthrough=[],
                workers=2,
                quiet=False,
            )
    assert outcome["overall_exit_code"] == 4
    assert len(outcome["results"]) == 2


def test_f11b_run_batch_exception_in_one_target_does_not_kill_batch():
    def fake_run(cmd, *a, **kw):
        target = cmd[2]
        if target == "bad-12345678":
            raise RuntimeError("boom")
        return _FakeProc(returncode=0, stdout='{"exit_code":0}')

    with patch("batch_runner.subprocess.run", side_effect=fake_run):
        err = io.StringIO()
        with redirect_stderr(err):
            outcome = batch_runner.run_batch(
                targets=["abc-12345678", "bad-12345678", "def-87654321"],
                passthrough=[],
                workers=1,
                quiet=False,
            )
    # Overall = 5 (batch driver error is worse than 0).
    assert outcome["overall_exit_code"] == 5
    # Every target has a result even though one exploded.
    assert len(outcome["results"]) == 3


def test_f11b_run_batch_quiet_emits_one_summary_per_target():
    def fake_run(cmd, *a, **kw):
        target = cmd[2]
        return _FakeProc(returncode=0, stdout=json.dumps({
            "event": "audit",
            "notebook_id": target,
            "exit_code": 0,
        }))

    out = io.StringIO()
    with patch("batch_runner.subprocess.run", side_effect=fake_run):
        with redirect_stdout(out):
            outcome = batch_runner.run_batch(
                targets=["abc-12345678", "def-87654321"],
                passthrough=[],
                workers=2,
                quiet=True,
            )
    # Each target gets a batch_item JSON line.
    lines = [json.loads(ln) for ln in out.getvalue().splitlines() if ln.strip()]
    batch_items = [ln for ln in lines if ln.get("event") == "batch_item"]
    assert len(batch_items) == 2
    assert outcome["overall_exit_code"] == 0


def test_f11b_run_batch_empty_targets_returns_exit_2():
    outcome = batch_runner.run_batch(targets=[], passthrough=[], workers=2)
    assert outcome["overall_exit_code"] == 2


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def test_f11b_cli_all_no_notebooks_exits_2():
    with tempfile.TemporaryDirectory() as tmp:
        m = Path(tmp) / "_notebook-manifest.json"
        m.write_text('{"version": 1, "notebooks": {}}', encoding="utf-8")
        err = io.StringIO()
        with redirect_stderr(err):
            rc = batch_runner._main(["--all", "--manifest-path", str(m)])
        assert rc == 2
        assert "no notebooks" in err.getvalue()


def test_f11b_cli_batch_no_targets_exits_2():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "batch.txt"
        p.write_text("# only comments\n\n", encoding="utf-8")
        err = io.StringIO()
        with redirect_stderr(err):
            rc = batch_runner._main(["--batch", str(p)])
        assert rc == 2


def test_f11b_cli_batch_forwards_passthrough_flags():
    """--dry-run and --skip-orphans must reach the router command line."""
    captured: list[list[str]] = []

    def fake_run(cmd, *a, **kw):
        captured.append(list(cmd))
        return _FakeProc(returncode=0, stdout="")

    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "batch.txt"
        p.write_text("abc-12345678\n", encoding="utf-8")
        out, err = io.StringIO(), io.StringIO()
        with patch("batch_runner.subprocess.run", side_effect=fake_run):
            with redirect_stdout(out), redirect_stderr(err):
                rc = batch_runner._main([
                    "--batch", str(p),
                    "--workers", "1",
                    "--skip-orphans",
                    "--max-retry", "7",
                ])
        assert rc == 0
        dispatched = captured[0]
        # Router is the second argv entry after python executable.
        assert "router.py" in dispatched[1]
        assert "--skip-orphans" in dispatched
        assert "--max-retry" in dispatched and "7" in dispatched


TESTS = [
    test_f11b_load_manifest_returns_sorted_ids,
    test_f11b_load_manifest_missing_file_returns_empty_list,
    test_f11b_load_file_strips_blanks_and_comments,
    test_f11b_run_batch_worst_case_exit_wins,
    test_f11b_run_batch_exception_in_one_target_does_not_kill_batch,
    test_f11b_run_batch_quiet_emits_one_summary_per_target,
    test_f11b_run_batch_empty_targets_returns_exit_2,
    test_f11b_cli_all_no_notebooks_exits_2,
    test_f11b_cli_batch_no_targets_exits_2,
    test_f11b_cli_batch_forwards_passthrough_flags,
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
