# Alibaba Qwen

## Qwen 2.5

**Sizes:** 0.5B - 72B (open weights)
**Context:** 128K tokens
**Variants:** Qwen2.5, Qwen2.5-Coder, Qwen2.5-Math, Qwen-Max (API)

### Chat Template (Critical)

Qwen uses ChatML format. Always use the tokenizer:
```python
# CORRECT
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)

# NEVER manually construct ChatML tokens
```

### Sampling Parameters

**General:**
```python
{
    "temperature": 0.7,
    "top_p": 0.8,
    "top_k": 20,
    "repetition_penalty": 1.05
}
```

**Code (Qwen-Coder):**
```python
{
    "temperature": 0.2,  # Lower for determinism
    "top_p": 0.9,
    "repetition_penalty": 1.05
}
```

### Key Differentiators

- **Bilingual strength:** Native Chinese + English (no quality penalty for Chinese)
- **29+ languages:** Strong multilingual without English bias
- **Open weights:** Apache 2.0 license (except 3B Coder)

### Default System Prompt

```
"You are Qwen, created by Alibaba Cloud. You are a helpful assistant."
```

### Notes

- `repetition_penalty: 1.05` recommended to prevent repetition
- Qwen-Coder specialized for code; use base for non-code
- Qwen2.5-Math: English and Chinese math only (not general use)

---

## Qwen 3.5

**Released:** February 17, 2026
**Parameters:** 397B (open-weight)
**Languages:** 201 languages and dialects (up from 82 in Qwen 2.5)
**Multimodal:** Native text, image, video (up to 2 hours)

### Key Improvements

- Outperforms previous Qwen-3-Max-Thinking (1T+ params) despite smaller size
- Native multimodal processing (no separate vision encoder needed)
- Hybrid thinking/non-thinking modes (inherited from Qwen 3-Max-Thinking)
- Integrated tools: web search, web extractor, code interpreter

### Prompting Notes

No major prompting paradigm shift from Qwen 2.5:
- ChatML format still applies (use tokenizer `apply_chat_template`)
- Standard system prompts work
- Few-shot examples are helpful
- Structured output supported

### Qwen 3-Max-Thinking (January 27, 2026)

Predecessor to Qwen 3.5 with hybrid thinking modes:
- Switches between thinking and non-thinking modes automatically
- Integrated tool use during reasoning

**Sources:**
- https://www.cnbc.com/2026/02/17/china-alibaba-qwen-ai-agent-latest-model.html
- https://www.alibabacloud.com/blog/alibaba-introduces-qwen3-setting-new-benchmark-in-open-source-ai-with-hybrid-reasoning_602192

---

## Quick Reference

| Model | CoT Prompting | Few-Shot | System Prompt |
|-------|---------------|----------|---------------|
| Qwen 2.5 | Manual | Helpful | Yes |
| Qwen 3.5 | Hybrid (automatic thinking) | Helpful | Yes |

---

*Last updated: February 2026*
