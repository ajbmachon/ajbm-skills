# Claude (Anthropic)

## Claude Opus 4.7 (current)

### Models & Specs

| Model | API ID | Context | Max Output | Pricing (in/out MTok) |
|-------|--------|---------|------------|----------------------|
| Claude Opus 4.7 | `claude-opus-4-7` | 1M (standard pricing) | 128K | $5 / $25 |
| Claude Opus 4.6 | `claude-opus-4-6` | 200K (1M beta) | 128K | $5 / $25 |
| Claude Sonnet 4.6 | `claude-sonnet-4-6` | 200K (1M beta) | 64K | $3 / $15 |
| Claude Haiku 4.5 | `claude-haiku-4-5-20251001` | 200K | 64K | $1 / $5 |

### Breaking Changes (Opus 4.7)

#### 1. Extended Thinking Removed
`thinking: {type: "enabled", budget_tokens: N}` returns a 400 error. Use adaptive thinking plus the `effort` parameter:

```python
client.messages.create(
    model="claude-opus-4-7",
    max_tokens=64000,
    thinking={"type": "adaptive"},
    output_config={"effort": "high"},  # or "max", "xhigh", "medium", "low"
    messages=[{"role": "user", "content": "..."}],
)
```

Adaptive thinking is **off by default** on 4.7 — requests with no `thinking` field run without thinking (matching 4.6 behavior). Set `thinking: {type: "adaptive"}` explicitly to enable it.

#### 2. Sampling Parameters Removed
`temperature`, `top_p`, `top_k` set to any non-default value return 400. Omit these parameters entirely. Use prompting to guide behavior.

#### 3. Thinking Content Omitted by Default
Thinking blocks appear in the response stream but the `thinking` field is empty unless you opt in:
```python
thinking = {"type": "adaptive", "display": "summarized"}
```
Without this, streaming UIs see a long pause before output begins instead of visible progress.

#### 4. New Tokenizer (~1x to 1.35x more tokens)
Same text counts 0–35% more tokens than on 4.6. Update `max_tokens` for headroom. The 1M context window is standard-priced with no long-context premium.

#### 5. Prefill Removal (carried over from 4.6)
Prefilling assistant messages returns 400. Use `output_config.format`, system prompt instructions, or structured outputs instead.

### Effort Parameter (Opus 4.7)

4.7 respects effort **strictly**, especially at the low end. At low/medium it scopes to what was asked rather than going above and beyond. Choose carefully:

| Effort | Use For |
|--------|---------|
| **`max`** | Intelligence-demanding tasks; test for diminishing returns from increased tokens. Can over-think. |
| **`xhigh`** (new) | Coding and agentic use cases — the recommended default for these |
| **`high`** | Minimum for intelligence-sensitive work — balances tokens and capability |
| **`medium`** | Cost-sensitive tasks; scopes tightly, may under-think complex problems |
| **`low`** | Short, scoped, latency-sensitive tasks only |

If 4.7 is under-thinking at low/medium on a complex problem, **raise effort to high/xhigh** rather than adding prompt nudges. If effort must stay low for latency, add a targeted nudge: "This task involves multi-step reasoning. Think carefully through the problem before responding."

### Behavioral Changes (4.7 vs 4.6)

These are not API breaking changes but may require prompt updates:

#### Response Length Calibrates to Complexity
4.7 shortens simple lookups and lengthens open-ended analysis. Drop fixed verbosity scaffolding. If you need concision, state it positively: "Provide focused responses. Skip non-essential context. Keep examples minimal."

#### More Literal Instruction Following
Especially at lower effort. 4.7 will not silently generalize from one example to another, and will not infer requests you didn't make. Upside: precision and less thrash. Downside: carefully tuned prompts are rewarded; vague ones get taken literally.

#### More Direct Tone
Less validation-forward phrasing ("I understand your concern"), fewer emoji, more opinionated stance. If your product relies on a warmer voice, re-evaluate style prompts — you may need to explicitly permission-escalate softer register (see `tactical-empathy` skill's Permission Escalation pattern).

#### Built-in Progress Updates
4.7 provides regular user-facing updates during long agentic traces natively. **Remove** scaffolding like "After every 3 tool calls, summarize progress" — it competes with the native behavior.

#### Fewer Subagents by Default
4.7 spawns fewer subagents unaided. If your workflow needs subagents, make the triggers explicit: "Spawn an Explore agent when: (a) codebase search needed, (b) external docs to verify, (c) task parallelizable across independent files."

#### Fewer Tool Calls by Default
4.7 uses reasoning more, tools less — usually this improves results. For scenarios where you want more tool use, raise effort (xhigh shows substantially more tool usage) and/or instruct explicit triggering conditions.

#### Cybersecurity Safeguards
Prohibited/high-risk cyber topics may refuse. Legitimate pentesting/research: apply to the Cyber Verification Program.

#### High-Resolution Image Support
Max image resolution 2576px on long edge (up from 1568). Automatic — no beta header needed. Full-res images use ~3x more image tokens (up to 4,784/image). Re-budget `max_tokens` for image-heavy workloads; downsample if fidelity isn't needed. Model-returned pointing/bounding-box coordinates are 1:1 with actual pixels — no scale factor to apply.

### Recommended Changes (Opus 4.7)

1. **Re-evaluate `max_tokens`** — heavier tokenizer + adaptive length means old ceilings may truncate
2. **Audit token-count estimations** — any client-side token math needs re-testing
3. **Adopt task budgets (beta)** for agentic workloads where the model should self-moderate toward a ceiling:
   ```python
   output_config = {
       "effort": "high",
       "task_budget": {"type": "tokens", "total": 128000},
   }
   # beta header: task-budgets-2026-03-13
   ```
   Minimum 20k. Not a hard cap — the model sees a running countdown. Distinct from `max_tokens` which is a hard per-request ceiling.
4. **Set max_tokens ≥ 64k** at `max` or `xhigh` effort — the model needs headroom to think and act across tool calls

### Critical Prompting Changes

#### DROP Anti-Laziness Prompts
Biggest prompting change for 4.6 that extends to 4.7. Per Anthropic engineer testimony: *"significant leaps in intelligence were observed as soon as anti-laziness prompts were removed."*

**Delete these patterns:** "be thorough", "think carefully", "do not be lazy", "take your time", "be comprehensive". On 4.6 they caused over-thinking. On 4.7 they fight the model's literal-interpretation bias.

#### SOFTEN Tool Instructions
```
# DROP:    "CRITICAL: You MUST use this tool when..."
# REPLACE: "Use this tool when it would help."
```
4.7 follows MUST statements too literally and can ignore context signals that would soften the rule. Same fix direction as 4.6, different reason.

#### DROP Explicit "Think Step by Step"
Adaptive thinking handles this. Your prompt just competes with it.

#### BE EXPLICIT About Actions
4.7 follows literal directives cleanly. Use directive language: "Change this function" not "Can you suggest changes?"

#### Use Effort as Primary Control Lever
Raise effort when the model under-thinks. Lower effort when cost matters. Don't compensate with prompt constraints.

### Behavioral Notes

- More concise, direct, grounded than 4.6
- Overengineering tendency persists (extra files, unnecessary abstractions) — add explicit scope constraints
- Defaults to LaTeX for math — add plain-text instructions if unwanted
- At high/xhigh effort, does significantly more upfront exploration — constrain with "Prioritize execution over deliberation" when you want action over analysis

---

## Claude 4.6 Family (legacy reference)

The 4.6 guidance below is preserved for projects still targeting 4.6. For 4.7, all of the above supersedes.

### Breaking Changes (Opus 4.6)

Prefill removal: same as 4.7.

Adaptive thinking: `thinking: {type: "adaptive"}` available; `budget_tokens` deprecated.

Effort parameter (4.6 levels): `max` (Opus only) > `high` (default) > `medium` > `low`. Note 4.7 added `xhigh`.

`output_config.format` replaces `output_format`.

### Sonnet 4.6

- Default effort: `medium` (most apps), `low` (latency-sensitive)
- Adaptive thinking excels at: autonomous agents, computer use, bimodal workloads
- For hard cost ceiling: extended thinking with `budget_tokens` cap (~16K) — still works on 4.6 Sonnet

### 4.6 Behavioral Notes

- More concise, direct, grounded than earlier families
- Overengineering tendency — add constraints
- Prompting changes from 4.5→4.6 match most of the 4.7 prompting changes above (anti-laziness removal, soften MUST, drop think-step-by-step)

---

## Quick Reference

| Model | CoT Prompting | Few-Shot | System Prompt | Effort |
|-------|---------------|----------|---------------|--------|
| Claude Opus 4.7 | Adaptive (effort) | Helpful | Yes | xhigh for coding, high default |
| Claude Opus 4.6 | Adaptive (effort) | Helpful | Yes | high default |
| Claude Sonnet 4.6 | Adaptive (effort) | Helpful | Yes | medium default, low for latency |
| Claude Haiku 4.5 | Adaptive (effort) | Helpful | Yes | low-medium |
