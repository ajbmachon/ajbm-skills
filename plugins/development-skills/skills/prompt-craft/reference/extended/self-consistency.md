# Self-Consistency

Generate multiple samples, select by majority vote. Improves reliability.

## Quick Summary

**Impact:** +5-10% accuracy, +80% confidence in correct answers
**When to use:** Tasks with verifiable correct answers, when reliability > speed
**Mechanism:** Multiple independent generations; consensus reduces random errors

## The Pattern

```
Generate [N] independent answers to this question.
Do not let previous answers influence subsequent ones.

Answer 1: [Generate]
Answer 2: [Generate]
Answer 3: [Generate]

Final answer: [Majority vote or consensus]
```

## Example

### Question
"What is 15% of 340?"

### Self-Consistency Approach
```
Generate 5 independent calculations:

Attempt 1: 340 × 0.15 = 51 ✓
Attempt 2: 340 × 15/100 = 51 ✓
Attempt 3: 34 × 1.5 = 51 ✓
Attempt 4: 340 × 0.15 = 51 ✓
Attempt 5: 340/100 × 15 = 51 ✓

Consensus: 51 (5/5 agreement)
Confidence: Very High
```

### With Disagreement
```
Attempt 1: 51
Attempt 2: 51
Attempt 3: 51
Attempt 4: 34 (error)
Attempt 5: 51

Consensus: 51 (4/5 agreement)
Note: Attempt 4 appears to have made an arithmetic error.
```

## Implementation Options

### Option 1: Within-Prompt
```
Calculate the answer 3 times using different approaches.
Then select the most consistent result.
```

### Option 2: Multi-Call with Temperature
Make N API calls with temperature > 0, then aggregate.

### Option 3: Hybrid
```
First, generate your answer.
Then, verify it by recalculating using a different method.
If they match, output the answer.
If they differ, explain the discrepancy and determine which is correct.
```

## When to Use

- Math problems
- Logic puzzles
- Factual questions with verifiable answers
- High-stakes decisions where reliability matters
- Code that can be verified multiple ways

## When NOT to Use

- Creative tasks (no "correct" answer)
- Speed-critical applications (multiple generations slow)
- Highly constrained outputs (will generate same answer anyway)
- Tasks with high token cost per generation

## Tips

- Use temperature > 0 for genuine diversity (if multi-call)
- 3-5 samples usually sufficient; diminishing returns beyond
- Weight by confidence if outputs include confidence scores
- Use for verification even if not full consensus protocol
