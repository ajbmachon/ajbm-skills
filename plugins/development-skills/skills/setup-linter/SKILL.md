---
name: setup-linter
description: Configure a Stop hook to run linters when Claude finishes. Use when user asks to set up automatic linting, add a linter hook, or configure code formatting on completion. (user)
---

# Setup Linter Hook

Auto-detect, install, and configure project-specific linting with a Stop hook.

## Quick Start

Just run without arguments - it auto-detects everything:

```bash
~/.claude/skills/setup-linter/scripts/setup.sh
```

Or specify a custom command:

```bash
~/.claude/skills/setup-linter/scripts/setup.sh "yarn lint:fix"
```

## What It Does

1. **Auto-detects project type** from config files
2. **Installs linter** if not present (eslint, ruff, etc.)
3. **Creates config file** with sensible defaults
4. **Adds lint scripts** to package.json (JS projects)
5. **Sets up Stop hook** in `.claude/settings.json`

## Supported Project Types

| Project | Detection | Linter | Config Created |
|---------|-----------|--------|----------------|
| **JavaScript/React** | `package.json` | ESLint | `eslint.config.js` |
| **Python** | `pyproject.toml`, `*.py` | Ruff | `ruff.toml` |
| **Rust** | `Cargo.toml` | rustfmt + clippy | (built-in) |
| **Go** | `go.mod` | golangci-lint | (optional) |
| **Deno** | `deno.json` | deno lint/fmt | (built-in) |
| **Biome** | `biome.json` | Biome | (existing) |

## JavaScript/TypeScript Details

- Detects package manager (yarn, pnpm, bun, npm)
- Detects React projects and adds react-hooks plugin
- Creates flat config format (`eslint.config.js`)
- Adds `lint` and `lint:fix` scripts to package.json
- Ignores: node_modules, dist, .vite, .storybook, .ai

## Python Details

- Uses Ruff (fastest Python linter/formatter)
- Supports uv, pip, or poetry for installation
- Creates `ruff.toml` with sensible defaults if missing
- Enables: E, F, W, I, N, UP, B, C4 rules

## Hook Behavior

The Stop hook runs `<linter> 2>&1 || true` to:
- Capture all output (stdout + stderr)
- Never block Claude even if linting fails
- Auto-fix what it can on every response

## Examples

```bash
# Auto-detect and setup everything
~/.claude/skills/setup-linter/scripts/setup.sh

# Custom Python command
~/.claude/skills/setup-linter/scripts/setup.sh "ruff check --fix . && ruff format ."

# Custom JS command with specific paths
~/.claude/skills/setup-linter/scripts/setup.sh "yarn lint:fix src/ server/"
```

## After Setup

Restart Claude Code for the Stop hook to take effect.
