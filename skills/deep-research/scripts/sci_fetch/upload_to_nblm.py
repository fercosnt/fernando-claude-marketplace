#!/usr/bin/env python3
"""Orchestrator: classify URLs, fetch content, upload to NotebookLM, write manifest.

Usage:
    python upload_to_nblm.py \\
        --urls <path-to-urls.txt> \\
        --notebook <NB_ID> \\
        --pesquisa <pesquisa-slug> \\
        --pesquisas-root <path-to-pesquisas-dir> \\
        [--work-dir <path>] \\
        [--skip-upload] \\
        [--no-cache] \\
        [--invalidate-cache-before YYYY-MM-DD] \\
        [--serial | --max-parallel N] \\
        [--from-auditor]

Pipeline (v2):
    1. Classify each URL via classify_url.classify
    2. Partition into NCBI / Academic / Generic buckets
    3. Fetch concurrently via three thread pools (respecting per-API token buckets)
    4. A single uploader thread drains a queue and posts to NotebookLM serially
       (the CLI is not thread-safe) + writes to _notebook-manifest.json
    5. Emit JSON summary to stdout

Flags:
    --no-cache                        set DR_SCI_NO_CACHE=1 so every handler bypasses the local cache
    --invalidate-cache-before DATE    prune cache entries older than DATE (YYYY-MM-DD) before running
    --serial                          disable pools (v1-like serial loop, useful for debugging)
    --max-parallel N                  override pool sizes; split 30% NCBI / 30% academic / 40% generic

Exit code: 0 ok, 1 fatal (bad args, missing tools).
"""
from __future__ import annotations

import argparse
import json
import os
import queue
import re
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Make sibling modules importable regardless of cwd.
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from classify_url import classify  # noqa: E402
import pubmed_abstract  # noqa: E402
import pmc_fulltext  # noqa: E402
import pmid_to_pmc  # noqa: E402
import unpaywall_resolver  # noqa: E402
import open_access_pdf  # noqa: E402
import biorxiv_fallback  # noqa: E402
import paper_scorer  # noqa: E402

# notebook_manifest lives one dir up.
sys.path.insert(0, str(HERE.parent))
import notebook_manifest as manifest  # noqa: E402


CAPTCHA_TITLE_RE = re.compile(
    r"checking your browser|recaptcha|access denied|just a moment",
    re.IGNORECASE,
)

# Default pool sizes (override via --max-parallel). Chosen so the NCBI bucket
# (3 req/s without API key) is comfortably saturated without 429.
DEFAULT_POOL_NCBI = 3
DEFAULT_POOL_ACADEMIC = 3
DEFAULT_POOL_GENERIC = 5


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _safe_slug(text: str, max_len: int = 60) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_")
    return s[:max_len] or "source"


def _nblm_add_file(file_path: Path, notebook_id: str) -> dict:
    cmd = ["notebooklm", "source", "add", str(file_path), "-n", notebook_id, "--json"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        return {"ok": False, "source_id": None, "error": result.stderr.strip() or "non-zero exit"}
    try:
        data = json.loads(result.stdout) if result.stdout.strip() else {}
    except json.JSONDecodeError:
        data = {}
    return {"ok": True, "source_id": data.get("id") or data.get("source_id"), "error": None}


def _nblm_list_sources(notebook_id: str) -> list[dict]:
    """Pull current NotebookLM sources. Returns [] on auth/exec failure (non-fatal)."""
    cmd = ["notebooklm", "source", "list", "-n", notebook_id, "--json"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        print(f"[warn] notebooklm source list failed: {result.stderr.strip()}", file=sys.stderr)
        return []
    try:
        data = json.loads(result.stdout) if result.stdout.strip() else {}
    except json.JSONDecodeError:
        return []
    if isinstance(data, dict):
        return data.get("sources") or data.get("data") or []
    if isinstance(data, list):
        return data
    return []


def _derive_canonical_for_source(source: dict) -> Optional[str]:
    """Best-effort canonical_key for a NotebookLM source dict.

    Mirrors the derivation used by notebook-source-auditor/retroactive_dedup
    so F8 skip-dupe stays aligned with the auditor's dedupe logic — without
    taking a cross-skill import dependency.
    """
    url = (source.get("url") or "").strip()
    if not url:
        return None
    try:
        cls = classify(url)
    except Exception:
        cls = {"type": "generic_web", "metadata": {}}
    ctype = cls.get("type")
    meta = cls.get("metadata") or {}
    if ctype == "pubmed" and meta.get("pmid"):
        return f"pmid:{meta['pmid']}"
    pmcid = meta.get("pmcid") or meta.get("pmc_id")
    if ctype == "pmc" and pmcid:
        return f"pmc:{pmcid}"
    if ctype == "doi" and meta.get("doi"):
        return f"doi:{meta['doi'].lower()}"
    try:
        return f"url:{manifest.normalize_url(url)}"
    except Exception:
        return None


def compute_present_canonical_keys(notebook_id: str) -> set[str]:
    """Return the set of canonical_keys currently present in the NotebookLM.

    Used by F8 skip-dupe: if a to-upload task's canonical is already here,
    skip the `notebooklm source add` call to prevent re-introducing the same
    paper in a different format (e.g., MARKDOWN after WEB_PAGE was kept by
    the auditor), which would trigger the dedupe↔readd loop observed in the
    Phase 5 validation (2026-04-23).
    """
    present: set[str] = set()
    for src in _nblm_list_sources(notebook_id):
        ck = _derive_canonical_for_source(src)
        if ck:
            present.add(ck)
    return present


def _nblm_add_url(url: str, notebook_id: str) -> dict:
    cmd = ["notebooklm", "source", "add", url, "-n", notebook_id, "--json"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        return {"ok": False, "source_id": None, "error": result.stderr.strip() or "non-zero exit"}
    try:
        data = json.loads(result.stdout) if result.stdout.strip() else {}
    except json.JSONDecodeError:
        data = {}
    return {"ok": True, "source_id": data.get("id") or data.get("source_id"), "error": None}


# -----------------------------------------------------------------------------
# Handler helpers (unchanged public behavior from v1; signatures kept stable
# for retrocompat with the `_handle_doi` tests).
# -----------------------------------------------------------------------------
def _handle_pubmed(url: str, pmid: str, work_dir: Path) -> tuple[Path | None, str | None]:
    try:
        pmc_result = pmid_to_pmc._resolve_batch([pmid])
    except Exception as e:
        print(f"[warn] elink for {pmid}: {e}", file=sys.stderr)
        pmc_result = {pmid: None}

    pmcid = pmc_result.get(pmid)
    if pmcid:
        try:
            title, text = pmc_fulltext.fetch_fulltext(pmcid)
            if len(text) >= pmc_fulltext.MIN_CONTENT_CHARS:
                out = work_dir / f"fulltext_{pmcid}.txt"
                out.write_text(
                    pmc_fulltext.format_output(pmcid, title, text), encoding="utf-8"
                )
                return out, f"pmc:{pmcid}"
        except Exception as e:
            print(f"[warn] PMC {pmcid}: {e}", file=sys.stderr)

    try:
        raw = pubmed_abstract.fetch_abstract(pmid)
        if len(raw) >= 100:
            out = work_dir / f"pubmed_{pmid}.txt"
            out.write_text(pubmed_abstract.format_output(pmid, raw), encoding="utf-8")
            return out, f"pmid:{pmid}"
    except Exception as e:
        print(f"[warn] abstract {pmid}: {e}", file=sys.stderr)
    return None, f"pmid:{pmid}"


def _handle_pmc(pmcid: str, work_dir: Path) -> tuple[Path | None, str]:
    try:
        title, text = pmc_fulltext.fetch_fulltext(pmcid)
        if len(text) < pmc_fulltext.MIN_CONTENT_CHARS:
            return None, f"pmc:{pmcid}"
        out = work_dir / f"fulltext_{pmcid}.txt"
        out.write_text(pmc_fulltext.format_output(pmcid, title, text), encoding="utf-8")
        return out, f"pmc:{pmcid}"
    except Exception as e:
        print(f"[warn] PMC {pmcid}: {e}", file=sys.stderr)
        return None, f"pmc:{pmcid}"


def _handle_doi(
    url: str,
    cls: dict,
    work_dir: Path,
    *,
    use_cache: bool = True,
    enable_biorxiv_fallback: bool = True,
) -> tuple[Path | None, str, dict]:
    """Try to resolve DOI to an OA PDF via Unpaywall, then bioRxiv preprint.

    Order:
        1. Unpaywall — if is_oa=true with oa_pdf_url, fetch + return
        2. bioRxiv/medRxiv — if Unpaywall said is_oa=false, try preprint fallback
        3. Manual bucket — caller falls back when this returns (None, _, {reason})
    """
    doi = cls["metadata"]["doi"]
    canonical = f"doi:{doi}"
    email = os.environ.get("UNPAYWALL_EMAIL")
    if not email:
        return None, canonical, {"reason": "UNPAYWALL_EMAIL nao setada — DOI nao resolvido"}

    try:
        result = unpaywall_resolver.resolve(doi, email, use_cache=use_cache)
    except Exception as e:
        return None, canonical, {"reason": f"Unpaywall error: {e}"}

    if result.get("is_oa") and result.get("oa_pdf_url"):
        pdf_path = work_dir / f"doi_{_safe_slug(doi)}.pdf"
        try:
            open_access_pdf.fetch(result["oa_pdf_url"], str(pdf_path))
        except open_access_pdf.NotAPDFError as e:
            return None, canonical, {
                "reason": f"Unpaywall OA URL mas nao retornou PDF (HTML fallback): {e.fallback_path}",
                "unpaywall_url": result["oa_pdf_url"],
            }
        except Exception as e:
            return None, canonical, {
                "reason": f"Falha baixando OA PDF: {e}",
                "unpaywall_url": result["oa_pdf_url"],
            }

        return pdf_path, canonical, {
            "unpaywall_host_type": result.get("host_type"),
            "unpaywall_pdf_url": result["oa_pdf_url"],
            "unpaywall_from_cache": result.get("from_cache"),
        }

    # Unpaywall said paywalled — try bioRxiv/medRxiv preprint as a last resort.
    if enable_biorxiv_fallback:
        try:
            preprint = biorxiv_fallback.find_preprint(doi, use_cache=use_cache)
        except Exception as e:
            preprint = None
            preprint_err = str(e)
        else:
            preprint_err = None

        if preprint and preprint.get("pdf_url"):
            pdf_path = work_dir / f"doi_{_safe_slug(doi)}_preprint.pdf"
            try:
                open_access_pdf.fetch(preprint["pdf_url"], str(pdf_path), use_cache=use_cache)
            except open_access_pdf.NotAPDFError as e:
                # Preprint server returned HTML — log and fall through to manual.
                return None, canonical, {
                    "reason": "DOI nao-OA; preprint encontrado mas URL nao retornou PDF",
                    "preprint_server": preprint.get("preprint_server"),
                    "preprint_pdf_url": preprint.get("pdf_url"),
                    "preprint_html_fallback": e.fallback_path,
                }
            except Exception as e:
                return None, canonical, {
                    "reason": f"DOI nao-OA; preprint encontrado mas falhou baixando: {e}",
                    "preprint_server": preprint.get("preprint_server"),
                    "preprint_pdf_url": preprint.get("pdf_url"),
                }

            return pdf_path, canonical, {
                "preprint_fallback": True,
                "preprint_server": preprint.get("preprint_server"),
                "preprint_version": preprint.get("version"),
                "preprint_doi": preprint.get("preprint_doi"),
                "preprint_pdf_url": preprint.get("pdf_url"),
                "unpaywall_checked": True,
            }

        meta = {
            "reason": "DOI nao-OA no Unpaywall; sem preprint em bioRxiv/medRxiv",
            "unpaywall_checked": True,
            "biorxiv_checked": True,
            "unpaywall_from_cache": result.get("from_cache"),
        }
        if preprint_err:
            meta["biorxiv_error"] = preprint_err
        return None, canonical, meta

    return None, canonical, {
        "reason": "DOI nao-OA no Unpaywall",
        "unpaywall_checked": True,
        "unpaywall_from_cache": result.get("from_cache"),
    }


# -----------------------------------------------------------------------------
# v2 parallel pipeline — classify → pool-fetch → queue-upload.
# -----------------------------------------------------------------------------
@dataclass
class UploadTask:
    url: str
    cls: dict
    file_path: Optional[Path]
    canonical: str
    ingest_method: str               # "pdf_upload" | "url_direct"
    url_norm: str
    metadata_meta: dict = field(default_factory=dict)
    manual_required_reason: Optional[str] = None  # when set, skip upload + log as manual
    manual_required_howto: Optional[str] = None
    download_error: Optional[str] = None
    # v3 academic scoring (optional). Populated by paper_scorer.score_paper()
    # when the URL has a DOI/PMID and --skip-scoring is not set.
    academic_score: Optional[dict] = None


NCBI_TYPES = ("pubmed", "pmc")
ACADEMIC_TYPES = ("doi",)
GENERIC_TYPES = ("gov_or_guideline", "blog_or_news", "generic_web", "cloudflare_known")


def _classify_and_partition(urls: list[str]):
    """Return (ncbi, academic, generic) lists of {url, cls, url_norm}."""
    ncbi, academic, generic = [], [], []
    for url in urls:
        cls = classify(url)
        url_norm = manifest.normalize_url(url)
        item = {"url": url, "cls": cls, "url_norm": url_norm}
        if cls["type"] in NCBI_TYPES:
            ncbi.append(item)
        elif cls["type"] in ACADEMIC_TYPES:
            academic.append(item)
        else:
            generic.append(item)
    return ncbi, academic, generic


def _maybe_score(
    *,
    doi: str | None,
    pmid: str | None,
    enable_scoring: bool,
    use_cache: bool,
    fetch_preprint: bool = True,
) -> Optional[dict]:
    """Wrapper around paper_scorer that swallows API failures (scorer is best-effort
    enrichment — it must never block the main pipeline)."""
    if not enable_scoring or not (doi or pmid):
        return None
    try:
        return paper_scorer.score_paper(
            doi=doi, pmid=pmid, use_cache=use_cache, fetch_preprint=fetch_preprint
        )
    except Exception as e:
        print(f"[warn] scorer failed for {doi or pmid}: {e}", file=sys.stderr)
        return None


def _worker_ncbi(
    item: dict,
    work_dir: Path,
    *,
    enable_scoring: bool = True,
    use_cache: bool = True,
) -> UploadTask:
    url, cls, url_norm = item["url"], item["cls"], item["url_norm"]
    try:
        if cls["type"] == "pubmed":
            fp, canonical = _handle_pubmed(url, cls["metadata"]["pmid"], work_dir)
        else:  # pmc
            fp, canonical = _handle_pmc(cls["metadata"]["pmcid"], work_dir)
    except Exception as e:
        return UploadTask(
            url=url, cls=cls, file_path=None,
            canonical=f"url:{url_norm}", ingest_method="url_direct",
            url_norm=url_norm, download_error=str(e),
        )
    ingest_method = "pdf_upload" if fp else "url_direct"

    pmid = cls["metadata"].get("pmid") if cls["type"] == "pubmed" else None
    score = _maybe_score(doi=None, pmid=pmid, enable_scoring=enable_scoring, use_cache=use_cache)

    return UploadTask(
        url=url, cls=cls, file_path=fp,
        canonical=canonical or f"url:{url_norm}",
        ingest_method=ingest_method, url_norm=url_norm,
        academic_score=score,
    )


def _worker_academic(
    item: dict,
    work_dir: Path,
    use_cache: bool,
    *,
    enable_scoring: bool = True,
    enable_biorxiv_fallback: bool = True,
) -> UploadTask:
    url, cls, url_norm = item["url"], item["cls"], item["url_norm"]
    fp, canonical, doi_meta = _handle_doi(
        url, cls, work_dir,
        use_cache=use_cache,
        enable_biorxiv_fallback=enable_biorxiv_fallback,
    )
    doi = cls["metadata"].get("doi")
    # If preprint fallback already fetched a bioRxiv version, the scorer can
    # reuse the cached result via biorxiv_fallback's TTL — no extra API hit.
    score = _maybe_score(doi=doi, pmid=None, enable_scoring=enable_scoring, use_cache=use_cache)

    if fp:
        return UploadTask(
            url=url, cls=cls, file_path=fp, canonical=canonical,
            ingest_method="pdf_upload", url_norm=url_norm,
            metadata_meta=doi_meta,
            academic_score=score,
        )
    # No OA PDF → manual bucket with the reason surfaced from _handle_doi.
    return UploadTask(
        url=url, cls=cls, file_path=None, canonical=canonical,
        ingest_method="url_direct", url_norm=url_norm,
        metadata_meta=doi_meta,
        manual_required_reason=doi_meta.get("reason", "DOI nao resolvido"),
        manual_required_howto="Abrir em browser → baixar PDF → arrastar para NotebookLM",
        academic_score=score,
    )


def _worker_generic(item: dict, work_dir: Path) -> UploadTask:
    url, cls, url_norm = item["url"], item["cls"], item["url_norm"]
    canonical = f"url:{url_norm}"
    if cls["type"] == "cloudflare_known":
        return UploadTask(
            url=url, cls=cls, file_path=None, canonical=canonical,
            ingest_method="url_direct", url_norm=url_norm,
            manual_required_reason=f"Cloudflare-protected publisher ({cls['metadata'].get('host')})",
            manual_required_howto="Open in browser → download PDF → drag into NotebookLM",
        )
    # gov/blog/generic: upload URL directly — NotebookLM scraper handles it.
    return UploadTask(
        url=url, cls=cls, file_path=None, canonical=canonical,
        ingest_method="url_direct", url_norm=url_norm,
    )


# Sentinel used to close the upload queue.
_UPLOAD_SENTINEL = object()


def _upload_worker(
    upload_queue: "queue.Queue",
    notebook_id: str,
    pesquisa_slug: str,
    pesquisas_root: Path,
    manifest_path: Path,
    skip_upload: bool,
    buckets: dict,
    buckets_lock: threading.Lock,
    skip_dupe_canonicals: Optional[set[str]] = None,
):
    """Single-threaded consumer — NotebookLM CLI is not thread-safe, so we
    serialise uploads here even though the downloads run in parallel."""
    while True:
        task = upload_queue.get()
        try:
            if task is _UPLOAD_SENTINEL:
                return
            _upload_and_record(
                task, notebook_id, pesquisa_slug, pesquisas_root,
                manifest_path, skip_upload, buckets, buckets_lock,
                skip_dupe_canonicals=skip_dupe_canonicals,
            )
        finally:
            upload_queue.task_done()


def _upload_and_record(
    task: UploadTask,
    notebook_id: str,
    pesquisa_slug: str,
    pesquisas_root: Path,
    manifest_path: Path,
    skip_upload: bool,
    buckets: dict,
    buckets_lock: threading.Lock,
    skip_dupe_canonicals: Optional[set[str]] = None,
):
    # F8 skip-dupe: if the canonical_key is already present in the live NBM,
    # do nothing — no upload, no manifest write. The existing source remains
    # the source of truth. This prevents the dedupe↔readd loop observed in
    # Phase 5 where WEB_PAGE + MARKDOWN of the same paper kept re-appearing.
    if skip_dupe_canonicals and task.canonical in skip_dupe_canonicals:
        with buckets_lock:
            buckets.setdefault("skipped_duplicate", []).append({
                "url": task.url,
                "canonical": task.canonical,
                "reason": "canonical_key already present in notebook",
            })
        return

    source_id = None
    status = "pending"
    error_msg = task.download_error

    # Case 1: download failed outright (worker raised).
    if task.download_error and not task.file_path:
        with buckets_lock:
            buckets["manual_required"].append({
                "url": task.url,
                "reason": f"Download error: {task.download_error}",
                "how_to": "Retry or inspect logs",
            })
        status = "failed"
    # Case 2: explicit manual bucket from worker (cloudflare, DOI not-OA, ...).
    elif task.manual_required_reason:
        with buckets_lock:
            buckets["manual_required"].append({
                "url": task.url,
                "reason": task.manual_required_reason,
                "how_to": task.manual_required_howto or "Open in browser → download → drag into NotebookLM",
            })
        status = "manual"
    elif skip_upload:
        status = "skipped"
    elif task.file_path:
        res = _nblm_add_file(task.file_path, notebook_id)
        if res["ok"]:
            status = "ok"
            source_id = res["source_id"]
            with buckets_lock:
                buckets["auto_uploaded"].append({
                    "url": task.url, "title": task.file_path.name, "canonical": task.canonical,
                })
        else:
            status = "failed"
            error_msg = res["error"]
            with buckets_lock:
                buckets["manual_required"].append({
                    "url": task.url,
                    "reason": f"Upload failed: {error_msg}",
                    "how_to": "Retry with `notebooklm source add <file>` or upload manually",
                })
    else:
        # URL-direct path (gov/blog/generic).
        if task.cls["type"] in ("gov_or_guideline", "blog_or_news", "generic_web"):
            res = _nblm_add_url(task.url, notebook_id)
            if res["ok"]:
                status = "ok"
                source_id = res["source_id"]
                with buckets_lock:
                    buckets["auto_uploaded"].append({
                        "url": task.url, "title": task.url, "canonical": task.canonical,
                    })
            else:
                status = "failed"
                error_msg = res["error"]
                with buckets_lock:
                    buckets["manual_required"].append({
                        "url": task.url,
                        "reason": f"Upload failed: {error_msg}",
                        "how_to": "Retry manually or skip if paywalled",
                    })

    # Manifest update (single uploader thread → no lock needed around manifest,
    # notebook_manifest.record_source already uses an internal file lock).
    ingest_meta = {
        "original_url": task.url,
        "pdf_local_path": str(task.file_path) if task.file_path else None,
        **task.metadata_meta,
    }
    if task.academic_score:
        ingest_meta["academic_score"] = task.academic_score.get("score")
        ingest_meta["academic_tier"] = task.academic_score.get("tier")
    try:
        manifest.record_source(
            manifest_path=manifest_path,
            notebook_id=notebook_id,
            pesquisa_slug=pesquisa_slug,
            pesquisas_root=pesquisas_root,
            canonical_key=task.canonical,
            title=task.file_path.name if task.file_path else task.url,
            source_type=task.cls["type"],
            origin_pesquisa=pesquisa_slug,
            status=status,
            notebooklm_source_id=source_id,
            ingest_method=task.ingest_method,
            ingest_metadata=ingest_meta,
            error=error_msg,
        )
    except Exception as e:
        print(f"[warn] manifest update for {task.url}: {e}", file=sys.stderr)


def _tier_distribution(scored_tasks: list["UploadTask"]) -> dict:
    """Aggregate the tier counts from scored tasks for the run summary."""
    counts = {"tier_1": 0, "tier_2": 0, "tier_3": 0, "unknown": 0}
    for t in scored_tasks:
        if not t.academic_score:
            continue
        tier = t.academic_score.get("tier")
        if tier == 1:
            counts["tier_1"] += 1
        elif tier == 2:
            counts["tier_2"] += 1
        elif tier == 3:
            counts["tier_3"] += 1
        else:
            counts["unknown"] += 1
    return counts


def _ranking_table_row(task: "UploadTask") -> str:
    """One Markdown table row for the academic ranking report."""
    s = task.academic_score or {}
    sig = s.get("signals") or {}
    title = (task.file_path.name if task.file_path else task.url)[:80]
    venue = sig.get("venue") or "-"
    year = sig.get("year") or "-"
    cpy = sig.get("citations_per_year")
    cpy_str = f"{cpy:.1f}" if isinstance(cpy, (int, float)) else "-"
    infl = sig.get("influential_citations")
    infl_str = str(infl) if infl is not None else "-"
    score = s.get("score", "-")
    tier = s.get("tier", "-")
    rationale = (s.get("rationale") or "").replace("|", "\\|")[:140]
    return f"| {tier} | {title} | {venue} | {year} | {cpy_str} | {infl_str} | {score} | {rationale} |"


def _write_ranking_report(
    scored_tasks: list["UploadTask"], work_dir: Path
) -> Optional[Path]:
    """Materialise the academic-ranking-report.md in the run's work_dir.

    Sorts by score desc; "unknown" tier sinks to the bottom. Returns the path
    written, or None when no tasks had scores attached (e.g., --skip-scoring).
    """
    if not scored_tasks:
        return None

    template_path = (
        Path(__file__).resolve().parent.parent.parent
        / "assets" / "templates" / "academic-ranking-report.md"
    )
    if not template_path.exists():
        return None

    def _sort_key(t):
        s = t.academic_score or {}
        tier = s.get("tier")
        # Push "unknown" to the bottom; otherwise sort by score desc.
        unknown_rank = 1 if tier == "unknown" else 0
        return (unknown_rank, -(s.get("score") or 0))

    rows = [_ranking_table_row(t) for t in sorted(scored_tasks, key=_sort_key)]
    counts = _tier_distribution(scored_tasks)

    template = template_path.read_text(encoding="utf-8")
    rendered = (
        template
        .replace("{{TABLE_ROWS}}", "\n".join(rows))
        .replace("{{TIER_1_COUNT}}", str(counts["tier_1"]))
        .replace("{{TIER_2_COUNT}}", str(counts["tier_2"]))
        .replace("{{TIER_3_COUNT}}", str(counts["tier_3"]))
        .replace("{{TIER_UNKNOWN_COUNT}}", str(counts["unknown"]))
    )

    out_path = work_dir / "academic-ranking-report.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(rendered, encoding="utf-8")
    return out_path


def _pool_sizes(max_parallel: int | None) -> tuple[int, int, int]:
    if max_parallel is None:
        return (DEFAULT_POOL_NCBI, DEFAULT_POOL_ACADEMIC, DEFAULT_POOL_GENERIC)
    n = max(1, max_parallel)
    ncbi = max(1, round(n * 0.30))
    academic = max(1, round(n * 0.30))
    generic = max(1, n - ncbi - academic)
    return ncbi, academic, generic


def _process_parallel(
    urls: list[str],
    notebook_id: str,
    pesquisa_slug: str,
    pesquisas_root: Path,
    work_dir: Path,
    skip_upload: bool,
    use_cache: bool,
    pool_sizes: tuple[int, int, int],
    manifest_path: Path,
    *,
    enable_scoring: bool = True,
    enable_biorxiv_fallback: bool = True,
    skip_dupe_canonicals: Optional[set[str]] = None,
) -> dict:
    buckets: dict[str, list[dict]] = {
        "auto_uploaded": [],
        "manual_required": [],
        "paywall_unavailable": [],
        "skipped_duplicate": [],
    }
    buckets_lock = threading.Lock()
    download_errors: list[str] = []
    scored_tasks: list[UploadTask] = []
    scored_lock = threading.Lock()

    ncbi_items, academic_items, generic_items = _classify_and_partition(urls)
    ncbi_w, academic_w, generic_w = pool_sizes

    upload_queue: "queue.Queue" = queue.Queue()
    uploader = threading.Thread(
        target=_upload_worker,
        args=(upload_queue, notebook_id, pesquisa_slug, pesquisas_root,
              manifest_path, skip_upload, buckets, buckets_lock),
        kwargs={"skip_dupe_canonicals": skip_dupe_canonicals},
        name="nblm-uploader",
        daemon=False,
    )
    uploader.start()

    try:
        with ThreadPoolExecutor(max_workers=ncbi_w, thread_name_prefix="ncbi") as ncbi_pool, \
             ThreadPoolExecutor(max_workers=academic_w, thread_name_prefix="acad") as academic_pool, \
             ThreadPoolExecutor(max_workers=generic_w, thread_name_prefix="gen") as generic_pool:

            futures = []
            futures += [
                ncbi_pool.submit(
                    _worker_ncbi, it, work_dir,
                    enable_scoring=enable_scoring, use_cache=use_cache,
                ) for it in ncbi_items
            ]
            futures += [
                academic_pool.submit(
                    _worker_academic, it, work_dir, use_cache,
                    enable_scoring=enable_scoring,
                    enable_biorxiv_fallback=enable_biorxiv_fallback,
                ) for it in academic_items
            ]
            futures += [generic_pool.submit(_worker_generic, it, work_dir) for it in generic_items]

            for fut in as_completed(futures):
                try:
                    task = fut.result()
                except Exception as e:
                    download_errors.append(str(e))
                    continue
                if task.academic_score is not None:
                    with scored_lock:
                        scored_tasks.append(task)
                upload_queue.put(task)
    finally:
        upload_queue.put(_UPLOAD_SENTINEL)
        uploader.join()

    summary = {
        "timestamp": _now_iso(),
        "notebook_id": notebook_id,
        "total": len(urls),
        "auto_uploaded": len(buckets["auto_uploaded"]),
        "manual_required": len(buckets["manual_required"]),
        "paywall_unavailable": len(buckets["paywall_unavailable"]),
        "skipped_duplicate": len(buckets.get("skipped_duplicate", [])),
        "download_errors": download_errors,
        "pool_sizes": {"ncbi": ncbi_w, "academic": academic_w, "generic": generic_w},
        "buckets": buckets,
    }
    if enable_scoring:
        summary["tier_distribution"] = _tier_distribution(scored_tasks)
        ranking_path = _write_ranking_report(scored_tasks, work_dir)
        if ranking_path:
            summary["academic_ranking_report"] = str(ranking_path)
    return summary


def _process_serial(
    urls: list[str],
    notebook_id: str,
    pesquisa_slug: str,
    pesquisas_root: Path,
    work_dir: Path,
    skip_upload: bool,
    use_cache: bool,
    manifest_path: Path,
    *,
    enable_scoring: bool = True,
    enable_biorxiv_fallback: bool = True,
    skip_dupe_canonicals: Optional[set[str]] = None,
) -> dict:
    """v1-like serial fallback (--serial flag). Uses the same worker functions
    but runs them inline + uploads one by one. Useful when debugging or on
    systems where spawning threads is undesirable."""
    buckets: dict[str, list[dict]] = {
        "auto_uploaded": [],
        "manual_required": [],
        "paywall_unavailable": [],
        "skipped_duplicate": [],
    }
    buckets_lock = threading.Lock()  # unused in serial but kept for shared helper
    download_errors: list[str] = []
    scored_tasks: list[UploadTask] = []

    ncbi_items, academic_items, generic_items = _classify_and_partition(urls)

    for it in ncbi_items + academic_items + generic_items:
        try:
            if it in ncbi_items:
                task = _worker_ncbi(
                    it, work_dir,
                    enable_scoring=enable_scoring, use_cache=use_cache,
                )
            elif it in academic_items:
                task = _worker_academic(
                    it, work_dir, use_cache,
                    enable_scoring=enable_scoring,
                    enable_biorxiv_fallback=enable_biorxiv_fallback,
                )
            else:
                task = _worker_generic(it, work_dir)
        except Exception as e:
            download_errors.append(f"{it['url']}: {e}")
            continue
        if task.academic_score is not None:
            scored_tasks.append(task)
        _upload_and_record(
            task, notebook_id, pesquisa_slug, pesquisas_root,
            manifest_path, skip_upload, buckets, buckets_lock,
            skip_dupe_canonicals=skip_dupe_canonicals,
        )
        # Be gentle with NCBI when we just fetched (v1 behavior).
        if task.cls["type"] in ("pubmed", "pmc"):
            time.sleep(0.1)

    summary = {
        "timestamp": _now_iso(),
        "notebook_id": notebook_id,
        "total": len(urls),
        "auto_uploaded": len(buckets["auto_uploaded"]),
        "manual_required": len(buckets["manual_required"]),
        "paywall_unavailable": len(buckets["paywall_unavailable"]),
        "skipped_duplicate": len(buckets.get("skipped_duplicate", [])),
        "download_errors": download_errors,
        "pool_sizes": {"ncbi": 1, "academic": 1, "generic": 1, "mode": "serial"},
        "buckets": buckets,
    }
    if enable_scoring:
        summary["tier_distribution"] = _tier_distribution(scored_tasks)
        ranking_path = _write_ranking_report(scored_tasks, work_dir)
        if ranking_path:
            summary["academic_ranking_report"] = str(ranking_path)
    return summary


def process(
    urls: list[str],
    notebook_id: str,
    pesquisa_slug: str,
    pesquisas_root: Path,
    work_dir: Path,
    skip_upload: bool,
    *,
    use_cache: bool = True,
    serial: bool = False,
    max_parallel: int | None = None,
    enable_scoring: bool = True,
    enable_biorxiv_fallback: bool = True,
    skip_dupe: bool = False,
    skip_dupe_canonicals: Optional[set[str]] = None,
) -> dict:
    work_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = pesquisas_root / "_notebook-manifest.json"

    # F8 skip-dupe: when the caller opts in but doesn't pass a pre-computed
    # set, derive it from the live notebook state. The auditor (F7) passes
    # its own set to avoid a double pull.
    effective_skip_set = skip_dupe_canonicals
    if skip_dupe and effective_skip_set is None and not skip_upload:
        effective_skip_set = compute_present_canonical_keys(notebook_id)
        print(
            f"[info] skip-dupe: {len(effective_skip_set)} canonical_keys already present in notebook",
            file=sys.stderr,
        )

    if serial:
        return _process_serial(
            urls, notebook_id, pesquisa_slug, pesquisas_root, work_dir,
            skip_upload, use_cache, manifest_path,
            enable_scoring=enable_scoring,
            enable_biorxiv_fallback=enable_biorxiv_fallback,
            skip_dupe_canonicals=effective_skip_set,
        )
    return _process_parallel(
        urls, notebook_id, pesquisa_slug, pesquisas_root, work_dir,
        skip_upload, use_cache, _pool_sizes(max_parallel), manifest_path,
        enable_scoring=enable_scoring,
        enable_biorxiv_fallback=enable_biorxiv_fallback,
        skip_dupe_canonicals=effective_skip_set,
    )


def _parse_invalidate_before(value: str) -> float:
    from datetime import datetime as _dt
    try:
        return _dt.strptime(value, "%Y-%m-%d").timestamp()
    except ValueError as e:
        raise SystemExit(f"--invalidate-cache-before expects YYYY-MM-DD, got {value!r}: {e}")


def _main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--urls", required=True, help="text file, one URL per line")
    parser.add_argument("--notebook", required=True, help="NotebookLM notebook id")
    parser.add_argument("--pesquisa", required=True, help="pesquisa slug")
    parser.add_argument("--pesquisas-root", required=True, help="path to pesquisas/ root")
    parser.add_argument("--work-dir", default=None, help="where to save fetched files")
    parser.add_argument("--skip-upload", action="store_true", help="fetch only, do not upload")

    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="bypass the local cache for this run (sets DR_SCI_NO_CACHE=1)",
    )
    parser.add_argument(
        "--invalidate-cache-before",
        metavar="YYYY-MM-DD",
        help="prune cache entries older than DATE before running",
    )

    parallel_group = parser.add_mutually_exclusive_group()
    parallel_group.add_argument(
        "--serial",
        action="store_true",
        help="disable pools (v1-like serial loop)",
    )
    parallel_group.add_argument(
        "--max-parallel",
        type=int,
        metavar="N",
        help=f"override pool sizes; split 30/30/40 NCBI/academic/generic (default {DEFAULT_POOL_NCBI+DEFAULT_POOL_ACADEMIC+DEFAULT_POOL_GENERIC})",
    )

    parser.add_argument(
        "--skip-scoring",
        action="store_true",
        help="disable v3 academic scoring (Semantic Scholar / OpenAlex / bioRxiv) — v1-like heuristic tiering",
    )
    parser.add_argument(
        "--skip-biorxiv-fallback",
        action="store_true",
        help="disable bioRxiv/medRxiv preprint fallback for paywalled DOIs",
    )

    parser.add_argument(
        "--from-auditor",
        action="store_true",
        help="telemetry: caller is notebook-source-auditor (tagged in JSON summary)",
    )
    parser.add_argument(
        "--skip-dupe",
        action="store_true",
        help="F8: before upload, pull NotebookLM state and skip any task whose "
             "canonical_key is already present. Prevents the dedupe↔readd loop "
             "observed in Phase 5 (2026-04-23).",
    )
    args = parser.parse_args()

    urls_path = Path(args.urls)
    if not urls_path.exists():
        print(f"[error] urls file not found: {urls_path}", file=sys.stderr)
        return 1

    # Boot-time env warnings for v3 APIs.
    if not args.skip_scoring:
        if not os.environ.get("OPENALEX_EMAIL"):
            print(
                "[warn] OPENALEX_EMAIL not set — using anonymous OpenAlex pool (lower rate limit). "
                "Set OPENALEX_EMAIL=you@example.com for the polite pool.",
                file=sys.stderr,
            )
        if not os.environ.get("SEMANTIC_SCHOLAR_API_KEY"):
            print(
                "[info] SEMANTIC_SCHOLAR_API_KEY not set — using public S2 rate limit (1 req/s). "
                "Optional, but improves scoring throughput.",
                file=sys.stderr,
            )

    # --no-cache propagates via env so every downstream script respects it without
    # us having to thread a flag through every layer.
    if args.no_cache:
        os.environ["DR_SCI_NO_CACHE"] = "1"

    if args.invalidate_cache_before:
        from _cache import cache_clear
        ts = _parse_invalidate_before(args.invalidate_cache_before)
        removed = cache_clear(before_date=ts)
        print(f"[info] invalidated {removed} cache entries older than {args.invalidate_cache_before}", file=sys.stderr)

    with open(urls_path) as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    pesquisas_root = Path(args.pesquisas_root).resolve()
    work_dir = Path(args.work_dir) if args.work_dir else pesquisas_root / args.pesquisa / "fontes" / "sci_fetch"

    summary = process(
        urls=urls,
        notebook_id=args.notebook,
        pesquisa_slug=args.pesquisa,
        pesquisas_root=pesquisas_root,
        work_dir=work_dir,
        skip_upload=args.skip_upload,
        use_cache=not args.no_cache,
        serial=args.serial,
        max_parallel=args.max_parallel,
        enable_scoring=not args.skip_scoring,
        enable_biorxiv_fallback=not args.skip_biorxiv_fallback,
        skip_dupe=args.skip_dupe,
    )
    if args.from_auditor:
        summary["caller"] = "notebook-source-auditor"
    json.dump(summary, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(_main())
