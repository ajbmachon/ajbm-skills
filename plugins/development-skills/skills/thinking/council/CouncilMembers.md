# Council Members

Reference for council member roles and perspectives. Use whichever agent types your environment exposes via the Task tool — role descriptions here are the key guidance; exact agent naming can be adapted to your setup.

## Default Council Members

| Agent | Perspective |
|-------|-------------|
| **Architect** | System design, patterns, long-term implications |
| **Designer** | UX, user needs, accessibility |
| **Engineer** | Implementation reality, tech debt, maintenance |
| **Researcher** | Data, precedent, external examples |

## Optional Members

Add these as needed based on the topic:

| Agent | Perspective | When to Add |
|-------|-------------|-------------|
| **Security** | Risk, attack surface, compliance | Auth, data, APIs |
| **Fresh Eyes** | Naive questions, outside view | Complex UX, onboarding |
| **Writer** | Communication, documentation | Public-facing, docs |

## Custom Council Composition

- "Council with security" — Add a pentester/security-focused agent
- "Council with fresh eyes" — Add an agent prompted for outside perspective
- "Just architect and engineer" — Only specified members

## Agent Invocation

Spawn each member via the `Task` tool with a role-specific prompt describing that member's perspective and the council context. See `workflows/Debate.md` for prompt templates.
