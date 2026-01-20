# Working Log Template

**Purpose:** Progressive capture during interview. Claude writes to this file AS things happen, not at the end.

**Location:** Create at interview start. Ask user for location or use `./interview-log-{topic}.md`

---

## Template

```markdown
# Interview Working Log

**Topic:** [Brief description]
**Started:** [Date/time]
**Status:** IN PROGRESS | COMPLETE

---

## Constraint Registry

> Updated live as constraints emerge. This section is the source of truth.

### Hard Constraints (Immutable)

| # | Constraint | Source | Added |
|---|------------|--------|-------|
| H1 | [constraint] | [where it came from] | [when] |

### Soft Constraints (Preferences)

| # | Constraint | Negotiable If | Added |
|---|------------|---------------|-------|
| S1 | [constraint] | [condition] | [when] |

### Boundaries (Out of Scope)

| # | What's Excluded | Reason | Added |
|---|-----------------|--------|-------|

---

## Decisions Log

> User decisions captured as they're made.

| # | Decision | Options Considered | Rationale | When |
|---|----------|-------------------|-----------|------|
| D1 | [what was decided] | [alternatives] | [why this choice] | [timestamp] |

---

## Assumptions & Corrections

> Assumptions surfaced and how they were resolved.

| # | Original Assumption | Correction | Source |
|---|---------------------|------------|--------|
| A1 | [what Claude assumed] | [what user clarified] | [Q&A ref] |

---

## Interview Q&A

> Append each exchange as it happens.

### Q1: [Question text]
**Asked:** [timestamp]
**Answer:** [User's response]
**Follow-up needed:** Yes/No
**Constraints extracted:** [H#, S#, or none]
**Decisions made:** [D# or none]

---

### Q2: [Question text]
**Asked:** [timestamp]
**Answer:** [User's response]
**Follow-up needed:** Yes/No
**Constraints extracted:** [H#, S#, or none]
**Decisions made:** [D# or none]

---

[Continue appending Q&A entries...]

---

## Research Findings

> Logged when research completes (blocking or background).

### R1: [Research topic]
**Source:** [agent/tool used]
**File created:** [path to research report, if any - e.g., `docs/research/topic-research.md`]
**Finding:** [what was discovered]
**Impact:** [how it affects the interview - new constraint? contradiction?]

---

## Research Artifacts

> Index of all research files created during this interview.

| # | File Path | Created By | Topic | Phase |
|---|-----------|------------|-------|-------|
| 1 | [full path] | [main agent / subagent name] | [what it covers] | [which phase] |

---

## Phase Transitions

> Mark when moving between phases.

| Phase | Entered | Notes |
|-------|---------|-------|
| Research Foundation | [time] | |
| Devil's Advocate | [time] | |
| Constraint Capture | [time] | Constraints confirmed: [list] |
| Deep Interview | [time] | |
| Verification | [time] | |
| Output | [time] | |

---

## Notes

> Free-form observations during interview.

- [timestamp]: [observation]
```

---

## Usage Instructions

1. **At interview start:** Create this file, fill in topic and start time
2. **After EACH Q&A:** Append a new Q&A entry immediately
3. **When constraint emerges:** Add to Constraint Registry AND note in Q&A entry
4. **When decision made:** Add to Decisions Log AND note in Q&A entry
5. **When assumption corrected:** Add to Assumptions & Corrections
6. **When research completes:** Add to Research Findings with file path (if created)
7. **When any research file is created:** Add to Research Artifacts table with full path
8. **At phase transitions:** Update Phase Transitions table
9. **At interview end:** Mark status COMPLETE, use as input for final spec

## Why This Matters

- **Prevents drift:** Written record is harder to contradict than memory
- **Creates accountability:** User can see what's being captured
- **Feeds final spec:** All sections map directly to spec templates
- **Catches errors early:** User sees constraints as they're captured, can correct immediately
