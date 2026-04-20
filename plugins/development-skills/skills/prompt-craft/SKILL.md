---
name: prompt-craft
description: USE WHEN improve prompt, write prompt, craft prompt, analyze prompt, prompt engineering, subagent prompts. Analyze, craft, and improve prompts using 19 research-backed techniques. Modes - Analyze (critique existing), Craft (build from scratch), Teach (explain techniques), Quick Fix (fast improvements).
---

# Prompt Craft

Diagnose why prompts underperform. Not a checklist service — a diagnostic practice. The default failure: "more instructions = better." Wrong. After a threshold, instructions degrade output (IFScale). Focus on what to REMOVE and ACTIVATE.

```
=== PROMPT CRAFT ===

MODES
A. Analyze    - Critique existing prompt, score techniques, suggest improvements
B. Craft      - Build optimized prompt from requirements
C. Teach      - Deep dive on a specific technique
D. Quick Fix  - Fast 3-improvement pass (minimal explanation)

CORE TECHNIQUES (1-10)
1. Chain-of-Thought   2. Structured Output   3. Few-Shot Examples
4. Placement          5. Salience            6. Roles
7. Positive Framing   8. Reasoning-First     9. Verbalized Sampling
10. Self-Reflection

EXTENDED: decomposition, compression, sufficiency, scope,
          format-spec, uncertainty, chaining, self-consistency,
          tree-of-thoughts, react-loop, tool-description-craft,
          context-engineering, multi-session

MODEL GUIDES: claude, openai, deepseek, gemini, kimi, qwen
              → See reference/models/{name}.md for model-specific prompting

Commands:
- A/B/C/D or mode name to begin
- 1-10 or technique name for Teach mode
- *model [name] - Load model-specific guidance (from reference/models/)
- *extended - Show extended techniques
- *help - Show this menu
```

---

## Mode Router

Detect the user's intent from context and route to the appropriate mode:
- Existing prompt provided -> **Analyze mode (A)**
- Requirements for new prompt -> **Craft mode (B)**
- Technique number/name -> **Teach mode (C)**
- Quick improvement request -> **Quick Fix mode (D)**

If unclear, ask which mode fits. Use `*help` to show the menu on demand.

---

## Mode A: Analyze

**Disposition:** Diagnose why this prompt will underperform. The failure mode is "checklist-completion" — noting what's present without naming what specific failure each absence causes. The diagnosis matters more than the score. Load reference files for techniques being applied.

**Competence note:** The common error is a scorecard that says "missing CoT" without explaining WHY that gap causes wrong answers for this specific task.

### Analyze Output Template

```
PROMPT ANALYSIS
===============

CURRENT PROMPT
--------------
[Quote user's prompt exactly]

TECHNIQUE SCORECARD
-------------------
| # | Technique | Status | Issue/Note |
|---|-----------|--------|------------|
| 1 | Chain-of-Thought | x/!/+/- | [Issue if x/!, "Good" if +, "N/A" if -] |
| 2 | Structured Output | | |
| 3 | Few-Shot | | |
| 4 | Placement | | |
| 5 | Salience | | |
| 6 | Roles | | |
| 7 | Positive Framing | | |
| 8 | Reasoning-First | | |
| 9 | Verbalized Sampling | | |
| 10 | Self-Reflection | | |

Legend: + Present | ! Partial | x Missing | - N/A for this task

TOP 3 IMPROVEMENTS
------------------
(Prioritize core techniques; include extended if highly relevant)

1. [Technique]: [Specific improvement]
   Before: [Original snippet]
   After: [Improved snippet]
   Why: [1-sentence explanation]

2. [Technique]: [Specific improvement]
   ...

3. [Technique]: [Specific improvement]
   ...

OPTIMIZED PROMPT
----------------
[Full rewritten prompt applying all improvements]

---------------------------------
QUALITY SUMMARY
- Improvement potential: [High/Medium/Low]
- Techniques applied: [List]
- Target model: [If specified, note model-specific adjustments]
---------------------------------

Next steps:
- Want me to explain any technique in depth? (Mode C)
- Want to iterate on the optimized prompt?
- Targeting a specific model? I can adjust for its quirks.
```

---

## Mode B: Craft

**Disposition:** Build a prompt that activates expert behavior. The common error: mechanically correct prompts that generate "probability-averaged centroid output" — the bland average of all expert responses.

**Process:**
1. **Elicit requirements** -- ASK the user these questions before drafting:
   - "What task should this prompt accomplish?"
   - "What model will run this? (Claude, GPT, DeepSeek, etc.)"
   - "What output format do you need?"
   - "Any specific constraints or requirements?"
   - "Should the prompt default to implementing or recommending?" (Action Bias)
   - "Is this a single-turn prompt or part of an agentic workflow?" (Context)
   - "Who is the audience? Expert peers, beginners, or mixed?" (Audience Priming)

   **Wait for answers before proceeding.** Don't assume.
   If the answer to #6 is "agentic workflow," apply the agentic template from the Agentic Prompting section.

2. Select techniques matching task type (reasoning -> CoT/Reasoning-First; structured data -> Structured Output/Format-Spec; complex -> Decomposition/Few-Shot; consistency -> Self-Reflection)
3. Draft, self-check against technique checklist, output with rationale

### Craft Output Template

```
CRAFTED PROMPT
==============

REQUIREMENTS UNDERSTOOD
-----------------------
- Task: [What the prompt should accomplish]
- Target model: [Claude/GPT/etc. or "general"]
- Output format: [Expected format]
- Constraints: [Any limitations]

TECHNIQUES APPLIED
------------------
- [Technique 1]: [Why it's relevant]
- [Technique 2]: [Why it's relevant]
- ...

THE PROMPT
----------
[Full optimized prompt]

RATIONALE
---------
[Brief explanation of key design choices]

---------------------------------
QUALITY SUMMARY
- Techniques applied: [Count]/10 core
- Model-specific: [Yes/No - what adjustments]
- Confidence: [High/Medium/Low]
---------------------------------

Next steps:
- Want to test this prompt and iterate?
- Should I explain any of the techniques used?
- Need a different approach?
```

---

## Mode C: Teach

Load `reference/[technique-name].md` for the requested technique. Present mechanism, deep example, model-specific notes. Offer practice exercise.

---

## Mode D: Quick Fix

Read, identify 3 highest-impact improvements, apply immediately, output with bullet-point changes. Speed over depth.

### Quick Fix Output Template

```
QUICK FIX
=========

CHANGES MADE
------------
- [Change 1]: [One-line description]
- [Change 2]: [One-line description]
- [Change 3]: [One-line description]

IMPROVED PROMPT
---------------
[Full improved prompt]

Want deeper analysis? Try mode A.
```

---

## Agentic Prompting

### Tool Description Optimization

See `reference/extended/tool-description-craft.md`. Make implicit context explicit, use human-readable return values, consolidate tools.

### Subagent Briefing Pattern

Every subagent prompt must include:
1. **Context** -- What the task is and why it matters
2. **Constraints** -- Time budget, scope limits, effort level
3. **Output format** -- What you need back, exactly
4. **Success criteria** -- How to know when done

### ReAct Loop Construction

Reason -> Act -> Observe -> Reason. See `reference/extended/react-loop.md`.

### Action Bias Selection

Choose one per prompt -- be explicit about what the agent should default to:
- **Proactive:** "Implement changes rather than suggesting them"
- **Conservative:** "Default to research and recommendations"
- **Balanced:** "Implement straightforward changes; recommend for complex ones"

### Context Window Management

See `reference/extended/context-engineering.md` and `reference/extended/multi-session.md`.
- Just-in-time loading over pre-loading
- Compaction strategies: summarize, clear tool results, full reset

### Clarity over Compulsion (Claude 4.6 and 4.7)

4.6's failure mode was over-triggering on "CRITICAL: You MUST…" language. 4.7's failure mode is the opposite: it follows literal MUST statements too rigidly and can ignore context signals that would soften the rule. Same direction of fix, different reason.

- Drop "CRITICAL: You MUST…" scaffolding — let the instruction stand on its own. Reserve CAPS imperatives for genuinely load-bearing rules (e.g., iron laws in systematic-debugging)
- Drop anti-laziness prompts ("be thorough", "don't be lazy") — both models execute proactively; the pressure causes overthinking
- Use the `effort` parameter for reasoning depth (xhigh for agentic work, high for knowledge work) instead of prompt-level simulation
- Drop explicit "think step by step" — adaptive thinking handles this; your prompt just competes with it
- Soften tool-triggering: "use when helpful" lets the model calibrate; "MUST use when X" fires literally and burns tokens on unnecessary calls
- At low/medium effort, 4.7 scopes tightly — add one targeted reasoning nudge where depth matters: "This step involves multi-step reasoning. Outline your logic before responding."

### Model-Specific Adjustments

When targeting a specific model, load `reference/models/{model}.md` and apply adjustments.

### Prompt Quality Gate

For high-stakes prompts (production, external APIs):
- [ ] Critical info at start or end (Placement)
- [ ] Constraints explicit and positive-framed
- [ ] Output format specified
- [ ] Model-specific adjustments applied (see `reference/models/`)
- [ ] Action bias declared
- [ ] Context budget considered

---

## Core Techniques Quick Reference

| # | Technique | Impact | One-Line Summary |
|---|-----------|--------|------------------|
| 1 | Chain-of-Thought | +40% accuracy | "Think step by step before answering" |
| 2 | Structured Output | 99%+ compliance | Constrain to JSON/XML schema |
| 3 | Few-Shot Examples | +15-30% specificity | Show 2-5 input/output examples |
| 4 | Placement | +50% retrieval | Critical info at start/end, not middle |
| 5 | Salience | +23-31% compliance | XML tags, caps, explicit labels |
| 6 | Roles | +10-20% domain accuracy | Assign persona with expertise |
| 7 | Positive Framing | +15-20% compliance | "Do X" instead of "Don't Y" |
| 8 | Reasoning-First | -20-30% hallucination | Evidence before conclusion |
| 9 | Verbalized Sampling | +1.6-2.1x diversity | Multiple variants with probabilities |
| 10 | Self-Reflection | +15-25% accuracy | Ask model to critique and revise |

**Failure if missing:** CoT → skips reasoning steps. Structured Output → format drift. Few-Shot → calibration gap. Placement → buried instructions. Salience → constraints overlooked. Roles → generic register. Positive Framing → constraint confusion. Reasoning-First → hallucinated conclusions. Verbalized Sampling → centroid output. Self-Reflection → uncaught errors.

**For deep dives:** Use Teach mode (C) or see `reference/[technique].md`

---

## Extended Techniques

Available in `reference/extended/`:

| Technique | When to Use |
|-----------|-------------|
| Decomposition | Break complex tasks into sequential steps |
| Compression | Reduce context size while preserving utility |
| Sufficiency | Ensure model has what it can't infer |
| Scope | Set explicit boundaries on what to include/exclude |
| Format-Spec | Provide exact output template |
| Uncertainty + Epistemic Labels | Confidence per claim: [E]vidence/[L]ogical/[S]peculation/[C]ontrarian |
| Chaining | Multi-stage prompts where outputs feed next stage |
| Self-Consistency | Multiple samples with majority voting |
| Tree-of-Thoughts | Explore multiple reasoning branches |
| ReAct Loop | Reason-Act-Observe cycles for tool-using agents |
| Tool Description Craft | Optimize tool/function descriptions for agents |
| Context Engineering | Curate optimal token set during inference |
| Multi-Session | State persistence across context windows |
| Negative Space Definition | Stack "this is NOT X" negations to close attractor basins |
| Permission Escalation | Graduated permission ladder to open RLHF-closed output regions |

---

## Model-Specific Guidance

**Command:** `*model [name]` or ask about prompting for a specific model.

**Available:** Claude, OpenAI (GPT-5.x, o1/o3), DeepSeek, Gemini, Kimi, Qwen

**Location:** `reference/models/{name}.md` (per-model files for JIT loading)

**Critical differences by model type:**

| Model Type | Chain-of-Thought | Few-Shot | System Prompt |
|------------|------------------|----------|---------------|
| Standard (Claude, GPT-5.x) | Add manually / use `reasoning.effort` | Helpful | Yes |
| Reasoning (o1/o3, R1) | **Built-in - don't add** | **Hurts performance** | Developer role |
| Agentic (Kimi K2) | Automatic | Varies | Goal-oriented |

---

## Checklist for Skill Authors

When creating prompts in skills or commands:

- [ ] Placed instructions at start or end (not middle)
- [ ] Used XML tags for important sections
- [ ] Stated what TO do (positive framing)
- [ ] Provided sufficient context
- [ ] Specified output format explicitly
- [ ] Considered target model's quirks
- [ ] Avoided ambiguous language
- [ ] Tested with representative inputs
