---
name: red-team
description: Adversarial analysis using parallel agents to find fatal flaws in arguments. Produces steelman plus counter-argument. USE WHEN red team, attack idea, counterarguments, critique, stress test, poke holes, devil's advocate, find weaknesses, break this, parallel analysis, adversarial validation.
---

# Red Team

Adversarial analysis using parallel agent deployment. Breaks arguments into atomic components, attacks from multiple expert perspectives (engineers, architects, pentesters, interns), synthesizes findings, and produces a strong counter-argument alongside a steelman representation.

## Workflow Routing

| Trigger | Workflow |
|---------|----------|
| Red team analysis (stress-test existing content) | `workflows/ParallelAnalysis.md` |
| Adversarial validation (produce new content via competition) | `workflows/AdversarialValidation.md` |

## Quick Reference

| Workflow | Purpose | Output |
|----------|---------|--------|
| **ParallelAnalysis** | Stress-test existing content | Steelman + Counter-argument (8 points each) |
| **AdversarialValidation** | Produce new content via competition | Synthesized solution from competing proposals |

**The Five-Phase Protocol (ParallelAnalysis):**
1. **Decomposition** — Break into 24 atomic claims
2. **Parallel Analysis** — Up to 32 agents examine strengths AND weaknesses
3. **Synthesis** — Identify convergent insights
4. **Steelman** — Strongest version of the argument
5. **Counter-Argument** — Strongest rebuttal

## Context Files

- `Philosophy.md` — Core philosophy, success criteria, agent types
- `Integration.md` — Skill integration, first principles usage, output format

## Examples

**Attack an architecture proposal:**
```
User: "red team this microservices migration plan"
→ workflows/ParallelAnalysis.md
→ Returns steelman + counter-argument (8 points each)
```

**Devil's advocate on a business decision:**
```
User: "poke holes in my plan to raise prices 20%"
→ workflows/ParallelAnalysis.md
→ Surfaces the core issue that could collapse the plan
```

**Adversarial validation for content:**
```
User: "battle of bots — which approach is better for this feature?"
→ workflows/AdversarialValidation.md
→ Synthesizes best solution from competing ideas
```
