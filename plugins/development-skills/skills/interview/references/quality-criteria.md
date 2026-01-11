# Spec Quality Criteria

A spec is the OUTPUT of the interview. Its quality determines whether implementation will succeed or fail.

---

## What Makes a Spec HIGH QUALITY

### 1. Self-Contained for Implementation

Another Claude instance could implement it WITHOUT:

- Asking clarifying questions
- Making assumptions about intent
- Needing additional context
- Referring back to the conversation

**Test:** Read the spec cold. Can you implement it correctly on the first try?

### 2. Well-Researched

- Technical claims are VERIFIED, not assumed
- Implementation patterns match CURRENT docs/codebase
- No outdated API signatures or deprecated approaches
- External dependencies are confirmed to exist and work as described
- Training-data assumptions have been validated

**Test:** Can you trace every technical claim to a source (codebase, docs, or explicit user confirmation)?

### 3. Answers Non-Obvious Questions

Captures answers to questions the user WOULDN'T think to ask:

- Edge cases discovered through deep probing
- Failure modes identified through devil's advocacy
- Alternative approaches considered and decided
- Implicit assumptions made explicit

**Test:** Does the spec contain insights that only emerged from the interview process?

### 4. Captures the Learning Journey

Documents:

- Questions asked and answers given (Interview Record)
- Assumptions that were corrected (both user's AND Claude's)
- Decisions made and the reasoning behind them
- What was considered but rejected, and why

**Test:** Can someone understand not just WHAT to build, but WHY these choices were made?

### 5. Alignment Verified

- User's intent is explicitly confirmed (quoted back)
- Contradictions between spec and codebase are surfaced
- Any remaining uncertainties are documented as Open Questions
- Nothing is assumed without acknowledgment

**Test:** Would the user be surprised by any interpretation of the spec?

---

## Quality Anti-Patterns

A spec is LOW QUALITY when:

### Content Issues

- ❌ **Long but unresearched** - Lots of words, no verification
- ❌ **Training-data assumptions** - "This is usually how it works" without checking
- ❌ **Missing the "why"** - Decisions without rationale
- ❌ **Vague implementation details** - "Handle errors appropriately"
- ❌ **Old/improper patterns** - Using deprecated approaches

### Process Issues

- ❌ **Subtle misunderstandings** - User and Claude meant different things
- ❌ **Unchallenged assumptions** - Neither party questioned obvious choices
- ❌ **Missing Q&A record** - No trace of how conclusions were reached
- ❌ **Silent contradictions** - Research contradicted claims but wasn't surfaced

### Structure Issues

- ❌ **Missing success criteria** - No way to know when it's done
- ❌ **No edge cases** - Only happy path considered
- ❌ **Orphan decisions** - Choices that don't connect to requirements

---

## Quality Checklist

Before finalizing the spec, verify:

### Completeness
- [ ] Problem statement is clear and specific
- [ ] Objective is concrete and measurable
- [ ] Success criteria are testable
- [ ] Interview Record captures key Q&A
- [ ] Assumption Corrections documented (if any)

### Accuracy
- [ ] Technical claims verified against current docs
- [ ] Patterns match codebase conventions
- [ ] Dependencies confirmed to exist
- [ ] No training-data assumptions unverified

### Clarity
- [ ] Another Claude could implement without questions
- [ ] Decisions include rationale
- [ ] Edge cases are addressed
- [ ] Open questions are explicit (not hidden)

### Alignment
- [ ] User's original intent is reflected
- [ ] Key points quoted back and confirmed
- [ ] No surprises or unstated assumptions

---

## The Ultimate Test

> **If you handed this spec to a Claude instance that wasn't in the interview, could it implement the feature correctly on the first try?**

If yes → High quality spec
If no → Something is missing or unclear
