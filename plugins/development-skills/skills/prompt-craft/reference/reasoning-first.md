# Reasoning-First

Present evidence before conclusions. Reduces hallucination and improves factual accuracy.

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
1. Forces the model to gather/state evidence before committing to a conclusion
2. Makes the reasoning chain visible and verifiable
3. Reduces "confident hallucination" where models state wrong answers confidently
4. Allows early detection of flawed reasoning

**The research:** Ordering evidence before conclusions reduces hallucination by 20-30% in factual tasks. Related to chain-of-thought but specifically about output structure.

**The mechanism in one sentence:** Requiring evidence before answers forces grounded reasoning and makes errors visible.

---

## When to Use

- **Factual questions** - Questions with verifiable answers
- **Analysis tasks** - When supporting reasoning matters
- **High-stakes decisions** - Where errors have consequences
- **Auditable outputs** - When humans need to verify reasoning
- **Claim verification** - Checking if something is true
- **Research synthesis** - Combining multiple sources

**Rule of thumb:** If the answer matters and could be wrong, require evidence first.

---

## When NOT to Use

- **Creative tasks** - Stories don't need evidence chains
- **Simple factual retrieval** - "What's 2+2?" doesn't need preamble
- **Speed-critical applications** - Adds tokens and latency
- **Conversational flow** - Can feel pedantic in casual chat
- **Reasoning models** - o1/o3 already do this internally

---

## Shallow vs Deep Examples

### Shallow (What to Avoid)

```
Prompt: "Is this medication safe for pregnant women?"

Response: "Yes, this medication is generally considered safe for
pregnant women. Some studies have shown positive outcomes..."
```

**Why it's shallow:**
- Answer comes first (before evidence)
- Evidence is vague ("some studies")
- No sources cited
- Confident-sounding but unverifiable

### Deep (What to Aim For)

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
- However, third-trimester use has limited data
- The medication does cross the placental barrier

LIMITATIONS:
- Long-term developmental effects not well-studied
- Sample sizes in studies are relatively small
- Individual risk factors may vary

SOURCES:
- FDA prescribing information
- Smith et al., Journal of Maternal Medicine, 2019

ASSESSMENT: Moderate confidence that this medication is likely safe for use
during pregnancy, particularly in the first two trimesters. Third-trimester
use should involve consultation with a healthcare provider due to limited data.
I recommend discussing with a doctor who can evaluate individual circumstances."
```

**Why it's deep:**
- Evidence presented first, structured clearly
- Limitations explicitly stated
- Sources cited
- Conclusion comes last with appropriate confidence level
- Appropriate referral to professional

---

## Implementation Patterns

### Pattern 1: Evidence → Conclusion Template

```
Before answering, structure your response as:

1. EVIDENCE: What facts are relevant?
2. SOURCES: Where does this information come from?
3. LIMITATIONS: What don't we know?
4. CONCLUSION: What can we conclude (with confidence level)?
```

### Pattern 2: Claim Verification

```
Evaluate whether this claim is true:
"[claim to verify]"

Structure your response:
1. STATE the claim clearly
2. EXAMINE evidence for and against
3. NOTE any verification challenges
4. VERDICT: True / False / Uncertain (with explanation)
```

### Pattern 3: Comparative Analysis

```
Compare [X] and [Y].

Before recommending, present:
1. Key factors for comparison
2. How each option performs on each factor (with evidence)
3. Trade-offs between options
4. Your recommendation with reasoning
```

### Pattern 4: Show Your Work

```
[Question]

Show your work:
- What information do you need to answer this?
- What do you know about each piece?
- What are you uncertain about?
- Based on the above, what's your answer?
```

---

## Common Mistakes

### 1. Evidence After Conclusion
**Mistake:** "Yes. Here's why..."
**Problem:** Conclusion stated first can bias the following "evidence"
**Fix:** Explicitly require evidence before any conclusion

### 2. Vague Evidence
**Mistake:** "Studies show..." / "Research indicates..." / "Experts say..."
**Problem:** Not specific enough to verify
**Fix:** Request specific sources, dates, or findings

### 3. No Confidence Level
**Mistake:** Presenting uncertain conclusions as certain
**Problem:** All answers sound equally reliable
**Fix:** Require explicit confidence: "How confident are you?"

### 4. Forgetting Limitations
**Mistake:** Evidence → Conclusion (skipping unknowns)
**Problem:** Creates false sense of completeness
**Fix:** Include "Limitations" or "What I don't know" section

### 5. Mixing Evidence Types
**Mistake:** Treating opinions, studies, and anecdotes equally
**Problem:** Not all evidence is equally reliable
**Fix:** Categorize evidence by type and reliability

---

## Self-Check

Before sending:

- [ ] Have I asked for evidence before conclusions?
- [ ] Did I request sources or citations?
- [ ] Is there a place for limitations/uncertainties?
- [ ] Will the response include confidence levels?
- [ ] Is the structure explicit (not assumed)?

---

## Structured Templates

### Template A: Academic Style

```
Question: [question]

Please respond in this format:

BACKGROUND
[Relevant context and definitions]

EVIDENCE
[Key findings from reliable sources]

ANALYSIS
[What the evidence suggests]

LIMITATIONS
[Gaps, uncertainties, caveats]

CONCLUSION
[Answer with confidence level]

REFERENCES
[Sources cited]
```

### Template B: Quick Verification

```
Claim: [claim]

Respond with:
✓ EVIDENCE FOR: [supporting evidence]
✗ EVIDENCE AGAINST: [contradicting evidence]
? UNKNOWNS: [what we can't verify]
→ VERDICT: [true/false/uncertain] (confidence: high/medium/low)
```

### Template C: Decision Support

```
Question: Should we [decision]?

Analyze by:
1. PRO factors (with evidence)
2. CON factors (with evidence)
3. UNCERTAINTIES
4. RECOMMENDATION (with confidence and conditions)
```

---

## Combining with Other Techniques

### With Chain-of-Thought

```
Think through this step by step, but structure your answer as:
1. First, gather relevant information
2. Then, reason through what it implies
3. Note any uncertainties
4. Finally, state your conclusion
```

### With Self-Reflection

```
After reaching your initial conclusion:
1. Challenge your own reasoning
2. Consider what would change your mind
3. Revise if needed
4. State final answer with confidence
```

### With Structured Output

```json
{
  "evidence": ["fact1", "fact2"],
  "sources": ["source1", "source2"],
  "confidence": 0.8,
  "limitations": ["limitation1"],
  "conclusion": "answer"
}
```

---

## Model-Specific Notes

| Model | Reasoning-First Notes |
|-------|----------------------|
| **Claude** | Handles well; explicit structure helps |
| **GPT-4o** | Responds well; may need explicit template |
| **o1/o3** | **Built-in**—model reasons internally before answering |
| **DeepSeek R1** | **Built-in**—reasoning visible in `reasoning_content` |
| **Gemini** | Works well; can use thinking mode |
| **Kimi K2** | K2-Thinking has built-in reasoning |
| **Qwen** | Standard implementation works |

### For Reasoning Models (o1/o3, DeepSeek R1)

These models already reason before concluding. You don't need to prompt for it. However, you may still want to:
- Request specific evidence/sources
- Ask for confidence levels
- Structure the visible output

The internal reasoning happens automatically; you can structure the final output.

---

## Anti-Hallucination Effect

Reasoning-first is specifically effective against hallucination because:

1. **Harder to confabulate evidence** - Making up specific sources is harder than vague claims
2. **Visible reasoning chain** - Errors in logic become apparent
3. **Commitment delay** - Model doesn't commit to answer before checking
4. **Uncertainty surfaces** - "I don't know" becomes acceptable when structured

### Example Anti-Hallucination Prompt

```
I need accurate information about [topic].

Important:
- Only state facts you're confident about
- Cite sources when possible
- Clearly mark anything uncertain with [UNCERTAIN]
- If you don't know, say "I don't have reliable information about this"

Structure: Evidence first, then conclusion with confidence level.
```

---

**Impact:** -20-30% hallucination rate
**Cost:** Additional tokens for structure
**Best for:** Factual queries, analysis, high-stakes decisions, verification
