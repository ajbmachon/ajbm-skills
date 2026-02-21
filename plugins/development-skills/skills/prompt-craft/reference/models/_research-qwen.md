# Qwen Research Findings — February 2026

## Qwen 3.5 (Latest)
- **Released:** February 17, 2026
- **Full name:** Qwen3.5-397B-A17B
- **Parameters:** 397B total, 17B active (MoE)
- **Type:** Native vision-language model (text + image + video up to 2hrs)
- **Languages:** 201 languages and dialects (up from 82 in Qwen 2.5)
- **License:** Apache 2.0 (open-source)
- **Key innovation:** Combines specialized models into single native VLM
- **Cheaper and more efficient** than predecessor
- **"Built for the agentic AI era"** — Alibaba's positioning

## Qwen 3.5-Plus
- Premium version with **1M token context window**
- Targets Gemini 3 Pro's long-context capabilities

## Qwen 3 Family (April 2025)
- **Qwen3-235B-A22B:** Large MoE flagship (235B total, 22B active)
- **Qwen3-30B-A3B:** Small MoE (30B total, 3B active) — outperforms QwQ-32B
- **Dense models:** Qwen3-32B, 14B, 8B, 4B, 1.7B, 0.6B
- **License:** Apache 2.0
- **Hybrid thinking:** Switches between thinking and non-thinking modes
- Competitive with DeepSeek-R1, o1, o3-mini, Grok-3, Gemini-2.5-Pro

## Qwen3-Coder-480B-A35B
- Specialized coding model
- 480B total, 35B active
- Mentioned as top recommendation alongside Qwen3-235B-A22B

## QwQ-32B (Reasoning Model)
- **Released:** March 2025
- **Parameters:** 32B dense
- **Recommended settings:** temperature 0.6, top_p 0.95, top_k 40, repetition_penalty 1.0
- **System prompt:** "You are a helpful and harmless assistant."
- Matches DeepSeek-R1 on AIME24, LiveBench, BFCL with only 5% of parameters

## Prompting Notes
- ChatML format still applies across all Qwen models
- Standard system prompts work
- Few-shot examples helpful
- Structured output supported
- Hybrid thinking mode inherited from Qwen 3-Max-Thinking

## Sources
- https://www.datacamp.com/blog/qwen3-5
- https://qwenlm.github.io/blog/qwen3/
- https://www.siliconflow.com/articles/en/the-best-qwen-models-in-2025
- https://hypereal.tech/a/best-qwen-models
- https://groq.com/blog/a-guide-to-reasoning-with-qwen-qwq-32b
