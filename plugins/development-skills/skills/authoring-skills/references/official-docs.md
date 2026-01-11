# Official Documentation Reference

Access to authoritative Claude Code documentation from docs.claude.com.

## Table of Contents

- [Quick Reference](#quick-reference)
- [Available Documentation](#available-documentation)
- [How to Use](#how-to-use)

---

## Quick Reference

| Topic | Documentation File |
|-------|-------------------|
| Create a plugin | `plugins.md` then `plugins-reference.md` |
| Set up MCP server | `mcp.md` |
| Configure hooks | `hooks.md` then `hooks-guide.md` |
| Write a skill | `skills.md` |
| CLI commands | `cli-reference.md` |
| Troubleshoot issues | `troubleshooting.md` |
| General setup | `setup.md` or `quickstart.md` |
| Configuration options | `settings.md` |

---

## Available Documentation

Documentation is available at docs.claude.com and can be fetched locally:

### Core
- `overview.md` - Claude Code introduction
- `quickstart.md` - Getting started guide
- `setup.md` - Installation and setup

### Extension
- `plugins.md` - Plugin development
- `plugins-reference.md` - Plugin API reference
- `plugin-marketplaces.md` - Plugin marketplaces
- `skills.md` - Skill creation
- `mcp.md` - MCP server integration

### Hooks & Events
- `hooks.md` - Hooks overview
- `hooks-guide.md` - Hooks implementation guide

### Configuration
- `settings.md` - Configuration reference
- `cli-reference.md` - CLI command reference
- `common-workflows.md` - Common usage patterns

### Modes & Features
- `interactive-mode.md` - Interactive mode guide
- `headless.md` - Headless mode guide
- `output-styles.md` - Output customization
- `statusline.md` - Status line configuration
- `memory.md` - Memory and context management
- `checkpointing.md` - Checkpointing feature
- `sub-agents.md` - Subagent usage

### Monitoring
- `analytics.md` - Usage analytics
- `costs.md` - Cost tracking
- `monitoring-usage.md` - Usage monitoring
- `data-usage.md` - Data usage policies

### Security & Enterprise
- `security.md` - Security features
- `iam.md` - IAM integration
- `network-config.md` - Network configuration

### Integrations
- `terminal-config.md` - Terminal configuration
- `vs-code.md` - VS Code integration
- `jetbrains.md` - JetBrains integration
- `devcontainer.md` - Dev container support

### CI/CD
- `github-actions.md` - GitHub Actions integration
- `gitlab-ci-cd.md` - GitLab CI/CD integration

### Model Configuration
- `model-config.md` - Model configuration
- `llm-gateway.md` - LLM gateway setup
- `amazon-bedrock.md` - AWS Bedrock integration
- `google-vertex-ai.md` - Google Vertex AI integration

### Maintenance
- `troubleshooting.md` - Troubleshooting guide
- `migration-guide.md` - Migration guide
- `legal-and-compliance.md` - Legal information
- `third-party-integrations.md` - Other integrations

---

## Updating Documentation

Use the included script to fetch latest docs from docs.claude.com:

```bash
node ~/.claude/skills/authoring-skills/scripts/update_docs.js
```

The script:
1. Fetches llms.txt from docs.claude.com
2. Extracts all Claude Code documentation URLs
3. Downloads each page to `references/`
4. Reports success/failures

**Run when:**
- Documentation seems outdated
- New Claude Code features are released
- Official docs have been updated

---

## How to Use

### For Specific Questions

1. Identify the relevant file from the list above
2. Fetch it: `node scripts/update_docs.js` (if not already local)
3. Read the documentation
4. Apply the solution

### For Broad Topics

Start with overview documents, then drill into specifics:

- **Extending Claude Code**: Start with `plugins.md`, `skills.md`, or `mcp.md`
- **Configuration**: Start with `settings.md` or `setup.md`
- **Integrations**: Check relevant integration file
- **Troubleshooting**: Start with `troubleshooting.md`

---

## Important Note

**Always consult official documentation before guessing.**

If you find yourself:
- Guessing about configuration file locations → Read `settings.md`
- Speculating about API structures → Read relevant reference doc
- Unsure about hook names → Read `hooks.md`
- Making assumptions about features → Search the docs first

---

**External Resource:** https://docs.claude.com/en/docs/claude-code/
