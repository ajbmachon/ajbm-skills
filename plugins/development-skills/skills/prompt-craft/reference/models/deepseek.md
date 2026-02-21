# DeepSeek

## DeepSeek V3

**Architecture:** 671B MoE (37B active)
**Context:** 128K tokens
**Best for:** General chat, code generation

### Temperature Settings

| Use Case | Temperature |
|----------|-------------|
| Coding / Math | 0.0 |
| Data Analysis | 1.0 |
| General Chat | 1.3 |
| Creative Writing | 1.5 |

### Prompting

Standard prompting works. System prompts supported.

```python
messages = [
    {"role": "system", "content": "You are an expert Python developer."},
    {"role": "user", "content": "Write a function to..."}
]
```

---

## DeepSeek R1

**Critical:** Requires FUNDAMENTALLY different prompting.

### What NOT to Do

```
DON'T: Use system prompts
DON'T: Provide few-shot examples (degrades performance)
DON'T: Trigger chain-of-thought manually (automatic)
DON'T: Set temperature/top_p (not supported for R1)
```

### What TO Do

**All instructions in user message:**
```python
messages = [
    {
        "role": "user",
        "content": """
You are an expert Python developer.

## Task
Write a function to validate email addresses.

## Requirements
- Handle edge cases
- Return boolean
- Include docstring

## Output Format
Provide only the Python code.
"""
    }
]
```

**Multi-turn handling:**
```python
# IMPORTANT: Strip reasoning_content between turns
for message in conversation_history:
    if 'reasoning_content' in message:
        del message['reasoning_content']  # Required to avoid 400 errors
```

### R1-Specific Tips

- For math: Include "Put your final answer within `\boxed{}`"
- Use `temperature=0.6` (official recommendation)
- If reasoning bypassed: "Start with the `<think>` tag"

---

## DeepSeek V4 (Upcoming)

**Status:** Expected mid-February 2026 (imminent or already released)

**Key specs (projected/leaked):**
- 1T total parameters, 32B active (sparse MoE)
- 1M token context window (silently upgraded from 128K on Feb 11, 2026)
- Engram architecture: hash-based O(1) memory retrieval
- ~$0.10/1M input tokens (projected ~50x cheaper than GPT-5.2)
- Open weights expected (MIT license, continuing V3 pattern)

**Architectural innovations:**
- Engram memory (O(1) retrieval in DRAM)
- Modified Hopfield Continuum (mHC) for bounded attention
- Dynamic Sparse Attention (DSA) with Lightning Indexer

**Hybrid model:** Supports both reasoning and non-reasoning tasks in one model (no separate R2 model expected).

**Prompting guidance:** Not yet available. Monitor for release notes. Expect standard prompting to work given the hybrid approach.

**Sources:**
- https://www.digitalapplied.com/blog/deepseek-v4-engram-architecture-coding-model-guide
- https://www.ai-supremacy.com/p/deepseeks-next-move-what-v4-will-like-model1

---

## Quick Reference

| Model | CoT Prompting | Few-Shot | System Prompt |
|-------|---------------|----------|---------------|
| DeepSeek V3 | Manual | Helpful | Yes |
| DeepSeek R1 | **NEVER** | **Hurts** | **NO** |
| DeepSeek V4 | TBD (hybrid) | TBD | TBD |

---

*Last updated: February 2026*
