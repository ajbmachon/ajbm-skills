# Verbalized Sampling

Generate multiple response variants with probability estimates. Combats mode collapse and surfaces non-obvious options.

## Table of Contents
1. [Mechanism](#mechanism)
2. [When to Use](#when-to-use)
3. [When NOT to Use](#when-not-to-use)
4. [Shallow vs Deep Examples](#shallow-vs-deep-examples)
5. [Tail Sampling](#tail-sampling)
6. [Implementation Patterns](#implementation-patterns)
7. [Common Mistakes](#common-mistakes)
8. [Self-Check](#self-check)

---

## Mechanism

**Why it works:**
1. RLHF training biases models toward "typical" responses
2. Forcing multiple variants breaks out of the mode collapse
3. Probability estimates make the model's uncertainty visible
4. Low-probability (tail) samples often contain novel insights

**The research:** Verbalized sampling shows +1.6-2.1x diversity in outputs. Tail sampling specifically surfaces non-obvious options that would otherwise be suppressed by mode collapse.

**The mechanism in one sentence:** Requiring multiple variants with probabilities forces diversity and surfaces insights hidden by RLHF bias.

---

## When to Use

- **Brainstorming** - When you want diverse ideas
- **Analysis** - Multiple interpretations of data
- **Creative tasks** - Different approaches to a problem
- **Decision support** - Multiple options to consider
- **Debugging** - Multiple hypotheses for root cause
- **High-stakes outputs** - When missing an option is costly

**Rule of thumb:** If there's more than one valid answer, use verbalized sampling to see options.

---

## When NOT to Use

- **Single correct answer** - "What's 2+2?" doesn't need variants
- **Speed-critical tasks** - Multiple variants take more tokens/time
- **Simple requests** - Overhead not justified
- **Highly constrained outputs** - When format is fixed
- **User wants one recommendation** - Sometimes they want decisiveness

---

## Shallow vs Deep Examples

### Shallow (What to Avoid)

```
Prompt: "Give me 3 ways to improve this code."

Response:
"1. Add error handling
2. Improve variable names
3. Add comments"
```

**Why it's shallow:**
- Generic improvements anyone would suggest
- No probability estimates
- No indication of which matters most
- No novel/unexpected insights

### Deep (What to Aim For)

```
Prompt: "Analyze how to improve this code. Generate 3-4 variants
with probability estimates (how likely each is the best approach).
Include at least one low-probability but potentially high-value option."

Response:
"VARIANT 1 (p ≈ 0.50) ────────────────────
Focus: Performance optimization
The nested loops create O(n²) complexity. Replacing with a hashmap lookup
would reduce to O(n). This is likely the highest-impact change.

VARIANT 2 (p ≈ 0.30) ────────────────────
Focus: Error handling
The function assumes valid input but will crash on null/undefined.
Adding defensive checks would improve reliability.

VARIANT 3 (p ≈ 0.12) ────────────────────
Focus: API redesign
The function does too many things. Splitting into smaller, single-purpose
functions would improve testability and reusability.

VARIANT 4 (p ≈ 0.08) ⚡ Tail ─────────────
Focus: Delete and replace
This entire approach may be wrong. A reactive/event-driven architecture
might eliminate the need for this polling-based solution entirely.

═══════════════════════════════════════
TAIL INSIGHT: The low-probability variant challenges the premise.
Sometimes the best improvement is questioning whether the code
should exist in its current form at all."
```

**Why it's deep:**
- Multiple distinct approaches (not variations of one idea)
- Probability estimates show confidence distribution
- Tail sample surfaces non-obvious option
- Explicit insight about what the tail reveals

---

## Tail Sampling

### What It Is

A "tail sample" is a low-probability (p < 0.10) variant that the model would normally suppress. These often contain:

- Non-obvious insights
- Contrarian perspectives
- Creative alternatives
- Challenges to premises

### Why It Matters

RLHF training pushes models toward "typical" responses. The typical response is:
- What most people would say
- What the training data rewards
- What feels "safe"

But the *best* response often isn't the typical one.

### How to Request

```
Include at least one variant with p < 0.10 marked with ⚡.
This should be a less obvious option that might be unexpectedly valuable.
```

### Tail Sampling Questions by Domain

| Domain | Tail Prompt |
|--------|-------------|
| **Analysis** | "What interpretation would challenge conventional wisdom?" |
| **Strategy** | "What counterintuitive approach might actually work?" |
| **Debugging** | "What unlikely root cause would explain everything?" |
| **Creative** | "What unexpected angle hasn't been explored?" |
| **Decision** | "What option seems wrong at first but might be right?" |

---

## Implementation Patterns

### Pattern 1: Standard Verbalized Sampling

```
Analyze [topic].

Generate 3-5 variants with probability estimates (p ≈ X.XX).
Include at least one low-probability (p < 0.10) tail sample marked with ⚡.

Format:
VARIANT 1 (p ≈ 0.XX) ────────────────────
[Analysis]

VARIANT 2 (p ≈ 0.XX) ────────────────────
[Analysis]

VARIANT 3 (p ≈ 0.XX) ⚡ Tail ─────────────
[Analysis]

═══════════════════════════════════════
TAIL INSIGHT: [What the tail sample reveals]
```

### Pattern 2: With Grading Criteria

```
Generate variants and grade each on:
- Feasibility (1-5)
- Novelty (1-5)
- Impact (1-5)

VARIANT 1 (p ≈ 0.XX)
[Content]
Grade: Feasibility 4 | Novelty 2 | Impact 3

VARIANT 2 (p ≈ 0.XX)
[Content]
Grade: Feasibility 3 | Novelty 4 | Impact 4

...
```

### Pattern 3: Hypothesis Generation

```
What could explain [phenomenon]?

Generate multiple hypotheses with probability estimates.
Include at least one "unlikely but would explain everything" option.

H1 (p ≈ 0.XX): [Hypothesis]
Supporting evidence: [Evidence]
What would falsify it: [Falsification test]

H2 (p ≈ 0.XX): [Hypothesis]
...
```

### Pattern 4: Decision Options

```
We need to decide [decision].

Generate options with:
- Probability estimate (how likely this is the best choice)
- Key trade-offs
- What would make this the right choice

Option A (p ≈ 0.XX): [Option]
Trade-offs: [Trade-offs]
Best if: [Conditions]

...
```

---

## Common Mistakes

### 1. Variants Are Too Similar
**Mistake:** Three variants that are really one idea with minor tweaks
**Problem:** No real diversity; defeats the purpose
**Fix:** Require variants to address different aspects or take different approaches

### 2. Probabilities Don't Sum to ~1.0
**Mistake:** Three variants at p=0.40, 0.45, 0.50
**Problem:** Probabilities are just guesses, not calibrated
**Fix:** Instruct that probabilities should roughly sum to 1.0

### 3. No Tail Sample
**Mistake:** All variants are "safe" conventional options
**Problem:** Missing the potentially valuable non-obvious insight
**Fix:** Explicitly require one variant with p < 0.10

### 4. Tail Is Just "Wrong"
**Mistake:** Tail sample is genuinely bad, not valuably contrarian
**Problem:** Should be "unlikely but potentially right," not "just unlikely"
**Fix:** "Tail should be something that might be unexpectedly correct"

### 5. No Insight About the Tail
**Mistake:** Tail sample presented without explaining its value
**Problem:** User doesn't understand why it's included
**Fix:** Require "TAIL INSIGHT" explaining what the tail reveals

---

## Self-Check

Before requesting verbalized sampling:

- [ ] Is there genuinely more than one valid approach?
- [ ] Have I specified how many variants to generate?
- [ ] Have I requested probability estimates?
- [ ] Have I required at least one tail sample (p < 0.10)?
- [ ] Have I specified grading criteria (if relevant)?
- [ ] Have I asked for tail insight?

---

## Calibration

### What Good Probabilities Look Like

The model's probability estimates should reflect:
- **Relative confidence** between options
- **Rough magnitude** (not precise calibration)
- **Sum to ~1.0** across all variants

### Interpreting Probabilities

| Probability | Interpretation |
|-------------|----------------|
| p > 0.50 | Model's primary recommendation |
| p ≈ 0.20-0.40 | Strong alternative |
| p ≈ 0.10-0.20 | Worth considering |
| p < 0.10 | Tail / contrarian option |

### Improving Calibration

```
When estimating probabilities:
- Consider how often this approach would be correct across similar situations
- Ensure probabilities sum to approximately 1.0
- Don't cluster all probabilities in the same range
```

---

## Combining with Other Techniques

### With Self-Reflection

```
Generate 3 variants, then:
1. Critique each variant
2. Revise based on critique
3. Re-estimate probabilities
4. State final recommendation
```

### With Reasoning-First

```
For each variant:
1. State the evidence supporting it
2. Note limitations
3. Then give probability estimate
```

### With Few-Shot

```
Example variants for similar problem:
[Show example with good diversity]

Now generate variants for:
[Current problem]
```

---

## Model-Specific Notes

| Model | Verbalized Sampling Notes |
|-------|--------------------------|
| **Claude** | Handles well; good at probability estimation |
| **GPT-4o** | Works well; may need explicit template |
| **o1/o3** | Can request; remember reasoning is internal |
| **DeepSeek** | Works; probability estimates may be less calibrated |
| **Gemini** | Works well; explicit format helps |
| **Kimi K2** | Works; keep format instructions clear |
| **Qwen** | Works; explicit template recommended |

### Temperature Interaction

Higher temperature naturally increases diversity but doesn't:
- Provide probability estimates
- Guarantee tail sampling
- Structure the comparison

Verbalized sampling provides structured diversity even at low temperature.

---

## When Diversity Fails

If variants are too similar despite requesting diversity:

1. **Add dimension requirements:** "Each variant should differ in [X]"
2. **Specify approaches:** "Include at least one option that [contrarian approach]"
3. **Challenge premise:** "Include one option that questions whether this is the right problem"
4. **Increase temperature:** Combine with higher temp for more variation

---

**Impact:** +1.6-2.1x output diversity
**Cost:** Additional tokens for multiple variants
**Best for:** Brainstorming, analysis, decisions, debugging, creative tasks
