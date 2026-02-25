# Moonshot Kimi

## Kimi K2.5 (Current Flagship)

**Architecture:** 1T MoE (32B active) | **Context:** 262K | **Max Output:** 32K
**Type:** Native multimodal (text, images, video, documents) | **License:** MIT
**Pricing:** $0.60/M input, $3/M output

### Key Capabilities Over K2
- Native vision capabilities (K2 was text-only)
- Agent Swarm mode (preview): up to 100 sub-agents, 1,500+ parallel tool calls
- 76.8% SWE-bench Verified
- MCP integration support

### Four Operational Modes

| Mode | Use Case |
|------|----------|
| **Instant** | Fast responses, simple queries |
| **Thinking** | Extended reasoning for complex problems |
| **Agent** | Office productivity |
| **Agent Swarm** (preview) | Parallel sub-agent execution |

---

## Kimi K2 (Foundation)

**Architecture:** 1T MoE (32B active) | **Context:** 128K-256K | **Design:** Agentic-first

### Critical Settings
```python
temperature = 0.6  # Official recommendation
```

### Prompting Style

**Use goal-oriented prompts (not step-by-step):**
```
# Don't: "Step 1: Read the file. Step 2: Parse JSON..."
# Do: "Count the number of users in this JSON file and return the total."
```

### Known Issues

| Issue | Mitigation |
|-------|------------|
| Instruction drift after ~900 words | Put critical constraints EARLY |
| Formatting inconsistencies in long outputs | Use explicit section markers |
| Overthinking simple tasks | Request brevity explicitly |

### K2-Thinking Variant

71.3% SWE-bench Verified. Sustains 200-300 sequential tool calls without drift.

```python
temperature = 1.0  # MUST be 1.0 -- different from K2-Instruct's 0.6!
max_tokens = 16000
```

Reasoning exposed via `reasoning_content` API field.

---

## Quick Reference

| Model | CoT Prompting | Few-Shot | System Prompt |
|-------|---------------|----------|---------------|
| Kimi K2.5 | Four modes (Instant/Thinking/Agent/Swarm) | Varies | Goal-oriented |
| Kimi K2 | Automatic (Thinking) | Varies | Goal-oriented |

---

*Last updated: February 2026*
