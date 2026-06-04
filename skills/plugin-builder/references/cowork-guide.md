# Cowork Plugin Guide

Building plugins for non-developer audiences in Claude Desktop's Cowork mode.

## Table of Contents
1. [What is Cowork](#what-is-cowork)
2. [VM Sandbox Constraints](#vm-sandbox-constraints)
3. [What Works vs What Doesn't](#what-works-vs-what-doesnt)
4. [Connectors (Tool-Agnostic Plugins)](#connectors)
5. [Plugin Create (No-Code Path)](#plugin-create)
6. [Communication Rules](#communication-rules)
7. [Cowork vs Claude Code Development](#cowork-vs-claude-code)
8. [Porting Skills to Cowork](#porting-skills-to-cowork)
9. [Official Cowork Plugins](#official-cowork-plugins)

---

## What is Cowork

Cowork is a feature of Claude Desktop (GUI) that brings Claude Code's agentic architecture to a graphical interface — no terminal required.

- **Async execution**: Describe the outcome, leave, come back to finished work
- **VM sandboxed**: Runs in isolated virtual machine
- **Autonomous planning**: Analyzes request, creates plan, coordinates parallel workstreams
- **Available on**: Pro, Max, Team, Enterprise plans (macOS and Windows)

**Key insight**: Cowork IS Claude Code for non-developers. Same engine, different interface. Same plugin system.

---

## VM Sandbox Constraints

Cowork runs in a Linux VM via Apple VZVirtualMachine framework. This has implications:

### What the sandbox blocks
- Private/internal APIs (no network access to private services)
- Docker (cannot run containers)
- Git credentials (no access to local git config)
- Host filesystem (only mounted folders are accessible)

### What this means for plugins
- **No build steps** — users can't run `npm install`, `pip install`, etc.
- **No compiled dependencies** — everything must be Markdown + JSON + pre-built scripts
- **No private API calls** — use MCP servers with connector pattern instead
- **Folder permissions** — only folders selected before session start are read/write

### MCP in Cowork
MCP servers run with system-level access (stdio transport). This is the escape hatch for capabilities the sandbox blocks.

---

## What Works vs What Doesn't

| Works | Doesn't work / uncertain |
|-------|-------------------------|
| Skills (Markdown) | LSP servers (depend on host tools) |
| Commands | Complex shell script hooks |
| MCP servers (stdio and HTTP) | Private APIs without connector |
| Connectors (`~~`) | Docker, git credentials |
| Plugin Create (no-code generation) | Build steps (npm install, etc.) |

---

## Connectors

Connectors make plugins tool-agnostic — they work regardless of which specific tool the user's organization uses.

### When to use

> **NOT by default.** Only introduce `~~` placeholders when the plugin will be shared OUTSIDE the organization.

### How it works

In plugin files (commands, skills, agents), reference tools generically:

```markdown
Check ~~project tracker for open tickets assigned to the user.
Post a summary to ~~chat in the team channel.
```

### CONNECTORS.md

```markdown
# Connectors

## How tool references work
Plugin files use `~~category` as a placeholder for whatever tool the user
connects in that category. Plugins are tool-agnostic.

## Connectors for this plugin
| Category | Placeholder | Included servers | Other options |
|----------|-------------|-----------------|---------------|
| Chat | `~~chat` | Slack | Teams, Discord |
| Project tracker | `~~project tracker` | Linear | Asana, Jira, Monday |
| Source control | `~~source control` | GitHub | GitLab, Bitbucket |
```

### Communication rule

> **NEVER mention `~~` to the user.** Frame in terms of capabilities and tools. `~~` is an internal implementation detail.

### MCP Discovery (Cowork)

Cowork has built-in tools for finding and connecting MCP servers:

1. `search_mcp_registry` — search the MCP directory by keywords
2. `suggest_connectors` — show Connect buttons to the user

Workflow:
1. Identify what tool the plugin references
2. Ask user which tool they use (if unknown)
3. `search_mcp_registry` with category keywords
4. `suggest_connectors` for auth
5. Update `.mcp.json` with the registered URL

---

## Plugin Create

Built-in feature in Cowork that generates plugins from natural language descriptions. Claude interviews about the workflow and builds the plugin. **No technical knowledge required.**

### When to use Plugin Create
- Prototyping an idea quickly
- Testing if a plugin concept makes sense
- Non-technical users creating simple plugins
- Plugins with 1-2 commands and no complex skills

### When NOT to use Plugin Create
- Plugins with multiple skills needing individual refinement
- Plugins for distribution to team or externally
- When you need versioning and change history
- When porting existing skills to plugin format
- When precise MCP server configuration is needed

---

## Communication Rules

Cowork users are typically non-technical. Adjust accordingly:

### Do
- Use simple, clear language
- Frame in capabilities: "This plugin lets you..."
- Explain what the plugin does, not how it's built
- Use business terms, not technical jargon

### Don't
- Mention file paths, SKILL.md, YAML, frontmatter
- Expose `~~` placeholders, schemas, or internal structure
- Use "terminal", "CLI", "repository", "JSON"
- Assume familiarity with Markdown or config files

### Example

```
# BAD (too technical):
"The plugin has a skill in skills/meeting-prep/SKILL.md with a
description field that triggers on 'meeting preparation' queries."

# GOOD (capability-focused):
"This plugin helps you prepare for meetings. When you mention an
upcoming meeting, it automatically gathers relevant context and
creates a structured prep document."
```

---

## Cowork vs Claude Code

### Development comparison

| Aspect | Cowork Plugin Create | Claude Code |
|--------|---------------------|-------------|
| Interface | Guided conversation | Terminal with full control |
| Speed | Fast for MVP/prototype | Slower, more precise |
| Control | Black box — Claude decides structure | Granular control of every file |
| Iteration | Difficult (reinstall/restart cycle) | Easy (edit directly, test immediately) |
| Versioning | None | Full Git (branches, tags, history) |
| Validation | Basic (plugin validate) | Programmatic + manual + tests |
| Best for | Quick ideas, MVPs, non-devs | Elaborate plugins, distribution, teams |

### Recommended hybrid workflow

```
1. PROTOTYPE in Cowork
   └── Create basic plugin via Plugin Create
   └── Test concept and flow with real user
   └── Validate skills trigger and commands work

2. REFINE in Claude Code
   └── Clone/recreate structure with full control
   └── Iterate each SKILL.md individually
   └── Add references/ with detailed documentation
   └── Configure MCP servers correctly
   └── Version with Git

3. DISTRIBUTE
   └── Validate: claude plugin validate
   └── Package: zip as .plugin
   └── Publish: marketplace, GitHub, or npm
```

---

## Porting Skills to Cowork

If you have standalone skills (in `~/.claude/skills/` or installed plugins), you can port them to a Cowork plugin:

1. **Identify skills to port**: `ls ~/.claude/skills/`
2. **Create plugin structure**: `mkdir -p my-plugin/.claude-plugin my-plugin/skills/skill-name`
3. **Adapt SKILL.md**:
   - Add/update frontmatter (name, description with trigger phrases)
   - Ensure third-person "Use when..." format
   - Move lengthy content to `references/`
4. **Adapt language for Cowork**:
   - Remove terminal/CLI references
   - Simplify technical language
   - Focus on what the plugin DOES, not how
   - Replace CLI tools with MCP equivalents where possible
5. **Add commands as shortcuts**: Identify manual actions → create commands
6. **Package**: `cd my-plugin && zip -r /tmp/my-plugin.plugin . -x "*.DS_Store"`

---

## Official Cowork Plugins

### Anthropic Knowledge Work Plugins

Repository: `github.com/anthropics/knowledge-work-plugins`

15+ plugins, 85+ skills covering all business functions:

| Plugin | Skills | Focus |
|--------|--------|-------|
| sales | 6 | Outreach, call prep, competitive intel |
| marketing | 5 | Brand voice, content, campaigns, analytics |
| human-resources | 6 | Recruiting, handbook, org planning |
| product-management | 6 | Feature spec, roadmap, user research |
| operations | 6 | Process optimization, compliance, vendors |
| finance | 8 | Audit, close management, SOX compliance |
| legal | ~6 | Contracts, compliance, risk assessment |
| engineering | ~6 | Code review, architecture, incidents |
| data | ~5 | SQL, visualization, analysis |
| customer-support | 5 | Ticket triage, escalation, KB articles |
| productivity | ~5 | Calendar, email, tasks |
| cowork-plugin-management | 2 | Create plugins, customize plugins |

### Core+Addon pattern (from financial-services-plugins)

```
financial-analysis/      # Core (required)
├── .claude-plugin/
├── skills/ (41 skills)
├── commands/ (38 commands)
└── .mcp.json (11 integrations)

portfolio-analytics/     # Add-on (optional)
├── .claude-plugin/
├── skills/
└── commands/
```

### Patterns from official plugins

1. **Connectors section**: Table mapping `~~category` to tools
2. **Detailed execution flow**: Numbered steps with conditionals
3. **Embedded domain frameworks**: AIDA (sales), MoSCoW (product), INVEST (user stories), SOX (finance)
4. **Explicit anti-patterns**: "What NOT to Do" section
5. **Customization section**: `[CUSTOMIZE]` placeholders for company-specific values
6. **Success metrics**: Measurable targets per skill
