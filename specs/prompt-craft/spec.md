# Prompt-Craft Skill Improvement Spec

**Generated:** 2026-02-21 via Interview/Ideation
**Source:** Agentic prompting research (2025-2026), Fabric comparison, Prompting skill comparison
**Working log:** ./interview-log-prompt-craft-improvements.md

---

## Problem Statement

Prompt-craft's 19-technique taxonomy and 4-mode system is solid for single-turn prompt engineering, but the 2025-2026 shift toward agentic AI workloads has created significant gaps. The skill lacks coverage for: context engineering, tool description optimization, ReAct loop patterns, multi-session state management, and Claude 4.6-specific changes. Additionally, the monolithic models.md (630 lines) wastes context on irrelevant model guidance, the mode router is over-directive for modern models, and the Salience technique conflicts with the Prompting skill's markdown-only mandate.

## Objective

Evolve prompt-craft into a technique reference that serves both human prompt engineers and AI agents writing prompts, while staying focused (under 500 lines in SKILL.md) and complementary to the Prompting and Fabric skills.

## Success Criteria

- [ ] 4 new extended techniques added with reference files
- [ ] Agentic Self-Use section expanded to ~80 lines with real depth
- [ ] models.md split into 6 per-model files under reference/models/
- [ ] Claude model file updated for 4.6 (adaptive thinking, effort parameter, anti-laziness, prefill deprecation)
- [ ] Salience reference updated with model-conditional guidance
- [ ] Roles reference updated to reflect diminishing returns on modern models
- [ ] Mode router simplified (remove "ALWAYS show menu" directive)
- [ ] Craft mode (B) updated with action bias and agentic template
- [ ] Cross-references to Prompting and Fabric skills added
- [ ] SKILL.md stays under 500 lines
- [ ] chaining.md updated with agentic pipeline patterns

---

## Constraint Registry

**Captured:** 2026-02-21 during Devil's Advocate phase
**Confirmed by:** Andre Machon

### Hard Constraints (Immutable)

| # | Constraint | Source | Notes |
|---|------------|--------|-------|
| H1 | Keep 19-technique taxonomy as backbone | User stated | Can update/modify individual techniques but structure stays |
| H2 | No pattern library mode | User stated | Fabric handles reusable pattern catalogs |
| H3 | No meta-prompting duplication | User stated | Prompting skill handles templates/Handlebars |
| H4 | SKILL.md stays under ~500 lines | User confirmed | Currently 375; budget ~125 lines for expansion |
| H5 | Verbalized Sampling stays core | User stated | User values this technique highly |

### Soft Constraints (Preferences)

| # | Constraint | Negotiable If | Notes |
|---|------------|---------------|-------|
| S1 | Model-conditional XML/markdown guidance | Strong model-specific evidence | Different models, different best practices |
| S2 | New techniques in reference/ files | Technique is trivially small | Keeps SKILL.md lean |
| S3 | Cross-reference sibling skills, don't duplicate | No sibling skill covers it | Prompting + Fabric |

### Boundaries (Out of Scope)

| # | What's Excluded | Reason |
|---|-----------------|--------|
| B1 | Handlebars template system | Prompting skill covers this |
| B2 | 240+ pattern catalog | Fabric skill covers this |
| B3 | Full context engineering course | Brief philosophical note only |

---

## Interview Record

### Theme 1: Scope & Direction

**Q: Should prompt-craft stay focused or evolve broadly?**
A: Focused expansion. Keep the 19-technique taxonomy. Add 3-5 agentic techniques. Update model guidance. No pattern libraries or meta-prompting.

**Q: Who is the audience?**
A: Both humans AND AI agents equally. Expand Agentic Self-Use significantly with tool description optimization, subagent briefing patterns, ReAct construction.

### Theme 2: Specific Improvements

**Q: Which new techniques?**
A: All four — ReAct Loop Pattern, Tool Description Craft, Context Engineering, Multi-Session State. All as extended techniques with reference files.

**Q: Which existing content updates?**
A: All four — Salience (XML/markdown fix), Models.md refresh, Agentic Self-Use overhaul, Craft mode (Mode B). Plus: mode router simplification and model file split.

### Theme 3: Structural Decisions

**Q: Agentic section: inline or reference file?**
A: Inline expansion (~80 lines in SKILL.md). Keep it immediately visible.

**Q: Model file structure?**
A: Per-model files: reference/models/claude.md, reference/models/openai.md, etc. JIT loading — Claude reads only the relevant file.

**Q: XML vs markdown conflict?**
A: Model-conditional. Markdown for Claude 4.x. XML for GPT/Gemini. Both valid for their contexts.

### Theme 4: Technique Freshness

**Q: Any stale techniques to remove/modify?**
A: Update Roles (#6) reference to reflect diminishing returns on modern models. Keep all 10 core techniques. Verbalized Sampling stays core.

---

## Changes Manifest

### NEW FILES (4 extended technique reference files)

#### 1. `reference/extended/react-loop.md`
**Research basis:** ReAct is the foundational agentic pattern (Machine Learning Mastery 2025, Anthropic 2024). Reason-Plan-ReAct variant (arXiv:2512.03560) separates planner from executor.

**Content should cover:**
- The Reason-Act-Observe loop pattern
- When to use single-prompt ReAct vs multi-turn
- Reason-Plan-ReAct variant (planner + executor separation)
- Prompt templates for each stage
- Common failures (losing the plan in long chains)
- Model-specific notes (Claude auto-delegates, GPT needs explicit structure)

#### 2. `reference/extended/tool-description-craft.md`
**Research basis:** Anthropic Sep 2025: "Even small refinements to tool descriptions can yield dramatic improvements." Highest-leverage prompt surface for agents.

**Content should cover:**
- Write descriptions as if explaining to a new team member
- Make implicit context explicit, define niche terminology
- Use human-readable return values (name > UUID)
- Expose response_format parameters
- Consolidate tools (fewer > many granular)
- Namespace tools consistently (e.g., asana_search)
- Use Claude to optimize its own tool descriptions (meta-pattern)
- Before/after examples

#### 3. `reference/extended/context-engineering.md`
**Research basis:** Anthropic Sep 2025: Context engineering = "the set of strategies for curating and maintaining the optimal set of tokens during LLM inference." Google Dec 2025: tiered context (hot/warm/cold).

**Content should cover:**
- Context = system prompt + tools + memory + history + retrieved docs
- Token budget as finite resource
- Just-in-time loading vs pre-loading
- Compaction strategies (summarize, clear tool results, full reset)
- Tiered context (hot: current conversation, warm: recent tool outputs, cold: long-term memory)
- Progressive disclosure through exploration
- When to compact vs fresh context reset (Claude 4.5+ excels at filesystem rediscovery)

#### 4. `reference/extended/multi-session.md`
**Research basis:** Anthropic Nov 2025: "Effective harnesses for long-running agents." Two-agent architecture (initializer + coding agent).

**Content should cover:**
- JSON state tracking (more robust than markdown for models)
- Progress files (features.json, progress.txt)
- Git checkpoints as rollback points
- Session startup checklist (pwd, read logs, read progress, run test)
- Fresh-context-vs-degraded-context tradeoff
- Context window awareness prompting ("save state before compaction")
- Two-agent harness pattern (initializer + worker)

### NEW FILES (6 per-model files, replacing models.md)

#### `reference/models/claude.md`
Content from existing Claude sections PLUS Claude 4.6 additions:
- Remove anti-laziness prompts (causes runaway thinking on 4.6)
- Soften tool-use language ("use when" not "MUST use")
- Remove explicit think tool instructions
- Effort parameter as primary quality control lever
- Adaptive thinking (`thinking: {type: "adaptive"}`) replaces manual budget_tokens
- Prefilled responses deprecated in 4.6
- Opus 4.6 / Sonnet 4.6 / Haiku 4.5 model IDs
- Anti-overtriggering: knowing when to REMOVE instructions

#### `reference/models/openai.md`
Existing GPT-5.2, GPT-5.1, GPT-4o, o1/o3 content (moved as-is, no major changes needed)

#### `reference/models/deepseek.md`
Existing DeepSeek V3 and R1 content (moved as-is)

#### `reference/models/gemini.md`
Existing Gemini 2.0 content (moved as-is)

#### `reference/models/kimi.md`
Existing Kimi K2 content (moved as-is)

#### `reference/models/qwen.md`
Existing Qwen 2.5 content (moved as-is)

### MODIFIED FILES

#### `SKILL.md` — Mode Router (lines 41-53)
**Change:** Remove "ALWAYS start by showing the menu" directive. Replace with contextual routing:

```
## Mode Router

Detect the user's intent from context and route to the appropriate mode:
- Existing prompt provided → Analyze mode (A)
- Requirements for new prompt → Craft mode (B)
- Technique number/name → Teach mode (C)
- Quick improvement request → Quick Fix mode (D)

If unclear, ask which mode fits. Use `*help` to show the menu on demand.
```

#### `SKILL.md` — Extended Techniques list (lines 25-26)
**Change:** Add 4 new entries:

```
EXTENDED: decomposition, compression, sufficiency, scope,
          format-spec, uncertainty, chaining, self-consistency,
          tree-of-thoughts, react-loop, tool-description-craft,
          context-engineering, multi-session
```

#### `SKILL.md` — Model Guides section (lines 28-29)
**Change:** Update to reflect per-model files:

```
MODEL GUIDES: claude, openai, deepseek, gemini, kimi, qwen
              → See reference/models/{name}.md for model-specific prompting
```

#### `SKILL.md` — Agentic Self-Use section (lines 265-304)
**Change:** Complete overhaul. Expand from 40 lines to ~80 lines. New content:

```markdown
## Agentic Prompting

When Claude or any agent is writing prompts for subagents, tool descriptions, or agentic loops.

### Tool Description Optimization
The highest-leverage prompt surface for agents. See reference/extended/tool-description-craft.md.
Key principle: write descriptions as if explaining to a new team member.

### Subagent Briefing Pattern
Every subagent prompt must include:
1. **Context** — What the task is and why it matters
2. **Constraints** — Time budget, scope limits, effort level
3. **Output format** — What you need back, exactly
4. **Success criteria** — How to know when done

### ReAct Loop Construction
For agents that use tools: Reason → Act → Observe → Reason...
See reference/extended/react-loop.md for templates.

### Action Bias Selection
Choose one per prompt:
- **Proactive:** "Implement changes rather than suggesting them"
- **Conservative:** "Default to research and recommendations"

### Context Window Management
Agents accumulate context across turns. Apply:
- Just-in-time loading (load via tools, don't pre-load)
- Compaction strategies (summarize, clear tool results)
- State persistence (JSON > markdown for structured state)
See reference/extended/context-engineering.md

### Anti-Overtriggering (Claude 4.6+)
Modern models need FEWER instructions, not more:
- Remove "CRITICAL: You MUST..." language
- Remove anti-laziness prompts ("be thorough", "don't be lazy")
- Use effort parameter instead of prompt-level reasoning simulation
- Remove explicit think tool instructions

### Prompt Quality Gate
For high-stakes prompts (production, external APIs):
- [ ] Critical info at start or end
- [ ] Constraints explicit and positive-framed
- [ ] Output format specified
- [ ] Model-specific adjustments applied (see reference/models/)
- [ ] Action bias declared
- [ ] Context budget considered

For programmatic prompt generation and templates, see the **Prompting skill**.
For reusable domain-specific prompt patterns, see the **Fabric skill**.
```

#### `SKILL.md` — Craft Mode (B) elicitation questions (lines 136-140)
**Change:** Add two new questions:

```
5. "Should the prompt default to implementing or recommending?" (Action Bias)
6. "Is this a single-turn prompt or part of an agentic workflow?" (Context)
```

Add agentic template variant to output when answer is "agentic workflow."

#### `reference/salience.md`
**Change:** Add model-conditional guidance section:

```markdown
## Model-Conditional Guidance

Salience mechanisms differ by model:

| Model Family | Primary Salience | Notes |
|---|---|---|
| Claude 4.x | **Markdown headers** | Claude prefers markdown over XML. Use ## headers for section breaks, **bold** for emphasis, CAPS for critical terms. |
| GPT-4o / GPT-5.x | **XML tags or delimiters** | Responds well to <context>, <instructions> tags and triple-quoted delimiters. |
| Gemini 2.0 | **Markdown or XML** | Both work. Place query at END for long contexts. |
| o1/o3 | **Delimiters and headings** | Use structure to separate task, context, constraints. |
| DeepSeek R1 | **Markdown headers** | All instructions in user message. Use ## headers for structure. |

**Default:** Markdown headers are the most universally effective. Use model-specific salience only when targeting a specific model.
```

#### `reference/roles.md`
**Change:** Add effectiveness update section:

```markdown
## 2025-2026 Effectiveness Update

Role prompting has **diminishing returns on modern models:**
- Claude 4.6 is personality-aware by default — explicit role assignment adds less than it did in 2023
- GPT-5.x: "Persona alone won't add knowledge" — personas shape tone, not capability
- Most effective when: domain-specific terminology matters, output style needs to match a persona, the role constrains what IS and ISN'T relevant

**When roles still matter:**
- Specialized domains (legal, medical, security analysis)
- Teaching scenarios where voice matters
- Multi-agent systems where role differentiation drives different outputs
- Non-English contexts where role framing improves quality

**When to skip roles:**
- Generic tasks where the model's default is fine
- When you'd just say "You are a helpful assistant" (adds nothing)
- When the role would be "You are an expert at X" for a task the model already handles well
```

#### `reference/extended/chaining.md`
**Change:** Add agentic pipeline section:

```markdown
## Agentic Pipeline Patterns

For agent-to-agent chaining (subagent orchestration):

### Input/Output Contracts
Each stage should define:
- **Input schema:** What data format the stage expects
- **Output schema:** What data format the stage produces
- **Success signal:** How to know the stage completed correctly

### Agent Handoff Template
When passing context between agents:
1. What was accomplished (not the full transcript)
2. What state exists (file paths, data structures)
3. What the next agent must NOT re-do
4. What constitutes completion for the next stage

### Multi-Context-Window Chaining
When a chain spans context window boundaries:
- Use structured state files (JSON > text) at each boundary
- Each new context starts by reading state, not resuming conversation
- Include a startup checklist: read state, verify environment, run baseline test
```

### DELETED FILES

#### `reference/models.md`
Replaced by 6 per-model files in `reference/models/`. Delete after migration.

---

## Tradeoffs & Decisions

| Decision | Alternatives Considered | Why This Choice |
|----------|------------------------|-----------------|
| Focused expansion (not overhaul) | Full overhaul, phased rollout | Preserves what works; minimizes risk; stays under 500 lines |
| Model-conditional XML/markdown | Markdown-only, leave as-is | prompt-craft serves 8+ models; XML IS correct for some |
| Per-model files (not TOC) | Single file with TOC/offsets | Cleaner JIT loading; Claude reads one file not 630 lines |
| Inline agentic expansion | Reference file | User wants immediate visibility; worth the line budget |
| Keep all 10 core techniques | Demote Roles and/or VS | User values Verbalized Sampling; Roles still useful for domains |
| All-at-once implementation | Phased rollout | User preference; coherent single update |

---

## Assumption Corrections

| Original Assumption | Who Held It | Correction | Source |
|---------------------|-------------|------------|--------|
| XML tags are universally good for salience | prompt-craft SKILL.md | Claude 4.x prefers markdown headers | Prompting/Standards.md, Anthropic best practices |
| Role prompting is a top-10 technique | prompt-craft (2023 research) | Diminishing returns on 2025-2026 models | GPT-5.x docs, Claude 4.6 behavioral changes |
| "Always show menu" is good UX | prompt-craft mode router | Over-directive for modern models; Claude 4.6 can contextually route | Anti-overtriggering research finding |
| models.md as single file is fine | prompt-craft structure | 630 lines wastes context; JIT loading per model is better | Context engineering research |

---

## Open Questions

- [ ] **Technique numbering**: If 4 extended techniques are added, should the extended list be numbered (11-23) for Teach mode consistency, or stay name-only?
  - Fallback: Keep name-only for extended (current pattern)

- [ ] **Chaining.md vs react-loop.md overlap**: ReAct is technically a form of chaining. Should react-loop.md reference chaining.md or be fully standalone?
  - Fallback: Standalone with a "See also: chaining" cross-reference

---

## Implementation File Manifest

| Action | File | Lines Changed (est.) |
|--------|------|---------------------|
| CREATE | reference/extended/react-loop.md | ~120 new |
| CREATE | reference/extended/tool-description-craft.md | ~100 new |
| CREATE | reference/extended/context-engineering.md | ~100 new |
| CREATE | reference/extended/multi-session.md | ~100 new |
| CREATE | reference/models/claude.md | ~80 (migrated + 4.6 additions) |
| CREATE | reference/models/openai.md | ~180 (migrated from models.md) |
| CREATE | reference/models/deepseek.md | ~80 (migrated) |
| CREATE | reference/models/gemini.md | ~60 (migrated) |
| CREATE | reference/models/kimi.md | ~60 (migrated) |
| CREATE | reference/models/qwen.md | ~60 (migrated) |
| EDIT | SKILL.md (mode router) | -12, +8 |
| EDIT | SKILL.md (extended list) | +2 |
| EDIT | SKILL.md (model guides) | -2, +2 |
| EDIT | SKILL.md (agentic section) | -40, +80 |
| EDIT | SKILL.md (craft mode) | +8 |
| EDIT | SKILL.md (cross-references) | +3 |
| EDIT | reference/salience.md | +20 |
| EDIT | reference/roles.md | +25 |
| EDIT | reference/extended/chaining.md | +30 |
| DELETE | reference/models.md | -630 |
| **NET SKILL.md** | | **~393 lines (within H4 budget)** |

---

## Sources

All improvements are traceable to research:

- [Effective context engineering for AI agents (Anthropic, Sep 2025)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Writing effective tools for AI agents (Anthropic, Sep 2025)](https://www.anthropic.com/engineering/writing-tools-for-agents)
- [Effective harnesses for long-running agents (Anthropic, Nov 2025)](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [Prompting best practices - Claude 4.6 (Anthropic API Docs)](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- [7 Must-Know Agentic AI Design Patterns (MachineLearningMastery, Oct 2025)](https://machinelearningmastery.com/7-must-know-agentic-ai-design-patterns/)
- [Reason-Plan-ReAct (arXiv:2512.03560, Dec 2025)](https://arxiv.org/abs/2512.03560)
- [Agent Context Protocols (arXiv:2505.14569, May 2025)](https://arxiv.org/abs/2505.14569)
- [Agentic Context Engineering (arXiv:2510.04618, Oct 2025)](https://www.alphaxiv.org/resources/2510.04618v1)
- [GPT-5.2 Prompting Guide (OpenAI Cookbook)](https://cookbook.openai.com/examples/gpt-5/gpt-5-2_prompting_guide)
