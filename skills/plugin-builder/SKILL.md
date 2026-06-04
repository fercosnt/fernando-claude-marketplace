---
name: plugin-builder
description: Build plugins for Claude Code and Cowork. Use when creating plugins, scaffolding plugin structure, adding skills/commands/hooks/agents/MCP, distributing via marketplace, porting skills to plugin format, debugging plugin issues, or when user mentions "plugin", "criar plugin", "plugin Cowork", "marketplace".
---

# Plugin Builder

Build plugins for Claude Code and Cowork — from idea to distribution.

## When to Use

- Creating a new plugin from scratch
- Adding components to an existing plugin (skills, commands, hooks, agents, MCP)
- Porting standalone skills to plugin format
- Setting up marketplace for testing or distribution
- Debugging plugin issues (not loading, skill not triggering, hooks not firing)
- Planning plugin architecture (choosing components)

## Quick Reference

| Need to... | Read |
|-----------|------|
| Understand plugin structure and rules | `references/plugin-structure.md` |
| Write skills, commands, agents, hooks, MCP | `references/components.md` |
| Build for Cowork (non-devs, sandbox, connectors) | `references/cowork-guide.md` |
| Apply advanced patterns, avoid anti-patterns | `references/patterns.md` |
| Distribute via marketplace, npm, or GitHub | `references/distribution.md` |

## Core Concepts

A plugin is a **portable, self-contained package** (Markdown + JSON) that extends Claude. No compilation, no infrastructure, no build steps.

**Components:**

| Component | What it does | Who invokes |
|-----------|-------------|-------------|
| **Skills** | Domain knowledge loaded on-demand | Claude (automatically) |
| **Commands** | Slash commands for user actions | User (via `/command`) |
| **Agents** | Specialized sub-agents for delegation | Claude (automatically) |
| **Hooks** | Event-driven automation | System (automatically) |
| **MCP Servers** | External tool/API connections | Claude (via tools) |

**Insight**: MCP provides *capability* (tools). Skills provide *judgment* (when and how to use them). They are complementary.

## Workflow

### Phase 1: Plan

Before writing anything:

1. **Define purpose** — What problem does this solve? For whom?
2. **Choose target** — Claude Code devs? Cowork non-devs? Both?
3. **Pick pattern** — Use the decision table below

#### Pattern Decision Table

| Goal | Pattern | Components |
|------|---------|------------|
| Teach a process/workflow | Skill Only | skill |
| Add tools + guidance | MCP + Skill | skill + .mcp.json |
| Project shortcuts | Command Collection | commands |
| Automate conventions | Hooks | hooks |
| Full domain coverage | Full-Featured | all components |
| External distribution | Tool-Agnostic | any + CONNECTORS.md + `~~` |

**Rule of thumb**: Start minimal. Add components only when justified.
```
Skill only → + References → + Commands → + Hooks → + MCP → Full-Featured
```

3. **Review similar plugins** — Check `anthropics/knowledge-work-plugins` for patterns in your domain.

### Phase 2: Scaffold

Create the directory structure. Read `references/plugin-structure.md` for the full spec.

```bash
# Minimal structure
mkdir -p my-plugin/.claude-plugin
mkdir -p my-plugin/skills/my-skill

# Write plugin.json
cat > my-plugin/.claude-plugin/plugin.json << 'EOF'
{
  "name": "my-plugin",
  "version": "0.1.0",
  "description": "What the plugin does",
  "author": { "name": "Your Name" }
}
EOF

# Dev marketplace for local testing
cat > my-plugin/.claude-plugin/marketplace.json << 'EOF'
{
  "name": "my-dev",
  "plugins": [{ "name": "my-plugin", "source": "./" }]
}
EOF
```

### Phase 3: Build Components

For each component type, read `references/components.md` for the full spec. Key rules:

**Skills** (`skills/name/SKILL.md`):
- Frontmatter: `name` + `description` only (extras can break discovery)
- Description: third person, "Use when..." format, list trigger phrases
- Body < 500 lines — move details to `references/`
- Combat undertriggering: be explicit about ALL activation scenarios

**Commands** (`commands/name.md`):
- Commands are instructions FOR Claude, not docs for the user
- Frontmatter: `description` (<60 chars), optional `argument-hint`, `allowed-tools`
- Special syntax: `$ARGUMENTS`, `$1`, `@path`, bash interpolation with `!` + backticked command

**Hooks** (`hooks/hooks.json`):
- Auto-discovered — do NOT reference in plugin.json (causes "Duplicate hooks" error)
- Use `${CLAUDE_PLUGIN_ROOT}` for all paths
- Scripts must be executable (`chmod +x`)

**MCP** (`.mcp.json` or in `plugin.json`):
- Types: stdio (local), SSE (remote), HTTP (remote)
- Use `${ENV_VAR}` for credentials, never hardcode

**Agents** (`agents/name.md`):
- Uncommon in Cowork — use only when multi-step delegation is needed
- Must have `<example>` blocks in description, `model` and `color` fields

### Phase 4: Test Locally

```bash
# Add dev marketplace
/plugin marketplace add /path/to/my-plugin

# Install
/plugin install my-plugin@my-dev

# RESTART Claude Code (mandatory after install)

# Quick test with --plugin-dir (no install needed)
claude --plugin-dir ./my-plugin

# Hot-reload without restart
/reload-plugins
```

**Test each component:**
- Skills: send prompts matching the description triggers
- Commands: run `/command-name`
- Hooks: trigger the relevant events
- MCP: verify tools appear in tool list

### Phase 5: Debug

Common issues and fixes:

| Problem | Cause | Fix |
|---------|-------|-----|
| Plugin won't load | Invalid plugin.json | `jq . .claude-plugin/plugin.json` |
| Skill doesn't trigger | Vague description | Add specific trigger phrases |
| Command missing | Inside `.claude-plugin/` | Move to `commands/` at root |
| Hook doesn't fire | Script not executable | `chmod +x hooks/*.sh` |
| MCP won't start | Hardcoded path | Use `${CLAUDE_PLUGIN_ROOT}` |
| Changes don't show | Didn't restart | Restart or `/reload-plugins` |
| "Duplicate hooks" | hooks.json in plugin.json | Remove the reference |

**Debug workflow:**
```bash
# 1. Validate all JSONs
jq . .claude-plugin/plugin.json
jq . hooks/hooks.json

# 2. Check hardcoded paths
grep -r "/Users/" .

# 3. Check permissions
find . -name "*.sh" -o -name "*.cmd" | xargs ls -la

# 4. Validate plugin
claude plugin validate .claude-plugin/plugin.json

# 5. Clean reinstall
/plugin uninstall my-plugin@my-dev
/plugin install my-plugin@my-dev
# Restart Claude Code

# 6. Debug mode
claude --debug
```

### Phase 6: Distribute

Read `references/distribution.md` for the full distribution guide.

**Quick options:**
- **GitHub direct**: `/plugin marketplace add org/repo`
- **Official marketplace**: Submit at `platform.claude.com/plugins/submit`
- **npm**: Publish to public/private registry
- **Team/private**: `extraKnownMarketplaces` in team settings.json

## Inviolable Rules

These are non-negotiable. Violating them causes hard-to-debug failures.

1. **`.claude-plugin/` contains ONLY manifests** — never put skills, commands, or code inside it
2. **Use `${CLAUDE_PLUGIN_ROOT}` for ALL internal paths** — never hardcode absolute paths
3. **`hooks/hooks.json` is auto-discovered** — referencing it in `plugin.json` causes duplicate error
4. **Kebab-case everywhere** — directories, files, plugin names, skill names
5. **Scripts must be executable** — `chmod +x` on all `.sh`, `.cmd`, and server files
6. **Skill frontmatter: fique nos campos documentados** — `name` e `description` são obrigatórios; `intent`, `effort` e demais campos v2.0.10+ (`context`, `agent`, `hooks`, `disable-model-invocation`, `user-invocable`, `allowed-tools`) são opcionais mas suportados. Campos inventados fora desta lista quebram discovery silenciosamente. Ver `references/components.md §Skills`.

## Cowork vs Claude Code

Both share the same plugin system. The difference is the audience.

| Aspect | Claude Code | Cowork |
|--------|-------------|--------|
| Users | Developers | Knowledge workers |
| Interface | Terminal/CLI | Desktop GUI |
| Security | Runs on local machine | VM sandbox (bwrap) |
| Best for | Elaborate plugins, distribution | Quick MVPs, simple workflows |
| Iteration | Fast (edit → test) | Slower (reinstall → restart) |

**Cowork-specific concerns:**
- Sandbox blocks: private APIs, Docker, git credentials
- No build steps — users can't run `npm install`
- Use simple language — never expose implementation details
- Read `references/cowork-guide.md` for the full guide

**Hybrid workflow (recommended):**
1. **Prototype** in Cowork (Plugin Create → quick MVP)
2. **Refine** in Claude Code (iterate each SKILL.md, add references, configure MCP)
3. **Distribute** (validate → package → publish)

## Validation Checklist

Run before considering a plugin ready:

### Structure
- [ ] `.claude-plugin/plugin.json` exists and is valid JSON
- [ ] `.claude-plugin/` contains ONLY manifests
- [ ] Skills in `skills/` at root, commands in `commands/` at root

### Paths
- [ ] Zero hardcoded paths — all use `${CLAUDE_PLUGIN_ROOT}`
- [ ] Paths in configs use `./` prefix or env variable

### Permissions
- [ ] All `.sh` and `.cmd` scripts are executable
- [ ] MCP server scripts are executable

### Skills
- [ ] Each has `SKILL.md` with valid YAML frontmatter
- [ ] `name` and `description` present; campos extras (se houver) estão na lista documentada (`intent`, `effort`, `context`, `agent`, `hooks`, `disable-model-invocation`, `user-invocable`, `allowed-tools`)
- [ ] Description uses "Use when..." format with trigger phrases
- [ ] Body < 500 lines (details in `references/`)

### Hooks
- [ ] `hooks.json` NOT referenced in `plugin.json`
- [ ] Matchers are valid regex
- [ ] Referenced scripts exist and are executable

### Distribution
- [ ] README.md with overview, components, setup, usage
- [ ] Semantic version in plugin.json
- [ ] Tested after clean reinstall + restart
