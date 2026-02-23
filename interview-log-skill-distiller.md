# Interview Working Log

**Topic:** SkillDistiller — Extract user guidance patterns from conversations into replayable skills
**Started:** 2026-02-23 15:10
**Status:** COMPLETE

---

## Constraint Registry

> Updated live as constraints emerge. This section is the source of truth.

### Hard Constraints (Immutable)

| # | Constraint | Source | Added |
|---|------------|--------|-------|
| H1 | Dual input — current session + stored transcripts (session ID/path) | User Q1 | 15:14 |
| H2 | Deterministic preprocessing before AI analysis | User Q2 | 15:14 |
| H3 | Output is valid replayable SKILL.md + docs | User Q2 | 15:14 |
| H4 | Human-in-the-loop — Claude presents, user decides what to codify | User Q5 correction | 15:17 |
| H5 | Full pipeline — analyze + generalize + verify, one integrated skill | User Q4 | 15:16 |

### Soft Constraints (Preferences)

| # | Constraint | Negotiable If | Added |
|---|------------|---------------|-------|
| S1 | Behavioral verification over A/B (checklist, correction regression, pattern hit rate) | A/B useful for specific cases | 15:18 |
| S2 | Deterministic preprocessing tools (qmd/vector for semantic search) | Simpler approach sufficient | 15:14 |
| S3 | Cross-conversation analysis support | Single conversation is enough | 15:16 |
| S4 | Integrate with existing Evals for comparative testing | Not needed | 15:18 |

### Boundaries (Out of Scope)

| # | What's Excluded | Reason | Added |
|---|-----------------|--------|-------|
| B1 | Autonomous e2e skill generation without user review | H4 | 15:17 |
| B2 | Real-time conversation interception | Post-hoc only | 15:18 |
| B3 | Traditional A/B as primary verification | Behavioral checks preferred | 15:18 |

---

## Decisions Log

> User decisions captured as they're made.

| # | Decision | Options Considered | Rationale | When |
|---|----------|-------------------|-----------|------|

---

## Assumptions & Corrections

> Assumptions surfaced and how they were resolved.

| # | Original Assumption | Correction | Source |
|---|---------------------|------------|--------|
| A1 | Fixed preprocessing pipeline (filter→pair→detect→AI) | On-demand toolbox — Claude picks which tools to use | Q8 user correction |
| A2 | qmd is a generic vectorization example | qmd is a specific tool — local CLI hybrid search (BM25+vector) for markdown | Research + user |
| A3 | Deterministic tools REPLACE AI analysis of transcripts | Tools AUGMENT Claude — context efficiency, not intelligence replacement. Claude still does all judgment. | Q10 user correction |
| A4 | One conversation might be enough | User wants cross-conversation pattern confirmation via qmd search | Implied by qmd emphasis |

---

## Interview Q&A

> Append each exchange as it happens.

### Q1: Where does conversation data come from?
**Asked:** 15:14 (Phase 2 — Devil's Advocate)
**Answer:** Current session (in-memory) AND transcripts when user provides session ID or way to find the right transcript. Both modes.
**Constraints extracted:** H1-candidate: Dual input mode (current session + stored transcripts)
**Decisions made:** D1: Support both in-memory and file-based input

### Q2: What's the value prop over manual authoring?
**Asked:** 15:14 (Phase 2 — Devil's Advocate)
**Answer:** (1) Claude identifies trends user can't see. (2) Deterministic tools to pre-filter — strip tool calls, filter user messages, vectorize for semantic search. (3) "Teach once, skill forever" — do PR review with Claude once, distill into skill, Claude does it alone next time. (4) User builds next upgrade instead of repeating.
**Constraints extracted:** H2-candidate: Deterministic preprocessing before AI analysis. H3-candidate: Output is a valid replayable skill.
**Decisions made:** D2: Core value = teach-once-distill-forever

### Q3: How to capture triggering context alongside corrections?
**Asked:** 15:16 (Phase 2)
**Answer:** Claude's intelligence handles inference and generalization. Some can't be captured, most can be inferred, cross-checked with other conversations. User defers to my (interviewer's) expertise on best mechanism — context pairs, annotated examples, or whatever works best to teach Claude judgment, questions, and error correction.
**Constraints extracted:** none new
**Decisions made:** D3: Use combination approach — my recommendation on mechanism

### Q4: Scope — three capabilities?
**Asked:** 15:16 (Phase 2)
**Answer:** Full pipeline — all three (analyze, generalize, A/B test) as one integrated skill.
**Constraints extracted:** none new
**Decisions made:** D4: Full pipeline scope

### Q5: USER CORRECTION — Generalization model
**Asked:** 15:17 (user-initiated correction during Phase 2)
**Answer:** "I don't want to generalize everything, just not stick to only the very specific example. Also I don't expect Claude to generalize e2e but to present findings to me as the user via the analysis skill and then I give input on what to use."
**Constraints extracted:** H-candidate: Human-in-the-loop. NOT autonomous generalization. H-candidate: Present analysis to user, user decides what to keep/generalize/discard.
**Decisions made:** D5: Interactive workflow — Claude analyzes and presents, user selects and guides generalization. NOT autonomous e2e.

### Q6: Workflow structure
**Asked:** 15:20 (Phase 3 — Partner)
**Answer:** Single guided flow. Not separate workflows. One progressive experience like Interview skill.
**Constraints extracted:** none new
**Decisions made:** D6: Single guided flow with 5 interactive steps

### Q7: Pattern taxonomy
**Asked:** 15:20 (Phase 3)
**Answer:** All four categories selected: Corrections, Questions & Probes, Quality Gates, Analysis Modes
**Constraints extracted:** none new
**Decisions made:** D7: Four-category extraction taxonomy

---

## Research Findings

> Logged when research completes (blocking or background).

### R1: Conversation Storage & Access
**Source:** Explore agent
**Finding:** Claude Code stores conversations at multiple levels:
- `~/.claude/history.jsonl` — global user prompts with sessionId, timestamp, project
- `.claude/sessions/{name}/history.jsonl` — per-session tool execution logs
- `MEMORY/LEARNING/FAILURES/` — full transcript.jsonl + tool-calls.json for captured sessions
- `MEMORY/WORK/` — task threads with algorithm phases
**Impact:** Rich data exists but conversations are NOT stored as clean user↔assistant turns. Tool calls, hook outputs, and system messages are interleaved. Extraction will need significant filtering.

### R2: Programmatic Invocation (claude -p)
**Source:** Explore agent
**Finding:** `claude -p` supports:
- `--output-format stream-json` for full conversation JSONL
- `--resume <session_id>` for continuing sessions
- `--append-system-prompt` for injecting custom behavior (KEY for A/B testing)
- `--input-format stream-json` for feeding conversation state
- `--no-session-persistence` for ephemeral runs
**Impact:** A/B testing is technically feasible — can run same prompt with/without distilled skill as system prompt.

### R3: Existing A/B Testing Infrastructure
**Source:** Explore agent
**Finding:** Evals skill already has ComparePrompts workflow with:
- Position swap protocol (bias mitigation)
- LLM-as-judge (pairwise comparison)
- Statistical significance testing
- YAML-based task schema
**Impact:** Don't need to build A/B testing from scratch — can integrate with existing Evals infrastructure.

### R4: Skill Structure Patterns
**Source:** Explore agent
**Finding:** Skills use flat structure (max 2 levels), SKILL.md with YAML frontmatter, USE WHEN triggers, Workflows/ for execution paths. Large skills use progressive loading.
**Impact:** Output format for generated skills is well-defined — need to generate valid SKILL.md + supporting docs.

---

## Research Artifacts

> Index of all research files created during this interview.

| # | File Path | Created By | Topic | Phase |
|---|-----------|------------|-------|-------|

---

## Phase Transitions

> Mark when moving between phases.

| Phase | Entered | Notes |
|-------|---------|-------|
| Research Foundation | 15:10 | |
| Devil's Advocate | 15:14 | Research complete, challenging viability |
| Constraint Capture | 15:18 | H1-H5, S1-S4, B1-B3 confirmed |
| Deep Interview | | |
| Verification | | |
| Output | | |

---

## Notes

> Free-form observations during interview.

- 15:10: User wants to capture HOW they guide AI through work — corrections, judgment, questions, analysis modes — and package into replayable skills with A/B testing
