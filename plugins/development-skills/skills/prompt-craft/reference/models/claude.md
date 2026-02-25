# Claude (Anthropic)

## Claude 4.6 Family (Opus 4.6 / Sonnet 4.6)

### Models & Specs

| Model | API ID | Context | Max Output | Pricing (in/out MTok) |
|-------|--------|---------|------------|----------------------|
| Claude Opus 4.6 | `claude-opus-4-6` | 200K (1M beta) | 128K | $5 / $25 |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | 200K (1M beta) | 64K | $3 / $15 |
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | 200K | 64K | $1 / $5 |

### Breaking Changes

#### 1. Prefill Removal (BREAKING - Opus 4.6)
Prefilling assistant messages on the last turn is **not supported** on Opus 4.6. Returns 400 error.

**Migration paths:**
- JSON/YAML format control -> Use `output_config.format`
- Eliminating preambles -> System prompt: "Respond directly without preamble"
- Continuations -> User message: "Your previous response ended with `[text]`. Continue from there."

#### 2. Adaptive Thinking (replaces budget_tokens)
`thinking: {type: "adaptive"}` is the recommended mode for 4.6 models. `budget_tokens` is **deprecated**.

```python
client.messages.create(
    model="claude-opus-4-6",
    max_tokens=16000,
    thinking={"type": "adaptive"},
    messages=[{"role": "user", "content": "..."}],
)
```

#### 3. Effort Parameter
Controls thinking depth: `max` (Opus only) > `high` (default) > `medium` > `low`.

#### 4. output_config.format (replaces output_format)
```python
output_config={"format": {"type": "json_schema", "schema": {...}}}
```

### Critical Prompting Changes

#### REMOVE Anti-Laziness Prompts
The single biggest prompting change for Claude 4.6. Per Anthropic engineer testimony: "significant leaps in intelligence were observed as soon as anti-laziness prompts were removed."

**Delete these patterns:** "be thorough", "think carefully", "do not be lazy", "take your time", "be comprehensive". These cause Claude 4.6 to overthink, loop, or write-then-rewrite.

#### SOFTEN Tool Instructions
```
# REMOVE: "CRITICAL: You MUST use this tool when..."
# REPLACE: "Use this tool when it would help."
```

#### REMOVE Explicit Think Tool Instructions
Claude 4.6 thinks adaptively without being told to.

#### BE EXPLICIT About Actions
Claude 4.6 tends toward suggestion over implementation. Use directive language: "Change this function" not "Can you suggest changes?"

#### Use Effort as Primary Control Lever
Lower the effort setting rather than adding more prompt constraints.

### Behavioral Notes

- More concise, direct, grounded than previous models
- Tendency to overengineer (extra files, unnecessary abstractions) -- add constraints
- Defaults to LaTeX for math -- add plain-text instructions if unwanted
- At high effort, does significantly more upfront exploration -- constrain with: "Prioritize execution over deliberation"

### Sonnet 4.6

- Default effort: `medium` (most apps), `low` (latency-sensitive)
- Adaptive thinking excels at: autonomous agents, computer use, bimodal workloads
- For hard cost ceiling: use extended thinking with `budget_tokens` cap (~16K)

### Quick Reference

| Model | CoT Prompting | Few-Shot | System Prompt |
|-------|---------------|----------|---------------|
| Claude 4.6 | Adaptive (effort parameter) | Helpful | Yes |

---

*Last updated: February 2026*
