# Few-Shot Examples

Demonstrate the desired behavior through input-output examples. Anchors the model's output distribution.

## Table of Contents
1. [Mechanism](#mechanism)
2. [When to Use](#when-to-use)
3. [When NOT to Use](#when-not-to-use)
4. [Shallow vs Deep Examples](#shallow-vs-deep-examples)
5. [How Many Examples](#how-many-examples)
6. [Example Selection](#example-selection)
7. [Common Mistakes](#common-mistakes)
8. [Self-Check](#self-check)

---

## Mechanism

**Why it works:**
1. Examples demonstrate the transformation you want (input → output)
2. Models learn patterns from in-context demonstrations
3. Reduces ambiguity about format, style, and content expectations
4. Activates relevant knowledge through similar examples

**The research:** Brown et al. (2020) showed GPT-3's few-shot performance often approaches fine-tuned models. 2-5 examples typically provide most of the benefit.

**The mechanism in one sentence:** Examples show rather than tell, anchoring the model to produce similar outputs.

---

## When to Use

- **Format-specific tasks** - When output format is non-obvious
- **Style matching** - When tone/voice matters
- **Classification** - Show examples of each category
- **Transformation tasks** - Input → Output mappings
- **Domain-specific terminology** - Demonstrate correct usage
- **Ambiguous instructions** - Examples clarify intent

**Rule of thumb:** If you're struggling to describe what you want, show examples instead.

---

## When NOT to Use

- **Reasoning models (o1/o3, DeepSeek R1)** - Few-shot often degrades performance
- **Simple, clear tasks** - When zero-shot works fine
- **Highly variable outputs** - When examples might over-constrain
- **Token-limited contexts** - Examples consume tokens
- **Creative tasks** - May cause imitation rather than creation

**Critical warning:** For o1, o3, and DeepSeek R1, few-shot examples typically *hurt* performance. These models work best with zero-shot prompts.

---

## Shallow vs Deep Examples

### Shallow (What to Avoid)

```
Prompt: "Classify these emails as spam or not spam.

Example:
Input: Buy now! Limited time offer!
Output: spam

Now classify:
Input: Meeting rescheduled to 3pm tomorrow
Output:"
```

**Why it's shallow:**
- Only one example (not enough variety)
- Example is too obvious (doesn't show edge cases)
- No explanation of classification criteria
- Same structure could lead to pattern matching, not understanding

### Deep (What to Aim For)

```
Prompt: "Classify emails as 'spam' or 'legitimate'.

Consider: promotional language, urgency tactics, sender relationship,
and whether the content is expected/relevant to the recipient.

Examples:

Input: "URGENT: Your account will be suspended! Click here immediately
to verify your identity and avoid losing access."
Classification: spam
Reasoning: Fake urgency, threatening language, suspicious call-to-action

Input: "Hi team, reminder that quarterly reports are due by Friday.
Let me know if you need an extension."
Classification: legitimate
Reasoning: Normal business communication, known context, no pressure tactics

Input: "Congratulations! You've been selected for an exclusive offer.
Reply YES to claim your free gift card."
Classification: spam
Reasoning: Unsolicited offer, "selected" language, requests action for "free" item

Input: "Your Amazon order #123-456 has shipped. Track your package here:
[legitimate Amazon tracking link]"
Classification: legitimate
Reasoning: Expected transactional email, specific order reference, standard format

Now classify:
Input: "{new_email}"
Classification:"
```

**Why it's deep:**
- Multiple examples (4) showing variety
- Mix of spam and legitimate
- Includes reasoning to show criteria
- Edge cases represented (transactional emails)
- Clear instruction with evaluation criteria

---

## How Many Examples

| # Examples | Use Case |
|------------|----------|
| **0 (zero-shot)** | Clear tasks, reasoning models (o1/o3/R1), creative tasks |
| **1-2** | Simple format demonstration |
| **3-5** | Most tasks; optimal cost/benefit ratio |
| **5-10** | Complex classification with many categories |
| **10+** | Rarely needed; consider fine-tuning instead |

**Research finding:** Most benefit comes from the first 3-5 examples. Returns diminish rapidly after that.

---

## Example Selection

### Diversity Matters

**Bad:** 5 examples that are all similar
**Good:** 5 examples covering different cases, edge cases, and potential confusions

### Include Edge Cases

If users might submit ambiguous inputs, show how to handle them:
```
Input: "Not sure if interested"
Classification: uncertain
Note: When sentiment is mixed, classify as uncertain
```

### Match Expected Distribution

If 80% of real inputs will be Category A, don't show 5 examples of Category B.

### Order Can Matter

- For some models, later examples have slightly more influence
- Put your most representative example last
- If showing a sequence, order matters for pattern recognition

---

## Common Mistakes

### 1. Using Few-Shot on Reasoning Models
**Mistake:** Adding examples to o1/o3/DeepSeek R1 prompts
**Problem:** Degrades performance compared to zero-shot
**Fix:** Keep prompts simple and direct for reasoning models

### 2. Inconsistent Format Across Examples
**Mistake:**
```
Example 1: Input: X → Output: Y
Example 2: Given: A, Result: B
Example 3: X produces Y
```
**Problem:** Model confused about expected format
**Fix:** Use identical structure for all examples

### 3. Too Few Categories Represented
**Mistake:** 5 examples of "positive" sentiment, 0 of "negative"
**Problem:** Model biased toward shown category
**Fix:** Balance examples across categories

### 4. Examples Are Too Easy
**Mistake:** Only showing obvious cases
**Problem:** Model fails on edge cases
**Fix:** Include at least one challenging/ambiguous example

### 5. Examples Without Explanations
**Mistake:** Just input → output with no reasoning
**Problem:** Model might learn wrong patterns
**Fix:** Add brief reasoning when the "why" matters

### 6. Token Bloat
**Mistake:** 20 long examples eating up context
**Problem:** Less room for actual task; increased cost
**Fix:** Keep examples concise; use the minimum needed

---

## Self-Check

Before adding few-shot examples:

- [ ] Am I targeting a standard model (not o1/o3/R1)?
- [ ] Do I have 2-5 diverse examples?
- [ ] Is the format consistent across all examples?
- [ ] Are different categories/cases represented?
- [ ] Have I included at least one edge case?
- [ ] Are examples concise (not token-bloated)?
- [ ] Would zero-shot work just as well? (try it first)

---

## Patterns

### Pattern 1: Basic Few-Shot

```
Task description.

Example 1:
Input: {input1}
Output: {output1}

Example 2:
Input: {input2}
Output: {output2}

Now process:
Input: {new_input}
Output:
```

### Pattern 2: Few-Shot with Reasoning

```
Task description.

Example 1:
Input: {input1}
Reasoning: {why1}
Output: {output1}

Example 2:
Input: {input2}
Reasoning: {why2}
Output: {output2}

Now process:
Input: {new_input}
Reasoning:
Output:
```

### Pattern 3: Classification with All Categories

```
Classify text into: positive, negative, or neutral.

Positive example:
"This product exceeded my expectations!" → positive

Negative example:
"Terrible quality, complete waste of money." → negative

Neutral example:
"The product arrived on time and works as described." → neutral

Now classify:
"{new_text}" →
```

### Pattern 4: Format Demonstration

```
Convert the data into our standard format.

Example:
Raw: John Smith | 555-1234 | john@email.com
Formatted:
{
  "name": "John Smith",
  "phone": "555-1234",
  "email": "john@email.com"
}

Now convert:
Raw: {new_data}
Formatted:
```

---

## Model-Specific Notes

| Model | Few-Shot Behavior |
|-------|-------------------|
| **Claude 4.x** | Works well; 3-5 examples optimal |
| **GPT-4o** | Works well; consistent format important |
| **o1/o3** | **Avoid few-shot - hurts performance** |
| **DeepSeek R1** | **Avoid few-shot - degrades quality** |
| **DeepSeek V3** | Works normally |
| **Gemini** | Works well; avoid negative examples |
| **Kimi K2** | Works for K2-Instruct; varies for K2-Thinking |
| **Qwen** | Works well; keep examples concise |

---

**Impact:** +15-30% task specificity
**Cost:** Tokens for examples; may hurt reasoning models
**Best for:** Format matching, classification, transformation, style matching
