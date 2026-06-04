# Knowledge Optimizer — References Index

**Updated:** 2026-02-19

Quick index of all reference files in this skill. Each reference is self-contained and can be read independently.

| File | Purpose | When to Consult |
|------|---------|----------------|
| `rag_best_practices.md` | Research-backed RAG parameters (chunk sizes, overlap, search methods) | Step 3: choosing chunking parameters |
| `claude_guidelines.md` | Claude-specific optimization (XML tags, context windows, document structure) | Step 3: Mode 2 (Claude Project) |
| `transcription_patterns.md` | PT-BR transcription cleaning patterns (fillers, fixes, topic markers) | Step 3: Transcription Cleaning |
| `exemplos.md` | Complete input→output examples for all modes, validation report template, metadata schema | Step 4: validation, any step for reference |

**Assets** (in `../assets/`):

| File | Purpose | When to Consult |
|------|---------|----------------|
| `quality_checklist.md` | Validation checklist for output quality | Step 4: validate output |

**Scripts** (in `../scripts/`):

| File | Purpose | How to Run |
|------|---------|-----------|
| `analyze_content.py` | Automated content quality analysis | `python scripts/analyze_content.py <file>` |
| `chunk_and_optimize.py` | Multi-mode chunking engine | `python scripts/chunk_and_optimize.py <file> <mode>` |
