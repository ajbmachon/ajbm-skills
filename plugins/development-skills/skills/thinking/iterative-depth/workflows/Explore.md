# Explore Workflow — Iterative Depth

## Purpose

Run N structured exploration passes over the same problem, each from a different lens, to extract richer criteria than single-pass analysis produces.

## Invocation

This workflow is invoked:
1. **Directly** by the user: "use iterative depth on this problem"
2. **By the calling workflow** during its observation phase when deeper requirement extraction is needed
3. **By other thinking modes** that need enhanced requirement extraction

## Inputs

- **Problem/Request:** The original user request or problem statement
- **Context:** Any available context (conversation history, codebase state, prior work)
- **Depth:** Determined by time budget or explicit user request

## Execution

### Step 1: Determine Depth

```
Skip → return immediately, no iterative depth
<30s → N = 2 (Literal + Failure)
<2min → N = 4 (Literal + Stakeholder + Failure + Experiential)
<5min → N = 8 (All lenses)
User specifies a number → N = that number (2-8)
```

### Step 2: Load Lenses

Read `TheLenses.md` for the lens definitions being used this run.

For domain-specific tasks, the ordering may be overridden:
- Security tasks: Failure, Stakeholder, Temporal, Constraint Inversion
- UX tasks: Experiential, Stakeholder, Literal, Analogical
- Architecture tasks: Temporal, Constraint Inversion, Analogical, Meta
- Ambiguous requests: Meta, Stakeholder, Literal, Failure

### Step 3: Execute Passes

**For each lens (1 through N):**

```
┌─────────────────────────────────────────────┐
│ ITERATIVE DEPTH — Pass {i}/{N}: {LENS_NAME}                          │
│                                                                       │
│ Lens Question: "{The lens's core question}"                          │
│                                                                       │
│ Exploring from this angle...                                         │
│                                                                       │
│ Findings:                                                            │
│ - [Finding 1 — potential criterion]                                  │
│ - [Finding 2 — potential criterion]                                  │
│ - [Finding 3 — refinement of existing criterion]                     │
│                                                                       │
│ New/Refined Criteria:                                                │
│ + C{N}: [new criterion, 8-12 words, state not action]               │
│ ~ C{M}: [refined criterion, was X, now Y]                           │
│ + A{N}: [new anti-criterion]                                         │
└─────────────────────────────────────────────┘
```

**Execution modes by time budget:**

- **Short (2 lenses):** Run both lenses inline as structured thought. No agents spawned. Output directly into the calling context.

- **Medium (4 lenses):** Run lenses 1-2 inline, then spawn 2 background agents for lenses 3-4 in parallel. Merge results.

- **Long (8 lenses):** Spawn 4 pairs of background agents (or 8 individual agents) for maximum parallelization. Each agent gets:
  - The original problem/request
  - Their assigned lens definition
  - Current criteria so far (from earlier lenses)
  - Instruction: "Return 2-5 new criteria or refinements from this lens"
  - Time budget: "Complete within 30 seconds"

### Step 4: Synthesize

After all passes complete:

1. **Deduplicate:** Remove criteria that are semantically identical across lenses
2. **Merge refinements:** If multiple lenses refined the same criterion, take the most specific version
3. **Prioritize:** Order criteria by how many lenses surfaced them (consensus = high priority)
4. **Format:** Output all new/refined criteria in consistent format (8-12 words, state not action, binary testable)

### Step 5: Integrate

Return the enriched criteria to the calling context:
- If called from a planning workflow: Feed directly into criterion creation
- If called standalone: Present the enriched criteria set to the user

## Output Format

```
ITERATIVE DEPTH COMPLETE ({N} lenses applied)

Coverage:
- Lenses used: {list of lens names}
- New criteria discovered: {count}
- Existing criteria refined: {count}
- Anti-criteria discovered: {count}

NEW CRITERIA:
[List of new criteria]

REFINED CRITERIA:
[List of refinements, with evidence of what changed]

NEW ANTI-CRITERIA:
[List of what must NOT happen]

Key Insight: [The most surprising finding across all lenses — the thing single-pass analysis would have missed]
```

## Agent Prompt Template (for Long budget)

When spawning agents for individual lenses:

```
CONTEXT: You are performing Iterative Depth analysis — examining a problem from a specific structured angle to discover requirements that other angles miss.

PROBLEM: {original user request / problem statement}

YOUR LENS: {lens name} — {lens description}
YOUR QUESTION: {lens core question}

CURRENT CRITERIA (from prior lenses):
{list of criteria already discovered}

TASK: Explore this problem EXCLUSIVELY through your assigned lens. Do NOT repeat criteria already found. Find what only YOUR lens can see.

OUTPUT FORMAT:
- 2-5 new criteria (8-12 words each, state not action, binary testable)
- 0-3 refinements to existing criteria (what changed and why)
- 0-2 anti-criteria (what must NOT happen)

Time budget: Complete within 30 seconds.
```

## Integration with Planning Workflows

When a planning workflow selects iterative-depth as a capability, it runs AFTER the initial reverse engineering but BEFORE criterion creation. The flow becomes:

```
Planning:
1. Reverse Engineering (standard — what they said/implied/don't want)
2. Capability Selection (standard)
3. >>> ITERATIVE DEPTH (if selected) <<<
   - Takes Reverse Engineering output as input
   - Runs N lenses over it
   - Produces enriched requirement understanding
4. Criterion Creation (now informed by iterative depth findings)
5. Quality Gate (standard)
```

This means criteria benefit from multi-angle exploration BEFORE they're created, rather than being corrected after the fact.
