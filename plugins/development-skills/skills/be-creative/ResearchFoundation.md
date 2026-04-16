# Research Foundation: Verbalized Sampling

Deeper background on the Verbalized Sampling technique referenced in SKILL.md. Read this when you want to understand *why* VS works, what its measured effects are, and when it might not transfer to your specific creative task.

---

## The Research

**Primary source:** Zhang et al., *Verbalized Sampling: Rescuing Diverse Generation in Aligned LLMs*, 2024 — [arXiv:2510.01171](https://arxiv.org/abs/2510.01171).

### What they found

Alignment training (RLHF, DPO, constitutional methods) systematically narrows output diversity. Models learn to produce answers that human raters approve of, and the most-approvable answer is often the *safest centroid* — the generic response that few people actively dislike but few find distinctive.

Zhang et al. showed this diversity loss is recoverable at inference time by asking the model to **explicitly verbalize probabilities** over multiple candidate responses before committing. The act of naming probabilities forces the model to imagine the distribution, which surfaces tail candidates that greedy decoding misses.

### Measured effects

- **1.6–2.1× diversity** on creative generation benchmarks (poetry, story continuations, naming tasks) measured via n-gram distinct-n and semantic spread
- **~25.7% quality improvement** on human-rated creative tasks — counterintuitive but consistent: selecting from a broader candidate set lets the model pick genuinely better answers instead of defaulting to the most-approvable one
- Effect compounds with model capability — larger/more capable models benefit more from VS because they have a wider latent distribution to sample from

### The mechanism

Alignment pushes output probability mass toward a small region around the training-approved centroid. Standard sampling (temperature, top-p, top-k) can't recover diversity without also adding noise — you get either safe-and-similar outputs or diverse-and-incoherent ones.

Verbalized Sampling is different because it operates at the **prompt level, not the decoding level.** By asking the model to *name* five candidates with probabilities, you're asking it to represent the distribution in its output tokens. The model has to enumerate tail options to fill the list, which surfaces them as candidates even when greedy decoding would have collapsed to the centroid.

The `p ≤ 0.10` threshold is the practical lever: it tells the model "don't just give me the centroid five times with trivial variations — go far enough into the tail that each candidate has ≤10% odds of being the modal first thought."

---

## When the technique transfers

Strong transfer:
- Naming, tagline, hook, headline generation (small search space, centroid is recognizable)
- Creative writing premises, story seeds, metaphor discovery
- Product positioning, brand concept exploration
- Visual design concepts (when describing to an image model)
- Architectural/technical decisions where multiple defensible approaches exist

Weaker transfer:
- Factual QA (there's a correct answer; diversity is noise)
- Code generation for well-defined specs (ditto)
- Summarization (centroid is often the right answer)
- Step-by-step reasoning (CoT is a different pattern; don't confuse them)

---

## Activation signals

The skill is worth invoking when the user's request contains any of these clusters:

**Explicit creative asks:**
- "be creative", "think creatively", "come up with creative..."
- "diverse options", "different angles", "varied approaches"
- "unconventional", "out of the box", "not obvious"
- "brainstorm", "surface options", "explore alternatives"

**Implicit creative asks:**
- "name this...", "what should I call...", "give me a tagline"
- "write a hook for...", "headline options for..."
- "help me position this..."
- "pitch ideas for..."

**Anti-signals (skip the skill):**
- "what's the best way to..." (usually wants the centroid)
- "fix this bug", "debug this" (not a creative task)
- "summarize...", "extract...", "classify..." (compressive, not divergent)
- "revise this draft" (refinement, not divergence — the draft is already committed)

---

## Related techniques

- **Tree-of-Thoughts:** branches on reasoning, not on content variants. Complementary to VS for multi-step creative tasks, but different primitive.
- **Self-Consistency:** multiple samples then majority vote. Opposite goal — consistency vs. diversity. Don't mix.
- **Tail sampling (top-p with high p):** decoding-level diversity. Works, but can't hit the same tail regions that VS can because top-p still filters by probability not by semantic region.
- **Ideation interview workflow (see `interview` skill):** When the creative task is large (whole product, whole story), use the interview skill's Ideation workflow which chains divergent (VS-style) and convergent phases.
