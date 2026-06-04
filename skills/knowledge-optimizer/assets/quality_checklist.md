# Quality Validation Checklist

**Updated:** 2026-02-19 | **Used in:** SKILL.md Step 4

Validate every output against this checklist before delivering to the user.

## Chunk Size

- [ ] Minimum: 100 tokens (below this = fragmented context)
- [ ] Maximum: 800 tokens (above this = noise in retrieval)
- [ ] Target range: 400-600 tokens (sweet spot per Pinecone 2024)
- [ ] >80% of chunks within target range

## Overlap

- [ ] Minimum: 10% of chunk size
- [ ] Maximum: 20% of chunk size
- [ ] Consistent across all chunk boundaries

## Metadata (all fields required)

- [ ] `document_id` present and unique
- [ ] `chunk_index` sequential (0, 1, 2, ...)
- [ ] `keywords` present (at least 3 per chunk)
- [ ] `content_type` specified (procedural, FAQ, informational, etc.)
- [ ] `source` — original filename or description
- [ ] `created_at` — ISO date

## Content Quality

- [ ] No encoding errors (mojibake, broken characters)
- [ ] Consistent language (monolingual chunks)
- [ ] Proper capitalization
- [ ] No excessive punctuation
- [ ] Contextual summary present in each chunk (Anthropic technique)

## Cross-References

- [ ] All `related_chunks` IDs exist in the output
- [ ] No circular references
- [ ] `linked_document` valid (for Hybrid mode)
