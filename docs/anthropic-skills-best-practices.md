# Anthropic Official Best Practices for Claude Code Skills and Plugins

**Research Date**: 2026-02-02
**Sources**: Official Anthropic documentation, Claude Code docs, Anthropic engineering blog

---

## Table of Contents

1. [Verification-First Design Patterns](#1-verification-first-design-patterns)
2. [Context Budget Guidance](#2-context-budget-guidance)
3. [Frontmatter Configuration](#3-frontmatter-configuration)
4. [Skill vs CLAUDE.md Decision Criteria](#4-skill-vs-claudemd-decision-criteria)
5. [Skill Structure and Triggers](#5-skill-structure-and-triggers)
6. [Skill Composition and Progressive Disclosure](#6-skill-composition-and-progressive-disclosure)
7. [Testing and Iteration](#7-testing-and-iteration)
8. [Anti-Patterns to Avoid](#8-anti-patterns-to-avoid)

---

## 1. Verification-First Design Patterns

### Official Guidance

From [Best Practices for Claude Code](https://code.claude.com/docs/en/best-practices):

> "Include tests, screenshots, or expected outputs so Claude can check itself. **This is the single highest-leverage thing you can do.**"

> "Claude performs dramatically better when it can verify its own work, like run tests, compare screenshots, and validate outputs."

> "Without clear success criteria, it might produce something that looks right but actually doesn't work. You become the only feedback loop, and every mistake requires your attention."

### Implementation Patterns

**1. Provide Verification Criteria**
```
Before: "implement a function that validates email addresses"
After: "write a validateEmail function. example test cases: user@example.com is true,
       invalid is false, user@.com is false. run the tests after implementing"
```

**2. Verify UI Changes Visually**
```
Before: "make the dashboard look better"
After: "[paste screenshot] implement this design. take a screenshot of the result
       and compare it to the original. list differences and fix them"
```

**3. Address Root Causes**
```
Before: "the build is failing"
After: "the build fails with this error: [paste error]. fix it and verify the
       build succeeds. address the root cause, don't suppress the error"
```

### Application to Skill Authoring

From [Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices):

> "Tell Claude what a good output looks like. If you're creating financial reports, specify required sections, formatting standards, validation checks, and quality thresholds. Include these criteria in your instructions so Claude can self-check."

**Verification can be:**
- A test suite
- A linter
- A Bash command that checks output
- Visual comparison for UI work

**Source**: https://code.claude.com/docs/en/best-practices

---

## 2. Context Budget Guidance

### Why Context Limits Matter

From [Best Practices for Claude Code](https://code.claude.com/docs/en/best-practices):

> "Most best practices are based on one constraint: **Claude's context window fills up fast, and performance degrades as it fills.**"

> "Claude's context window holds your entire conversation, including every message, every file Claude reads, and every command output. However, this can fill up fast. A single debugging session or codebase exploration might generate and consume tens of thousands of tokens."

> "**This matters since LLM performance degrades as context fills.** When the context window is getting full, Claude may start 'forgetting' earlier instructions or making more mistakes. The context window is the most important resource to manage."

### Skill Description Budget

From [GitHub Issue #13099](https://github.com/anthropics/claude-code/issues/13099) and documentation:

> "Skill descriptions are loaded into context so Claude knows what's available. If you have many skills, they may exceed the character budget (default **15,000 characters**). Run `/context` to check for a warning about excluded skills."

**Key Details:**
- Budget limit is approximately 15,500-16,000 characters for skill metadata
- Each skill consumes ~109 characters of XML overhead plus description length
- With 63 installed skills, only 42 may be shown due to token limits

**Recommendations for Staying Within Budget:**
- Keep descriptions under 130 characters for collections of 60+ skills
- Keep descriptions under 150 characters for collections of 40-60 skills
- Front-load trigger keywords in the first 50 characters

### Progressive Disclosure Architecture

From [Anthropic Engineering Blog](https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills):

> "The key innovation is **progressive disclosure**, a three-level system for managing context efficiently:
> - **Metadata**: At startup, the agent loads only the name and description of each installed skill (~100 tokens)
> - **Instructions**: When a skill is triggered, the agent loads the full SKILL.md body (<5k tokens)
> - **Resources**: If the task requires more detail, the agent can dynamically load additional files"

**Context Efficiency:**
> "Files are read on-demand, and scripts are executed efficiently with only the script's output consuming tokens. There's no context penalty for large files until they're actually read."

### CLAUDE.md Size Guidance

From [Claude Code Docs](https://code.claude.com/docs/en/best-practices):

> "Keep CLAUDE.md concise. CLAUDE.md is loaded every session, so only include things that apply broadly. For domain knowledge or workflows that are only relevant sometimes, use skills instead."

> "An unbounded CLAUDE.md defeats the purpose. If it grows to 500 lines, you're wasting context window on low-value information."

**Source**: https://code.claude.com/docs/en/best-practices, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

---

## 3. Frontmatter Configuration

### Available Frontmatter Fields

From [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills):

| Field | Required | Description |
|-------|----------|-------------|
| `name` | No | Display name. Lowercase letters, numbers, hyphens only (max 64 chars). If omitted, uses directory name. |
| `description` | Recommended | What the skill does and when to use it. Claude uses this to decide when to apply the skill. Max 1024 characters. |
| `argument-hint` | No | Hint shown during autocomplete. Example: `[issue-number]` |
| `disable-model-invocation` | No | Set `true` to prevent Claude from automatically loading. Default: `false` |
| `user-invocable` | No | Set `false` to hide from `/` menu. Default: `true` |
| `allowed-tools` | No | Tools Claude can use without permission when skill is active. |
| `model` | No | Model to use when skill is active. |
| `context` | No | Set to `fork` to run in a forked subagent context. |
| `agent` | No | Which subagent type to use when `context: fork` is set. |
| `hooks` | No | Hooks scoped to skill's lifecycle. |

### `disable-model-invocation` Usage

From [Official Documentation](https://code.claude.com/docs/en/skills):

> "`disable-model-invocation: true`: Only you can invoke the skill. Use this for workflows with side effects or that you want to control timing, like `/commit`, `/deploy`, or `/send-slack-message`. You don't want Claude deciding to deploy because your code looks ready."

**Example:**
```yaml
---
name: deploy
description: Deploy the application to production
disable-model-invocation: true
---
```

### `user-invocable` Usage

> "`user-invocable: false`: Only Claude can invoke the skill. Use this for background knowledge that isn't actionable as a command. A `legacy-system-context` skill explains how an old system works. Claude should know this when relevant, but `/legacy-system-context` isn't a meaningful action for users to take."

### `allowed-tools` Usage

From documentation:

> "Use the `allowed-tools` field to limit which tools Claude can use when a skill is active."

**Example - Read-only mode:**
```yaml
---
name: safe-reader
description: Read files without making changes
allowed-tools: Read, Grep, Glob
---
```

**Important Limitation:**
> "The `allowed-tools` frontmatter field in SKILL.md is only supported when using Claude Code CLI directly. It does not apply when using Skills through the SDK."

**Known Issue** (from [GitHub Issue #18837](https://github.com/anthropics/claude-code/issues/18837)):
> "The `allowed-tools` field in skill/command frontmatter does not appear to be enforced. Claude can freely use tools not listed in `allowed-tools`."

### Invocation Control Matrix

| Frontmatter | You can invoke | Claude can invoke | When loaded into context |
|-------------|----------------|-------------------|--------------------------|
| (default) | Yes | Yes | Description always in context, full skill loads when invoked |
| `disable-model-invocation: true` | Yes | No | Description not in context, full skill loads when you invoke |
| `user-invocable: false` | No | Yes | Description always in context, full skill loads when invoked |

**Source**: https://code.claude.com/docs/en/skills

---

## 4. Skill vs CLAUDE.md Decision Criteria

### Official Guidance

From [Best Practices](https://code.claude.com/docs/en/best-practices):

> "CLAUDE.md is loaded every session, so only include things that apply broadly. For domain knowledge or workflows that are only relevant sometimes, **use skills instead**. Claude loads them on demand without bloating every conversation."

### When to Use CLAUDE.md

| Use CLAUDE.md For | Avoid in CLAUDE.md |
|-------------------|-------------------|
| Bash commands Claude can't guess | Anything Claude can figure out by reading code |
| Code style rules that differ from defaults | Standard language conventions Claude already knows |
| Testing instructions and preferred test runners | Detailed API documentation (link to docs instead) |
| Repository etiquette (branch naming, PR conventions) | Information that changes frequently |
| Architectural decisions specific to your project | Long explanations or tutorials |
| Developer environment quirks (required env vars) | File-by-file descriptions of the codebase |
| Common gotchas or non-obvious behaviors | Self-evident practices like "write clean code" |

### When to Use Skills

From [Skills Documentation](https://code.claude.com/docs/en/skills):

**Reference Content Skills:**
> "Reference content adds knowledge Claude applies to your current work. Conventions, patterns, style guides, domain knowledge. This content runs inline so Claude can use it alongside your conversation context."

**Task Content Skills:**
> "Task content gives Claude step-by-step instructions for a specific action, like deployments, commits, or code generation. These are often actions you want to invoke directly with `/skill-name` rather than letting Claude decide when to run them."

### Key Decision Criteria

1. **Frequency of Use**
   - Always needed? -> CLAUDE.md
   - Sometimes needed? -> Skill

2. **Scope**
   - Applies to all work in project? -> CLAUDE.md
   - Applies to specific task type? -> Skill

3. **Side Effects**
   - Read-only context? -> Either
   - Has side effects (deploy, commit)? -> Skill with `disable-model-invocation: true`

4. **Size**
   - Short (< 20 lines)? -> Either
   - Detailed reference material? -> Skill with supporting files

**Source**: https://code.claude.com/docs/en/best-practices, https://code.claude.com/docs/en/skills

---

## 5. Skill Structure and Triggers

### Required Structure

From [Official Documentation](https://code.claude.com/docs/en/skills):

```
my-skill/
├── SKILL.md           # Main instructions (required)
├── template.md        # Template for Claude to fill in
├── examples/
│   └── sample.md      # Example output showing expected format
└── scripts/
    └── validate.sh    # Script Claude can execute
```

> "Every skill needs a `SKILL.md` file with two parts: YAML frontmatter (between `---` markers) that tells Claude when to use the skill, and markdown content with instructions Claude follows when the skill is invoked."

### Description Best Practices

From [Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices):

**Always Write in Third Person:**
> "The description is injected into the system prompt, and inconsistent point-of-view can cause discovery problems."

```yaml
# Good
description: "Processes Excel files and generates reports"

# Avoid
description: "I can help you process Excel files"
description: "You can use this to process Excel files"
```

**Be Specific and Include Key Terms:**

```yaml
# Good - PDF Processing skill
description: Extract text and tables from PDF files, fill forms, merge documents.
             Use when working with PDF files or when the user mentions PDFs, forms,
             or document extraction.

# Bad - Vague
description: Helps with documents
```

**Include "Use when..." Language:**
> "Add explicit triggers within the description field."

### How Skill Selection Works

From [Claude Agent Skills Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/):

> "There is no regex, no keyword matching, and no ML-based intent detection. The decision happens inside Claude's forward pass through the transformer, not in the application code."

> "Pay special attention to the name and description of your skill. Claude uses these when deciding whether to trigger the skill in response to its current task."

### Size Limits

From [Official Documentation](https://code.claude.com/docs/en/skills):

> "Keep `SKILL.md` under 500 lines. Move detailed reference material to separate files."

**Frontmatter Limits:**
- `name`: Maximum 64 characters
- `description`: Maximum 1024 characters, cannot contain XML tags

**Source**: https://code.claude.com/docs/en/skills, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

---

## 6. Skill Composition and Progressive Disclosure

### Progressive Disclosure Patterns

From [Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices):

#### Pattern 1: High-Level Guide with References

```markdown
---
name: pdf-processing
description: Extracts text and tables from PDF files...
---

# PDF Processing

## Quick start
[Essential code example]

## Advanced features
**Form filling**: See [FORMS.md](FORMS.md) for complete guide
**API reference**: See [REFERENCE.md](REFERENCE.md) for all methods
**Examples**: See [EXAMPLES.md](EXAMPLES.md) for common patterns
```

#### Pattern 2: Domain-Specific Organization

```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── reference/
    ├── finance.md (revenue metrics)
    ├── sales.md (pipeline data)
    ├── product.md (usage analytics)
    └── marketing.md (campaigns)
```

> "When a user asks about revenue, Claude reads SKILL.md, sees the reference to `reference/finance.md`, and invokes bash to read just that file. The sales.md and product.md files remain on the filesystem, consuming zero context tokens until needed."

#### Pattern 3: Conditional Details

```markdown
# DOCX Processing

## Creating documents
Use docx-js for new documents. See [DOCX-JS.md](DOCX-JS.md).

## Editing documents
For simple edits, modify the XML directly.

**For tracked changes**: See [REDLINING.md](REDLINING.md)
**For OOXML details**: See [OOXML.md](OOXML.md)
```

### Avoid Deeply Nested References

> "Keep references one level deep from SKILL.md. All reference files should link directly from SKILL.md to ensure Claude reads complete files when needed."

**Bad:**
```
SKILL.md -> advanced.md -> details.md
```

**Good:**
```
SKILL.md -> advanced.md
SKILL.md -> reference.md
SKILL.md -> examples.md
```

### Table of Contents for Long Files

> "For reference files longer than 100 lines, include a table of contents at the top. This ensures Claude can see the full scope of available information even when previewing with partial reads."

**Source**: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

---

## 7. Testing and Iteration

### Build Evaluations First

From [Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices):

> "**Create evaluations BEFORE writing extensive documentation.** This ensures your Skill solves real problems rather than documenting imagined ones."

**Evaluation-Driven Development:**
1. Identify gaps: Run Claude on representative tasks without a Skill. Document specific failures.
2. Create evaluations: Build three scenarios that test these gaps
3. Establish baseline: Measure Claude's performance without the Skill
4. Write minimal instructions: Create just enough content to address gaps
5. Iterate: Execute evaluations, compare against baseline, refine

**Evaluation Structure Example:**
```json
{
  "skills": ["pdf-processing"],
  "query": "Extract all text from this PDF file and save it to output.txt",
  "files": ["test-files/document.pdf"],
  "expected_behavior": [
    "Successfully reads the PDF file using appropriate library",
    "Extracts text content from all pages without missing any",
    "Saves the extracted text to output.txt in clear format"
  ]
}
```

### Iterative Development with Claude

> "Work with one instance of Claude ('Claude A') to create a Skill that will be used by other instances ('Claude B'). Claude A helps you design and refine instructions, while Claude B tests them in real tasks."

**Process:**
1. Complete a task without a Skill (gather context naturally)
2. Identify the reusable pattern
3. Ask Claude A to create a Skill
4. Review for conciseness
5. Improve information architecture
6. Test on similar tasks with Claude B
7. Iterate based on observation

### Test with All Target Models

> "Skills act as additions to models, so effectiveness depends on the underlying model. Test your Skill with all the models you plan to use it with."

**Testing Considerations:**
- **Claude Haiku** (fast, economical): Does the Skill provide enough guidance?
- **Claude Sonnet** (balanced): Is the Skill clear and efficient?
- **Claude Opus** (powerful reasoning): Does the Skill avoid over-explaining?

**Source**: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

---

## 8. Anti-Patterns to Avoid

### From Official Best Practices

From [Best Practices for Claude Code](https://code.claude.com/docs/en/best-practices):

**1. The Kitchen Sink Session**
> "You start with one task, then ask Claude something unrelated, then go back to the first task. Context is full of irrelevant information."
> **Fix**: `/clear` between unrelated tasks.

**2. Correcting Over and Over**
> "Claude does something wrong, you correct it, it's still wrong, you correct again. Context is polluted with failed approaches."
> **Fix**: After two failed corrections, `/clear` and write a better initial prompt.

**3. The Over-Specified CLAUDE.md**
> "If your CLAUDE.md is too long, Claude ignores half of it because important rules get lost in the noise."
> **Fix**: Ruthlessly prune. If Claude already does something correctly without the instruction, delete it.

**4. The Trust-Then-Verify Gap**
> "Claude produces a plausible-looking implementation that doesn't handle edge cases."
> **Fix**: Always provide verification (tests, scripts, screenshots).

**5. The Infinite Exploration**
> "You ask Claude to 'investigate' something without scoping it. Claude reads hundreds of files, filling the context."
> **Fix**: Scope investigations narrowly or use subagents.

### Skill-Specific Anti-Patterns

From [Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices):

**1. Offering Too Many Options**
```markdown
# Bad - Too many choices
"You can use pypdf, or pdfplumber, or PyMuPDF, or pdf2image, or..."

# Good - Provide a default with escape hatch
"Use pdfplumber for text extraction:
```python
import pdfplumber
```
For scanned PDFs requiring OCR, use pdf2image with pytesseract instead."
```

**2. Windows-Style Paths**
> "Always use forward slashes in file paths, even on Windows."
```
Good: scripts/helper.py, reference/guide.md
Bad: scripts\helper.py, reference\guide.md
```

**3. Assuming Tools Are Installed**
```markdown
# Bad
"Use the pdf library to process the file."

# Good
"Install required package: `pip install pypdf`
Then use it:
```python
from pypdf import PdfReader
```"
```

**4. Time-Sensitive Information**
```markdown
# Bad
"If you're doing this before August 2025, use the old API."

# Good - Use collapsible old patterns section
## Current method
Use the v2 API endpoint...

## Old patterns
<details>
<summary>Legacy v1 API (deprecated 2025-08)</summary>
...
</details>
```

**5. Inconsistent Terminology**
```markdown
# Bad - Mixing terms
"API endpoint", "URL", "API route", "path"

# Good - Pick one and use consistently
Always use "API endpoint"
```

**Source**: https://code.claude.com/docs/en/best-practices, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

---

## Checklist for Effective Skills

From [Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices):

### Core Quality
- [ ] Description is specific and includes key terms
- [ ] Description includes both what the Skill does AND when to use it
- [ ] SKILL.md body is under 500 lines
- [ ] Additional details in separate files (if needed)
- [ ] No time-sensitive information
- [ ] Consistent terminology throughout
- [ ] Examples are concrete, not abstract
- [ ] File references are one level deep
- [ ] Progressive disclosure used appropriately
- [ ] Workflows have clear steps

### Code and Scripts
- [ ] Scripts solve problems rather than punt to Claude
- [ ] Error handling is explicit and helpful
- [ ] No "voodoo constants" (all values justified)
- [ ] Required packages listed and verified as available
- [ ] Scripts have clear documentation
- [ ] No Windows-style paths
- [ ] Validation/verification steps for critical operations
- [ ] Feedback loops included for quality-critical tasks

### Testing
- [ ] At least three evaluations created
- [ ] Tested with Haiku, Sonnet, and Opus
- [ ] Tested with real usage scenarios
- [ ] Team feedback incorporated

---

## Summary of Key Numbers

| Metric | Limit | Source |
|--------|-------|--------|
| SKILL.md body | 500 lines max | Skill authoring best practices |
| Skill name | 64 characters max | Frontmatter reference |
| Skill description | 1024 characters max | Frontmatter reference |
| Total skill descriptions budget | ~15,000 characters | Context management |
| CLAUDE.md suggested limit | 500 lines | Best practices |

---

## Sources

- [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills)
- [Skill Authoring Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Best Practices for Claude Code](https://code.claude.com/docs/en/best-practices)
- [Manage Claude's Memory](https://code.claude.com/docs/en/memory)
- [Equipping Agents for the Real World with Agent Skills](https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills)
- [GitHub anthropics/skills](https://github.com/anthropics/skills)
- [GitHub anthropics/claude-code Issues](https://github.com/anthropics/claude-code/issues)
