# DeepSeek

## DeepSeek V3.2 (Current Production)

**Released:** December 1, 2025
**Architecture:** 671B MoE (37B active) — same base as V3
**Context:** 128K tokens
**API IDs:** `deepseek-chat` (non-thinking), `deepseek-reasoner` (thinking mode)
**Max Output:** 8K (chat) / 64K (reasoner)
**Pricing:** $0.028/M input (cache hit), $0.28/M (cache miss), $0.42/M output

### What Changed from V3

- DeepSeek Sparse Attention for improved efficiency
- Thinking-in-tool-use: reasons while using tools
- Agentic training across 1,800+ environments
- **V3.2-Speciale** variant: gold-medal math/coding olympiad performance
- DeepSeek-Coder merged into V3.2 (no separate coder model)

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

## DeepSeek R1 (Reasoning — Being Superseded)

**Note:** The `deepseek-reasoner` API endpoint now serves V3.2 in thinking mode. R1 guidance still applies to that endpoint.

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

## DeepSeek V4 (Imminent — Not Officially Released)

**Status as of Feb 21, 2026:** NOT officially released. Expected mid-February 2026. Multiple confirmed technical breakthroughs.

### What's Confirmed vs Leaked

| Claim | Status | Source |
|-------|--------|--------|
| Engram conditional memory | **CONFIRMED** | Published paper + open-source code |
| 1M token context window | **CONFIRMED** | Observed in production (Feb 11, 2026) |
| 1T parameter MoE architecture | LEAKED | GitHub code leak ("MODEL1") |
| ~32B active parameters | LEAKED | Architecture analysis |
| 90% HumanEval | LEAKED | Internal benchmark leak |
| >80% SWE-bench | LEAKED | Internal benchmark leak |
| Consumer GPU support | CLAIMED | Third-party reports |
| Open-source release (MIT) | EXPECTED | Based on V3 track record |

### Architectural Innovations

- **Engram memory:** Hash-based O(1) retrieval in DRAM — 1M token context costs roughly same compute as 128K
- **Modified Hopfield Continuum (mHC):** Bounded attention mechanism
- **Dynamic Sparse Attention (DSA):** Lightning Indexer for efficient long-context processing

### Projected Specs

- 1T total parameters, ~32B active (sparse MoE)
- 1M token context window (already live)
- ~$0.10/M input tokens (~50x cheaper than GPT-5.2)
- Hybrid reasoning/non-reasoning in one model — **R2 absorbed into V4** (CEO stalled separate R2 in June 2025 due to unsatisfactory performance)
- Target: autonomous coding — managing entire software repositories

**Prompting guidance:** Not yet available. Monitor for release notes. Expect standard prompting given the hybrid approach.

**Sources:**
- https://www.digitalapplied.com/blog/deepseek-v4-engram-architecture-coding-model-guide
- https://introl.com/blog/deepseek-v4-trillion-parameter-coding-model-february-2026
- https://www.nxcode.io/resources/news/deepseek-v4-engram-memory-1t-model-guide-2026
- https://aitoolsreview.co.uk/insights/deepseek-v4-everything-we-know

---

## Quick Reference

| Model | CoT Prompting | Few-Shot | System Prompt |
|-------|---------------|----------|---------------|
| DeepSeek V3.2 | Manual / thinking mode | Helpful | Yes |
| DeepSeek R1 | **NEVER** | **Hurts** | **NO** |
| DeepSeek V4 | TBD (hybrid) | TBD | TBD |

---

*Last updated: February 2026*
