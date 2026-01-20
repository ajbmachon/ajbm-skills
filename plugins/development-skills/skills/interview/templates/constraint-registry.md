# Constraint Registry Template

Include this section in every spec produced by the interview skill.

---

## Template

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

---

## Example

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

---

## Usage Notes

1. **Capture at transition** - Fill this out when moving from Devil's Advocate to Partner
2. **Get confirmation** - User must confirm before proceeding
3. **Reference throughout** - Cite constraints when making recommendations
4. **Include in final spec** - This section makes specs auditable
5. **Update if constraints change** - Document mutations with reasons
