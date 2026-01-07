# Output Building Blocks

<purpose>
These templates are for **assembling the final spec output only**.
Questions come from deep thinking about the specific situation, not these templates.
</purpose>

<critical>
**MATCH COMPLEXITY TO FEATURE**

Simple feature = Simple spec. Complex feature = Detailed spec.
Don't over-engineer. A button change doesn't need architecture diagrams.
</critical>

---

## Always Include

Every spec needs these basics:

```markdown
## Problem Statement

[What pain does this solve? Why does it matter?]

## Objective

[What are we building? Clear, concrete goal.]

## Success Criteria

[How do you know it worked? What's "done"?]
```

---

## For Simple Features

Most features only need:

```markdown
## Problem Statement
[1-2 sentences]

## Objective
[1-2 sentences]

## Tasks
- [ ] [Task 1]
- [ ] [Task 2]
- [ ] [Task 3]

## Success Criteria
- [Specific outcome 1]
- [Specific outcome 2]
```

**Examples of simple features:**
- Add a button/UI element
- Fix a bug
- Update text/styling
- Add a field to a form
- Simple refactoring

---

## For Medium Features

Add more detail when the feature touches multiple files or has decisions to make:

```markdown
## Problem Statement
[Context and why this matters]

## Objective
[What we're building]

## Approach
[Brief description of how we'll solve it]

## Files to Modify
- `path/to/file.js` - [what changes]
- `path/to/other.js` - [what changes]

## Tasks
- [ ] [Task 1]
- [ ] [Task 2]

## Edge Cases
- [Edge case]: [How to handle]

## Success Criteria
- [Outcomes]
```

**Examples of medium features:**
- New API endpoint
- New component with state
- Feature with a few edge cases
- Modifications across 3-5 files

---

## For Complex Features

Only use detailed blocks when genuinely needed:

### System Architecture (multi-repo or major integrations only)

```markdown
## System Architecture

[Diagram showing components and their responsibilities]

```
Component A (repo: xxx)
    │
    ▼
Component B (repo: yyy)
```

### What Each Component Does
- **Component A:** [responsibility]
- **Component B:** [responsibility]
```

### Existing Code (when modifying existing systems)

```markdown
## Existing Code

| File | Purpose | Changes Needed |
|------|---------|----------------|
| `path/file.js` | [what it does] | [what we'll change] |

### Key Methods
- `methodName()` - [what it does, when to use it]
```

### Data Formats (when format is tricky or non-obvious)

```markdown
## Data Format

**Expected format:**
```json
{ "example": "payload" }
```

**Common mistake to avoid:**
[What people get wrong and why]
```

### Phased Implementation (for large features)

```markdown
## Phases

### Phase 1: [Name]
**Goal:** [What this achieves]
- [ ] Task 1
- [ ] Task 2
**Done when:** [Acceptance criteria]

### Phase 2: [Name]
**Depends on:** Phase 1
- [ ] Task 1
**Done when:** [Acceptance criteria]
```

---

## Optional Blocks (use when relevant)

### Tradeoffs (when decisions were made)

```markdown
## Decisions

| Decision | Why |
|----------|-----|
| [Choice] | [Reasoning] |
```

### Open Questions (when uncertainties remain)

```markdown
## Open Questions
- [ ] [Unresolved question]
```

### Code Examples (only for tricky patterns)

```markdown
## Code Pattern

> Use this pattern because [reason].

```javascript
// Example
```
```

---

## Anti-Patterns

**DON'T do these:**

❌ **Enterprise spec for simple feature**
```markdown
## Error Handling Matrix
| Scenario | Detection | Recovery | Logging | Alerting |
```
For a button click? No.

❌ **Vague spec for complex feature**
```markdown
## Approach
Call the API and handle the response.
```
Which API? What response format? What errors?

❌ **Time estimates**
```markdown
## Timeline
Phase 1: 2-3 weeks
```
Meaningless with Claude Code. Just list what's needed.

---

## Quick Reference

| Feature Type | What to Include |
|--------------|-----------------|
| Bug fix | Problem, fix location, success criteria |
| UI change | Problem, component path, visual outcome |
| New endpoint | Problem, route, request/response format |
| Integration | Architecture, data flow, existing code |
| New system | Full detailed spec with all blocks |

---

## Self-Check

Before finalizing, ask:

1. **Is this the right level of detail?** (not too much, not too little)
2. **Can a fresh Claude implement this?** (without extensive exploration)
3. **Did I avoid over-engineering?** (no enterprise patterns for simple tasks)
