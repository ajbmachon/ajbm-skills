# Plugin Development Reference

Complete guide for creating, testing, and distributing Claude Code plugins.

## Table of Contents

- [Directory Structure](#directory-structure)
- [Plugin Manifest](#plugin-manifest)
- [Component Types](#component-types)
- [Development Workflow](#development-workflow)
- [Common Patterns](#common-patterns)
- [Cross-Platform Hooks](#cross-platform-hooks)
- [Distribution](#distribution)

---

## Directory Structure

All paths relative to plugin root:

```
my-plugin/
├── .claude-plugin/
│   ├── plugin.json          # REQUIRED - Plugin metadata
│   └── marketplace.json     # Optional - For local dev/distribution
├── skills/                  # Optional - Agent Skills
│   └── skill-name/
│       ├── SKILL.md         # Required for each skill
│       ├── scripts/         # Optional - Executable helpers
│       ├── references/      # Optional - Documentation
│       └── assets/          # Optional - Templates/files
├── commands/                # Optional - Custom slash commands
│   └── command-name.md
├── agents/                  # Optional - Specialized subagents
│   └── agent-name.md
├── hooks/                   # Optional - Event handlers
│   └── hooks.json
├── .mcp.json               # Optional - MCP server config
├── LICENSE
└── README.md
```

### Critical Rules

**1. `.claude-plugin/` Contains ONLY Manifests**

```
# WRONG
.claude-plugin/
├── plugin.json
├── skills/              # NO! Skills don't go here
└── commands/            # NO! Commands don't go here

# CORRECT
.claude-plugin/
├── plugin.json          # Only manifests
└── marketplace.json     # Only manifests

skills/                  # Skills at plugin root
commands/                # Commands at plugin root
```

**2. Use `${CLAUDE_PLUGIN_ROOT}` for Paths in Config**

```json
// WRONG - Hardcoded paths
{
  "mcpServers": {
    "my-server": {
      "command": "/Users/name/plugins/my-plugin/server.js"
    }
  }
}

// CORRECT - Variable paths
{
  "mcpServers": {
    "my-server": {
      "command": "${CLAUDE_PLUGIN_ROOT}/server.js"
    }
  }
}
```

**3. Use Relative Paths in `plugin.json`**

All paths must start with `./` and be relative to plugin root.

---

## Plugin Manifest

### Minimal plugin.json

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Brief description of what the plugin does",
  "author": {
    "name": "Your Name"
  }
}
```

### Complete plugin.json

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Comprehensive plugin description",
  "author": {
    "name": "Your Name",
    "email": "you@example.com",
    "url": "https://github.com/you"
  },
  "homepage": "https://github.com/you/my-plugin",
  "repository": "https://github.com/you/my-plugin",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "mcpServers": {
    "server-name": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/path/to/server.js"],
      "env": {
        "ENV_VAR": "value"
      }
    }
  }
}
```

### Development Marketplace (marketplace.json)

For local testing, create in `.claude-plugin/`:

```json
{
  "name": "my-plugin-dev",
  "description": "Development marketplace for my plugin",
  "owner": {
    "name": "Your Name"
  },
  "plugins": [
    {
      "name": "my-plugin",
      "description": "Plugin description",
      "version": "1.0.0",
      "source": "./",
      "author": {
        "name": "Your Name"
      }
    }
  ]
}
```

---

## Component Types

### Skills (skills/skill-name/SKILL.md)

```markdown
---
name: skill-name
description: Use when [triggering conditions] - [what it does]
---

# Skill Name

## Overview

What this skill does in 1-2 sentences.

## When to Use

- Specific scenario 1
- Specific scenario 2

## Workflow

1. Step one
2. Step two
3. Step three
```

### Commands (commands/command-name.md)

```markdown
---
description: Brief description of what this command does
---

# Command Instructions

Tell Claude what to do when this command is invoked.
Be specific and clear about the expected behavior.
```

### Hooks (hooks/hooks.json)

**WARNING:** The `hooks/hooks.json` file is automatically loaded. Do NOT reference it in `plugin.json` or you'll get "Duplicate hooks file detected" errors.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}/hooks/run-hook.cmd\" format.sh"
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}/hooks/run-hook.cmd\" init.sh"
          }
        ]
      }
    ]
  }
}
```

**Available hook events:**
- `PreToolUse`, `PostToolUse`
- `UserPromptSubmit`
- `SessionStart`, `SessionEnd`
- `Stop`, `SubagentStop`
- `PreCompact`
- `Notification`

### MCP Servers

**In plugin.json:**

```json
{
  "name": "my-plugin",
  "mcpServers": {
    "server-name": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/server/index.js"],
      "env": {
        "API_KEY": "${PLUGIN_ENV_API_KEY}"
      }
    }
  }
}
```

**Or separate .mcp.json file:**

```json
{
  "mcpServers": {
    "server-name": {
      "command": "${CLAUDE_PLUGIN_ROOT}/bin/server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"]
    }
  }
}
```

### Agents (agents/agent-name.md)

```markdown
---
description: What this agent specializes in
capabilities: ["capability1", "capability2"]
---

# Agent Name

Detailed description of when to invoke this specialized agent.

## Expertise

- Specific domain knowledge
- Specialized techniques
- When to use vs other agents
```

---

## Development Workflow

### Phase 1: Plan

1. Define your plugin's purpose (problem, users, components)
2. Choose your pattern (see [Common Patterns](#common-patterns))
3. Review existing plugins for examples

### Phase 2: Create Structure

```bash
mkdir -p my-plugin/.claude-plugin
mkdir -p my-plugin/skills
# Add other component directories as needed
```

### Phase 3: Test Locally

1. **Install for testing:**
   ```bash
   /plugin marketplace add /path/to/my-plugin
   /plugin install my-plugin@my-plugin-dev
   ```
   Then restart Claude Code.

2. **Test each component:**
   - Skills: Ask for tasks matching skill descriptions
   - Commands: Run `/your-command`
   - MCP servers: Check tools are available
   - Hooks: Trigger relevant events

3. **Iterate:**
   ```bash
   /plugin uninstall my-plugin@my-plugin-dev
   # Make changes
   /plugin install my-plugin@my-plugin-dev
   # Restart Claude Code
   ```

---

## Common Patterns

### Simple Plugin with One Skill

**Use when:** Creating focused documentation/reference material

```
my-plugin/
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── skills/
│   └── my-skill/
│       ├── SKILL.md
│       └── references/
└── README.md
```

### MCP Plugin with Skill

**Use when:** Providing tool integration (MCP) with usage guidance (skill)

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json              # Includes mcpServers config
├── skills/
│   └── using-the-tools/
│       └── SKILL.md             # How to use the MCP tools
├── mcp/
│   └── dist/
│       └── index.js
└── README.md
```

**Key insight:** MCP provides *capability*, skill provides *judgment*.

### Command Collection

**Use when:** Providing multiple slash commands for common tasks

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── status.md
│   ├── logs.md
│   └── deploy.md
└── README.md
```

### Hook-Enhanced Workflow

**Use when:** Automating actions in response to Claude's behavior

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
├── hooks/
│   └── hooks.json
├── scripts/
│   ├── format-code.sh
│   └── run-linter.sh
└── README.md
```

### Full-Featured Plugin

**Use when:** Building comprehensive plugin with multiple integration points

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── main-workflow/
│   └── advanced-techniques/
├── commands/
├── hooks/
├── agents/
├── mcp/
└── README.md
```

**Caution:** Start simple, add complexity only when justified.

---

## Cross-Platform Hooks

Claude Code runs hooks through the system's default shell:
- **Windows**: CMD.exe
- **macOS/Linux**: bash or sh

### The Polyglot Wrapper Solution

Use a single `run-hook.cmd` that works on all platforms:

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

### Usage in hooks.json

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}/hooks/run-hook.cmd\" session-start.sh"
          }
        ]
      }
    ]
  }
}
```

### Requirements

**Windows:** Git for Windows (provides `bash.exe`)
**Unix:** Standard bash, `.cmd` file must be executable (`chmod +x`)

---

## Distribution

### Option A: Direct GitHub

Users install directly from your repo:
```bash
/plugin marketplace add your-org/your-plugin-repo
```

### Option B: Marketplace (Multi-Plugin Collections)

Create marketplace repository with `.claude-plugin/marketplace.json`:

```json
{
  "name": "my-marketplace",
  "owner": {"name": "Your Name"},
  "plugins": [{
    "name": "your-plugin",
    "source": {
      "source": "url",
      "url": "https://github.com/your-org/your-plugin.git"
    },
    "version": "1.2.1",
    "description": "Plugin description"
  }]
}
```

Users add: `/plugin marketplace add your-org/your-marketplace`

### Option C: Private/Team Distribution

Configure in team's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "team-tools": {
      "source": {"source": "github", "repo": "your-org/plugins"}
    }
  }
}
```

### Versioning

Use semantic versioning (major.minor.patch):

```bash
# Update version in plugin.json
git add .
git commit -m "Release v1.2.1: [description]"
git tag v1.2.1
git push origin main
git push origin v1.2.1
```

---

**Related:**
- [skill-triggers.md](skill-triggers.md) - Skill activation configuration
- [troubleshooting.md](troubleshooting.md) - Debug plugin issues
