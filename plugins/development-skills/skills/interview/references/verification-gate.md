# Unified Verification Gate

The Verification Gate fires before recommendations to ensure they honor established constraints.

---

## Purpose

Prevent Claude from recommending solutions that contradict user's stated constraints, especially when applying "standard patterns" that may not fit THIS user's situation.

**The problem it solves:** Claude knew "standard Turborepo monorepo" pattern, applied it without checking if it fit the user's "separate customer repos" constraint.

---

## When the Gate Fires

### Tier 1: Major Structural Decisions (FULL CHECK)

The gate fires with FULL constraint verification before:

- **Architecture patterns**: Monorepo vs polyrepo, microservices vs monolith, serverless vs containers
- **Database choices**: SQL vs NoSQL, managed vs self-hosted, single vs sharded
- **Deployment strategy**: Single tenant vs multi-tenant, per-customer vs shared
- **Framework selection**: React vs Vue, Express vs Fastify, any major tech choice
- **Team structure assumptions**: Who maintains what, ownership boundaries
- **Service architecture**: How components communicate, API design
- **Data flow**: Where data lives, how it moves between systems

**Heuristic:** If it would take more than a day to undo, it's major.

### Tier 2: Minor Refinements (LIGHTWEIGHT CHECK)

The gate fires with lightweight verification before:

- File naming conventions
- Code style decisions
- Small implementation details
- Variable naming
- Comment style

**Lightweight check:** Quick mental scan - "Does this conflict with anything?" No formal constraint citation required.

---

## Full Verification Protocol

Before stating ANY Tier 1 recommendation:

### Step 1: Identify Relevant Constraints

```
Claude (internal): "I'm about to recommend [X]. Which constraints are relevant?"
- H1: Separate customer repos → RELEVANT (affects repo structure)
- H2: Team of 2 → RELEVANT (affects complexity)
- S1: Prefer TypeScript → NOT RELEVANT (doesn't affect architecture)
```

### Step 2: Verify Alignment

```
Claude (internal): "Does [X] honor these constraints?"
- H1: Does monorepo allow separate customer repos? → NO, CONFLICT
- H2: Is monorepo manageable for team of 2? → MAYBE, worth noting
```

### Step 3: State Recommendation WITH Constraint Reference

If aligned:
> "Given constraint H1 (separate customer repos) and H2 (team of 2), I recommend a template-based approach where each customer gets their own generated repository. This honors both constraints because..."

If conflict detected:
> "Wait - I was about to recommend a monorepo, but that conflicts with H1 (separate customer repos). Let me reconsider..."

---

## The "Standard Pattern" Trap

**This is the most common failure mode.** Claude knows "standard" patterns from training:

- "Turborepo monorepos have apps/ and packages/"
- "Microservices communicate via message queues"
- "React apps use Redux for state management"

These patterns are often good, but they're not always right for THIS user.

### Before Applying Any Standard Pattern

Ask internally:
1. "Is this a standard pattern I'm applying?"
2. "Have I verified it fits THIS user's constraints?"
3. "What assumptions does this pattern make?"
4. "Do those assumptions match the user's situation?"

**Example of the trap:**
```
Standard pattern: "Turborepo monorepos put all apps in one repo"
User's constraint: "Each customer needs their own repo"
Conflict: Standard pattern assumes shared ownership; user needs isolation
```

### Pattern Verification Checklist

Before recommending a standard pattern:

- [ ] Identified the pattern explicitly ("I'm applying the X pattern")
- [ ] Listed the pattern's assumptions
- [ ] Checked assumptions against user's constraints
- [ ] Noted any conflicts or modifications needed
- [ ] Stated the recommendation WITH the constraint verification visible

---

## Gate Bypass (When to Skip)

The gate can be bypassed when:

1. **User explicitly requests** - "Just give me the standard approach"
2. **Already verified** - Same recommendation, constraints unchanged
3. **Trivial decisions** - Tier 2 refinements that can't violate constraints

**Even when bypassed, stay alert.** If something feels off, re-engage the gate.

---

## Conflict Resolution

When the gate detects a conflict:

### Option 1: Adjust the Recommendation
Find an alternative that honors the constraint.

> "Standard monorepos won't work here. Instead, let's use a template repo that generates separate customer repos."

### Option 2: Surface the Tradeoff
If no good alternative exists, be explicit.

> "The standard approach conflicts with H1. We could either:
> A) Modify H1 to allow shared infrastructure
> B) Accept more complexity with separate repos
> Which direction should we go?"

### Option 3: Challenge the Constraint
If the constraint seems problematic, revisit it.

> "I'm finding that H1 (separate repos) is making this much harder. Was there a specific reason for that constraint? Would [alternative] address the underlying concern?"

**NEVER silently violate the constraint.** Always surface the conflict.

---

## Visible Verification

Make the gate VISIBLE to the user. This builds trust and catches errors.

### Good (Visible)
> "Given your constraint that each customer needs their own repo (H1), I recommend a template approach rather than a shared monorepo. Here's why this fits..."

### Bad (Invisible)
> "I recommend a template approach. Here's how it works..."

The second version hides the reasoning. The user can't verify that Claude considered their constraints.

---

## Integration with Self-Challenge

The Verification Gate checks STATED constraints.
The Self-Challenge Trigger checks UNSTATED assumptions.

Together they cover:
- Things the user said (Verification Gate)
- Things Claude is assuming (Self-Challenge)

See `self-challenge.md` for the complementary mechanism.
