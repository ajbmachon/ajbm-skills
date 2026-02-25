---
name: SkillDistiller
description: USE WHEN distill, extract skill, capture patterns, teach from conversation, learn from session, skill from conversation. Analyzes conversations to extract user guidance patterns — corrections, questions, quality gates, analysis modes — and collaboratively distills them into permanent, replayable skills that teach Claude behavioral dispositions.
---

# SkillDistiller

Transform expert guidance buried in conversations into permanent, replayable skills.

**Core mental model:** The distilled skill teaches **behavioral dispositions** — how an expert thinks about a type of work — not rigid rules. The difference:

- NOT: "Always check for race conditions" (rule)
- YES: "When reviewing code that touches shared state, slow down and reason about concurrent access patterns" (disposition)

**Generalization spectrum** — the user controls where each pattern lands:

```
Raw:        "You forgot to check if the DB connection is open"
Specific:   "Verify resource availability before operations"
Behavioral: "Practice defensive programming at resource boundaries"
```

---

## Reference Docs (Read On-Demand)

| Doc | When to Read | What It Contains |
|-----|-------------|-----------------|
| [PatternTaxonomy.md](PatternTaxonomy.md) | Step 2 (Analyze) | Four extraction categories with signals and examples |
| [SkillTemplate.md](SkillTemplate.md) | Step 4 (Generate) | Template for generated skills using behavioral dispositions format |
| [ToolGuide.md](ToolGuide.md) | Step 1 (when using stored transcripts) | How and when to use each tool in the toolbox |

---

## Prerequisites

**qmd** — Required for cross-conversation semantic search (BM25 + vector hybrid).

```bash
# Check if installed
which qmd

# Install if missing (macOS)
brew install qmd

# Index transcripts for cross-conversation search
qmd index ~/.claude/
```

If qmd is not available, fall back to Grep-based keyword search with reduced capability.

---

## The Guided Flow

A single progressive experience. All five steps happen in one session.

### Step 1: SOURCE — "What conversation should I analyze?"

Determine the input source. Ask the user if not obvious from context.

| Input Mode | How It Works | Tools Needed |
|------------|-------------|-------------|
| **Current session** (default) | Read your own in-memory context. If compacted, recover from disk transcript (always saved). | None |
| **Session ID** | Locate transcript via `~/.claude/` session storage. | Toolbox (filter, extract) |
| **File path** | User provides path to transcript file. | Toolbox (filter, extract) |

**For current session:** Proceed directly to Step 2 — no preprocessing needed.

**For stored transcripts:** Use the toolbox to filter noise and extract clean turns. See [ToolGuide.md](ToolGuide.md) for which tools to use and when. Claude decides which tools are appropriate — they are an **on-demand toolbox, not a fixed pipeline**.

**Cross-conversation search:** If the user wants to find patterns across multiple sessions, use qmd:
```bash
qmd search "the pattern or behavior to find"
```

---

### Step 2: ANALYZE — Extract patterns across four categories

<mandatory_read phase="analyze">
Read [PatternTaxonomy.md](PatternTaxonomy.md) before starting analysis.
</mandatory_read>

Read the conversation with maximum intelligence. Look for moments where the user:

1. **Corrected or redirected** Claude's approach → **Corrections**
2. **Asked questions** that surface non-obvious considerations → **Questions & Probes**
3. **Told Claude to stop and check** something before proceeding → **Quality Gates**
4. **Directed Claude to think** from a specific angle or framework → **Analysis Modes**

**For stored transcripts:** After extracting clean turns with the toolbox, read through them looking for correction signals — keywords like "no", "actually", "instead", "wait", negation patterns, and redirect signals. Start with the strongest signals, then review subtler patterns.

**Output for each extracted pattern:**

| Field | Content |
|-------|---------|
| **Source moment** | What happened — context + user action (quote relevant text) |
| **Category** | Which of the four taxonomy types |
| **Proposed generalization** | Claude's suggested behavioral principle (not a rule) |
| **Confidence** | Strong signal / Inferred / Weak |

Present a summary of all extracted patterns before moving to Step 3.

---

### Step 3: REVIEW & CO-EDIT — Shape patterns collaboratively

**This is the core value step. Claude proposes, user decides. (H4)**

Present extracted patterns one at a time using `AskUserQuestion`. For each pattern:

1. **Show:** Source moment, category, proposed behavioral generalization
2. **Options:**
   - **Approve** — Keep as proposed
   - **Edit wording** — Refine the generalization together
   - **Adjust level** — Make more specific or more general
   - **Reject** — Remove this pattern

**Generalization controls the user can apply:**
- **Keep specific** → Preserve the concrete example as-is (good for anti-patterns)
- **Generalize** → Elevate to a behavioral principle
- **Merge** → Combine multiple raw extractions into one broader pattern

After reviewing all patterns individually, present the full approved set for final review:

> "Here are all approved patterns organized by category. Any final adjustments before I generate the skill?"

**Key principle:** Claude may suggest "this pattern appeared 4 times — I think it generalizes to X" but the user has final say on everything.

---

### Step 4: GENERATE — Write the skill

<mandatory_read phase="generate">
Read [SkillTemplate.md](SkillTemplate.md) before generating.
</mandatory_read>

Generate a complete SKILL.md from approved patterns using the behavioral dispositions template.

**Before writing, ask the user:**

```
Where should I save the generated skill?
1. This plugin repo: plugins/development-skills/skills/{SkillName}/
2. Personal skills: ~/.claude/skills/{SkillName}/
3. Custom path
```

**Structure of generated skill:** See [SkillTemplate.md](SkillTemplate.md) for the full template. The generated skill:
- Uses behavioral dispositions format (thinking patterns, attention cues, quality checkpoints)
- Includes anti-patterns section (from Corrections category, may stay specific)
- Includes annotated examples from source conversation(s)
- Has YAML frontmatter with `distilled_from` and `distilled_date`
- Follows codebase conventions: flat structure, under 500 lines

Write the skill file and present it to the user for final confirmation.

---

### Step 5: VERIFY — Behavioral checks (on-demand)

Run later via `/distill verify <skill-path>` after using the skill in real work.

Three verification methods:

**1. Behavioral Checklist**
For each disposition in the skill, check: did Claude exhibit this behavior during the session?
- Did Claude ask the probing questions?
- Did Claude pause at quality checkpoints?
- Did Claude apply the thinking patterns?
- Did Claude avoid the anti-patterns?

**2. Correction Regression**
Compare user corrections in sessions WITH the skill vs. baseline. Fewer corrections on target behaviors = skill is working.

**3. Pattern Hit Rate**
When triggering context appeared (e.g., shared mutable state), did the disposition actually fire?

For stored transcripts, use the toolbox (transcript-filter, turn-extractor) to prepare clean turns, then read the skill's dispositions and check each against the transcript evidence.

**Escalation path:** If verification shows patterns aren't being followed:
1. Refine the prompt wording in the skill
2. If still failing → escalate critical patterns to hooks (PreToolUse gates)

---

## Edge Cases

| Scenario | Handling |
|----------|---------|
| Short conversation, few patterns | Quality over quantity — user initiated distillation knowing there are patterns. Few is fine. |
| Conversation was compacted | Transcripts are always saved to disk. Recover from disk if in-memory context is incomplete. |
| Pure collaboration (no corrections) | Extract collaborative escalation patterns — moments where user elevated beyond Claude's default. |
| Session ID not found | Fall back to asking for file path. Guide to `~/.claude/` session storage. |
| qmd not installed | Run install script. If install fails, use Grep with reduced capability. |
| Generated skill too vague | Push for specificity during co-editing: "Can you give a concrete example of when this matters?" |
| Conflicting patterns across sessions | Present conflict: "In session A you said X, in session B you said Y. Which applies, or both context-dependent?" |

---

## Examples

**Current session distillation:**
"We just did a thorough code review together. `/distill` this session to capture my review approach."
→ Analyzes in-memory context. Extracts patterns: user's attention to error handling, questions about edge cases, stop-and-check before merging. Collaboratively shapes into a code-review skill.

**Stored transcript distillation:**
"Distill the patterns from my architecture session yesterday. Session ID: abc123."
→ Locates transcript, filters noise with toolbox, extracts patterns, collaboratively reviews and generates skill.

**Cross-conversation analysis:**
"I've done 5 QA sessions. Find the common testing patterns across all of them."
→ Uses qmd to search across transcripts for correction and quality gate patterns, synthesizes into a comprehensive QA skill.

**Verification:**
"/distill verify ~/.claude/skills/code-review/SKILL.md"
→ Reads the skill's dispositions and checks them against recent session transcripts, reports which dispositions are being followed and which need refinement.
