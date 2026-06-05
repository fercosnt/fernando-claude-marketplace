# GHL Lead Scoring Reference

**When to load:** User mentions lead scoring, qualification scores, lead prioritization, or routing by engagement level.

## CRM Variable

Native lead score field accessible via `{{contact.lead_score}}`. Usable in prompts, workflows, and automations.

## Two Approaches

### 1. Native Predictive Lead Scoring

- GHL's built-in "Intelligent Lead Scoring" uses predictive AI on historical campaign data and behavioral signals.
- Automatic segmentation by engagement score.
- **Gap:** Exact UI configuration screens and weight definitions are undocumented. Native scoring integration with Conversation AI is not fully documented.

### 2. Custom Field Scoring (Recommended for SDR Bots)

When native scoring lacks granularity, use custom fields updated by workflow actions.

**Custom fields to create:**
- `qualification_score` (number)
- `qualification_status` (text: Cold / Warm / Hot / Qualified)

**GHL-MCP tools:**
- `ghl_create_custom_field` -- create the fields
- `ghl_get_custom_fields_by_object_key` -- verify existing fields

## Scoring Rules

### Add Points

| Action | Points |
|--------|--------|
| Responded to first message | +5 |
| Provided name | +5 |
| Described need/problem | +10 |
| Has urgency or time-bound event | +15 |
| Is the decision maker | +10 |
| Already researched prices | +5 |
| Asked to schedule | +20 |

### Subtract Points

| Action | Points |
|--------|--------|
| No response after 24h | -10 |
| Said "just researching" | -5 |
| Location outside service area | -15 |
| Asked to stop messages | -30 |

## Thresholds (action-based, granular)

| Range | Label | Action |
|-------|-------|--------|
| 0-15 | Cold | Nurturing sequence |
| 16-35 | Warm | Follow-up in 24-48h |
| 36-50 | Hot | Prioritize handoff |
| 51+ | Qualified | Immediate handoff |

The table above scores **micro-actions** (replied, gave name, asked to schedule). Use it when you want fine-grained behavioral scoring inside the bot.

## BANT Scoring (N→A→T→B) — recommended for SDR qualification

For qualification decisions, score the **four BANT dimensions** on a 0–100 scale. Each dimension is worth **25 points**:

| Dimension | Strong (25) | Medium (10–15) | Absent (0) |
|-----------|-------------|----------------|------------|
| **Need** | Confirmed pain + consequence | Vague interest | No problem stated |
| **Authority** | Decision maker | Influencer | Unknown |
| **Timeline** | Event/deadline | "Sometime" | None |
| **Budget** | Fits the anchored range | "Need to check" | Below range / refuses |

### BANT thresholds

| Score | Label | Routing |
|-------|-------|---------|
| **≥ 75** | Hot | Pass to AE / human handoff now |
| **50–74** | Warm | Nurture, re-qualify in 7–14 days |
| **< 50** | Cold | Long nurturing, 30–90 days |

### Booking evidence (why capture all 4)

| Dimensions captured | Booking rate |
|---------------------|--------------|
| 4 / 4 | **29%** |
| 3 / 4 | 14% |
| ≤ 2 / 4 | < 5% |

**One automated follow-up doubles bookings (+106%)** — always configure at least one. See `qualification-patterns.md` §1 for the 8-question flow (budget anchored, asked last).

### Which model to use
- **BANT 0–100** → the qualification verdict (Hot/Warm/Cold → handoff decision). Maps to `qualification_status`.
- **Action-based table** → optional behavioral layer for prioritization within a stage. Maps to `qualification_score`.
- They are not mutually exclusive — BANT decides handoff; the action table fine-tunes priority.

## Routing via Conversation AI

Use the **AI Decision Maker** or **AI Router Node** in Agent Studio for score-based routing.

- Accepts natural language instructions instead of If/Else trees.
- Example instruction: `"Route to High-Priority branch if lead score is over 80 and they are in Real Estate industry"`
- Evaluates in real-time during conversation, combined with CRM context.

## Known Gaps

- No documented UI walkthrough for configuring Predictive Lead Scoring rules.
- Exact weights per action in the native algorithm are not published.
- Integration path between native scoring output and Conversation AI bot decisions is partially undocumented -- custom field approach is more reliable for SDR bots.
