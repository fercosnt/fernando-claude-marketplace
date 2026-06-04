#!/usr/bin/env python3
"""Render audit reports (RF-11, RF-12).

Takes the diff output plus the results of each resolver and produces:
    1. A human-readable markdown report at
       {audits_dir}/<notebook_id>-<YYYY-MM-DD>.md
    2. A raw JSON sibling at
       {audits_dir}/raw/<notebook_id>-<YYYY-MM-DD>.json

Same-day re-runs overwrite both (idempotency — Q1 decision).
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def write_report(
    *,
    notebook_id: str,
    notebook_title: str,
    pesquisa_slugs: list[str],
    diff: dict,
    actions: dict,
    mode: str,  # "dry-run" | "apply"
    audits_dir: Path,
) -> dict[str, Path]:
    """Write markdown and raw JSON report. Returns {md: path, json: path}."""
    audits_dir = Path(audits_dir)
    audits_dir.mkdir(parents=True, exist_ok=True)
    raw_dir = audits_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    date_tag = _today()
    md_path = audits_dir / f"{notebook_id}-{date_tag}.md"
    json_path = raw_dir / f"{notebook_id}-{date_tag}.json"

    md_path.write_text(_render_markdown(
        notebook_id=notebook_id,
        notebook_title=notebook_title,
        pesquisa_slugs=pesquisa_slugs,
        diff=diff,
        actions=actions,
        mode=mode,
    ), encoding="utf-8")

    json_path.write_text(json.dumps({
        "generated_at": _now_iso(),
        "notebook_id": notebook_id,
        "notebook_title": notebook_title,
        "pesquisa_slugs": pesquisa_slugs,
        "mode": mode,
        "diff": diff,
        "actions": actions,
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    return {"md": md_path, "json": json_path}


def _render_markdown(
    *,
    notebook_id: str,
    notebook_title: str,
    pesquisa_slugs: list[str],
    diff: dict,
    actions: dict,
    mode: str,
) -> str:
    title_prefix = "DRY-RUN: " if mode == "dry-run" else ""
    lines: list[str] = []
    lines.append(f"# {title_prefix}Audit Report — {notebook_title} ({notebook_id})")
    lines.append("")
    lines.append(f"**Generated:** {_now_iso()}")
    lines.append(f"**Mode:** {mode}")
    lines.append(f"**Pesquisas audited:** {', '.join(pesquisa_slugs) if pesquisa_slugs else '(none)'}")
    totals = diff.get("totals", {})
    lines.append(f"**Sources in NotebookLM:** {totals.get('current_sources', '?')}")
    lines.append(f"**Expected canonical_keys:** {totals.get('expected_canonical_keys', '?')}")
    lines.append("")

    # ---- Summary table ----
    summary_rows = [
        ("✅ Missing — re-added",           diff.get("missing", []),                  actions.get("missing", {})),
        ("🔁 Retryable — resolved",         diff.get("retryable", []),                actions.get("retryable", {})),
        ("🧹 Duplicates — merged",          diff.get("duplicates", []),               actions.get("duplicates", {})),
        ("🛑 Captcha-pages — delete+readd", diff.get("captcha_page_disguised", []),   actions.get("captcha_page_disguised", {})),
        ("❓ Orphans — listed/actioned",    diff.get("orphans", []),                  actions.get("orphans", {})),
        ("🗑️  Stale manifest — cleaned",    diff.get("stale_manifest", []),           actions.get("stale_manifest", {})),
    ]
    lines.append("## Summary")
    lines.append("")
    lines.append("| Bucket | Count | Action |")
    lines.append("|---|---|---|")
    for label, items, action in summary_rows:
        count = len(items)
        note = action.get("summary_note") if isinstance(action, dict) else ""
        lines.append(f"| {label} | {count} | {note or ('dry-run: would act' if mode == 'dry-run' else '—')} |")
    lines.append(f"| 💤 No-op (already ok) | {diff.get('noop_count', 0)} | nothing to do |")
    lines.append("")

    # ---- Detail sections ----
    _section_missing(lines, diff.get("missing", []), actions.get("missing", {}), mode)
    _section_retryable(lines, diff.get("retryable", []), actions.get("retryable", {}), mode)
    _section_duplicates(lines, diff.get("duplicates", []), actions.get("duplicates", {}), mode)
    _section_captcha_pages(lines, diff.get("captcha_page_disguised", []), actions.get("captcha_page_disguised", {}), mode)
    _section_orphans(lines, diff.get("orphans", []), actions.get("orphans", {}), mode)
    _section_stale(lines, diff.get("stale_manifest", []), actions.get("stale_manifest", {}), mode)
    _section_manual_required(lines, actions.get("manual_required", []))

    lines.append("## 💤 No-op — Sources already conformant")
    lines.append("")
    lines.append(f"{diff.get('noop_count', 0)} sources in the notebook match the expected state and required no action.")
    lines.append("Full list lives in the raw JSON sibling of this report (see `raw/` folder).")
    lines.append("")

    return "\n".join(lines) + "\n"


def _section_missing(lines: list[str], items: list[dict], action: dict, mode: str) -> None:
    lines.append(f"## ✅ Missing sources ({len(items)})")
    lines.append("")
    if not items:
        lines.append("_None._")
        lines.append("")
        return
    results = {r["canonical_key"]: r for r in action.get("results", [])}
    lines.append("| Canonical Key | Origin pesquisa | Title | Result |")
    lines.append("|---|---|---|---|")
    for it in items:
        ck = it["canonical_key"]
        ex = it.get("expected", {})
        origins = ", ".join(ex.get("origin_pesquisas", []) or [])
        result = results.get(ck, {}).get("status", "dry-run" if mode == "dry-run" else "—")
        lines.append(f"| `{ck}` | {origins} | {ex.get('title', '')[:60]} | {result} |")
    lines.append("")


def _section_retryable(lines: list[str], items: list[dict], action: dict, mode: str) -> None:
    lines.append(f"## 🔁 Retryable sources ({len(items)})")
    lines.append("")
    if not items:
        lines.append("_None._")
        lines.append("")
        return
    results = {r["canonical_key"]: r for r in action.get("results", [])}
    lines.append("| Canonical Key | Ingest method | Attempts | Result |")
    lines.append("|---|---|---|---|")
    for it in items:
        ck = it["canonical_key"]
        res = results.get(ck, {})
        status = res.get("status", "dry-run" if mode == "dry-run" else "—")
        attempts_before = it.get("attempts", 0)
        lines.append(f"| `{ck}` | {it.get('ingest_method', '')} | {attempts_before} | {status} |")
    lines.append("")


def _section_duplicates(lines: list[str], items: list[dict], action: dict, mode: str) -> None:
    lines.append(f"## 🧹 Duplicates ({len(items)} groups)")
    lines.append("")
    if not items:
        lines.append("_None._")
        lines.append("")
        return
    results = {r["canonical_key"]: r for r in action.get("results", [])}
    lines.append("| Canonical Key | Kept | Deleted | Result |")
    lines.append("|---|---|---|---|")
    for it in items:
        ck = it["canonical_key"]
        res = results.get(ck, {})
        status = res.get("status", "dry-run" if mode == "dry-run" else "—")
        deleted_list = ", ".join(it.get("delete", []))
        lines.append(f"| `{ck}` | `{it.get('keep', '')}` | {deleted_list} | {status} |")
    lines.append("")


def _section_captcha_pages(lines: list[str], items: list[dict], action: dict, mode: str) -> None:
    lines.append(f"## 🛑 Captcha-pages disguised ({len(items)})")
    lines.append("")
    if not items:
        lines.append("_None._")
        lines.append("")
        return
    lines.append(
        "These NBM sources are Cloudflare challenges, publisher walls, or "
        "access-denied pages saved as sources by an upstream upload that could "
        "not reach the real content. Action in `--apply`: delete + re-add the "
        "URL via `sci_fetch`; manifest history is flipped to `deleted` with "
        "reason `captcha_page_detected` when the canonical_key is known."
    )
    lines.append("")
    results = {r["source_id"]: r for r in action.get("results", []) if r.get("source_id") != "(batch)"}
    batch_result = next((r for r in action.get("results", []) if r.get("source_id") == "(batch)"), None)
    lines.append("| Source ID | Title | URL | Canonical (derived) | In manifest | Result |")
    lines.append("|---|---|---|---|---|---|")
    for it in items:
        sid = it["source_id"]
        status = results.get(sid, {}).get("status", "dry-run" if mode == "dry-run" else "—")
        title = (it.get("title") or "")[:50]
        url = (it.get("url") or "")[:40]
        ck = it.get("derived_canonical_key") or "(none)"
        in_mf = "yes" if it.get("in_manifest") else "no"
        lines.append(f"| `{sid}` | {title} | {url} | `{ck}` | {in_mf} | {status} |")
    if batch_result:
        lines.append("")
        lines.append(f"**Re-add batch:** {batch_result.get('status', '')}")
    lines.append("")


def _section_orphans(lines: list[str], items: list[dict], action: dict, mode: str) -> None:
    lines.append(f"## ❓ Orphans ({len(items)})")
    lines.append("")
    if not items:
        lines.append("_None._")
        lines.append("")
        return
    decisions = {d["source_id"]: d for d in action.get("results", [])}
    lines.append("| Source ID | Title | URL | Confidence | Action |")
    lines.append("|---|---|---|---|---|")
    for it in items:
        sid = it["source_id"]
        decision = decisions.get(sid, {})
        act = decision.get("action") or ("dry-run: listed" if mode == "dry-run" else "listed only")
        title = (it.get("title") or "")[:50]
        url = (it.get("url") or "")[:40]
        lines.append(f"| `{sid}` | {title} | {url} | {it.get('derivation_confidence', '?')} | {act} |")
    lines.append("")


def _section_stale(lines: list[str], items: list[dict], action: dict, mode: str) -> None:
    lines.append(f"## 🗑️ Stale manifest entries ({len(items)})")
    lines.append("")
    if not items:
        lines.append("_None._")
        lines.append("")
        return
    lines.append("These sources are marked `ok` in the manifest but the user removed them from the notebook via the UI. Auditor flipped the manifest status to `deleted`.")
    lines.append("")
    lines.append("| Canonical Key | Title | Status change |")
    lines.append("|---|---|---|")
    results = {r["canonical_key"]: r for r in action.get("results", [])}
    for it in items:
        ck = it["canonical_key"]
        title = (it.get("manifest_entry", {}).get("title") or "")[:60]
        change = results.get(ck, {}).get("status", "dry-run: would mark deleted" if mode == "dry-run" else "—")
        lines.append(f"| `{ck}` | {title} | {change} |")
    lines.append("")


def _section_manual_required(lines: list[str], items: list[dict]) -> None:
    lines.append(f"## ⚠ Manual required ({len(items)})")
    lines.append("")
    if not items:
        lines.append("_None._")
        lines.append("")
        return
    lines.append("These sources cannot be auto-retried. Resolve them manually.")
    lines.append("")
    lines.append("| Source | Reason | Instruction |")
    lines.append("|---|---|---|")
    for it in items:
        lines.append(
            f"| `{it.get('canonical_key', '?')}` | "
            f"{it.get('reason', '?')} | "
            f"{it.get('instruction', '')} |"
        )
    lines.append("")
