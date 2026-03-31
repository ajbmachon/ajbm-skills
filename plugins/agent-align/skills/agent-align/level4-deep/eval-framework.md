# Eval Framework

Metrics, test cases, and grading rubrics for evaluating AI-to-AI interview quality.

---

## Core Question

Given the same starting point as a human-AI interview, does the AI-to-AI interview produce a similarly comprehensive spec? The eval compares decision surface area coverage, not decision correctness.

---

## Quantitative Metrics

| Metric | How to Measure | Target | Why |
|---|---|---|---|
| **Decision Coverage** | Decisions surfaced by A2A / decisions in human interview ground truth | >70% | Proves the interview surfaces comparable decision surface area |
| **Non-Obviousness Rate** | Decisions NOT in the original spec / total decisions surfaced | >15% | Per synthesis: 15.2% of human interview decisions were "new decisions." A2A should match or exceed. |
| **Completeness** | Decisions with DECIDED or DEFERRED status / total decisions | 100% | Every surfaced decision must have an explicit disposition |
| **Constraint Coverage** | Constraints referenced in at least one recommendation / total constraints | 100% | No orphan constraints — every constraint must influence a decision |
| **Structure Quality** | Working log has all required sections (constraint registry, decisions, assumptions, Q&A, research, phases) | Pass/Fail | Structural completeness of the output artifact |
| **DEFERRED Rate** | DEFERRED decisions / total decisions | <30% | Too many deferrals means the Decision Policy is inadequate |
| **Round Efficiency** | Total decisions / rounds completed | >3 decisions/round | Interviews should be productive, not padding |

---

## Qualitative Metrics (LLM-as-Judge or Human Review)

| Metric | Assessment Question | Judge |
|---|---|---|
| **Cold-Read Test** | Could a fresh Claude implement from the output spec without asking questions? | LLM-as-judge: give spec to fresh instance, count questions it would need to ask |
| **Decision Rationale Quality** | Are the reasons for each decision traceable and defensible? | Human review: sample 5 decisions, rate rationale 1-5 |
| **DEFERRED Accuracy** | Did the DEFERRED items genuinely need human input? | Human review: rate each DEFERRED as "correctly deferred" or "could have been decided" |
| **Fidelity Stack Discovery** | Did the interview surface an implicit value hierarchy? | LLM-as-judge: does the output contain a fidelity policy or value ordering? |
| **Spec Quality Assessment** | Does the output distinguish well-justified vs weakly-justified decisions? | Structural check: is the Spec Quality Report section populated? |

---

## Test Cases

### Test Case 1: Paper Planner App (Gold Standard)

**Starting point:** 84-decision spec at `company/initiatives/IN-2602-2_run-experiments/EXP-2602-2_atomic-decisions/phase-6_validation-test/6a_decision-tree-1990.md`

**Ground truth:** 33 human decisions in `phase-6_validation-test/interview-log-paper-planner-app.md`, plus full synthesis analysis at `phase-6_validation-test/analysis/00_synthesis-interview-as-spec-refinement.md`

**Why best:** Most analyzed — has decision type breakdown (adaptation 51.5%, ambiguity resolution 15.2%, new decisions 15.2%), testability metrics, AI-derivability classification, 8-lens iterative depth analysis.

**Decision Policy for test:** Product (faithful digital replica), fidelity hierarchy: Visual fidelity > Interaction ritual > Input pragmatism > Simplicity > Performance.

**Success criteria:**
- Decision coverage: surface at least 23 of 33 human decisions (>70%)
- Non-obvious: at least 5 decisions not in the original 84-decision spec
- Novel: at least 1 decision not found in EITHER the original spec or the human interview

### Test Case 2: Fabric v0.1 Spec Review

**Starting point:** Orchestrator spec + briefs (referenced in `.ai/interview-log-fabric-v0.1-spec-review.md`)

**Ground truth:** 33 decisions + 4 assumption corrections in the interview log

**Why useful:** Complex multi-agent system, many architectural decisions, tests DevSpec-style domain questions.

**Decision Policy for test:** Experiment (validate Fabric build process), fidelity hierarchy: Process fidelity > Correctness > Simplicity > Performance > Speed.

### Test Case 3: ACT Tracker Design

**Starting point:** ACT tracker code + playbook system context (referenced in `company/units/engineering/runtime/initiatives/2026-03-11-act-tracker-design/interview.md`)

**Ground truth:** 6 major assumption corrections in the interview

**Why useful:** Tests assumption surfacing depth. The human interview caught fundamental misunderstandings (playbooks as process vs role definitions). Can the A2A interview catch similar conceptual gaps?

### Test Case 4: Langfuse Skill

**Starting point:** Research docs + Langfuse SDK context (referenced in `.claude/plugins/marketplaces/ajbm/specs/langfuse/interview-log.md`)

**Ground truth:** 20 decisions in the interview log

**Why useful:** Tests a skill specification domain with clear Devil's Advocate challenges.

---

## Eval Execution Process

### Step 1: Extract Starting Points
For each test case, identify the exact input that was given at the START of the human interview. This is the starting point for the A2A interview.

### Step 2: Run A2A Interview
Invoke AgentAlign Deep with the starting point and appropriate Decision Policy. Let the interview run to convergence.

### Step 3: Compare Decision Lists
Align A2A decisions against human interview decisions:
- **Matched:** Both found the same decision (may differ in choice)
- **A2A-only:** A2A found decisions the human interview missed
- **Human-only:** Human interview found decisions A2A missed (false negatives)

### Step 4: Measure Metrics
Calculate all quantitative metrics from the comparison.

### Step 5: Qualitative Review
Run LLM-as-judge for Cold-Read Test and Fidelity Stack Discovery. Human reviews a sample of DEFERRED items.

### Step 6: Iterate
Based on gaps:
- Low decision coverage → strengthen Interviewer's question angles
- High DEFERRED rate → strengthen Decision Policy defaults
- Missing assumption corrections → strengthen Stakeholder's AUDIT protocol
- Poor structure → strengthen Working Log enforcement

---

## Grading Rubric

| Grade | Decision Coverage | Non-Obvious | Completeness | Structure |
|---|---|---|---|---|
| **A** | >85% | >20% | 100% | Pass |
| **B** | >70% | >15% | 100% | Pass |
| **C** | >55% | >10% | >90% | Pass |
| **D** | >40% | >5% | >80% | Partial |
| **F** | <40% | <5% | <80% | Fail |

Target for v1: Grade B across all test cases.
