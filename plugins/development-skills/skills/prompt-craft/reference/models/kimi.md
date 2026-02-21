# Moonshot Kimi

## Kimi K2

**Architecture:** 1T MoE (32B active)
**Context:** 128K-256K tokens
**Design:** Agentic-first

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

### K2-Thinking Variant

```python
temperature = 1.0  # Different from Instruct!
max_tokens = 16000  # Minimum for reasoning + output
min_p = 0.01
```

---

## Quick Reference

| Model | CoT Prompting | Few-Shot | System Prompt |
|-------|---------------|----------|---------------|
| Kimi K2 | Automatic (Thinking) | Varies | Goal-oriented |

---

*Last updated: February 2026*
