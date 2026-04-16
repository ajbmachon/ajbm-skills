# Decision Policy

Template document for the Stakeholder agent. Defines how decisions are made during AI-to-AI interviews. The user provides this alongside the spec/mandate, or the Stakeholder generates defaults.

---

## Purpose

In human-AI interviews, the human brings tacit knowledge, taste, and lived experience. In AI-to-AI, the Decision Policy is the substitute — it gives the Stakeholder agent a basis for making choices that would otherwise require human judgment.

---

## Template

```markdown
# Decision Policy: [Topic]

## Meta-Goals
What is this spec FOR?
- [ ] Production product
- [ ] Experiment / prototype
- [ ] Internal tool
- [ ] Learning exercise
- [ ] Other: ___

What is the primary optimization target?
- [ ] Correctness / reliability
- [ ] Speed of implementation
- [ ] User experience
- [ ] Performance / scale
- [ ] Simplicity / maintainability
- [ ] Other: ___

## Fidelity Policy
When the source spec and pragmatic simplicity conflict, which wins?

Value hierarchy (1 = highest priority):
1. ___
2. ___
3. ___
4. ___
5. ___

Example: For a "faithful digital replica of a paper planner":
1. Visual fidelity to original
2. Interaction ritual preservation
3. Input pragmatism (digital > paper where no fidelity cost)
4. Technical simplicity
5. Performance

## Decision Authority

### Evaluation Order

Check criteria in this order; stop at the first that produces an answer:

1. **Explicit spec text** — does the spec directly state the requirement? If yes, DECIDE [HIGH].
2. **Logical entailment from spec** — is the constraint a necessary consequence of what the spec states (e.g., "React app" entails JavaScript)? If yes, DECIDE [HIGH].
3. **Policy hierarchy** — does the value hierarchy produce a clear winner among the viable options? If yes, DECIDE [HIGH] or [MEDIUM] per the tier definitions below.
4. **Domain convention** — is there standard practice in the domain AND no spec contradiction? If yes, DECIDE [MEDIUM].
5. **None of the above** — DEFER [HUMAN].

### DECIDE with HIGH confidence when:
- The spec explicitly states the requirement
- The mandate logically entails the constraint (e.g., "React app" → must use JS)
- The decision policy's value hierarchy gives a clear winner
- Standard practice in the domain AND no spec contradiction

### DECIDE with MEDIUM confidence when:
- Reasonable inference from spec + policy, but assumption required
- Multiple valid approaches exist, one fits the value hierarchy better
- Domain convention applies but spec is silent

### DEFER to HUMAN when:
- Aesthetic/taste decision with no spec guidance
- Business context needed that's outside the spec
- Trade-off where the value hierarchy doesn't give a clear winner
- Meta-goal ambiguity (is this a product or a prototype?)

### Default Behaviors
- When ambiguous: [choose simpler option / choose spec-faithful option / flag and decide]
- When contradictory: [attempt resolution then surface]
- When novel (not in spec): [infer from fidelity policy / flag as new decision]

## Domain Context (optional)
Any additional context about the domain, team, constraints, or history that helps the Stakeholder make informed decisions.
```

---

## When No Policy Is Provided

If the user doesn't provide a Decision Policy, the Stakeholder generates defaults:

1. **Meta-goals:** Infer from the spec's tone and content. A spec with test criteria → production. A spec with "explore" language → prototype.
2. **Fidelity policy:** Default to `Correctness > Simplicity > Performance > UX > Speed`.
3. **Decision authority:** Use the standard tiers above. DEFER more aggressively when uncertain.
4. **Default behavior for ambiguity:** Flag and decide with MEDIUM confidence, noting the assumption.

The Stakeholder MUST announce these defaults in Phase 0 (ECHO) so the Interviewer can challenge them.
