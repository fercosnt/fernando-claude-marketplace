#!/usr/bin/env python3
"""Resolve PMID(s) to PMCID via NCBI E-utilities elink.

Usage:
    python pmid_to_pmc.py <PMID> [<PMID> ...]
    python pmid_to_pmc.py --batch <file-with-one-PMID-per-line>

Output: JSON object {pmid: pmcid_or_null}
Exit codes: 0 ok (even if some have no PMC), 1 error.
"""
from __future__ import annotations

import json
import re
import sys

from _http import fetch_with_retry, ncbi_throttle, ncbi_api_key_param
from _cache import cache_get_json, cache_put, TTL_DEFAULTS


ELINK = (
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi"
    "?dbfrom=pubmed&db=pmc&id={ids}"
)

_DBFROM_BLOCK_RE = re.compile(
    r"<IdList>\s*<Id>(\d+)</Id>\s*</IdList>\s*"
    r"<LinkSetDb>.*?<LinkName>pubmed_pmc</LinkName>\s*<Link>\s*<Id>(\d+)</Id>",
    re.DOTALL,
)


def _resolve_batch(
    pmids: list[str], *, use_cache: bool = True
) -> dict[str, str | None]:
    """Resolve a batch of PMIDs to PMCIDs. Hits cache per-PMID first, only
    calls elink for the cache-miss subset.

    Cache layout (kind=pmc_link, TTL 365d): one entry per PMID storing
    `{"pmcid": "PMC1234"|null}`. Even null results are cached so delta-research
    doesn't re-hit the elink API for papers known to lack a PMC id.
    """
    out: dict[str, str | None] = {}
    to_fetch: list[str] = []

    if use_cache:
        for p in pmids:
            cached = cache_get_json("pmc_link", p, ttl_days=TTL_DEFAULTS["pmc_link"])
            if cached is not None:
                out[p] = cached.get("pmcid")  # may be None — still a cache hit
            else:
                to_fetch.append(p)
    else:
        to_fetch = list(pmids)

    if not to_fetch:
        return out

    ids = ",".join(to_fetch)
    ncbi_throttle()
    url = ELINK.format(ids=ids) + ncbi_api_key_param()
    status, body, _ = fetch_with_retry(url, timeout=30, bucket="ncbi")
    if status != 200:
        raise RuntimeError(f"elink HTTP {status}")

    xml = body.decode("utf-8", errors="replace")
    # Seed fetched PMIDs with None first so unmatched ones are still stored.
    fetched: dict[str, str | None] = {p: None for p in to_fetch}

    for block in re.finditer(
        r"<LinkSet>(.*?)</LinkSet>",
        xml,
        flags=re.DOTALL,
    ):
        m = _DBFROM_BLOCK_RE.search(block.group(1))
        if m:
            pmid, pmcid_num = m.group(1), m.group(2)
            if pmid in fetched:
                fetched[pmid] = f"PMC{pmcid_num}"

    if use_cache:
        for pmid, pmcid in fetched.items():
            cache_put("pmc_link", pmid, {"pmcid": pmcid})

    out.update(fetched)
    return out


def _main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(
            "usage: pmid_to_pmc.py <PMID> [<PMID> ...] [--no-cache]\n"
            "       pmid_to_pmc.py --batch <file> [--no-cache]",
            file=sys.stderr,
        )
        return 1

    use_cache = "--no-cache" not in argv
    args = [a for a in argv[1:] if a != "--no-cache"]

    if not args:
        print("no valid PMIDs provided", file=sys.stderr)
        return 1

    if args[0] == "--batch":
        if len(args) < 2:
            print("usage: pmid_to_pmc.py --batch <file>", file=sys.stderr)
            return 1
        with open(args[1]) as f:
            pmids = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    else:
        pmids = [a.strip() for a in args if a.strip().isdigit()]

    if not pmids:
        print("no valid PMIDs provided", file=sys.stderr)
        return 1

    # NCBI elink supports many IDs per call, but chunk to keep URL < 2000 chars.
    result: dict[str, str | None] = {}
    for i in range(0, len(pmids), 100):
        chunk = pmids[i : i + 100]
        try:
            result.update(_resolve_batch(chunk, use_cache=use_cache))
        except Exception as e:
            print(f"[error] chunk starting at {chunk[0]}: {e}", file=sys.stderr)
            for p in chunk:
                result.setdefault(p, None)

    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
