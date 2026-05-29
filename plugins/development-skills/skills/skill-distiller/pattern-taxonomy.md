# Pattern Taxonomy

Four categories for extracting user guidance patterns from conversations. Each captures a different facet of expert judgment.

---

## 1. Corrections

**What it captures:** Moments where the user redirected Claude's approach — explicit disagreements, course corrections, "no, do it this way" moments.

**Extraction signals:**
- Keywords: "no", "actually", "instead", "not like that", "wrong", "that's not what I meant"
- Explicit disagreement with Claude's output or approach
- User providing a different solution after Claude attempted one
- "Don't" / "stop" / "wait" interruptions

**Skill output section:** Anti-Patterns

**Generalization guidance:**
- Anti-patterns often stay **specific** — the concrete example is more useful than a vague generalization
- Pattern: "DON'T default to X when Y" with the specific example
- Only generalize when the same correction appears across multiple contexts

**Example extraction:**

| Source Moment | Proposed Generalization |
|--------------|------------------------|
| "No, don't just catch all exceptions. Let unexpected ones propagate." | "At error boundaries, distinguish between expected and unexpected failures. Handle expected; propagate unexpected." |

---

## 2. Questions & Probes

**What it captures:** Questions the user asked that Claude should have asked itself — probing questions that surface non-obvious considerations.

**Extraction signals:**
- User questions that reveal blind spots in Claude's analysis
- "What about...?" / "Did you consider...?" / "Have you thought about...?"
- Questions that change the direction of work
- Questions that surface edge cases or requirements Claude missed

**Skill output section:** Attention Cues (within Behavioral Dispositions)

**Generalization guidance:**
- Generalize to the **type of question**, not the specific question
- Pattern: "When [context], ask yourself: [generalized question]"
- The question itself is the behavioral disposition — it teaches what to notice

**Example extraction:**

| Source Moment | Proposed Generalization |
|--------------|------------------------|
| "What would a junior developer misunderstand about this API?" | "When writing developer-facing interfaces, reason about the gap between expert and novice mental models." |

---

## 3. Quality Gates

**What it captures:** Stop-and-check moments — where the user told Claude to pause and verify something before proceeding.

**Extraction signals:**
- "Wait", "before you", "first check", "hold on", "verify that"
- Blocking instructions (user preventing Claude from moving forward)
- Conditions stated before allowing an action: "Only if X, then Y"
- User requiring evidence or proof before acceptance

**Skill output section:** Quality Checkpoints (within Behavioral Dispositions)

**Generalization guidance:**
- Quality gates generalize to **checkpoint types** — when to pause
- Pattern: "Before [action type], verify [condition]"
- Group related gates: e.g., all "check before deploying" gates into a deployment checkpoint

**Example extraction:**

| Source Moment | Proposed Generalization |
|--------------|------------------------|
| "Before you refactor that, show me the test coverage first." | "Before restructuring working code, establish that test coverage captures current behavior." |

---

## 4. Analysis Modes

**What it captures:** Specific thinking strategies the user directed Claude to apply — lenses, frameworks, perspectives, comparison methods.

**Extraction signals:**
- "Look at this from the perspective of...", "Compare against..."
- "What about the [specific angle]?", "Consider the [framework/lens]"
- User switching Claude's analytical frame
- Requests for specific types of analysis (threat model, cost-benefit, user journey, etc.)

**Skill output section:** Thinking Patterns (within Behavioral Dispositions)

**Generalization guidance:**
- Analysis modes are the **most generalizable** category
- Pattern: "When [context], apply [thinking strategy/lens/framework]"
- These become the core thinking patterns of the distilled skill

**Example extraction:**

| Source Moment | Proposed Generalization |
|--------------|------------------------|
| "Now look at this from the attacker's perspective. What would they try?" | "When evaluating system design, adopt an adversarial lens: reason about how the design could be exploited or misused." |

---

## Cross-Category Patterns

Some user guidance spans multiple categories. When this happens:

- **Log it under the primary category** (strongest signal)
- **Note the cross-reference** in the pattern's source moment
- **During co-editing (Step 3)**, surface the overlap: "This pattern touches both Quality Gates and Analysis Modes. Where should it live?"

The user decides during collaborative review.

---

## Signal Strength

| Confidence | Signal Type | Example |
|-----------|------------|---------|
| **Strong** | Explicit correction with explanation | "No, do X because Y" |
| **Strong** | Repeated pattern (3+ occurrences) | Same type of question asked across different contexts |
| **Medium** | Single clear instance | One obvious quality gate moment |
| **Medium** | Implicit correction (user redoes Claude's work differently) | User rewrites Claude's code without explicit "no" |
| **Weak** | Inferred from context | Behavior change that might indicate dissatisfaction |

Present signal strength during Step 3 review so the user can prioritize.
