# Plan: AgentAlign — AI-to-AI Elicitation Workflow for Multi-Agent Systems

## Context

The Interview skill's EpistemologicalFramework.md identifies **complementary intelligence** — bridging human depth with AI breadth — as the foundation of human-AI elicitation. But in fully autonomous multi-agent systems, agents delegate to other agents. Both parties are the same KIND of intelligence, yet they hold DIFFERENT context. The problem shifts from "how do we combine two different intelligences?" to **"how do we verify that information survives the compression of delegation?"**

Without structured alignment at delegation junctions, multi-agent systems suffer from: context compression loss (rich conversation compressed to a prompt), assumption stacking (each layer adds unchecked assumptions), constraint evaporation (human principal's constraints lost through the chain), and parallel divergence (workers building incompatible things from the same brief).

The Interview skill's four irreducible operations (Mirror → Surface → Probe → Converge) still apply, but the WHY behind each changes. This plan designs a new graduated workflow: **AgentAlign**.

---

## Part 1: Epistemological Foundation — Context Asymmetry

### The Core Shift

| Human-AI Elicitation | AI-to-AI Elicitation |
|---|---|
| Complementary intelligence (depth + breadth) | Context asymmetry (same intelligence, different information) |
| Tacit knowledge extraction | Context recovery from delegation compression |
| Intent behind intent | Principal intent preservation through chains |
| Ego-free challenge as advantage | Cross-context verification (both ego-free) |
| Externalized thinking catalyzes new insight | Information transfer, not insight generation |

### The Three Asymmetries

1. **Context asymmetry** — Agent A talked to the user for 30 min; Agent B starts fresh. Delegation compresses rich context into a prompt. Information is inevitably lost. This is analogous to tacit knowledge — the delegator "knows" things it can't fully articulate in the handoff.

2. **Role asymmetry** — Architect reasons about tradeoffs; Engineer reasons about implementation. Same information, different conclusions because they weight factors differently.

3. **Capability asymmetry** — Different tools, permissions, models, isolation modes. Delegating a task requiring capabilities the worker lacks is a silent failure mode.

### The Four Operations Adapted

| Human-AI | AI-to-AI | Purpose Shift |
|---|---|---|
| **Mirror** | **ECHO** | From "see your idea externally" → verify compression didn't lose information |
| **Surface** | **AUDIT** | From bilateral assumptions → cascade prevention + constraint inheritance |
| **Probe** | **RECOVER** | From extracting tacit knowledge → filling delegation compression gaps |
| **Converge** | **CONTRACT** | From shared understanding → binding execution agreement with testable criteria |

### What Gets Stripped (Human-Specific)

- Devil's Advocate / Challenge — task validity settled by human
- Epistemological labels ([E], [L], [S], [C]) — both reason the same way
- Working log — handoff spec replaces it for Full level
- Showpiece questions — no visual UI between agents
- Research phases — worker reads files directly
- Progressive logging — no memory drift within short exchanges

### What's New (AI-to-AI Specific)

- **Constraint inheritance verification** — explicit chain-of-custody for principal's constraints
- **Capability audit** — worker declares tools/permissions; delegator confirms sufficiency
- **Compression loss detection** — systematic check for information lost in handoff
- **Token budget awareness** — convergence pressure higher than human-AI

---

## Part 2: AgentAlign Workflow Design — Three Graduated Levels

### Level Selection (Boundary Tests)

| Level | When | Boundary Test | Max Rounds | Token Cost |
|---|---|---|---|---|
| **Inline** | Simple, well-specified tasks | Could worker proceed after just reading the delegation prompt? | 0 (echo only) | ~50-80 tokens |
| **Quick** | Moderate tasks with a few ambiguities | Can alignment be achieved in one back-and-forth? | 2 | ~200-400 tokens |
| **Full** | Complex tasks, multi-layer chains, architecture decisions | Does this need iterative refinement of scope, approach, or constraints? | 4 | ~500-1000 tokens |

**Mapping to delegation TIMING SCOPE:**
- `fast` → Inline (default)
- `standard` → Quick (default), Full if ambiguous
- `deep` → Full (default), Quick if clear
- Leader can override explicitly

---

### Level 1: INLINE (Behavioral Norm)

Not a workflow invocation — a behavioral disposition for every worker agent.

**Format (embedded in worker's first output):**
```
## Understanding
Task: [one-sentence restatement]
Success: [restatement of success criteria]
Constraints inherited: [H1, S1, etc. or "none specified"]
Approach: [brief statement of how worker will proceed]
```

**Convergence:** Implicit. Delegator reads echo; if correct, no response needed. If wrong, one correction message.

---

### Level 2: QUICK (1 Round of SendMessage)

**Phase structure (two messages total):**

**Message 1 — Worker to Leader:**
```
## ECHO
Task: [restatement in worker's own words]
Intent: [why this matters]
Success: [what "done" looks like]

## AUDIT
Constraints inherited: [list with IDs]
My assumptions: [things not specified, worker filling in]
Capability check: [tools available / gaps identified]

## RECOVER
Questions (answer changes my approach):
1. [specific question about gap]
2. [specific question about ambiguity]
```

**Message 2 — Leader to Worker:**
```
## Corrections
[corrections to ECHO, or "none"]

## Answers
1. [answer]
2. [answer]

## Additional constraints
[any forgotten constraints, or "none"]

## CONTRACT: Confirmed
```

Worker proceeds after receiving Message 2. If leader's response reveals NEW ambiguity, one follow-up round allowed (Quick-Extended), then proceed regardless.

**Question rules (from QuestionGuidelines.md, adapted):**
- Max 5 questions (hard cap)
- Each must earn its place — would a different answer change the implementation?
- No questions answerable by re-reading the delegation prompt

---

### Level 3: FULL (Multi-Round with Handoff Spec)

**Phase 1: ECHO + AUDIT (Worker → Leader)**

Comprehensive understanding + constraint inheritance + capability check.

```
## ECHO
Task: [detailed restatement]
Intent: [business context]
Success criteria: [enumerated, testable]
Scope: In: [list] | Out: [list]

## AUDIT
### Constraints inherited
| ID | Constraint | Source | My interpretation |
|----|-----------|--------|-------------------|
| H1 | [text] | [human principal / leader] | [how I'll honor this] |

### My assumptions (not specified)
- [assumption 1] — proceeding with this unless corrected
- [assumption 2] — proceeding with this unless corrected

### Capability check
- Tools: [available / missing]
- Model: [what I'm running on]
- Permissions: [file write, bash, etc.]

### Potential conflicts
- [constraint X might conflict with approach Y]
```

**Phase 2: RECOVER (Max 2 rounds)**

Questions organized by what they unlock:
```
## RECOVER — Round 1

### [Architecture decision name]
1. [question] — determines approach A or B
2. [question] — clarifies scope

### [Implementation detail name]
3. [question] — affects file structure
```

Leader answers + corrections. Hard cap: 2 RECOVER rounds. If not aligned after 2, task needs human-AI interview first — too ambiguous for agent delegation.

**Phase 3: CONTRACT (Handoff Spec Document)**

Worker produces shared document at `.claude/handoffs/{task-name}.md`:

```markdown
# Handoff Spec: [Task Name]

**Leader:** [agent name] | **Worker:** [agent name]
**Status:** CONFIRMED | IN PROGRESS | COMPLETE

## Task
[what will be done]

## Intent
[business context from human principal]

## Success Criteria
- [ ] [testable criterion 1]
- [ ] [testable criterion 2]

## Constraint Registry (Inherited Chain)

### From Human Principal
| ID | Constraint | Type | How Honored |
|----|-----------|------|-------------|
| H1 | [text] | Hard | [approach] |

### From Leader
| ID | Constraint | Type | How Honored |
|----|-----------|------|-------------|
| L1 | [text] | Soft | [approach] |

## Scope
In: [enumerated] | Out: [enumerated]

## Approach
[architecture, file changes, testing strategy]

## Assumptions Confirmed
- [confirmed in Round N]

## Decisions Made
| Decision | Alternatives | Chosen | Rationale |
|----------|-------------|--------|-----------|
```

Leader confirms: `CONTRACT: CONFIRMED` or `CONTRACT: REVISED — [changes]` (one revision round max).

---

## Part 3: Constraint Inheritance Protocol (Multi-Layer Chains)

**Rule:** Constraints are PASSED DOWN, never invented. Workers cannot create Hard Constraints the human didn't establish. Workers can add Soft Constraints consistent with inherited Hard Constraints.

**Chain format:**
```
### Layer 0: Human Principal
| ID | Constraint | Type |
| H1 | Must work offline | Hard |

### Layer 1: Leader → Architect
| H1 | Must work offline | Hard | Inherited from Human (H1) |
| L1 | Event-driven architecture | Soft | Leader decision (consistent with H1) |

### Layer 2: Architect → Engineer
| H1 | Must work offline | Hard | Inherited from Human (H1) |
| L1 | Event-driven architecture | Soft | Inherited from Leader (L1) |
| A1 | Service worker for offline sync | Soft | Architect decision (implements H1) |
```

**Verification at each layer:**
1. Worker lists ALL inherited constraints (no evaporation)
2. Worker states how each is honored (no drift)
3. If approach would violate a constraint, STOP and surface

---

## Part 4: Anti-Patterns

| Anti-Pattern | What It Looks Like | Fix |
|---|---|---|
| **Bureaucracy Trap** | 10 questions for a 3-file change | Questions proportional to blast radius |
| **Echo Theater** | Verbatim copy of delegation prompt | Echo must restate in worker's own words |
| **Constraint Inflation** | Worker invents Hard Constraints | Only human principal establishes Hard Constraints |
| **Assumption Hiding** | Worker proceeds without listing assumptions | AUDIT requires explicit enumeration |
| **Round Padding** | Questions answerable from delegation prompt | Same "earn its place" rule as QuestionGuidelines |
| **Chain Amnesia** | Middle agent drops principal's constraints | Constraint Chain Protocol at every layer |

---

## Part 5: Implementation Plan

### Files to Create

1. **`plugins/interview/skills/Interview/Workflows/AgentAlign.md`** (~250-300 lines)
   - Self-contained workflow with all three levels
   - Includes format templates, constraint inheritance protocol, convergence signals, anti-patterns
   - No additional reference files needed — simpler than human-AI workflows

### Files to Modify

2. **`plugins/interview/skills/Interview/SKILL.md`**
   - Add routing table entry: `AgentAlign | "agent alignment", "delegation alignment", multi-agent delegation | Workflows/AgentAlign.md`
   - Add note in Workflow Routing explaining AgentAlign is the only AI-to-AI workflow
   - Verify line count stays under 500

3. **`plugins/interview/skills/Interview/EpistemologicalFramework.md`**
   - Add new section: "AI-to-AI Elicitation: Context Asymmetry"
   - Contrast with human-AI complementary intelligence model
   - Document the three asymmetries and four adapted operations

4. **`plugins/interview/.claude-plugin/plugin.json`**
   - Add "agent-align" to keywords
   - Update description to mention 8 workflows

5. **`CLAUDE.md` (root)**
   - Add AgentAlign to Interview Plugin section
   - Brief description of when it triggers and what it does

### Implementation Order

1. Update `EpistemologicalFramework.md` — foundation first
2. Create `Workflows/AgentAlign.md` — the core deliverable
3. Update `SKILL.md` — routing + AI-to-AI note
4. Update `plugin.json` — metadata
5. Update root `CLAUDE.md` — documentation

---

## Part 6: Verification

1. **Self-containment test:** Can a Leader agent read this workflow and know exactly how to delegate at each level?
2. **Worker test:** Can a Worker agent read this and know exactly how to respond at each level?
3. **Constraint chain test:** In a 3-layer chain (Leader → Architect → Engineer), do constraints propagate correctly?
4. **Line count:** SKILL.md stays under 500 lines
5. **Routing:** AgentAlign triggers on correct keywords
6. **Token efficiency:** Quick level stays under 400 tokens total; Full under 1000
