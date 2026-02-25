# Verbalized Sampling

Generate multiple response variants with probability estimates. Combats mode collapse and surfaces non-obvious options.

## Mechanism

**Why it works:** RLHF training biases models toward "typical" responses. Forcing multiple variants breaks out of mode collapse. Probability estimates make uncertainty visible. Low-probability (tail) samples often contain novel insights.

**The research:** Verbalized sampling shows +1.6-2.1x diversity in outputs. Tail sampling specifically surfaces non-obvious options that would otherwise be suppressed by mode collapse.

## When to Use

- Brainstorming, analysis, creative tasks, decision support
- Debugging (multiple hypotheses for root cause)
- High-stakes outputs where missing an option is costly

**Rule of thumb:** If there's more than one valid answer, use verbalized sampling to see options.

## When NOT to Use

- Single correct answer tasks
- Speed-critical tasks or simple requests
- Highly constrained outputs with fixed format
- When the user wants one decisive recommendation

## Tail Sampling

A "tail sample" is a low-probability (p < 0.10) variant that the model would normally suppress. These often contain non-obvious insights, contrarian perspectives, creative alternatives, and challenges to premises.

RLHF pushes toward "typical" responses -- what most people would say, what feels safe. But the *best* response often isn't the typical one.

### Tail Sampling Questions by Domain

| Domain | Tail Prompt |
|--------|-------------|
| **Analysis** | "What interpretation would challenge conventional wisdom?" |
| **Strategy** | "What counterintuitive approach might actually work?" |
| **Debugging** | "What unlikely root cause would explain everything?" |
| **Creative** | "What unexpected angle hasn't been explored?" |
| **Decision** | "What option seems wrong at first but might be right?" |

## Deep Example

```
Prompt: "Analyze how to improve this code. Generate 3-4 variants
with probability estimates (how likely each is the best approach).
Include at least one low-probability but potentially high-value option."

Response:
"VARIANT 1 (p ~ 0.50) --------------------
Focus: Performance optimization
The nested loops create O(n^2) complexity. Replacing with a hashmap lookup
would reduce to O(n). This is likely the highest-impact change.

VARIANT 2 (p ~ 0.30) --------------------
Focus: Error handling
The function assumes valid input but will crash on null/undefined.
Adding defensive checks would improve reliability.

VARIANT 3 (p ~ 0.12) --------------------
Focus: API redesign
The function does too many things. Splitting into smaller, single-purpose
functions would improve testability and reusability.

VARIANT 4 (p ~ 0.08) * Tail ---------------
Focus: Delete and replace
This entire approach may be wrong. A reactive/event-driven architecture
might eliminate the need for this polling-based solution entirely.

======================================
TAIL INSIGHT: The low-probability variant challenges the premise.
Sometimes the best improvement is questioning whether the code
should exist in its current form at all."
```

## Best Pattern: Standard Verbalized Sampling

```
Analyze [topic].

Generate 3-5 variants with probability estimates (p ~ X.XX).
Include at least one low-probability (p < 0.10) tail sample marked with *.

Format:
VARIANT 1 (p ~ 0.XX)
[Analysis]

VARIANT N (p ~ 0.XX) * Tail
[Analysis]

TAIL INSIGHT: [What the tail sample reveals]
```

## Model-Specific Notes

| Model | Verbalized Sampling Notes |
|-------|--------------------------|
| **Claude** | Handles well; good at probability estimation |
| **GPT-5.x** | Works well; explicit template helps at lower reasoning effort |
| **o1/o3** | Can request; remember reasoning is internal |
| **DeepSeek** | Works; probability estimates may be less calibrated |
| **Gemini** | Works well; explicit format helps |
| **Kimi K2** | Works; keep format instructions clear |
| **Qwen** | Works; explicit template recommended |

---

**Impact:** +1.6-2.1x output diversity
**Cost:** Additional tokens for multiple variants
**Best for:** Brainstorming, analysis, decisions, debugging, creative tasks
