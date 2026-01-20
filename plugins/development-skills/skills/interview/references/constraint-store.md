# Constraint Store

The Constraint Store captures immutable constraints established during Devil's Advocate phase and enforces them throughout Partner phase.

---

## Purpose

Prevent "helpful assistant drift" where Claude fills in architecture details that contradict user's stated constraints.

**The problem it solves:** Claude understood "separate customer repos" in Devil's Advocate, agreed with it, then explained a monorepo pattern that put all customers in one repo - contradicting the constraint.

---

## When to Capture

**Trigger:** End of Devil's Advocate phase, when transitioning to Partner.

After the user has successfully defended their idea, BEFORE saying "This idea has merit":

1. Extract all constraints that emerged from the challenge
2. Validate for internal consistency
3. Display to user for confirmation
4. Store for reference throughout Partner phase

---

## What to Capture

### Hard Constraints (Immutable)
Things that CANNOT be violated. If a solution violates these, it's wrong.

Examples:
- "Each customer must have their own separate repository"
- "No third-party services - must be self-hosted"
- "Team of 2 developers - no complex tooling"
- "Must work offline"

### Soft Constraints (Preferences)
Things the user prefers but could negotiate if necessary.

Examples:
- "Prefer TypeScript over JavaScript"
- "Would like to use Tailwind"
- "Hoping to deploy to Vercel"

### Boundaries (Scope Limits)
What's explicitly OUT of scope.

Examples:
- "Not handling authentication - using existing system"
- "Only supporting English for now"
- "Desktop only, no mobile"

---

## Constraint Format

```markdown
## 🔒 CONSTRAINT REGISTRY

**Captured:** [timestamp]
**Source:** Devil's Advocate phase

### Hard Constraints (Immutable)
| # | Constraint | Source | Established |
|---|------------|--------|-------------|
| H1 | [constraint text] | User stated | [when in conversation] |
| H2 | [constraint text] | User defended | [when in conversation] |

### Soft Constraints (Preferences)
| # | Constraint | Source | Negotiable If |
|---|------------|--------|---------------|
| S1 | [constraint text] | User stated | [condition] |

### Boundaries (Out of Scope)
| # | What's Excluded | Reason |
|---|-----------------|--------|
| B1 | [exclusion] | [why] |

---
**User confirmed:** ☐ Yes / ☐ No (with corrections)
```

---

## Validation Rules

Before storing, check for:

### Internal Consistency
Constraints should not contradict each other.

❌ "Must be simple" + "Must handle every edge case"
❌ "Team of 2" + "Microservices architecture"
❌ "No external dependencies" + "Use AWS Lambda"

**If contradiction detected:** Surface it to user, require resolution before proceeding.

### Completeness
Key architectural constraints should be captured:
- Deployment model (single tenant vs multi-tenant)
- Team size / maintenance capacity
- Integration requirements
- Performance requirements
- Security requirements

**If missing:** Ask explicitly before proceeding to Partner phase.

---

## Display Protocol

### At Partner Phase Transition
Show the full Constraint Registry and require acknowledgment:

> "Before we proceed, here are the constraints I'll honor throughout our discussion:
>
> **Hard Constraints:**
> - H1: Each customer gets their own separate repository
> - H2: Team of 2 developers
>
> **Soft Constraints:**
> - S1: Prefer TypeScript
>
> Is this complete and accurate?"

### Before Major Structural Decisions
Reference relevant constraints:

> "Given constraint H1 (separate customer repos), I recommend..."

### When Constraint Might Be Violated
STOP and surface explicitly:

> "Wait - this approach might conflict with constraint H1 (separate customer repos). Let me reconsider."

---

## Mutation Rules

Constraints CAN be changed, but only with explicit acknowledgment:

### To Add a Constraint
```
User: "Oh, I forgot to mention - it also needs to work offline."
Claude: "Adding to Hard Constraints: H3 - Must work offline. This might affect earlier recommendations. Let me check..."
```

### To Remove/Modify a Constraint
```
User: "Actually, separate repos is negotiable if there's a good reason."
Claude: "Moving H1 from Hard to Soft Constraints. This opens up additional options. The monorepo pattern could now work if [conditions]."
```

### To Override a Constraint
```
User: "I know I said team of 2, but we might hire. Ignore that constraint."
Claude: "Removing H2. Noted that team size is flexible. This affects complexity recommendations."
```

**NEVER silently ignore a constraint.** Always acknowledge and document changes.

---

## Error Recovery

When Claude realizes it violated a constraint:

1. **Stop immediately** - Don't continue down wrong path
2. **Acknowledge explicitly** - "That recommendation conflicts with constraint H1"
3. **Explain the conflict** - Why the recommendation violates the constraint
4. **Re-approach** - "Let me reconsider with H1 in mind..."
5. **Offer alternative** - That honors the constraint

**Example:**
> "Wait - I just recommended a monorepo structure, but constraint H1 says each customer needs their own repo. That's a conflict. Let me re-approach: instead of apps living in one monorepo, we need a template that generates separate repos. Here's how that would work..."

---

## Integration with Verification Gate

The Constraint Store feeds into the Verification Gate. Before any recommendation:

1. Gate checks: "Is this a major structural decision?"
2. If yes: "Which constraints are relevant?"
3. Display: "Given constraints [X, Y], I recommend [Z] because..."

See `verification-gate.md` for the full gate protocol.
