# SkillDistiller — Implementation Plan

## Prerequisites: READ THESE FIRST

**You MUST read both files below before starting any implementation work.**

### 1. Full Specification (REQUIRED)
```
plugins/development-skills/skills/interview-log-skill-distiller-spec.md
```
This is the complete, Interview-derived specification for the SkillDistiller skill. It contains:
- Problem statement and objective
- Constraint registry (H1-H5, S1-S4, B1-B3) — every design decision must honor these
- Architecture and core mental model (behavioral dispositions, NOT rules)
- Pattern taxonomy (4 categories: Corrections, Questions & Probes, Quality Gates, Analysis Modes)
- The 5-step guided flow (Source → Analyze → Review & Co-Edit → Generate → Verify)
- Toolbox design (on-demand tools, NOT a fixed pipeline)
- Edge cases, tradeoffs, assumption corrections
- Future v2 composable pattern library vision

### 2. Interview Working Log (REQUIRED)
```
interview-log-skill-distiller.md
```
This captures the full design rationale: every question asked, every answer given, every assumption corrected, every constraint that emerged. It documents WHY decisions were made, not just what was decided. Critical corrections:
- A1: Tools are an on-demand toolbox, NOT a pipeline
- A2: qmd is a specific local hybrid search tool (BM25 + vector)
- A3: Deterministic tools AUGMENT Claude's intelligence (context efficiency), not replace it
- A4: User initiates distillation when they KNOW there are patterns to capture
- Compaction is not an issue — transcripts are always saved to disk

---

## Core Mental Model (DO NOT DEVIATE)

The distilled skill teaches **behavioral dispositions**, not rules.

- NOT: "Always check for race conditions" (rule)
- YES: "When reviewing code that touches shared state, slow down and reason about concurrent access patterns" (disposition)

The generalization spectrum per extracted pattern:
```
Raw:        "You forgot to check if the DB connection is open"
Specific:   "Verify resource availability before operations"
Behavioral: "Practice defensive programming at resource boundaries"
```

During collaborative editing, the USER controls where each pattern lands on this spectrum. Some stay specific, most generalize to behavioral principles.

---

## Implementation Tasks

### Phase 1: Skill Structure & SKILL.md

Create the skill directory and main routing file:

```
plugins/development-skills/skills/SkillDistiller/
├── SKILL.md                     # Guided flow + routing (single workflow)
├── PatternTaxonomy.md           # Four extraction categories defined
├── SkillTemplate.md             # Template for generated skills
├── ToolGuide.md                 # How Claude uses the toolbox
└── Tools/
    ├── transcript-filter.ts     # Strip tool calls, hooks, system prompts from JSONL
    ├── turn-extractor.ts        # Extract user/assistant turn pairs
    ├── correction-detector.ts   # Heuristic flagging of correction signals
    └── behavior-checker.ts      # Post-session behavioral verification
```

**SKILL.md must include:**
- YAML frontmatter with name, description, USE WHEN triggers
- The 5-step guided flow as the single workflow
- Reference links to supporting docs (PatternTaxonomy, ToolGuide, SkillTemplate)
- Constraint: under 500 lines, use progressive disclosure

**Triggers:** `USE WHEN distill, extract skill, capture patterns, teach from conversation, learn from session, distill skill, skill from conversation`

### Phase 2: Supporting Documents

**PatternTaxonomy.md** — Define the four extraction categories:
| Category | Extraction Signals | Skill Output Section |
|----------|-------------------|---------------------|
| Corrections | "no", "actually", "instead", disagreement | Anti-patterns |
| Questions & Probes | User questions surfacing non-obvious considerations | Probing Protocol |
| Quality Gates | "wait", "before you", "first check", blocking | Checkpoints |
| Analysis Modes | "look at from", "compare against", "consider" | Thinking Strategies |

**SkillTemplate.md** — Template for generated skills (behavioral dispositions format):
- Behavioral Dispositions section (NOT checklists)
- Thinking Patterns, Attention Cues, Quality Checkpoints subsections
- Anti-Patterns section (specific examples when useful)
- Examples section (annotated conversation excerpts)
- Frontmatter with distilled_from and distilled_date

**ToolGuide.md** — When and how Claude uses each tool:
- Current session = no tools needed (in-memory context, or recover from disk if compacted)
- Stored transcripts = toolbox on demand (Claude decides which tools)
- qmd = cross-conversation semantic search (required dependency, install script if missing)
- Tools augment intelligence, not replace it

### Phase 3: Deterministic Tools

**transcript-filter.ts** — TypeScript tool that:
- Reads JSONL transcript files
- Strips: tool_use, tool_result, system messages, hook output, progress events
- Keeps: user messages, assistant text content
- Outputs: clean JSONL with just conversational turns
- Usage: `bun run transcript-filter.ts <input.jsonl> [--output <out.jsonl>]`

**turn-extractor.ts** — TypeScript tool that:
- Takes filtered JSONL (or raw — can call filter internally)
- Pairs each user message with the preceding assistant response
- Outputs: JSON array of {assistant_context, user_action, turn_number} objects
- Usage: `bun run turn-extractor.ts <input.jsonl> [--output <out.json>]`

**correction-detector.ts** — TypeScript tool that:
- Takes turn pairs
- Heuristic flags turns with correction signals:
  - Keywords: "no", "actually", "instead", "wait", "not like that", "but"
  - Question marks (user asking = probing)
  - Contradiction patterns (user says opposite of assistant)
- Outputs: turn pairs with correction_type tags
- Usage: `bun run correction-detector.ts <turns.json> [--output <tagged.json>]`

**behavior-checker.ts** — TypeScript tool that:
- Takes a skill path and a session transcript
- Extracts behavioral dispositions from the skill
- Checks transcript for evidence of each disposition being followed
- Outputs: behavioral compliance report (disposition, evidence, pass/fail)
- Usage: `bun run behavior-checker.ts <skill-path> <transcript.jsonl>`

### Phase 4: qmd Integration

- Check if qmd is installed (`which qmd`)
- If not: provide install instructions or run install script
- Index conversation transcripts: `qmd index ~/.claude/` (or targeted path)
- Search semantically: `qmd search "pattern description"` to find similar patterns across conversations
- Document in ToolGuide.md how Claude uses qmd during analysis

### Phase 5: CLAUDE.md & Plugin Registration

- Add SkillDistiller to CLAUDE.md skill descriptions
- Update plugin hooks if needed (hooks.json, skill-rules.json)
- Register trigger keywords

### Phase 6: Testing

- Test with current session analysis (the primary use case)
- Test with a stored transcript (session ID lookup)
- Test the full guided flow: Source → Analyze → Review → Generate → Verify
- Validate generated SKILL.md is valid and follows codebase conventions
- Run behavior-checker against a generated skill

---

## Key Constraints to Honor (from spec)

| # | Constraint | Implementation Implication |
|---|------------|--------------------------|
| H1 | Dual input (current session + transcripts) | Step 1 must handle both modes |
| H2 | Deterministic tools as on-demand toolbox | Tools are utilities Claude invokes, NOT a fixed pipeline |
| H3 | Output is valid SKILL.md | Generated skill must follow codebase conventions |
| H4 | Human-in-the-loop | Step 3 uses AskUserQuestion for collaborative editing, NEVER autonomous |
| H5 | Full pipeline in single guided flow | One workflow, 5 interactive steps |
| S1 | Behavioral verification, not A/B | behavior-checker.ts implements checklist + regression checks |
| S2 | qmd required | Install script for missing dependency |
| B1 | No autonomous generation | Claude proposes, user decides |

---

## Definition of Done

The skill is complete when:
1. `/distill` triggers the guided flow
2. Current session analysis works without tools
3. Stored transcript analysis works with toolbox
4. Collaborative pattern review presents patterns one at a time
5. Generated SKILL.md teaches behavioral dispositions (not rules)
6. `/distill verify <path>` runs behavioral checks
7. All files follow codebase conventions (flat structure, <500 line SKILL.md)
