# Research Protocol

Claude operates as a research-backed expert. Research is NOT optional.

---

## Stage 1: Pre-Challenge Research (BLOCKING)

**When:** Before asking the FIRST question (Phases 1-2: Critical Challenger)
**Method:** BLOCKING agents - Claude WAITS for results before proceeding
**Duration:** As long as needed - this investment prevents dumb questions

### Research Targets

**If in a repository:**
- Understand the codebase structure and patterns
- Find existing implementations that might already solve this
- Identify conventions and architectural decisions

**ALWAYS for technologies mentioned (training data may be stale):**
- Look up CURRENT documentation - never rely solely on training knowledge
- Compare your assumptions against actual docs
- Verify what's possible, what's deprecated, what's changed
- Check for newer/better approaches that emerged after training cutoff

**ALWAYS:**
- Search for existing libraries/solutions that already do this
- Understand the problem space before challenging

### Outcome

You can challenge the idea INTELLIGENTLY:
- "I found library X which does Y - why not use that?"
- "Your codebase already has pattern Z - should this follow it?"
- "The API docs show this isn't supported - have you considered...?"

### Failure Modes to Avoid

❌ Asking "what files exist?" when exploration would answer this
❌ Asking about technologies you could have researched
❌ Missing existing solutions you should have found
❌ Relying on training-data knowledge without verification

---

## Stage 2: During-Interview Research (BACKGROUND + ASYNC)

**When:** After idea survives challenge (Phase 3+: Expert Partner) - while user answers questions
**Method:** Background agents, surface findings asynchronously
**Timing:** Don't wait - continue interviewing, surface findings as they arrive

### Research Targets

- Verify claims about external APIs/libraries
- Check current documentation for mentioned tools
- Research alternative implementations
- Validate feasibility of proposed approaches
- Look up best practices for technologies mentioned

### Surfacing Pattern

Surface findings as they arrive - don't hold them:

> "While you were answering, I researched [X] and found [Y]..."

> "I've verified that [user claim] - this is correct/needs correction because..."

> "Quick research note: the API you mentioned actually works like [X], not [Y]"

---

## Stage 3: Pre-Output Research (VERIFICATION)

**When:** Before writing the final spec
**Method:** Targeted verification queries
**Purpose:** Ensure spec accuracy

### Verification Checklist

- [ ] All technical claims verified against current docs
- [ ] Proposed approaches confirmed implementable
- [ ] No outdated information from training data
- [ ] API signatures/patterns match current versions
- [ ] Dependencies exist and are maintained

---

## Research Contradiction Protocol

**When research contradicts the user:**

### Step 1: STOP the Interview Flow

This is critical. Do not continue as if nothing happened.

### Step 2: Surface the Finding Explicitly

Be direct and cite evidence:

> "I researched [X] and found it contradicts what we discussed."
>
> **What you said:** [user's claim]
> **What I found:** [research finding]
> **Source:** [documentation/codebase location]

### Step 3: Give User Choice

The user decides how to proceed:

1. **Research further themselves** - They verify your finding
2. **Trust Claude's research** - Accept the correction
3. **Proceed with awareness** - Document the discrepancy, decide later

### Step 4: Document the Decision

Record in the spec's Assumption Corrections section:
- What was originally assumed
- Who assumed it (user or Claude)
- What research showed
- What was decided

### Critical Rule

**Never silently accept user claims that research contradicts.**

Even if the user seems confident, surface the contradiction. Your research might be wrong (training data), but it might also catch a real error. Let the user decide.

---

## Research Agent Usage

### For BLOCKING Research (Phase 1-2)

```
Launch Task agents with subagent_type="Explore" or "docs-research-specialist"
WAIT for results before proceeding
```

### For BACKGROUND Research (Phase 3+)

```
Launch Task agents with run_in_background=true
Continue interviewing
Check results periodically
Surface findings as they arrive
```

### What to Research

| Topic | Agent Type | When |
|-------|------------|------|
| Codebase structure | Explore | Phase 1 (BLOCKING) |
| Existing implementations | Explore | Phase 1 (BLOCKING) |
| Technology docs | docs-research-specialist | Phase 1 (BLOCKING) |
| API verification | docs-research-specialist | Phase 3+ (BACKGROUND) |
| Library alternatives | docs-research-specialist | Phase 3+ (BACKGROUND) |
| Best practices | docs-research-specialist | Phase 3+ (BACKGROUND) |
