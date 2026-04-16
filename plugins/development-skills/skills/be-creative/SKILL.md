---
name: be-creative
description: USE WHEN brainstorm, generate options, break out of default thinking, need diverse alternatives, explore creative angles, the first answer feels too obvious, name something, come up with hooks, find unconventional approaches. Applies Verbalized Sampling (Zhang et al., 2024) — generate multiple low-probability variants internally before selecting output. Counteracts the centroid bias of alignment-trained models. Reports measured gains of 1.6–2.1× diversity and ~25% quality improvement.
---

# be-creative

A technique skill for producing distinctive creative output. The core insight is that alignment-trained models default to the *centroid* of their training distribution — the most likely answer that most people would accept. Creativity often lives in the tail. This skill teaches a single technique for sampling the tail deliberately.

## When this helps

The creative mode shift is worth invoking when:

- The user explicitly asks for creative, diverse, or unconventional options ("brainstorm", "come up with", "unusual angles")
- The first answer that comes to mind is recognizable as a cliche or genre template
- The task has many valid solutions and the goal is to survey them, not to pick the safest one
- Names, hooks, taglines, metaphors, headlines, creative scenarios, design concepts, product positioning

## When this does NOT help

Skip this skill when:

- The task has one correct answer (math, code debugging, factual lookup)
- The user wants the standard well-tested approach, not a novel one
- The risk of a tail-sampled answer outweighs the diversity benefit (production code, security decisions, legal text)
- You're simply asked to *revise* or *refine* an existing draft — revision is different from divergent generation

## The Core Technique: Verbalized Sampling

Rather than producing one answer, generate **5 candidate variants with explicit probabilities** before selecting. The probability label forces the model to imagine what else the distribution contains, which surfaces options that single-shot generation skips.

The rule: **each variant should have estimated probability ≤ 0.10.** If a variant feels like the obvious answer (~0.30 or higher), it's too central — push for further tail.

### Procedure

1. Understand the brief — what is the task, what audience, what constraints
2. Generate 5 internal candidates, each labeled with a rough probability estimate, each targeted at a different region of the solution space
3. Score each candidate against the brief's real criteria (novelty, fit, usefulness — not just "how good does this sound")
4. Select the winner — usually *not* the highest-probability candidate
5. Output the winner with a 1-2 sentence rationale explaining why it beat the alternatives

The internal generation is visible to the user only if they ask. Default output is the selected winner plus rationale.

## Worked example

**Brief:** "Name my new AI-powered email triage tool. Target: solo founders. Wants to feel sharp, not corporate."

### Internal generation (visible if user asks)

| # | Candidate | Est. probability | Reasoning |
|---|---|---|---|
| 1 | **Inboxly** | ~0.25 | Obvious centroid: `<action>ly` SaaS naming convention. Too safe. |
| 2 | **Hermes** | ~0.08 | Mythological messenger god. Evocative, memorable. Slightly overused in the shipping/finance space. |
| 3 | **Filter** | ~0.03 | Radical simplification — an English common noun. Strong if trademark-clearable. |
| 4 | **Clearwater** | ~0.02 | Metaphor (email → water, clarity). Unusual register for productivity tools. |
| 5 | **Noise Floor** | ~0.02 | Technical audio-engineering term. Positions the tool as removing noise, not managing messages. Strongest differentiation. |

### Selection

**Winner: Noise Floor.** Rationale: it reframes the category — instead of "email manager" (more mail) it claims "noise removal" (less of what the user hates). Matches the "sharp, not corporate" brief. Filter was close but lacks a distinctive hook. Hermes is memorable but has thematic overlap with shipping/finance brands.

## Why this works

The technique is grounded in [Zhang et al. 2024](https://arxiv.org/abs/2510.01171), which reports that explicit probability labeling during generation forces the model to consider the distribution's spread rather than collapsing to the mode. Reported effects: **1.6–2.1× diversity** and **~25% quality improvement** on creative tasks. The mechanism: alignment training pulls outputs toward the most-agreeable answer; verbalized probability acts as a counterweight that gives the model *permission* to deviate.

Generating multiple candidates also helps the model catch weak answers by contrast — a bad candidate looks worse next to a better one, so the final selection is calibrated rather than defended.

## Common failure modes

- **Pseudo-diversity:** Five candidates that are all the same idea with synonyms swapped. If candidates 1 and 4 mean the same thing, tail-sample harder.
- **Probability theater:** Writing probabilities without using them — if the highest-probability candidate always wins, the labeling added nothing. The point is to select *against* the centroid when the tail is better.
- **Ignoring the brief:** A diverse candidate list that doesn't respect constraints is not creative, it's undisciplined. Each candidate must still satisfy the task.
- **Over-applying the technique:** Not every task needs five candidates. Short scoped creative asks (one tagline for one product) benefit. Broad asks (redesign the entire brand) benefit from decomposing first.

## References

- [ResearchFoundation.md](ResearchFoundation.md) — deeper mechanism description, activation triggers, research citations
- [Examples.md](Examples.md) — additional worked examples across domains (writing, product naming, technical architecture, visual design briefs)
