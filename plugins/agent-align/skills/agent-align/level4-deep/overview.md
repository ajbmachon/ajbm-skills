# Level 4: Deep — AI-to-AI Interview for Spec Refinement

Extended elicitation where two AI agents interview each other to produce comprehensive, decision-rich specifications from rough mandates or specs.

---

## When to Use Deep

- A spec or mandate exists but needs exhaustive decision coverage
- Non-obvious questions need surfacing before implementation
- The starting point is good but has implicit assumptions and ambiguities
- You need a structured decision list with explicit choices for every fork

**Not for:** Quick delegation alignment (use Levels 1-3), human-AI elicitation (use Interview skill), pure challenge without spec output (use DevilsAdvocate).

---

## Shared Infrastructure

Deep level reuses battle-tested infrastructure from the Interview skill. These files define mechanics that work identically in AI-to-AI:

| File | Purpose | Where |
|---|---|---|
| **ConstraintStore** | Hard/Soft/Boundary constraint capture + enforcement | Interview skill's `ConstraintStore.md` |
| **AssumptionAudit** | Two-layer assumption surfacing (Interviewer's + Stakeholder's) | Interview skill's `AssumptionAudit.md` |
| **VerificationGate** | Self-check before Tier 1 decisions | Interview skill's `VerificationGate.md` |
| **QuestionGuidelines** | Question design standards (Standard + Showpiece modes) | Interview skill's `QuestionGuidelines.md` |
| **WorkingLogTemplate** | Progressive file-based memory | Interview skill's `WorkingLogTemplate.md` |
| **OutputTemplatesCore** | Spec output format | Interview skill's `OutputTemplatesCore.md` |

**Adaptations from Interview skill for A2A:**
- All `AskUserQuestion` calls → `SendMessage` between agents
- Menu Mode → removed entirely (AIs don't fatigue — ask everything)
- "User confirms" → Stakeholder confirms via SendMessage
- Both agents run VerificationGate (not just Interviewer)

---

## Constraint System: Merged Model

Combines Interview's rich types with AgentAlign's provenance tracking.

**Types:** Hard / Soft / Boundary (from Interview's ConstraintStore)

**Source Provenance:** Each constraint tracks where it came from:
- Human Principal (highest authority)
- Spec/Mandate (logically entailed from the task)
- Decision Policy (defaults and preferences)
- Agent-Inferred (derived during interview)

**Key rule:** Constraint TYPE is determined by logical necessity, NOT by source. "Make a React app" in the mandate → Hard constraint on JS/React/compatible webstack, even though no human explicitly said "must use JavaScript." If violating it means not doing the task, it's Hard.

**From AgentAlign:** Types cannot be downgraded through delegation chains. Mutations require explicit acknowledgment.

---

## Phase Structure

| Phase | What Happens | Who Leads |
|---|---|---|
| **0: ECHO + AUDIT** | Stakeholder echoes spec understanding, derives initial constraints, surfaces interpretation assumptions | Stakeholder |
| **1: Research** | Interviewer conducts blocking research on codebase, tech, domain | Interviewer |
| **2: Challenge** | Interviewer challenges spec quality. Stakeholder defends by citing spec evidence. Reveals well-justified vs weakly-justified decisions. | Interviewer |
| **T: Constraint Capture** | Extract constraints from challenge phase. Merged types + provenance. Stakeholder confirms. | Interviewer captures, Stakeholder confirms |
| **3: Deep Interview** | Many rounds of structured questions via SendMessage. No Menu Mode — ask everything. Tradeoff analysis for every fork. | Interviewer asks, Stakeholder answers |
| **4: Contradiction** | Surface conflicts between research and claims. Stop and require resolution. | Interviewer |
| **5: Verification** | Stakeholder confirms alignment. Orchestrator runs independent gap check. | Orchestrator |
| **6: CONTRACT + Output** | Compile spec from working log. CONTRACT as agreement frame. Human Review Doc with DEFERRED items. | Orchestrator |

---

## Orchestrator Procedure

The invoking agent (session agent / team lead) runs the Deep level:

### 1. Initialize
- Create the Working Log file (use WorkingLogTemplate from Interview skill)
- Read the input spec/mandate
- Read the DecisionPolicy (if provided; use defaults if not)

### 2. Spawn Team

This workflow requires two separate agent contexts — not one agent role-switching. The Interviewer is briefed only with the spec and challenge targets; the Stakeholder is briefed only with the spec, decision policy, and meta-goals. Separating the constraint bases is the anti-sycophancy mechanism: each agent reasons from its own grounding, so the challenge is genuine rather than a single context arguing with itself. A single-context implementation invites drift and confirmation bias — the same reasoning chain cannot meaningfully challenge the decisions it just produced, and role labels erode within one context window.

- Create team with `TeamCreate`
- Spawn **Interviewer** agent with: spec path, working log path, Interview skill file paths
- Spawn **Stakeholder** agent with: spec path, decision policy path, meta-goals

### 3. Phase 0: Stakeholder ECHO + AUDIT
- Stakeholder sends initial ECHO of spec understanding to Interviewer
- Interviewer reviews, corrects interpretation gaps
- Working log updated with initial constraints

### 4. Phase 1-2: Interviewer Research + Challenge
- Interviewer conducts blocking research
- Interviewer challenges spec via SendMessage to Stakeholder
- Stakeholder defends with spec citations
- Working log updated with research findings and challenge exchanges

### 5. Transition: Constraint Capture
- Interviewer extracts constraint registry
- Sends to Stakeholder for confirmation
- Working log updated with confirmed registry

### 6. Phase 3: Deep Interview Rounds
- Interviewer sends structured questions (2-4 per round)
- Stakeholder answers with confidence levels
- Interviewer writes to working log after each exchange
- Orchestrator monitors convergence (see ConvergenceProtocol)

### 7. Phase 4-5: Contradiction + Verification
- Surface and resolve contradictions
- Run verification loop against constraint registry
- Orchestrator runs independent gap check

### 8. Phase 6: CONTRACT + Output
- Compile spec from working log
- Produce: refined spec + interview log + Human Review Document
- Human Review Doc lists all `DEFERRED [HUMAN]` items for override

---

## Output Artifacts

| Artifact | Content | Purpose |
|---|---|---|
| **Working Log** (interview-log-{topic}.md) | Full Q&A record, constraint registry, decisions, assumptions, research | Primary artifact — captures reasoning, not just conclusions |
| **Refined Spec** (spec-{topic}.md) | Implementation-ready spec compiled from working log | Derived artifact — what to build |
| **Human Review Document** | All DEFERRED items with recommendations | Human override points |

---

## Behavioral Norms

### Anti-Sycophancy in A2A
The biggest risk in AI-to-AI is premature agreement. Mitigations:
- Interviewer's Phase 2 brief MANDATES adversarial challenge
- Stakeholder's brief MANDATES vigorous defense (cite spec evidence, don't concede easily)
- Convergence requires minimum 3 rounds regardless of agreement

### Progressive Logging Is Mandatory
Even more critical than in human-AI: there's no human memory as backup. The working log prevents drift across many rounds. Write AFTER EVERY EXCHANGE.

### Both Agents Run Verification Gates
Not just the Interviewer — the Stakeholder must also check its decisions against the constraint registry before answering. This prevents "standard pattern trap" on both sides.
