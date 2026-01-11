# Decomposition

Break complex tasks into sequential steps. Reduces errors on multi-part problems.

## Quick Summary

**Impact:** +25-40% on complex tasks
**When to use:** Tasks with multiple distinct phases or dependencies
**Mechanism:** Smaller steps are easier to execute correctly; errors don't compound

## The Pattern

```
Complete this task in stages:

Stage 1: [First subtask]
Stage 2: [Second subtask - may depend on Stage 1]
Stage 3: [Third subtask]

Complete each stage before moving to the next.
```

## Example

### Without Decomposition
```
"Write a blog post about AI safety, including research, outline, draft, and editing."
```

### With Decomposition
```
"Write a blog post about AI safety.

Stage 1 - Research: List 5 key AI safety concerns with brief descriptions
Stage 2 - Outline: Create a structure with intro, 3 main sections, conclusion
Stage 3 - Draft: Write the full post following your outline
Stage 4 - Edit: Review for clarity, remove jargon, add transitions

Complete each stage fully before starting the next."
```

## When to Use

- Multi-step processes with dependencies
- Complex analysis requiring distinct phases
- Tasks where partial results inform next steps
- Long-form content creation
- Problem-solving with research → analysis → solution pattern

## When NOT to Use

- Simple, atomic tasks
- When steps are truly independent (use parallel execution instead)
- Speed-critical tasks where decomposition adds overhead

## Tips

- Make dependencies explicit: "Using the results from Stage 1..."
- Allow for iteration: "If Stage 2 reveals issues, return to Stage 1"
- Consider natural breakpoints in the task
- Don't over-decompose simple tasks
