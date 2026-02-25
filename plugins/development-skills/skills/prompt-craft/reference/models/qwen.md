# Alibaba Qwen

## Qwen 3.5 (Current Flagship)

**Full name:** Qwen3.5-397B-A17B | **Architecture:** 397B total, 17B active (MoE)
**Type:** Native vision-language model (text + image + video up to 2 hours)
**Languages:** 201 languages and dialects | **License:** Apache 2.0

### Key Capabilities
- "Built for the agentic AI era" -- outperforms Qwen-3-Max-Thinking despite smaller size
- Native multimodal processing
- Hybrid thinking/non-thinking modes
- Integrated tools: web search, web extractor, code interpreter
- **Qwen 3.5-Plus:** 1M token context window variant

### Prompting
- ChatML format: **always use `apply_chat_template`** (never manually construct ChatML tokens)
- Standard system prompts work
- Few-shot examples are helpful
- Structured output supported

---

## Qwen 3 Family

### Hybrid Thinking Mode (Key Innovation)
Model switches between deep reasoning and fast response automatically. Integrated tool use during reasoning. Competitive with DeepSeek-R1, o1, o3-mini.

### /think and /no_think Toggles
Control thinking mode per-message:
- `/think` -- enable deep reasoning for current message
- `/no_think` -- disable thinking for fast response

---

## Qwen 2.5 (Legacy -- Still Relevant for Fine-Tuning)

**Context:** 128K | **Variants:** Qwen2.5, Qwen2.5-Coder, Qwen2.5-Math

### Chat Template (Critical)
```python
# CORRECT -- always use tokenizer
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)

# NEVER manually construct ChatML tokens
```

### Sampling Parameters
```python
# General
{"temperature": 0.7, "top_p": 0.8, "top_k": 20, "repetition_penalty": 1.05}

# Code (Qwen-Coder)
{"temperature": 0.2, "top_p": 0.9, "repetition_penalty": 1.05}
```

### Key Differentiators
- Native Chinese + English (no quality penalty for Chinese)
- 29+ languages without English bias
- Apache 2.0 license

---

## Quick Reference

| Model | CoT Prompting | Few-Shot | System Prompt |
|-------|---------------|----------|---------------|
| Qwen 3.5 | Hybrid (automatic thinking) | Helpful | Yes |
| Qwen3-235B | Hybrid thinking | Helpful | Yes |
| Qwen 2.5 | Manual | Helpful | Yes |

---

*Last updated: February 2026*
