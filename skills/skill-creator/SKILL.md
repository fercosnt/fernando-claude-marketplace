---
name: skill-creator
description: >-
  Create, improve, and evaluate skills. Use when creating a skill from
  scratch, editing or optimizing an existing skill, running evals, or
  benchmarking skill performance.
intent: >-
  Full lifecycle skill for creating skills: intent capture, SKILL.md writing,
  subagent testing, qualitative and quantitative evaluation, description
  optimization for triggering, and packaging. Supports three paths: guided
  wizard, content-first, and improving an existing skill.
---

# Skill Creator

A skill for creating new skills and iteratively improving them.

At a high level, the process goes like this:

- Decide what you want the skill to do and roughly how it should do it
- Write a draft of the skill
- Create test prompts and run claude-with-access-to-the-skill on them
- Help the user evaluate the results both qualitatively and quantitatively
  - While runs happen in the background, draft quantitative evals if there aren't any. Then explain them to the user.
  - Use the `eval-viewer/generate_review.py` script to show the user the results, and also let them look at the quantitative metrics
- Rewrite the skill based on feedback from evaluation
- Repeat until satisfied
- Expand the test set and try again at larger scale

Your job is to figure out where the user is in this process and jump in. Maybe they have just an idea, maybe they have material ready, maybe they want to improve an existing skill. Read on for how to handle each case.

Cool? Cool.

## Communicating with the user

The skill creator is used by people across a wide range of familiarity with coding jargon. Pay attention to context cues to understand how to phrase your communication! In the default case:

- "evaluation" and "benchmark" are borderline, but OK
- for "JSON" and "assertion" you want to see serious cues from the user that they know what those things are before using them without explaining them

It's OK to briefly explain terms if you're in doubt.

---

## Preflight: Check for Existing Skills

Before creating anything, check if a similar skill already exists. This prevents duplicate skills and guides users to the right path.

1. **Search for existing skills** — use glob/search across the user's skill directories (`.claude/skills/`, project `skills/`, installed plugins) looking for skills with similar names or keywords.
2. **Compare functionality** — read the `description` and `intent` of any matches. Does the proposed skill overlap significantly?
3. **Present findings** — if you find similar skills, show them to the user:
   - "I found a skill called `[name]` that does [X]. Want to improve that one instead, or create a new one?"
   - Options: (a) proceed with new skill, (b) switch to improving the existing one, (c) cancel.

If no similar skills are found, proceed with creation. If the user is already pointing at an existing skill to improve, skip preflight — they've already made their choice.

---

## Path Detection

Before diving in, figure out which creation path fits the user's situation. There are four:

| Path | User has... | Flow |
|------|------------|------|
| **Wizard** | Just an idea, no material | Preflight -> Interview -> Draft -> Test -> Iterate |
| **Content-first** | Material ready (notes, framework, research, example workflow) | Preflight -> Analyze material -> Generate skill -> Test -> Iterate |
| **Manual + validation** | An existing skill to improve | Load skill -> Run evals -> Identify gaps -> Improve -> Re-test |
| **Model migration** | Existing skill(s) + research on a new Claude model | Load research -> Apply migration checklist per skill -> Re-test |

**Auto-detection heuristics:**
- "Create a skill for X" without attachments -> Wizard
- User provides text, files, framework, or conversation history -> Content-first
- User wants a skill based on or similar to an existing one -> Content-first (use the existing skill's SKILL.md as input material)
- User points to existing skill or says "improve/fix/optimize/extend this skill" or wants to add features to it -> Manual + validation
- User mentions migrating skills to a new model ("update for Opus 4.7", "atualizar para [modelo novo]"), references a research file under `pesquisas/[modelo]/`, or wants to bulk-update model IDs across skills -> Model migration (Path D)
- User mentions having material but hasn't shared it yet -> ask them to share before choosing a path
- No heuristic matches clearly -> ask: "I can guide you through creating a skill from scratch (Wizard), work from material you already have (Content-first), improve an existing skill (Manual), or migrate skills to a new model (Migration). Which fits?"

Always confirm the detected path: "It looks like you [have material ready / want to improve an existing skill / want to migrate to a new model / have an idea to explore]. I'll follow the [X] path. Sound right?"

---

## Creating a skill

### Path A: Wizard (guided creation)

For users who have an idea but no material. This is the full guided flow.

#### Capture Intent

Start by understanding the user's intent. The current conversation might already contain a workflow the user wants to capture (e.g., "turn this into a skill"). If so, extract answers from the conversation history first — the tools used, the sequence of steps, corrections the user made, input/output formats observed. Confirm before proceeding.

1. What should this skill enable Claude to do?
2. When should this skill trigger? (what user phrases/contexts)
3. What's the expected output format?
4. Should we set up test cases to verify the skill works? Skills with objectively verifiable outputs benefit from test cases. Skills with subjective outputs (writing style, art) often don't. Suggest the appropriate default, but let the user decide.

#### Interview and Research

Proactively ask about edge cases, input/output formats, example files, success criteria, and dependencies. Wait to write test prompts until you've got this part ironed out.

Check available MCPs — if useful for research (searching docs, finding similar skills), research in parallel via subagents if available, otherwise inline. Come prepared with context to reduce burden on the user.

### Path B: Content-first

For users who already have material (notes, frameworks, research docs, example conversations, reference implementations).

> **Important:** This path replaces the full interview. Do not run Capture Intent or Interview and Research from Path A.

1. **Receive and analyze material** — read everything the user provides. Identify the core workflow, decision points, input/output formats, and edge cases embedded in the material.
2. **Extract structure** — map the material to skill components: what triggers it, what steps it follows, what output it produces, what patterns it enforces.
3. **Ask clarification questions** — the material won't cover everything. Ask targeted questions about gaps: "Your notes mention handling errors but don't specify how — should the skill retry, skip, or ask the user?"
4. **Generate draft** — write the SKILL.md based on extracted structure + clarifications. Present to the user for validation before testing.
5. **Enter test cycle** — proceed to test cases and iteration as normal.

### Path C: Manual + validation (improving existing skill)

For users who have a skill that needs improvement.

1. **Load the existing skill** — read its SKILL.md, understand its structure, purpose, and current state.
2. **Run evals immediately** — skip the interview. Go straight to running test cases (use existing evals if available, or create new ones based on the skill's purpose).
3. **Identify gaps** — from eval results and user feedback, identify what's not working: wrong outputs, missing edge cases, poor triggering, structural issues.
4. **Propose improvements** — present specific changes with rationale. Don't rewrite from scratch unless the skill is fundamentally broken.
5. **Iterate** — apply improvements, re-test, repeat until the user is satisfied.

See the "Improving the skill" section below for detailed guidance on how to think about improvements.

### Path D: Migrating skills to a new Claude model

For users who want to update one or more existing skills to a newer Claude model (e.g., Opus 4.6 → 4.7). This path assumes the user has already run a deep-research on the target model — typically saved at `pesquisas/[modelo]/PESQUISA-[modelo].md` (e.g., `pesquisas/opus-4-7/PESQUISA-opus-4-7.md`).

**Workflow:**

1. **Load the model research** — read the research file from `pesquisas/[modelo]/`. If it doesn't exist, suggest running `/deep-research` on the new model first.
2. **Identify the skills to migrate** — usually a focused list (e.g., "all GHL skills", "all legal-analyzer skills") or "all skills under `~/.claude/skills/`".
3. **For each skill, run the migration checklist** — see below.
4. **Apply changes per skill** — propose minimal targeted edits. Don't rewrite. If the skill has evals, re-run them after the change to confirm no regression.
5. **Update the skill's memory entry** — note the model migration in the project memory file.

**Migration checklist (apply per skill):**

| Check | What to look for | Action |
|-------|-----------------|--------|
| Hardcoded deprecated model IDs | Any file in the skill mentions `claude-3-haiku-20240307`, `claude-sonnet-4-20250514`, `claude-opus-4-20250514`, or other retired models | Replace with current model IDs from research |
| Extended Thinking with `budget_tokens` | Code or docs reference `thinking: {type: "enabled", budget_tokens: N}` | Update to `thinking: {type: "adaptive"}` per Opus 4.7 research |
| `temperature`/`top_p`/`top_k` non-default | Sampling params hardcoded in scripts | Remove (Opus 4.7 returns 400 if non-default) |
| Hardcoded `max_tokens` in scripts | Any `max_tokens=N` in Python/TS files | If migrating to Opus 4.7+, add ~35% headroom for new tokenizer |
| References to outdated context window | Docs say "200K tokens", "100K tokens" | Update to current window from research (Opus 4.7: 1M) |
| References to deprecated model names in prose | "Claude 3.5 Sonnet", "Opus 4.1", "Sonnet 4" | Update to current names |
| Skill description mentions a specific model | Description hardcodes a model ID | Decide: keep version-specific or generalize |

**When done with all skills, update memory:** create or append to `project_skills_migrated_to_[modelo].md` listing which skills were updated and what changed.

**Important:** Don't add `effort` to skill frontmatter as part of migration — it's experimental and the user typically controls effort globally in Claude Code.

---

### Write the SKILL.md

Based on the user interview or material analysis, fill in these components:

- **name**: Skill identifier (max 64 characters)
- **description**: When to trigger, what it does (max 200 characters). This is the primary triggering mechanism — include both what the skill does AND specific contexts for when to use it. All "when to use" info goes here, not in the body. Write in third person ("Creates X", not "I help create X") — the description is read by the agent picking the skill, not addressed to the user. Make descriptions a bit "pushy" to combat under-triggering. Instead of "How to build a dashboard", write "How to build a dashboard. Use whenever the user mentions dashboards, data visualization, or wants to display data, even if they don't explicitly ask for a 'dashboard.'"

**Good vs bad description (concrete contrast):**

```
GOOD: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when user mentions PDFs, forms, or document extraction.

BAD:  Helps with documents.
```

The bad one gives the agent no way to distinguish this from any other document skill — it loses every triggering competition. The good one names file types, verbs, and trigger keywords.
- **intent**: Fuller explanation of the skill's purpose, what problem it solves, and context of use. No size limit. This field is for understanding, not for triggering — it helps the model (and humans) understand the "why" behind the skill.
- **effort** *(optional, experimental — Claude Code only, added with Opus 4.7)*: Override the default reasoning effort for this skill. Valid values: `low`, `medium`, `high`, `xhigh`, `max`. **Caveat:** field-level support in frontmatter is from community sources, not officially documented by Anthropic. The user typically toggles `effort` globally in Claude Code (e.g., set to `xhigh`), so adding it here is usually redundant. Only add it if you want to FORCE a different effort for this specific skill (e.g., a heavy research skill that should always run at `max` even if the session is at `low`). Test that the skill still appears in `/help` after adding.
- **compatibility**: Required tools, dependencies (optional, rarely needed)
- **the rest of the skill :)**

The `description` and `intent` serve different purposes: `description` is the trigger mechanism (concise, action-oriented), while `intent` provides context once the skill is loaded (detailed, explanatory). Every skill generated by this skill-creator must have both fields.

**Frontmatter example (with optional `effort`):**

```yaml
---
name: deep-research
description: Pesquisa profunda e compilada sobre qualquer tópico usando subagentes paralelos. Use quando precisar pesquisar frameworks, melhores práticas, ou compilar fontes externas com profundidade.
intent: Skill para pesquisa exaustiva multi-fonte com subagentes paralelos, síntese estruturada e citação de fontes.
effort: xhigh
---
```

### Skill Writing Guide

#### Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description, intent required; effort optional)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/    - Executable code for deterministic/repetitive tasks
    ├── references/ - Docs loaded into context as needed
    └── assets/     - Files used in output (templates, icons, fonts)
```

#### Progressive Disclosure

Skills use a three-level loading system:
1. **Metadata** (name + description + intent) — Always in context (~100 words)
2. **SKILL.md body** — In context whenever skill triggers (<500 lines ideal)
3. **Bundled resources** — As needed (unlimited, scripts can execute without loading)

**Key patterns:**
- Keep SKILL.md under 500 lines; if approaching the limit, add hierarchy with clear pointers about where to go next.
- `name` max 64 characters, `description` max 200 characters
- Reference files clearly from SKILL.md with guidance on when to read them
- For large reference files (>300 lines), include a table of contents

**Domain organization**: When a skill supports multiple domains/frameworks, organize by variant:
```
cloud-deploy/
├── SKILL.md (workflow + selection)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

#### When to Add Scripts

Bundle a script in `scripts/` (instead of letting Claude regenerate code each time) when **any** of these is true:

- **Deterministic operation** — validation, formatting, parsing, packaging. Same input always produces the same output.
- **Repeated generation** — Claude would write essentially the same helper across runs. Bundle once, save tokens forever.
- **Errors need explicit handling** — retry logic, fallbacks, edge cases that are easy to forget. A script encodes them once; generated code may skip them under pressure.

Scripts cost tokens at write-time (you wrote them once) but save them at every invocation, and they're more reliable than re-generated code because they don't drift.

#### When to Split into Separate Files

Move content out of SKILL.md into `references/` when **any** of these is true:

- **Length** — SKILL.md approaching the 500-line ceiling. Aim for a sweet spot of 200–300 lines for most skills; complex orchestrators (deep-research, this skill) earn more.
- **Distinct domains** — content covers variants that aren't all needed in every invocation (e.g., AWS vs GCP vs Azure). Split per variant so only the relevant one loads.
- **Advanced/rare features** — material only needed in edge cases. Keep the main path tight, defer the long tail.

When you split, leave a clear pointer in SKILL.md: "For X, see [references/x.md](references/x.md)" — don't make the agent guess what's where.

#### Principle of Lack of Surprise

Skills must not contain malware, exploit code, or any content that could compromise system security. Don't go along with requests to create misleading skills or skills designed to facilitate unauthorized access.

#### Writing Patterns

Prefer using the imperative form in instructions.

**Defining output formats:**
```markdown
## Report structure
ALWAYS use this exact template:
# [Title]
## Executive summary
## Key findings
## Recommendations
```

**Examples pattern:**
```markdown
## Commit message format
**Example 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

### Writing Style

Explain to the model why things are important rather than heavy-handed MUSTs. Use theory of mind and try to make the skill general, not super-narrow. Start by writing a draft and then look at it with fresh eyes and improve it.

### Test Cases

After writing the skill draft, come up with 2-3 realistic test prompts. Share with the user: "Here are a few test cases I'd like to try. Do these look right, or do you want to add more?" Then run them.

Save test cases to `evals/evals.json`. Don't write assertions yet — just the prompts. You'll draft assertions in the next step while runs are in progress.

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's task prompt",
      "expected_output": "Description of expected result",
      "files": []
    }
  ]
}
```

See `references/schemas.md` for the full schema (including assertions).

## Running and evaluating test cases

This section is one continuous sequence — don't stop partway through. Do NOT use `/skill-test` or any other testing skill.

Put results in `<skill-name>-workspace/` as a sibling to the skill directory. Organize by iteration (`iteration-1/`, `iteration-2/`, etc.) and within that, each test case gets a directory. Don't create all of this upfront — just create directories as you go.

### Step 1: Spawn all runs (with-skill AND baseline) in the same turn

For each test case, spawn two subagents in the same turn — one with the skill, one without. Launch everything at once.

**With-skill run:**
```
Execute this task:
- Skill path: <path-to-skill>
- Task: <eval prompt>
- Input files: <eval files if any, or "none">
- Save outputs to: <workspace>/iteration-<N>/eval-<ID>/with_skill/outputs/
- Outputs to save: <what the user cares about — e.g., "the .docx file", "the final CSV">
```

**Baseline run** (same prompt, but depends on context):
- **Creating a new skill**: no skill at all. Save to `without_skill/outputs/`.
- **Improving an existing skill**: the old version. Snapshot first (`cp -r <skill-path> <workspace>/skill-snapshot/`), then point baseline at snapshot. Save to `old_skill/outputs/`.

Write `eval_metadata.json` for each test case with a descriptive name based on what it's testing — not just "eval-0". Use this name for the directory too. If this iteration uses new or modified prompts, create these files for each new eval directory — don't assume they carry over from previous iterations.

```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name-here",
  "prompt": "The user's task prompt",
  "assertions": []
}
```

### Step 2: While runs are in progress, draft assertions

Don't wait — draft quantitative assertions for each test case and explain them to the user. Good assertions are objectively verifiable with descriptive names. Subjective skills are better evaluated qualitatively — don't force assertions.

Update `eval_metadata.json` files and `evals/evals.json` with assertions.

### Step 3: As runs complete, capture timing data

When each subagent task completes, you receive a notification containing `total_tokens` and `duration_ms`. Save it immediately to `timing.json` in the run directory:

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

This is the only opportunity to capture this data — the notification isn't persisted elsewhere. Process each one as it arrives rather than batching.

**Note (Opus 4.7+ tokenizer):** the new tokenizer consumes 1.0×–1.35× more tokens for the same text vs Opus 4.6. If your eval workspace tracks token budgets or uses scripts that hardcode `max_tokens`, add ~35% headroom or you'll see truncated outputs.

### Step 4: Grade, aggregate, and launch the viewer

Once all runs are done:

1. **Grade each run** — spawn a grader (reads `agents/grader.md`). Save to `grading.json`. The expectations array must use fields `text`, `passed`, and `evidence`. For programmatically checkable assertions, write and run a script.

2. **Aggregate into benchmark**:
   ```bash
   python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>
   ```

3. **Analyst pass** — read benchmark data and surface patterns. See `agents/analyzer.md`.

4. **Launch the viewer**:
   ```bash
   nohup python <skill-creator-path>/eval-viewer/generate_review.py \
     <workspace>/iteration-N \
     --skill-name "my-skill" \
     --benchmark <workspace>/iteration-N/benchmark.json \
     > /dev/null 2>&1 &
   VIEWER_PID=$!
   ```
   For iteration 2+, also pass `--previous-workspace`.
   **Headless:** use `--static <output_path>` for standalone HTML.

5. **Tell the user**: "I've opened the results in your browser. There are two tabs — 'Outputs' lets you click through each test case and leave feedback, 'Benchmark' shows the quantitative comparison. When you're done, come back here and let me know."

### What the user sees in the viewer

The "Outputs" tab shows one test case at a time:
- **Prompt**: the task that was given
- **Output**: the files the skill produced, rendered inline where possible
- **Previous Output** (iteration 2+): collapsed section showing last iteration's output
- **Formal Grades** (if grading was run): collapsed section showing assertion pass/fail
- **Feedback**: a textbox that auto-saves as they type
- **Previous Feedback** (iteration 2+): comments from last time, shown below the textbox

The "Benchmark" tab shows pass rates, timing, and token usage for each configuration, with per-eval breakdowns and analyst observations.

Navigation is via prev/next buttons or arrow keys. When done, "Submit All Reviews" saves all feedback to `feedback.json`.

### Step 4.5: Trigger-Readiness Audit

Before collecting user feedback, run a quick check on whether the skill's `description` will actually trigger correctly. This catches triggering problems early — during iteration, not after packaging.

1. **Generate 10 test prompts** — 5 should-trigger (the skill is clearly needed) and 5 should-not-trigger (related but a different skill/no skill is better). Keep them realistic and concise — this is a quick check, not the full Description Optimization.
2. **Evaluate mentally** — for each prompt, assess: would an agent seeing this skill's `description` in the available skills list choose to invoke it?
3. **Score** — should-trigger hit rate should be >= 70%, should-not-trigger false positive rate should be <= 30%.
4. **Report to user** — "Quick trigger check: the skill would correctly activate for 4/5 target scenarios and correctly skip 4/5 non-target scenarios." If scores are poor, flag it: "The description might need work — I'd recommend running the full Description Optimization after we're done iterating."

This is lighter than the full Description Optimization (which uses 20 queries, train/test splits, and automated loops). Think of it as a smoke test for trigger quality.

### Step 5: Read the feedback

When the user tells you they're done, read `feedback.json`. Empty feedback means the user thought it was fine. Focus improvements on test cases with specific complaints.

Kill the viewer server when done: `kill $VIEWER_PID 2>/dev/null`

---

## Improving the skill

This is the heart of the loop. You've run the test cases, the user has reviewed the results, and now you need to make the skill better.

### How to think about improvements

1. **Generalize from the feedback.** We're trying to create skills used across many prompts. Rather than fiddly overfitty changes, try different metaphors or patterns if something is stubborn.

2. **Keep the prompt lean.** Remove things that aren't pulling their weight. Read the transcripts, not just outputs — if the skill makes the model waste time on unproductive steps, cut those parts.

3. **Explain the why.** Explain the reasoning behind instructions. If you find yourself writing ALWAYS or NEVER in all caps, reframe and explain the reasoning instead — that's more powerful and effective.

4. **Look for repeated work.** If all test cases independently wrote similar helper scripts, bundle that script in `scripts/` and tell the skill to use it.

### The iteration loop

After improving the skill:

1. Apply improvements
2. Rerun all test cases into a new `iteration-<N+1>/` directory
3. Launch the reviewer with `--previous-workspace`
4. Wait for user review
5. Read feedback, improve again, repeat

Keep going until the user is happy, feedback is all empty, or you're not making meaningful progress.

---

## Structural Definition of Done (DoD)

Before marking a skill as "ready" or packaging it, run this structural checklist. These are format/metadata checks — separate from the quality evals that test whether the skill works well.

**Checklist:**
- [ ] Frontmatter has `name`, `description`, `intent` (all required)
- [ ] `name` <= 64 characters
- [ ] `description` <= 200 characters
- [ ] `description` says WHAT the skill does AND WHEN to use it
- [ ] `intent` explains the WHY and broader context
- [ ] If `effort` is declared (optional), value is one of: `low`, `medium`, `high`, `xhigh`, `max`
- [ ] SKILL.md under 500 lines
- [ ] No placeholder text remaining (`[CUSTOMIZE]`, `TODO`, `TBD`, `XXX`)
- [ ] Cross-references resolve (files referenced in SKILL.md actually exist)
- [ ] Section order follows convention (frontmatter -> overview -> instructions -> examples)
- [ ] **No time-sensitive info hardcoded** — grep for absolute month/year stamps ("April 2026", "as of Q2 2026", "current as of"), library version pins inside prose, and dated phrasing like "the latest model is X". These rot fast. Move them to a single `references/changelog.md` if you really need them, or replace with relative phrasing ("the most recent model family") so the skill ages well
- [ ] **Consistent terminology** — the skill uses the same word for the same concept throughout. If you call it "eval" in one place, don't switch to "test case" or "benchmark run" in another. Same for entity names ("user input" vs "prompt" vs "query"). Inconsistent vocabulary confuses the model and forces it to guess whether two terms mean the same thing
- [ ] **No deprecated model IDs anywhere in the skill** — grep `scripts/`, `references/`, `assets/`, and SKILL.md itself for retired/deprecated IDs: `claude-3-haiku-20240307` (retired 2026-04-20), `claude-sonnet-4-20250514` and `claude-opus-4-20250514` (retirement 2026-06-15). If found, replace with current IDs (`claude-haiku-4-5`, `claude-sonnet-4-6`, `claude-opus-4-7`) or use the alias (`haiku`, `sonnet`, `opus`)
- [ ] **No references to removed API patterns** — grep for `budget_tokens` (removed in Opus 4.7, replaced by `thinking: {type: "adaptive"}`), and for hardcoded `temperature`/`top_p`/`top_k` non-default values (return 400 in Opus 4.7)
- [ ] **`max_tokens` headroom** — if scripts hardcode `max_tokens=N` and target Opus 4.7+, N should be ~35% above the actual expected size to accommodate the new tokenizer

How to run these grep checks fast:
```bash
SKILL_DIR="path/to/skill"
grep -rn -E "claude-3-haiku-20240307|claude-sonnet-4-20250514|claude-opus-4-20250514|budget_tokens|temperature\s*=\s*[0-9]" "$SKILL_DIR" 2>/dev/null
```
If output is empty, all model-version checks pass.

**When it runs:**
- After each iteration: as warnings (visible but non-blocking)
- Before packaging: failures BLOCK packaging until fixed
- On demand: user can ask to run the checklist anytime

If a check fails during iteration, mention it: "Heads up — the description is 215 characters, over the 200-char limit. I'll trim it in the next revision." Before packaging, all checks must pass.

---

## Advanced: Blind comparison

For situations where you want a more rigorous comparison between two versions (e.g., "is the new version actually better?"), there's a blind comparison system. Read `agents/comparator.md` and `agents/analyzer.md` for details. Optional, requires subagents.

---

## Description Optimization

The `description` field is the primary mechanism that determines whether Claude invokes a skill. After creating or improving a skill, offer to optimize the description for better triggering accuracy. Note: this optimizes `description` only — `intent` does not affect triggering.

### Step 1: Generate trigger eval queries

Create 20 eval queries — a mix of should-trigger and should-not-trigger. Save as JSON:

```json
[
  {"query": "the user prompt", "should_trigger": true},
  {"query": "another prompt", "should_trigger": false}
]
```

Queries must be realistic — something a real Claude Code or Claude.ai user would actually type. Concrete and specific, with detail: file paths, personal context about the user's job or situation, column names and values, company names, URLs, a little backstory. Some might be lowercase or contain abbreviations, typos, or casual speech. Use a mix of lengths.

Bad: `"Format this data"`, `"Extract text from PDF"`, `"Create a chart"`

Good: `"ok so my boss just sent me this xlsx file (its in my downloads, called something like 'Q4 sales final FINAL v2.xlsx') and she wants me to add a column that shows the profit margin as a percentage. The revenue is in column C and costs are in column D i think"`

For the **should-trigger** queries (8-10), vary phrasing — some formal, some casual. Include cases where the user doesn't explicitly name the skill or file type but clearly needs it. Throw in uncommon use cases and cases where this skill competes with another but should win.

For the **should-not-trigger** queries (8-10), prioritize near-misses — queries that share keywords or concepts with the skill but actually need something different. Don't make them obviously irrelevant ("write a fibonacci function" as a negative test for a PDF skill is useless — it doesn't test anything). The negative cases should be genuinely tricky.

**Difference from Trigger-Readiness Audit:** The audit (Step 4.5) is a quick 10-prompt smoke test during iteration. Description Optimization is the full rigorous process — 20 queries, train/test split, automated optimization loop. Run the audit during iteration; run Description Optimization when the skill is otherwise done.

### Step 2: Review with user

Present the eval set using the HTML template from `assets/eval_review.html`. Replace `__EVAL_DATA_PLACEHOLDER__`, `__SKILL_NAME_PLACEHOLDER__`, and `__SKILL_DESCRIPTION_PLACEHOLDER__`. Write to temp file and open. User edits and exports to `~/Downloads/eval_set.json`.

### Step 3: Run the optimization loop

Tell the user: "This will take some time — I'll run the optimization loop in the background and check on it periodically."

```bash
python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --model <model-id-powering-this-session> \
  --max-iterations 5 \
  --verbose
```

Use the model ID that powers the current session so the triggering test matches what the user actually experiences. Current model IDs (Apr 2026): `claude-opus-4-7`, `claude-sonnet-4-6`, `claude-haiku-4-5`. In Claude Code you can also use the aliases `opus`, `sonnet`, `haiku`, or 1M-context variants `opus[1m]` and `sonnet[1m]`.

While it runs, periodically tail the output to give the user updates on which iteration it's on and what the scores look like.

This splits 60% train / 40% held-out test, evaluates the current description (3x per query for reliable trigger rate), proposes improvements, re-evaluates, iterating up to 5 times. Selects best by test score to avoid overfitting.

### How skill triggering works

Skills appear in Claude's `available_skills` list with name + description. Claude only consults skills for tasks it can't easily handle on its own — simple queries won't trigger skills regardless of description quality. Eval queries should be substantive enough that Claude would benefit from consulting a skill.

### Step 4: Apply the result

Take `best_description` from the JSON output and update the skill's frontmatter. Show before/after and report scores.

---

### Package and Present (only if `present_files` tool is available)

Check for `present_files` tool. If available:

```bash
python -m scripts.package_skill <path/to/skill-folder>
```

Before packaging, run the Structural DoD checklist. All checks must pass — fix any failures before packaging. After packaging, direct the user to the `.skill` file.

---

## Claude.ai-specific instructions

Core workflow is the same, but without subagents some mechanics change:

- **Running test cases**: No parallel execution. Read the skill's SKILL.md, then follow its instructions yourself for each test case. Skip baseline runs.
- **Reviewing results**: If no browser, present results directly in conversation. Ask for feedback inline.
- **Benchmarking**: Skip quantitative benchmarking. Focus on qualitative feedback.
- **Iteration loop**: Same, just without browser reviewer.
- **Description optimization**: Requires `claude -p` (Claude Code only). Skip on Claude.ai.
- **Blind comparison**: Requires subagents. Skip.
- **Packaging**: Works anywhere with Python and filesystem.
- **Updating existing skill**: Preserve the original name. Copy to `/tmp/skill-name/` before editing (installed path may be read-only).

---

## Cowork-Specific Instructions

- Subagents work, so the full workflow applies. (If timeouts occur, run tests in series.)
- No browser — use `--static <output_path>` for the viewer. Proffer a link for the user.
- GENERATE THE EVAL VIEWER *BEFORE* evaluating inputs yourself. Get results in front of the human ASAP!
- Feedback: "Submit All Reviews" downloads `feedback.json` as a file.
- Description optimization works (uses `claude -p` via subprocess).
- **Updating existing skill**: Follow the Claude.ai update guidance above.

---

## Reference files

The agents/ directory contains instructions for specialized subagents:
- `agents/grader.md` — How to evaluate assertions against outputs
- `agents/comparator.md` — How to do blind A/B comparison
- `agents/analyzer.md` — How to analyze why one version beat another

The references/ directory:
- `references/schemas.md` — JSON structures for evals.json, grading.json, benchmark.json, etc.

---

Core loop summary:

- **Preflight** — check for existing similar skills
- **Detect path** — wizard, content-first, or manual improvement
- Figure out what the skill is about (via interview, material analysis, or existing skill review)
- Draft or edit the skill (with `description` + `intent` in frontmatter)
- Run claude-with-access-to-the-skill on test prompts
- Evaluate outputs:
  - Create benchmark.json and run `eval-viewer/generate_review.py`
  - Run quantitative evals
  - **Trigger-readiness audit** — quick check that the description triggers correctly
- **Structural DoD check** — verify metadata, limits, and references
- Repeat until satisfied
- **Description Optimization** — full rigorous trigger optimization
- Package the final skill

Please add steps to your TodoList to make sure you don't forget. If you're in Cowork, specifically put "Create evals JSON and run `eval-viewer/generate_review.py` so human can review test cases" in your TodoList.

Good luck!
