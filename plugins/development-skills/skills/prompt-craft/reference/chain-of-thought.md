# Chain-of-Thought (CoT)

Externalize reasoning steps before reaching a conclusion. The most impactful single technique for reasoning tasks.

## Mechanism

**Why it works:** LLMs generate tokens sequentially. By forcing intermediate reasoning tokens, you give the model "working memory" in its output, reduce the probability of skipping logical steps, and make errors visible and correctable.

**The research:** Wei et al. (2022) showed +40% accuracy on arithmetic, commonsense, and symbolic reasoning tasks. Kojima et al. (2022) found even zero-shot CoT ("Let's think step by step") significantly improves performance.

## When to Use

- Math and logic problems (multi-step calculations, proofs)
- Complex reasoning (any task requiring more than one logical step)
- Analysis, planning, and debugging tasks
- Ambiguous problems where the path to the answer isn't obvious

**Rule of thumb:** If a human would need scratch paper, use CoT.

## When NOT to Use

- Simple factual retrieval ("What's the capital of France?")
- Classification with clear categories (binary yes/no, sentiment)
- Speed-critical applications (CoT adds tokens and latency)
- **Reasoning models (o1/o3, DeepSeek R1)** -- they have built-in CoT; adding more **hurts** performance
- Tasks where the answer is obvious (overthinking simple problems)

## Deep Example

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
   - At least 3 apples (a >= 3)
   - At least 3 oranges (o >= 3)
   - Budget: <= $20
   - a + o = 12

2. VALID COMBINATIONS (given a + o = 12 and both >= 3):
   - a=3, o=9 ... a=9, o=3

3. COSTS:
   - 3+9: $4.50 + $18.00 = $22.50 (over budget)
   - 4+8: $6.00 + $16.00 = $22.00 (over budget)
   ...
   - 8+4: $12.00 + $8.00 = $20.00 (within budget)
   - 9+3: $13.50 + $6.00 = $19.50 (within budget)

4. MINIMUM: 9 apples and 3 oranges at $19.50"
```

**Why it works:** Prompt provides explicit reasoning structure. Each step has clear purpose. Intermediate work is visible. Errors would be easy to spot.

## Model-Specific Notes

| Model | CoT Behavior |
|-------|--------------|
| **Claude 4.x** | Works well; can use extended thinking for complex problems |
| **GPT-5.x** | Works well; use `reasoning.effort` to control depth |
| **o1/o3** | **Built-in -- do NOT prompt for CoT** |
| **DeepSeek R1** | **Built-in -- do NOT prompt for CoT** |
| **Gemini 3.x** | Thinking mode (low/medium/high); simplify prompts at high |
| **Kimi K2** | Automatic for K2-Thinking; standard for K2-Instruct |
| **Qwen 3.5** | Hybrid thinking mode; automatic for complex tasks |

---

**Impact:** +40% accuracy on reasoning tasks
**Cost:** Increased tokens, latency
**Best for:** Math, logic, analysis, planning, debugging
