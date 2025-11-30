# Sufficiency

Provide all information the model can't infer. Reduces hallucination from missing context.

## Quick Summary

**Impact:** Significant hallucination reduction
**When to use:** Domain-specific tasks, proprietary information, non-public facts
**Mechanism:** Model can only work with what's in context; missing info gets hallucinated

## The Pattern

```
Context you need to complete this task:
- [Specific fact 1]
- [Specific fact 2]
- [Domain-specific term definition]

If you need information not provided above, say so rather than guessing.
```

## What Models Can't Infer

| They Know | They Don't Know |
|-----------|-----------------|
| Public facts (pre-cutoff) | Proprietary data |
| Common knowledge | Your company's specifics |
| General patterns | Recent events |
| Standard definitions | Internal terminology |
| Published research | Your preferences |

## Example

### Insufficient Context
```
"Write an email to John about the project delay."
```
Model must guess: Who is John? What project? What's the relationship? What tone?

### Sufficient Context
```
"Write an email to John Chen (our VP of Engineering, direct report relationship,
prefers concise communication) about the 2-week delay in Project Aurora
(our Q1 priority, originally due Jan 15). Cause: dependency on external API
not yet available. Tone: professional, solution-focused."
```

## Checklist for Sufficiency

Before sending, verify you've provided:

- [ ] **Who**: Relevant people, roles, relationships
- [ ] **What**: Specific subject matter details
- [ ] **Why**: Context for decisions or situations
- [ ] **When**: Timeline, deadlines, sequence
- [ ] **Constraints**: Rules, limitations, requirements
- [ ] **Terminology**: Definitions for non-standard terms
- [ ] **Preferences**: Style, format, tone requirements

## When to Use

- Tasks involving proprietary or internal information
- Domain-specific content with jargon
- Any task where guessing would be harmful
- Personalized outputs requiring knowledge of preferences

## When NOT to Use

- General knowledge tasks
- When asking the model to use its own knowledge
- When exploration/creativity is desired

## The "Say So" Instruction

Always include an escape hatch:

```
If you need information I haven't provided, ask for clarification
rather than making assumptions.
```

This prevents confident hallucinations about missing details.
