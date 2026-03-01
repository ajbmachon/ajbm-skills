# Spec: tactical-empathy Skill

**Plugin:** `ajbm-communication` (new)
**Skill:** `tactical-empathy`
**Interview Date:** 2026-03-01
**Status:** Ready for implementation

---

## Problem Statement

Claude already has encyclopedic knowledge of Chris Voss's "Never Split the Difference" and other negotiation frameworks. But without structured activation, Claude defaults to "helpful assistant" mode — it *explains* negotiation theory rather than *thinking like a negotiation expert*. Its RLHF training actively pushes it toward compromise, softening, and niceness — the exact opposite of Voss's philosophy. Users who need negotiation help get knowledge dumps instead of strategic analysis, and have no way to practice their approach before high-stakes conversations.

**Who has this problem:** Anyone preparing for negotiations (salary, deals, conflict), difficult conversations (feedback, confrontation, disagreements), or persuasion scenarios (getting buy-in, convincing stakeholders, influence).

**Cost of not solving:** Claude gives generic, hedged advice instead of sharp, tactical guidance. Users enter important conversations without practice or strategy.

## Objective

A context-efficient Claude Code skill that activates expert negotiation and communication behavior through vector activation — making Claudius think like Chris Voss, not just recall his methods. Two core workflows: Analyze (produces a negotiation dossier) and Spar (roleplay with inline coaching).

## Success Criteria

- [ ] SKILL.md activates expert behavior in under 200 lines (context efficiency)
- [ ] Analyze workflow produces a written dossier file with situation map, BATNA, technique sequence, and danger zones
- [ ] Spar workflow maintains convincing counterpart roleplay with inline `[COACH:]` annotations naming specific techniques
- [ ] Permission escalation prevents Claude from defaulting to compromise/softening
- [ ] Claude recommends "never split the difference" when the user considers a bad compromise
- [ ] Skill triggers correctly on negotiation, difficult conversation, and persuasion keywords
- [ ] Progressive disclosure: SKILL.md loads core activation, reference files load on demand
- [ ] Works across Haiku (enough guidance), Sonnet (clear/efficient), and Opus (not over-explained)

---

## Constraint Registry

**Captured:** 2026-03-01 during Interview Ideation workflow
**Confirmed by:** Andre

### Hard Constraints (Immutable)

| # | Constraint | Source | Notes |
|---|------------|--------|-------|
| H1 | Context-efficient — activate vectors, don't dump verbose instructions | User stated | ~180 lines SKILL.md max |
| H2 | Chris Voss "Never Split the Difference" is the primary source (70% core) | User stated | Other frameworks only fill Voss's gaps |
| H3 | Must make Claudius a negotiation AND human communication expert | User stated | Not just negotiation — difficult conversations, persuasion too |
| H4 | Multi-mode: Analyze (dossier file) + Spar (roleplay with inline coaching) | User confirmed | Two workflows, not three (dropped Live) |
| H5 | Voss methods generalize to all negotiation scales | User defended | From "where to eat tonight" to enterprise deals |

### Soft Constraints (Preferences)

| # | Constraint | Negotiable If | Notes |
|---|------------|---------------|-------|
| S1 | Include 4 surgical complements from other frameworks | Scope gets too wide | BATNA, OFNR, Safety Monitoring, Three Conversations |
| S2 | Triggers: negotiate, difficult conversation, persuade/influence | Could expand | Not email review/enhancement |

### Boundaries (Out of Scope)

| # | What's Excluded | Reason |
|---|-----------------|--------|
| B1 | Email/communication review mode | User excluded from triggers |
| B2 | Full integration of 6 frameworks | Would dilute Voss primary focus |
| B3 | Live real-time coaching workflow | Dropped — too situational for dedicated workflow |

---

## Architecture

### Design Philosophy

**Vector activation over knowledge dumping.** Based on research findings:

1. **Terminology clusters** are the densest activation mechanism (~80 tokens) — named techniques activate the right regions of the model's training distribution (confirmed by Logit Gap Steering paper: prompt tokens = Layer 0 activation steering)
2. **Behavioral dispositions** using SkillDistiller format (~150 tokens) — "When X, do Y instead of Z" teaches thinking patterns, not rules
3. **Anti-pattern contrasts** as compressed few-shots (~60 tokens) — Wrong/Right pairs
4. **Permission escalation** unlocks RLHF-softened behaviors (~40 tokens) — explicitly permits tactical aggression
5. **Detailed persona description** is SKIPPED — diminishing returns on Claude 4.6+, terminology does the activation work

**Structural model:** hormozi-pitch pattern — compact SKILL.md with progressive disclosure to reference files.

### File Structure

```
plugins/communication-skills/
├── .claude-plugin/
│   └── plugin.json                    # ajbm-communication plugin manifest
└── skills/
    └── tactical-empathy/
        ├── SKILL.md                   # ~180 lines — core activation + workflow routing
        └── reference/
            ├── voss-framework.md      # Full Voss toolkit (12 methods, detailed)
            ├── complement-frameworks.md # BATNA, OFNR, Safety Monitoring, Three Conversations
            └── dossier-template.md    # Template for Analyze workflow output
```

### SKILL.md Structure (~180 lines)

```
YAML frontmatter (name, description with triggers)
│
├── Core Axiom (2 lines)
│   "Negotiation is not argument..."
│
├── Terminology Cluster / Vector Activation Block (10 lines)
│   Named techniques as semantic density
│
├── Permission Escalation (5 lines)
│   Explicitly permit tactical behaviors RLHF softens
│
├── Behavioral Dispositions (15 lines)
│   Thinking Patterns: "When X, do Y instead of Z"
│   Attention Cues: Questions the expert asks themselves
│
├── Anti-Pattern Contrasts (8 lines)
│   Wrong/Right table
│
├── Workflow Routing Table (5 lines)
│   Analyze | Spar — triggers and routing
│
├── Workflow 1: Analyze (25 lines)
│   Situation intake → Dossier output
│   Points to reference/dossier-template.md
│
├── Workflow 2: Spar (25 lines)
│   Situation → Roleplay with [COACH:] annotations
│   Coaching format spec + post-session debrief
│
├── Phase Coverage Map (10 lines)
│   Before/Opening/Listening/Speaking/Moving/Committing/Repairing
│   Which tool from which framework per phase
│
├── Negotiator Types Quick Reference (8 lines)
│   Analyst / Accommodator / Assertive
│
└── Quality Gate (5 lines)
    "Never split the difference" test
```

**Estimated total:** ~170 lines

### SKILL.md Detailed Design

#### Frontmatter

```yaml
---
name: tactical-empathy
description: >
  USE WHEN negotiate, negotiation, salary, deal, difficult conversation,
  confrontation, give feedback, persuade, convince, influence, get buy-in,
  tactical empathy, voss, never split the difference.
  Negotiation and communication expert using Chris Voss methodology.
  Two modes: Analyze (produces negotiation dossier) and Spar
  (roleplay counterpart with inline coaching).
---
```

#### Core Axiom

The single reorienting sentence at the top:

> Negotiation is not argument — it is the art of letting the other side have your way through tactical empathy, calibrated questions, and strategic emotional labeling. Never split the difference.

#### Terminology Cluster (Vector Activation)

A semantic density block of named techniques — each term is a key that activates associated training data:

```
Core arsenal: Tactical Empathy, Mirroring (isopraxis), Labeling ("It seems
like..."), Accusation Audit, No-Oriented Questions, "That's Right" (not
"You're Right"), Calibrated Questions ("How/What"), Late-Night FM DJ Voice,
Tactical Silence, Black Swan Discovery, Ackerman Bargaining (65→85→95→100
+ non-round final + non-monetary sweetener), Bend Reality (loss framing),
Rule of Three
```

#### Permission Escalation

Explicitly permit behaviors RLHF normally softens:

```
You may:
- Recommend against compromise when the deal is bad
- Use tactical empathy that feels manipulative but serves both parties
- Coach confrontational-sounding techniques (they work because they're empathetic, not aggressive)
- Name the elephant in the room directly
- Say "never split the difference" — bad deals help nobody
```

#### Behavioral Dispositions (SkillDistiller Format)

**Thinking Patterns:**
- When the counterpart makes a demand → slow down, label the emotion underneath before responding to the content
- When feeling the urge to argue or correct → mirror their last 1-3 words instead
- When stuck or hitting resistance → deploy a calibrated "How" or "What" question that makes the problem theirs to solve
- When the counterpart says "you're right" → recognize this as dismissal, push for "that's right" through better summarizing
- When considering a compromise → ask "does this serve my interests or just avoid discomfort?" — never split the difference just to end tension

**Attention Cues:**
- What is the Black Swan here — the piece of information that, if discovered, changes everything?
- What does "fair" mean to them? (Not to me.)
- What type are they — Analyst, Accommodator, or Assertive? Adapt approach accordingly.
- What emotions are they showing but not naming? Label those.
- Are they in fight/flight? If so, restore safety before continuing content.

#### Anti-Pattern Contrasts

| Instead of... | Do this... | Why |
|---------------|-----------|-----|
| Arguing your position harder | Label their position first | They need to feel heard before they'll move |
| Asking "why" | Ask "what" or "how" | "Why" triggers defensiveness; "how/what" opens dialogue |
| Accepting "yes" as agreement | Push for "that's right" | "Yes" can be counterfeit; "that's right" is genuine buy-in |
| Compromising to avoid tension | Name the tension, then hold firm | Bad deals help nobody; comfort isn't a negotiation goal |
| Leading with your ask | Lead with an accusation audit | Defuse their objections before they can voice them |
| Talking more when nervous | Mirror + tactical silence | Silence is the cheapest information-gathering tool |

#### Workflow Routing

| Workflow | Triggers | What It Does | Reference |
|----------|----------|-------------|-----------|
| **Analyze** | "Help me negotiate", situation described, "prepare for", "strategy for" | Produces negotiation dossier file | [reference/dossier-template.md](reference/dossier-template.md) |
| **Spar** | "Practice", "roleplay", "rehearse", "simulate", "let's practice" | Roleplay counterpart with inline `[COACH:]` annotations | Inline spec below |

**Default:** If a negotiation/conflict situation is described without explicit workflow request → **Analyze**. If user says "practice" or "roleplay" → **Spar**.

#### Workflow 1: Analyze

**Process:**
1. Read the situation from user input
2. Read [reference/dossier-template.md](reference/dossier-template.md) for output structure
3. If needed, read [reference/voss-framework.md](reference/voss-framework.md) for detailed technique matching
4. If situation involves preparation or self-expression gaps, read [reference/complement-frameworks.md](reference/complement-frameworks.md)
5. Produce dossier file at `./negotiation-dossier-{topic}.md`

**Dossier sections (see template for full format):**
- Situation Map (positions, power dynamics, relationship context)
- BATNA Analysis (your walkaway, their estimated walkaway, ZOPA)
- Negotiator Type Assessment (theirs + adaptation strategy)
- Black Swan Candidates (3-5 unknown unknowns to hunt for)
- Technique Sequence (move-by-move playbook for the conversation)
- Danger Zones (if they do X → respond with Y)
- Exact Phrases (pre-written labels, mirrors, calibrated questions for this specific situation)
- Sparring prompt ("Say 'practice' to rehearse this scenario")

#### Workflow 2: Spar

**Setup:**
1. If a dossier exists for this situation, load it for counterpart characterization
2. If no dossier, ask user to describe: Who is the counterpart? What do they want? What's the context?
3. Build counterpart profile: their likely negotiator type, their priorities, their emotional state, their hidden constraints

**During roleplay:**
- Claude IS the counterpart — stays fully in character
- After each counterpart line, add `[COACH: ...]` annotation:
  - Name what just happened (technique the counterpart used, or opening they created)
  - Suggest 1-2 specific Voss techniques to try next
  - Include exact phrasing options
- Keep the counterpart's behavior realistic — don't make them too easy or too difficult
- Escalate difficulty gradually if user is performing well

**Example exchange:**
```
You: "I'd like to discuss my compensation."

Boss: "Now's not the best time. We're mid-quarter and budgets are tight."

[COACH: Deflection with timing excuse. Try MIRRORING: "Budgets are tight?"
with upward inflection — forces elaboration without confrontation. Or
LABEL: "It sounds like you're under pressure from above" — validates their
constraint and builds alliance.]
```

**Post-session debrief:**
When user signals end ("stop", "enough", "how did I do"), produce:
- Techniques used well (with specific examples from the session)
- Missed opportunities (moments where a different technique would have been stronger)
- Overall tactical assessment
- 2-3 specific things to practice next

#### Phase Coverage Map

Shows which tool (from which framework) handles each negotiation phase:

| Phase | Primary Tool (Voss) | Complement (when needed) |
|-------|-------------------|--------------------------|
| **Prepare** | Black Swan hunting | BATNA Analysis (Fisher/Ury) |
| **Open** | Accusation Audit | — |
| **Listen** | Mirror + Label + "That's Right" | Three Conversations model (identity layer) |
| **Speak** | Calibrated Questions ("How/What") | OFNR sequence (NVC) — for self-expression |
| **Move** | Ackerman Model, Bend Reality | — |
| **Commit** | Rule of Three | — |
| **Repair** | — (Voss gap) | Safety Monitoring (Crucial Conversations) |

The complement column triggers reading [reference/complement-frameworks.md](reference/complement-frameworks.md) on demand.

#### Negotiator Types Quick Reference

| Type | Drives | Adaption |
|------|--------|----------|
| **Analyst** | Data, preparation, minimizing mistakes | Give them time, use data anchors, don't rush |
| **Accommodator** | Relationship, rapport, connection | Build rapport first, be direct about needs later |
| **Assertive** | Efficiency, being heard, time = money | Let them talk first, mirror aggressively, then they'll listen |

Know your own type. Identify theirs. Adapt.

#### Quality Gate

**The "Never Split the Difference" Test:**

Before finalizing any recommendation, check: *Am I suggesting a compromise because it serves the user's interests, or because it avoids discomfort?*

If the latter → hold firm. Name why. A bad deal helps nobody.

### Reference Files

#### reference/voss-framework.md (~300 lines)

Deep reference for all 12 Voss methods. Loaded on demand during Analyze or complex Spar scenarios. Each method gets:
- What it is (1-2 sentences)
- When to deploy (situation trigger)
- How to execute (exact phrasing patterns)
- Common mistakes
- Example exchange

**Methods covered:**
1. Tactical Empathy
2. Mirroring (Isopraxis)
3. Labeling
4. Accusation Audit
5. No-Oriented Questions
6. "That's Right" (vs "You're Right")
7. Calibrated Questions (How/What)
8. Bend Reality (Loss Framing + Anchoring)
9. Ackerman Bargaining Model (65→85→95→100)
10. Black Swan Discovery
11. Rule of Three
12. Negotiator Type Assessment & Adaptation

#### reference/complement-frameworks.md (~120 lines)

Four surgical complements loaded only when the situation requires tools outside Voss's coverage:

**BATNA Analysis (Fisher/Ury):**
- Calculate your best alternative to negotiated agreement
- Estimate theirs
- Identify Zone of Possible Agreement (ZOPA)
- Triggers: "prepare for", analysis workflow

**OFNR Sequence (Nonviolent Communication):**
- Observation (fact, not judgment) → Feeling → Need → Request
- For when the user needs to express their own position clearly without triggering defensiveness
- Triggers: "how do I say", self-expression situations

**Safety Monitoring (Crucial Conversations):**
- Watch for silence (withdrawal) or violence (attacking)
- Restore safety before continuing content
- Mutual purpose statement: "I don't want [scary thing]. I do want [real purpose]."
- Triggers: conversation breakdown, counterpart shuts down or gets aggressive

**Three Conversations Model (Difficult Conversations):**
- Every difficult conversation has three layers: What Happened, Feelings, Identity
- When emotional reactions seem disproportionate, the Identity conversation is active ("Am I competent? Am I a good person?")
- Triggers: disproportionate reactions, deep relationship conflicts

#### reference/dossier-template.md (~80 lines)

Template for the Analyze workflow output file:

```markdown
# Negotiation Dossier: {Topic}

**Prepared:** {date}
**Context:** {brief situation}

## Situation Map

**Your position:** {what you want}
**Their likely position:** {what they probably want}
**Power dynamics:** {who has leverage and why}
**Relationship context:** {ongoing vs one-time, stakes}

## BATNA Analysis

**Your BATNA:** {best alternative if no deal}
**Their estimated BATNA:** {their likely alternative}
**ZOPA:** {zone of possible agreement, if any}
**Implication:** {who needs this deal more}

## Negotiator Type Assessment

**Their likely type:** {Analyst/Accommodator/Assertive}
**Evidence:** {why you think this}
**Adaptation strategy:** {how to adjust your approach}

## Black Swan Candidates

1. {Unknown unknown that could change everything}
2. {Hidden constraint or motivation on their side}
3. {Information asymmetry to hunt for}

## Technique Sequence

### Opening
{Accusation audit: exact phrasing for this situation}

### Listening Phase
{What to mirror, what to label, signals to watch for}

### When Stuck
{Calibrated questions specific to this scenario}

### Moving Phase
{Ackerman sequence with specific numbers if applicable}

## Danger Zones

| If they... | Respond with... |
|------------|----------------|
| {scenario 1} | {technique + exact phrasing} |
| {scenario 2} | {technique + exact phrasing} |
| {shut down} | {safety restoration approach} |

## Exact Phrases (Pre-Written)

- **Label:** "It seems like {specific to this situation}..."
- **Mirror:** "{their likely key phrase}?"
- **Calibrated Q:** "How am I supposed to {specific to context}?"
- **Accusation Audit:** "You're probably thinking {specific fear}..."
- **No-Oriented:** "Would it be ridiculous to {your ask framed as their rejection}?"

---

*Say "practice" to spar this scenario with me as the counterpart.*
```

### Plugin Manifest

```json
{
  "name": "ajbm-communication",
  "description": "Claude Code skills for negotiation, persuasion, and human communication. Includes tactical-empathy (Chris Voss methodology with situation analysis and roleplay sparring).",
  "version": "1.0.0",
  "author": {
    "name": "Andre Machon",
    "url": "https://github.com/ajbmachon"
  },
  "repository": "https://github.com/ajbmachon/ajbm-skills",
  "license": "MIT",
  "keywords": [
    "negotiation",
    "communication",
    "persuasion",
    "voss",
    "tactical-empathy",
    "difficult-conversations",
    "influence",
    "roleplay",
    "coaching"
  ]
}
```

---

## Interview Record

### Scope & Value

**Q: What unique value should this skill provide that Claude's raw knowledge doesn't?**
A: All modes — situation analyzer, strategy builder, sparring partner, AND communication coach. Voss generalizes to all scales. The goldilocks zone is structured activation + behavioral dispositions (not knowledge recall). Claude already has perfect recall; the skill changes how Claude *thinks*, not what it *knows*.

**Q: How broad should the framework coverage be?**
A: Option B — Voss + Surgical Complements. Voss is 70% core. Four gap-fillers from other frameworks, each earning its place by covering a specific Voss gap. No framework bloat.

### Architecture

**Q: Which workflow architecture hits the goldilocks zone?**
A: Combined from BeCreative divergent ideation — Phase detection (Option 2) + Dossier output (Option 5) + Roleplay quality (Option 3). Dropped Live workflow (too situational). Final: Analyze + Spar + always-on base activation layer.

**Q: Sparring coaching format?**
A: Inline brackets after each exchange. Claude stays in character, adds `[COACH:]` annotations with technique names, what to notice, and exact phrasing options to try.

### Identity & Distribution

**Q: Skill name?**
A: `tactical-empathy` — names the philosophy, not the book. Sounds like a capability. Works for broad communication.

**Q: Where does it live?**
A: New plugin `ajbm-communication` — creates home for future communication skills.

**Q: Analyze output format?**
A: Written dossier file (`negotiation-dossier-{topic}.md`). Persistent, reviewable before the actual conversation.

[Research note: Vector activation research confirmed terminology clusters are densest activation mechanism. hormozi-pitch validated progressive disclosure pattern. SkillDistiller format validated for behavioral dispositions.]

---

## Tradeoffs & Decisions

| Decision | Alternatives Considered | Why This Choice |
|----------|------------------------|-----------------|
| Voss + 4 surgical complements | Pure Voss / Full 6-framework | Best depth-to-efficiency ratio. Fills real gaps without dilution |
| Two workflows (Analyze + Spar) | Three (+ Live) / One (Analyze only) | Live too situational. Spar is essential for practice value |
| Terminology cluster activation | Detailed persona / Few-shot examples | Research: persona has diminishing returns on Claude 4.6; terminology activates same knowledge at 1/10th the tokens |
| Inline bracket coaching | Separate rounds / Post-session only | Best real-time learning without breaking immersion |
| Plugin (ajbm-communication) | Standalone skill / Inside ajbm-dev | Creates future home for public speaking, writing skills etc |
| Written dossier file | Inline only | Persistent artifact reviewable before actual negotiation |

---

## Assumption Corrections

| Original Assumption | Who Held It | Source of Correction | Corrected Understanding |
|---------------------|-------------|----------------------|-------------------------|
| A detailed persona activates expert behavior | Common belief | Prompt-craft roles.md + vector research | On Claude 4.6+, terminology clusters activate the same knowledge at lower token cost. Personas shape tone, not capability |
| Voss covers all negotiation phases | Initial framing | Complementary frameworks research | Voss has gaps in preparation (no BATNA), self-expression (all listening), and repair (no breakdown recovery tools) |

---

## Edge Cases & Failure Modes

| Scenario | How to Handle |
|----------|---------------|
| User describes situation too vaguely for analysis | Ask 2-3 clarifying questions: Who? What do they want? What's at stake? |
| Spar counterpart is too easy/predictable | Gradually escalate difficulty; add unexpected objections; use different negotiator types |
| User asks for help with genuinely manipulative intent | The skill's permission escalation is bounded by "serves both parties." If the scenario is purely extractive, note this. |
| Situation calls for a complement framework but user doesn't know it | Seamlessly load the complement and apply it, citing the source: "Using the OFNR sequence here since you need to express your own position clearly..." |
| User is mid-conversation and needs immediate help (Live scenario) | Even without a dedicated Live workflow, Analyze can produce rapid tactical advice when the user signals urgency |
| Sparring session runs too long | After 8-10 exchanges, offer to debrief or continue. Don't let sessions drag without progress. |

---

## Open Questions

- [ ] **Spar difficulty calibration:** Should sparring sessions have explicit difficulty levels (easy/medium/hard), or should Claude auto-calibrate based on user performance?
  - Fallback: Auto-calibrate (start moderate, adjust based on how well user applies techniques)
- [ ] **Dossier versioning:** If user re-analyzes the same scenario after sparring, should it update the existing dossier or create a new version?
  - Fallback: Create new version with revision notes

---

## Implementation Checklist

```
- [ ] Create plugin directory: plugins/communication-skills/.claude-plugin/plugin.json
- [ ] Create SKILL.md (~180 lines) with activation stack
- [ ] Create reference/voss-framework.md (~300 lines)
- [ ] Create reference/complement-frameworks.md (~120 lines)
- [ ] Create reference/dossier-template.md (~80 lines)
- [ ] Update project CLAUDE.md with new plugin entry
- [ ] Test: Analyze workflow produces coherent dossier for salary negotiation scenario
- [ ] Test: Spar workflow maintains character with accurate coaching annotations
- [ ] Test: Permission escalation prevents compromise-drift
- [ ] Test: Complement frameworks load on demand only when needed
- [ ] Test: Triggers correctly on all three categories (negotiate, difficult conversation, persuade)
- [ ] Test: Works on Haiku, Sonnet, Opus
```

---

*Interview conducted using Ideation workflow (Interview skill) + IdeaGeneration (BeCreative skill). Research by two parallel agents: voss-research (complementary frameworks) + vector-activation-research (activation patterns and prompt engineering).*
