#!/usr/bin/env python3
"""F10a tests for router.py — mode auto-detection + argv assembly.

We mock subprocess.run so we never touch the real notebooklm CLI. The router
calls subprocess.run twice:
    1. `notebooklm source list -n <id> --json` (preflight)
    2. `python auditor.py ... [--fix-captcha] [--apply]` (dispatch)

Tests assert the dispatched auditor command matches the expected flags.

Run: python3 evals/test_router.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_SKILL = _HERE.parent
sys.path.insert(0, str(_SKILL / "scripts"))

import router  # noqa: E402


class _FakeCompleted:
    def __init__(self, *, returncode=0, stdout=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = ""


def _install_subprocess_mock(preflight_sources: list[dict]):
    """Stub subprocess.run to return:
        - preflight call → JSON payload with `preflight_sources`
        - dispatch call → returncode 0 (not inspected beyond rc)
    Records every call so tests can assert the exact argv of the auditor dispatch.
    """
    calls: list[list[str]] = []

    def fake_run(cmd, *a, **kw):
        calls.append(list(cmd))
        if len(cmd) >= 2 and cmd[0] == "notebooklm" and cmd[1] == "source":
            payload = json.dumps({"sources": preflight_sources})
            return _FakeCompleted(stdout=payload)
        # dispatch path — signal auditor success
        return _FakeCompleted(returncode=0)

    router.subprocess.run = fake_run  # type: ignore[attr-defined]
    return calls


def _dispatch_cmd(calls: list[list[str]]) -> list[str]:
    """The dispatch call is the second invocation (non-notebooklm)."""
    for c in calls:
        if "auditor.py" in " ".join(c):
            return c
    raise AssertionError(f"no auditor.py dispatch found in {calls}")


def test_router_no_captcha_dispatches_standard_dry_run():
    calls = _install_subprocess_mock([
        {"id": "s1", "title": "Real paper", "url": "https://pubmed.ncbi.nlm.nih.gov/1/"},
    ])
    rc = router._main([
        "https://notebooklm.google.com/notebook/abc-123",
        "--pesquisas", "/tmp/p",
    ])
    assert rc == 0
    disp = _dispatch_cmd(calls)
    assert "--fix-captcha" not in disp, disp
    assert "--apply" not in disp, disp
    # the notebook target should be passed straight through
    assert "https://notebooklm.google.com/notebook/abc-123" in disp


def test_router_captcha_triggers_fix_captcha_mode():
    calls = _install_subprocess_mock([
        {"id": "c1", "title": "Checking your browser", "url": "https://x.com"},
        {"id": "s2", "title": "Real paper", "url": "https://pubmed.ncbi.nlm.nih.gov/2/"},
    ])
    rc = router._main([
        "abc-12345",
        "--pesquisas", "/tmp/p",
    ])
    assert rc == 0
    disp = _dispatch_cmd(calls)
    assert "--fix-captcha" in disp, disp
    assert "--apply" not in disp, disp  # dry-run default persists in v2 Fase A


def test_router_apply_flag_propagates():
    calls = _install_subprocess_mock([])  # no captcha
    rc = router._main([
        "abc-12345",
        "--pesquisas", "/tmp/p",
        "--apply",
    ])
    assert rc == 0
    disp = _dispatch_cmd(calls)
    assert "--apply" in disp


def test_router_force_mode_override():
    # Preflight says no captcha, but user forces fix-captcha.
    calls = _install_subprocess_mock([
        {"id": "s1", "title": "Real paper", "url": "https://x.com"},
    ])
    rc = router._main([
        "abc-12345",
        "--pesquisas", "/tmp/p",
        "--force-mode", "fix-captcha",
    ])
    assert rc == 0
    disp = _dispatch_cmd(calls)
    assert "--fix-captcha" in disp


def test_router_invalid_url_exit_2():
    router.subprocess.run = lambda *a, **k: _FakeCompleted(returncode=0)  # unused
    rc = router._main([
        "",  # invalid bare id/url
        "--pesquisas", "/tmp/p",
    ])
    assert rc == 2


def test_router_passes_through_advanced_flags():
    calls = _install_subprocess_mock([])
    rc = router._main([
        "abc-12345",
        "--pesquisas", "/tmp/p",
        "--audits-dir", "/tmp/a",
        "--skip-orphans",
        "--skip-duplicates",
        "--max-retry", "5",
    ])
    assert rc == 0
    disp = _dispatch_cmd(calls)
    for f in ["--audits-dir", "/tmp/a", "--skip-orphans", "--skip-duplicates"]:
        assert f in disp, disp
    # --max-retry 5 should appear as two adjacent tokens
    i = disp.index("--max-retry")
    assert disp[i + 1] == "5"


TESTS = [
    test_router_no_captcha_dispatches_standard_dry_run,
    test_router_captcha_triggers_fix_captcha_mode,
    test_router_apply_flag_propagates,
    test_router_force_mode_override,
    test_router_invalid_url_exit_2,
    test_router_passes_through_advanced_flags,
]


def main() -> int:
    import importlib
    passed = failed = 0
    for t in TESTS:
        # Reload router each test to reset subprocess monkeypatch.
        importlib.reload(router)
        globals()["router"] = sys.modules["router"]
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
