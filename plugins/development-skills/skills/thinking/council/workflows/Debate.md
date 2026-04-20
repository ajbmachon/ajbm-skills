# Debate Workflow

Full structured multi-agent debate with 3 rounds and visible transcript.

## Prerequisites

- Topic or question to debate
- Optional: Custom council members (default: architect, designer, engineer, researcher)

## Execution

### Step 1: Announce the Council

Output the debate header:

```markdown
## Council Debate: [Topic]

**Council Members:** [List agents participating]
**Rounds:** 3 (Positions → Responses → Synthesis)
```

### Step 2: Round 1 — Initial Positions

Launch 4 parallel Task calls (one per council member).

**Each agent prompt includes:**
```
You are the [Agent Role] on a council. [Brief role description.]

COUNCIL DEBATE — ROUND 1: INITIAL POSITIONS

Topic: [The topic being debated]

Give your initial position on this topic from your specialized perspective.
- Speak in first person as your role
- Be specific and substantive (50-150 words)
- State your key concern, recommendation, or insight
- You'll respond to other council members in Round 2

Your perspective focuses on: [agent's domain]
```

**Agent domains:**
- **Architect**: System design, patterns, scalability, long-term architectural implications
- **Designer**: User experience, accessibility, user needs, interface implications
- **Engineer**: Implementation reality, tech debt, maintenance burden, practical constraints
- **Researcher**: Data, precedent, external examples, what others have done

**Output each response as it completes:**
```markdown
### Round 1: Initial Positions

**Architect:**
[Response]

**Designer:**
[Response]

**Engineer:**
[Response]

**Researcher:**
[Response]
```

### Step 3: Round 2 — Responses & Challenges

Launch 4 parallel Task calls with Round 1 transcript included.

**Each agent prompt includes:**
```
You are the [Agent Role].

COUNCIL DEBATE — ROUND 2: RESPONSES & CHALLENGES

Topic: [The topic being debated]

Here's what the council said in Round 1:
[Full Round 1 transcript]

Now respond to the other council members:
- Reference specific points they made ("I disagree with [Role]'s point about X...")
- Challenge assumptions or add nuance
- Build on points you agree with
- Maintain your specialized perspective
- 50-150 words

The value is in genuine intellectual friction — engage with their actual arguments.
```

**Output:**
```markdown
### Round 2: Responses & Challenges

**Architect:**
[Response referencing others' points]

**Designer:**
[Response referencing others' points]

**Engineer:**
[Response referencing others' points]

**Researcher:**
[Response referencing others' points]
```

### Step 4: Round 3 — Synthesis

Launch 4 parallel Task calls with Round 1 + Round 2 transcripts.

**Each agent prompt includes:**
```
You are the [Agent Role].

COUNCIL DEBATE — ROUND 3: SYNTHESIS

Topic: [The topic being debated]

Full debate transcript so far:
[Round 1 + Round 2 transcripts]

Final synthesis from your perspective:
- Where does the council agree?
- Where do you still disagree with others?
- What's your final recommendation given the full discussion?
- 50-150 words

Be honest about remaining disagreements — forced consensus is worse than acknowledged tension.
```

**Output:**
```markdown
### Round 3: Synthesis

**Architect:**
[Final synthesis]

**Designer:**
[Final synthesis]

**Engineer:**
[Final synthesis]

**Researcher:**
[Final synthesis]
```

### Step 5: Council Synthesis

After all rounds complete, synthesize the debate:

```markdown
### Council Synthesis

**Areas of Convergence:**
- [Points where 3+ agents agreed]
- [Shared concerns or recommendations]

**Remaining Disagreements:**
- [Points still contested between agents]
- [Trade-offs that couldn't be resolved]

**Recommended Path:**
[Based on convergence and weight of arguments, the recommended approach is...]
```

## Custom Council Members

If user specifies custom members, adjust accordingly:

- "Council with security" → Add security/pentester agent
- "Council with fresh eyes" → Add outside-perspective agent
- "Council with writer" → Add communication-focused agent
- Omit agents: "Just architect and engineer" → Only those two

## Timing

- Round 1: ~10-20 seconds (parallel)
- Round 2: ~10-20 seconds (parallel)
- Round 3: ~10-20 seconds (parallel)
- Synthesis: ~5 seconds

**Total: 30-90 seconds for full debate**

## Done

Debate complete. The transcript shows the full intellectual journey from initial positions through challenges to synthesis.
