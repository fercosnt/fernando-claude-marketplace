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

## Thresholds

| Range | Label | Action |
|-------|-------|--------|
| 0-15 | Cold | Nurturing sequence |
| 16-35 | Warm | Follow-up in 24-48h |
| 36-50 | Hot | Prioritize handoff |
| 51+ | Qualified | Immediate handoff |

## Routing via Conversation AI

Use the **AI Decision Maker** or **AI Router Node** in Agent Studio for score-based routing.

- Accepts natural language instructions instead of If/Else trees.
- Example instruction: `"Route to High-Priority branch if lead score is over 80 and they are in Real Estate industry"`
- Evaluates in real-time during conversation, combined with CRM context.

## Known Gaps

- No documented UI walkthrough for configuring Predictive Lead Scoring rules.
- Exact weights per action in the native algorithm are not published.
- Integration path between native scoring output and Conversation AI bot decisions is partially undocumented -- custom field approach is more reliable for SDR bots.
