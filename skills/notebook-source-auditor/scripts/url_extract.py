#!/usr/bin/env python3
"""Parse a NotebookLM notebook identifier from a URL or a bare UUID.

Usage:
    python url_extract.py <url_or_id>

Accepts:
    https://notebooklm.google.com/notebook/<id>
    https://notebooklm.google.com/notebook/<id>?...
    <id>                              # already a raw id

Exit: 0 ok (prints id to stdout), 2 on malformed input.
"""
from __future__ import annotations

import re
import sys

# Matches `/notebook/<id>` where id is URL-safe; NotebookLM ids are
# typically uuid-like but we do not enforce uuid strictly — the CLI is
# the ultimate authority on whether the id exists.
_NBM_URL_RE = re.compile(
    r"notebooklm\.google\.com/notebook/([A-Za-z0-9_-]+)",
    re.IGNORECASE,
)

# A bare id: printable URL-safe chars, no slashes, no dots, min 8 chars.
_BARE_ID_RE = re.compile(r"^[A-Za-z0-9_-]{8,}$")


def extract_notebook_id(value: str) -> str:
    """Return the notebook_id from a URL or a bare id.

    Raises ValueError if the input cannot be parsed as either form.
    """
    if not value or not isinstance(value, str):
        raise ValueError("empty or non-string input")
    value = value.strip()

    # URL form first (wins over bare id if input happens to contain the URL).
    m = _NBM_URL_RE.search(value)
    if m:
        return m.group(1)

    # Bare id fallback.
    if _BARE_ID_RE.match(value):
        return value

    raise ValueError(
        f"cannot parse notebook id from {value!r}: expected a "
        f"notebooklm.google.com/notebook/<id> URL or a bare id"
    )


def _main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: url_extract.py <url_or_id>", file=sys.stderr)
        return 2
    try:
        print(extract_notebook_id(argv[1]))
        return 0
    except ValueError as e:
        print(f"[error] {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
