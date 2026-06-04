#!/usr/bin/env python3
"""F12: auto-discover pesquisa folders for a given notebook title.

When the user invokes `/notebook-source-auditor <url>` without `--pesquisas`,
the router calls into this module to:
    1. Scan a root for pesquisa candidates (subfolders with a PESQUISA-*.md,
       standalone .md files, or folders whose name looks like a slug)
    2. Extract each candidate's slug + title (title is the first H1 in the
       PESQUISA-*.md, falling back to the slug with underscores→spaces)
    3. Score similarity against the NotebookLM notebook title using
       tokenized Jaccard overlap
    4. Return a MatchResult that splits candidates into three tiers:
         auto        — score >= AUTO_MATCH_THRESHOLD (0.8), top N kept
         ambiguous   — AMBIGUOUS_MIN (0.5) <= score < AUTO_MATCH_THRESHOLD
         below       — score < AMBIGUOUS_MIN (dropped; reported as no-match
                       only when the auto + ambiguous tiers are both empty)

The router handles the interactive prompt for ambiguous matches — this
module is pure data + scoring, no I/O prompts. Keeps the scorer testable.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path


# Defaults. Every knob is override-able by the caller (router) so tests can
# point the scan at a temp dir without touching the real skill tree.
DEFAULT_PESQUISAS_ROOT = Path.home() / ".claude" / "skills" / "deep-research" / "pesquisas"
AUTO_MATCH_THRESHOLD = 0.8
AMBIGUOUS_MIN = 0.5
MAX_AUTO_MATCHES = 3

# Token-extraction heuristics. We deliberately keep stopwords tiny — a
# pesquisa slug "hashimoto" vs notebook title "Hashimoto's Thyroiditis" is
# already distinctive; stripping too much risks collisions between unrelated
# pesquisas ("projeto X" vs "projeto Y" collapse to a single token).
_TOKEN_RE = re.compile(r"[A-Za-zÀ-ÿ0-9]+", re.UNICODE)
_MIN_TOKEN_LEN = 3
_STOPWORDS = {
    # Portuguese connectives and articles.
    "de", "do", "da", "dos", "das", "em", "no", "na", "nos", "nas",
    "para", "por", "com", "sem", "sobre", "entre", "como", "que", "ou",
    "mas", "ao", "aos", "uma", "uns", "umas", "se",
    # English analogues.
    "the", "and", "for", "with", "from", "into", "onto", "this", "that",
    "these", "those", "its", "not", "but", "also",
    # Terms that show up in almost every medical pesquisa title and add no
    # discrimination power.
    "study", "studies", "review", "reviews", "paper", "papers", "article",
    "articles", "research", "pesquisa", "notebook",
}


@dataclass
class PesquisaCandidate:
    """A single discovered pesquisa. `path` is what we'd pass to
    `--pesquisas` in the resolved auditor call."""
    path: Path
    slug: str
    title: str
    score: float = 0.0
    # Tokens kept for debugging only — not part of the sort key.
    _tokens: set[str] = field(default_factory=set, repr=False)


@dataclass
class MatchResult:
    auto: list[PesquisaCandidate] = field(default_factory=list)
    ambiguous: list[PesquisaCandidate] = field(default_factory=list)
    scanned_count: int = 0
    scan_root: Path | None = None

    @property
    def has_auto(self) -> bool:
        return bool(self.auto)

    @property
    def needs_prompt(self) -> bool:
        """Router should prompt the user when no auto-match survived but
        there is at least one ambiguous candidate worth confirming."""
        return not self.auto and bool(self.ambiguous)

    @property
    def no_match(self) -> bool:
        """Zero candidates cleared the ambiguous threshold — caller should
        error out rather than force the user through a long pick-list."""
        return not self.auto and not self.ambiguous


# ---------------------------------------------------------------------------
# Token extraction and scoring
# ---------------------------------------------------------------------------

def tokenize(text: str) -> set[str]:
    """Lowercase, strip punctuation, drop stopwords and very short tokens."""
    if not text:
        return set()
    out: set[str] = set()
    for m in _TOKEN_RE.finditer(text.lower()):
        tok = m.group(0)
        if len(tok) < _MIN_TOKEN_LEN:
            continue
        if tok in _STOPWORDS:
            continue
        out.add(tok)
    return out


def jaccard(a: set[str], b: set[str]) -> float:
    """Symmetric overlap score in [0, 1]. Returns 0 when either side empty."""
    if not a or not b:
        return 0.0
    intersection = a & b
    union = a | b
    return len(intersection) / len(union)


# ---------------------------------------------------------------------------
# Scanning
# ---------------------------------------------------------------------------

_PESQUISA_GLOB = "PESQUISA-*.md"


def _extract_title_from_md(md_path: Path) -> str:
    """Return the first H1 line or the file stem as fallback."""
    try:
        with md_path.open("r", encoding="utf-8", errors="ignore") as f:
            for raw in f:
                line = raw.strip()
                if line.startswith("# "):
                    return line[2:].strip()
                # Cheap safety net: if we've scanned the first 50 lines and
                # found no H1, give up. Stops us pulling a 10MB file into memory
                # just to learn there is no heading.
                if f.tell() > 10_000:
                    break
    except OSError:
        pass
    return md_path.stem


def _slug_from_path(p: Path) -> str:
    return p.stem if p.is_file() else p.name


def scan_pesquisas(root: Path) -> list[PesquisaCandidate]:
    """Enumerate candidates under `root`.

    Two shapes are supported:
        1. `<root>/<slug>/PESQUISA-*.md` — canonical folder layout
        2. `<root>/<slug>.md` — standalone file (legacy)

    Hidden paths and names starting with `_` (reserved for audit output like
    `_audits/` and the manifest) are skipped.
    """
    candidates: list[PesquisaCandidate] = []
    if not root.exists() or not root.is_dir():
        return candidates

    for child in sorted(root.iterdir()):
        name = child.name
        if name.startswith(".") or name.startswith("_"):
            continue

        if child.is_dir():
            matches = sorted(child.glob(_PESQUISA_GLOB))
            if matches:
                title_source = matches[0]
                title = _extract_title_from_md(title_source)
            else:
                # Folder without canonical PESQUISA file — still index so the
                # user gets a shot at picking it manually, but title = slug.
                title = name.replace("-", " ").replace("_", " ")
            slug = _slug_from_path(child)
            candidates.append(PesquisaCandidate(path=child, slug=slug, title=title))
        elif child.is_file() and child.suffix.lower() == ".md":
            title = _extract_title_from_md(child)
            slug = _slug_from_path(child)
            candidates.append(PesquisaCandidate(path=child, slug=slug, title=title))

    return candidates


# ---------------------------------------------------------------------------
# Matching
# ---------------------------------------------------------------------------

def _candidate_tokens(c: PesquisaCandidate) -> set[str]:
    """Combine slug and title tokens — slug words often carry the domain
    ('hashimoto', 'glp1'), title words carry the longer phrasing. Union
    gives both a chance to match the notebook title."""
    return tokenize(c.slug.replace("-", " ").replace("_", " ")) | tokenize(c.title)


def match_pesquisas(
    *,
    notebook_title: str,
    candidates: list[PesquisaCandidate],
    auto_threshold: float = AUTO_MATCH_THRESHOLD,
    ambiguous_min: float = AMBIGUOUS_MIN,
    max_auto: int = MAX_AUTO_MATCHES,
    scan_root: Path | None = None,
) -> MatchResult:
    """Score every candidate against `notebook_title` and bucket them.

    Scores are attached in-place so the caller can surface them to the user
    (ambiguous prompts read better when they show the score).
    """
    nb_tokens = tokenize(notebook_title)
    scored: list[PesquisaCandidate] = []
    for c in candidates:
        c._tokens = _candidate_tokens(c)
        c.score = jaccard(nb_tokens, c._tokens)
        scored.append(c)

    scored.sort(key=lambda x: (-x.score, x.slug))
    auto = [c for c in scored if c.score >= auto_threshold][:max_auto]
    ambiguous = [c for c in scored if ambiguous_min <= c.score < auto_threshold]

    return MatchResult(
        auto=auto,
        ambiguous=ambiguous,
        scanned_count=len(candidates),
        scan_root=scan_root,
    )


def autodiscover(
    *,
    notebook_title: str,
    root: Path | None = None,
) -> MatchResult:
    """Convenience wrapper: scan the default (or caller-provided) root and
    return a MatchResult. The router uses this as its only public hook."""
    r = Path(root) if root is not None else DEFAULT_PESQUISAS_ROOT
    candidates = scan_pesquisas(r)
    return match_pesquisas(
        notebook_title=notebook_title,
        candidates=candidates,
        scan_root=r,
    )
