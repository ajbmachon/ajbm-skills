# Patterns Library

Reusable patterns for skill design and trigger configuration.

## Table of Contents

- [Skill Design Patterns](#skill-design-patterns)
- [Behavioral Enforcement Patterns](#behavioral-enforcement-patterns)
- [Output Structure Patterns](#output-structure-patterns)
- [Research & Verification Patterns](#research--verification-patterns)
- [Trigger Patterns (Regex/Glob)](#trigger-patterns-regexglob)

---

## Skill Design Patterns

### Iron Law Pattern

**Use when:** A practice is non-negotiable and must never be skipped.

**Structure:**
```markdown
## The Iron Law

```
NO [FORBIDDEN ACTION] WITHOUT [REQUIRED PRECONDITION] FIRST
```

[Brief consequence statement]

**No exceptions:**
- [Exception someone might claim]
- [Another exception someone might claim]

[Action to take if violated]: Delete it. Start over.
```

**Example** (from `test-driven-development`):
```markdown
## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? Delete it. Start over.
```

**Why it works:** Named rules create accountability. "You violated the Iron Law" is clearer than "You should have tested first."

---

### Two-Phase Identity Pattern

**Use when:** Claude needs different behaviors at different workflow stages.

**Structure:**
```markdown
**Your identity evolves:**
- **Phase 1-N:** [Identity A] (behavioral keywords)
- **Transition:** [Explicit criteria and actions]
- **Phase N+1:** [Identity B] (behavioral keywords)
```

**Example** (from `interview`):
```markdown
**Your identity evolves:**
- **Phases 1-2:** Critical Challenger (skeptical, probing, BLOCKING research)
- **Transition:** Capture Constraint Registry, get user confirmation
- **Phase 3+:** Expert Partner (collaborative, thorough, CONSTRAINT-ENFORCED)
```

**Why it works:** Without explicit phases, Claude defaults to agreeable partner mode. Named identities ("Challenger") create behavioral anchors.

---

### Mandatory Read Tags Pattern

**Use when:** Files MUST be read before proceeding.

**Structure:**
```xml
<mandatory_read phase="[phase_name]">
## REQUIRED READING - DO NOT SKIP

Before doing ANYTHING else, you MUST read these files:
1. [file1.md](file1.md) - [what it defines]
2. [file2.md](file2.md) - [what it defines]

**Do NOT proceed until you have read [all/both] files.**
</mandatory_read>
```

**Why it works:** Makes skipping a visible violation rather than oversight.

---

### Constraint Registry Pattern

**Use when:** Decisions made early must be enforced throughout workflow.

**Structure:**
```markdown
## Constraint Registry

**Hard Constraints:** (immutable)
- H1: [constraint]
- H2: [constraint]

**Soft Constraints:** (negotiable with justification)
- S1: [constraint]

**Verification:** Before ANY major recommendation:
1. Identify relevant constraints
2. Verify alignment BEFORE stating recommendation
3. State recommendation WITH constraint reference
```

**Why it works:** Without explicit registry, constraints drift. "Given constraint H1..." creates accountability.

---

## Behavioral Enforcement Patterns

### Rationalization Defense Table

**Use when:** Users (or Claude) might talk themselves out of following the skill.

**Structure:**
```markdown
## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "[Common excuse]" | [Why it's wrong] |
| "[Another excuse]" | [Why it's wrong] |
```

**Example** (from `test-driven-development`):
```markdown
| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "TDD is dogmatic" | TDD IS pragmatic: finds bugs before commit. |
```

**Why it works:** Preemptive counters prevent Claude from accepting rationalizations.

---

### Red Flags / Stop Conditions Pattern

**Use when:** Certain states should halt progress and force restart.

**Structure:**
```markdown
## Red Flags - STOP and Start Over

- [Condition 1]
- [Condition 2]
- [Condition N]

**All of these mean:** [Required action]
```

**Example** (from `test-driven-development`):
```markdown
## Red Flags - STOP and Start Over

- Code before test
- Test passes immediately
- Rationalizing "just this once"
- "I already manually tested it"

**All of these mean: Delete code. Start over with TDD.**
```

**Why it works:** Named stop conditions create clear decision points.

---

### Verification Gate Pattern

**Use when:** Major decisions need explicit constraint checking.

**Structure:**
```markdown
**Before ANY [decision type]:**

1. **Verification Gate**
   - Identify relevant constraints from registry
   - Verify alignment BEFORE stating recommendation
   - State recommendation WITH constraint reference:
   > "Given constraint H1 ([description]), I recommend..."
```

---

### Self-Challenge Trigger Pattern

**Use when:** Claude might make assumptions without realizing.

**Structure:**
```markdown
**Self-Challenge Trigger** (when filling in details user didn't specify):
- Ask: "Am I assuming this or did the user say it?"
- If assuming → surface it: "I'm assuming [X]. Is that correct?"
- Offer alternatives when ambiguous
```

---

## Output Structure Patterns

### Tiered Output Pattern

**Use when:** Findings have different severity/confidence levels.

**Structure:**
```markdown
## 🟢 [TIER 1 NAME] ([characteristic])
> [Confidence level, action type]

[Items in this tier]

## 🟡 [TIER 2 NAME] ([characteristic])
> [Confidence level, action type]

[Items in this tier]

## 🔴 [TIER 3 NAME] ([characteristic])
> [Confidence level, action type]

[Items in this tier]
```

**Example** (from `clean-code-reviewer`):
```markdown
## 🟢 SYNTACTIC ISSUES (Auto-Fixable)
> Safe to fix automatically. Confidence: 99%+

## 🟡 SEMANTIC ISSUES (Review & Apply)
> Localized changes requiring judgment. Confidence: 80-99%

## 🔴 ARCHITECTURAL ISSUES (Human Judgment Required)
> Design-level concerns. Do NOT auto-fix.
```

**Why it works:** Gives users clear triage and action guidance.

---

### Why This Matters Pattern

**Use when:** Users should understand principles, not just fixes.

**Structure:**
```markdown
**Why This Matters:** [Cognitive/maintenance cost] + [principle reference] + [benefit of fix]
```

**Example:**
```markdown
**Why This Matters:** Functions over 20 lines force readers to hold too much
context in working memory. Studies show comprehension drops after 7±2 concepts.
Extracting `validateUserInput()` creates a named abstraction that communicates
intent without requiring implementation parsing.
```

**Anti-pattern:**
```markdown
**Why:** Function too long. Should be shorter.
```

---

### Blast Radius Pattern

**Use when:** Changes affect multiple files.

**Structure:**
```markdown
**Blast Radius:**
- `file1.ts` - [reason affected]
- `file2.ts` - [reason affected]
- `file3.ts` - [reason affected]
```

**Why it works:** Shows impact scope, prevents surprise breakage.

---

## Research & Verification Patterns

### Tool Priority Chain Pattern

**Use when:** Multiple tools can accomplish the same task.

**Structure:**
```markdown
## Tool Selection Priority

**1. PRIMARY:** [Tool] (if available)
   - [capability]

**2. FALLBACK:** [Tool] (if primary unavailable)
   - [capability]

**3. TERTIARY:** [Tool] - Only for [specific case]

**4. LOCAL:** [Local option] when applicable
```

**Example** (from `docs-research-specialist`):
```markdown
**1. PRIMARY: Exa MCP** (if available)
**2. FALLBACK: Context7 MCP** (if Exa unavailable)
**3. TERTIARY: WebFetch** - Only for known specific URLs
**4. LOCAL: Check codebase first** when applicable
```

---

### Caching with Staleness Detection

**Use when:** Research results should be reused but expire.

**Structure:**
```yaml
---
topic: "{{topic}}"
researched: "{{YYYY-MM-DD}}"
expires: "{{researched + 30 days}}"
sources:
  - "{{url}}"
---
```

**Staleness check:**
1. If < 30 days: Check changelog for breaking changes
2. If changelog clean: USE CACHED
3. If changelog has changes OR >= 30 days: REFRESH

---

### Source Attribution Pattern

**Use when:** Claims must be verifiable.

**Rule:** `NO CLAIM WITHOUT A SOURCE LINK — ZERO EXCEPTIONS`

**Format:** `[claim] [[source](url)]`

**Enforcement:**
- Before finalizing, verify every claim has source
- Remove unsourced claims
- Quality > quantity

---

## Trigger Patterns (Regex/Glob)

### Intent Patterns (Regex)

**Feature/Endpoint Creation:**
```regex
(add|create|implement|build).*?(feature|endpoint|route|service|controller)
```

**Component Creation:**
```regex
(create|add|make|build).*?(component|UI|page|modal|dialog|form)
```

**Database Work:**
```regex
(add|create|modify|update).*?(user|table|column|field|schema|migration)
```

**Testing:**
```regex
(write|create|add).*?(test|spec|unit.*?test)
```

### File Path Patterns (Glob)

```glob
frontend/src/**/*.tsx        # React components
**/schema.prisma             # Prisma schema
**/migrations/**/*.sql       # Migration files
**/*.test.ts                 # Test files (for exclusion)
```

### Content Patterns (Regex)

```regex
import.*[Pp]risma            # Prisma imports
export class.*Controller     # Controller classes
try\s*\{                     # Try blocks
useState|useEffect           # React hooks
```

### Pattern Best Practices

**DO:**
- Use non-greedy matching: `.*?` not `.*`
- Escape special chars: `\\.findMany\\(`
- Test at regex101.com
- Include common variations

**DON'T:**
- Use overly generic keywords
- Make patterns too broad or too specific
- Forget to test with real prompts

---

**Line count:** ~300
**Related:** [skill-triggers.md](skill-triggers.md), [agent-skill-composition.md](agent-skill-composition.md)
