---
name: knowledge-optimizer
description: Use when user needs to transform unstructured content into RAG-optimized knowledge bases, clean transcriptions, prepare documents for Claude Projects or N8N agents, optimize for vector search. Ativar quando pedir para transformar conteudo em RAG, otimizar para Claude Projects, limpar transcricao, organizar conhecimento, estruturar documento para IA, preparar base vetorial.
intent: Skill para transformar conteudo bruto (transcricoes, artigos, manuais, Q&A) em bases de conhecimento otimizadas para RAG, Claude Projects ou agentes N8N. Resolve o problema de qualidade de retrieval em sistemas de IA: chunking ruim, metadata incompleta, overlap inadequado, mistura de idiomas, fillers em transcricao. Baseada em pesquisa Pinecone 2024 + Anthropic Contextual Retrieval + padroes PT-BR. Compativel com Opus 4.7 / Sonnet 4.6 (1M contexto).
---

# Knowledge Optimizer & RAG Transformer

**Version:** 2.1 | **Updated:** 2026-04-21

Transform any text-based content into optimized knowledge bases ready for RAG systems, Claude Projects, or N8N agents through intelligent analysis, cleaning, and enrichment.

## When to Use

Activate this skill when requests involve:
- "Transform this into RAG format" / "Transformar em formato RAG"
- "Optimize this for Claude Projects" / "Otimizar para Claude Projects"
- "Clean up this transcription" / "Limpar essa transcricao"
- "Prepare this document for vector search" / "Preparar para busca vetorial"
- "Analyze the quality of this knowledge base" / "Analisar qualidade da base"
- "Organizar conhecimento para agente" / "Estruturar documento para IA"
- Any request involving **knowledge base optimization**, **RAG preparation**, or **document structuring** for AI systems

### When NOT to Use

Do **not** use this skill for:
- **Pure source code** — use code-specific tools; code has its own structure that chunking breaks
- **Structured tabular data** (CSV, spreadsheets) — use data processing approaches; tables need row integrity
- **Binary files or images** — this skill handles text-based content only
- **Real-time data streams** — this skill processes static documents, not streams
- **Single short texts** (<100 words) — too small to benefit from chunking or optimization

## Quick Start

### Step 1: Analyze Content Quality

**Do:** Use `Read` to load the user's file. Use `TodoWrite` to create 4 todos (Analyze, Choose Mode, Transform, Validate). Run `python scripts/analyze_content.py <file>` via `Bash` for automated metrics.

**Assess** the content across these dimensions:
- **Redundancy** — detect duplicate information and repetitive content
- **Language quality** — identify filler words, clarity issues, jargon
- **Structure** — assess hierarchy, organization, and flow
- **Content type** — classify as procedural, FAQ, narrative, technical, mixed

**WHY:** Analysis determines **content type** which dictates optimal **mode** and **parameters**. Skipping leads to wrong chunking strategy and poor retrieval quality.

**Exit criteria:** You have a quality report with scores for each dimension, content type identified, and recommended mode determined.
**If analysis fails** (encoding error, binary file, empty content) → inform user, request valid text file. Do not proceed.

---

### Step 2: Choose Transformation Mode

**Use the decision tree** below to suggest a mode, then **confirm with the user** via `AskUserQuestion`:

| Signal in Input | Recommended Mode |
|-----------------|------------------|
| Q&A pairs, FAQ format, support scripts | **N8N Agent** |
| Long unstructured text, articles, manuals | **RAG Standard** |
| PT-BR transcription with fillers/stuttering | **Transcription Cleaning** first, then RAG or Claude |
| Technical docs with clear hierarchy | **Claude Project** |
| Need both human navigation + automated retrieval | **Hybrid** |
| Mixed content types in same document | Split by section, apply appropriate mode to each |

**Present the suggested mode** with reasoning from the analysis, and offer all 4 modes:
- **RAG Standard** — for N8N, LangChain, general vector databases
- **Claude Project** — for persistent context with XML structure
- **N8N Agent** — three-layer architecture for conversational agents
- **Hybrid** — both Claude Project and RAG versions, linked by document IDs

**WHY:** User confirmation prevents wasting effort on the wrong format. The decision tree automates 80% of cases but edge cases need human judgment.

**Exit criteria:** User has confirmed the transformation mode. If user is unsure, explain trade-offs and recommend based on their use case.
**If user wants a mode not listed** → ask for their target system's requirements and adapt.

---

### Step 3: Execute Transformation

**Apply** the selected mode following the detailed instructions in the **Transformation Modes** section below.

**Core parameters** (unified baseline — Pinecone 2024):
- **Chunk size:** 400-600 tokens (sweet spot; 512 as default baseline — 95% accuracy retention with 75% cost reduction)
- **Overlap:** 10-20% of chunk size (prevents context loss at boundaries; 15% = ~77 tokens default)
- **Contextual embeddings:** Add LLM-generated context summary to each chunk (Anthropic 2024 technique — 49% fewer retrieval failures)

**WHY:** These parameters are research-backed defaults. Chunks too small (<100 tokens) fragment context; too large (>800 tokens) introduce noise in retrieval.

**Exit criteria:** All content transformed, all chunks within size range, metadata complete on every chunk.
**If transformation produces chunks outside range** → re-split oversized chunks at sentence boundaries; merge undersized chunks with adjacent ones.

---

### Step 4: Validate and Package

**Validate** against `assets/quality_checklist.md` — check each item explicitly:

1. **Verify chunk sizes** — confirm >80% of chunks are in the 400-600 token range
2. **Verify overlap** — confirm 10-20% overlap between consecutive chunks
3. **Verify metadata** — confirm every chunk has `document_id`, `chunk_index`, `keywords` (3+), `content_type`
4. **Verify cross-references** — confirm all `related_chunks` IDs exist, no circular references
5. **Verify content quality** — no encoding errors, consistent language, proper capitalization

**Generate a validation report** using the template in `references/exemplos.md` (section "Validation Report Template"). Include: chunk count, avg/min/max token size, overlap %, metadata completeness %, quality issues found.

**Save output** via `Write` with descriptive filename: `{source_name}_{mode}_{date}.{ext}`

**Present** before/after metrics summary to user: word count delta, chunk count, quality score, issues found.

**WHY:** Validation catches chunking errors before they reach production. A single malformed chunk can cause retrieval failures.

**Exit criteria:** All checklist items pass, validation report generated, output file saved, user received summary.
**If validation fails** → report which checks failed with specifics. Use `AskUserQuestion` to ask whether to fix issues or proceed with warnings.

---

## Transformation Modes

### Mode 1: RAG Standard

Optimized for **semantic search** and **retrieval systems**.

1. **Split** content into 400-600 token chunks using recursive method (respect paragraph/sentence boundaries) — WHY: recursive preserves semantic coherence vs fixed-size which cuts mid-sentence
2. **Add overlap** of 10-20% between consecutive chunks — WHY: prevents context loss at boundaries
3. **Enrich** each chunk with metadata: `document_id`, `chunk_index`, `keywords`, `content_type`, `confidence_score`, `related_chunks`
4. **Add contextual summary** at the start of each chunk (Anthropic 2024 technique) — WHY: 49% fewer retrieval failures
5. **Output** as JSON with embeddings-ready structure

### Mode 2: Claude Project Optimized

Human-readable with **AI-optimized structure**.

1. **Organize** content hierarchically with `<document>`, `<section>`, `<context>` XML tags — WHY: Claude was trained with XML and pays special attention to this structure
2. **Preserve** full context between sections (no chunking) — WHY: Claude Projects use full-context retrieval, not chunk-based
3. **Add** document metadata and cross-references between sections
4. **Format** as Markdown with semantic XML markup

### Mode 3: N8N Agent Knowledge

Structured for **conversational agent** workflows.

1. **Extract** Q&A pairs from content — WHY: N8N agents retrieve by intent matching, not semantic similarity
2. **Structure** in three-layer architecture: System (instructions), Input (knowledge), Action (tool calls)
3. **Add** intent classification and follow-up actions per entry — WHY: enables agent routing and proactive suggestions
4. **Output** as JSON with tool-calling patterns

### Mode 4: Hybrid Output

**Best of both worlds** — human navigation + automated retrieval.

1. **Create** Claude Project version (Mode 2) for human access
2. **Create** RAG Standard version (Mode 1) for automated retrieval
3. **Link** both versions by shared `document_id` — WHY: enables cross-reference between human and machine views
4. **Output** two files: `{name}_claude.md` and `{name}_rag.json`

### Special: Transcription Cleaning

For content identified as **transcriptions** (PT-BR or other languages):

1. **Remove** filler words — consult `references/transcription_patterns.md` for PT-BR patterns. WHY: fillers add noise without information, reducing retrieval precision
2. **Fix** grammatical issues while preserving original intent — never change meaning
3. **Remove** repetitions and stuttering — merge repeated ideas into single clear statement
4. **Detect** topic changes (markers: "passando para...", "mudando de assunto...") and **restructure** hierarchically
5. **Generate** before/after comparison for user review — WHY: user must verify no content was lost

Choose cleaning level based on target audience:
- **Aggressive** (formal publications): remove 90%+ fillers, full restructure
- **Moderate** (instructional content): remove 60-70% fillers, basic structure
- **Light** (casual/conversational): remove 30-40% fillers, minimal changes

## Output Examples

See `references/exemplos.md` for **complete input→output examples** with annotations for all modes (Transcription Cleaning, RAG Standard, N8N Agent, Hybrid, edge cases, and contra-examples).

## Quality Validation

**Validate** every output against these standards:

| Metric | Target Range | WHY |
|--------|-------------|-----|
| **Chunk size** | 400-600 tokens (min 100, max 800) | Sweet spot per RAG research; too small = fragmented context, too large = noise in retrieval |
| **Overlap** | 10-20% of chunk size | Prevents context loss at boundaries without excessive duplication |
| **Metadata fields** | 100% of `document_id`, `chunk_index`, `keywords`, `content_type` | Enables filtered retrieval and provenance tracking |
| **Cross-references** | All `related_chunks` IDs exist, no circular refs | Broken references cause retrieval errors |
| **Content quality** | No encoding errors, consistent language, proper formatting | Garbage in = garbage out |

## Anti-Patterns

**NEVER do these** — each has documented consequences:

1. **NEVER chunk without overlap** — causes context loss at boundaries; retrieval quality drops 30%+ (Pinecone 2024)
2. **NEVER skip the analysis step** — analysis determines content type which dictates mode and parameters; skipping leads to wrong chunking strategy
3. **NEVER mix languages in the same chunk** — bilingual chunks confuse embeddings and reduce retrieval accuracy by 40%+
4. **NEVER ignore source metadata** — chunks without provenance (source, date, section) are unverifiable and reduce trust in retrieval results
5. **NEVER blindly chunk everything** — evaluate content quality first; noise in = noise out in knowledge bases
6. **NEVER use fixed-size chunking on structured content** — breaks tables, lists, and code blocks mid-element; use recursive chunking that respects structural boundaries. Consequence: broken chunks return garbage in retrieval
7. **NEVER remove content without user confirmation** — aggressive cleaning may delete important nuances the user needs. Consequence: data loss that cannot be recovered
8. **NEVER produce chunks without validating the output** — unvalidated chunks may have encoding errors, empty content, or broken metadata. Consequence: silent failures in production retrieval
9. **NEVER hardcode parameters without justification** — every numeric parameter (chunk size, overlap %, confidence threshold) must have a research citation or explicit rationale. Consequence: cargo-cult settings that may not fit the use case

**VERIFY at each step:** Before moving to the next workflow step, confirm the current step's exit criteria are met. Do not proceed with incomplete results.

## Best Practices

1. **Always analyze before transforming** — analysis identifies content type which determines optimal mode and parameters. Skipping risks wrong chunking strategy.
2. **Confirm aggressive changes with user** — use `AskUserQuestion` before aggressive transcription cleaning or major restructuring. WHY: prevents data loss.
3. **Preserve examples and specifics** — examples are often the most-retrieved content in knowledge bases. WHY: high retrieval value.
4. **Test retrieval quality with sample queries** — validates that chunks are semantically coherent and retrievable. WHY: catches chunking errors early.
5. **Provide before/after metrics** — word count, chunk count, quality scores. WHY: gives user confidence in transformation quality.
6. **Match destination system requirements** — N8N expects JSON, Claude Projects benefit from XML, vector DBs need embeddings-ready format. WHY: wrong format = integration failures.
7. **Save outputs with descriptive names** — use `Write` with `{source}_{mode}_{date}.{ext}`. WHY: enables comparison and rollback.

## Limits and Edge Cases

| Scenario | Action | Fallback |
|----------|--------|----------|
| **Empty or corrupted input** | Inform user, request valid file. Do not proceed. | If user insists file is valid → check encoding (UTF-8, Latin-1), try re-reading with explicit encoding. |
| **Document >100k tokens** | Split into logical sections first (by chapter/heading), process each independently, link via `document_id`. | If no clear sections → split at ~50k token boundaries at paragraph breaks. |
| **Mixed languages (PT + EN)** | Separate by language before chunking. Each chunk must be monolingual. | If separation is impractical → tag each chunk with `language` metadata field. |
| **Non-textual content** (images, tables) | Flag to user. Extract text descriptions where possible, note limitations in metadata. | For complex tables → convert to structured text representation preserving row/column relationships. |
| **Validation fails** | Report which checks failed with specifics. Ask user whether to fix or proceed with warnings. | If >50% of checks fail → recommend re-running from Step 1 with different parameters. |
| **Source code or structured data** | This skill handles prose/text. For code, suggest code-specific tools. For CSV/JSON, suggest data processing. | If code is embedded in documentation → extract prose, keep code as-is in separate chunks tagged `content_type: code`. |
| **Content with PII/credentials** | Flag immediately. Never include PII in chunks without explicit user acknowledgment. | Suggest redaction patterns or PII masking before processing. |
| **Script execution fails** (encoding, missing deps) | Report the error. Proceed manually without scripts — scripts are helpers, not requirements. | Try with explicit `encoding='utf-8'` or `encoding='latin-1'`. |
| **Input quality too low** (>80% fillers, no real content) | Inform user that content quality is insufficient for meaningful optimization. | Suggest transcription cleaning first, then re-evaluate. Threshold: clarity_score < 3/10. |

## Claude Code Integration

**Use these tools** at each workflow step:

| Step | Tools | How | Error Handling |
|------|-------|-----|----------------|
| **Detect input type** | `Glob` | Run `Glob` with `**/*.{md,txt,json,pdf}` to identify file types in user's directory | If no files found → ask user for explicit path |
| **Read input** | `Read` | Load user's file with `Read` | If file too large → read in chunks with `offset` and `limit` |
| **Track progress** | `TodoWrite` | Create 4 todos (Analyze, Choose Mode, Transform, Validate) and update as you go | — |
| **Analyze** | `Bash` | Run `python scripts/analyze_content.py <file>` for automated metrics | If script fails → analyze manually using the dimensions in Step 1 |
| **Choose mode** | `AskUserQuestion` | Present decision tree result + all 4 modes, ask user to confirm | — |
| **Transform** | `Bash` | Run `python scripts/chunk_and_optimize.py <file> <mode>` for chunking | If script fails → transform manually following mode instructions |
| **Parallel processing** | `Task` (subagents) | For documents >50k tokens: dispatch one subagent per section to analyze/transform in parallel | If subagent fails → fall back to sequential processing |
| **Confirm changes** | `AskUserQuestion` | Before aggressive cleaning, show preview and ask for confirmation | — |
| **Save output** | `Write` | Save transformed content with descriptive filename | — |
| **Report** | Text output | Present before/after metrics summary to user | — |

## Resources

### Scripts
- `analyze_content.py` — content quality analyzer. Run: `python scripts/analyze_content.py <file>`
- `chunk_and_optimize.py` — multi-mode chunking engine. Run: `python scripts/chunk_and_optimize.py <file> <mode>`

### References
- `rag_best_practices.md` — research-backed optimization techniques (Pinecone 2024, Anthropic 2024)
- `claude_guidelines.md` — Claude-specific best practices (XML tags, context windows)
- `transcription_patterns.md` — Portuguese language cleaning patterns and quality targets
- `exemplos.md` — complete input→output examples with annotations for all modes + validation report template

### Assets
- `quality_checklist.md` — validation checklist (consult in Step 4)

---

### Adding a New Transformation Mode

To extend this skill with a new mode:
1. Add the mode description to **Transformation Modes** section with numbered steps
2. Add a complete input→output example to `references/exemplos.md` with annotations
3. Add the mode to the **decision tree** in Step 2 with triggering signals
4. Update `scripts/chunk_and_optimize.py` if the mode has specific chunking logic
5. Test with 3+ real documents to validate output quality

### Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-02-18 | Initial version: 4 modes, analysis workflow, PT-BR cleaning |
| 1.5 | 2026-02-18 | T1-T8: Anti-patterns, edge cases, Claude Code integration, exemplos.md, triggers PT-BR |
| 2.0 | 2026-02-19 | T9-T19: Decision tree, imperative rewrite, fallback chains, output templates, expanded anti-patterns, negative triggers, versioning, numeric consistency |
| 2.1 | 2026-04-21 | Migracao Opus 4.7: frontmatter com `intent`; context window atualizado para 1M (4.7/4.6) nos references; nota sobre tokenizer +35% em `rag_best_practices.md` |
