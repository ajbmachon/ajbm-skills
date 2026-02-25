# Chaining

Stage outputs feed into next stage. Enables complex workflows and error recovery.

## Quick Summary

**Impact:** Error recovery + specialization
**When to use:** Multi-stage workflows, complex transformations, refinement tasks
**Mechanism:** Each stage optimized independently; intermediate outputs enable validation

## The Pattern

```
Stage 1: [Task] -> [Output A]
Stage 2: Using [Output A], [Task] -> [Output B]
Stage 3: Using [Output B], [Task] -> [Final Output]
```

## Example Chains

### Research -> Analysis -> Synthesis
```
Chain 1: "Find key facts about [topic]" -> Facts list
Chain 2: "Using these facts, identify patterns" -> Analysis
Chain 3: "Using this analysis, write executive summary" -> Final output
```

### Draft -> Critique -> Revise
```
Chain 1: "Write initial version of [content]" -> Draft
Chain 2: "Review this draft. List improvements needed." -> Critique
Chain 3: "Revise this draft based on this feedback" -> Final version
```

## When to Use

- Tasks too complex for single prompt
- When intermediate validation is valuable
- Workflows with clear sequential dependencies

## When NOT to Use

- Simple tasks that don't benefit from staging
- Latency-critical tasks (chains add round-trips)
- Tightly coupled stages (might as well be one prompt)

## Agentic Pipeline Patterns

### Agent Handoff Template
When passing context between agents:
1. What was accomplished (not the full transcript)
2. What state exists (file paths, data structures)
3. What the next agent must NOT re-do
4. What constitutes completion for the next stage

### Multi-Context-Window Chaining
- Use structured state files (JSON > text) at each boundary
- Each new context starts by reading state, not resuming conversation
- Include a startup checklist: read state, verify environment, run baseline test
