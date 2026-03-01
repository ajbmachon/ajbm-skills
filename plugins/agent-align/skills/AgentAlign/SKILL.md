---
name: AgentAlign
description: USE WHEN agent alignment, delegation alignment, agent handoff, multi-agent delegation, agent-to-agent task transfer. Structured AI-to-AI alignment protocol that prevents context compression loss, assumption stacking, and constraint evaporation during task delegation between agents.
---

# AgentAlign

Structured alignment between agents during task delegation. Prevents the delegation failures that cause multi-agent systems to build the wrong thing: context compression loss, assumption stacking, constraint evaporation, and capability blindness.

**This skill is for AI-to-AI only.** For human-AI elicitation, use the Interview skill.

---

## Why AI-to-AI Alignment Matters

### The Core Problem: Context Asymmetry

Human-AI elicitation bridges **complementary intelligence** — human depth meets AI breadth. AI-to-AI alignment bridges a different problem: **context asymmetry** — same intelligence, different information.

When Agent A delegates to Agent B, both are LLMs with the same training data. They differ in context: different conversation histories, files read, constraints captured, tools available, and roles. The delegating agent's rich 30-minute conversation with the user gets compressed into a prompt. Information is inevitably lost.

This compression loss is analogous to tacit knowledge. The delegator "knows" things it can't fully articulate in the handoff — not because the knowledge is experiential, but because context windows are finite and summarization is lossy.

### The Three Asymmetries

**1. Context asymmetry** — Each agent has different conversation history, files read, and environmental awareness. The delegator's conversation with the user becomes a compressed prompt. What was lost?

**2. Role asymmetry** — Agents have different system prompts and heuristics. The Architect reasons about tradeoffs; the Engineer reasons about implementation. Same information, different conclusions.

**3. Capability asymmetry** — Different tools, permissions, models, and isolation modes. Delegating a task requiring capabilities the worker lacks is a silent failure mode.

### The Failure Modes This Prevents

**The Telephone Game** — Intent degrades through each delegation layer. User: "fast API response" → Leader: "use caching" → Worker: "add Redis" → But the codebase uses in-memory caching. Each handoff added a reasonable assumption that compounded wrong.

**Assumption Stacking** — Leader assumes X (unchecked), Worker adds Y on top. In a 3-layer chain, three stacked unchecked assumptions cascade into a misaligned implementation.

**Constraint Evaporation** — Human sets H1: "no external services." Leader captures it. Leader spawns 3 Engineers. Do all 3 know about H1?

**Capability Blindness** — Leader asks Worker to analyze distributed architecture. Worker runs on haiku with fast-execution focus. The task needs opus-level reasoning. Neither surfaces the mismatch.

---

## The Four Operations

Adapted from the four irreducible operations of elicitation (Mirror, Surface, Probe, Converge), with purpose shifted for AI-to-AI context:

| Operation | What the Worker Does | Purpose |
|---|---|---|
| **ECHO** | Restate the task in own words | Verify delegation compression didn't lose information |
| **AUDIT** | Surface assumptions + verify constraint inheritance | Prevent assumption stacking and constraint evaporation |
| **RECOVER** | Ask questions to fill delegation gaps | Recover context lost in compression |
| **CONTRACT** | Confirm shared execution agreement | Produce a verifiable, testable commitment |

---

## Three Graduated Levels

### Level Selection

| Level | When | Boundary Test | Max Rounds |
|---|---|---|---|
| **Inline** | Simple, well-specified tasks | Could worker proceed after reading the delegation prompt? | 0 |
| **Quick** | Moderate tasks with a few ambiguities | Can alignment be achieved in one back-and-forth? | 2 |
| **Full** | Complex tasks, architecture decisions, multi-layer chains | Does this need iterative refinement? | 4 |

**Mapping to delegation TIMING SCOPE:**
- `fast` → Inline (default)
- `standard` → Quick (default), Full if ambiguous
- `deep` → Full (default), Quick if clear

Leader can override by specifying the level explicitly.

---

## Level 1: INLINE

Not a workflow invocation — a behavioral disposition for every worker agent.

The worker's first substantive output includes a brief echo block:

```
## Understanding
Task: [one-sentence restatement]
Success: [restatement of success criteria]
Constraints inherited: [H1, S1, etc. or "none specified"]
Approach: [brief statement of how worker will proceed]
```

**Convergence:** Implicit. Delegator reads echo; if correct, no response needed. If wrong, one correction message. Worker re-echoes and proceeds.

**Token cost:** ~50-80 tokens.

**Anti-pattern — Echo Theater:** Echo must restate in the worker's OWN words. Copy-pasting the delegation prompt proves nothing about understanding.

---

## Level 2: QUICK

One round of SendMessage back-and-forth before work begins.

### Message 1 — Worker to Leader

```
## ECHO
Task: [restatement in own words]
Intent: [why this matters — business context]
Success: [what "done" looks like]

## AUDIT
Constraints inherited: [list with IDs, or "none specified"]
My assumptions: [things not specified, worker filling in]
Capability check: [tools available / gaps identified]

## RECOVER
Questions (answer changes my approach):
1. [specific question about gap in delegation]
2. [specific question about ambiguity]
```

### Message 2 — Leader to Worker

```
## Corrections
[corrections to ECHO, or "none — understanding is correct"]

## Answers
1. [answer]
2. [answer]

## Additional constraints
[any constraints forgotten in delegation, or "none"]

## CONTRACT: Confirmed
```

**Worker proceeds after receiving Message 2.** If the leader's response reveals NEW ambiguity, one follow-up round is allowed (Quick-Extended). After that, proceed regardless.

### Question Rules

- **Max 5 questions** — hard cap. This is alignment, not an interview.
- **Each must earn its place** — would a different answer change the implementation?
- **No re-reading questions** — if the answer is in the delegation prompt, don't ask it
- **Gap-specific only** — each question targets a specific piece of missing context

### Convergence Signals

- Leader's response answers all questions without raising new ones → converged
- Leader's corrections are minor (naming, not architecture) → converged
- If Quick-Extended still leaves ambiguity → escalate to Full

---

## Level 3: FULL

Multi-round alignment with a shared handoff spec document.

### Phase 1: ECHO + AUDIT (Worker → Leader)

```
## ECHO
Task: [detailed restatement]
Intent: [business context from the human principal]
Success criteria:
- [testable criterion 1]
- [testable criterion 2]
Scope:
- In: [enumerated]
- Out: [enumerated]

## AUDIT

### Constraints inherited
| ID | Constraint | Source | My interpretation |
|----|-----------|--------|-------------------|
| H1 | [text] | [human principal / leader] | [how I'll honor this] |
| S1 | [text] | [source] | [how I'll honor this] |

### My assumptions (things not specified)
- [assumption 1] — proceeding with this unless corrected
- [assumption 2] — proceeding with this unless corrected

### Capability check
- Tools available: [list]
- Tools needed but missing: [list, or "none"]
- Model: [what I'm running on]
- Permissions: [file write, bash, etc.]

### Potential conflicts
- [constraint X might conflict with approach Y]
- [or "no conflicts detected"]
```

Leader responds with corrections, confirmations, and missing context.

### Phase 2: RECOVER (Max 2 rounds)

Questions organized by what decision they unlock:

```
## RECOVER — Round 1

### [Architecture decision name]
1. [question] — determines whether I use approach A or B
2. [question] — clarifies scope boundary

### [Implementation detail name]
3. [question] — affects file structure
4. [question] — affects testing approach
```

Leader answers. If answers resolve all ambiguity → Phase 3. If new gaps emerge → one more RECOVER round.

**Hard cap: 2 RECOVER rounds.** If not aligned after 2 rounds, the task is too ambiguous for agent-to-agent delegation. Escalate to a human-AI interview.

### Phase 3: CONTRACT (Handoff Spec Document)

Worker writes a shared handoff spec to `.claude/handoffs/{task-name}.md`:

```markdown
# Handoff Spec: [Task Name]

**Leader:** [agent name] | **Worker:** [agent name]
**Status:** CONFIRMED | IN PROGRESS | COMPLETE

---

## Task
[clear statement of what will be done]

## Intent
[business context — why this matters to the human principal]

## Success Criteria
- [ ] [testable criterion 1]
- [ ] [testable criterion 2]
- [ ] [testable criterion 3]

## Constraint Registry (Inherited Chain)

### From Human Principal
| ID | Constraint | Type | How Honored |
|----|-----------|------|-------------|
| H1 | [text] | Hard | [specific approach] |

### From Leader
| ID | Constraint | Type | How Honored |
|----|-----------|------|-------------|
| L1 | [text] | Soft | [specific approach] |

## Scope
- **In:** [enumerated]
- **Out:** [enumerated]

## Approach
[architecture, file changes, testing strategy]

## Assumptions Confirmed
- [assumption] — confirmed by leader in Round [N]

## Assumptions Unconfirmed (Proceeding With)
- [assumption] — not addressed; worker proceeding with default

## Decisions Made During Alignment
| Decision | Alternatives | Chosen | Rationale |
|----------|-------------|--------|-----------|
```

Leader confirms: `CONTRACT: CONFIRMED` or `CONTRACT: REVISED — [changes]` (one revision round max).

---

## Constraint Inheritance Protocol

For multi-layer chains (Leader → Architect → Engineer), constraints must survive every junction.

### Rules

1. **Constraints are PASSED DOWN, never invented.** Workers cannot create Hard Constraints the human principal didn't establish. Workers CAN add Soft Constraints consistent with inherited Hard Constraints.
2. **Every junction echoes the full chain.** The downstream agent lists ALL inherited constraints, not just those from its immediate delegator.
3. **Traceability is mandatory.** Each constraint traces to its source: human principal, leader, or intermediate agent.
4. **Type cannot be downgraded.** Hard stays Hard through the chain.

### Chain Format

```
### Layer 0: Human Principal
| ID | Constraint | Type |
|----|-----------|------|
| H1 | Must work offline | Hard |
| S1 | Prefer TypeScript | Soft |

### Layer 1: Leader → Architect
| ID | Constraint | Type | Source |
|----|-----------|------|--------|
| H1 | Must work offline | Hard | Inherited from Human (H1) |
| S1 | Prefer TypeScript | Soft | Inherited from Human (S1) |
| L1 | Use event-driven architecture | Soft | Leader decision (consistent with H1) |

### Layer 2: Architect → Engineer
| ID | Constraint | Type | Source |
|----|-----------|------|--------|
| H1 | Must work offline | Hard | Inherited from Human (H1) |
| S1 | Prefer TypeScript | Soft | Inherited from Human (S1) |
| L1 | Use event-driven architecture | Soft | Inherited from Leader (L1) |
| A1 | Service worker for offline sync | Soft | Architect decision (implements H1) |
```

### Verification at Each Layer

1. Worker lists ALL inherited constraints (catches evaporation)
2. Worker states how each will be honored (catches drift)
3. If approach would violate an inherited constraint, worker STOPS and surfaces the conflict

---

## Anti-Patterns

| Anti-Pattern | What It Looks Like | Prevention |
|---|---|---|
| **Bureaucracy Trap** | 10 questions for a 3-file change | Questions proportional to blast radius. Use Inline for simple tasks. |
| **Echo Theater** | Verbatim copy of delegation prompt | Echo must restate in worker's OWN words. |
| **Constraint Inflation** | Worker invents Hard Constraints | Only human principal establishes Hard Constraints. |
| **Assumption Hiding** | Worker proceeds without listing assumptions | AUDIT requires explicit enumeration. |
| **Round Padding** | Questions answerable from the delegation prompt | Read before asking. |
| **Chain Amnesia** | Middle agent drops principal's constraints | Full chain required at every layer. |
| **Premature Execution** | Worker starts before CONTRACT confirmed | Quick and Full require leader confirmation first. |

---

## Integration with Delegation Systems

AgentAlign maps onto the standard 5-component delegation prompt:

| Delegation Component | AgentAlign Phase | What AgentAlign Adds |
|---|---|---|
| WHY (business context) | ECHO — Intent field | Worker verifies it understood the "why" |
| WHAT (current state) | ECHO — Task field | Worker confirms scope understanding |
| EXACTLY (precise actions) | RECOVER — Questions | Worker asks about gaps in "exactly" |
| SUCCESS CRITERIA | ECHO + CONTRACT | Worker restates; contract makes them binding |
| TIMING SCOPE | Level selection | fast→Inline, standard→Quick, deep→Full |

---

## Degrees of Freedom

| Component | Freedom | Notes |
|-----------|---------|-------|
| Level selection | **Medium** | Mapped to timing scope, but leader can override |
| Phase ordering | **None** | ECHO → AUDIT → RECOVER → CONTRACT is fixed |
| Question content | **High** | Specific to THIS delegation |
| Constraint inheritance | **None** | Full chain must be propagated |
| Handoff spec format | **Low** | Template required for interoperability |
| Number of RECOVER rounds | **Medium** | 0-2, driven by convergence signals |

---

## Example: Quick Level in Action

**Leader delegates to Engineer:**
> "Implement the webhook retry system. Events POST to client URLs with HMAC-SHA256 signing. Retry on failure with exponential backoff (30s, 2m, 15m, 1h, 6h). 24-hour TTL. Constraints from Andre: H1 — no external services (use existing Postgres for queue, not Redis/RabbitMQ). S1 — prefer TypeScript. Files: src/webhooks/retry.ts, tests alongside."

**Engineer (Message 1):**
> ## ECHO
> Task: Build a webhook retry system that queues failed deliveries and retries with exponential backoff, using Postgres as the queue backend.
> Intent: Clients get reliable webhook delivery with at-least-once guarantee within 24 hours.
> Success: Failed webhooks retried at 30s/2m/15m/1h/6h intervals; dead letters after 24h.
>
> ## AUDIT
> Constraints inherited: H1 — no external services (Postgres only), S1 — TypeScript
> My assumptions:
> - Retry intervals are fixed, not configurable per-client
> - Dead-lettered webhooks are logged but not re-queued
> - HMAC signing uses a per-client secret stored in the clients table
> Capability check: File write, bash, Explore tools. No gaps.
>
> ## RECOVER
> 1. Should the retry worker poll Postgres on a cron interval, or use LISTEN/NOTIFY for immediate retry?
> 2. The existing codebase has `src/webhooks/deliver.ts` — should I extend that or create a separate retry module?

**Leader (Message 2):**
> ## Corrections
> None — understanding is correct.
>
> ## Answers
> 1. LISTEN/NOTIFY — near-immediate retry after backoff period.
> 2. Separate module — keep delivery and retry concerns isolated.
>
> ## CONTRACT: Confirmed

**Engineer proceeds with implementation.**
