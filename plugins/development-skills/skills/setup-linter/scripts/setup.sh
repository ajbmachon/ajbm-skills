#!/bin/bash
# Setup linter hook for Claude Code
# Usage: setup.sh [linter-command]
# If no command provided, auto-detects project type and installs/configures linter

set -e

# Ensure we're in a project directory
if [ -z "$CLAUDE_PROJECT_DIR" ]; then
    PROJECT_DIR="$(pwd)"
else
    PROJECT_DIR="$CLAUDE_PROJECT_DIR"
fi

SETTINGS_DIR="$PROJECT_DIR/.claude"
SETTINGS_FILE="$SETTINGS_DIR/settings.json"

#==============================================================================
# Utility Functions
#==============================================================================

detect_package_manager() {
    if [ -f "$PROJECT_DIR/yarn.lock" ]; then
        echo "yarn"
    elif [ -f "$PROJECT_DIR/pnpm-lock.yaml" ]; then
        echo "pnpm"
    elif [ -f "$PROJECT_DIR/bun.lockb" ]; then
        echo "bun"
    else
        echo "npm"
    fi
}

has_command() {
    command -v "$1" &> /dev/null
}

#==============================================================================
# JavaScript/TypeScript Setup
#==============================================================================

setup_eslint() {
    local pm=$(detect_package_manager)
    local has_react=false
    local pkg_file="$PROJECT_DIR/package.json"

    echo "Setting up ESLint..."

    # Detect React
    if grep -q '"react"' "$pkg_file" 2>/dev/null; then
        has_react=true
    fi

    cd "$PROJECT_DIR"

    # Install dependencies
    if [ "$has_react" = true ]; then
        echo "Detected React project"
        $pm add -D eslint @eslint/js eslint-plugin-react eslint-plugin-react-hooks globals
    else
        echo "Detected Node.js project"
        $pm add -D eslint @eslint/js globals
    fi

    # Create eslint.config.js
    if [ "$has_react" = true ]; then
        cat > "$PROJECT_DIR/eslint.config.js" << 'ESLINT_REACT'
import js from '@eslint/js';
import react from 'eslint-plugin-react';
import reactHooks from 'eslint-plugin-react-hooks';
import globals from 'globals';

export default [
  js.configs.recommended,
  {
    files: ['src/**/*.{js,jsx,ts,tsx}'],
    plugins: {
      react,
      'react-hooks': reactHooks,
    },
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'module',
      parserOptions: { ecmaFeatures: { jsx: true } },
      globals: { ...globals.browser, ...globals.es2021 },
    },
    settings: { react: { version: 'detect' } },
    rules: {
      'react/react-in-jsx-scope': 'off',
      'react/prop-types': 'off',
      'react-hooks/rules-of-hooks': 'error',
      'react-hooks/exhaustive-deps': 'warn',
      'no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
    },
  },
  {
    files: ['server/**/*.js', 'scripts/**/*.js'],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'module',
      globals: { ...globals.node, ...globals.es2021 },
    },
    rules: { 'no-unused-vars': ['warn', { argsIgnorePattern: '^_' }] },
  },
  { ignores: ['node_modules/', 'dist/', 'build/', '.storybook/', 'storybook-static/', 'coverage/', '.vite/', '.ai/'] },
];
ESLINT_REACT
    else
        cat > "$PROJECT_DIR/eslint.config.js" << 'ESLINT_NODE'
import js from '@eslint/js';
import globals from 'globals';

export default [
  js.configs.recommended,
  {
    files: ['**/*.js'],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'module',
      globals: { ...globals.node, ...globals.es2021 },
    },
    rules: { 'no-unused-vars': ['warn', { argsIgnorePattern: '^_' }] },
  },
  { ignores: ['node_modules/', 'dist/', 'build/', 'coverage/'] },
];
ESLINT_NODE
    fi

    # Add lint scripts to package.json
    node -e "
const fs = require('fs');
const pkg = JSON.parse(fs.readFileSync('$pkg_file', 'utf8'));
if (!pkg.scripts) pkg.scripts = {};
if (!pkg.scripts.lint) pkg.scripts.lint = 'eslint .';
if (!pkg.scripts['lint:fix']) pkg.scripts['lint:fix'] = 'eslint . --fix';
fs.writeFileSync('$pkg_file', JSON.stringify(pkg, null, 2) + '\n');
"

    echo "ESLint configured: eslint.config.js created, scripts added"
    echo "$pm run lint:fix"
}

#==============================================================================
# Python Setup
#==============================================================================

setup_ruff() {
    echo "Setting up Ruff (Python linter/formatter)..."

    cd "$PROJECT_DIR"

    # Check if uv, pip, or poetry is available
    if has_command uv; then
        uv pip install ruff
    elif has_command pip; then
        pip install ruff
    elif has_command poetry; then
        poetry add --group dev ruff
    else
        echo "Error: No Python package manager found (uv, pip, or poetry)" >&2
        exit 1
    fi

    # Create ruff.toml if not exists
    if [ ! -f "$PROJECT_DIR/ruff.toml" ] && [ ! -f "$PROJECT_DIR/pyproject.toml" ]; then
        cat > "$PROJECT_DIR/ruff.toml" << 'RUFF_CONFIG'
# Ruff configuration
line-length = 100
target-version = "py311"

[lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "C4"]
ignore = ["E501"]  # Line too long - handled by formatter

[lint.per-file-ignores]
"__init__.py" = ["F401"]  # Unused imports in __init__

[format]
quote-style = "double"
indent-style = "space"
RUFF_CONFIG
        echo "Created ruff.toml"
    fi

    echo "Ruff configured"
    echo "ruff check --fix . && ruff format ."
}

#==============================================================================
# Rust Setup
#==============================================================================

setup_rust() {
    echo "Setting up Rust linting (rustfmt + clippy)..."

    # rustfmt and clippy come with rustup
    if ! has_command rustfmt; then
        rustup component add rustfmt
    fi
    if ! has_command cargo-clippy; then
        rustup component add clippy
    fi

    echo "Rust linting configured"
    echo "cargo fmt && cargo clippy --fix --allow-dirty"
}

#==============================================================================
# Go Setup
#==============================================================================

setup_go() {
    echo "Setting up Go linting..."

    # Install golangci-lint if not present
    if ! has_command golangci-lint; then
        echo "Installing golangci-lint..."
        go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
    fi

    echo "Go linting configured"
    echo "golangci-lint run --fix"
}

#==============================================================================
# Hook Setup
#==============================================================================

setup_hook() {
    local linter_cmd="$1"

    mkdir -p "$SETTINGS_DIR"

    local full_cmd="$linter_cmd > /dev/null 2>&1 || true"

    local hook_json=$(cat <<EOF
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$full_cmd"
          }
        ]
      }
    ]
  }
}
EOF
)

    if [ -f "$SETTINGS_FILE" ]; then
        if has_command jq; then
            local existing=$(cat "$SETTINGS_FILE")

            if echo "$existing" | jq -e '.hooks.Stop' > /dev/null 2>&1; then
                echo "Warning: Stop hook already exists in $SETTINGS_FILE" >&2
                echo "Current Stop hook:" >&2
                echo "$existing" | jq '.hooks.Stop' >&2
                echo "To replace, delete hooks.Stop first or pass --force" >&2
                return 1
            fi

            echo "$existing" | jq --argjson new "$hook_json" '
                .hooks = (.hooks // {}) + $new.hooks
            ' > "$SETTINGS_FILE.tmp" && mv "$SETTINGS_FILE.tmp" "$SETTINGS_FILE"

            echo "Updated $SETTINGS_FILE with Stop hook"
        else
            echo "Error: jq required to merge with existing settings" >&2
            return 1
        fi
    else
        echo "$hook_json" > "$SETTINGS_FILE"
        echo "Created $SETTINGS_FILE with Stop hook"
    fi
}

#==============================================================================
# Clean Code Reviewer instruction in project CLAUDE.md
#==============================================================================

CLEAN_CODE_MARKER="<!-- ajbm-clean-code-reviewer -->"

setup_clean_code_instruction() {
    local claude_md="$PROJECT_DIR/CLAUDE.md"

    # Skip if marker already present
    if [ -f "$claude_md" ] && grep -q "$CLEAN_CODE_MARKER" "$claude_md" 2>/dev/null; then
        echo "Clean code reviewer instruction already in CLAUDE.md"
        return 0
    fi

    cat >> "$claude_md" <<EOF

$CLEAN_CODE_MARKER
## Clean Code Review (auto-added by setup-linter)

After any meaningful code changes (20+ lines), invoke the \`clean-code-reviewer\` agent via Task tool (subagent_type="clean-code-reviewer") to analyze your work for Clean Code compliance. The goal is to always leave code cleaner than you found it — producing a tiered report (green/yellow/red) that enables a focused clean-code commit after the working implementation.
EOF

    echo "Added clean-code-reviewer instruction to $claude_md"
}

#==============================================================================
# Auto-detection
#==============================================================================

auto_detect_and_setup() {
    echo "Auto-detecting project type..."

    # JavaScript/TypeScript (package.json)
    if [ -f "$PROJECT_DIR/package.json" ]; then
        local pm=$(detect_package_manager)

        # Check for existing lint script
        if node -e "const p=require('$PROJECT_DIR/package.json'); process.exit(p.scripts && p.scripts['lint:fix'] ? 0 : 1)" 2>/dev/null; then
            echo "Found existing lint:fix script"
            echo "$pm run lint:fix"
            return
        elif node -e "const p=require('$PROJECT_DIR/package.json'); process.exit(p.scripts && p.scripts.lint ? 0 : 1)" 2>/dev/null; then
            echo "Found existing lint script (adding lint:fix)"
            node -e "
const fs = require('fs');
const pkg = JSON.parse(fs.readFileSync('$PROJECT_DIR/package.json', 'utf8'));
if (!pkg.scripts['lint:fix']) pkg.scripts['lint:fix'] = pkg.scripts.lint + ' --fix';
fs.writeFileSync('$PROJECT_DIR/package.json', JSON.stringify(pkg, null, 2) + '\n');
"
            echo "$pm run lint:fix"
            return
        fi

        # Check for biome
        if [ -f "$PROJECT_DIR/biome.json" ]; then
            echo "Found Biome config"
            echo "npx biome check --fix ."
            return
        fi

        # Install ESLint
        setup_eslint
        return
    fi

    # Python (pyproject.toml, setup.py, requirements.txt, or .py files)
    if [ -f "$PROJECT_DIR/pyproject.toml" ] || [ -f "$PROJECT_DIR/setup.py" ] || [ -f "$PROJECT_DIR/requirements.txt" ] || ls "$PROJECT_DIR"/*.py &>/dev/null; then
        # Check for existing ruff config
        if [ -f "$PROJECT_DIR/ruff.toml" ] || grep -q '\[tool.ruff\]' "$PROJECT_DIR/pyproject.toml" 2>/dev/null; then
            echo "Found existing Ruff config"
            echo "ruff check --fix . && ruff format ."
            return
        fi

        setup_ruff
        return
    fi

    # Rust
    if [ -f "$PROJECT_DIR/Cargo.toml" ]; then
        setup_rust
        return
    fi

    # Go
    if [ -f "$PROJECT_DIR/go.mod" ]; then
        setup_go
        return
    fi

    # Deno
    if [ -f "$PROJECT_DIR/deno.json" ] || [ -f "$PROJECT_DIR/deno.jsonc" ]; then
        echo "Deno project detected"
        echo "deno lint && deno fmt"
        return
    fi

    echo "Error: Could not detect project type" >&2
    echo "Please provide linter command: $0 \"<linter-command>\"" >&2
    exit 1
}

#==============================================================================
# Main
#==============================================================================

LINTER_CMD="$1"

if [ -z "$LINTER_CMD" ]; then
    LINTER_CMD=$(auto_detect_and_setup)
fi

echo ""
echo "=============================================="
echo "Setting up Stop hook"
echo "=============================================="
echo "Linter command: $LINTER_CMD"
echo ""

setup_hook "$LINTER_CMD"
setup_clean_code_instruction

echo ""
echo "Done! Linter hook and clean-code-reviewer instruction configured."
echo "Restart Claude Code for changes to take effect."
