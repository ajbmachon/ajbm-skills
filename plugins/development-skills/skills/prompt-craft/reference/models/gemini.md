# Google Gemini

## Gemini 3.1 Pro (Current Flagship)

**Context:** 1M | **Max Output:** 64K
**Pricing:** $2.00/M input, $8.00/M output

### Three-Tier Thinking System

| `thinking_level` | Use Case | Latency |
|-------------------|----------|---------|
| `LOW` | Quick responses, routine queries | Fastest |
| `MEDIUM` | Balanced cost/performance | Moderate |
| `HIGH` | Complex reasoning, multi-step problems | Slowest |

```
# Quick tasks: thinking_level: "LOW" + system instruction: "think silently"
# Balanced: thinking_level: "MEDIUM"
# Complex: thinking_level: "HIGH" + simplified prompts
```

### Critical Prompting Rules

#### Temperature MUST be 1.0
Google strongly recommends default temperature of 1.0 for Gemini 3. Setting below 1.0 "may lead to unexpected behavior, looping, or degraded performance, particularly with complex mathematical or reasoning tasks." This is a **hard rule**.

#### Prompt Structure (Placement Matters)
- Place core requests and critical restrictions as the **final line**
- Order: context -> main task -> constraints (negative last)

#### Avoid Overly Broad Constraints
```
# BAD: "Do not infer. Do not guess." (breaks logic)
# GOOD: "Perform calculations based strictly on provided text."
```
The model may fail basic logic/arithmetic if given blanket "do not infer" instructions.

#### Grounding
Explicitly state provided context is "the only source of truth." Model may revert to training data without explicit anchoring.

#### Communication Style
Gemini 3 defaults to less verbose, direct responses. For conversational tone, explicitly request it.

### New Capabilities (3.0+)
- 2M token context window (3.0)
- Native 3D understanding
- Advanced parallel + nested tool use
- ~1.5s median latency

---

## Gemini 2.0 (Legacy)

For long contexts, place the question LAST:
```
[All context / documents]
...
Based on the information above, answer: [question]
```

Temperature 0 works for deterministic output (unlike Gemini 3).

---

## Quick Reference

| Model | CoT Prompting | Few-Shot | System Prompt |
|-------|---------------|----------|---------------|
| Gemini 3.1 Pro | Thinking mode (low/medium/high) | Helpful (no negatives) | Yes |
| Gemini 3.0 | Thinking mode (`thinking_level`) | Helpful (no negatives) | Yes |
| Gemini 2.0 | Manual/Thinking | Helpful (no negatives) | Yes |

---

*Last updated: February 2026*
