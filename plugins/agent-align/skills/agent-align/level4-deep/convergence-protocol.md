# Convergence Protocol

How to detect when the AI-to-AI interview is complete, without human convergence signals.

---

## The Problem

In human-AI interviews, convergence is signaled by the human: shorter answers, more confirmatory tone, no new constraints. In AI-to-AI, neither agent naturally "winds down." Without explicit termination rules, interviews either end too early (missing decisions) or run indefinitely.

---

## Termination Rules

### Minimum Rounds: 3
No termination before Round 3, regardless of apparent convergence. Early agreement is often shallow — important questions haven't been asked yet.

### Maximum Rounds: 12 (configurable)
Hard cap to prevent runaway interviews. If not converged by Round 12, compile what exists and note "interview capped — remaining gaps listed."

### Convergence Signals (ALL must be true)

| Signal | How to Check |
|---|---|
| **No new constraints** in last 2 rounds | Review working log — constraint registry unchanged for 2 rounds |
| **No new DEFERRED decisions** in last round | All recent decisions are DECIDED, not DEFERRED |
| **Spec section checklist complete** | Every major section of the target spec has at least one decision |
| **Follow-up debt cleared** | All flagged follow-ups from earlier rounds have been addressed |
| **Interviewer can write spec without guessing** | Interviewer self-assesses: "Could I compile the output spec right now without making assumptions?" |

### Early Termination Triggers
- Stakeholder explicitly signals: "All spec areas have been covered, I have no remaining ambiguities"
- Interviewer explicitly signals: "I have no remaining questions that would change the spec"
- Both agree in the same round → converged

---

## Convergence Check Procedure

The Orchestrator runs this check after each round:

1. Read the working log
2. Count rounds completed
3. If rounds < 3 → continue
4. If rounds >= 12 → terminate with "capped" note
5. Check all 5 convergence signals
6. If all true → trigger Phase 5 (Verification)
7. If not all true → continue to next round

---

## Anti-Premature-Convergence

The most dangerous failure mode is two AIs agreeing too quickly. Mitigations:

1. **Minimum 3 rounds is non-negotiable.** Even if both agents agree after Round 1.
2. **Spec section checklist must be explicitly enumerated** at the start of Phase 3. Sections not yet covered cannot be skipped.
3. **The Interviewer must ask at least one non-obvious question per round.** If all questions are surface-level, the interview isn't probing deep enough.
4. **The Stakeholder must flag at least one assumption per round.** If no assumptions surfaced, the audit isn't thorough enough.

---

## Convergence Report

When convergence is detected, the Orchestrator writes a brief convergence report to the working log:

```markdown
## Convergence Report
- **Rounds completed:** N
- **Total decisions:** N (HIGH: N, MEDIUM: N, DEFERRED: N)
- **Constraints captured:** N (Hard: N, Soft: N, Boundary: N)
- **Assumptions corrected:** N
- **Follow-ups resolved:** N/N
- **Convergence signals met:** [list which signals triggered]
- **Remaining gaps:** [any spec sections not fully covered]
```
