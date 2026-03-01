# Build Log: tactical-empathy Skill

**Date:** 2026-03-01
**Plugin:** `ajbm-communication` (new)
**Skill:** `tactical-empathy`
**Effort:** Advanced (Algorithm mode)
**Status:** Built, committed, tested, refined. All 15 refinements applied.

---

## 1. Origin

Built from a completed Interview Ideation workflow that produced two artifacts:
- `tactical-empathy-spec.md` — full implementation spec with constraint registry, architecture, file structure
- `interview-log-negotiation-skill.md` — working log from the ideation session

The ideation session ran two parallel research agents (voss-research + vector-activation-research) and produced 9 decisions (D1-D9) through a 7-phase interview process. The spec was "ready for implementation."

### Key Ideation Decisions (D1-D9)

| # | Decision | Rationale |
|---|----------|-----------|
| D1 | Covers negotiation + difficult conversations + persuasion (not email review) | User selected 3 of 4 trigger categories |
| D2 | Value = structured activation + behavioral dispositions, not knowledge recall | Claude already knows Voss — the skill changes how it thinks |
| D3 | Voss + Surgical Complements (~180 lines SKILL.md) | 70% Voss core, 4 gap-fillers earning their place |
| D4 | Sparring is a CORE workflow, not optional | Practice-before-real-thing as primary value |
| D5 | Two workflows: Analyze + Spar (dropped Live) | Live too situational for dedicated workflow |
| D6 | Inline bracket coaching `[COACH:]` after each exchange | Real-time learning without breaking immersion |
| D7 | Name: `tactical-empathy` | Names the philosophy, not the book |
| D8 | New plugin: `ajbm-communication` | Home for future communication skills |
| D9 | Analyze produces written dossier file | Persistent, reviewable before actual negotiation |

---

## 2. Build Session

### 2.1 Clarification Phase

**Two open questions from spec resolved before building:**

1. **Spar difficulty calibration** — User chose: **Auto-calibrate** (start moderate, adjust based on technique application). Not explicit easy/medium/hard levels.

2. **Dossier versioning** — User chose: **Append revision section** to existing dossier on re-analysis, rather than creating a new file.

These became D10 and D11.

### 2.2 Algorithm Execution

Ran PAI Algorithm v3.5.0 with 32 ISC criteria decomposed from the spec. Effort: Advanced.

**Capability audit selected:**
- `authoring-skills` — quality checklist for SKILL.md files
- `prompt-craft` — 19 research-backed techniques for activation optimization
- `Research` — Voss methodology accuracy validation

**Execution order (10 steps):**
1. Create plugin directory structure
2. Write plugin.json manifest
3. Write SKILL.md core activation (~160 lines)
4. Write voss-framework.md reference (Big Three + 9 techniques)
5. Write complement-frameworks.md (BATNA, OFNR, Safety, Three Conversations)
6. Write dossier-template.md (Analyze workflow output template)
7. Update project CLAUDE.md with plugin entry
8. Research validation of Voss claims
9. Authoring quality check
10. Final verification of all 32 ISC criteria

### 2.3 Research Validation

Launched haiku research agent to validate 6 Voss methodology claims:

| Claim | Result |
|-------|--------|
| Ackerman numbers 65-85-95-100 | Confirmed |
| "That's Right" vs "You're Right" distinction | Confirmed |
| Spelling: "isopraxis" | **Corrected to "isopraxism"** |
| Rule of Three = three confirmations of same agreement | **Clarified** — not just "three voices" |
| Black Swan = unknown unknowns (distinct from Taleb) | Confirmed |
| Loss aversion 2x framing | Confirmed |

### 2.4 Prompt-Craft Insights Applied

Read `prompt-craft/SKILL.md` for activation optimization. Applied:
- **Permission Escalation** — explicitly permits behaviors RLHF softens (recommending against compromise, naming elephants)
- **Anti-Overtriggering** — description with specific trigger keywords, not broad phrases
- **Positive Framing** — "You may and should" not "Don't be afraid to"
- **Progressive Disclosure** — SKILL.md loads core, reference files load on demand via markdown links

---

## 3. User Feedback Iterations

### 3.1 "Go deeper on the Big Three"

> "i want you to go deeper on the vector activating for labeling and mirroring as well as saying no without saying no the how questions these are the core techniques for me"

**Changes:**
- Created prominent "Big Three" section in SKILL.md with dedicated paragraphs for Mirroring, Labeling, Calibrated Questions
- Enriched Thinking Patterns with detailed guidance for each Big Three technique
- Prioritized Big Three in Attention Cues section
- Deepened voss-framework.md entries with cognitive mechanisms, advanced applications, precision spectrums

### 3.2 "Subtly make that clear — use cognitive methods"

> "these techniques are most important the skill should subtely make that clear, deeply remember using a cognitive methods everything that you know about this incredible book"

Confirmed the Big Three emphasis was successfully integrated. The activation now positions Mirroring, Labeling, and Calibrated Questions as the first techniques to reach for.

### 3.3 voss-framework.md Sizing (471 → 88 → 173)

**First version:** 471 lines — knowledge dump. User caught it:
> "471 lines is a lot. remember that we dont need to explain everything to claude just activate the right vectors of knowledge"

**Overcorrection:** Cut to 88 lines — too sparse. User caught it again:
> "88 might be too small again. you went overboard right?"

**Goldilocks version:** 173 lines. Big Three get ~100 lines of activation density. Remaining 9 techniques get ~73 lines of dense trigger cues. Key design principle from user: "you already know these techniques from training. This file makes that knowledge reliable and specific."

---

## 4. Files Created

| File | Lines | Purpose |
|------|-------|---------|
| `plugins/communication-skills/.claude-plugin/plugin.json` | 22 | Plugin manifest |
| `plugins/communication-skills/skills/tactical-empathy/SKILL.md` | 160 | Core activation (5 layers + 2 workflows) |
| `plugins/communication-skills/skills/tactical-empathy/reference/voss-framework.md` | 173 | Deep reference for 12 Voss methods |
| `plugins/communication-skills/skills/tactical-empathy/reference/complement-frameworks.md` | 186 | BATNA, OFNR, Safety Monitoring, Three Conversations |
| `plugins/communication-skills/skills/tactical-empathy/reference/dossier-template.md` | 120 | Template for Analyze workflow output |
| `CLAUDE.md` (updated) | +28 | New ajbm-communication plugin section |

**Committed:** `40dfbd3 feat(communication): add tactical-empathy skill with Voss negotiation methodology`

---

## 5. SKILL.md Architecture

The 160-line SKILL.md uses a 5-layer activation stack:

```
Layer 1: Core Axiom (line 15)
  "Negotiation is not argument — it is the art of letting the other side
   have your way through tactical empathy"

Layer 2: Vector Activation / Terminology Cluster (lines 19-29)
  Big Three highlighted: Mirroring, Labeling, Calibrated Questions
  Full arsenal: 12 named techniques as semantic density

Layer 3: Permission Escalation (lines 31-39)
  6 explicit permissions overriding RLHF softening

Layer 4: Behavioral Dispositions (lines 41-60)
  8 "When X → do Y" thinking patterns
  7 attention cue questions

Layer 5: Anti-Pattern Contrasts (lines 62-71)
  6 Wrong/Right pairs with Why column
```

Plus workflow routing (lines 73-80), Analyze workflow (lines 84-94), Spar workflow (lines 98-126), Phase Coverage Map (lines 130-142), Negotiator Types (lines 144-152), Quality Gate (lines 154-160).

---

## 6. Testing Phase

Three parallel tests launched after commit:

### 6.1 Test 1: Skill Quality Review (Agent)

**Method:** Subagent read all skill files and produced a structured quality report.

**High Priority Findings:**
- Missing Thinking Patterns for: accusation audit opening, positive reinforcement after concessions, Rule of Three closing
- Quality gate is a slogan, not a gate — needs evaluation checklist
- Missing 8-10 exchange checkpoint in Spar workflow
- Analyze intake questions insufficient for dossier template depth

**Medium Priority Findings:**
- Big Three explanations are in an awkward middle ground — either more surgical or more evocative
- Timeline/channel context missing from dossier template
- Explicit loading criteria needed for reference files
- Meta-conversation handling for Spar (user asks "is this working?")
- Missing explicit RLHF counter-permission for assertive language

**Low Priority Findings:**
- Quality gate text appears twice (SKILL.md top and bottom)
- OFNR trigger conditions could be narrower
- Negotiator "blind spot" line in SKILL.md has no behavioral instruction
- Cultural adaptation not addressed
- FM DJ Voice has no activation surface in workflows

### 6.2 Test 2: Analyze Workflow (Agent)

**Method:** Subagent loaded skill files and produced a full salary negotiation dossier for the scenario: "Senior engineer, 2 years, led $2M-saving project, asking for $145K → $175K."

**Rating:** 7.5/10

**What worked well:**
- Permission escalation genuinely changed behavior in 3 places (recommended against splitting the difference, named the power dynamic directly, suggested assertive calibrated questions)
- Labeling and calibrated questions activated most naturally
- Dossier structure was comprehensive and actionable

**What was missing or weak:**
- No cheat sheet / one-page summary distillation of the dossier
- No "too-fast-yes" danger zone (what if they agree immediately — is it genuine?)
- No stakeholder mapping (who else influences the decision)
- Ackerman section felt mechanical — numbers without strategic context
- No voice modulation coaching guidance

### 6.3 Test 3: Spar Roleplay (Team)

**Method:** Two-agent team (`coach` + `practitioner`) exchanged messages. Coach played Sarah Chen (VP Engineering, Analyst type) with `[COACH:]` annotations. Practitioner made realistic mistakes and sent meta-evaluation.

**Team:** `tactical-empathy-spar-test`
**Exchanges:** 6 rounds + full debrief
**Coach characterization:** Sarah Chen — data-driven, methodical, stressed about retention but pressured by finance
**Hidden Black Swan:** Two recent senior engineer departures

**Session Arc:**
1. Practitioner opened direct (no accusation audit) — Sarah pushed back on budget/fairness
2. Good mirror ("watching every line item?"), then broke it by arguing and using "fair"
3. Self-corrected mid-redirect, mirrored Black Swan hint ("changes on the team?")
4. Landed surgical label, then undermined it with explicit recruiter threat — Sarah went cold
5. Strong recovery — accepted her frame, built collaborative case with OFNR, double calibrated question close
6. Clean Rule of Three close, Sarah committed to taking case to finance

**Debrief Highlights:**
- Strengths: mirroring instinct, Black Swan discovery, surgical labeling, calibrated questions, self-correction, Rule of Three
- Growth edges: accusation audit openers, discipline after labels (label + silence, not label + argument), implicit over explicit leverage
- Biggest lesson: the recruiter threat destroyed momentum that the label had built — unspoken implications are far more powerful than stated threats

**Practitioner Meta-Evaluation: 8/10**

What worked:
- `[COACH:]` annotations were "arguably the most valuable part" — directly changed next response at least twice
- Dual-track format (in-character + coaching) maintained immersion — "felt like having an earpiece during a live conversation"
- Technique suggestions specific enough to act on (exact words, not abstract advice)
- Sarah's characterization was consistent and realistic throughout (Analyst-type behaviors)

What was missing:
- **Pre-session calibration:** No brief primer on "three techniques most relevant to this counterpart type" before starting
- **Real-time progress indicator:** No sense of whether overall negotiation was going well until debrief
- **Ackerman plan:** Mentioned once but never walked through the actual sequence for this scenario's numbers
- **Replay feature:** Debrief says what to do differently, but no option to re-do a specific exchange with coaching applied

---

## 7. Proposed Refinements

Based on all three tests, these are the concrete improvements to consider:

### Priority 1 — Should Do

| # | What | Where | Why |
|---|------|-------|-----|
| R1 | Add 3 missing Thinking Patterns: accusation audit opening, positive reinforcement after concessions, Rule of Three closing | SKILL.md lines 41-50 | Core techniques without behavioral dispositions won't activate reliably |
| R2 | Strengthen Quality Gate from slogan to mini-checklist | SKILL.md lines 154-160 | "Am I compromising for comfort?" alone isn't actionable enough |
| R3 | Add exchange checkpoint to Spar (after 8-10 exchanges, offer debrief or continue) | SKILL.md lines 105-111 | Prevents sessions from dragging without progress |
| R4 | Expand Analyze intake to ask about timeline, communication channel, and stakeholders | SKILL.md lines 86-87 | Dossier template has sections that can't be filled without this context |
| R5 | Add "too-fast-yes" danger zone to dossier template | dossier-template.md | Immediate agreement often signals counterfeit yes — critical to catch |

### Priority 2 — Nice to Have

| # | What | Where | Why |
|---|------|-------|-----|
| R6 | Add cheat sheet / one-page summary section to dossier output | dossier-template.md | Users want a quick reference to take into the actual conversation |
| R7 | Add meta-conversation handling to Spar ("User asks: is this working?") | SKILL.md Spar section | Currently unclear how to handle breaks in roleplay |
| R8 | Add stakeholder mapping to dossier template | dossier-template.md | Who else influences the decision beyond the counterpart |
| R9 | Make Ackerman guidance less mechanical — add strategic context | voss-framework.md | Numbers alone feel like a recipe; need the "why" of each step |
| R10 | Add explicit RLHF counter-permission for assertive language | SKILL.md Permission Escalation | Some assertive techniques still get softened |
| R11 | Add pre-session calibration to Spar setup ("3 techniques most relevant to this counterpart type") | SKILL.md Spar Setup | Practitioner rated 8/10 — missing primer caused avoidable accusation-audit skip |
| R12 | Add "replay moment" option to Spar debrief ("re-do exchange 4 with coaching applied") | SKILL.md Spar Debrief | Debrief tells what to do differently but no chance to practice the correction |

### Priority 3 — Consider Later

| # | What | Where | Why |
|---|------|-------|-----|
| R13 | FM DJ Voice activation surface in workflows | SKILL.md | Currently described but never triggered |
| R14 | Cultural adaptation notes | complement-frameworks.md | Different cultures have different norms for directness |
| R15 | Negotiator blind spot line needs behavioral instruction | SKILL.md line 152 | "Know your own type" without guidance on what to do about it |

---

## 8. Verification Summary

All 32 ISC criteria PASS. Full verification in PRD at:
`~/.claude/MEMORY/WORK/20260301-153000_build-tactical-empathy-skill/PRD.md`

### Key Verifications

| Category | Criteria | Status |
|----------|----------|--------|
| Plugin Structure | 6 criteria (dirs, manifest, naming) | All PASS |
| SKILL.md Core | 8 criteria (frontmatter, axiom, techniques, permissions, dispositions, anti-patterns, quality gate) | All PASS |
| Workflow Routing | 4 criteria (routing table, defaults, phase map, negotiator types) | All PASS |
| Analyze Workflow | 4 criteria (process, output path, template ref, re-analysis) | All PASS |
| Spar Workflow | 4 criteria (setup, coaching annotations, auto-calibrate, debrief) | All PASS |
| Reference Files | 4 criteria (voss 12 methods, complements 4 frameworks, dossier template, on-demand loading) | All PASS |
| Documentation | 2 criteria (CLAUDE.md updated, follows pattern) | All PASS |

---

## 9. Design Insights

### What worked well in this build

**Vector activation over knowledge dumping.** The spec's core insight proved correct. The 160-line SKILL.md activates expert negotiation behavior without re-explaining what's in the training data. The voss-framework.md reference (173 lines) provides precision cues, not explanations.

**Progressive disclosure.** SKILL.md loads core activation. Reference files load on demand. This keeps context cost low for simple queries while allowing deep dives when needed.

**Permission escalation.** The Analyze test confirmed this genuinely changed behavior. Without it, Claude defaults to compromise and softening. With it, Claude recommended against splitting the difference in 3 places.

**The Big Three emphasis.** User correctly identified that Mirroring, Labeling, and Calibrated Questions are THE core techniques. Everything else is supporting cast. The skill now makes this clear structurally (Big Three section first, detailed paragraphs, priority in Thinking Patterns and Attention Cues).

### What required iteration

**Reference file sizing.** The goldilocks problem (471 → 88 → 173) showed that "vector activation" doesn't mean minimal — it means precise. The right amount is enough to activate reliable, specific behavior without re-teaching.

**User feedback as calibration.** Three rounds of user feedback each improved the skill. The user caught both overcorrection (88 lines too sparse) and undercorrection (Big Three not emphasized enough). This suggests skills benefit from a build-test-refine loop with the domain expert.

---

## 10. Source Files

| File | Role |
|------|------|
| `/Users/andremachon/Projects/claude-skills/tactical-empathy-spec.md` | Implementation spec (from Interview Ideation) |
| `/Users/andremachon/Projects/claude-skills/interview-log-negotiation-skill.md` | Interview working log (from Ideation) |
| `~/.claude/MEMORY/WORK/20260301-153000_build-tactical-empathy-skill/PRD.md` | Algorithm PRD with 32 ISC criteria |
| `~/.claude/PAI/Algorithm/v3.5.0.md` | Algorithm execution instructions |

---

*Build session used PAI Algorithm v3.5.0 in Advanced mode. Research validation via haiku agent. Testing via 3 parallel agents (quality reviewer, analyze workflow, spar team). Total: 32/32 ISC criteria verified.*
