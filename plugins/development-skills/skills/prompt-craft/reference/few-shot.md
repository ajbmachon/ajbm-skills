# Few-Shot Examples

Demonstrate the desired behavior through input-output examples. Anchors the model's output distribution.

## Mechanism

**Why it works:** Examples demonstrate the transformation you want (input -> output). Models learn patterns from in-context demonstrations, reducing ambiguity about format, style, and content expectations.

**The research:** Brown et al. (2020) showed GPT-3's few-shot performance often approaches fine-tuned models. 2-5 examples typically provide most of the benefit.

## When to Use

- Format-specific tasks, style matching, classification
- Transformation tasks (input -> output mappings)
- Domain-specific terminology and ambiguous instructions

**Rule of thumb:** If you're struggling to describe what you want, show examples instead.

## When NOT to Use

- **Reasoning models (o1/o3, DeepSeek R1)** -- few-shot often **degrades** performance
- Simple, clear tasks where zero-shot works fine
- Highly variable outputs or creative tasks (may cause imitation)
- Token-limited contexts (examples consume tokens)

## How Many Examples

| # Examples | Use Case |
|------------|----------|
| **0 (zero-shot)** | Clear tasks, reasoning models (o1/o3/R1), creative tasks |
| **1-2** | Simple format demonstration |
| **3-5** | Most tasks; optimal cost/benefit ratio |
| **5-10** | Complex classification with many categories |

## Deep Example

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

**Why it works:** Multiple examples (4) showing variety, mix of spam and legitimate, includes reasoning to show criteria, edge cases represented (transactional emails).

## Example Selection

- **Diversity matters:** Cover different cases, edge cases, and potential confusions
- **Include edge cases:** Show how to handle ambiguous inputs
- **Match expected distribution:** If 80% of inputs are Category A, reflect that
- **Order can matter:** Put most representative example last

## Model-Specific Notes

| Model | Few-Shot Behavior |
|-------|-------------------|
| **Claude 4.x** | Works well; 3-5 examples optimal |
| **GPT-5.x** | Helpful at `none`/`low` reasoning effort; less needed at `medium+` |
| **o1/o3** | **Avoid few-shot -- hurts performance** |
| **DeepSeek R1** | **Avoid few-shot -- degrades quality** |
| **DeepSeek V3** | Works normally |
| **Gemini** | Works well; avoid negative examples |
| **Kimi K2** | Works for K2-Instruct; varies for K2-Thinking |
| **Qwen** | Works well; keep examples concise |

---

**Impact:** +15-30% task specificity
**Cost:** Tokens for examples; may hurt reasoning models
**Best for:** Format matching, classification, transformation, style matching
