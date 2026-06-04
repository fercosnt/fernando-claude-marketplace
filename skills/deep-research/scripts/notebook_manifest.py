#!/usr/bin/env python3
"""NotebookLM manifest helper — dedup, atomic write, URL normalization, file lock.

The manifest lives at `{pesquisas_root}/_notebook-manifest.json` and is the
single source of truth for every source pushed to any NotebookLM notebook
owned by this user, across multiple pesquisas.

Design rules (enforced here):

    * Bootstrap — file auto-created with {version:1, notebooks:{}} if missing.
    * Canonical key priority: doi > url (normalized) > sha256 > title+author.
    * URL normalization: lowercase scheme+host, trailing slash stripped,
      tracking params removed (utm_*, fbclid, gclid, mc_cid, mc_eid, ref,
      ref_src, source), fragments dropped (except semantic #page=N), path
      case preserved.
    * Dedup: if canonical_key already exists in a notebook's sources[],
      update last_attempt_at/attempts/status; do NOT re-add.
    * File lock: lockfile `{manifest}.lock` holds PID; stale-PID locks are
      reclaimed. Always released in finally.
    * Atomic write: write to `{manifest}.tmp` then os.rename.
    * Never remove entries — the notebook-source-auditor handles removal.

Usage (library):

    from notebook_manifest import record_source, normalize_url

    record_source(
        manifest_path=Path("pesquisas/_notebook-manifest.json"),
        notebook_id="abc123",
        pesquisa_slug="glp1-hashimoto",
        pesquisas_root=Path("pesquisas/"),
        canonical_key="pmc:PMC12345",
        title="Full-text PMC12345",
        source_type="article",
        origin_pesquisa="glp1-hashimoto",
        status="ok",
        notebooklm_source_id="src_xyz",
        ingest_method="pdf_upload",
    )

Usage (CLI):

    python notebook_manifest.py init <pesquisas_root>
    python notebook_manifest.py show <pesquisas_root> [<notebook_id>]
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

MANIFEST_VERSION = 1

TRACKING_PARAMS = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "utm_id", "utm_name",
    "fbclid", "gclid", "msclkid", "dclid", "yclid",
    "mc_cid", "mc_eid",
    "ref", "ref_src", "source",
    "igshid", "s_cid", "spm", "_hsenc", "_hsmi", "hsCtaTracking",
}

SEMANTIC_FRAGMENT_RE = re.compile(r"^(?:page=\d+|section-\S+|sec-\S+|sec\d+)$", re.IGNORECASE)


def normalize_url(url: str) -> str:
    """Return canonical form of URL per the manifesto rules."""
    if not url:
        return ""
    try:
        parsed = urlparse(url.strip())
    except ValueError:
        return url.strip()

    scheme = (parsed.scheme or "http").lower()
    netloc = (parsed.hostname or "").lower()
    if parsed.port:
        # Keep non-default ports.
        default = 443 if scheme == "https" else 80
        if parsed.port != default:
            netloc = f"{netloc}:{parsed.port}"

    # Preserve path case (case-sensitive in many servers).
    path = parsed.path or ""
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")

    # Filter tracking params.
    params = [
        (k, v)
        for (k, v) in parse_qsl(parsed.query, keep_blank_values=False)
        if k.lower() not in TRACKING_PARAMS and not k.lower().startswith("utm_")
    ]
    query = urlencode(params, doseq=True)

    # Keep semantic fragments only.
    fragment = parsed.fragment or ""
    if fragment and not SEMANTIC_FRAGMENT_RE.match(fragment):
        fragment = ""

    return urlunparse((scheme, netloc, path, "", query, fragment))


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _is_pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True  # exists but not ours
    return True


class _FileLock:
    """PID-based file lock. Stale locks (dead PID) are reclaimed."""

    def __init__(self, lock_path: Path, *, timeout_s: float = 30.0, poll_s: float = 0.1):
        self.lock_path = lock_path
        self.timeout_s = timeout_s
        self.poll_s = poll_s

    def __enter__(self) -> "_FileLock":
        deadline = time.monotonic() + self.timeout_s
        while True:
            try:
                # O_EXCL fails if the file already exists.
                fd = os.open(str(self.lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(fd, str(os.getpid()).encode())
                os.close(fd)
                return self
            except FileExistsError:
                # Check if the holder is still alive.
                try:
                    holder = int(self.lock_path.read_text().strip() or "0")
                except (OSError, ValueError):
                    holder = 0
                if holder and not _is_pid_alive(holder):
                    # Stale lock — reclaim.
                    try:
                        self.lock_path.unlink()
                    except FileNotFoundError:
                        pass
                    continue
                if time.monotonic() > deadline:
                    raise TimeoutError(
                        f"could not acquire lock {self.lock_path} within {self.timeout_s}s "
                        f"(held by pid {holder})"
                    )
                time.sleep(self.poll_s)

    def __exit__(self, *exc) -> None:
        try:
            self.lock_path.unlink()
        except FileNotFoundError:
            pass


def _load_or_bootstrap(manifest_path: Path) -> dict:
    if not manifest_path.exists():
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        return {"version": MANIFEST_VERSION, "notebooks": {}}
    try:
        raw = manifest_path.read_text(encoding="utf-8")
        data = json.loads(raw) if raw.strip() else {}
    except (OSError, json.JSONDecodeError) as e:
        raise RuntimeError(f"manifest {manifest_path} is corrupt: {e}") from e
    if "notebooks" not in data:
        data["notebooks"] = {}
    data.setdefault("version", MANIFEST_VERSION)
    return data


def _atomic_write(manifest_path: Path, data: dict) -> None:
    tmp = manifest_path.with_suffix(manifest_path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, manifest_path)


def _ensure_notebook(data: dict, notebook_id: str, title: str | None = None) -> dict:
    nb = data["notebooks"].setdefault(
        notebook_id,
        {
            "title": title or notebook_id,
            "created_at": _now_iso(),
            "updated_at": _now_iso(),
            "pesquisas": [],
            "sources": [],
        },
    )
    if title and not nb.get("title"):
        nb["title"] = title
    return nb


def _touch_pesquisa(nb: dict, pesquisa_slug: str, pesquisas_root: Path) -> None:
    now = _now_iso()
    full = pesquisas_root / pesquisa_slug
    if pesquisas_root.is_absolute():
        resolved = full.resolve()
        try:
            # Prefer a cwd-relative path when the work_dir is inside cwd —
            # keeps the manifest portable across different checkouts.
            path = str(resolved.relative_to(Path.cwd().resolve()))
        except ValueError:
            # Work_dir lives outside cwd (e.g. /tmp/regression/...). Storing
            # the absolute path is informative and preserves the audit trail.
            # Raising here would lose the source — manifest is meant to be
            # a best-effort record across arbitrary pesquisas_root layouts.
            path = str(resolved)
    else:
        path = str(full)
    for entry in nb["pesquisas"]:
        if entry.get("slug") == pesquisa_slug:
            entry["last_delta_at"] = now
            return
    nb["pesquisas"].append({
        "slug": pesquisa_slug,
        "path": path,
        "added_at": now,
        "last_delta_at": now,
    })


def record_source(
    *,
    manifest_path: Path,
    notebook_id: str,
    pesquisa_slug: str,
    pesquisas_root: Path,
    canonical_key: str,
    title: str,
    source_type: str,
    origin_pesquisa: str,
    status: str = "ok",
    notebooklm_source_id: str | None = None,
    ingest_method: str = "url_direct",
    ingest_metadata: dict | None = None,
    error: str | None = None,
    notebook_title: str | None = None,
) -> dict:
    """Upsert a source into the manifest. Returns the source dict as stored."""
    if not canonical_key:
        raise ValueError("canonical_key is required")

    manifest_path = Path(manifest_path)
    lock_path = manifest_path.with_suffix(manifest_path.suffix + ".lock")

    with _FileLock(lock_path):
        data = _load_or_bootstrap(manifest_path)
        nb = _ensure_notebook(data, notebook_id, notebook_title)
        _touch_pesquisa(nb, pesquisa_slug, pesquisas_root)

        now = _now_iso()
        for src in nb["sources"]:
            if src.get("canonical_key") == canonical_key:
                # Update in place.
                src["last_attempt_at"] = now
                src["attempts"] = int(src.get("attempts", 0)) + 1
                src["status"] = status
                if notebooklm_source_id:
                    src["notebooklm_source_id"] = notebooklm_source_id
                if ingest_metadata:
                    merged = dict(src.get("ingest_metadata") or {})
                    merged.update({k: v for k, v in ingest_metadata.items() if v is not None})
                    src["ingest_metadata"] = merged
                if error:
                    src["last_error"] = error
                src["ingest_method"] = ingest_method
                nb["updated_at"] = now
                _atomic_write(manifest_path, data)
                return src

        new_src = {
            "canonical_key": canonical_key,
            "title": title,
            "type": source_type,
            "origin_pesquisa": origin_pesquisa,
            "added_at": now,
            "status": status,
            "last_attempt_at": now,
            "attempts": 1,
            "notebooklm_source_id": notebooklm_source_id,
            "ingest_method": ingest_method,
            "ingest_metadata": {k: v for k, v in (ingest_metadata or {}).items() if v is not None},
        }
        if error:
            new_src["last_error"] = error
        nb["sources"].append(new_src)
        nb["updated_at"] = now
        _atomic_write(manifest_path, data)
        return new_src


def lookup_source(manifest_path: Path, notebook_id: str, canonical_key: str) -> dict | None:
    manifest_path = Path(manifest_path)
    if not manifest_path.exists():
        return None
    with _FileLock(manifest_path.with_suffix(manifest_path.suffix + ".lock")):
        data = _load_or_bootstrap(manifest_path)
    nb = data.get("notebooks", {}).get(notebook_id)
    if not nb:
        return None
    for src in nb.get("sources", []):
        if src.get("canonical_key") == canonical_key:
            return src
    return None


def mark_deleted(
    *,
    manifest_path: Path,
    notebook_id: str,
    canonical_key: str,
    reason: str,
) -> dict | None:
    """Mark a source as deleted in the manifest. Preserves history.

    Unlike `record_source()`, this is destructive-by-intent — only the
    notebook-source-auditor skill should call this.

    Returns the updated source dict, or None if notebook/source not found.

    The source entry is NOT removed from the manifest — status flips to
    `deleted`, `deleted_at` and `deletion_reason` are set. Callers that
    need to distinguish active vs deleted should filter on status.
    """
    manifest_path = Path(manifest_path)
    lock_path = manifest_path.with_suffix(manifest_path.suffix + ".lock")

    with _FileLock(lock_path):
        data = _load_or_bootstrap(manifest_path)
        nb = data.get("notebooks", {}).get(notebook_id)
        if not nb:
            return None

        for src in nb.get("sources", []):
            if src.get("canonical_key") == canonical_key:
                now = _now_iso()
                src["status"] = "deleted"
                src["deleted_at"] = now
                src["deletion_reason"] = reason
                nb["updated_at"] = now
                _atomic_write(manifest_path, data)
                return src
        return None


def _cli_init(root: Path) -> int:
    path = root / "_notebook-manifest.json"
    if path.exists():
        print(f"[info] manifest already exists at {path}")
        return 0
    with _FileLock(path.with_suffix(path.suffix + ".lock")):
        _atomic_write(path, {"version": MANIFEST_VERSION, "notebooks": {}})
    print(f"[ok] initialized {path}")
    return 0


def _cli_show(root: Path, notebook_id: str | None) -> int:
    path = root / "_notebook-manifest.json"
    if not path.exists():
        print(f"[error] no manifest at {path}", file=sys.stderr)
        return 1
    data = _load_or_bootstrap(path)
    if notebook_id:
        nb = data.get("notebooks", {}).get(notebook_id)
        if not nb:
            print(f"[error] notebook {notebook_id} not in manifest", file=sys.stderr)
            return 1
        json.dump(nb, sys.stdout, ensure_ascii=False, indent=2)
    else:
        summary = {
            "version": data.get("version"),
            "notebooks": {
                nid: {
                    "title": nb.get("title"),
                    "pesquisas": [p["slug"] for p in nb.get("pesquisas", [])],
                    "source_count": len(nb.get("sources", [])),
                    "by_status": _count_by_status(nb.get("sources", [])),
                }
                for nid, nb in data.get("notebooks", {}).items()
            },
        }
        json.dump(summary, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


def _count_by_status(sources: list[dict]) -> dict[str, int]:
    out: dict[str, int] = {}
    for s in sources:
        out[s.get("status", "unknown")] = out.get(s.get("status", "unknown"), 0) + 1
    return out


def _main(argv: list[str]) -> int:
    if len(argv) < 3:
        print("usage: notebook_manifest.py (init|show) <pesquisas_root> [<notebook_id>]", file=sys.stderr)
        return 1
    cmd, root = argv[1], Path(argv[2])
    if cmd == "init":
        return _cli_init(root)
    if cmd == "show":
        nb_id = argv[3] if len(argv) > 3 else None
        return _cli_show(root, nb_id)
    print(f"unknown command: {cmd}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
