# Self-Reflection

Ask the model to critique and revise its own output. Improves accuracy and catches errors.

## Mechanism

**Why it works:** Second pass catches errors missed in first generation. Critique activates different evaluation pathways than generation. Revision allows correction without starting over. Makes uncertainty visible through self-identified issues.

**The research:** Self-reflection shows +15-25% accuracy improvement, especially on tasks where initial answers are often wrong. Works best when the critique is genuine (not rubber-stamping).

## When to Use

- High-stakes outputs where errors have real consequences
- Complex reasoning (multi-step problems prone to mistakes)
- Code generation (catch bugs before returning)
- Factual claims and writing tasks

**Rule of thumb:** If you'd ask a human to double-check their work, ask the model to self-reflect.

## When NOT to Use

- Simple tasks (overhead not justified)
- Speed-critical tasks
- High-temperature creative tasks (revision may bland-ify creativity)
- When the model is confidently wrong (same errors in reflection)

## Deep Example

```
Prompt: "Write a factorial function in Python.

After writing, critique your code by checking:
1. Does it handle the base case(s)?
2. Does it handle edge cases (0, negative numbers)?
3. Could it cause stack overflow?
4. Is it efficient?

If you find issues, fix them and explain what you changed."

Response:
"Initial code:
def factorial(n):
    return n * factorial(n-1)

CRITIQUE:
1. Base case: MISSING - No base case, will recurse infinitely
2. Edge cases: MISSING - No handling for n=0 or n<0
3. Stack overflow: RISK - Deep recursion for large n
4. Efficiency: OK for small n, but recursive overhead

REVISED CODE:
def factorial(n):
    if n < 0:
        raise ValueError('Factorial not defined for negative numbers')
    if n <= 1:
        return 1
    return n * factorial(n - 1)

CHANGES MADE:
- Added base case (n <= 1 returns 1)
- Added validation for negative input
- Note: For very large n, iterative version would be safer"
```

**Why it works:** Specific critique criteria provided, each criterion explicitly checked, issues identified and explained, code actually revised based on critique, remaining limitations noted.

## Best Pattern: Generate -> Critique -> Revise

```
Task: [task]

Process:
1. Generate your initial response
2. Critique it against these criteria:
   - [Criterion 1]
   - [Criterion 2]
   - [Criterion 3]
3. If issues found, revise and explain changes
4. If no issues, confirm why it passes each criterion
```

## Limits of Self-Reflection

Self-reflection has limits:
1. **Systematic biases** -- same bias in generation and critique
2. **Knowledge gaps** -- can't catch errors about unknown facts
3. **Confident hallucinations** -- may double-down on wrong answers

For high-stakes outputs, combine with external verification, human review, or tool-based checking.

## Model-Specific Notes

| Model | Self-Reflection Notes |
|-------|----------------------|
| **Claude** | Good at genuine critique when prompted properly |
| **GPT-5.x** | Works well; explicit criteria important |
| **o1/o3** | Reasons internally; can still add explicit verification step |
| **DeepSeek R1** | Already reflects in reasoning_content |
| **Gemini** | Works well; structured prompts help |
| **Kimi K2** | Self-correction smooth when prompted |
| **Qwen** | Standard implementation works |

---

**Impact:** +15-25% accuracy improvement
**Cost:** Additional tokens for critique/revision
**Best for:** Complex reasoning, code, high-stakes outputs, verification
