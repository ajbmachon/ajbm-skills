# QuickClarify Workflow

Lightweight elicitation for tasks where the WHAT is roughly known but the HOW, edges, and assumptions need 2-5 minutes of refinement.

---

## When to Use (vs Full Workflows)

**QuickClarify** — The idea doesn't need to defend its right to exist. The user knows what they want. But there are ambiguities, unstated assumptions, or scope questions that would cause errors if left unresolved. Examples: "Add caching to this endpoint," "Refactor the auth middleware," "Build a webhook system."

**Full Workflows** (DevSpec, BusinessIdea, etc.) — The idea itself needs validation, the scope is large, or significant research and challenge are required. Examples: "Design our entire notification architecture," "I have a startup idea," "Redesign the onboarding flow."

**The boundary test:** Could Claude start implementing with reasonable confidence after 3-5 questions? → QuickClarify. Does Claude need to research, challenge the premise, and capture formal constraints? → Full workflow.

---

## Phase Structure

```
Phase 1: MIRROR     — Reflect back understanding (catch gross misalignment)
Phase 2: SURFACE    — Brief assumption audit (name what's unstated)
Phase 3: PROBE      — 1-3 rounds of targeted questions (resolve ambiguities)
Phase 4: CONVERGE   — Inline summary of aligned understanding
```

**Time budget:** 2-5 minutes total
**Max rounds:** 3 rounds of AskUserQuestion (hard cap)
**No working log:** Context window sufficient for 3-8 turns
**No blocking research:** Optional background research only
**No devil's advocate:** Purely collaborative

---

## Phase 1: MIRROR

Paraphrase what you understood from the user's request. This is NOT a summary — it's a **cognitive mirror** that lets the user see their idea from outside their head for the first time.

**Format:**
```
Here's what I understand you want:
  • [paraphrase of task]
  • [paraphrase of intent/desired outcome]
  • [paraphrase of scope, if stated]
```

**Purpose:** Catches gross misalignment immediately. If your mirror is wrong, the user corrects before any work begins. If it's right, both parties start from confirmed shared understanding.

**What makes a good mirror:**
- Restate in YOUR words, not the user's — prove you understood, don't parrot
- Include the WHY (intent) not just the WHAT (task)
- Note scope if the user implied it ("for external consumers, not internal services")

---

## Phase 2: SURFACE (Hybrid Assumption Audit)

Surface assumptions from BOTH sides before asking questions. This is where the highest value lives — small tasks fail most often because of unstated assumptions.

<mandatory_read phase="surface">
Before surfacing assumptions, review your reasoning against:
- [AssumptionAudit.md](../AssumptionAudit.md) — The Three Questions and Common Traps

Focus on: "Am I assuming or did the user say this?" and "What is the user assuming without realizing it?"
</mandatory_read>

### Step A — Brief Audit Block

State your assumptions AND surface what the user appears to assume.

**Format:**
```
I'm assuming:
  • [assumption about tech/approach]
  • [assumption about scope/requirements]

You appear to assume:
  • [implicit belief in their request]
  • [unstated expectation]
```

### Step B — Embedded in Questions

Remaining assumptions woven into probe questions naturally in Phase 3: "I'm assuming X — is that right?" This hybrid ensures assumptions are VISIBLE (audit block) and ACTIONABLE (resolved through questions).

**The two most dangerous assumption traps for small tasks:**
1. **"Standard Approach" trap** — Claude defaults to the common pattern without checking if it fits THIS codebase/context
2. **"Obvious Default" trap** — Claude fills in "obvious" choices (the default tool, structure, format) without checking if the user intended something different

---

## Phase 3: PROBE

<mandatory_read phase="probe">
**Read before asking questions:**
- [QuestionGuidelines.md](../QuestionGuidelines.md) — Question quality rules, what to ask vs avoid

Every question must earn its place. If the answer wouldn't change what you build, don't ask it.
</mandatory_read>

Use `AskUserQuestion` with 2-4 questions per round.

### Question Quality Rules

- **Earn your place** — Could I answer this myself through research? Does the answer change the outcome? If no to both, don't ask it.
- **No canned questions** — Specific to THIS situation, not templates
- **Include the non-obvious** — At least one question the user wouldn't think to ask themselves
- **Reference context** — Codebase findings, domain knowledge, or research in questions
- **Embed remaining assumptions** — "I'm assuming X — is that right?" resolves assumptions AND gathers information

### Convergence Signals (when to stop)

- No new ambiguities emerged in last round
- You could proceed without guessing on any aspect
- User's answers are getting shorter and confirmatory
- All key assumptions from the audit block have been addressed

**Hard cap:** 3 rounds maximum. If still unclear after 3 rounds, escalate to a full Interview workflow — this task is bigger than it seemed.

### Background Research

You MAY launch background research agents during probing — non-blocking only. Surface findings asynchronously: "While you answered, I found that..."

Do NOT block the conversation waiting for research. The user's answers are the primary source of truth for small tasks.

### Showpiece Questions

You may use ONE markdown-preview Showpiece question per QuickClarify session, for structural forks where text is ambiguous about the shape of the solution. See QuestionGuidelines.md for the technique. Max 1 — this is a quick flow.

---

## Phase 4: CONVERGE

Deliver an inline summary of the aligned understanding. NOT a spec file — the conversation IS the artifact.

**Format:**
```markdown
## Aligned Understanding

**Task:** [one-sentence description]
**Key decisions:**
  • [decision 1 from Q&A]
  • [decision 2 from Q&A]

**Assumptions confirmed:**
  • [confirmed assumption]

**Assumptions corrected:**
  • [what changed and why]

**Scope boundaries:**
  • In: [what's included]
  • Out: [what's excluded]

**Ready to proceed.**
```

This becomes your reference for implementation. If a question arises during implementation, check the Aligned Understanding first — the answer may already be there.

---

## Behavioral Norms

### Anti-Sycophancy (Compressed)

QuickClarify skips formal Devil's Advocate, but that doesn't mean you agree with everything. If you see a problem with the approach during probing, say so directly in your questions: "Have you considered that X might cause Y?" Challenge is embedded, not absent.

### Question Guidelines Apply

Read QuestionGuidelines.md. The same principles that make full Interview questions good apply here:
- No obvious questions (things you could find yourself)
- No generic questions (could apply to any project)
- No agreement-seeking (questions designed to confirm what you think)
- Quote user's input to prove you read it

### Information-Maximizing Questions

Each question should maximize information gain — the best question is one where DIFFERENT answers lead to DIFFERENT implementations. If all possible answers lead to the same outcome, the question wastes time.

---

## Degrees of Freedom

| Component | Freedom | Notes |
|-----------|---------|-------|
| Phase ordering | **None** | Mirror → Surface → Probe → Converge is fixed |
| Number of Q&A rounds | **High** | 1-3, convergence-signal driven |
| Question content | **High** | Specific to THIS situation |
| Background research | **Medium** | Optional, non-blocking only |
| Output format | **Low** | Must follow Converge template |
| Showpiece questions | **Low** | Max 1 per session |

---

## Example: Quick Interview in Action

**User:** "I want to add a webhook system to our API so clients can get notified of events"

### MIRROR
> Here's what I understand you want:
> - Add outbound webhooks to your existing API
> - Clients register a URL, and when events occur, you POST a payload to their URL
> - This is for external consumers of your API, not internal services

### SURFACE
> I'm assuming:
> - HTTP POST with JSON payload (standard webhook pattern)
> - Retry on failure with exponential backoff
> - Events are things like `order.created`, `user.updated`
>
> You appear to assume:
> - Clients will handle idempotency on their side
> - Webhook delivery doesn't need to be exactly-once (at-least-once is fine)

### PROBE (Round 1)
> Q1: "What events should be supported initially? I noticed your API has 12 resource types — are all of them webhook-eligible or just a subset?"
> Q2: "How should authentication work for webhook delivery? I'm assuming HMAC signature verification — but your API uses API keys elsewhere. Should webhooks follow the same pattern?"
> Q3: "What's your failure budget? If a client's endpoint is down for 2 hours, should webhooks queue indefinitely or is there a TTL?"

*[User answers: only orders and payments for phase 1, HMAC-SHA256, 24-hour retry window]*

### CONVERGE
> ## Aligned Understanding
>
> **Task:** Add webhook system for order and payment events (phase 1)
> **Key decisions:**
> - HMAC-SHA256 signature verification (consistent with API key model)
> - At-least-once delivery with 24-hour retry window
> - 5 event types: order.created, order.updated, order.cancelled, payment.succeeded, payment.failed
>
> **Assumptions confirmed:**
> - JSON POST payloads, exponential backoff (30s, 2m, 15m, 1h, 6h)
>
> **Assumptions corrected:**
> - NOT all resource types — orders and payments only for phase 1
>
> **Scope boundaries:**
> - In: Registration API, delivery engine, retry logic, signature verification
> - Out: Webhook management UI (phase 2), event filtering, batch delivery
>
> **Ready to proceed.**
