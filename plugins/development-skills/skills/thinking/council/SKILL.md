---
name: council
description: Multi-agent debate with visible transcripts where specialized agents respond to each other. USE WHEN council, debate, perspectives, weigh options, deliberate, multiple viewpoints, collaborative critique. Collaborative-adversarial — use Red Team for purely adversarial attack.
---

# Council

Multi-agent debate system where specialized agents discuss topics in rounds, respond to each other's points, and surface insights through intellectual friction.

**Key Differentiator from Red Team:** Council is collaborative-adversarial (debate to find best path). Red Team is purely adversarial (attack the idea). Council produces visible conversation transcripts; Red Team produces steelman + counter-argument.

## Workflow Routing

| Trigger | Workflow |
|---------|----------|
| Full structured debate (3 rounds, visible transcript) | `workflows/Debate.md` |
| Quick consensus check (1 round, fast) | `workflows/Quick.md` |
| Pure adversarial analysis | Red Team mode |

## Quick Reference

| Workflow | Purpose | Rounds | Output |
|----------|---------|--------|--------|
| **Debate** | Full structured discussion | 3 | Complete transcript + synthesis |
| **Quick** | Fast perspective check | 1 | Initial positions only |

## Context Files

| File | Content |
|------|---------|
| `CouncilMembers.md` | Agent roles, perspectives, voice mapping |
| `RoundStructure.md` | Three-round debate structure and timing |
| `OutputFormat.md` | Transcript format templates |

## Core Philosophy

**Origin:** Best decisions emerge from diverse perspectives challenging each other. Not just collecting opinions — genuine intellectual friction where experts respond to each other's actual points.

**Speed:** Parallel execution within rounds, sequential between rounds. A 3-round debate of 4 agents = 12 agent calls but only 3 sequential waits. Complete in 30-90 seconds.

## Examples

```
"Council: Should we use WebSockets or SSE?"
→ Invokes Debate workflow → 3-round transcript

"Quick council check: Is this API design reasonable?"
→ Invokes Quick workflow → Fast perspectives

"Council with security: Evaluate this auth approach"
→ Debate with Security agent added
```

## Integration

**Works well with:**
- **Red Team** — Pure adversarial attack after collaborative discussion
- **Before major architectural decisions** — Surface concerns early
- **Research** — Gather context before convening the council

## Best Practices

1. Use Quick for sanity checks, Debate for important decisions
2. Add domain-specific experts as needed (security for auth, etc.)
3. Review the transcript — insights are in the responses, not just positions
4. Trust multi-agent convergence when it occurs
