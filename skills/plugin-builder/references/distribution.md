# Plugin Distribution Reference

## Table of Contents
1. [Versioning](#versioning)
2. [Distribution Options](#distribution-options)
3. [Marketplace Configuration](#marketplace-configuration)
4. [Packaging for Cowork](#packaging-for-cowork)
5. [Plugin Commands Reference](#plugin-commands)
6. [CI/CD](#cicd)
7. [Ecosystem Resources](#ecosystem-resources)

---

## Versioning

Use semantic versioning in `plugin.json`:

```json
{ "version": "1.2.1" }
```

Release workflow:
```bash
# Update version in plugin.json
# Commit and tag
git add .
git commit -m "Release v1.2.1: brief description"
git tag v1.2.1
git push origin main
git push origin v1.2.1
```

---

## Distribution Options

| Method | How | Best for |
|--------|-----|----------|
| GitHub direct | `/plugin marketplace add org/repo` | Open source, simple |
| Official marketplace | Submit at `platform.claude.com/plugins/submit` | Wide discovery |
| npm packages | Public or private registry | Package ecosystem |
| Team/private | `extraKnownMarketplaces` in settings.json | Enterprise teams |
| Local file | `/plugin marketplace add /path/to/plugin` | Development, testing |

### A) GitHub direct

Users add your repo as marketplace:
```bash
/plugin marketplace add org/my-plugin-repo
/plugin install my-plugin@org-my-plugin-repo
```

### B) Official Anthropic marketplace

Submit at `platform.claude.com/plugins/submit`. Once approved, available via `/plugin` > Discover.

### C) npm package

Works with public and private npm registries. Source type `"npm"` in marketplace.json.

### D) Team/private marketplace

Configure in team settings.json:
```json
{
  "extraKnownMarketplaces": {
    "team-tools": {
      "source": { "source": "github", "repo": "org/plugins" }
    }
  }
}
```

### E) Private marketplace (Enterprise)

Since Feb 2026:
```json
{
  "strictKnownMarketplaces": {
    "internal": {
      "hostPattern": "github\\.mycompany\\.com",
      "pathPattern": "^/plugins/"
    }
  }
}
```

Admin can restrict to approved sources with `strict: false` for operator control.

---

## Marketplace Configuration

### Monorepo marketplace (multiple plugins)

```json
{
  "name": "my-company-plugins",
  "owner": { "name": "My Company" },
  "plugins": [
    {
      "name": "sales-toolkit",
      "source": "./sales-toolkit",
      "description": "Sales automation tools",
      "version": "1.0.0",
      "author": { "name": "My Company" }
    },
    {
      "name": "engineering-workflow",
      "source": "./engineering-workflow",
      "description": "Engineering workflow automation",
      "version": "0.5.0",
      "author": { "name": "My Company" }
    }
  ]
}
```

### Remote marketplace

```json
{
  "name": "my-marketplace",
  "owner": { "name": "Org" },
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

| Source type | Use case |
|------------|----------|
| `"./"` or `"./subdir"` | Local or monorepo |
| `{ "source": "url", "url": "https://..." }` | Remote git repo |
| `"git-subdir"` | Sparse clone of monorepo subdirectory |
| `"npm"` | npm public/private registry |

---

## Packaging for Cowork

For distribution as a `.plugin` file:

```bash
# Always create zip in /tmp/ first, then copy
cd /path/to/plugin && \
  zip -r /tmp/plugin-name.plugin . -x "*.DS_Store" && \
  cp /tmp/plugin-name.plugin /path/to/outputs/plugin-name.plugin
```

Before packaging, run validation:
```bash
claude plugin validate .claude-plugin/plugin.json
```

---

## Plugin Commands

### Management

```bash
# List installed plugins
/plugin list

# List marketplaces
/plugin marketplace list

# Add marketplace (local)
/plugin marketplace add /path/to/plugin

# Add marketplace (GitHub)
/plugin marketplace add org/repo-name

# Install plugin
/plugin install plugin-name@marketplace

# Uninstall plugin
/plugin uninstall plugin-name@marketplace

# Remove marketplace
/plugin marketplace remove /path

# Hot-reload without restart
/reload-plugins
```

### Development

```bash
# Test with local plugin (no install needed)
claude --plugin-dir ./my-plugin

# Validate plugin
claude plugin validate .claude-plugin/plugin.json

# Debug mode
claude --debug

# Full test cycle
/plugin uninstall plugin@market
# make edits
/plugin install plugin@market
# restart Claude Code
```

---

## CI/CD

### Pre-populating plugins in containers

Use `CLAUDE_CODE_PLUGIN_SEED_DIR` to pre-populate plugins without runtime git clone:

```bash
# In Dockerfile or CI setup
export CLAUDE_CODE_PLUGIN_SEED_DIR=/opt/claude-plugins
# Copy plugin files to seed directory
cp -r ./plugins/* $CLAUDE_CODE_PLUGIN_SEED_DIR/
```

### Git timeout

`CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS` — default 120s. Increase for slow networks or large repos.

---

## Ecosystem Resources

### Official Repositories

| Repo | Content |
|------|---------|
| `anthropics/knowledge-work-plugins` | 15+ official Cowork plugins (sales, HR, ops, etc.) |
| `anthropics/claude-plugins-official` | Official plugins (feature-dev, code-review, etc.) |
| `anthropics/skills` | Public skills from Anthropic |
| `anthropics/financial-services-plugins` | Financial services plugins (41 skills + MCP) |

### Community (Tier 1 — 10K+ stars)

| Repo | Stars | Pattern |
|------|-------|---------|
| everything-claude-code | 97K | Full harness (skills + instincts + hooks) |
| gstack (Garry Tan) | 37K | Org-chart as multi-agent |
| wshobson/agents | 32K | 72 plugins + 16 orchestrators + 79 tools |
| ruflo | 22K | Swarm orchestration + RAG + ADR + DDD |
| awesome-claude-code-subagents | 15K | 100+ standalone subagents |
| compound-engineering-plugin | 11K | Cross-tool converter + 29 agents |

### Community (Tier 2)

| Repo | Stars | Pattern |
|------|-------|---------|
| claude-code-hooks-mastery | 3.4K | Advanced hooks + meta-agents |
| open-claude-cowork | 3.2K | Open-source Cowork clone |
| CCPlugins | 2.7K | Anti-overengineering commands (V2 redesign) |

### Community Registries

| URL | Description |
|-----|-------------|
| claude-plugins.dev | Community registry with CLI |
| claudemarketplaces.com | Marketplace aggregator + learning hub |
| claudecodeplugins.io | Skills hub |

### Official Documentation

| Resource | URL |
|----------|-----|
| Plugins Reference | code.claude.com/docs/en/plugins-reference |
| Create Plugins | code.claude.com/docs/en/plugins |
| Skills Docs | code.claude.com/docs/en/skills |
| Skill Best Practices | platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| Plugin Marketplaces | code.claude.com/docs/en/plugin-marketplaces |
| Output Styles | code.claude.com/docs/en/output-styles |
| Cowork Plugin Tutorial | claude.com/resources/tutorials/how-to-build-a-plugin-from-scratch-in-cowork |
| Cowork Plugins Help | support.claude.com/en/articles/13837440 |

### Articles

| Title | URL |
|-------|-----|
| Skill authoring best practices | platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices |
| Claude Code Hooks — All 12 Events | pixelmojo.io/blogs/claude-code-hooks-production-quality-ci-cd-patterns |
| Turning Antipatterns into Skills | ihoka.me/blog/2026/03/06/turning-antipatterns-into-claude-skills.html |
| How to Build Claude Code Plugins | datacamp.com/tutorial/how-to-build-claude-code-plugins |
