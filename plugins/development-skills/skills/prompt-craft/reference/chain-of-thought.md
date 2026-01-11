# Chain-of-Thought (CoT)

Externalize reasoning steps before reaching a conclusion. The most impactful single technique for reasoning tasks.

## Table of Contents
1. [Mechanism](#mechanism)
2. [When to Use](#when-to-use)
3. [When NOT to Use](#when-not-to-use)
4. [Shallow vs Deep Examples](#shallow-vs-deep-examples)
5. [Common Mistakes](#common-mistakes)
6. [Self-Check](#self-check)
7. [Model-Specific Notes](#model-specific-notes)

---

## Mechanism

**Why it works:** LLMs generate tokens sequentially. By forcing intermediate reasoning tokens, you:
1. Give the model "working memory" in its output
2. Reduce the probability of skipping logical steps
3. Make errors visible and correctable
4. Allow complex problems to be solved incrementally

**The research:** Wei et al. (2022) showed +40% accuracy on arithmetic, commonsense, and symbolic reasoning tasks with CoT prompting. Kojima et al. (2022) found even "Let's think step by step" (zero-shot CoT) significantly improves performance.

**The mechanism in one sentence:** Reasoning in the output gives the model space to "think" rather than jumping directly to an answer.

---

## When to Use

- **Math and logic problems** - Multi-step calculations, proofs
- **Complex reasoning** - Any task requiring more than one logical step
- **Analysis tasks** - Breaking down arguments, evaluating evidence
- **Planning** - Step-by-step procedures, decision trees
- **Debugging** - Tracing through code or logic
- **Ambiguous problems** - Where the path to the answer isn't obvious

**Rule of thumb:** If a human would need scratch paper, use CoT.

---

## When NOT to Use

- **Simple factual retrieval** - "What's the capital of France?"
- **Classification with clear categories** - Binary yes/no, sentiment
- **Speed-critical applications** - CoT adds tokens and latency
- **Reasoning models (o1/o3, DeepSeek R1)** - They have built-in CoT; adding more hurts performance
- **Tasks where the answer is obvious** - Overthinking simple problems

**Warning:** For o1/o3 and DeepSeek R1, explicitly prompting for CoT *degrades* performance because these models already reason internally.

---

## Shallow vs Deep Examples

### Shallow (What to Avoid)

```
Prompt: "Solve this math problem step by step: If a train travels
at 60 mph for 2.5 hours, how far does it go?"

Response: "Step by step: 60 x 2.5 = 150 miles."
```

**Why it's shallow:**
- "Step by step" is present but there's only one step
- No actual reasoning decomposition
- Works for trivial problems but fails on complex ones

### Deep (What to Aim For)

```
Prompt: "A store sells apples for $1.50 each and oranges for $2.00 each.
Maria has $20 and wants to buy exactly 12 fruits. She wants at least
3 of each type. How many of each should she buy to minimize spending?

Before giving your answer, work through this systematically:
1. First, identify the constraints
2. Then, explore valid combinations
3. Calculate cost for each valid option
4. Select the minimum"

Response:
"Let me work through this systematically.

1. CONSTRAINTS:
   - Total fruits: exactly 12
   - At least 3 apples (a ≥ 3)
   - At least 3 oranges (o ≥ 3)
   - Budget: ≤ $20
   - a + o = 12

2. VALID COMBINATIONS (given a + o = 12 and both ≥ 3):
   - a=3, o=9
   - a=4, o=8
   - a=5, o=7
   - a=6, o=6
   - a=7, o=5
   - a=8, o=4
   - a=9, o=3

3. COSTS:
   - 3 apples + 9 oranges: $4.50 + $18.00 = $22.50 ❌ (over budget)
   - 4 apples + 8 oranges: $6.00 + $16.00 = $22.00 ❌
   - 5 apples + 7 oranges: $7.50 + $14.00 = $21.50 ❌
   - 6 apples + 6 oranges: $9.00 + $12.00 = $21.00 ❌
   - 7 apples + 5 oranges: $10.50 + $10.00 = $20.50 ❌
   - 8 apples + 4 oranges: $12.00 + $8.00 = $20.00 ✓
   - 9 apples + 3 oranges: $13.50 + $6.00 = $19.50 ✓

4. MINIMUM: 9 apples and 3 oranges at $19.50"
```

**Why it's deep:**
- Prompt provides explicit reasoning structure
- Each step has clear purpose
- Intermediate work is visible
- Errors would be easy to spot

---

## Common Mistakes

### 1. Using CoT on Reasoning Models
**Mistake:** Adding "think step by step" to o1, o3, or DeepSeek R1 prompts
**Problem:** These models already reason internally; explicit CoT interferes
**Fix:** For reasoning models, keep prompts simple and direct

### 2. Vague CoT Triggers
**Mistake:** "Think about this carefully"
**Problem:** Doesn't specify what kind of thinking or structure
**Fix:** Provide explicit structure: "First analyze X, then consider Y, finally conclude Z"

### 3. CoT for Simple Tasks
**Mistake:** "Think step by step about what the capital of France is"
**Problem:** Wastes tokens, adds latency, looks silly
**Fix:** Only use CoT when there are actually multiple steps

### 4. Not Verifying the Reasoning
**Mistake:** Assuming CoT output is correct because it shows work
**Problem:** Models can produce confident-looking but wrong reasoning
**Fix:** Pair with Self-Reflection or verify critical steps

### 5. Forgetting to Request the Final Answer
**Mistake:** Prompt triggers reasoning but doesn't ask for a conclusion
**Problem:** Model may just reason forever or stop mid-thought
**Fix:** Include "After your reasoning, provide your final answer clearly"

---

## Self-Check

Before using CoT, ask yourself:

- [ ] Does this task actually require multiple reasoning steps?
- [ ] Am I targeting a standard model (not o1/o3/R1)?
- [ ] Have I provided structure for the reasoning (not just "think step by step")?
- [ ] Have I asked for a final answer after the reasoning?
- [ ] Is the added latency acceptable for this use case?

---

## Model-Specific Notes

| Model | CoT Behavior |
|-------|--------------|
| **Claude 4.x** | Works well; can use extended thinking for complex problems |
| **GPT-4o** | Works well; standard CoT prompting |
| **o1/o3** | **Built-in - do NOT prompt for CoT** |
| **DeepSeek R1** | **Built-in - do NOT prompt for CoT** |
| **Gemini 2.0** | Works well; can enable thinking mode |
| **Kimi K2** | Automatic for K2-Thinking; standard for K2-Instruct |
| **Qwen 2.5** | Works well; include "step by step" for complex tasks |

---

## Variants

### Zero-Shot CoT
Just add "Let's think step by step" - surprisingly effective for many tasks.

### Few-Shot CoT
Provide examples that demonstrate the reasoning process:
```
Example: [Problem] → [Step 1] → [Step 2] → [Answer]
Now solve: [New problem]
```

### Structured CoT
Provide explicit sections:
```
Analyze this in three parts:
1. OBSERVATIONS: What do we know?
2. REASONING: What can we infer?
3. CONCLUSION: What's the answer?
```

---

**Impact:** +40% accuracy on reasoning tasks
**Cost:** Increased tokens, latency
**Best for:** Math, logic, analysis, planning, debugging
