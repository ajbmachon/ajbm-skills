# SkillDistiller — Specification

**Generated:** 2026-02-23
**Source:** Interview with Andre Machon
**Working Log:** `./interview-log-skill-distiller.md`

---

## Problem Statement

When a user guides Claude through complex work — code reviews, document writing, QA testing, architecture analysis — they contribute expert judgment that Claude lacks: the right questions to ask, when to stop and check, which assumptions to challenge, what "good" looks like in context. This expert guidance is ephemeral. It dies with the session. The user must re-teach Claude every time.

**Who experiences this:** Expert users who repeatedly guide Claude through similar types of work, supplying the judgment, questions, and error correction that make the output excellent.

**When it manifests:** Every new session starts from zero. Claude doesn't remember that the user always checks for race conditions before approving concurrent code, or that the user asks "what would a junior developer misunderstand here?" during doc reviews.

**Cost of not solving:** The user becomes a permanent bottleneck. They can't delegate because their expertise only exists in their head and in ephemeral conversation history.

---

## Objective

A Claude Code skill that analyzes conversations to extract user guidance patterns — corrections, questions, quality gates, analysis modes — and, through collaborative editing with the user, distills them into permanent, replayable skills that teach Claude behavioral dispositions for that type of work.

**In one sentence:** Teach Claude once by doing the work together, then distill that teaching into a permanent skill so Claude can do it alone next time.

---

## Success Criteria

- [ ] Skill can analyze the current session's conversation (in-memory context)
- [ ] Skill can locate and analyze stored transcripts by session ID or file path
- [ ] Deterministic tools filter transcripts without loading everything into context
- [ ] Patterns are extracted across four taxonomy categories
- [ ] User reviews and co-edits each pattern interactively before codification
- [ ] Generated output is a valid, self-contained SKILL.md with supporting docs
- [ ] Behavioral verification can be run on-demand against any generated skill
- [ ] The entire flow is a single guided experience (not separate workflows)

---

## Constraint Registry

**Captured:** 2026-02-23 during Devil's Advocate phase
**Confirmed by:** Andre Machon at Partner transition

### Hard Constraints (Immutable)

| # | Constraint | Source | Notes |
|---|------------|--------|-------|
| H1 | Dual input — current session (in-memory) + stored transcripts (session ID/path) | User Q1 | Current session is the primary use case |
| H2 | Deterministic tools for transcript preprocessing — not a pipeline, an on-demand toolbox | User Q2, corrected Q8 | Tools augment Claude's intelligence (context efficiency), don't replace it |
| H3 | Output is valid, replayable SKILL.md + supporting docs | User Q2 | Single skill per domain for MVP; composable pattern library deferred to v2 |
| H4 | Human-in-the-loop — Claude analyzes and presents, user decides what to codify | User Q5 correction | Full collaborative editing, NOT autonomous e2e generalization |
| H5 | Full pipeline — analyze + generalize + verify, one integrated skill | User Q4 | Single guided flow, not separate workflows |

### Soft Constraints (Preferences)

| # | Constraint | Negotiable If | Notes |
|---|------------|---------------|-------|
| S1 | Behavioral verification over A/B testing — checklist, correction regression, pattern hit rate | A/B useful for specific comparisons | Emerged from user challenging traditional A/B |
| S2 | qmd required for semantic search across transcripts, with install script if missing | Simpler search acceptable as fallback during install | qmd = local hybrid search (BM25 + vector) |
| S3 | Cross-conversation analysis support via qmd | Single conversation is enough for MVP | Pattern confirmation across sessions |
| S4 | Integrate with existing Evals if comparative testing needed | Not needed for behavioral verification | Existing infrastructure available |

### Boundaries (Out of Scope)

| # | What's Excluded | Reason |
|---|-----------------|--------|
| B1 | Autonomous e2e skill generation without user review | H4 — human judgment is the point |
| B2 | Real-time conversation interception | Post-hoc analysis only |
| B3 | Traditional A/B as primary verification | Behavioral checks are more natural and reliable |

---

## Architecture & Design

### Core Mental Model

**The distilled skill teaches behavioral dispositions, not rules.**

A behavioral disposition is how an expert thinks about a type of work — what they notice, what questions they ask, what tradeoffs they weigh, when they stop and check. It's the difference between "always check for race conditions" (a rule) and "when reviewing code that touches shared state, slow down and reason about concurrent access patterns" (a disposition).

The generalization spectrum per extracted pattern:
```
Raw:        "You forgot to check if the DB connection is open"
Specific:   "Verify resource availability before operations"
Behavioral: "Practice defensive programming at resource boundaries"
```

During collaborative editing, the user controls where each pattern lands. Some stay specific (concrete anti-patterns). Most move to behavioral principles. The right level varies per pattern — the skill does NOT try to generalize everything.

### Skill Directory Structure

```
SkillDistiller/
├── SKILL.md                     # Guided flow + routing
├── PatternTaxonomy.md           # Four extraction categories defined
├── SkillTemplate.md             # Template for generated skills
├── ToolGuide.md                 # How Claude uses the toolbox
└── Tools/
    ├── transcript-filter.ts     # Strip tool calls, hooks, system prompts from JSONL
    ├── turn-extractor.ts        # Extract user/assistant turn pairs
    ├── correction-detector.ts   # Heuristic flagging of correction signals
    └── behavior-checker.ts      # Post-session behavioral verification
```

**External dependency:** qmd (required, install script provided if missing)

### Pattern Taxonomy (Four Categories)

| Category | What It Captures | Extraction Signal | Skill Output Section |
|----------|-----------------|-------------------|---------------------|
| **Corrections** | Where user redirected Claude's approach | "no", "actually", "instead", "not like that", explicit disagreement | Anti-patterns: "DON'T default to X when Y" |
| **Questions & Probes** | Questions user asked that Claude should have asked itself | User questions that surface non-obvious considerations | Probing Protocol: thinking cues and questions to ask |
| **Quality Gates** | Stop-and-check moments before proceeding | "wait", "before you", "first check", "verify", blocking instructions | Checkpoints: conditions to verify before actions |
| **Analysis Modes** | Specific thinking strategies user directed | "look at this from", "compare against", "what about", "consider the perspective of" | Thinking Strategies: lenses and frameworks to apply |

### The Toolbox (NOT a Pipeline)

Claude has tools available for on-demand use. Claude decides which tools to use based on the situation. For the **current session** (primary use case), no tools are needed — Claude reads its own in-memory context.

For **stored transcripts**, Claude uses whichever tools are appropriate:

| Tool | Purpose | When Used |
|------|---------|-----------|
| `transcript-filter` | Strip tool_use, tool_result, system prompts, hook output, progress events from raw JSONL | Stored transcripts with noisy data |
| `turn-extractor` | Extract clean user/assistant turn pairs from filtered JSONL | After filtering, to structure the data |
| `correction-detector` | Heuristic flagging of turns with correction signals (keywords, question marks, contradictions) | To prioritize which turns to analyze first |
| `qmd` | Semantic search across ALL conversation transcripts | Cross-conversation pattern confirmation, finding similar corrections in other sessions |
| `behavior-checker` | Audit a session transcript against a distilled skill's behavioral dispositions | During verification (Step 5) |

Claude is the intelligent analyst. These tools handle data plumbing so Claude doesn't waste context window on noise.

---

## The Guided Flow

### Step 1: SOURCE

"What conversation should I analyze?"

| Input Mode | How It Works |
|------------|-------------|
| **Current session** (default) | Claude reads its own in-memory context. If compacted, recovers from disk transcript (always saved). Simplest path. |
| **Session ID** | User provides session ID. Claude locates transcript via `~/.claude/` session storage. Uses toolbox to filter and load. |
| **File path** | User provides path to a transcript file. Claude reads and processes. |

For stored transcripts, Claude uses the toolbox to filter noise and extract clean turns before analysis.

### Step 2: ANALYZE

Claude reads the conversation with maximum intelligence and identifies patterns across the four taxonomy categories.

**For current session:** Claude reviews the conversation it just participated in, looking for moments where the user:
- Corrected or redirected Claude's approach
- Asked questions that surface non-obvious considerations
- Told Claude to stop and check something before proceeding
- Directed Claude to think from a specific angle or apply a specific framework

**For stored transcripts:** Claude uses tools to filter, then applies the same analytical intelligence.

**Output:** A structured set of extracted patterns, each with:
- **Source moment:** What happened in the conversation (context + user action)
- **Category:** Which of the four taxonomy types
- **Proposed generalization:** Claude's suggested behavioral principle (not a rule)
- **Confidence:** How clear the pattern is (strong signal vs. inferred)

### Step 3: REVIEW & CO-EDIT

Claude presents extracted patterns one at a time via `AskUserQuestion`. For each pattern:

1. **Shows:** Source moment, category, proposed behavioral generalization
2. **User action:** Approve / Edit wording / Adjust generalization level / Reject
3. **Together:** Shape the final wording — this is collaborative editing, not just approval

The generalization level is a dial the user controls:
- Keep specific → preserve the concrete example as-is
- Generalize → elevate to a behavioral principle
- Merge → combine multiple raw extractions into one broader pattern

**Key principle (H4):** Claude proposes, user decides. Claude may suggest "this pattern appeared 4 times — I think it generalizes to X" but the user has final say.

### Step 4: GENERATE SKILL

Claude writes a SKILL.md from the approved patterns:

**Structure of the generated skill:**

```markdown
---
name: {SkillName}
description: {Domain-specific description with USE WHEN triggers}
distilled_from: {session ID(s) or "current session"}
distilled_date: {date}
---

# {Skill Name}

{Brief description of the behavioral disposition this skill teaches.}

## Behavioral Dispositions

{The core of the skill — how to think about this type of work.
NOT a checklist. A description of expert attention patterns.}

### Thinking Patterns
{Analysis modes and cognitive frameworks extracted from the user's guidance.}

### Attention Cues
{What to notice — the probing questions an expert would ask.}

### Quality Checkpoints
{When to pause and verify — gates extracted from the user's stop-and-check moments.}

## Anti-Patterns

{What NOT to do — concrete examples from corrections.
These may stay specific when the raw example is more useful than a generalization.}

## Examples

{Specific examples from the source conversation(s) where useful.
Annotated with: what happened, what the expert did, why it mattered.}
```

User chooses the output path (this plugin repo, `~/.claude/skills/`, or a custom location).

### Step 5: VERIFY (On-Demand)

Run later via `/distill verify <skill-path>` after using the skill in real work.

**Behavioral Checklist:** For each disposition in the skill, check: did Claude exhibit this behavior during the session?
- Did Claude ask the probing questions?
- Did Claude pause at the quality checkpoints?
- Did Claude apply the thinking patterns?
- Did Claude avoid the anti-patterns?

**Correction Regression:** Compare the number of user corrections in sessions WITH the skill vs. the baseline. Fewer corrections on target behaviors = skill is working.

**Pattern Hit Rate:** When the triggering context appeared (e.g., shared mutable state), did the disposition actually fire?

**Escalation path:** If verification shows patterns aren't being followed after iteration:
1. Refine the prompt wording
2. If still failing → escalate critical patterns to hooks (PreToolUse gates)

---

## Edge Cases & Failure Modes

| Scenario | How to Handle |
|----------|---------------|
| Short conversation with few patterns | User initiates distillation when they know there are valuable things to teach. Few patterns is fine — quality over quantity. |
| Conversation was compacted | Not an issue — chat transcripts are saved to disk regardless of compaction. Recover from disk transcript if in-memory context is incomplete. |
| Conversation was pure collaboration (no corrections) | User chose to distill for a reason — extract collaborative escalation patterns: moments where user elevated beyond Claude's default. |
| Session ID doesn't map to a stored transcript | Fall back to asking for file path. Guide user to check `~/.claude/` session storage. |
| qmd not installed | Run install script. If install fails, fall back to keyword-based search (Grep) with reduced capability. |
| Generated skill is too vague/generic | During collaborative editing, push for specificity: "Can you give me a concrete example of when this pattern matters?" |
| Conflicting patterns across conversations | Present the conflict to user during co-editing: "In session A you said X, in session B you said Y. Which applies, or are these context-dependent?" |

---

## Tradeoffs & Decisions

| Decision | Alternatives Considered | Why This Choice |
|----------|------------------------|-----------------|
| Single guided flow | Three separate workflows (Analyze, Distill, Verify) | Matches Interview skill pattern. User preferred progressive experience over phased approach. |
| On-demand toolbox, not fixed pipeline | Fixed preprocessing pipeline | User corrected: tools augment Claude, not replace. Claude decides what to use. |
| Behavioral dispositions, not rules | Rule-based extraction, checklist generation | Rules are brittle. Dispositions teach HOW to think, which is what the user actually demonstrates. |
| Behavioral verification, not A/B testing | Forked conversation A/B via Evals | A/B measures subjective quality. Behavioral checks measure if dispositions are followed — more natural and deterministic. |
| Single skill per domain (MVP) | Composable pattern library | Pragmatic: prove the distillation process works first. Pattern library is v2 when the unit of value (patterns) is better understood. |
| qmd required | Optional with fallback, or no external deps | Cross-conversation semantic search is core to the value prop. Install script mitigates friction. |
| Full collaborative editing | Approve/reject only, or approve/reject/edit | User wants to shape dispositions together. The editing IS the value — that's where human judgment enters. |
| Start prompt-based, escalate to hooks | Prompt-only, or hooks from the start | Most behavioral dispositions work as prompt instructions. Hooks are a fallback for patterns that prompt engineering can't enforce. |

---

## Assumption Corrections

| Original Assumption | Who Held It | Source of Correction | Corrected Understanding |
|---------------------|-------------|----------------------|-------------------------|
| Fixed preprocessing pipeline (filter→pair→detect→AI) | Claude | User Q8 correction | On-demand toolbox. Claude picks tools as needed. |
| Deterministic tools replace AI analysis | Claude | User Q10 correction | Tools augment Claude for context efficiency. Claude still applies maximum intelligence. |
| A/B testing via forked conversations is the right verification | Both initially | User challenge during Phase 2 | Behavioral verification (checklist, correction regression, pattern hit rate) is more natural. |
| The skill generates hard rules ("always check X") | Claude | User Q on conflict handling | Behavioral dispositions at the right generalization level. User controls the specificity dial. |
| qmd was a generic example | Claude | Research + user clarification | qmd is a specific tool — local hybrid search (BM25 + vector) for markdown knowledge bases. |
| Compaction loses conversation data | Claude | User correction | Transcripts are always saved to disk. Compaction only affects in-memory context. Recovery from disk is always possible. |
| "No corrections found" is a likely edge case | Claude | User correction | User initiates distillation when they KNOW there are valuable patterns. It's intentional, not speculative. |

---

## Interview Record

### Theme 1: Data Source & Access

**Q: Where does the conversation data come from?**
A: Current session (primary, in-memory) + stored transcripts when user provides session ID or path. Toolbox for preprocessing stored transcripts.

**Q: How do you handle the signal-to-noise problem in raw transcripts?**
A: Deterministic tools filter noise (tool calls, system prompts) WITHOUT replacing Claude's intelligence. Tools are for context efficiency — Claude still does all judgment.

### Theme 2: Value Proposition

**Q: What does automated extraction give you that direct authoring doesn't?**
A: (1) Claude identifies trends the user can't see — blind spots. (2) Tools enable searching across all transcripts for wider patterns. (3) "Teach once, skill forever" — do a task with Claude once, distill, Claude does it alone next time. User builds the next upgrade instead of repeating themselves.

### Theme 3: Generalization Model

**Q: How to handle context-dependent guidance that contradicts across conversations?**
A: NOT hard rules. Behavioral dispositions at the right generalization level. The collaborative editing step is where user and Claude decide per-pattern how much to generalize. Some patterns stay specific (concrete anti-patterns), most become behavioral principles.

[User correction: "I don't want such hard rules in the distilled skills. 'Always check' is the wrong mental model. We move from one-off instructions to general behaviour patterns teaching Claude what good work looks like."]

### Theme 4: Architecture & Composability

**Q: Single skill per domain or composable pattern library?**
A: MVP = single skill per domain. Pattern library is v2. Reasoning: prove the distillation process works first. The library architecture (patterns as source, skills as compiled output) is the right long-term model but adds complexity before the core value is proven.

### Theme 5: Verification Strategy

**Q: How to verify the skill actually changes Claude's behavior?**
A: Behavioral verification over A/B testing. Checklist (did Claude follow dispositions?), correction regression (fewer user corrections?), pattern hit rate (did behaviors fire?). Start prompt-based, escalate to hooks if verification fails.

---

## Open Questions

- [ ] **qmd integration depth:** How deeply should the skill integrate with qmd? Index all session transcripts automatically, or only on-demand when user requests cross-conversation analysis?
  - **Fallback:** On-demand indexing. User runs qmd index when they want cross-conversation search.

- [ ] **Skill template refinement:** The generated SKILL.md template should be validated against real distillation runs. First few runs will likely reveal improvements needed.
  - **Fallback:** Template is a starting point; iterate based on actual usage.

- [ ] **v2 Pattern Library Migration:** When and how to migrate from single-skill to composable pattern library. Design the migration path during v1 usage to understand what patterns actually look like in practice.
  - **Fallback:** Keep v1 forever if single skills are sufficient.

---

## Future: v2 — Composable Pattern Library

Deferred to v2 but documented for context:

```
~/.claude/distilled-patterns/
├── patterns/
│   ├── architecture-tradeoffs.md    # From code review #1
│   ├── edge-case-awareness.md       # From code review #3
│   ├── probing-questions.md         # From reviews #1, #5
│   └── defensive-coding.md          # From reviews #2, #4
├── skills/
│   ├── code-review.md               # Composes: [arch, edge, probing]
│   └── doc-writing.md               # Composes: [probing, structure]
└── index.json                        # Tags, sources, composition map
```

Pattern library as authoring format, self-contained skill as deployment format. Each pattern lives once, composed into many skills. qmd indexes the entire library for semantic discovery. When a pattern is refined, all skills using it improve.

---

*This spec was generated through the Interview skill. Working log: `./interview-log-skill-distiller.md`*
