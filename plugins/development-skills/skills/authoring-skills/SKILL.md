---
name: authoring-skills
description: Use when creating skills, plugins, or hooks for Claude Code - covers writing SKILL.md files, plugin structure, distribution via marketplaces, hook configuration, trigger patterns, and troubleshooting. Complete guide from authoring to distribution. Note - slash commands were removed from Claude Code, only skills remain.
---

# Authoring Skills for Claude Code

> **Note:** Slash commands were removed from Claude Code. Skills are now the only extension mechanism for providing guidance and workflows.

## Quick Reference

| Task | Resource |
|------|----------|
| Write a SKILL.md | [Core Principles](#core-principles) |
| Create a plugin | [references/plugin-development.md](references/plugin-development.md) |
| Configure triggers | [references/skill-triggers.md](references/skill-triggers.md) |
| Set up hooks | [references/hook-architecture.md](references/hook-architecture.md) |
| Debug skill/plugin issues | [references/skill-troubleshooting.md](references/skill-troubleshooting.md) |
| Find patterns | [references/patterns-library.md](references/patterns-library.md) |
| Official docs | [references/official-docs.md](references/official-docs.md) |

---

## Core Principles

### 1. Conciseness is Critical

Context window is shared. Every token competes with conversation history.

**Default assumption:** Claude is already smart. Only add what Claude doesn't know.

**Challenge each paragraph:**
- Does Claude need this explanation?
- Can I assume Claude knows this?
- Does this justify its token cost?

```markdown
# BAD (~150 tokens)
PDF (Portable Document Format) files are a common file format...

# GOOD (~50 tokens)
Use pdfplumber for text extraction:
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

### 2. Set Degrees of Freedom

Match specificity to task fragility:

| Freedom | When | Example |
|---------|------|---------|
| **High** | Multiple valid approaches | Code review process |
| **Medium** | Preferred pattern exists | Report template |
| **Low** | Fragile operations, consistency critical | Database migration |

**Analogy:**
- **Narrow bridge + cliffs** = Low freedom (exact instructions)
- **Open field** = High freedom (general direction)

### 3. Test Across Models

| Model | Check |
|-------|-------|
| **Haiku** | Enough guidance? |
| **Sonnet** | Clear and efficient? |
| **Opus** | Avoiding over-explanation? |

---

## YAML Frontmatter

```yaml
---
name: processing-pdfs          # max 64 chars, lowercase, hyphens
description: Extract text...   # max 1024 chars, third person
---
```

### Name Conventions

**Use gerund form (verb + -ing):**
- `processing-pdfs`
- `analyzing-spreadsheets`
- `managing-databases`

**Avoid:** `helper`, `utils`, `tools`, `documents`

### Description Rules

**CRITICAL:** Write in third person. Description is injected into system prompt.

```yaml
# BAD
description: I can help you process Excel files

# GOOD
description: Extract text and tables from PDF files. Use when working with PDFs or document extraction.
```

**Include both:**
1. What the skill does
2. When to use it (triggers/contexts)

---

## Progressive Disclosure

SKILL.md = overview pointing to details. **Keep under 500 lines.**

### Directory Structure

```
skill-name/
├── SKILL.md              # Main (loaded when triggered)
├── FORMS.md              # Loaded as needed
├── reference.md          # Loaded as needed
└── scripts/
    └── validate.py       # Executed, not loaded
```

### Pattern: High-Level Guide

```markdown
# PDF Processing

## Quick start
[Inline essentials]

## Advanced features
**Form filling**: See [FORMS.md](FORMS.md)
**API reference**: See [REFERENCE.md](REFERENCE.md)
```

### Pattern: Domain Organization

```
bigquery-skill/
├── SKILL.md
└── reference/
    ├── finance.md    # Only loaded when asking about revenue
    ├── sales.md      # Only loaded when asking about pipeline
    └── product.md
```

### Rules

1. **One level deep** - Don't nest references (SKILL.md → file.md, NOT file.md → details.md)
2. **TOC for 100+ lines** - Add table of contents to long reference files
3. **Descriptive names** - `form_validation_rules.md` not `doc2.md`

---

## Workflows

### Checklists for Complex Tasks

```markdown
## PDF Form Workflow

Copy and track:
- [ ] Step 1: Analyze form (`python analyze_form.py`)
- [ ] Step 2: Create field mapping
- [ ] Step 3: Validate (`python validate.py`)
- [ ] Step 4: Fill form
- [ ] Step 5: Verify output
```

### Feedback Loops

**Pattern:** Run validator → fix errors → repeat

```markdown
1. Make edits
2. **Validate immediately**: `python validate.py`
3. If fails → fix → validate again
4. **Only proceed when validation passes**
```

---

## Content Guidelines

### Avoid Time-Sensitive Info

```markdown
# BAD
If before August 2025, use old API. After, use new API.

# GOOD
## Current method
Use v2 API: `api.example.com/v2/messages`

## Old patterns
<details>
<summary>Legacy v1 API (deprecated 2025-08)</summary>
...
</details>
```

### Consistent Terminology

Pick one term, use throughout:
- Always "API endpoint" (not "URL", "route", "path")
- Always "field" (not "box", "element", "control")

---

## Common Patterns

### Template Pattern

**Strict:** "ALWAYS use this exact structure..."
**Flexible:** "Sensible default, adapt as needed..."

### Examples Pattern

Provide input/output pairs:

```markdown
**Example 1:**
Input: Added user authentication with JWT
Output:
feat(auth): implement JWT-based authentication
```

### Conditional Workflow

```markdown
**Creating new content?** → Creation workflow below
**Editing existing?** → Editing workflow below
```

---

## Scripts in Skills

### Solve, Don't Punt

```python
# BAD - punt to Claude
return open(path).read()

# GOOD - handle errors
try:
    with open(path) as f:
        return f.read()
except FileNotFoundError:
    print(f"File {path} not found, creating default")
    return ''
```

### No Magic Numbers

```python
# BAD
TIMEOUT = 47  # Why?

# GOOD
# HTTP requests typically complete within 30s
REQUEST_TIMEOUT = 30
```

### Utility Scripts

Benefits:
- More reliable than generated code
- Save tokens (not loaded into context)
- Ensure consistency

**Make intent clear:**
- "Run `analyze_form.py`" = execute
- "See `analyze_form.py` for algorithm" = read

### MCP Tool References

Use fully qualified names:
```markdown
Use BigQuery:bigquery_schema to retrieve schemas.
Use GitHub:create_issue to create issues.
```

---

## Anti-Patterns

| Anti-Pattern | Problem |
|--------------|---------|
| Windows paths (`\`) | Use forward slashes (`/`) |
| Too many options | Provide ONE default with escape hatch |
| Assuming packages | List required packages explicitly |
| Deeply nested refs | Keep one level deep |
| Vague descriptions | Be specific with triggers |
| Time-sensitive info | Use "old patterns" section |

---

## Plugin Development (Overview)

Skills can be distributed via plugins. See [references/plugin-development.md](references/plugin-development.md) for complete guide.

**Key concepts:**
- Plugin directory structure (`.claude-plugin/`, `plugin.json` manifest)
- Component types: Skills, Commands, Hooks, MCP Servers, Agents
- Distribution: GitHub, Marketplace, Private/Team
- Use `${CLAUDE_PLUGIN_ROOT}` for portable paths

**Common patterns:**
- Simple plugin with one skill
- MCP plugin with skill (tools + guidance)
- Command collection
- Hook-enhanced workflow

---

## Skill Activation System (Overview)

Skills can auto-activate based on triggers. See [references/skill-triggers.md](references/skill-triggers.md) for configuration.

**Two skill types:**
- **Guardrail** (blocking) - Enforce critical practices
- **Domain** (advisory) - Provide guidance

**Trigger types:**
- Keywords (explicit topic matching)
- Intent patterns (implicit action detection via regex)
- File paths (glob patterns)
- Content patterns (regex in files)

**Enforcement levels:**
- `BLOCK` - Prevents tool execution until skill used
- `SUGGEST` - Advisory injection into context
- `WARN` - Low priority suggestion

**Configuration:** `.claude/skills/skill-rules.json`

---

## Testing (Quick Reference)

**Full methodology:** Use `superpowers:writing-skills` for TDD approach.

**Minimum:**
1. Create 3+ evaluation scenarios
2. Test with actual tasks (not hypotheticals)
3. Test across models you'll use
4. Iterate based on observation

**Watch for:**
- Unexpected file reading order
- Missed references
- Overreliance on certain sections
- Ignored bundled files

**Test hooks manually:**
```bash
# UserPromptSubmit
echo '{"prompt":"test"}' | npx tsx .claude/hooks/skill-activation-prompt.ts

# PreToolUse
cat <<'EOF' | npx tsx .claude/hooks/skill-verification-guard.ts
{"tool_name":"Edit","tool_input":{"file_path":"test.ts"}}
EOF
```

---

## Quality Checklist

### Core Quality
- [ ] Description specific with triggers (max 1024 chars)
- [ ] Description in third person
- [ ] SKILL.md under 500 lines
- [ ] Additional details in separate files
- [ ] No time-sensitive information
- [ ] Consistent terminology
- [ ] Concrete examples
- [ ] References one level deep
- [ ] Workflows have clear steps

### Scripts (if applicable)
- [ ] Scripts solve problems (don't punt)
- [ ] Explicit error handling
- [ ] No magic numbers
- [ ] Required packages listed
- [ ] Forward slashes only
- [ ] Validation/verification steps

### Plugins (if applicable)
- [ ] `.claude-plugin/` contains only manifests
- [ ] `${CLAUDE_PLUGIN_ROOT}` used for paths
- [ ] Scripts are executable (`chmod +x`)
- [ ] hooks.json not duplicated in plugin.json

### Testing
- [ ] 3+ evaluation scenarios
- [ ] Tested with real tasks
- [ ] Tested across target models
- [ ] Iterated based on observation

---

**Line count:** ~450 (within 500-line budget)
**Complements:** `superpowers:writing-skills` (TDD testing methodology)
