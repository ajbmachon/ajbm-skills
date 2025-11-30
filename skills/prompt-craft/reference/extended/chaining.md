# Chaining

Stage outputs feed into next stage. Enables complex workflows and error recovery.

## Quick Summary

**Impact:** Error recovery + specialization
**When to use:** Multi-stage workflows, complex transformations, refinement tasks
**Mechanism:** Each stage can be optimized independently; intermediate outputs enable validation

## The Pattern

```
Stage 1: [Task] → [Output A]
↓
Stage 2: Using [Output A], [Task] → [Output B]
↓
Stage 3: Using [Output B], [Task] → [Final Output]
```

## Example Chains

### Research → Analysis → Synthesis
```
Chain 1 - Research: "Find key facts about [topic]"
→ Facts list

Chain 2 - Analysis: "Using these facts: [facts list], identify patterns and insights"
→ Analysis

Chain 3 - Synthesis: "Using this analysis: [analysis], write executive summary"
→ Final output
```

### Draft → Critique → Revise
```
Chain 1 - Draft: "Write initial version of [content]"
→ Draft

Chain 2 - Critique: "Review this draft: [draft]. List improvements needed."
→ Critique

Chain 3 - Revise: "Revise this draft: [draft] based on this feedback: [critique]"
→ Final version
```

### Extract → Transform → Format
```
Chain 1 - Extract: "Extract structured data from: [raw text]"
→ JSON data

Chain 2 - Transform: "Using this data: [JSON], calculate [metrics]"
→ Calculated metrics

Chain 3 - Format: "Format these metrics: [metrics] as a report"
→ Final report
```

## Implementation Options

### Option 1: Sequential Prompts (Manual)
Send each stage as a separate API call, feeding output into next input.

### Option 2: Single Prompt with Stages
```
Complete this in stages:

Stage 1: [Task 1]
[Space for output]

Stage 2: Using your Stage 1 output, [Task 2]
[Space for output]

Stage 3: Using your Stage 2 output, [Task 3]
[Space for output]
```

### Option 3: Tool-Based Chaining
Use function calling to trigger stages, with outputs passed between calls.

## When to Use

- Tasks too complex for single prompt
- When intermediate validation is valuable
- Workflows with clear sequential dependencies
- Error recovery (can retry from failed stage)

## When NOT to Use

- Simple tasks that don't benefit from staging
- When latency is critical (chains add round-trips)
- Tightly coupled stages (might as well be one prompt)

## Tips

- Keep intermediate outputs structured (easier to pass forward)
- Include context about what was done in previous stages
- Design recovery points: What if Stage 2 fails?
- Consider parallel chains for independent subtasks
