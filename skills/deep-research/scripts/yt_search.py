#!/usr/bin/env python3
"""YouTube search via yt-dlp with structured JSON output for deep-research skill."""

import io
import json
import shutil
import subprocess
import sys
from datetime import datetime, timedelta

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


def parse_args(argv):
    args = argv[1:]
    count = 15
    months = 12
    query_parts = []
    output_format = "json"
    i = 0
    while i < len(args):
        if args[i] == "--count" and i + 1 < len(args):
            count = int(args[i + 1])
            i += 2
        elif args[i] == "--months" and i + 1 < len(args):
            months = int(args[i + 1])
            i += 2
        elif args[i] == "--no-date-filter":
            months = 0
            i += 1
        elif args[i] == "--format" and i + 1 < len(args):
            output_format = args[i + 1]
            i += 2
        else:
            query_parts.append(args[i])
            i += 1
    query = " ".join(query_parts)
    if not query:
        print("Usage: yt_search.py <query> [--count N] [--months N] [--format json|markdown]", file=sys.stderr)
        sys.exit(1)
    return query, count, months, output_format


def format_number(n):
    if n is None:
        return "N/D"
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}K"
    return str(n)


def format_duration(info):
    if info.get("duration_string"):
        return info["duration_string"]
    dur = info.get("duration")
    if dur is None:
        return "N/D"
    dur = int(dur)
    hours, remainder = divmod(dur, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    return f"{minutes}:{seconds:02d}"


def format_date(raw):
    if not raw or len(raw) != 8:
        return "N/D"
    try:
        dt = datetime.strptime(raw, "%Y%m%d")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        return raw


def get_cutoff_date(months):
    if months <= 0:
        return None
    cutoff = datetime.now() - timedelta(days=months * 30)
    return cutoff.strftime("%Y%m%d")


def calculate_relevance(video, query_terms):
    """Score video relevance: views/subs ratio + recency + title match."""
    score = 0.0
    views = video.get("view_count") or 0
    subs = video.get("channel_follower_count") or 1

    # Engagement: views/subs ratio (capped at 10x)
    ratio = min(views / max(subs, 1), 10.0)
    score += ratio * 10  # 0-100

    # Views raw (log scale bonus)
    if views > 100_000:
        score += 30
    elif views > 10_000:
        score += 20
    elif views > 1_000:
        score += 10

    # Recency bonus
    upload = video.get("upload_date", "")
    if upload:
        try:
            days_ago = (datetime.now() - datetime.strptime(upload, "%Y%m%d")).days
            if days_ago < 90:
                score += 25
            elif days_ago < 180:
                score += 15
            elif days_ago < 365:
                score += 5
        except ValueError:
            pass

    # Title keyword match
    title = (video.get("title") or "").lower()
    matches = sum(1 for term in query_terms if term.lower() in title)
    score += matches * 15

    # Channel authority (subscriber count)
    if subs > 100_000:
        score += 20
    elif subs > 10_000:
        score += 10

    return round(score, 1)


def main():
    query, count, months, output_format = parse_args(sys.argv)

    if not shutil.which("yt-dlp"):
        print("Error: yt-dlp not found. Install with: pip install yt-dlp", file=sys.stderr)
        sys.exit(1)

    fetch_count = count * 3 if months > 0 else count * 2
    search_query = f"ytsearch{fetch_count}:{query}"
    cmd = [
        "yt-dlp", search_query,
        "--dump-json", "--no-download", "--no-warnings", "--quiet",
    ]

    print(f"Searching YouTube: \"{query}\" (top {count}, last {months}mo)...", file=sys.stderr)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        print("Error: Search timed out.", file=sys.stderr)
        sys.exit(1)

    if result.returncode != 0 and not result.stdout.strip():
        print(f"Error: yt-dlp failed: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)

    videos = []
    for line in result.stdout.strip().splitlines():
        if not line.strip():
            continue
        try:
            videos.append(json.loads(line))
        except json.JSONDecodeError:
            continue

    if not videos:
        print("No results found.", file=sys.stderr)
        sys.exit(0)

    # Date filter
    cutoff = get_cutoff_date(months)
    if cutoff:
        videos = [v for v in videos if (v.get("upload_date") or "00000000") >= cutoff]

    # Score and sort by relevance
    query_terms = query.split()
    for v in videos:
        v["_relevance_score"] = calculate_relevance(v, query_terms)
    videos.sort(key=lambda v: v["_relevance_score"], reverse=True)
    videos = videos[:count]

    # Build structured output
    results = []
    for i, info in enumerate(videos, 1):
        views = info.get("view_count")
        subs = info.get("channel_follower_count")
        ratio = round(views / max(subs, 1), 2) if views and subs else None

        entry = {
            "rank": i,
            "title": info.get("title", "Unknown"),
            "url": f"https://youtube.com/watch?v={info.get('id', '')}",
            "channel": info.get("channel", info.get("uploader", "Unknown")),
            "subscribers": subs,
            "subscribers_formatted": format_number(subs),
            "views": views,
            "views_formatted": format_number(views),
            "duration": format_duration(info),
            "date": format_date(info.get("upload_date", "")),
            "views_subs_ratio": ratio,
            "relevance_score": info["_relevance_score"],
            "description": (info.get("description") or "")[:200],
            "has_subtitles": bool(info.get("subtitles") or info.get("automatic_captions")),
        }
        results.append(entry)

    if output_format == "json":
        print(json.dumps({"query": query, "count": len(results), "results": results}, indent=2, ensure_ascii=False))
    elif output_format == "markdown":
        print(f"## YouTube Search: {query}\n")
        print(f"| # | Video | Canal | Views | Subs | Ratio | Duracao | Data | Legendas |")
        print(f"|---|-------|-------|-------|------|-------|---------|------|----------|")
        for r in results:
            print(f"| {r['rank']} | [{r['title'][:50]}]({r['url']}) | {r['channel']} | {r['views_formatted']} | {r['subscribers_formatted']} | {r['views_subs_ratio'] or 'N/D'}x | {r['duration']} | {r['date']} | {'Sim' if r['has_subtitles'] else 'Nao'} |")


if __name__ == "__main__":
    main()
