"""Local cache for sci_fetch pipeline with per-kind TTL (stdlib only).

Layout:
    ~/.cache/deep-research-sci/
    |-- pmid/33567185.txt                    (TTL 365d)
    |-- pmcid/PMC7054893.txt                 (TTL 365d)
    |-- doi/10.1089_thy.2014.0028.json       (TTL 30d)
    |-- pdf/<sha256-16>.pdf                  (TTL 365d)
    |-- s2/doi_10.1089_thy.2014.0028.json    (TTL 90d)
    `-- errors/
        |-- doi/10.1089_thy.2014.0028.json   (TTL 7d)
        `-- pmcid/PMC9999999.json

TTL is enforced by comparing mtime to now. Atomic write via .tmp + os.replace.
Corrupt JSON files are renamed to .corrupt-<ts>.json and treated as miss.

Env:
    DR_SCI_CACHE_ROOT   override default ~/.cache/deep-research-sci
    DR_SCI_NO_CACHE=1   bypass entirely (get always returns None, put is no-op)
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Optional


CACHE_ROOT_ENV = "DR_SCI_CACHE_ROOT"
NO_CACHE_ENV = "DR_SCI_NO_CACHE"

TTL_DEFAULTS = {
    "pmid": 365,
    "pmcid": 365,
    "pmc_link": 365,
    "doi": 30,
    "pdf": 365,
    "s2": 90,
    "openalex": 90,
    "biorxiv": 30,
    "errors": 7,
}

EXT_BY_KIND = {
    "pmid": "txt",
    # pmcid stores {"title": str, "text": str} — structured so callers can
    # reconstruct the tuple returned by pmc_fulltext.fetch_fulltext().
    "pmcid": "json",
    # pmc_link stores {"pmcid": "PMC1234"|null} — result of the elink
    # PMID→PMCID resolution, keyed by the source PMID.
    "pmc_link": "json",
    "doi": "json",
    "pdf": "pdf",
    "s2": "json",
    "openalex": "json",
    "biorxiv": "json",
    "errors": "json",
}


def _disabled() -> bool:
    return os.environ.get(NO_CACHE_ENV) == "1"


def cache_root() -> Path:
    override = os.environ.get(CACHE_ROOT_ENV)
    if override:
        return Path(override).expanduser()
    return Path.home() / ".cache" / "deep-research-sci"


def _safe_key(key: str) -> str:
    # Keep alnum, dot, dash, underscore; replace everything else with underscore.
    out = []
    for ch in key:
        if ch.isalnum() or ch in ".-_":
            out.append(ch)
        else:
            out.append("_")
    safe = "".join(out).strip("_.")
    return safe or "empty"


def cache_path(kind: str, key: str, *, error: bool = False) -> Path:
    if kind not in EXT_BY_KIND and not error:
        raise ValueError(f"unknown cache kind: {kind}")
    ext = "json" if error else EXT_BY_KIND[kind]
    base = cache_root()
    if error:
        return base / "errors" / kind / f"{_safe_key(key)}.{ext}"
    return base / kind / f"{_safe_key(key)}.{ext}"


def _is_fresh(path: Path, ttl_days: int) -> bool:
    if ttl_days <= 0:
        return False  # 0 / negative = always expired (useful in tests)
    try:
        age = time.time() - path.stat().st_mtime
    except FileNotFoundError:
        return False
    return age <= ttl_days * 86400


def _atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # Unique tmp name avoids races when multiple threads write the same key.
    import tempfile
    fd, tmp_name = tempfile.mkstemp(
        dir=path.parent, prefix=path.name + ".", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_name, path)
    except Exception:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def _rename_corrupt(path: Path) -> None:
    ts = int(time.time())
    try:
        path.rename(path.with_suffix(path.suffix + f".corrupt-{ts}"))
    except OSError:
        pass


def cache_get(
    kind: str,
    key: str,
    *,
    ttl_days: Optional[int] = None,
    binary: bool = False,
) -> Optional[bytes] | Optional[str]:
    """Return cached value or None (miss/expired/corrupt/disabled).

    binary=True returns bytes; otherwise returns decoded string.
    """
    if _disabled():
        return None
    if ttl_days is None:
        ttl_days = TTL_DEFAULTS.get(kind, 30)
    path = cache_path(kind, key)
    if not _is_fresh(path, ttl_days):
        return None
    try:
        raw = path.read_bytes()
    except OSError:
        return None
    if binary:
        return raw
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        _rename_corrupt(path)
        return None


def cache_put(
    kind: str,
    key: str,
    content,
    *,
    binary: bool = False,
) -> Optional[Path]:
    """Write content to cache atomically. Returns path written, or None if disabled."""
    if _disabled():
        return None
    path = cache_path(kind, key)
    if binary:
        data = content if isinstance(content, (bytes, bytearray)) else bytes(content)
    else:
        if isinstance(content, (dict, list)):
            data = json.dumps(content, ensure_ascii=False).encode("utf-8")
        elif isinstance(content, bytes):
            data = content
        else:
            data = str(content).encode("utf-8")
    _atomic_write(path, data)
    return path


def cache_get_json(kind: str, key: str, *, ttl_days: Optional[int] = None) -> Optional[dict]:
    raw = cache_get(kind, key, ttl_days=ttl_days)
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        _rename_corrupt(cache_path(kind, key))
        return None


def cache_get_error(
    kind: str, key: str, *, ttl_days: Optional[int] = None
) -> Optional[dict]:
    """Return cached error record or None.

    Error record shape: {"status": "<code>", "cached_at": "<iso>", "ttl_days": <int>, ...}.
    Separate TTL per call; default is TTL_DEFAULTS["errors"] (7d).
    """
    if _disabled():
        return None
    if ttl_days is None:
        ttl_days = TTL_DEFAULTS["errors"]
    path = cache_path(kind, key, error=True)
    if not _is_fresh(path, ttl_days):
        return None
    try:
        raw = path.read_bytes()
    except OSError:
        return None
    try:
        return json.loads(raw.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        _rename_corrupt(path)
        return None


def cache_put_error(
    kind: str,
    key: str,
    status: str,
    *,
    ttl_days: Optional[int] = None,
    extra: Optional[dict] = None,
) -> Optional[Path]:
    if _disabled():
        return None
    if ttl_days is None:
        ttl_days = TTL_DEFAULTS["errors"]
    record = {
        "status": status,
        "cached_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "ttl_days": ttl_days,
    }
    if extra:
        record.update(extra)
    path = cache_path(kind, key, error=True)
    _atomic_write(path, json.dumps(record, ensure_ascii=False).encode("utf-8"))
    return path


def cache_clear(
    *,
    before_date: Optional[float] = None,
    kinds: Optional[list[str]] = None,
) -> int:
    """Delete cache entries.

    before_date: Unix timestamp; entries with mtime < before_date are deleted.
                 None means delete everything (respecting kinds filter).
    kinds: restrict to these kinds; None means all kinds + errors.

    Returns number of files removed.
    """
    base = cache_root()
    if not base.exists():
        return 0

    targets: list[Path] = []
    if kinds is None:
        targets.append(base)
    else:
        for k in kinds:
            targets.append(base / k)
            targets.append(base / "errors" / k)

    removed = 0
    for root in targets:
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if not p.is_file():
                continue
            if before_date is not None and p.stat().st_mtime >= before_date:
                continue
            try:
                p.unlink()
                removed += 1
            except OSError:
                pass
    return removed


def _human_size(num: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if num < 1024:
            return f"{num:.1f}{unit}"
        num /= 1024
    return f"{num:.1f}TB"


def cache_stats() -> dict:
    base = cache_root()
    stats: dict = {"root": str(base), "exists": base.exists(), "kinds": {}}
    if not base.exists():
        return stats
    total_bytes = 0
    total_files = 0
    for kind_dir in sorted(base.iterdir()):
        if not kind_dir.is_dir() or kind_dir.name == "errors":
            continue
        kind_bytes = 0
        kind_files = 0
        for p in kind_dir.rglob("*"):
            if p.is_file():
                kind_bytes += p.stat().st_size
                kind_files += 1
        stats["kinds"][kind_dir.name] = {"files": kind_files, "size": _human_size(kind_bytes)}
        total_bytes += kind_bytes
        total_files += kind_files
    errors_dir = base / "errors"
    if errors_dir.exists():
        err_bytes = 0
        err_files = 0
        for p in errors_dir.rglob("*"):
            if p.is_file():
                err_bytes += p.stat().st_size
                err_files += 1
        stats["errors"] = {"files": err_files, "size": _human_size(err_bytes)}
        total_bytes += err_bytes
        total_files += err_files
    stats["total"] = {"files": total_files, "size": _human_size(total_bytes)}
    return stats


def _main(argv: list[str]) -> int:
    """CLI for introspection: stats, clear."""
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(
            "usage: _cache.py stats\n"
            "       _cache.py clear [--before YYYY-MM-DD] [--kind <kind> ...]",
            file=__import__("sys").stderr,
        )
        return 1
    import sys
    cmd = argv[1]
    if cmd == "stats":
        json.dump(cache_stats(), sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0
    if cmd == "clear":
        before = None
        kinds: list[str] = []
        i = 2
        while i < len(argv):
            a = argv[i]
            if a == "--before" and i + 1 < len(argv):
                from datetime import datetime
                before = datetime.strptime(argv[i + 1], "%Y-%m-%d").timestamp()
                i += 2
            elif a == "--kind" and i + 1 < len(argv):
                kinds.append(argv[i + 1])
                i += 2
            else:
                print(f"unknown arg: {a}", file=sys.stderr)
                return 1
        n = cache_clear(before_date=before, kinds=kinds or None)
        print(f"removed {n} files")
        return 0
    print(f"unknown command: {cmd}", file=__import__("sys").stderr)
    return 1


if __name__ == "__main__":
    import sys
    sys.exit(_main(sys.argv))
