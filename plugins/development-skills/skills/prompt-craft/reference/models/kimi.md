# Moonshot Kimi

## Kimi K2.5 (Current Flagship)

**Released:** January 27, 2026 (open weights February 2026)
**Architecture:** 1T MoE (32B active per token) — same base as K2
**Context:** 262K tokens | **Max Output:** 32K tokens
**Training:** ~15T mixed visual and text tokens
**Type:** Native multimodal — text, images, video, documents
**License:** MIT (fully open-weight)
**Pricing:** $0.60/M input, $3/M output (Moonshot) | $0.50/$2.40 (OpenRouter)

### Key Capabilities Over K2

- Native vision capabilities (K2 was text-only)
- Visual debugging and front-end dev tasks
- Agent Swarm mode (research preview): up to 100 sub-agents, 1,500+ parallel tool calls
- 4.5x speed improvement via Parallel-Agent Reinforcement Learning (PARL)
- **76.8% SWE-bench Verified**, 50.2% HLE
- MCP integration support

### Four Operational Modes

| Mode | Use Case |
|------|----------|
| **Instant** | Fast responses, simple queries |
| **Thinking** | Extended reasoning for complex problems |
| **Agent** | Office productivity (documents, spreadsheets) |
| **Agent Swarm** (preview) | Parallel sub-agent execution for complex tasks |

### API Access

- **Web:** kimi.com
- **API:** platform.moonshot.ai (OpenAI-compatible)
- **CLI:** Kimi Code CLI
- **Weights:** HuggingFace (moonshotai/Kimi-K2.5)

**Sources:**
- https://platform.moonshot.ai/docs/guide/kimi-k2-quickstart
- https://www.infoq.com/news/2026/02/kimi-k25-swarm/
- https://dev.to/czmilo/kimi-k25-in-2026
- https://www.datacamp.com/tutorial/kimi-k2-agent-swarm-guide

---

## Kimi K2 (Foundation)

**Released:** July 2025
**Architecture:** 1T MoE (32B active)
**Context:** 128K-256K tokens
**Training:** 15.5T tokens
**Design:** Agentic-first
**License:** Modified MIT

### Critical Settings

```python
temperature = 0.6  # Official recommendation
system_prompt = "You are Kimi, an AI assistant created by Moonshot AI."
```

### Prompting Style

**Use goal-oriented prompts (not step-by-step):**
```
# Don't
"Step 1: Read the file. Step 2: Parse JSON. Step 3: Extract users..."

# Do
"Count the number of users in this JSON file and return the total."
```

### Known Issues

| Issue | Mitigation |
|-------|------------|
| Instruction drift after ~900 words | Put critical constraints EARLY |
| Formatting inconsistencies in long outputs | Use explicit section markers |
| Overthinking simple tasks | Request brevity explicitly |
| Over-confident paraphrasing | Ask for direct quotes |

### Long Context

- Normal speed < 100K tokens
- Speed drops 100K-256K tokens
- For very long: add executive summary in final user message

### Tool Calling

- Nearly 100% accuracy via official API
- 10+ built-in tools (web search, etc.)
- Performance may decrease on third-party open-source platforms

### K2-Thinking Variant (November 6, 2025)

**71.3% SWE-bench Verified**, 44.9% HLE, 60.2% BrowseComp. Sustains 200-300 sequential tool calls without drift. Native INT4 quantization via QAT (lossless performance).

```python
temperature = 1.0  # MUST be 1.0 — different from Instruct!
max_tokens = 16000  # Minimum for reasoning + output
min_p = 0.01
```

Reasoning exposed via `reasoning_content` API field (similar to DeepSeek R1).

---

## Quick Reference

| Model | CoT Prompting | Few-Shot | System Prompt |
|-------|---------------|----------|---------------|
| Kimi K2.5 | Four modes (Instant/Thinking/Agent/Swarm) | Varies | Goal-oriented |
| Kimi K2 | Automatic (Thinking) | Varies | Goal-oriented |

---

*Last updated: February 2026*
