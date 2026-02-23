# Interview Working Log

**Topic:** Prompt-craft skill improvements based on agentic prompting research (2025-2026)
**Started:** 2026-02-21 22:55 CET
**Status:** COMPLETE
**Type:** Ideation

---

## Constraint Registry

> Updated live as constraints emerge. This section is the source of truth.

### Hard Constraints (Immutable)

| # | Constraint | Source | Added |
|---|------------|--------|-------|
| H1 | Keep 19-technique taxonomy as backbone | User stated | Q1 |
| H2 | No pattern library mode (Fabric handles that) | User stated | Q1 |
| H3 | No meta-prompting duplication (Prompting handles that) | User stated | Q1 |
| H4 | SKILL.md stays under ~500 lines | User confirmed | Q1 |

### Soft Constraints (Preferences)

| # | Constraint | Negotiable If | Added |
|---|------------|---------------|-------|
| S1 | Model-conditional XML/markdown guidance | Strong model-specific evidence | Q2 |
| S2 | New techniques in reference/ files, not SKILL.md | Technique is trivially small | Q1 |
| S3 | Cross-reference sibling skills, don't duplicate | No sibling skill covers it | Q1 |

### Boundaries (Out of Scope)

| # | What's Excluded | Reason | Added |
|---|-----------------|--------|-------|
| B1 | Handlebars template system | Prompting skill covers this | Q1 |
| B2 | 240+ pattern catalog | Fabric skill covers this | Q1 |
| B3 | Full context engineering course | Brief note only, not a course | Q1 |

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

---

## Interview Q&A

> Append each exchange as it happens.

### Q1: Scope vision for prompt-craft
**Asked:** 22:56
**Answer:** Focused expansion — keep the 19-technique taxonomy as core. Add 3-5 new agentic techniques. Update model guidance. Fix XML/markdown. Don't add pattern libraries or meta-prompting.
**Constraints extracted:** H1 (keep technique taxonomy), H2 (no pattern library), H3 (no meta-prompting duplication)
**Decisions made:** D1 (focused expansion scope)

### Q2: XML vs Markdown resolution
**Asked:** 22:56
**Answer:** Model-conditional — keep XML for models that benefit (GPT-4o, Gemini). Add Claude 4.x note recommending markdown. Different models, different best practices.
**Constraints extracted:** S1 (model-conditional approach)
**Decisions made:** D2 (model-conditional XML/markdown)

### Q3: Audience — human vs agentic
**Asked:** 22:56
**Answer:** Both equally — expand the Agentic Self-Use section significantly. Add tool description optimization, subagent briefing patterns, ReAct loop construction.
**Constraints extracted:** None
**Decisions made:** D3 (equal human + agentic audience)

### Q4: New techniques to add
**Asked:** 22:58
**Answer:** ALL FOUR — ReAct Loop Pattern, Tool Description Craft, Context Engineering, Multi-Session State
**Constraints extracted:** None
**Decisions made:** D4 (add 4 new extended techniques)

### Q5: Existing content to update
**Asked:** 22:58
**Answer:** ALL FOUR — Salience (XML/markdown), Models.md refresh, Agentic Self-Use overhaul, Craft mode (Mode B). PLUS: overhaul mode router (remove rigid menu requirement, let Claude judge), split model files for JIT loading.
**Constraints extracted:** S4 (split model files for context efficiency)
**Decisions made:** D5 (update all 4 + mode router + model file split)

### Q6: Agentic section location
**Asked:** 23:01
**Answer:** Inline expansion (~80 lines in SKILL.md). Keep it immediately visible, don't bury in reference file.
**Constraints extracted:** None
**Decisions made:** D6 (agentic section inline, ~80 lines)

### Q7: Model file structure
**Asked:** 23:01
**Answer:** Per-model files. reference/models/claude.md, reference/models/openai.md, etc. Claude loads only relevant file via *model command.
**Constraints extracted:** S4 refined (per-model files, not TOC)
**Decisions made:** D7 (split models.md into per-model files)

### Q8: Implementation priority
**Asked:** 23:05
**Answer:** All at once — one cohesive update.
**Decisions made:** D8 (single implementation, not phased)

### Q9: Stale techniques (user-initiated)
**Asked:** 23:06
**Answer:** User notes some techniques may be stale or less effective (e.g., Roles). Should consider removing or modifying. Research supports: Claude 4.6 is personality-aware by default, explicit role prompting has diminishing returns.
**Constraints extracted:** None (modifies H1 slightly — taxonomy backbone stays but individual techniques can be updated/removed)
**Decisions made:** D9 (update Roles reference to reflect diminishing returns, keep all 10 core)

### Q10: Technique staleness resolution
**Asked:** 23:08
**Answer:** Update Roles only — rewrite reference to reflect 2025-2026 reality. Keep Verbalized Sampling (user loves it). All 10 stay core.
**Constraints extracted:** H5 (Verbalized Sampling stays core — user values it highly)
**Decisions made:** D10 (Roles reference updated, VS stays)

### Q11: Model table deduplication
**Asked:** 23:08
**Answer:** Remove inline model table from Agentic section, replace with pointer to per-model files. Saves ~15 lines.
**Decisions made:** D11 (dedup model table, add pointer)

---

## Research Findings

### R1: Agentic Prompting Research (2025-2026)
**Source:** Research agent (multi-model web search)
**Finding:** 9 novel techniques identified: adaptive thinking, context engineering as primary frame, agent-optimized tool writing, prefill deprecation, Reason-Plan-ReAct, Agent Context Protocols, anti-overtriggering, two-agent multi-session harnesses, effort parameter as primary lever. 15+ sources cited.
**Impact:** Identifies significant gaps in prompt-craft's technique coverage, especially for agentic workloads.

### R2: Fabric Comparison
**Source:** Comparison subagent
**Finding:** 5 critical gaps — no pattern library, no pipeline orchestration, no structural scaffold (IDENTITY/PURPOSE/STEPS/OUTPUT), missing ReAct pattern, no tool description optimization. Fabric offers composition architecture prompt-craft lacks.
**Impact:** Suggests adding pattern library mode, pipeline templates, and structural scaffold for system prompts.

### R3: Prompting Skill Comparison
**Source:** Comparison subagent
**Finding:** 8 priority gaps — XML vs markdown conflict (Salience technique recommends XML, Prompting bans it), missing context engineering philosophy, no multi-session state management, no ReAct loop, missing action bias elicitation, no effort-first framing, shallow subagent composition, no cross-reference. prompt-craft uniquely strong on: named technique taxonomy, quantified impacts, multi-model coverage, interactive modes.
**Impact:** Identifies specific file-level changes needed and a direct conflict requiring resolution.

---

## Research Artifacts

| # | File Path | Created By | Topic | Phase |
|---|-----------|------------|-------|-------|
| 1 | (in-memory) | Research agent | Agentic prompting 2025-2026 | Phase 1 |
| 2 | (in-memory) | Comparison subagent | Fabric vs prompt-craft gaps | Phase 1 |
| 3 | (in-memory) | Comparison subagent | Prompting vs prompt-craft comparison | Phase 1 |

---

## Phase Transitions

| Phase | Entered | Notes |
|-------|---------|-------|
| Research Foundation | 22:53 | Research + 2 comparison agents completed |
| Diverge (BeCreative) | | |
| Devil's Advocate | | |
| Constraint Capture | | |
| Deep Interview | | |
| Verification | 23:09 | All constraints verified, no conflicts |
| Output | 23:10 | Spec written to prompt-craft-improvement-spec.md |

---

## Notes

- 22:53: All three research streams completed with comprehensive findings
- 22:55: Working log initialized
