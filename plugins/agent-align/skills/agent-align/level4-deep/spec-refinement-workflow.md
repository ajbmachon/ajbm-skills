# Spec Refinement Workflow

Research targets, challenge angles, and domain questions for AI-to-AI spec refinement interviews.

---

## Round 0: Fidelity Policy Elicitation

**Before any domain questions**, the Interviewer should ask the Stakeholder about the fidelity policy. This is the meta-decision that governs all subsequent decisions.

Per synthesis research (P6): "The stakeholder's fidelity policy was discovered incrementally across 9 rounds. It should be asked explicitly in Round 1."

**Questions to surface:**
- "When the source spec's intent and practical simplicity conflict, which wins?"
- "What's the value hierarchy? Correctness > Simplicity > Performance > UX?"
- "Is this a product, prototype, or experiment? That changes how I evaluate tradeoffs."
- "What does the new domain require that the original spec provided implicitly?"

---

## Phase 1: Research Targets (BLOCKING)

Research before challenging. You cannot challenge intelligently without current knowledge.

| Topic | How to Research | Why |
|---|---|---|
| **Spec domain** | Read the full spec, identify the domain | Understand what's being built |
| **Technology mentioned** | Verify against current docs if tech is named | Training data may be stale |
| **Existing patterns** | If codebase context exists, explore for conventions | Spec may reference or assume codebase patterns |
| **Similar systems** | Search for existing solutions to the same problem | Challenge: "does this need to be built?" |
| **Known failure modes** | Research common failures in this domain | Challenge: "what typically goes wrong here?" |

---

## Phase 2: Challenge Angles for Spec Quality

These reveal whether spec decisions are well-justified, weakly-justified, or unjustified:

### Existence Challenges
- "Does this entire section need to exist? Could a simpler approach handle it?"
- "Is there an existing solution that does this?"
- "The spec says [X] but doesn't explain WHY. What's the reasoning?"

### Contradiction Challenges
- "Section A says [X] but section B implies [Y]. Which is correct?"
- "The spec requires both [constraint] and [approach]. These may conflict."
- "This decision depends on [assumption]. But the spec also says [contradicting fact]."

### Completeness Challenges
- "The spec covers [X] but is silent on [Y]. Is that intentional?"
- "What happens when [edge case]? The spec doesn't address this."
- "The spec assumes [X] without stating it. Is that assumption valid for the target domain?"

### Scale/Failure Challenges
- "This pattern tends to break at [threshold]. Has that been considered?"
- "What's the blast radius if [component] fails?"
- "The spec doesn't mention error handling for [scenario]. What should happen?"

---

## Phase 3: Domain-Specific Question Areas

### Architecture & Design
- How do components interact?
- What data model changes are needed?
- What are the performance requirements?
- How will this be deployed?

### Implementation Details
- What testing strategy?
- What error handling approach?
- How does this interact with existing systems?
- What migration path from current state?

### Edge Cases
- What happens under concurrent access?
- How does this behave with large datasets?
- What if dependencies are unavailable?
- What's the rollback strategy?

### New Decision Axes (A2A-specific)
Per synthesis (P7): "Scan for new decision axes — concepts that exist in the target domain but not the source."

- "What does the implementation domain require that the spec's domain provided implicitly?"
- "Are there decisions the spec doesn't address because they weren't relevant in the original context?"
- "What infrastructure, storage, auth, or deployment decisions are needed that the spec takes for granted?"

---

## Question Prioritization

Per synthesis (P5): "Lead with paradigm-setting questions — high fan-out dependency nodes first."

### Round 1: Paradigm-Setting
Questions whose answers shape 5+ downstream decisions. Architecture patterns, core tech choices, deployment model.

### Rounds 2-4: Branch Exploration
Questions that explore specific branches opened by Round 1 answers. Data model, API design, error handling.

### Rounds 5+: Edge Cases and Gaps
Questions about failure modes, edge cases, and spec sections not yet covered. Follow-up debt resolution.

---

## Output Additions (for Phase 6)

### Decision Summary Table
Include in the final spec:

```markdown
## Decisions Made

| # | Decision | Confidence | Options Considered | Rationale | Round |
|---|----------|------------|-------------------|-----------|-------|
| D1 | [text] | HIGH | [A, B, C] | [why] | R1 |
| D2 | [text] | MEDIUM | [A, B] | [why, assumption noted] | R2 |
| D3 | [text] | DEFERRED | [A, B, C] | [why human needed, recommendation: B] | R3 |
```

### Spec Quality Report
Include in the working log:

```markdown
## Spec Quality Assessment
- **Well-justified decisions:** N (survived challenge with evidence)
- **Weakly-justified decisions:** N (defended only by "spec says so")
- **Unjustified decisions:** N (could not be defended)
- **Novel decisions surfaced:** N (not in original spec)
- **Contradictions found:** N
- **Assumptions corrected:** N
```
