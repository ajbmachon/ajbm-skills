# Google Gemini

## Gemini 3.1 Pro (Current Flagship)

**Released:** February 19, 2026
**Based on:** Gemini 3 Pro
**Context:** 1M tokens | **Max Output:** 64K tokens
**Pricing:** $2.00/M input, $8.00/M output (same as Gemini 3 Pro — free upgrade)

Google's most advanced reasoning model. Achieves ARC-AGI-2 score of 77.1% (vs 31.1% for 3.0 Pro).

### What Changed from Gemini 3.0

#### Three-Tier Thinking System (Key Innovation)
Previous Gemini 3 models had binary low/high thinking. 3.1 Pro introduces **medium** thinking level:

| `thinking_level` | Use Case | Latency |
|-------------------|----------|---------|
| `LOW` | Quick responses, routine queries | Fastest |
| `MEDIUM` | Balanced cost/performance tradeoff | Moderate |
| `HIGH` | Complex reasoning, multi-step problems | Slowest |

This gives developers fine-grained control over reasoning depth, effectively making 3.1 Pro a "Deep Think Mini" with adjustable reasoning on demand.

#### Other Improvements
- More efficient token usage and thinking across use cases
- Improved software engineering behavior and agentic capabilities
- Better agentic performance in finance and spreadsheet domains
- 64K output tokens (resolves 3.0 Pro's ~21K truncation issues in code generation)

### Prompting Rules (Same as Gemini 3 Series)

All Gemini 3 prompting rules apply:
- **Temperature:** KEEP at 1.0 (mandatory — see Gemini 3.0 section below)
- **Prompt structure:** Context → main task → constraints (negative last)
- **Avoid broad constraints:** "Do not infer" breaks logic; be specific instead
- **Grounding:** Explicitly state context is "the only source of truth"
- **Verbosity:** Defaults to direct responses; explicitly request conversational tone

#### Thinking Level Strategy for 3.1
```
# Quick tasks — minimize latency
thinking_level: "LOW" + system instruction: "think silently"

# Balanced — default for most applications
thinking_level: "MEDIUM"

# Complex reasoning — when accuracy matters most
thinking_level: "HIGH" + simplified prompts (let model reason internally)
```

**Sources:**
- Announcement: https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-pro
- Model card: https://deepmind.google/models/model-cards/gemini-3-1-pro/
- Vertex AI docs: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/3-1-pro

---

## Gemini 3.0

### Models & Specs

| Model | Context | Output | Key Feature |
|-------|---------|--------|-------------|
| Gemini 3.0 Pro | 2M tokens | 128K | Frontier reasoning, 3D multimodal |
| Gemini 3.0 Flash | 2M tokens | 128K | Fast, cost-efficient |

**Pricing:** ~$2.00/M input, ~$8.00/M output (vs Gemini 2.5 Pro at $1.25/$5.00)

### Critical Prompting Rules

#### 1. Temperature: KEEP at 1.0 (Mandatory)
Google strongly recommends default temperature of 1.0 for Gemini 3. Setting below 1.0 "may lead to unexpected behavior, looping, or degraded performance, particularly with complex mathematical or reasoning tasks."

This is a **hard rule** -- unlike Gemini 2.x where lower temperatures were fine.

#### 2. Simplified Prompts with Thinking
If you used complex prompt engineering (chain-of-thought forcing) on Gemini 2.5, try Gemini 3 with `thinking_level: "high"` and simplified prompts. The model handles reasoning internally.

#### 3. Latency Optimization
For faster responses: set thinking level to `LOW` and add system instruction "think silently."

#### 4. Prompt Structure (Placement Matters)
- Place core requests and critical restrictions as the **final line**
- Order: context -> main task -> constraints (negative, formatting, quantitative)
- Negative constraints at the end to prevent model dropping them

#### 5. Avoid Overly Broad Constraints
```
# BAD: Too broad, causes over-indexing
"Do not infer. Do not guess."

# GOOD: Specific about what to avoid
"Perform calculations based strictly on provided text.
Do not introduce external information."
```

The model may fail basic logic/arithmetic if given blanket "do not infer" instructions.

#### 6. Multimodal Prompting
- Refer to "the image" or "this chart" with a specific question
- "Analyze this" alone is insufficient -- ask specific questions
- Native support for text, image, audio, video, and 3D (new in Gemini 3)

#### 7. Grounding Context
- Explicitly state provided context is "the only source of truth"
- Model may revert to training data without explicit anchoring
- Use split-step verification: first verify capability, then generate

#### 8. Communication Style
- Gemini 3 defaults to less verbose, direct responses
- For conversational tone, explicitly request it
- Review personas for contradictory instructions

### New Capabilities
- 2M token context window (up from 1M in Gemini 2.0)
- Advanced parallel + nested tool use
- ~1.5s median latency (down from ~3s)
- Native 3D understanding

**Sources:**
- Official prompting guide: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/gemini-3-prompting-guide
- Prompting strategies: https://ai.google.dev/gemini-api/docs/prompting-strategies
- Gemini 3 best practices: https://www.philschmid.de/gemini-3-prompt-practices
- Gemini 3 developer guide: https://ai.google.dev/gemini-api/docs/gemini-3

---

## Gemini 2.0 (Legacy)

**Context:** 1M tokens
**Strengths:** Multimodal, long context, native tool use

### Key Principle: Query at END

For long contexts, place the question LAST:
```
[All context / documents]
...
Based on the information above, answer: [question]
```

### Temperature

| Model | Temperature |
|-------|-------------|
| Gemini 2.0 | 0 works for deterministic |
| Gemini 2.5 | 0 works for deterministic |
| Gemini 3.0/3.1 | 1.0 (required default) |

### Multimodal Prompting

**Images:** Place text prompt AFTER image.
```python
contents = [
    image_part,  # Image first
    "Describe what you see"  # Text after
]
```

### Grounding

Enable Google Search for factual accuracy:
```python
response = model.generate_content(
    "What happened in tech news today?",
    tools=[{"google_search": {}}]
)
```

### Key Behaviors

- **No negative examples:** Don't show "what NOT to do"
- **Thinking mode:** Use `thinkingBudget` for complex tasks
- **Lost-in-middle:** Still applies even with 1M context
- **Object detection:** Returns 0-1000 normalized coordinates

---

## Quick Reference

| Model | CoT Prompting | Few-Shot | System Prompt |
|-------|---------------|----------|---------------|
| Gemini 3.1 Pro | Thinking mode (low/medium/high) | Helpful (no negatives) | Yes |
| Gemini 3.0 | Thinking mode (`thinking_level`) | Helpful (no negatives) | Yes |
| Gemini 2.0 | Manual/Thinking | Helpful (no negatives) | Yes |

---

*Last updated: February 2026*
