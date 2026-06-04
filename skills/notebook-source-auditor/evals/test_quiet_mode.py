#!/usr/bin/env python3
"""F13 tests — --quiet cron-friendly mode in auditor + router.

Scenarios:
    - auditor.run --quiet --dry-run emits one JSON line on stdout
    - auditor.run --quiet suppresses [info]/[diff]/[ok] stderr prints
    - auditor.run --quiet still prints [error] to stderr
    - auditor.run --quiet --bootstrap emits the bootstrap-shape summary
    - auditor.run --quiet --rollback emits the rollback-shape summary
    - router._main --quiet propagates the flag to the auditor dispatch
    - router._main --quiet suppresses the [router] preflight stderr banner

Run: python3 evals/test_quiet_mode.py
"""
from __future__ import annotations

import io
import json
import subprocess
import sys
import tempfile
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

_HERE = Path(__file__).resolve().parent
_SKILL = _HERE.parent
sys.path.insert(0, str(_SKILL / "scripts"))
sys.path.insert(0, str(Path.home() / ".claude/skills/deep-research/scripts"))


def _capture_run(*, argv, fake_nbm=None):
    """Run `auditor.run(argv)` with captured stdout/stderr. Returns
    (rc, stdout_str, stderr_str)."""
    import auditor
    out, err = io.StringIO(), io.StringIO()
    patch_target = fake_nbm if fake_nbm is not None else {"title": "T", "sources": []}
    with redirect_stdout(out), redirect_stderr(err), patch(
        "auditor.list_notebook_sources", return_value=patch_target
    ):
        rc = auditor.run(argv)
    return rc, out.getvalue(), err.getvalue()


def _only_json_line(stdout: str) -> dict:
    """Confirm stdout contains exactly one JSON dict (F13 contract)."""
    lines = [ln for ln in stdout.splitlines() if ln.strip()]
    assert len(lines) == 1, f"expected exactly one stdout line, got {lines!r}"
    return json.loads(lines[0])


def test_f13_quiet_dry_run_emits_single_json_line():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "hashimoto-farmacologia"
        p.mkdir()
        rc, stdout, stderr = _capture_run(argv=[
            "--notebook", "nb-abcdefgh",
            "--pesquisas", str(p),
            "--quiet",
        ])
        assert rc == 3  # partial_bootstrap — manifest absent, no --bootstrap
        summary = _only_json_line(stdout)
        assert summary["event"] == "audit"
        assert summary["notebook_id"] == "nb-abcdefgh"
        assert summary["mode"] == "dry-run"
        assert summary["exit_code"] == 3
        assert "diff" in summary
        # stderr should carry [error] lines only (preflight/info are gated)
        assert "[info] notebook=" not in stderr
        assert "[diff]" not in stderr
        assert "[ok] report:" not in stderr


def test_f13_quiet_preserves_error_messages_on_stderr():
    """Even in quiet mode, hard errors must reach stderr so cron/launchd
    can persist them in its log — a silent failure is the worst thing a
    cron job can do."""
    import auditor
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        rc = auditor.run([
            "--notebook", "nb-abcdefgh",
            "--pesquisas", "/no/such/path",  # triggers [error] pesquisa path does not exist
            "--quiet",
        ])
    assert rc == 2
    assert "[error]" in err.getvalue()


def test_f13_quiet_bootstrap_summary_shape():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "hashimoto-farmacologia"
        p.mkdir()
        rc, stdout, _ = _capture_run(
            argv=[
                "--notebook", "nb-abcdefgh",
                "--pesquisas", str(p),
                "--bootstrap",
                "--apply",
                "--quiet",
            ],
            fake_nbm={
                "title": "Hashimoto",
                "sources": [
                    {"id": "s1", "title": "Paper A", "url": "https://pubmed.ncbi.nlm.nih.gov/1/"},
                ],
            },
        )
        assert rc == 0
        summary = _only_json_line(stdout)
        assert summary["event"] == "bootstrap"
        assert summary["notebook_id"] == "nb-abcdefgh"
        assert summary["created"] == 1
        assert summary["exit_code"] == 0


def test_f13_quiet_rollback_summary_shape():
    import manifest_backup
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        p = tmp / "hashimoto-farmacologia"
        p.mkdir()
        m = tmp / "_notebook-manifest.json"
        m.write_text('{"version": 1, "tag": "v1"}', encoding="utf-8")
        manifest_backup.create_backup(m)
        # Mutate so rollback has something to restore.
        m.write_text('{"version": 1, "tag": "v2"}', encoding="utf-8")

        rc, stdout, _ = _capture_run(argv=[
            "--notebook", "nb-abcdefgh",
            "--pesquisas", str(p),
            "--rollback",
            "--quiet",
        ])
        assert rc == 0
        summary = _only_json_line(stdout)
        assert summary["event"] == "rollback"
        assert summary["notebook_id"] == "nb-abcdefgh"
        assert summary["exit_code"] == 0
        assert summary["restored_from"].startswith("_notebook-manifest.backup-")
        # Manifest content must be back to v1.
        data = json.loads(m.read_text(encoding="utf-8"))
        assert data["tag"] == "v1"


# ---------------------------------------------------------------------------
# Router propagation
# ---------------------------------------------------------------------------

class _FakeCompleted:
    def __init__(self, *, returncode=0, stdout=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = ""


def _install_router_mock(preflight_sources: list[dict]):
    import router
    calls: list[list[str]] = []

    def fake_run(cmd, *a, **kw):
        calls.append(list(cmd))
        if len(cmd) >= 2 and cmd[0] == "notebooklm" and cmd[1] == "source":
            return _FakeCompleted(stdout=json.dumps({"sources": preflight_sources}))
        return _FakeCompleted(returncode=0)

    router.subprocess.run = fake_run  # type: ignore[attr-defined]
    return calls


def _dispatch(calls: list[list[str]]) -> list[str]:
    for c in calls:
        if "auditor.py" in " ".join(c):
            return c
    raise AssertionError(f"no auditor dispatch in {calls}")


def test_f13_router_quiet_passthrough_to_auditor():
    import importlib, router
    importlib.reload(router)
    calls = _install_router_mock([])
    err = io.StringIO()
    with redirect_stderr(err):
        rc = router._main([
            "abc-12345678",
            "--pesquisas", "/tmp/p",
            "--quiet",
        ])
    assert rc == 0
    disp = _dispatch(calls)
    assert "--quiet" in disp
    # Router's own [router] banner must also vanish under --quiet.
    assert "[router]" not in err.getvalue()


def test_f13_router_rollback_passthrough_without_pesquisas_fails_fast():
    """--rollback with no --pesquisas is a hard error at the router level
    so rollback never runs against the wrong manifest root."""
    import importlib, router
    importlib.reload(router)
    _install_router_mock([])
    err = io.StringIO()
    with redirect_stderr(err):
        rc = router._main([
            "abc-12345678",
            "--rollback",
        ])
    assert rc == 2
    assert "--pesquisas" in err.getvalue()


TESTS = [
    test_f13_quiet_dry_run_emits_single_json_line,
    test_f13_quiet_preserves_error_messages_on_stderr,
    test_f13_quiet_bootstrap_summary_shape,
    test_f13_quiet_rollback_summary_shape,
    test_f13_router_quiet_passthrough_to_auditor,
    test_f13_router_rollback_passthrough_without_pesquisas_fails_fast,
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
