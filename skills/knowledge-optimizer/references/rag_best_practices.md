# RAG Best Practices (2024-2025)

**Updated:** 2026-04-21 | **Sources:** Pinecone 2024, Anthropic 2024, LangChain docs, Opus 4.7 release notes (abr/2026)

This reference provides research-backed parameters and techniques for RAG (Retrieval-Augmented Generation) systems. Use alongside the knowledge-optimizer skill for optimal chunking, embedding, and retrieval configuration.

## Table of Contents

1. [Optimal Chunk Sizes](#optimal-chunk-sizes)
2. [Overlap Strategy](#overlap-strategy)
3. [Chunking Methods](#chunking-methods)
4. [Hybrid Search](#hybrid-search)
5. [Reranking](#reranking)
6. [Context Windows](#context-windows)
7. [Metadata Types](#metadata-types)
8. [Production Guidelines](#production-guidelines)
9. [Common Pitfalls](#common-pitfalls)

---

## Optimal Chunk Sizes

| Content Type | Recommended Size | Rationale |
|-------------|-----------------|-----------|
| **General RAG** | 400-600 tokens (512 default) | Pinecone 2024 baseline — 95% accuracy with 75% cost reduction |
| **Technical docs** | 400-500 tokens | Slightly smaller preserves precision of technical terms |
| **Support logs** | 150-250 tokens | Short interactions need tight chunks for accurate retrieval |
| **Research papers** | 300 tokens + 50 overlap | Dense content benefits from smaller chunks |

## Overlap Strategy

- **Standard:** 10-20% of chunk size
- **Purpose:** Preserve context at chunk boundaries — prevents information loss when a concept spans two chunks
- **Example:** 512 tokens chunk → 51-102 token overlap (15% = ~77 tokens)
- **Trade-off:** Higher overlap = more redundancy but better boundary handling

## Chunking Methods

| Method | Description | When to Use |
|--------|-------------|-------------|
| **Fixed-Size** | Split at exact token counts | Start here for unknown content; predictable but may cut mid-sentence |
| **Recursive** | Respects paragraphs/sentences | Recommended default — preserves semantic coherence |
| **Semantic** | Groups by topic similarity | Experimental; high quality but slow and compute-intensive |
| **Contextual** (Anthropic 2024) | Adds LLM-generated context to each chunk | Best quality — 49% fewer retrieval failures; adds processing cost |

## Hybrid Search (Industry Standard)

- **BM25** (sparse): Exact keyword matches — good for proper nouns, codes, IDs
- **Vector** (dense): Semantic meaning — good for paraphrased queries
- **Combined**: Best of both — 43% better than vector alone (Pinecone 2024)
- **RRF Formula**: `RRF_score = Σ(1 / (k + rank_i))` where k=60

## Reranking

- Essential refinement step after initial retrieval
- **Cohere Rerank 3**: Industry leader, 49% improvement over no reranking
- **Process**: Retrieve 20-50 candidates → Rerank by relevance → Return top 3-5
- **Cost-benefit**: Small compute cost for large quality gain

## Context Windows

| Model | Context Window |
|-------|---------------|
| Claude Opus 4.7 / Sonnet 4.6 | 1M tokens (nativo, abr/2026) |
| Claude Haiku 4.5 | 200K tokens |
| GPT-4 | 128K tokens |
| Gemini 1.5 | 2M tokens |

**Key Finding** (Pinecone 2024): RAG preserves 95% accuracy using only 25% of tokens = 75% cost reduction vs stuffing full context. Mesmo com 1M de contexto disponível no 4.7/4.6, RAG continua ganhando em custo e latência.

**Optimal fill**: 40-70% of context window — leave room for instructions and output.

**Atenção ao tokenizer (Opus 4.7):** o novo tokenizer consome 1.0×–1.35× mais tokens que o 4.6 para o mesmo texto. Adicionar ~35% de headroom em cálculos de custo e em `max_tokens` ao planejar chunks/prompts para evitar truncamento.

## Metadata Types

| Category | Fields | Purpose |
|----------|--------|---------|
| **Source** | title, author, date, version | Provenance and trust |
| **Structural** | section, page, hierarchy, chunk_index | Navigation and ordering |
| **Content** | keywords, content_type, language | Filtering and classification |
| **Quality** | confidence_score, verification_status | Trust signals for retrieval ranking |

## Production Guidelines

1. **Quality > Quantity** — curate sources before ingesting; garbage in = garbage out
2. **Update pipelines** — implement delta processing to keep index current
3. **Evaluation framework** — test with real user queries, measure precision/recall
4. **Monitor and iterate** — track retrieval accuracy over time, adjust parameters

## Common Pitfalls

| Pitfall | Impact | Fix |
|---------|--------|-----|
| Using only vector search | Misses exact matches (codes, IDs) | Always use hybrid (BM25 + vector) |
| Ignoring overlap | Context loss at boundaries | 10-20% overlap mandatory |
| No reranking | Missing 30-49% quality improvement | Add reranking step |
| Static indexes | Content goes stale | Implement update pipeline |
| Wrong chunk size | Too small = fragmented; too large = noise | Target 400-600 tokens |
| No metadata | Can't filter or trace provenance | Always include source + structural metadata |
