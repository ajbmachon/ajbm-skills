---
name: authoring-skills
description: Use when writing or reviewing SKILL.md files - covers conciseness principles, description writing, progressive disclosure, degrees of freedom, naming conventions, workflows, and the quality checklist. Complements TDD-focused testing in superpowers:writing-skills.
---

# Authoring Skills

Condensed best practices from Anthropic's official guide. For TDD testing methodology, use `superpowers:writing-skills`.

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
PDF (Portable Document Format) files are a common file format that contains
text, images, and other content. To extract text from a PDF, you'll need to
use a library. There are many libraries available...

# GOOD (~50 tokens)
Use pdfplumber for text extraction:
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

### 2. Set Degrees of Freedom

Match specificity to task fragility:

| Freedom | When | Example |
|---------|------|---------|
| **High** | Multiple valid approaches, context-dependent | Code review process |
| **Medium** | Preferred pattern exists, some variation OK | Report template with parameters |
| **Low** | Fragile operations, consistency critical | Database migration script |

**Analogy:**
- **Narrow bridge + cliffs** = Low freedom (exact instructions)
- **Open field** = High freedom (general direction)

### 3. Test Across Models

| Model | Check |
|-------|-------|
| **Haiku** | Enough guidance? |
| **Sonnet** | Clear and efficient? |
| **Opus** | Avoiding over-explanation? |

What works for Opus may need more detail for Haiku.

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
description: You can use this to process Excel files

# GOOD
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

**Include both:**
1. What the skill does
2. When to use it (triggers/contexts)

## Progressive Disclosure

SKILL.md = overview pointing to details. Keep under **500 lines**.

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

## Anti-Patterns

| Anti-Pattern | Problem |
|--------------|---------|
| Windows paths (`\`) | Use forward slashes (`/`) |
| Too many options | Provide ONE default with escape hatch |
| Assuming packages | List required packages explicitly |
| Deeply nested refs | Keep one level deep |
| Vague descriptions | Be specific with triggers |
| Time-sensitive info | Use "old patterns" section |

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

## Checklist

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
- [ ] Feedback loops for quality

### Testing
- [ ] 3+ evaluation scenarios
- [ ] Tested with real tasks
- [ ] Tested across target models
- [ ] Iterated based on observation

---

**Line count:** ~250 (within 500-line budget)
**Complements:** `superpowers:writing-skills` (TDD), `skill-developer` (hooks/triggers)
