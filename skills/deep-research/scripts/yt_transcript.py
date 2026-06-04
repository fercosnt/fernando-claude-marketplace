#!/usr/bin/env python3
"""YouTube transcript extraction with 3-level fallback for deep-research skill.

Fallback chain:
1. yt-dlp manual subtitles (human-made captions)
2. yt-dlp automatic captions (auto-generated)
3. Report as PENDENTE (no local whisper — too heavy for research context)
"""

import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


def parse_args(argv):
    args = argv[1:]
    urls = []
    output_dir = None
    langs = ["en", "en-US", "en-GB", "pt", "pt-BR"]
    i = 0
    while i < len(args):
        if args[i] == "--output-dir" and i + 1 < len(args):
            output_dir = args[i + 1]
            i += 2
        elif args[i] == "--langs" and i + 1 < len(args):
            langs = args[i + 1].split(",")
            i += 2
        else:
            urls.append(args[i])
            i += 1
    if not urls:
        print("Usage: yt_transcript.py <url1> [url2 ...] [--output-dir DIR] [--langs pt,en]", file=sys.stderr)
        sys.exit(1)
    return urls, output_dir, langs


def extract_video_id(url):
    """Extract video ID from various YouTube URL formats."""
    if "watch?v=" in url:
        return url.split("watch?v=")[1].split("&")[0]
    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    if "shorts/" in url:
        return url.split("shorts/")[1].split("?")[0]
    return url


def try_subtitles(url, langs, tmpdir, sub_type="manual"):
    """Try to download subtitles using yt-dlp."""
    lang_str = ",".join(langs)

    if sub_type == "manual":
        cmd = [
            "yt-dlp", url,
            "--write-subs", "--sub-langs", lang_str,
            "--skip-download", "--no-warnings", "--quiet",
            "--sub-format", "vtt/srt/best",
            "--output", os.path.join(tmpdir, "%(id)s.%(ext)s"),
        ]
    else:
        cmd = [
            "yt-dlp", url,
            "--write-auto-subs", "--sub-langs", lang_str,
            "--skip-download", "--no-warnings", "--quiet",
            "--sub-format", "vtt/srt/best",
            "--output", os.path.join(tmpdir, "%(id)s.%(ext)s"),
        ]

    try:
        subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    except subprocess.TimeoutExpired:
        return None

    # Find the subtitle file
    for f in os.listdir(tmpdir):
        if f.endswith((".vtt", ".srt")):
            filepath = os.path.join(tmpdir, f)
            with open(filepath, "r", encoding="utf-8", errors="replace") as fh:
                content = fh.read()
            if len(content.strip()) > 50:
                return content
    return None


def clean_vtt(raw_text):
    """Clean VTT/SRT subtitle text: remove timestamps, duplicates, formatting tags."""
    lines = raw_text.splitlines()
    cleaned = []
    seen = set()

    for line in lines:
        line = line.strip()
        # Skip VTT headers, timestamps, sequence numbers
        if not line:
            continue
        if line.startswith("WEBVTT"):
            continue
        if line.startswith("Kind:") or line.startswith("Language:"):
            continue
        if "-->" in line:
            continue
        if line.isdigit():
            continue

        # Remove HTML-like tags
        import re
        line = re.sub(r"<[^>]+>", "", line)
        line = line.strip()

        if not line:
            continue

        # Deduplicate consecutive lines (common in auto-captions)
        if line not in seen:
            cleaned.append(line)
            seen.add(line)
        else:
            # Reset seen after gap to allow repeated phrases in different contexts
            if len(seen) > 20:
                seen.clear()

    return " ".join(cleaned)


def get_video_metadata(url):
    """Get basic video metadata via yt-dlp."""
    cmd = [
        "yt-dlp", url,
        "--dump-json", "--no-download", "--no-warnings", "--quiet",
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0 and result.stdout.strip():
            info = json.loads(result.stdout)
            return {
                "title": info.get("title", "Unknown"),
                "channel": info.get("channel", info.get("uploader", "Unknown")),
                "duration": info.get("duration_string", "N/D"),
                "date": info.get("upload_date", "N/D"),
            }
    except (subprocess.TimeoutExpired, json.JSONDecodeError):
        pass
    return {"title": "Unknown", "channel": "Unknown", "duration": "N/D", "date": "N/D"}


def process_video(url, langs):
    """Process a single video through the fallback chain."""
    video_id = extract_video_id(url)
    metadata = get_video_metadata(url)

    result = {
        "video_id": video_id,
        "url": url,
        "title": metadata["title"],
        "channel": metadata["channel"],
        "duration": metadata["duration"],
        "date": metadata["date"],
        "transcript_source": None,
        "transcript": None,
        "status": "PENDENTE",
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        # Level 1: Manual subtitles
        print(f"  [{video_id}] Trying manual subtitles...", file=sys.stderr)
        text = try_subtitles(url, langs, tmpdir, sub_type="manual")
        if text:
            result["transcript_source"] = "manual_subtitles"
            result["transcript"] = clean_vtt(text)
            result["status"] = "OBTIDA"
            print(f"  [{video_id}] Got manual subtitles ({len(result['transcript'])} chars)", file=sys.stderr)
            return result

        # Level 2: Auto-generated captions
        print(f"  [{video_id}] Trying auto-captions...", file=sys.stderr)
        text = try_subtitles(url, langs, tmpdir, sub_type="auto")
        if text:
            result["transcript_source"] = "auto_captions"
            result["transcript"] = clean_vtt(text)
            result["status"] = "OBTIDA"
            print(f"  [{video_id}] Got auto-captions ({len(result['transcript'])} chars)", file=sys.stderr)
            return result

    # Level 3: No transcript available
    print(f"  [{video_id}] No transcript available — marking PENDENTE", file=sys.stderr)
    return result


def main():
    urls, output_dir, langs = parse_args(sys.argv)

    if not shutil.which("yt-dlp"):
        print("Error: yt-dlp not found. Install with: pip install yt-dlp", file=sys.stderr)
        sys.exit(1)

    print(f"Processing {len(urls)} video(s)...", file=sys.stderr)
    results = []
    for url in urls:
        print(f"\nProcessing: {url}", file=sys.stderr)
        result = process_video(url, langs)
        results.append(result)

    # Output JSON
    output = {
        "total": len(results),
        "obtained": sum(1 for r in results if r["status"] == "OBTIDA"),
        "pending": sum(1 for r in results if r["status"] == "PENDENTE"),
        "results": results,
    }

    json_output = json.dumps(output, indent=2, ensure_ascii=False)

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, "transcripts.json")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(json_output)
        print(f"\nSaved to: {filepath}", file=sys.stderr)
    else:
        print(json_output)

    # Summary
    print(f"\nSummary: {output['obtained']}/{output['total']} transcripts obtained", file=sys.stderr)
    for r in results:
        status_icon = "OK" if r["status"] == "OBTIDA" else "PENDENTE"
        source = f" ({r['transcript_source']})" if r["transcript_source"] else ""
        print(f"  [{status_icon}] {r['title'][:60]}{source}", file=sys.stderr)


if __name__ == "__main__":
    main()
