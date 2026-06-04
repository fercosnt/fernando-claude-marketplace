# Plugin Components Reference

## Table of Contents
1. [Skills](#skills)
2. [Commands](#commands)
3. [Agents](#agents)
4. [Hooks](#hooks)
5. [MCP Servers](#mcp-servers)

---

## Skills

Skills are the primary extension mechanism. Claude invokes them automatically when conversation context matches the description.

### Format

```markdown
---
name: my-skill
description: Use when [trigger conditions]. Covers [what it does]. Also activate for "phrase 1", "phrase 2", "phrase 3".
---

# Skill Title

Overview in 1-2 sentences.

## Workflow
1. Step one
2. Step two

## Output Format
Template of expected output.

## What NOT to Do
- Anti-pattern 1
- Anti-pattern 2
```

### Frontmatter fields

| Field | Required | Notes |
|-------|----------|-------|
| `name` | Yes | Kebab-case identifier |
| `description` | Yes | Trigger mechanism — "Use when..." format |

**Important**: `name` and `description` são os únicos campos OBRIGATÓRIOS. Os campos abaixo (v2.0.10+ e Opus 4.7+) são opcionais e suportados. Campos inventados/fora desta lista podem quebrar discovery silenciosamente.

### Optional frontmatter fields (v2.0.10+ / Opus 4.7+)

Use apenas quando justificado:

| Field | Type | Description |
|-------|------|-------------|
| `intent` | String | Explicação mais longa do propósito da skill — não afeta discovery, ajuda o modelo a entender o "porquê" quando a skill carrega (Opus 4.7+) |
| `effort` | String | `low`, `medium`, `high`, `xhigh`, `max` — `xhigh` é default no Claude Code (Pro/Max) desde Opus 4.7. Use apenas para forçar effort diferente do da sessão |
| `context` | String | `fork` to run in isolation from history |
| `agent` | String | Custom agent as executor |
| `hooks` | Object | Hooks scoped to skill lifecycle |
| `disable-model-invocation` | Bool | Prevent automatic activation by model |
| `user-invocable` | Bool | `false` = hidden from `/` menu but model can activate |
| `allowed-tools` | String/Array | Restrict tools during execution |

### Progressive disclosure (3 levels)

| Level | Content | When loaded | Limit |
|-------|---------|-------------|-------|
| 1 - Metadata | name + description | Always in context | ~100 words |
| 2 - Body | SKILL.md content | When triggered | < 500 lines |
| 3 - Resources | references/, scripts/, assets/ | On demand | Unlimited |

### Writing rules

- **Third person** in description: "Processes Excel files..." not "I can help you..."
- **Imperative** in body: "Parse the file" not "You should parse the file"
- **"Pushy" descriptions**: Claude tends to undertrigger — be explicit about ALL scenarios
- **Trigger phrases in quotes**: `"design an API"`, `"create API endpoints"`
- **List aliases**: users say the same thing many different ways — capture all of them
- **Max 1024 chars** in description field
- **No "anthropic" or "claude"** in skill name

### Description quality ladder

```yaml
# BAD:
description: A helpful skill

# GOOD:
description: Use when debugging test failures - systematic approach to finding root causes

# EXCELLENT:
description: >
  Use when working on Claude Code plugins (creating, modifying, testing,
  releasing, or maintaining) - provides streamlined workflows, patterns,
  and examples for the complete plugin lifecycle
```

### Budget limit

Skills compete for context space. Budget = 2% of context window (fallback 16K chars). Too many skills → some get silently excluded. Controlled by `SLASH_COMMAND_TOOL_CHAR_BUDGET`.

### Resources structure

```
skills/my-skill/
├── SKILL.md              # Core (< 500 lines)
├── scripts/              # Executables (via Bash tool)
│   └── validate.py
├── references/           # Docs (loaded on demand)
│   ├── api-docs.md       # "See references/api-docs.md for..."
│   └── examples.md
└── assets/               # Templates, configs
    └── template.json
```

Reference files 100+ lines should have a TOC at the top.

---

## Commands

Slash commands invoked manually by the user with `/command-name`.

### Format

```markdown
---
description: Generate meeting notes from transcript (<60 chars)
argument-hint: [transcript-file]
allowed-tools: Read, Write
---

Read the transcript at @$1 and generate structured meeting notes.

Include: Attendees, Summary, Key Decisions, Action Items, Open Questions.
Write to a new file with `-notes` appended.
```

### Frontmatter fields

| Field | Required | Description |
|-------|----------|-------------|
| `description` | No | Shown in `/help` (<60 chars) |
| `argument-hint` | No | Hint for arguments |
| `allowed-tools` | No | Restrict available tools |
| `model` | No | Override: `sonnet`, `opus`, `haiku`, `opus[1m]`, `sonnet[1m]`, `opusplan` (Opus 4.7+) |
| `disable-model-invocation` | No | Prevent model from auto-invoking |

### Special syntax

| Syntax | Function | Example |
|--------|----------|---------|
| `$ARGUMENTS` | All arguments as string | `/cmd arg1 arg2` → `"arg1 arg2"` |
| `$1`, `$2` | Positional arguments | `/cmd file.txt` → `$1 = "file.txt"` |
| `@path` | Include file content | `@$1` includes first arg's file |
| exclamation-mark prefix + backticked command | Execute bash for dynamic context | exclamation-mark prefix then "git diff --name-only" inside backticks |
| `${CLAUDE_PLUGIN_ROOT}` | Portable path to plugin files | Templates, scripts |

### Nesting (subcommands)

Folders create namespaces:

```
commands/
├── deploy.md              # /deploy
├── tasks/
│   ├── setup.md           # /tasks:setup
│   └── list.md            # /tasks:list
└── db/
    ├── reset.md           # /db:reset
    └── migrate.md         # /db:migrate
```

### Command-as-skill-wrapper pattern

Emerging pattern from superpowers plugin — command is just an entry point, logic lives in the skill:

```markdown
---
description: "You MUST use this before any creative work..."
disable-model-invocation: true
---
Invoke the my-plugin:brainstorming skill and follow it exactly
```

This cleanly separates entry point from logic.

### Key rule

> Commands are instructions FOR Claude, not documentation for the user. Write as directives.

---

## Agents

Sub-agents that receive delegated tasks. Uncommon in Cowork — use only for autonomous multi-step work.

### Format

```markdown
---
name: ticket-analyzer
description: Use this agent when the user needs to analyze tickets or triage issues.

<example>
Context: User preparing for sprint planning
user: "Help me triage these new tickets"
assistant: "I'll use the ticket-analyzer agent to review and categorize."
<commentary>Ticket triage requires systematic analysis.</commentary>
</example>

model: inherit
color: cyan
tools: ["Read", "Grep", "Glob"]
---

You are a ticket analysis specialist. Analyze tickets for priority, effort, and dependencies.

**Output Format:**
| Ticket | Type | Effort | Dependencies | Priority |
|--------|------|--------|-------------|----------|
```

### Frontmatter fields

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `name` | Yes | String | 3-50 chars, kebab-case |
| `description` | Yes | String | Trigger conditions + `<example>` blocks |
| `model` | Yes | String | `inherit`, `sonnet`, `opus`, `haiku`, `opus[1m]`, `sonnet[1m]` (Opus 4.7+) |
| `color` | Yes | String | Agent color in UI |
| `tools` | No | Array | Restrict available tools |

### Colors

| Color | Use |
|-------|-----|
| Blue/Cyan | Analysis, review |
| Green | Success tasks |
| Yellow | Caution, validation |
| Red | Critical, security |
| Magenta | Creative, generation |

---

## Hooks

Event-driven automation — scripts that execute in response to system events.

### Events

| Event | When it fires | Notes |
|-------|--------------|-------|
| `PreToolUse` | Before executing a tool | Can block OR modify input (v2.0.10+) |
| `PostToolUse` | After executing a tool | Good for auto-formatting |
| `Stop` | When Claude finishes a response | Exit 2 = conditional continuation |
| `SubagentStop` | When sub-agent finishes | |
| `SessionStart` | Session start | Subtypes: `startup`, `resume`, `clear`, `compact` |
| `SessionEnd` | Session end | |
| `UserPromptSubmit` | When user sends message | |
| `PreCompact` | Before compacting context | |
| `Notification` | When notification is sent | |
| `WorktreeCreate` | When git worktree created | New |
| `WorktreeRemove` | When git worktree removed | New |
| `InstructionsLoaded` | When CLAUDE.md etc. loaded | New |
| `ConfigChange` | When configuration changes | New |
| `PostCompact` | After compacting context | New |
| `Elicitation` | When elicitation sent | New |
| `TaskCompleted` | When task completes | New |

### Hook types

**Command-based** (deterministic checks):
```json
{
  "type": "command",
  "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/validate.sh",
  "timeout": 60
}
```

**Prompt-based** (complex logic):
```json
{
  "type": "prompt",
  "prompt": "Check that this file write follows project conventions: $TOOL_INPUT",
  "timeout": 30
}
```

### hooks.json format

```json
{
  "PreToolUse": [
    {
      "matcher": "Write|Edit",
      "hooks": [
        {
          "type": "command",
          "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/lint.sh",
          "timeout": 30
        }
      ]
    }
  ],
  "SessionStart": [
    {
      "matcher": "startup|resume",
      "hooks": [
        {
          "type": "command",
          "command": "cat ${CLAUDE_PLUGIN_ROOT}/context/project-context.md",
          "timeout": 10
        }
      ]
    }
  ]
}
```

### Matcher

Regex to filter when hook fires:
- `"Write|Edit"` — Write OR Edit
- `"Bash"` — only Bash
- `"startup|resume|clear|compact"` — multiple SessionStart subtypes
- `""` — any (no filter)

### Command hook output

```json
{
  "decision": "block",
  "reason": "File write violates naming convention"
}
```

Decisions: `approve`, `block`, `ask_user`.

### SessionStart with structured JSON

Inject context as system instruction:
```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "<EXTREMELY_IMPORTANT>Your context here</EXTREMELY_IMPORTANT>"
  }
}
```

### Cross-platform wrapper (`run-hook.cmd`)

Polyglot script that works on CMD (Windows) and bash (Unix):

```cmd
: << 'CMDBLOCK'
@echo off
REM Polyglot wrapper: runs .sh scripts cross-platform
"C:\Program Files\Git\bin\bash.exe" -l "%~dp0%~1"
exit /b
CMDBLOCK

# Unix shell runs from here
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SCRIPT_NAME="$1"
shift
"${SCRIPT_DIR}/${SCRIPT_NAME}" "$@"
```

**Requirements**: Windows needs Git for Windows. Unix needs bash + `chmod +x`.

### Critical rules

- `hooks/hooks.json` is auto-discovered — do NOT reference in plugin.json
- Scripts must be executable: `chmod +x hooks/run-hook.cmd hooks/scripts/*.sh`
- PreToolUse is the only hook that can block tool execution
- Matchers are case-sensitive

---

## MCP Servers

Connect to external tools and APIs via Model Context Protocol.

### Transport types

**stdio** (local process):
```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/servers/server.js"],
      "env": { "API_KEY": "${API_KEY}" }
    }
  }
}
```

**SSE** (remote, Server-Sent Events):
```json
{
  "mcpServers": {
    "asana": {
      "type": "sse",
      "url": "https://mcp.asana.com/sse"
    }
  }
}
```

**HTTP** (remote, REST):
```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": { "Authorization": "Bearer ${GITHUB_TOKEN}" }
    }
  }
}
```

### Config location

1. Check `plugin.json` for `mcpServers` field or custom path
2. If not found, use `.mcp.json` at plugin root (default)

### MCP categories

| Category | Keywords | Common servers |
|----------|----------|---------------|
| Project management | asana, jira, linear | Linear, Asana |
| Source control | github, gitlab | GitHub Copilot MCP |
| Chat | slack, teams, discord | Slack MCP |
| Documents | notion, confluence | Notion MCP |
| Design | figma, sketch | Figma MCP |
| Analytics | datadog, grafana | Datadog |
| CRM | salesforce, hubspot | Salesforce |
