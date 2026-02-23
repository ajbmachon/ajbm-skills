# Verification Gate

Fires before recommendations to ensure they honor established constraints.

---

## Purpose

Prevent Claude from recommending solutions that contradict the user's stated constraints, especially when applying "standard patterns" that may not fit THIS user's situation.

**The problem it solves:** Claude knows a common approach from training, applies it without checking if it fits the user's specific constraints. The recommendation sounds reasonable but violates something the user explicitly stated.

---

## When the Gate Fires

### Tier 1: Major Decisions (FULL CHECK)

Decisions that would take more than a day to undo. The active workflow defines domain-specific Tier 1 examples (see DevSpec.md, BusinessIdea.md, etc.).

**General Tier 1 patterns across all domains:**
- Major strategic direction or approach
- Structural organization choices
- Key methodology or approach selection
- Foundational decisions that downstream work depends on

### Tier 2: Minor Refinements (LIGHTWEIGHT CHECK)

Easily reversible decisions. Quick mental scan: "Does this conflict with anything?" No formal constraint citation required.

---

## Full Verification Protocol

Before stating ANY Tier 1 recommendation:

**Step 1 — Identify relevant constraints:** Which constraints from the registry apply to this recommendation?

**Step 2 — Verify alignment:** Does the recommendation honor each relevant constraint? If conflict detected, STOP.

**Step 3 — State recommendation WITH constraint reference:** Make verification visible.
> "Given constraint H1 ([constraint]), I recommend [X] because it honors that constraint by..."

If conflict detected:
> "Wait — I was about to recommend [X], but that conflicts with H1 ([constraint]). Let me reconsider..."

**Example** — User wants to redesign their team's onboarding program. Constraints: H1 (must work for remote employees), H2 (team of 3 — no dedicated L&D staff), S1 (prefer async over synchronous).

> **Step 1:** I'm about to recommend a cohort-based workshop series. Relevant constraints: H1 (remote), H2 (team of 3), S1 (async preference).
>
> **Step 2:** Cohort workshops require synchronous attendance — conflicts with S1. They also need someone to facilitate — strains H2. Remote compatibility (H1) is fine with video calls, but that doubles down on the synchronous problem.
>
> **Step 3:** "Wait — cohort workshops conflict with your async preference (S1) and would strain your team of 3 (H2) to facilitate. Given those constraints, a self-paced onboarding track with async check-ins fits better. It honors H1 (fully remote), H2 (no facilitator needed), and S1 (async-first)."

---

## The "Standard Pattern" Trap

Claude knows common patterns from training and applies them without checking fit. This is the most common failure mode.

Before applying any pattern that feels "standard" or "obvious":
1. "Is this a standard pattern I'm applying?"
2. "Have I verified it fits THIS user's constraints?"
3. "What assumptions does this pattern make?"
4. "Do those assumptions match the user's situation?"

---

## Gate Bypass

The gate can be bypassed when:
1. **User explicitly requests** — "Just give me the standard approach"
2. **Already verified** — Same recommendation, constraints unchanged
3. **Trivial decisions** — Tier 2 refinements that can't violate constraints

Even when bypassed, stay alert. If something feels off, re-engage the gate.

---

## Conflict Resolution

When the gate detects a conflict:

1. **Adjust the recommendation** — Find an alternative that honors the constraint
2. **Surface the tradeoff** — If no good alternative, present options explicitly
3. **Challenge the constraint** — If the constraint seems problematic, ask if the underlying concern could be addressed differently

**NEVER silently violate a constraint.** Always surface the conflict.

---

## Visible Verification

Make the gate VISIBLE. This builds trust and catches errors.

**Good:** "Given your constraint [H1], I recommend [X] rather than [Y]. Here's why this fits..."
**Bad:** "I recommend [X]. Here's how it works..." (hides the reasoning)

---

## Integration with Assumption Audit

| Mechanism | What It Checks |
|-----------|----------------|
| **Verification Gate** | Does this violate STATED constraints? |
| **Assumption Audit** | Am I ASSUMING things? What is the USER assuming? |

Together they cover stated constraints, Claude's assumptions, and user's implicit beliefs.

See `AssumptionAudit.md` for the complementary mechanism.
