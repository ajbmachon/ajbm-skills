# DeepSeek

## DeepSeek V3.2 (Current Production)

**Architecture:** 671B MoE (37B active) | **Context:** 128K
**API IDs:** `deepseek-chat` (non-thinking), `deepseek-reasoner` (thinking mode)
**Pricing:** $0.028/M input (cache hit), $0.28/M (miss), $0.42/M output

### Temperature Settings

| Use Case | Temperature |
|----------|-------------|
| Coding / Math | 0.0 |
| Data Analysis | 1.0 |
| General Chat | 1.3 |
| Creative Writing | 1.5 |

Standard prompting works. System prompts supported.

---

## DeepSeek R1 (Reasoning)

**Critical:** Requires fundamentally different prompting.

### What NOT to Do
- Do NOT use system prompts
- Do NOT provide few-shot examples (degrades performance)
- Do NOT trigger chain-of-thought manually (automatic)

### What TO Do

**All instructions in user message:**
```python
messages = [
    {
        "role": "user",
        "content": """You are an expert Python developer.

## Task
Write a function to validate email addresses.

## Requirements
- Handle edge cases
- Return boolean

## Output Format
Provide only the Python code."""
    }
]
```

**Multi-turn: Strip `reasoning_content` between turns** (required to avoid 400 errors):
```python
for message in conversation_history:
    if 'reasoning_content' in message:
        del message['reasoning_content']
```

### R1-Specific Tips
- For math: include "Put your final answer within `\boxed{}`"
- Use `temperature=0.6` (official recommendation)
- If reasoning bypassed: "Start with the `<think>` tag"

---

## Quick Reference

| Model | CoT Prompting | Few-Shot | System Prompt |
|-------|---------------|----------|---------------|
| DeepSeek V3.2 | Manual / thinking mode | Helpful | Yes |
| DeepSeek R1 | **NEVER** | **Hurts** | **NO** |

---

*Last updated: February 2026*
