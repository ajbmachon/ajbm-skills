# OpenAI

## GPT-5.2 (Current Flagship)

**Context:** 400K | **Max output:** 128K | **Chat:** `gpt-5.2-chat-latest` (128K/16K)
**Pricing:** $1.75/M input ($0.175 cached), $14/M output

### The Knobs That Matter

**`reasoning.effort`** -- Six levels: `none` (default, no internal reasoning) -> `minimal` -> `low` -> `medium` -> `high` -> `xhigh` (Pro only). Temperature/top_p only work at `none`. With `none`, explicitly ask for a brief plan before the final answer.

**`text.verbosity`** -- `low`, `medium` (default), `high`. Use this instead of fighting verbosity with prompting.

**`reasoning.summary`** -- Concise summaries of reasoning (useful for audits without exposing full hidden reasoning).

**Compaction (`POST /v1/responses/compact`)** -- For long-running workflows. Output is opaque/encrypted: treat as state to continue with, not data to parse.

### Prompting Patterns

- **Output-shape + length clamps:** Bullet caps, section names, snippet limits (high ROI)
- **Scope-drift prevention:** "Implement ONLY what I asked. No embellishments."
- **Long-context:** Summarize relevant sections first, restate constraints, anchor claims to sections
- **Ambiguity guardrails:** Ask 1-3 clarifying questions or give 2-3 interpretations with labeled assumptions

### Tools & Agents

- Prefer **Responses API** for tool-heavy workflows
- Post-trained on `apply_patch` and `shell`; supports custom tools
- Compact after milestones (not every turn)

---

## o3 / o4-mini Reasoning Models

| Model | Context | Pricing (in/out) | Reasoning Effort |
|-------|---------|-------------------|-----------------|
| **o3** | 200K | $2/$8 per M | low/medium/high |
| **o4-mini** | 200K | $1.10/$4.40 per M | low/medium/high |

### Prompting Rules

- **Keep prompts simple and direct.** Never use chain-of-thought prompting.
- **Try zero-shot first.** Few-shot only for strict formatting.
- Use **delimiters** to separate task, context, constraints.
- Use **developer messages** (not "system"). Include `Formatting re-enabled` on first line for markdown.

### Function Calling

- `strict: True` always in function schemas
- **`encrypted_content`** to maintain CoT between function calls:
```python
response = client.responses.create(
    model="o3",
    input=context,
    tools=tools,
    include=["reasoning.encrypted_content"]
)
context += response.output  # Preserves reasoning for next turn
```

### Anti-Patterns

- Do NOT use chain-of-thought prompting
- Do NOT carry irrelevant past tool calls in history
- Avoid deeply nested parameter hierarchies (<100 tools, <20 args)

---

## Quick Reference

| Model | CoT Prompting | Few-Shot | System Prompt |
|-------|---------------|----------|---------------|
| GPT-5.2 | Brief plan at `none` | Helpful at `none`/`low` | Yes (system/developer) |
| o3 / o4-mini | **NEVER** | Only for strict formatting | Developer role |

---

*Last updated: February 2026*
