# Plugin Structure Reference

## Table of Contents
1. [Directory Layout](#directory-layout)
2. [Plugin Manifest (plugin.json)](#plugin-manifest)
3. [Marketplace Manifest (marketplace.json)](#marketplace-manifest)
4. [Environment Variables](#environment-variables)
5. [Component Paths](#component-paths)

---

## Directory Layout

Every plugin follows this structure. Components at root — manifests inside `.claude-plugin/`.

```
plugin-name/
├── .claude-plugin/              # ONLY manifests go here
│   ├── plugin.json              # Required: plugin metadata
│   └── marketplace.json         # Optional: dev/distribution
├── skills/                      # Agent Skills
│   └── skill-name/
│       ├── SKILL.md             # Required per skill
│       ├── scripts/             # Executable helpers
│       ├── references/          # Docs loaded on demand
│       └── assets/              # Templates, configs
├── commands/                    # Slash commands
│   ├── command-name.md          # /command-name
│   └── namespace/               # Subcommands via folders
│       ├── sub1.md              # /namespace:sub1
│       └── sub2.md              # /namespace:sub2
├── agents/                      # Sub-agents
│   └── agent-name.md
├── hooks/                       # Event handlers
│   ├── hooks.json               # Hook configuration (auto-discovered)
│   ├── run-hook.cmd             # Cross-platform wrapper (polyglot)
│   └── scripts/
│       └── validate.sh
├── .mcp.json                    # MCP server configuration
├── CONNECTORS.md                # Optional: for tool-agnostic plugins (~~)
├── LICENSE
└── README.md
```

### Critical Rule: `.claude-plugin/` is manifest-only

```
WRONG:                          CORRECT:
.claude-plugin/                 .claude-plugin/
├── plugin.json                 └── plugin.json
├── skills/          # NO!
└── commands/        # NO!      skills/          # At ROOT
                                commands/        # At ROOT
```

---

## Plugin Manifest

### Minimal (required)

```json
{
  "name": "my-plugin",
  "version": "0.1.0",
  "description": "What the plugin does",
  "author": {
    "name": "Your Name"
  }
}
```

### Full spec

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Full description of the plugin",
  "author": {
    "name": "Your Name",
    "email": "you@email.com",
    "url": "https://github.com/you"
  },
  "homepage": "https://github.com/you/my-plugin",
  "repository": "https://github.com/you/my-plugin",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "mcpServers": {
    "server-name": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/server/index.js"],
      "env": { "API_KEY": "${PLUGIN_ENV_API_KEY}" }
    }
  }
}
```

### Supported fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Kebab-case, no spaces or special chars |
| `version` | Yes | Semver (start at `0.1.0`) |
| `description` | Yes | What the plugin does |
| `author` | Yes | Object with `name`, optional `email`/`url` |
| `homepage` | No | Plugin homepage URL |
| `repository` | No | Source code URL |
| `license` | No | License identifier (e.g., "MIT") |
| `keywords` | No | Array of search keywords |
| `commands` | No | Custom path to commands dir |
| `agents` | No | Custom path(s) to agents |
| `skills` | No | Custom path to skills dir |
| `hooks` | No | Custom path to hooks.json |
| `mcpServers` | No | MCP server configurations |
| `outputStyles` | No | Path to output styles directory |
| `lspServers` | No | LSP server configurations |

### Custom component paths (optional)

```json
{
  "name": "my-plugin",
  "commands": "./custom-commands",
  "agents": ["./agents", "./specialized-agents"],
  "hooks": "./config/hooks.json",
  "mcpServers": "./.mcp.json"
}
```

---

## Marketplace Manifest

### For local development

Place `marketplace.json` inside `.claude-plugin/`:

```json
{
  "name": "my-dev",
  "description": "Dev marketplace",
  "owner": { "name": "Your Name" },
  "plugins": [
    {
      "name": "my-plugin",
      "description": "What it does",
      "version": "0.1.0",
      "source": "./",
      "author": { "name": "Your Name" }
    }
  ]
}
```

### For distribution via URL

```json
{
  "name": "my-marketplace",
  "owner": { "name": "Your Name" },
  "plugins": [
    {
      "name": "my-plugin",
      "source": { "source": "url", "url": "https://github.com/org/plugin.git" },
      "version": "1.2.1",
      "description": "Description"
    }
  ]
}
```

### Source types

| Type | Use case | Example |
|------|----------|---------|
| `"./"` | Local development | `"source": "./"` |
| `"url"` | GitHub/remote repo | `"source": { "source": "url", "url": "https://..." }` |
| `"git-subdir"` | Monorepo subdirectory | Sparse clone of specific dir |
| `"npm"` | npm registry | Public or private npm packages |

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `${CLAUDE_PLUGIN_ROOT}` | Current install directory (changes between versions) |
| `${CLAUDE_PLUGIN_DATA}` | Persistent data directory (`~/.claude/plugins/data/{id}/`) |
| `${CLAUDE_SKILL_DIR}` | Directory of the currently executing skill |
| `${CLAUDE_SESSION_ID}` | Current session ID |
| `CLAUDE_CODE_PLUGIN_SEED_DIR` | Pre-populate plugins in containers/CI without runtime clone |
| `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS` | Git operation timeout (default 120s) |

**Key distinction**: `CLAUDE_PLUGIN_ROOT` changes on update. `CLAUDE_PLUGIN_DATA` persists across versions — use it for data that must survive updates.

---

## Component Paths

By default, Claude auto-discovers components in conventional directories. Override with explicit paths in `plugin.json` only when needed.

**Auto-discovered locations:**
- `skills/` — subdirectories with `SKILL.md`
- `commands/` — `.md` files
- `agents/` — `.md` files
- `hooks/hooks.json` — hook configuration
- `.mcp.json` — MCP server config

**Path rules:**
- Always use `${CLAUDE_PLUGIN_ROOT}` prefix in configs
- Relative paths in plugin.json start with `./`
- Never hardcode absolute paths (`/Users/...`, `C:\...`)
