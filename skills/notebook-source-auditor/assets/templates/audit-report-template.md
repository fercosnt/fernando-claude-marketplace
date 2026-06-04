# Audit Report — {notebook_title} ({notebook_id})

**Generated:** {timestamp_iso}
**Mode:** {dry-run | apply}
**Pesquisas audited:** {slug-1}, {slug-2}
**Sources in NotebookLM:** {N}
**Expected canonical_keys:** {M}

## Summary

| Bucket | Count | Action |
|---|---|---|
| ✅ Missing — re-added | {N} | auto via sci_fetch/ |
| 🔁 Retryable — resolved | {N} | auto via CLI |
| 🧹 Duplicates — merged | {N} | deleted N-1, kept oldest |
| ❓ Orphans — listed/actioned | {N} | manual review or `--interactive` |
| 🗑️ Stale manifest — cleaned | {N} | marked deleted in manifest |
| 💤 No-op (already ok) | {N} | nothing to do |

## ✅ Missing sources ({N})

| Canonical Key | Origin pesquisa | Title | Result |
|---|---|---|---|
| `pmid:...` | `prd-4` | ... | delegated_to_sci_fetch |

## 🔁 Retryable sources ({N})

| Canonical Key | Ingest method | Attempts | Result |
|---|---|---|---|
| `url:...` | `url_direct` | 2 | ok |

## 🧹 Duplicates ({N} groups)

| Canonical Key | Kept | Deleted | Result |
|---|---|---|---|
| `pmc:PMC...` | `src_abc` | src_def, src_ghi | merged |

## ❓ Orphans ({N})

| Source ID | Title | URL | Confidence | Action |
|---|---|---|---|---|
| `src_xyz` | ... | ... | high | link → hashimoto-farmacologia |

## 🗑️ Stale manifest entries ({N})

These sources were marked `ok` in the manifest but the user removed them
from the notebook via the UI. Auditor flipped the manifest status to
`deleted`.

| Canonical Key | Title | Status change |
|---|---|---|
| `pmid:...` | ... | ok → deleted (deleted_from_nbm_externally) |

## ⚠ Manual required ({N})

These sources cannot be auto-retried. Resolve them manually.

| Source | Reason | Instruction |
|---|---|---|
| mdpi.com/... | captcha_bypass_flow_v1 | Open URL → download PDF → drag into notebook |

## 💤 No-op — Sources already conformant ({N})

Collapsed. Full list in the raw JSON sibling of this report
(`raw/{notebook_id}-{date}.json`).
