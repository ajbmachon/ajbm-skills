---
name: prompt-craft
description: USE WHEN improve prompt, write prompt, craft prompt, analyze prompt, prompt engineering, subagent prompts. Analyze, craft, and improve prompts using 19 research-backed techniques. Modes - Analyze (critique existing), Craft (build from scratch), Teach (explain techniques), Quick Fix (fast improvements).
---

# Prompt Craft

Master the art and science of prompting through research-backed techniques.

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
- Existing prompt provided → **Analyze mode (A)**
- Requirements for new prompt → **Craft mode (B)**
- Technique number/name → **Teach mode (C)**
- Quick improvement request → **Quick Fix mode (D)**

If unclear, ask which mode fits. Use `*help` to show the menu on demand.

**Interactive principle:** Guide the user through each mode. Ask clarifying questions before producing output. Don't assume—ask.

---

## Mode A: Analyze

**Purpose:** Critique an existing prompt using the technique checklist.

**Process:**
1. Read the user's prompt carefully
2. Score against each core technique (present/partial/absent)
3. Identify the top 3 highest-impact improvements
4. Provide before/after examples for each improvement
5. Output the optimized prompt

**Load reference files as needed** for techniques being applied.

### Analyze Output Template

```
PROMPT ANALYSIS
═══════════════

CURRENT PROMPT
──────────────
[Quote user's prompt exactly]

TECHNIQUE SCORECARD
───────────────────
| # | Technique | Status | Issue/Note |
|---|-----------|--------|------------|
| 1 | Chain-of-Thought | ❌/⚠️/✅/— | [Issue if ❌⚠️, "Good" if ✅, "N/A" if —] |
| 2 | Structured Output | | |
| 3 | Few-Shot | | |
| 4 | Placement | | |
| 5 | Salience | | |
| 6 | Roles | | |
| 7 | Positive Framing | | |
| 8 | Reasoning-First | | |
| 9 | Verbalized Sampling | | |
| 10 | Self-Reflection | | |

Legend: ✅ Present | ⚠️ Partial | ❌ Missing | — N/A for this task

TOP 3 IMPROVEMENTS
──────────────────
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
────────────────
[Full rewritten prompt applying all improvements]

─────────────────────────────────
QUALITY SUMMARY
• Improvement potential: [High/Medium/Low]
• Techniques applied: [List]
• Target model: [If specified, note model-specific adjustments]
─────────────────────────────────

Next steps:
- Want me to explain any technique in depth? (Mode C)
- Want to iterate on the optimized prompt?
- Targeting a specific model? I can adjust for its quirks.
```

---

## Mode B: Craft

**Purpose:** Build an optimized prompt from scratch based on requirements.

**Process:**
1. **Elicit requirements** — ASK the user these questions before drafting:
   - "What task should this prompt accomplish?"
   - "What model will run this? (Claude, GPT, DeepSeek, etc.)"
   - "What output format do you need?"
   - "Any specific constraints or requirements?"
   - "Should the prompt default to implementing or recommending?" (Action Bias)
   - "Is this a single-turn prompt or part of an agentic workflow?" (Context)

   **Wait for answers before proceeding.** Don't assume.
   If the answer to #6 is "agentic workflow," apply the agentic template from the Agentic Prompting section.

2. **Select applicable techniques** based on task type:
   - Reasoning tasks → Chain-of-Thought, Reasoning-First
   - Structured data → Structured Output, Format-Spec
   - Complex tasks → Decomposition, Few-Shot
   - Consistency needs → Self-Reflection, Self-Consistency

3. **Draft the prompt** applying selected techniques

4. **Self-check** against technique checklist

5. **Output** the prompt with rationale

### Craft Output Template

```
CRAFTED PROMPT
══════════════

REQUIREMENTS UNDERSTOOD
───────────────────────
• Task: [What the prompt should accomplish]
• Target model: [Claude/GPT/etc. or "general"]
• Output format: [Expected format]
• Constraints: [Any limitations]

TECHNIQUES APPLIED
──────────────────
• [Technique 1]: [Why it's relevant]
• [Technique 2]: [Why it's relevant]
• ...

THE PROMPT
──────────
[Full optimized prompt]

RATIONALE
─────────
[Brief explanation of key design choices]

─────────────────────────────────
QUALITY SUMMARY
• Techniques applied: [Count]/10 core
• Model-specific: [Yes/No - what adjustments]
• Confidence: [High/Medium/Low]
─────────────────────────────────

Next steps:
- Want to test this prompt and iterate?
- Should I explain any of the techniques used?
- Need a different approach?
```

---

## Mode C: Teach

**Purpose:** Deep dive on a single technique with mechanism, examples, and practice.

**Process:**
1. Identify which technique (1-10 or name)
2. **Load the reference file** for that technique
3. Present the content following the reference structure
4. Offer a practice exercise

**Reference files:** See `reference/[technique-name].md`

### Teach Output Structure

```
TECHNIQUE: [Name]
═════════════════

[Content from reference file, including:]
- Mechanism (why it works)
- When to use / when NOT to use
- Shallow vs Deep examples
- Common mistakes
- Self-check questions

PRACTICE EXERCISE
─────────────────
[A concrete exercise to apply this technique]

Want to try it? Paste a prompt and I'll help you apply [technique].
```

---

## Mode D: Quick Fix

**Purpose:** Fast improvement pass with minimal explanation. Speed over depth.

**Process:**
1. Read the prompt
2. Identify the **3 highest-impact** improvements (don't score everything)
3. Apply them immediately
4. Output improved prompt with bullet-point changes

**Time budget:** Mental model of <30 seconds. No lengthy analysis.

### Quick Fix Output Template

```
QUICK FIX
═════════

CHANGES MADE
────────────
• [Change 1]: [One-line description]
• [Change 2]: [One-line description]
• [Change 3]: [One-line description]

IMPROVED PROMPT
───────────────
[Full improved prompt]

Want deeper analysis? Try mode A.
```

---

## Agentic Prompting

When Claude or any agent is writing prompts for subagents, tool descriptions, or agentic loops.

### Tool Description Optimization

The highest-leverage prompt surface for agents. See `reference/extended/tool-description-craft.md`.
Key principle: write descriptions as if explaining to a new team member.
- Make implicit context explicit; define niche terminology
- Use human-readable return values (name > UUID)
- Consolidate tools (fewer > many granular); namespace consistently
- Use Claude to optimize its own tool descriptions (meta-pattern)

### Subagent Briefing Pattern

Every subagent prompt must include:
1. **Context** — What the task is and why it matters
2. **Constraints** — Time budget, scope limits, effort level
3. **Output format** — What you need back, exactly
4. **Success criteria** — How to know when done

### ReAct Loop Construction

For agents that use tools: Reason → Act → Observe → Reason...
See `reference/extended/react-loop.md` for templates and the Reason-Plan-ReAct variant.
- Single-prompt ReAct for simple tool chains
- Multi-turn ReAct for complex workflows
- Model-specific: Claude auto-delegates; GPT needs explicit structure

### Action Bias Selection

Choose one per prompt — be explicit about what the agent should default to:
- **Proactive:** "Implement changes rather than suggesting them"
- **Conservative:** "Default to research and recommendations"
- **Balanced:** "Implement straightforward changes; recommend for complex ones"

### Context Window Management

Agents accumulate context across turns. Apply:
- Just-in-time loading (load via tools, don't pre-load everything)
- Compaction strategies (summarize, clear tool results, full reset)
- State persistence (JSON > markdown for structured state across sessions)
- See `reference/extended/context-engineering.md` and `reference/extended/multi-session.md`

### Anti-Overtriggering (Claude 4.6+)

Modern models need FEWER instructions, not more:
- Remove "CRITICAL: You MUST..." language — causes overtriggering
- Remove anti-laziness prompts ("be thorough", "don't be lazy") — causes overthinking
- Use effort parameter instead of prompt-level reasoning simulation
- Remove explicit think tool instructions — Claude 4.6 thinks adaptively
- Soften tool-use language: "use when helpful" not "MUST use when..."

### Model-Specific Adjustments

When targeting a specific model, load `reference/models/{model}.md` and apply adjustments.
Key differences: Claude prefers directive language; GPT-5.x uses reasoning effort + verbosity controls;
o1/o3 uses developer role (no CoT prompts); DeepSeek R1 uses user message only;
Gemini places query at END; Kimi is goal-oriented; Qwen uses ChatML format.

### Prompt Quality Gate

For high-stakes prompts (production, external APIs):
- [ ] Critical info at start or end (Placement)
- [ ] Constraints explicit and positive-framed
- [ ] Output format specified
- [ ] Model-specific adjustments applied (see `reference/models/`)
- [ ] Action bias declared
- [ ] Context budget considered

For programmatic prompt generation and templates, see the **Prompting skill**.
For reusable domain-specific prompt patterns, see the **Fabric skill**.

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
| Uncertainty | Request confidence levels |
| Chaining | Multi-stage prompts where outputs feed next stage |
| Self-Consistency | Multiple samples with majority voting |
| Tree-of-Thoughts | Explore multiple reasoning branches |
| ReAct Loop | Reason-Act-Observe cycles for tool-using agents |
| Tool Description Craft | Optimize tool/function descriptions for agents |
| Context Engineering | Curate optimal token set during inference |
| Multi-Session | State persistence across context windows |

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
