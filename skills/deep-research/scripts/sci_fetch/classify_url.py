#!/usr/bin/env python3
"""Classify a URL into a scientific source type.

Usage:
    python classify_url.py <url>
    python classify_url.py --batch <path-to-urls.txt>

Output: JSON {url, type, confidence, metadata}

Types:
    pubmed           — pubmed.ncbi.nlm.nih.gov/<pmid>
    pmc              — pmc.ncbi.nlm.nih.gov/articles/PMC<id> (or legacy path)
    doi              — doi.org/10.x/... or direct publisher URL with /doi/10.
    cloudflare_known — known Cloudflare-protected publishers (MDPI, Karger, etc.)
    gov_or_guideline — government / public-health sites
    blog_or_news     — blogs, newsletters, news outlets
    generic_web      — anything else

Exit codes: 0 ok, 1 invalid input, 2 empty/malformed URL.
"""
from __future__ import annotations

import json
import re
import sys
from urllib.parse import urlparse

# Ordered list: first match wins.
_PUBMED_RE = re.compile(r"pubmed\.ncbi\.nlm\.nih\.gov/(\d+)", re.IGNORECASE)
_PMC_RE = re.compile(
    r"(?:pmc\.ncbi\.nlm\.nih\.gov/articles|ncbi\.nlm\.nih\.gov/pmc/articles)/(PMC\d+)",
    re.IGNORECASE,
)
_DOI_RE = re.compile(
    r"(?:doi\.org/|/doi/(?:full/|abs/|pdf/|pdfplus/)?)(10\.\d{4,9}/[^\s?#]+)",
    re.IGNORECASE,
)

# Publishers known to front with Cloudflare / anti-bot; scraping fails silently.
_CLOUDFLARE_HOSTS = {
    "www.mdpi.com", "mdpi.com",
    "www.karger.com", "karger.com",
    "www.liebertpub.com", "liebertpub.com",
    "jamanetwork.com", "www.jamanetwork.com",
    "academic.oup.com",
    "www.sciencedirect.com", "sciencedirect.com",
    "link.springer.com",
    "onlinelibrary.wiley.com",
    "journals.lww.com",
    "www.nature.com",  # some Nature subpaths are OK but treat as cloudflare by default
    "www.tandfonline.com", "tandfonline.com",
}

_GOV_HOSTS_SUFFIXES = (
    ".gov", ".nih.gov", ".cdc.gov", ".fda.gov", ".who.int",
    "guidelines.gov", "uspreventiveservicestaskforce.org",
    "europa.eu", "nhs.uk",
)

_BLOG_HOSTS = {
    "medium.com", "substack.com", "peterattiamd.com",
    "selfhacked.com", "examine.com", "consumerlab.com",
    "lesswrong.com", "dev.to",
}


def classify(url: str) -> dict:
    if not url or not isinstance(url, str):
        return {"url": url, "type": "invalid", "confidence": 0.0, "metadata": {}}

    url = url.strip()
    if not url:
        return {"url": url, "type": "invalid", "confidence": 0.0, "metadata": {}}

    # High-confidence regex matches first.
    m = _PUBMED_RE.search(url)
    if m:
        return {
            "url": url,
            "type": "pubmed",
            "confidence": 1.0,
            "metadata": {"pmid": m.group(1)},
        }

    m = _PMC_RE.search(url)
    if m:
        return {
            "url": url,
            "type": "pmc",
            "confidence": 1.0,
            "metadata": {"pmcid": m.group(1)},
        }

    m = _DOI_RE.search(url)
    if m:
        return {
            "url": url,
            "type": "doi",
            "confidence": 0.95,
            "metadata": {"doi": m.group(1).rstrip(").,;")},
        }

    # Host-based classification.
    try:
        host = (urlparse(url).hostname or "").lower()
    except ValueError:
        return {"url": url, "type": "invalid", "confidence": 0.0, "metadata": {}}

    if not host:
        return {"url": url, "type": "generic_web", "confidence": 0.3, "metadata": {}}

    if host in _CLOUDFLARE_HOSTS:
        return {
            "url": url,
            "type": "cloudflare_known",
            "confidence": 0.9,
            "metadata": {"host": host},
        }

    if host in _BLOG_HOSTS:
        return {
            "url": url,
            "type": "blog_or_news",
            "confidence": 0.85,
            "metadata": {"host": host},
        }

    if any(host.endswith(suf) for suf in _GOV_HOSTS_SUFFIXES):
        return {
            "url": url,
            "type": "gov_or_guideline",
            "confidence": 0.9,
            "metadata": {"host": host},
        }

    return {
        "url": url,
        "type": "generic_web",
        "confidence": 0.5,
        "metadata": {"host": host},
    }


def _main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: classify_url.py <url>  |  classify_url.py --batch <file>", file=sys.stderr)
        return 1

    if argv[1] == "--batch":
        if len(argv) < 3:
            print("usage: classify_url.py --batch <file>", file=sys.stderr)
            return 1
        results = []
        with open(argv[2]) as f:
            for line in f:
                u = line.strip()
                if u and not u.startswith("#"):
                    results.append(classify(u))
        json.dump(results, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0

    url = argv[1]
    result = classify(url)
    json.dump(result, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0 if result["type"] != "invalid" else 2


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
