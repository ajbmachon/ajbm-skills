# Reasoning-First

Present evidence before conclusions. Reduces hallucination and improves factual accuracy.

## Mechanism

**Why it works:** Forces the model to gather/state evidence before committing to a conclusion, making the reasoning chain visible and verifiable. Reduces "confident hallucination" where models state wrong answers confidently.

**The research:** Ordering evidence before conclusions reduces hallucination by 20-30% in factual tasks. Related to chain-of-thought but specifically about output structure.

## When to Use

- Factual questions with verifiable answers
- Analysis tasks where supporting reasoning matters
- High-stakes decisions and auditable outputs
- Claim verification and research synthesis

**Rule of thumb:** If the answer matters and could be wrong, require evidence first.

## When NOT to Use

- Creative tasks (stories don't need evidence chains)
- Simple factual retrieval ("What's 2+2?")
- Speed-critical applications
- **Reasoning models (o1/o3, DeepSeek R1)** -- they already do this internally

## Deep Example

```
Prompt: "Is this medication safe for pregnant women?

Before giving your conclusion:
1. State what evidence you have about this medication
2. Note any limitations or unknowns
3. Cite sources if available
4. Then provide your assessment with confidence level"

Response: "Let me examine the available evidence:

EVIDENCE:
- FDA Pregnancy Category B (animal studies show no risk; human studies insufficient)
- A 2019 cohort study (n=1,200) found no increased risk of birth defects
- Third-trimester use has limited data
- The medication does cross the placental barrier

LIMITATIONS:
- Long-term developmental effects not well-studied
- Sample sizes in studies are relatively small

SOURCES:
- FDA prescribing information
- Smith et al., Journal of Maternal Medicine, 2019

ASSESSMENT: Moderate confidence that this medication is likely safe for use
during pregnancy, particularly in the first two trimesters. Third-trimester
use should involve consultation with a healthcare provider."
```

**Why it works:** Evidence presented first, structured clearly. Limitations explicitly stated. Sources cited. Conclusion comes last with appropriate confidence level.

## Best Pattern: Evidence -> Conclusion Template

```
Before answering, structure your response as:

1. EVIDENCE: What facts are relevant?
2. SOURCES: Where does this information come from?
3. LIMITATIONS: What don't we know?
4. CONCLUSION: What can we conclude (with confidence level)?
```

## Model-Specific Notes

| Model | Reasoning-First Notes |
|-------|----------------------|
| **Claude** | Handles well; explicit structure helps |
| **GPT-5.x** | Use `reasoning.effort` to control; explicit templates at `none` effort |
| **o1/o3** | **Built-in** -- model reasons internally before answering |
| **DeepSeek R1** | **Built-in** -- reasoning visible in `reasoning_content` |
| **Gemini** | Works well; can use thinking mode |
| **Kimi K2** | K2-Thinking has built-in reasoning |
| **Qwen** | Standard implementation works |

---

**Impact:** -20-30% hallucination rate
**Cost:** Additional tokens for structure
**Best for:** Factual queries, analysis, high-stakes decisions, verification
