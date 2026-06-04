#!/usr/bin/env python3
"""F9: load env vars from `~/.claude/skills/notebook-source-auditor/.env`.

The skill and its upstream (sci_fetch, NCBI client, Unpaywall client,
OpenAlex, Semantic Scholar) consult a handful of env vars for API keys and
contact emails. Requiring users to `export` them in `~/.zshrc` ran into a
hard block observed in Phase 5 — the Claude Code permission hook refused
to edit the shell rc file. F9 sidesteps that: the skill reads a per-user
dotenv file it owns (chmod 600) and merges the contents into `os.environ`
at boot.

Semantics
---------
- File format: `KEY=VALUE` per line. Blank lines and `#`-prefixed lines
  are ignored. Leading/trailing whitespace is stripped. Surrounding single
  or double quotes on VALUE are removed. `export KEY=VALUE` is accepted
  (the leading `export ` is stripped).
- Keys already present in `os.environ` are NOT overridden. Explicit
  exports in the caller's shell always win — consistent with every
  mainstream dotenv library. This also makes tests hermetic: setting an
  env var in the test process keeps its value.
- Missing file is a silent no-op (returns empty list). This is the
  expected state for fresh installs — callers print a one-line hint the
  first time they need a missing key.
- Permissions: if the file exists and is world- or group-readable, we
  call `chmod 600` on it. Failure to chmod is a warning, not fatal.

Supported keys
--------------
(listed for documentation — this module does not validate key names)
    NCBI_API_KEY            — raises PubMed/PMC rate limits from 3 to 10 rps
    UNPAYWALL_EMAIL         — required by Unpaywall API
    OPENALEX_EMAIL          — polite-pool header for OpenAlex
    SEMANTIC_SCHOLAR_API_KEY — raises S2 rate limit off the anonymous tier
"""
from __future__ import annotations

import os
import stat
import sys
from pathlib import Path


DEFAULT_ENV_PATH = Path.home() / ".claude" / "skills" / "notebook-source-auditor" / ".env"
WORLD_GROUP_READABLE = stat.S_IRGRP | stat.S_IROTH | stat.S_IWGRP | stat.S_IWOTH


def parse_env_file(path: Path) -> dict[str, str]:
    """Parse a dotenv-style file. Returns {KEY: VALUE}."""
    result: dict[str, str] = {}
    try:
        raw = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return result
    for line_no, line in enumerate(raw.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        # Accept both `KEY=VALUE` and `export KEY=VALUE` for convenience —
        # users migrating from a shell rc file paste either form.
        if stripped.startswith("export "):
            stripped = stripped[len("export "):].lstrip()
        if "=" not in stripped:
            # Malformed line — skip quietly but record so callers can warn.
            result.setdefault("__warnings__", "")
            result["__warnings__"] += f"L{line_no}: no '=' sign; "
            continue
        key, _, value = stripped.partition("=")
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        if not key:
            continue
        result[key] = value
    return result


def ensure_restrictive_perms(path: Path) -> bool:
    """chmod 600 if `path` is group/world readable. Returns True when the
    file mode was changed (or already restrictive), False on error."""
    try:
        st = path.stat()
    except OSError:
        return False
    if st.st_mode & WORLD_GROUP_READABLE:
        try:
            path.chmod(0o600)
            return True
        except OSError as e:
            print(f"[warn] could not chmod 600 {path}: {e}", file=sys.stderr)
            return False
    return True


def apply_env_file(path: Path | None = None, *, override: bool = False) -> list[str]:
    """Merge parsed env file into os.environ. Returns keys actually applied.

    `override=False` (default) mirrors dotenv convention: shell exports
    win over file contents. Pass `override=True` only in tests that
    explicitly need to replay the file.
    """
    p = Path(path) if path is not None else DEFAULT_ENV_PATH
    if not p.exists():
        return []
    ensure_restrictive_perms(p)
    parsed = parse_env_file(p)
    warnings = parsed.pop("__warnings__", None)
    if warnings:
        print(f"[warn] {p}: {warnings.strip(' ;')}", file=sys.stderr)
    applied: list[str] = []
    for key, value in parsed.items():
        if not override and key in os.environ:
            continue
        os.environ[key] = value
        applied.append(key)
    return applied


def boot() -> list[str]:
    """Convenience entry for CLI scripts. Prints a debug line when any keys
    were loaded so the user can confirm the file was picked up."""
    applied = apply_env_file()
    if applied:
        # Only surface key names — never the values.
        print(f"[env] loaded {len(applied)} var(s) from {DEFAULT_ENV_PATH}: {', '.join(sorted(applied))}",
              file=sys.stderr)
    return applied


if __name__ == "__main__":
    # Manual invocation: report what would be loaded without actually
    # mutating os.environ (useful for `notebook-source-auditor env-check`).
    p = DEFAULT_ENV_PATH
    if not p.exists():
        print(f"[info] no env file at {p}; create one to enable dotenv loading")
        sys.exit(0)
    print(f"[info] env file: {p}")
    parsed = parse_env_file(p)
    parsed.pop("__warnings__", None)
    for k in sorted(parsed):
        print(f"  {k}=(hidden)")
    print(f"[info] {len(parsed)} var(s) would be applied")
