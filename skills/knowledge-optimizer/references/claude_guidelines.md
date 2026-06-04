# Claude Project Optimization

**Updated:** 2026-04-21 | **Sources:** Anthropic Documentation 2024, Claude API docs, Opus 4.7 release notes (abr/2026)

This reference provides Claude-specific best practices for structuring documents in Claude Projects. Use when transforming content for Claude Project mode in the knowledge-optimizer skill.

## Table of Contents

1. [Key Features](#key-features)
2. [XML Tags](#xml-tags)
3. [Document Structure](#document-structure)
4. [File Format Priority](#file-format-priority)
5. [Contextual Retrieval](#contextual-retrieval)
6. [Best Practices](#best-practices)

---

## Key Features

| Feature | Detail |
|---------|--------|
| **Context window** | 1M tokens (Opus 4.7 / Sonnet 4.6) — varia por modelo |
| **Persistence** | Content persists across conversations in the same project |
| **RAG activation** | Auto-activated for large project knowledge bases |
| **XML support** | Claude was trained with XML — pays special attention to this structure |

## XML Tags

Claude was trained with XML and responds strongly to tag-based structure. Use XML tags to organize content for optimal Claude retrieval and comprehension.

**Standard patterns:**
```xml
<instructions>Task instructions</instructions>
<context>Background info for the section</context>
<document id="unique_id">Full document content</document>
<section level="1">Main section</section>
<procedure>Step-by-step instructions</procedure>
```

**Custom tags:** Use any semantic name — format matters more than tag names: `<tag>content</tag>`

**Best practice:** Use descriptive tag names that match the content's purpose (e.g., `<policy>`, `<faq>`, `<guideline>`).

## Document Structure

```xml
<document id="doc_001" title="Guide Title" version="1.0">
<section level="1" id="overview">
# Overview
<context>High-level description of this section's purpose</context>
Content here...

<subsection level="2" id="details">
## Details
More specific content...
</subsection>
</section>

<section level="1" id="next-topic">
# Next Topic
<context>What this topic covers and why it matters</context>
<cross-reference target="overview">Related to the overview section.</cross-reference>
Content...
</section>
</document>
```

**Key principles:**
- Use `id` attributes for cross-referencing between sections
- Use `<context>` blocks to help Claude understand section purpose before reading content
- Preserve Markdown formatting inside XML for human readability
- Use semantic IDs (not numeric) for easier reference

## File Format Priority

Ranked by Claude's processing effectiveness:

| Priority | Format | Notes |
|----------|--------|-------|
| 1 | PDFs (searchable, <100 pages) | Best for structured documents |
| 2 | Markdown (.md) | Excellent for mixed content |
| 3 | Word (.docx) | Good, but may lose some formatting |
| 4 | CSV/Excel | Good for tabular data |
| 5 | HTML | Acceptable, may have noise from markup |
| 6 | Code files | Good for reference, but use code-specific tools for analysis |

## Contextual Retrieval (Anthropic 2024)

Add LLM-generated context summary to each chunk/section before embedding:

| Technique | Improvement |
|-----------|-------------|
| Contextual embeddings alone | 49% fewer retrieval failures |
| Contextual + reranking | 67% fewer retrieval failures |
| Contextual + prompt caching | 90% cost reduction |

**How to apply:** Prepend a 1-2 sentence context summary to each chunk that situates it within the full document. Example: "This section covers contraindications for dental whitening procedures, part of the dental aesthetics manual."

## Best Practices

1. **Use clear hierarchy** with headers (H1 → H2 → H3) — Claude navigates hierarchical structure more effectively
2. **Wrap key sections in XML tags** — `<context>`, `<instructions>`, `<procedure>` — Claude pays special attention to tagged content
3. **Add context blocks** per section — helps Claude understand purpose before reading details
4. **Include metadata** — author, version, date — enables Claude to assess recency and source authority
5. **Use searchable text only** — avoid images-as-text; Claude can't OCR embedded images in Projects
6. **Use descriptive filenames** — `dental_whitening_protocol_v2.md` not `doc1.md` — Claude uses filenames for context
7. **Group related documents** — keep related content together for cross-referencing
