# Self-Reflection

Ask the model to critique and revise its own output. Improves accuracy and catches errors.

## Table of Contents
1. [Mechanism](#mechanism)
2. [When to Use](#when-to-use)
3. [When NOT to Use](#when-not-to-use)
4. [Shallow vs Deep Examples](#shallow-vs-deep-examples)
5. [Implementation Patterns](#implementation-patterns)
6. [Common Mistakes](#common-mistakes)
7. [Self-Check](#self-check)

---

## Mechanism

**Why it works:**
1. Second pass catches errors missed in first generation
2. Critique activates different evaluation pathways than generation
3. Revision allows correction without starting over
4. Makes model's uncertainty visible through self-identified issues

**The research:** Self-reflection shows +15-25% accuracy improvement, especially on tasks where initial answers are often wrong. Works best when the critique is genuine (not rubber-stamping).

**The mechanism in one sentence:** Having the model review its own work catches errors that slip through in initial generation.

---

## When to Use

- **High-stakes outputs** - Where errors have real consequences
- **Complex reasoning** - Multi-step problems prone to mistakes
- **Code generation** - Catch bugs before returning
- **Factual claims** - Verify accuracy
- **Writing tasks** - Improve quality through revision
- **Ambiguous inputs** - Check interpretation

**Rule of thumb:** If you'd ask a human to double-check their work, ask the model to self-reflect.

---

## When NOT to Use

- **Simple tasks** - Overhead not justified
- **Speed-critical tasks** - Adds latency
- **High-temperature creative tasks** - Revision may bland-ify creativity
- **Tasks where first instinct is best** - Some intuitive tasks suffer from overthinking
- **When model is confidently wrong** - Same errors in reflection

---

## Shallow vs Deep Examples

### Shallow (What to Avoid)

```
Prompt: "Write some code, then check if it's correct."

Response:
"Here's the code:
```python
def factorial(n):
    return n * factorial(n-1)
```

Checking: Yes, this looks correct. It recursively calculates factorial."
```

**Why it's shallow:**
- "Check" is vague
- Reflection is superficial (rubber-stamping)
- Missing base case not caught
- No specific criteria for evaluation

### Deep (What to Aim For)

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
```python
def factorial(n):
    return n * factorial(n-1)
```

CRITIQUE:
1. Base case: ❌ MISSING - No base case, will recurse infinitely
2. Edge cases: ❌ MISSING - No handling for n=0 or n<0
3. Stack overflow: ⚠️ RISK - Deep recursion for large n
4. Efficiency: ⚠️ OK for small n, but recursive overhead

REVISED CODE:
```python
def factorial(n):
    if n < 0:
        raise ValueError('Factorial not defined for negative numbers')
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

CHANGES MADE:
- Added base case (n <= 1 returns 1)
- Added validation for negative input
- Note: For very large n, iterative version would be safer"
```

**Why it's deep:**
- Specific critique criteria provided
- Each criterion explicitly checked
- Issues identified and explained
- Code actually revised based on critique
- Remaining limitations noted

---

## Implementation Patterns

### Pattern 1: Generate → Critique → Revise

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

### Pattern 2: Red Team Yourself

```
[Complete the task]

Then attack your own response:
- What could be wrong?
- What did you assume that might not be true?
- What would a critic say?

Address any valid criticisms in a revised response.
```

### Pattern 3: Verification Checklist

```
[Complete the task]

Before finalizing, verify:
- [ ] All requirements addressed
- [ ] No logical errors
- [ ] Edge cases handled
- [ ] Format correct
- [ ] Sources accurate (if applicable)

Mark each item ✓ or ✗ with explanation. Fix any ✗ items.
```

### Pattern 4: Iterative Refinement

```
[Initial task]

After completing:
Pass 1: Check for factual errors
Pass 2: Check for logical errors
Pass 3: Check for completeness
Pass 4: Check for clarity

Refine after each pass if needed.
```

### Pattern 5: Devil's Advocate

```
[Make your argument/recommendation]

Now argue against yourself:
- What's the strongest counterargument?
- What evidence would change your mind?
- What are you most uncertain about?

Revise your recommendation considering these challenges.
```

---

## Common Mistakes

### 1. Rubber-Stamp Reflection
**Mistake:** "I checked my work and it looks good!"
**Problem:** Not actually critiquing; just confirming
**Fix:** Require specific criteria to check against

### 2. No Actual Revision
**Mistake:** Identifying issues but not fixing them
**Problem:** Critique without action is useless
**Fix:** Explicitly require fixes: "If issues found, revise"

### 3. Over-Reflection
**Mistake:** Three rounds of revision that bland-ify the output
**Problem:** Diminishing returns; can remove personality/creativity
**Fix:** One focused reflection pass is usually enough

### 4. Reflecting on Wrong Criteria
**Mistake:** Code review that checks grammar instead of bugs
**Problem:** Reflection misaligned with actual quality needs
**Fix:** Provide criteria specific to the task type

### 5. Confident Errors Survive
**Mistake:** Model confidently wrong in generation AND reflection
**Problem:** Same biases affect both passes
**Fix:** Use external verification for high-stakes; reflection isn't perfect

---

## Self-Check

Before requesting self-reflection:

- [ ] Have I provided specific criteria to check against?
- [ ] Is revision explicitly required (not just identification)?
- [ ] Are the criteria appropriate for this task type?
- [ ] Is one pass enough? (Usually yes)
- [ ] For high-stakes: Am I relying solely on self-reflection?

---

## Criteria by Task Type

### For Code

```
Critique checklist:
- [ ] Syntax correct
- [ ] Logic correct
- [ ] Edge cases handled
- [ ] Error handling present
- [ ] No security vulnerabilities
- [ ] Efficient (no obvious inefficiencies)
```

### For Writing

```
Critique checklist:
- [ ] Thesis/main point clear
- [ ] Arguments supported with evidence
- [ ] Flow logical
- [ ] No redundancy
- [ ] Tone appropriate
- [ ] Grammar/spelling correct
```

### For Analysis

```
Critique checklist:
- [ ] Data correctly interpreted
- [ ] Conclusions supported by evidence
- [ ] Alternative explanations considered
- [ ] Limitations acknowledged
- [ ] Confidence calibrated
```

### For Factual Claims

```
Critique checklist:
- [ ] Claims are accurate (to my knowledge)
- [ ] Sources cited where possible
- [ ] Uncertain claims marked
- [ ] No hallucinated specifics
- [ ] Appropriate caveats included
```

---

## Multi-Pass Strategies

### When to Use Multiple Passes

- Very complex tasks
- High-stakes outputs
- Multiple quality dimensions
- When first pass reflection was superficial

### Structured Multi-Pass

```
Pass 1 (Correctness): Are there any errors?
Pass 2 (Completeness): Is anything missing?
Pass 3 (Clarity): Could this be misunderstood?

[Apply each pass, revise as needed]
```

### Diminishing Returns

| Pass | Typical Improvement |
|------|---------------------|
| 1 | Significant (catches obvious errors) |
| 2 | Moderate (catches subtler issues) |
| 3+ | Minimal (may over-edit) |

Usually stop at 1-2 passes unless task is extremely high-stakes.

---

## Combining with Other Techniques

### With Chain-of-Thought

```
Think through the problem step by step.

Then review your reasoning:
- Is each step valid?
- Does the conclusion follow?

Revise any flawed steps.
```

### With Verbalized Sampling

```
Generate 3 variants.

For each variant:
1. Critique against criteria
2. Note strengths and weaknesses

Select the best variant and refine it.
```

### With Structured Output

```
Generate the JSON output.

Validate:
- Does it match the schema?
- Are all required fields present?
- Are values in expected ranges?

If invalid, fix and explain.
```

---

## Model-Specific Notes

| Model | Self-Reflection Notes |
|-------|----------------------|
| **Claude** | Good at genuine critique when prompted properly |
| **GPT-4o** | Works well; explicit criteria important |
| **o1/o3** | Reasons internally; can still add explicit verification step |
| **DeepSeek R1** | Already reflects in reasoning_content |
| **Gemini** | Works well; structured prompts help |
| **Kimi K2** | Self-correction smooth when prompted |
| **Qwen** | Standard implementation works |

### For Reasoning Models

o1/o3 and DeepSeek R1 already do internal reflection. You can still:
- Request explicit verification of specific criteria
- Ask for confidence levels
- Have them check specific types of errors

But the basic "think harder" benefit is already happening.

---

## When Self-Reflection Isn't Enough

Self-reflection has limits:

1. **Systematic biases** - Same bias in generation and critique
2. **Knowledge gaps** - Can't catch errors about unknown facts
3. **Confident hallucinations** - May double-down on wrong answers

For high-stakes outputs, combine self-reflection with:
- External verification
- Human review
- Multiple independent generations
- Tool-based checking (linters, validators)

---

**Impact:** +15-25% accuracy improvement
**Cost:** Additional tokens for critique/revision
**Best for:** Complex reasoning, code, high-stakes outputs, verification
