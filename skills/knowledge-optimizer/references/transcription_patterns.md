# Portuguese Transcription Patterns

**Updated:** 2026-02-19 | **Language:** Brazilian Portuguese (PT-BR)

This reference provides patterns for cleaning Brazilian Portuguese transcriptions. Use when the knowledge-optimizer skill identifies content as a transcription (audio/video to text) that needs cleaning before optimization.

## Table of Contents

1. [Common Fillers](#common-fillers)
2. [Cleaning Strategy](#cleaning-strategy)
3. [Common Fixes](#common-fixes)
4. [Topic Change Markers](#topic-change-markers)
5. [Quality Targets](#quality-targets)

---

## Common Fillers (Brazilian Portuguese)

Fillers are words that add no information. Remove based on the chosen cleaning level.

| Frequency | Words | Occurrence Rate |
|-----------|-------|----------------|
| **Very frequent** | entao, ne, tipo, assim | >5% of words |
| **Frequent** | e..., ahn/hum, bom, ta, sabe | 2-5% of words |
| **Moderate** | basicamente, na verdade, meio que, sei la | 1-2% of words |

**Detection tip:** If `filler_pct` from `analyze_content.py` is >5%, content is likely a transcription.

## Cleaning Strategy

Choose level based on the target audience and content purpose:

| Level | Filler Removal | Grammar Fixes | Restructuring | When to Use |
|-------|---------------|---------------|---------------|-------------|
| **Aggressive** | 90%+ | Fix all | Complete | Formal publications, official docs, marketing |
| **Moderate** | 60-70% | Fix major | Basic structure (headings, sections) | Instructional content, training material |
| **Light** | 30-40% | Minimal | Minimal | Casual content, interviews, podcasts |

**WHY these levels:** Aggressive cleaning produces professional-grade content but may lose speaker personality. Light cleaning preserves voice but may be hard to read. Moderate is the safe default.

**Decision rule:** When in doubt, use **Moderate**. Ask user with `AskUserQuestion` if context suggests Aggressive or Light would be better.

## Common Fixes

| Spoken (PT-BR) | Written | Note |
|----------------|---------|------|
| pra | para | Always fix |
| ta | esta | Always fix |
| ne | (remove) | Filler — no replacement needed |
| ce | voce | Informal contraction |
| num | nao/em um | Depends on context |
| to | estou | Informal contraction |
| vamo(s) la | vamos | Informal emphasis |

## Topic Change Markers

These phrases in PT-BR signal a topic change. Use them to detect section boundaries and restructure into headings:

| Marker | Indicates |
|--------|-----------|
| "entao agora vamos falar sobre..." | New topic introduction |
| "passando para..." | Transition to next topic |
| "mudando de assunto..." | Explicit topic change |
| "voltando ao tema..." | Return to previous topic — may need reordering |
| "bom, outro ponto importante..." | New subtopic |
| "para finalizar..." / "por ultimo..." | Final topic — closing section |

**Action on detection:** Create a new heading (`##` or `###`) with the topic name extracted from the marker.

## Quality Targets

| Metric | Target | Signal of Problem |
|--------|--------|-------------------|
| Filler reduction | 50-80% (varies by level) | <30% = cleaning insufficient |
| Length reduction | 15-25% | >40% = possible content loss — review |
| Clarity improvement | 5-6/10 → 8-9/10 | <7/10 after cleaning = needs manual review |
| Meaning preservation | 100% | Any meaning change = cleaning too aggressive |
| Topic restructuring | All topic changes detected | Missed topic = review markers list |
