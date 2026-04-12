# Output Templates

Consolidated output templates for interview specs. Read before writing Phase 6 output.

---

## 1. Base Block (Required)

### Template

```markdown
## Problem Statement

[What pain does this solve? Why does it matter? Who has this problem?]

Be specific:
- Who experiences this problem?
- When/how does it manifest?
- What's the cost of not solving it?

## Objective

[What are we building? Clear, concrete goal.]

One sentence that captures the essence. Should be quotable.

Example: "A caching layer that reduces API latency by 80% for repeat queries."

## Success Criteria

[How do you know it worked? What does "done" look like?]

List specific, testable criteria:
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]
- [ ] [Measurable outcome 3]

Each criterion should be verifiable - someone should be able to check "yes, this is met" or "no, it's not."
```

### Guidance

**Problem Statement** - Don't be vague:
- Bad: "Users have trouble with performance"
- Good: "Dashboard load times exceed 5 seconds for users with >1000 items, causing page abandonment"

**Objective** - Keep it concrete:
- Bad: "Improve the user experience"
- Good: "Add real-time search filtering to the project list, updating results as user types"

**Success Criteria** - Make them testable:
- Bad: "Works well"
- Good: "Response time < 200ms for 95th percentile queries"
- Good: "All existing tests pass"
- Good: "User can filter 10,000 items in under 1 second"

---

## 2. Interview Record (Required)

### Purpose

The Interview Record makes the spec self-contained by documenting:
- Key questions that were asked
- User's answers (condensed, not verbatim)
- Research findings that informed decisions
- The reasoning path that led to conclusions

Without this, future readers (including implementation Claude) won't understand WHY choices were made.

### Template

```markdown
## Interview Record

### [Theme 1: e.g., "Scope & Boundaries"]

**Q: [Question Claude asked]**
A: [User's answer, condensed to key points]

**Q: [Follow-up question]**
A: [Answer]

[Research note: Verified X against current docs - confirmed/corrected]

### [Theme 2: e.g., "Technical Approach"]

**Q: [Question]**
A: [Answer]

**Q: [Question]**
A: [Answer]

[Research note: Found that library Y actually does Z, not what was assumed]

### [Theme 3: e.g., "Edge Cases & Failure Modes"]

**Q: [Question about edge case]**
A: [How to handle it]

**Q: [Question about failure scenario]**
A: [Recovery/mitigation approach]

---

*This record captures the key decisions and reasoning that led to this spec.*
```

### Guidance

**Organize by Theme** - Common themes: Scope & Boundaries, Technical Approach, Edge Cases & Failure Modes, Integration Points, Success Criteria, Open Questions Resolved.

**Condense Answers** - Don't transcribe verbatim. Extract the decision/key information.
- Bad: "Well, I think maybe we should probably use Redis because we've used it before..."
- Good: "Use Redis for caching (team familiarity, proven in codebase)"

**Include Research Notes** - When research informed the discussion, note it:
- `[Research note: Verified Redis Cluster supports this pattern - docs confirm]`
- `[Research note: User assumed API v2, but current docs show v3 has breaking changes]`

**Only Include Q&A That:** Led to a decision, clarified something important, resolved an ambiguity, or corrected an assumption. Skip small talk, confirmations, and tangents.

---

## 3. Constraint Registry (Required)

### Template

```markdown
## Constraint Registry

**Captured:** [Date/time of capture]
**Confirmed by:** [User name] at [phase transition point]

### Hard Constraints (Immutable)

| # | Constraint | Source | Notes |
|---|------------|--------|-------|
| H1 | [constraint text] | User stated/defended | [optional context] |
| H2 | [constraint text] | User stated/defended | [optional context] |

### Soft Constraints (Preferences)

| # | Constraint | Negotiable If | Notes |
|---|------------|---------------|-------|
| S1 | [constraint text] | [condition] | [optional context] |

### Boundaries (Out of Scope)

| # | What's Excluded | Reason |
|---|-----------------|--------|
| B1 | [exclusion] | [why] |

---

**Constraint Verification Log:**

| Decision | Constraints Checked | Result |
|----------|---------------------|--------|
| [architecture decision] | H1, H2 | Aligned |
| [framework choice] | S1 | Preference honored |
```

### Example

```markdown
## Constraint Registry

**Captured:** 2026-01-19 during Devil's Advocate phase
**Confirmed by:** Andre at Partner transition

### Hard Constraints (Immutable)

| # | Constraint | Source | Notes |
|---|------------|--------|-------|
| H1 | Each customer gets their own separate repository | User defended during DA | Proprietary code isolation |
| H2 | Team of 2 developers | User stated | Affects complexity budget |
| H3 | Single-tenant multi-deployment | User corrected Claude's multi-tenant assumption | NOT multi-tenant |

### Soft Constraints (Preferences)

| # | Constraint | Negotiable If | Notes |
|---|------------|---------------|-------|
| S1 | Prefer TypeScript | JavaScript acceptable if TS adds friction | Existing codebase is TS |
| S2 | Use Turborepo for tooling | Alternative build system equally capable | Familiar with Turborepo |

### Boundaries (Out of Scope)

| # | What's Excluded | Reason |
|---|-----------------|--------|
| B1 | Multi-tenant architecture | Contradicts H3 |
| B2 | Public npm publishing | Proprietary code |

---

**Constraint Verification Log:**

| Decision | Constraints Checked | Result |
|----------|---------------------|--------|
| Template repo approach | H1 (separate repos) | Aligned - generates isolated repos |
| Package structure | H2 (team of 2) | Aligned - 2 packages manageable |
| Private git deps | H1, B2 | Aligned - no public publishing |
```

### Usage Notes

1. **Capture at transition** - Fill this out when moving from Devil's Advocate to Partner
2. **Get confirmation** - User must confirm before proceeding
3. **Reference throughout** - Cite constraints when making recommendations
4. **Include in final spec** - This section makes specs auditable
5. **Update if constraints change** - Document mutations with reasons

---

## 4. Assumption Corrections (Conditional)

Include when assumptions were corrected during the interview (either user's or Claude's). Omit if no assumptions were corrected.

### Template

```markdown
## Assumption Corrections

| Original Assumption | Who Held It | Source of Correction | Corrected Understanding |
|---------------------|-------------|----------------------|-------------------------|
| [What was assumed] | User/Claude | [How we learned otherwise] | [What's actually true] |
| API X supports feature Y | User | Claude researched docs | API X requires Z workaround for Y |
| Common pattern is A | Claude | Codebase investigation | This project uses pattern B instead |
| Library handles edge case | User | Testing during interview | Library throws, need custom handling |

---

*Documenting corrected assumptions prevents repeating mistakes during implementation.*
```

### Guidance

**What Qualifies:** Research contradicted a stated belief, codebase investigation showed different patterns, documentation revealed outdated understanding, testing showed unexpected behavior.

**Be Specific About Sources:**
- Bad: "Found out it doesn't work"
- Good: "Redis docs v7.2 section 4.3 - SCAN doesn't guarantee ordering"

**Include Both Parties' Corrections** - Document when Claude was wrong too.

**Document the Decision** - After noting the correction, be clear about what was decided.

---

## 5. Edge Cases (Conditional)

Include when edge cases or failure modes were surfaced during the interview.

### Template - Table Format

```markdown
## Edge Cases & Failure Modes

| Scenario | How to Handle |
|----------|---------------|
| [Edge case description] | [Approach to handle it] |
| [Failure mode] | [Recovery/prevention strategy] |
| Empty input | Return empty result, don't error |
| Network timeout | Retry 3x with exponential backoff, then surface error to user |
| Concurrent modifications | Use optimistic locking, show conflict resolution UI |
```

### Template - List Format

Use when more detail is needed:

```markdown
## Edge Cases & Failure Modes

- **[Scenario]**: [How to handle]
  - Detail if needed
  - Additional consideration

- **[Failure mode]**: [Recovery/prevention]
  - Specific steps
  - Fallback behavior
```

### Guidance

**Categories to Consider:**
- **Input:** Empty/null values, extremely large inputs, malformed data, Unicode/special characters
- **State:** First-time use, migration scenarios, partial completion
- **Timing:** Race conditions, concurrent access, stale data
- **Failure:** Network failures, dependency unavailable, rate limiting, disk full, permission denied

**Be Specific About Handling:**
- Bad: "Handle gracefully"
- Good: "Show inline error message, preserve user input, enable retry button"

**Prioritize** if many edge cases: Critical (must handle), Important (should handle), Nice to Have (can defer).

---

## 6. Tradeoffs (Conditional)

Include when decisions were made between alternatives during the interview.

### Template

```markdown
## Tradeoffs & Decisions

### TD1: [Decision name]

**Chosen:** [Selected approach]
**Over:** [Rejected alternatives]
**Tradeoff axis:** [What dimension separates the options — e.g., complexity vs. flexibility]

| Option | Pros | Cons | Who Pays |
|--------|------|------|----------|
| [Chosen] | [concrete benefits] | [concrete costs] | [who bears the cost] |
| [Rejected A] | [what this offered] | [why it lost] | [who would have paid] |

**Reasoning:** [Why this choice won given constraints and context]
**What we gave up:** [Explicit statement of the cost accepted]
```

### Example

```markdown
### TD1: Caching layer

**Chosen:** Redis
**Over:** Memcached, in-memory Map
**Tradeoff axis:** Operational familiarity vs. simplicity

| Option | Pros | Cons | Who Pays |
|--------|------|------|----------|
| Redis | Team already operates it, persistence, pub/sub | ~500MB baseline, monitoring overhead | Ops (already absorbed) |
| Memcached | Simpler, lower memory | New dependency, no persistence | Ops (new runbook) |
| In-memory Map | Zero infra, fastest | Lost on restart, no sharing across instances | Users (stale data) |

**Reasoning:** Team of 2 (H2) can't afford a new operational dependency. Redis is already in the stack.
**What we gave up:** Memcached's lower memory footprint. Acceptable — current Redis instance has headroom.
```

### Guidance

**Include When:** Multiple valid approaches were discussed, a conscious choice was made, reasoning should be preserved.

**Every tradeoff entry must answer:**
1. What did we choose and what did we reject?
2. What axis separates the options?
3. What are the concrete pros and cons of each?
4. Who bears the cost of each option?
5. What did we explicitly give up by choosing this?

**Quantify costs concretely:**
- Bad: "Better performance"
- Good: "2x faster for 95th percentile queries (400ms → 200ms)"
- Bad: "More complex"
- Good: "Adds ~200 lines of config and a migration step"

**Include rejected alternatives with their strengths** — Knowing what was NOT chosen AND what it offered prevents relitigating the decision. If someone revisits this, they can see exactly what the rejected option would have bought them.

---

## 7. Open Questions (Conditional)

Include when uncertainties remain after the interview.

### Template

```markdown
## Open Questions

- [ ] [Unresolved decision or uncertainty]
- [ ] [Thing that needs more investigation]
- [ ] [Dependency on external factor]

### Details

**[Question 1]**
Context: [Why this is unresolved]
Blocker: [What's needed to resolve it]
Fallback: [What to do if it can't be resolved]

**[Question 2]**
Context: [Why this is unresolved]
Impact: [What depends on this answer]
```

### Guidance

**Include:** Decisions that couldn't be made during interview, technical unknowns, dependencies on external people/teams, things needing production data.

**Be Specific About What's Needed:**
- Bad: "Need to figure out authentication"
- Good: "Need to confirm with security team: can we use OAuth refresh tokens with 7-day expiry, or is there a policy limit?"

**Include Fallback/Default** - What should implementation do if the question can't be resolved in time?

**Keep It Short** - Ideal: 0-3 open questions. 5+ means the interview wasn't thorough enough.

**Mark Resolution Path** - Who/what can resolve this?

---

## 8. AI-Decided Items (Conditional)

Include when any topics were deferred via Menu mode during the interview. Omit if no topics were deferred.

### Purpose

Provides a permanent, auditable record of decisions Claude made autonomously when the user chose to defer. Each item includes the decision, reasoning, assumptions, and constraint alignment — giving future readers (and implementation Claude) full context on WHY these decisions were made and WHAT could be wrong about them.

### Template

```markdown
## AI-Decided Items

> These items were decided by Claude's best judgment during the interview.
> The user chose to defer on these topics. Each was reviewed in Phase 5.
> Override any decision by updating this section before implementation.

### AD1: [Topic name]

| Field | Value |
|-------|-------|
| **Decision** | [What Claude decided] |
| **Confidence** | [🟢 High / 🟡 Medium] |
| **Reasoning** | [Why — cite codebase evidence, research findings, or logical inference] |
| **Assumptions** | (1) [First assumption]. (2) [Second assumption]. |
| **Constraint alignment** | [Which constraints checked — e.g., H1 ✓, S2 ✓] |
| **Reviewed in Phase 5** | [✓ User confirmed / ✗ User overrode → new decision] |
```

### Guidance

**Every assumption must be explicit.** The assumptions field is the most important — it tells the implementer what could invalidate this decision. If an assumption turns out wrong, the decision should be revisited.

**Include the reasoning chain, not just the conclusion:**
- Bad: "Chose Redis"
- Good: "Redis already in stack (R1 finding), 5-min TTL standard for session-adjacent data, no invalidation triggers needed beyond expiry"

**Mark Phase 5 review outcome:**
- `✓ User confirmed` — user saw the assumption and agreed
- `✗ User overrode → [new decision]` — user changed the decision (update the item)

**Keep items distinct.** Each deferred topic gets its own AD entry. Don't combine multiple topics into one.

**Typical count:** 0-3 items. If more than 3, the interview may have been too permissive with deferrals — the Menu mode guardrails cap at 3 deferrable topics per interview.
