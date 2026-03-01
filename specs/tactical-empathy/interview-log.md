# Interview Working Log

**Topic:** Negotiation & Communication Expert Skill Design
**Started:** 2026-03-01
**Status:** COMPLETE

---

## Constraint Registry

> Updated live as constraints emerge. This section is the source of truth.

### Hard Constraints (Immutable)

| # | Constraint | Source | Added |
|---|------------|--------|-------|
| H1 | Context-efficient — activate vectors, don't dump verbose instructions | User stated | Phase 0 |
| H2 | Based on Chris Voss "Never Split the Difference" as primary source | User stated | Phase 0 |
| H3 | Must make Claudius into a negotiation AND human communication expert | User stated | Phase 0 |
| H4 | Multi-mode: situation analysis, strategy building, AND real-time sparring | User defended | Phase 2 |
| H5 | Voss methods are the primary framework — they generalize to all negotiation scales | User defended | Phase 2 |

### Soft Constraints (Preferences)

| # | Constraint | Negotiable If | Added |
|---|------------|---------------|-------|
| S1 | Include complementary methods beyond just Voss | If scope gets too wide | Phase 0 |
| S2 | Triggers: negotiate, difficult conversation, persuade/influence | Could expand to email review | Phase 2 |

### Boundaries (Out of Scope)

| # | What's Excluded | Reason | Added |
|---|-----------------|--------|-------|

---

## Decisions Log

> User decisions captured as they're made.

| # | Decision | Options Considered | Rationale | When |
|---|----------|-------------------|-----------|------|
| D1 | Skill covers negotiation + difficult conversations + persuasion (not email review) | All 4 trigger categories | User selected 3 of 4. Email/comms review excluded | Phase 2 |
| D2 | Skill value = structured activation + behavioral dispositions, not knowledge recall | Knowledge dump vs activation | User acknowledged Claude already knows Voss | Phase 2 |
| D3 | Option B: Voss + Surgical Complements (~180 lines SKILL.md) | Pure Voss / Voss+Surgical / Full Phase-Based | Voss 70% core, 4 gap-fillers from other frameworks. Best balance of depth and efficiency | Phase 3 |
| D4 | Sparring mode is a CORE workflow, not optional | Core / Optional / No sparring | User wants practice-before-the-real-thing as primary value | Phase 3 |
| D5 | Two workflows: Analyze + Spar (dropped Live) | 3 workflows / 2 workflows | Simpler. Live coaching too situational for dedicated workflow | Phase 3 |
| D6 | Sparring uses inline bracket coaching after each exchange | Inline / Separate rounds / Post-session | Real-time learning without breaking immersion | Phase 3 |
| D7 | Skill name: tactical-empathy | never-split / tactical-empathy / negotiate | Names the philosophy, works for broad communication, sounds like a capability | Phase 3 |
| D8 | Lives in new plugin: ajbm-communication | Standalone / New plugin / Inside ajbm-dev | Creates home for future communication skills | Phase 3 |
| D9 | Analyze produces written dossier file | File / Inline only | Persistent, reviewable before actual negotiation | Phase 3 |

---

## Assumptions & Corrections

> Assumptions surfaced and how they were resolved.

| # | Original Assumption | Correction | Source |
|---|---------------------|------------|--------|

---

## Interview Q&A

> Append each exchange as it happens.

### Q1: Devil's Advocate Challenges + Scope Questions
**Asked:** Phase 2
**Answer:**
- Value: ALL modes — situation analyzer, sparring partner, AND communication coach. Voss generalizes to all negotiation including trivial ("where to eat tonight").
- Scope: UNDECIDED — wants to work it out collaboratively. Acknowledged Claude already has perfect recall of methods. Key question: what's the goldilocks value a skill adds?
- Triggers: Negotiation, difficult conversations, persuasion/influence. DID NOT select communication review/enhancement.
- Explicitly wants to go through research together to decide framework breadth.
**Follow-up needed:** Yes — the scope question IS the interview
**Constraints extracted:** See below
**Decisions made:** D1 (partial)

---

## Research Findings

> Logged when research completes (blocking or background).

### R1: Complementary Negotiation Frameworks
**Source:** voss-research agent (web + training knowledge)
**Finding:** 6 frameworks mapped against Voss with dedup. Key complements:
- Cialdini: Reciprocity, Commitment/Consistency, Scarcity, Unity, Pre-suasion (covers BEFORE and COMMITTING phases Voss is weak on)
- Fisher/Ury: BATNA, Interests vs Positions, Mutual Gain, Objective Criteria (covers preparation and integrative negotiation)
- Difficult Conversations: Three Conversations model (Identity layer Voss misses), Contribution vs Blame, Learning Stance
- NVC: OFNR sequence (self-expression — Voss is all listening), Needs Inventory (deeper than emotions)
- Crucial Conversations: Safety monitoring, Mutual Purpose, STATE method (speaking structure), Contrasting
- Phase coverage map: Voss has a REPAIR gap — no tools for when conversations break down
**Impact:** Shapes skill architecture — need phase-based routing, not just technique list

### R2: Vector Activation Research
**Source:** vector-activation-research agent (prompt-craft refs + codebase analysis + web research)
**Finding:** 5-layer activation stack ranked by token efficiency:
1. Terminology cluster (~80 tokens) — highest ROI, named techniques activate training distribution
2. Behavioral dispositions (~150 tokens) — SkillDistiller "When X, do Y" format
3. Anti-pattern contrasts (~60 tokens) — Wrong/Right pairs as compressed few-shots
4. Core axiom (~20 tokens) — single reorienting sentence
5. Permission escalation (~40 tokens) — unlock RLHF-softened behaviors
- Total SKILL.md activation: ~310 tokens (~80 lines)
- Skip detailed persona (diminishing on Claude 4.6)
- Progressive disclosure to reference files for depth
- Logit Gap Steering paper confirms: prompt tokens = Layer 0 activation steering
**Impact:** Defines the architectural pattern — hormozi-pitch structure + SkillDistiller dispositions + systematic-debugging anti-patterns

---

## Research Artifacts

> Index of all research files created during this interview.

| # | File Path | Created By | Topic | Phase |
|---|-----------|------------|-------|-------|
| 1 | (inline in log) | voss-research agent | Complementary frameworks | Phase 1 |
| 2 | (inline in log) | vector-activation-research agent | Vector activation patterns | Phase 1 |

---

## Phase Transitions

> Mark when moving between phases.

| Phase | Entered | Notes |
|-------|---------|-------|
| Research Foundation | 2026-03-01 | BLOCKING — vector activation, complementary frameworks, skill patterns |
| Devil's Advocate | 2026-03-01 | Challenging scope, activation approach, and design assumptions |
| Constraint Capture | 2026-03-01 | Constraints confirmed by user |
| Deep Interview (Diverge) | 2026-03-01 | BeCreative 5 options generated |
| Deep Interview (Converge) | 2026-03-01 | Combined architecture selected + details |
| Verification | 2026-03-01 | Final constraint check |
| Output | 2026-03-01 | Compiling spec |

---

## Notes

> Free-form observations during interview.

- Phase 0: User wants "vector activation" approach — not verbose instruction dumping. This aligns with prompt-craft insight that roles have diminishing returns on Claude 4.6+ but domain-specific terminology activation still works.
- Phase 0: User explicitly asked to consult prompt-craft and vector activation best practices.
- Phase 3: User confirmed Option B (Voss + Surgical Complements), sparring as core, inline brackets.
- Phase 3: Final spec compiled to tactical-empathy-spec.md. Interview complete.
