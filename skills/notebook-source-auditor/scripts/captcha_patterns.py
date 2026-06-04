#!/usr/bin/env python3
"""F15: expanded regex for detecting captcha / access-denied pages saved as
NotebookLM sources.

Phase 5 (2026-04-23) validation against the Hashimoto notebook uncovered
48/125 sources (38%) that were Cloudflare challenge pages or publisher
walls saved by deep-research v2 before the fix. The v1 regex only caught a
subset; this module centralizes the expanded list so both the auditor
(F7 --fix-captcha) and the standalone cleanup_captcha_sources.py use the
same patterns.

New patterns added in v2 (vs v1 cleanup script):
    - "Access Denied"
    - "403 Forbidden" / "Error 403"
    - "Cloudflare"
    - "Attention Required"
    - "Please Wait"
    - "Security Check"
    - "Verify you are human"
    - "Sage Journals: Discover world-class research" (Sage publisher wall)
"""
from __future__ import annotations

import re

# Case-insensitive, single alternation — each branch is a known captcha /
# access-denied title. Ordered roughly by observed frequency in Phase 5.
CAPTCHA_PATTERNS = re.compile(
    r"("
    r"checking your browser"
    r"|recaptcha"
    r"|just a moment"
    r"|access denied"
    r"|attention required"
    r"|cloudflare"
    r"|error\s*40[13]"
    r"|403\s*forbidden"
    r"|^forbidden\b"
    r"|please\s*wait"
    r"|security\s*check"
    r"|verify\s*you\s*are\s*human"
    r"|sage\s*journals?:\s*discover\s*world.class\s*research"
    r")",
    re.IGNORECASE,
)


def is_captcha_title(title: str | None) -> bool:
    """True when the source title looks like a captcha / access-denied page.

    Defensive: accepts None / empty strings (returns False) so callers can
    pass raw NBM source dicts without pre-filtering.
    """
    if not title:
        return False
    return bool(CAPTCHA_PATTERNS.search(title))


def filter_captcha_sources(sources: list[dict]) -> list[dict]:
    """Return the subset of NBM source dicts whose title matches a captcha
    pattern. Each source must have `title` (str) — other keys are preserved.
    """
    return [s for s in sources if is_captcha_title(s.get("title"))]
