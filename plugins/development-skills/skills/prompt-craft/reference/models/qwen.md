# Alibaba Qwen

## Qwen 3.5 (Current Flagship)

**Released:** February 17, 2026
**Full name:** Qwen3.5-397B-A17B
**Architecture:** 397B total, 17B active (MoE)
**Type:** Native vision-language model (text + image + video up to 2 hours)
**Languages:** 201 languages and dialects (up from 82 in Qwen 2.5)
**License:** Apache 2.0 (open-source)

### Key Capabilities

- "Built for the agentic AI era" — Alibaba's positioning
- Outperforms Qwen-3-Max-Thinking (1T+ params) despite smaller size
- Native multimodal processing (no separate vision encoder needed)
- Hybrid thinking/non-thinking modes (inherited from Qwen 3 series)
- Integrated tools: web search, web extractor, code interpreter
- Cheaper and more efficient than predecessor

### Qwen 3.5-Plus (Premium Variant)

- **1M token context window** — targets Gemini 3 Pro's long-context capabilities
- Same architecture, extended for long-context workloads

### Prompting Notes

No major prompting paradigm shift from Qwen 2.5:
- ChatML format still applies (use tokenizer `apply_chat_template`)
- Standard system prompts work
- Few-shot examples are helpful
- Structured output supported

**Sources:**
- https://www.datacamp.com/blog/qwen3-5
- https://www.cnbc.com/2026/02/17/china-alibaba-qwen-ai-agent-latest-model.html

---

## Qwen 3 Family (April 2025)

### Models

| Model | Type | Parameters | License |
|-------|------|-----------|---------|
| Qwen3-235B-A22B | Large MoE flagship | 235B total, 22B active | Apache 2.0 |
| Qwen3-30B-A3B | Small MoE | 30B total, 3B active | Apache 2.0 |
| Qwen3-32B | Dense | 32B | Apache 2.0 |
| Qwen3-14B | Dense | 14B | Apache 2.0 |
| Qwen3-8B | Dense | 8B | Apache 2.0 |
| Qwen3-4B | Dense | 4B | Apache 2.0 |
| Qwen3-1.7B | Dense | 1.7B | Apache 2.0 |
| Qwen3-0.6B | Dense | 0.6B | Apache 2.0 |

### Qwen3-Coder-480B-A35B

- Specialized coding model (480B total, 35B active)
- Top-tier coding performance alongside Qwen3-235B-A22B

### Hybrid Thinking Mode (Key Innovation)

Qwen 3 introduced hybrid thinking/non-thinking modes:
- Model switches between deep reasoning and fast response automatically
- Integrated tool use during reasoning
- Competitive with DeepSeek-R1, o1, o3-mini, Grok-3, Gemini-2.5-Pro

### Qwen 3-Max-Thinking (January 27, 2026)

Predecessor to Qwen 3.5. Hybrid thinking modes with integrated tool use during reasoning.

**Sources:**
- https://qwenlm.github.io/blog/qwen3/
- https://www.siliconflow.com/articles/en/the-best-qwen-models-in-2025

---

## QwQ-32B (Reasoning Model)

**Released:** March 2025
**Parameters:** 32B dense
**Best for:** Complex reasoning tasks at small model size

### Recommended Settings

```python
{
    "temperature": 0.6,
    "top_p": 0.95,
    "top_k": 40,
    "repetition_penalty": 1.0
}
```

**System prompt:** `"You are a helpful and harmless assistant."`

### Key Facts

- Matches DeepSeek-R1 on AIME24, LiveBench, BFCL with only 5% of the parameters
- RL-trained for reasoning (similar approach to DeepSeek-R1)
- Strong for math, code, and logical reasoning

**Sources:**
- https://groq.com/blog/a-guide-to-reasoning-with-qwen-qwq-32b

---

## Qwen 2.5 (Legacy — Still Relevant for Fine-Tuning)

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

---

## Quick Reference

| Model | CoT Prompting | Few-Shot | System Prompt |
|-------|---------------|----------|---------------|
| Qwen 3.5 | Hybrid (automatic thinking) | Helpful | Yes |
| Qwen3-235B-A22B | Hybrid thinking | Helpful | Yes |
| QwQ-32B | **Built-in reasoning** | Varies | Yes |
| Qwen 2.5 | Manual | Helpful | Yes |

---

*Last updated: February 2026*
