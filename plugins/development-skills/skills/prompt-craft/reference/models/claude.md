# Claude (Anthropic)

## Claude 4.6 Family (Opus 4.6 / Sonnet 4.6)

### Models & Specs

| Model | API ID | Context | Max Output | Pricing (in/out MTok) | Released |
|-------|--------|---------|------------|----------------------|----------|
| Claude Opus 4.6 | `claude-opus-4-6` | 200K (1M beta) | 128K | $5 / $25 | Feb 5, 2026 |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | 200K (1M beta) | 64K | $3 / $15 | Feb 17, 2026 |
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | 200K | 64K | $1 / $5 | Oct 2025 |

**Knowledge cutoffs:**
- Opus 4.6: Reliable May 2025, training data Aug 2025
- Sonnet 4.6: Reliable Aug 2025, training data Jan 2026
- Haiku 4.5: Reliable Feb 2025, training data Jul 2025

**Platform IDs:**
- AWS Bedrock: `anthropic.claude-opus-4-6-v1`, `anthropic.claude-sonnet-4-6`
- GCP Vertex: `claude-opus-4-6`, `claude-sonnet-4-6`

### Breaking Changes from Previous Claude Models

#### 1. Prefill Removal (BREAKING - Opus 4.6)
Prefilling assistant messages on the last turn is **not supported** on Opus 4.6. Returns 400 error.

**Migration paths:**
- JSON/YAML format control -> Use Structured Outputs (`output_config.format`)
- Eliminating preambles -> System prompt: "Respond directly without preamble"
- Avoiding bad refusals -> Claude 4.6 has much better refusal calibration
- Continuations -> Move to user message: "Your previous response ended with `[text]`. Continue from there."
- Context hydration -> Inject via user turns or tools, not assistant prefill

#### 2. Adaptive Thinking (NEW - replaces budget_tokens)
`thinking: {type: "adaptive"}` is the recommended mode for Opus 4.6 and Sonnet 4.6. Claude dynamically decides when and how much to think.

`thinking: {type: "enabled"}` and `budget_tokens` are **deprecated** on 4.6 models.

```python
# NEW way (4.6)
client.messages.create(
    model="claude-opus-4-6",
    max_tokens=16000,
    thinking={"type": "adaptive"},
    messages=[{"role": "user", "content": "..."}],
)

# OLD way (deprecated)
client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=64000,
    thinking={"type": "enabled", "budget_tokens": 32000},
    messages=[{"role": "user", "content": "..."}],
)
```

#### 3. Effort Parameter (GA - no beta header needed)
Controls thinking depth. New `max` level on Opus 4.6.

- `max` - Absolute highest capability (Opus 4.6 only)
- `high` - Default for Opus 4.6 and Sonnet 4.6
- `medium` - Recommended for most Sonnet 4.6 use cases
- `low` - Latency-sensitive workloads

#### 4. output_format -> output_config.format
```python
# Old (deprecated)
output_format={"type": "json_schema", "schema": {...}}
# New
output_config={"format": {"type": "json_schema", "schema": {...}}}
```

#### 5. Interleaved Thinking Beta Header
`interleaved-thinking-2025-05-14` is deprecated on Opus 4.6 (safely ignored). Adaptive thinking enables interleaved thinking automatically. Sonnet 4.6 still supports the header for manual extended thinking.

### Critical Prompting Changes

#### REMOVE Anti-Laziness Prompts
This is the single biggest prompting change for Claude 4.6. Per Anthropic engineer testimony: "significant leaps in intelligence were observed as soon as anti-laziness prompts were removed."

**Delete these patterns:**
- "be thorough"
- "think carefully"
- "do not be lazy"
- "take your time"
- "be comprehensive"

These cause Claude 4.6 to overthink, loop, or write-then-rewrite.

#### SOFTEN Tool Instructions
Old workarounds for undertriggering now cause overtriggering.

```
# REMOVE
"CRITICAL: You MUST use this tool when..."
"If in doubt, use [tool]"

# REPLACE WITH
"Use this tool when it would enhance your understanding of the problem."
"Use [tool] when it would help."
```

#### REMOVE Explicit Think Tool Instructions
```
# REMOVE
"Use the think tool to plan your approach"

# Claude 4.6 thinks effectively without being told to
```

#### BE EXPLICIT About Actions
Claude 4.6 tends toward suggestion over implementation.

```
# Less effective (Claude will only suggest)
"Can you suggest some changes to improve this function?"

# More effective (Claude will act)
"Change this function to improve its performance."
"Make these edits to the authentication flow."
```

#### Use Effort as Primary Control Lever
If the model is still overly aggressive after prompt cleanup, lower the effort setting rather than adding more prompt constraints.

### New Capabilities

#### Fast Mode (Research Preview)
Up to 2.5x faster output at premium pricing ($30/$150 per MTok). Same model, faster inference.
```python
response = client.beta.messages.create(
    model="claude-opus-4-6",
    speed="fast",
    betas=["fast-mode-2026-02-01"],
    ...
)
```

#### Compaction API (Beta)
Server-side context summarization for effectively infinite conversations.

#### 128K Output Tokens (Opus 4.6)
Double the previous 64K limit. Requires streaming for large `max_tokens`.

#### Dynamic Web Filtering
Web search/fetch with code execution filtering (tool versions `web_search_20260209`, `web_fetch_20260209`).

#### Context Awareness
Models track remaining context window. For agent harnesses with compaction:
```
Your context window will be automatically compacted as it approaches its limit.
Do not stop tasks early due to token budget concerns.
Save progress to memory before context refreshes.
```

#### Subagent Orchestration
Claude 4.6 proactively delegates to subagents. May overuse them -- add guidance:
```
Use subagents when tasks can run in parallel or require isolated context.
For simple tasks, sequential operations, or single-file edits, work directly.
```

#### Parallel Tool Calling
Aggressive parallel execution. Steerable to ~100%:
```
If you intend to call multiple tools and there are no dependencies between
the calls, make all independent calls in parallel.
```

### Behavioral Notes

- **Communication style:** More concise, direct, grounded. Less verbose than previous models.
- **Overeagerness:** Tendency to overengineer (extra files, unnecessary abstractions). Add constraints.
- **LaTeX default:** Opus 4.6 defaults to LaTeX for math. Add explicit plain-text instructions if unwanted.
- **File creation:** May create temp files as scratchpads. Instruct cleanup if unwanted.
- **Overthinking:** Does significantly more upfront exploration, especially at high effort. Constrain with:
  ```
  Prioritize execution over deliberation. Choose one approach and start immediately.
  Do not compare alternatives or plan the entire solution before writing.
  ```

### Sonnet 4.6 Specific Notes

**Effort defaults:**
- `medium` for most applications
- `low` for high-volume or latency-sensitive
- 64K max output recommended at medium/high effort

**When to try adaptive thinking on Sonnet 4.6:**
- Autonomous multi-step agents (start at `high`)
- Computer use agents (best-in-class accuracy in adaptive mode)
- Bimodal workloads (mix of easy/hard tasks)

**For hard ceiling on thinking costs:** Use extended thinking with `budget_tokens` cap (~16K recommended) instead of adaptive.

**Sources:**
- Prompting best practices: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- What's new in Claude 4.6: https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-6
- Models overview: https://platform.claude.com/docs/en/about-claude/models/overview
- Introducing Opus 4.6: https://www.anthropic.com/news/claude-opus-4-6
- Sonnet 4.6 guide: https://www.nxcode.io/resources/news/claude-sonnet-4-6-complete-guide-benchmarks-pricing-2026

---

## Claude 4.x Family (Legacy Baseline)

**Note:** This section covers the Claude 4.x baseline (Sonnet 4.5, etc.) prior to Opus 4.6 / Sonnet 4.6. Much of this guidance still applies to Claude 4.6, but see the 4.6 section above for critical changes.

### Key Changes from Claude 3.x

| Aspect | Claude 3.x | Claude 4.x |
|--------|------------|------------|
| Verbosity | Naturally verbose | Concise by default |
| Tool calling | Conservative | Aggressive parallel execution |
| Instructions | Flexible interpretation | Precise, literal following |
| Action vs suggestion | Mixed | Tends toward suggestion |

### Prompting Adjustments

**Be directive:** Claude 4.x tends toward suggestion over action.
```
# Don't
"Can you suggest some changes to improve this function?"

# Do
"Change this function to handle edge cases. Implement the changes."
```

**Request detail explicitly:** Concise by default.
```
"Include as many relevant features as possible. Go beyond basics."
```

**Explain why:** Context helps Claude follow constraints better.
```
# Don't
"NEVER use ellipses in responses."

# Do
"Never use ellipses--they don't render in our text-to-speech system."
```

**Use positive framing:** Tell what TO do.
```
# Don't
"Do not use markdown formatting."

# Do
"Format your response as smoothly flowing prose paragraphs."
```

### Tool Use Notes

- Sonnet 4.5 aggressively executes parallel tool calls
- Overtriggering is more common than undertriggering
- Use balanced prompting (not "MUST use tool")

---

## Claude Opus 4.5 (Superseded by Opus 4.6)

**Released:** November 24, 2025
**Context:** 200K tokens
**Strengths:** Coding, agentic workflows, computer use
**Status:** Superseded by Opus 4.6 (Feb 2026). Still available but no longer the flagship.

### Specific Guidance

**Extended thinking:** Enable for complex STEM, coding, constraint optimization.
```
# Use high-level direction, not prescriptive steps
"Analyze this problem thoroughly before providing your solution."

# Avoid prescriptive steps that limit model creativity
```

**Agentic workflows:** For long-running agents, use two-agent pattern:
1. Initializer agent (runs once, establishes structure)
2. Coding agent (operates across sessions)

**State persistence:** Maintain across sessions:
- `features.json` for feature tracking (JSON > Markdown for stability)
- `progress.txt` for session logging
- Git commits for checkpoints

**API note:** Use `temperature` OR `top_p`, not both (causes errors in 4.5).

---

## Quick Reference

| Model | CoT Prompting | Few-Shot | System Prompt |
|-------|---------------|----------|---------------|
| Claude 4.6 (Opus/Sonnet) | Adaptive (effort parameter) | Helpful | Yes |
| Claude 4.x (Legacy) | Manual | Helpful | Yes |
| Claude Opus 4.5 | Extended thinking | Helpful | Yes |

---

*Last updated: February 2026*
