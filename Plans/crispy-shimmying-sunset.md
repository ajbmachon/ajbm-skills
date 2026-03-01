# Plan: Interview Skill Evolution — Quick Interview + Plugin Extraction

## Context

The Interview skill has outgrown the `development-skills` plugin — it's used for business ideas, design reviews, document drafts, ideation, and devil's advocate. It needs its own plugin. Additionally, the full 7-phase Interview is too heavy for smaller tasks where users still benefit from structured elicitation. A new lightweight "QuickClarify" workflow is needed.

A First Principles decomposition revealed that the full Interview's overhead exists to prevent memory drift across 30+ Q&A turns — irrelevant for 3-8 turn tasks. The irreducible value of human-AI elicitation comes from four operations:

1. **Mirror** — Reflect back understanding so the user sees their idea externally
2. **Surface** — Name unstated assumptions (both sides)
3. **Probe** — Ask questions whose answers change the outcome
4. **Converge** — Narrow to shared understanding

Quick Interview preserves these four and strips everything else.

---

## Part 1: QuickClarify Workflow Design

### File: `Workflows/QuickClarify.md`

**Routing table entry:**

| Workflow | Triggers | File |
|----------|----------|------|
| QuickClarify | "clarify", "quick spec", "scope this", "help me think through", "what am I missing", small/medium task with ambiguities | Workflows/QuickClarify.md |

**Boundary with full workflows:** QuickClarify is for tasks where the WHAT is roughly known but the HOW/edges/assumptions need 2-5 minutes of refinement. Full workflows (DevSpec, BusinessIdea, etc.) are for tasks where the idea itself needs validation, research, and challenge.

### Phase Structure (4 phases, no challenge)

```
Phase 1: MIRROR     — Reflect back understanding
Phase 2: SURFACE    — Brief assumption audit + assumptions in questions
Phase 3: PROBE      — 1-3 rounds of AskUserQuestion (2-4 Qs each)
Phase 4: CONVERGE   — Inline summary of aligned understanding
```

**Time budget:** 2-5 minutes total
**Max rounds:** 3 rounds of AskUserQuestion (hard cap)
**No working log:** Context window sufficient for 3-8 turns
**No blocking research:** Optional background research only
**No devil's advocate:** Purely collaborative — full Interview handles challenge for big decisions

### Phase 1: MIRROR

Claude paraphrases what it understood from the user's request. This is NOT a summary — it's a **cognitive mirror** that lets the user see their idea from outside their head.

Format:
```
Here's what I understand you want:
  [2-4 bullet paraphrase of the task, intent, and desired outcome]
```

Purpose: Catches gross misalignment immediately. If Claude's mirror is wrong, the user corrects before any work begins.

### Phase 2: SURFACE (Hybrid Assumption Audit)

**Step A — Brief audit block:** State Claude's assumptions AND surface what the user appears to assume.

Format:
```
I'm assuming:
  • [assumption 1]
  • [assumption 2]

You appear to assume:
  • [implicit belief 1]
  • [implicit belief 2]
```

**Step B — Embedded in questions:** Remaining assumptions woven into probe questions naturally: "I'm assuming X — is that right? Also..."

This hybrid ensures assumptions are VISIBLE (audit block) and ACTIONABLE (embedded in questions that resolve them).

### Phase 3: PROBE

Use `AskUserQuestion` with 2-4 questions per round. Claude must read QuestionGuidelines.md before asking.

**Question quality rules (from full Interview, still apply):**
- Every question must earn its place — could I answer this myself? Does the answer change the outcome?
- No canned/generic questions — specific to THIS situation
- Include at least one question the user wouldn't think to ask themselves
- Reference codebase findings, research, or domain knowledge in questions

**Convergence signals (when to stop):**
- No new ambiguities emerged in last round
- Claude could proceed without guessing on any aspect
- User's answers are getting shorter/confirmatory

**Hard cap:** 3 rounds maximum. If still unclear after 3 rounds, this should have been a full Interview.

**Background research:** Claude MAY launch background research agents during probing (not blocking). Surface findings as they arrive: "While you answered, I found..."

### Phase 4: CONVERGE

Inline summary of the aligned understanding. NOT a spec file — delivered directly in conversation.

Format:
```
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

This becomes Claude's reference for implementation. No separate file — the conversation IS the artifact.

### Behavioral Norms (inherited from full Interview, compressed)

- **Anti-sycophancy:** If you see a problem with the approach, say so in the probe questions — don't save it for later
- **Question Guidelines apply:** Read them. No obvious questions, no generic questions, no agreement-seeking
- **Assumption Audit lite:** Hybrid (audit block + embedded). Surface BOTH Claude's and user's assumptions
- **Showpiece questions:** May use markdown previews for structural forks (max 1 per QuickClarify session)

### Degrees of Freedom

| Component | Freedom | Notes |
|-----------|---------|-------|
| Phase ordering | **None** | Mirror → Surface → Probe → Converge is fixed |
| Number of Q&A rounds | **High** | 1-3, convergence-signal driven |
| Question content | **High** | Specific to THIS situation |
| Background research | **Medium** | Optional, non-blocking only |
| Output format | **Low** | Must follow Converge template |
| Showpiece questions | **Low** | Max 1 per session |

### Example: Quick Interview in Action

User: "I want to add a webhook system to our API so clients can get notified of events"

**MIRROR:**
> Here's what I understand: you want to add outbound webhooks to your existing API. Clients register a URL, and when events occur in your system, you POST a payload to their URL. This is for external consumers of your API, not internal services.

**SURFACE:**
> I'm assuming:
> - HTTP POST with JSON payload (standard webhook pattern)
> - Retry on failure with exponential backoff
> - Events are things like `order.created`, `user.updated`
>
> You appear to assume:
> - Clients will handle idempotency on their side
> - Webhook delivery doesn't need to be exactly-once (at-least-once is fine)

**PROBE (Round 1):**
> Q1: "What events should be supported initially? I noticed your API has 12 resource types — are all of them webhook-eligible or just a subset?"
> Q2: "How should authentication work for webhook delivery? I'm assuming HMAC signature verification — but your API uses API keys elsewhere. Should webhooks follow the same pattern?"
> Q3: "What's your failure budget? If a client's endpoint is down for 2 hours, should webhooks queue indefinitely or is there a TTL?"

[User answers...]

**CONVERGE:**
> ## Aligned Understanding
>
> **Task:** Add webhook system for order and payment events only (phase 1)
> **Key decisions:**
> - HMAC-SHA256 signature verification (consistent with API key model)
> - At-least-once delivery with 24-hour retry window
> - 5 event types initially: order.created, order.updated, order.cancelled, payment.succeeded, payment.failed
>
> **Assumptions confirmed:**
> - JSON POST payloads
> - Exponential backoff (30s, 2m, 15m, 1h, 6h)
>
> **Assumptions corrected:**
> - NOT all resource types — only orders and payments for phase 1
>
> **Scope boundaries:**
> - In: Registration API, delivery engine, retry logic, signature verification
> - Out: Webhook management UI (phase 2), event filtering/subscriptions, batch delivery
>
> **Ready to proceed.**

---

## Part 2: Plugin Extraction Plan

### New plugin: `ajbm-interview`

Move Interview from `plugins/development-skills/skills/Interview/` to `plugins/interview/skills/Interview/`.

**Files to move (all from `plugins/development-skills/skills/Interview/`):**

```
Interview/
├── SKILL.md                    (update routing table to add QuickClarify)
├── AssumptionAudit.md
├── ConstraintStore.md
├── QuestionGuidelines.md
├── VerificationGate.md
├── OutputTemplatesCore.md
├── WorkingLogTemplate.md
└── Workflows/
    ├── DevSpec.md
    ├── BusinessIdea.md
    ├── DocumentDraft.md
    ├── DesignReview.md
    ├── Ideation.md
    ├── DevilsAdvocate.md
    └── QuickClarify.md          (NEW — created from this plan)
```

**New plugin structure:**

```
plugins/interview/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── Interview/
        ├── [all files above]
```

**New `plugin.json`:**
```json
{
  "name": "ajbm-interview",
  "description": "Structured elicitation and spec crystallization through rigorous challenge, assumption surfacing, and constraint enforcement. Workflows: DevSpec, BusinessIdea, DocumentDraft, DesignReview, Ideation, DevilsAdvocate, QuickClarify.",
  "version": "2.0.0",
  "author": {
    "name": "Andre Machon",
    "url": "https://github.com/ajbmachon"
  },
  "repository": "https://github.com/ajbmachon/ajbm-skills",
  "license": "MIT",
  "keywords": [
    "interview",
    "spec",
    "requirements",
    "elicitation",
    "clarify",
    "quick-spec",
    "business-idea",
    "design-review",
    "ideation",
    "devil's-advocate",
    "brainstorm",
    "alignment"
  ]
}
```

### Updates needed:

1. **Remove Interview from `development-skills` plugin.json** — update description and keywords to remove interview references
2. **Update root CLAUDE.md** — move Interview listing from "Development Skills" section to its own "Interview Plugin" section; add QuickClarify description
3. **SKILL.md routing table** — add QuickClarify entry

---

## Part 3: Enrich Full Interview with Epistemological Framework

The deep thinking analysis revealed the fundamental WHY of elicitation. This should be embedded in the Interview SKILL.md to give Claude the right mental model when running ANY workflow.

### Add to SKILL.md — New section: "Why Elicitation Works"

Add after "Behavioral Norms" and before "Procedure." This section explains the complementary intelligence dynamic:

- **What the human brings:** Tacit knowledge, intent behind intent, contextual judgment, the right to decide
- **What the model brings:** Combinatorial breadth, ego-free challenge, cognitive mirroring, exhaustive patience
- **The four irreducible operations:** Mirror → Surface → Probe → Converge
- **Why this matters:** Error prevention at point of maximum leverage; mutual assumption correction; externalized thinking

This gives Claude the deeper WHY that improves question quality across all workflows — not just QuickClarify.

### Update Behavioral Norms

Reframe the existing norms through the epistemological lens:
- "Anti-Sycophancy" becomes grounded in "ego-free challenge is your unique advantage"
- "Structured Assumption Audit" becomes grounded in "mutual assumption correction — neither party knows what the other assumes"
- Question quality becomes grounded in "convergent narrowing — each question must maximize information gain"

---

## Part 4: Verification

1. **QuickClarify workflow:** Run a test scenario — give Claude a medium-complexity task and verify it follows Mirror → Surface → Probe → Converge
2. **Plugin extraction:** After moving files, verify `ajbm-interview` plugin loads correctly and Interview skill triggers on expected keywords
3. **SKILL.md updates:** Verify routing table includes QuickClarify with correct triggers
4. **CLAUDE.md:** Verify Interview appears in its own section with QuickClarify documented
5. **Full Interview enrichment:** Verify the epistemological framework section appears in SKILL.md and doesn't exceed 500-line limit

---

## Implementation Order

1. Create `plugins/interview/` plugin structure with plugin.json
2. Move all Interview files from development-skills to interview plugin
3. Create `Workflows/QuickClarify.md` from the design above
4. Update SKILL.md: add routing table entry, add epistemological framework section, update behavioral norms
5. Update development-skills plugin.json (remove interview references)
6. Update root CLAUDE.md (new Interview plugin section with QuickClarify)
7. Verify everything loads and triggers correctly
