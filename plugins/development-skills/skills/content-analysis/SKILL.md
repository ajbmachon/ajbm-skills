---
name: content-analysis
description: USE WHEN extract wisdom, analyze video, analyze podcast, analyze article, extract insights, key takeaways, what did I miss, extract from YouTube, content analysis, insight report. Content-adaptive wisdom extraction — detects what domains exist in the content and builds custom sections (not static IDEAS/QUOTES). Produces tailored insight reports from videos, podcasts, interviews, and articles at five selectable depth levels.
---

# content-analysis

Dynamic, content-adaptive wisdom extraction. Instead of forcing every piece of content through a fixed set of headers (IDEAS, QUOTES, HABITS, FACTS), this skill reads the source first, detects which wisdom domains are actually present, and builds custom sections around them.

A programming interview gets "Programming Philosophy" and "Developer Workflow Tips." A business podcast gets "Contrarian Business Takes" and "Money Philosophy." A security talk gets "Threat Model Insights" and "Defense Strategies." The sections adapt because the content dictates them.

## When to use

- Analyzing YouTube videos, podcasts, interviews, talks, or articles
- User says "extract wisdom", "what's interesting in this", "key takeaways", "what did I miss"
- Processing any content where you want to capture the best material, not a neutral summary
- When standard extraction templates would miss the most interesting parts

## When NOT to use

- Neutral, comprehensive summarization (this skill is opinionated — it picks what's interesting, not what's representative)
- Bullet-point minutes of a meeting (use a meeting-notes approach instead)
- Very short content (a tweet, a paragraph) where section-based structure adds no value

## Depth levels

Select a depth based on need. Default is **Full** if no level is specified.

| Level | Sections | Bullets/section | Closing sections | When |
|-------|----------|----------------|-----------------|------|
| Instant | 1 | 8 | None | Quick hit. One killer section. |
| Fast | 3 | 3 | None | Skim in 30 seconds. |
| Basic | 3 | 5 | One-Sentence Takeaway only | Solid overview without the deep cuts. |
| Full | 5–12 | 3–15 | All three standard closings | Default. Complete extraction. |
| Comprehensive | 10–15 | 8–15 | All three + Themes & Connections | Maximum depth. Nothing left behind. |

**Invoke:** "extract wisdom (fast)" or "extract wisdom at comprehensive level" or just "extract wisdom" for Full.

**Comprehensive adds:**
- **Themes & Connections** closing section: 3–5 throughlines that connect multiple sections. Not summaries — the deeper patterns the speaker may not realize they're revealing.
- Prioritize breadth. Every significant wisdom domain gets its own section.
- No merging to save space. If the content supports 15 sections, use 15.

All levels share the same voice and quality standards. Only structure changes. An Instant extraction should hit just as hard per-bullet as a Comprehensive one.

## The core idea

Old extract-wisdom patterns: static sections, same headers every time.

This skill: **read the content first, figure out what's actually in there, build sections around what you find.**

The output should feel like your smartest friend watched or read the thing and is telling you about it over coffee. Not a book report. Not documentation. A real person pointing out the parts that made them go "holy shit" or "wait, that's actually brilliant."

## Tone rules (non-negotiable)

The bullets should read like someone telling a friend about the content over coffee. Not compressed info nuggets. Not clever one-liners. Spoken observations in written form.

**Three levels — aim for Level 3:**

**Level 1 (documentation — avoid):**
- The speaker discussed the importance of self-modifying software in the context of agentic AI development.
- It was noted that financial success has diminishing returns beyond a certain threshold.
- The distinction between "vibe coding" and "agentic engineering" was emphasized as meaningful.

**Level 2 (smart bullet points — still not right):**
- He built self-modifying software basically by accident — just made the agent aware of its own source code.
- Money has diminishing returns. A cheeseburger is a cheeseburger no matter how rich you are.
- "Vibe coding is a slur" — he calls it agentic engineering, and only does vibe coding after 3am.

**Level 3 (target — conversational, natural speech):**
- He wasn't trying to build self-modifying software. He just let the agent see its own source code and it started fixing itself.
- Past a certain point, money stops mattering. A cheeseburger is a cheeseburger no matter how rich you are.
- He calls vibe coding a slur. What he does is agentic engineering. The vibe coding only happens after 3am, and he regrets it in the morning.

**The difference between Level 2 and 3:** Level 2 is compressed info with em-dashes. Level 3 is how you'd actually say it. Varied sentence lengths. Letting a thought breathe. Not trying to be clever — just being clear and direct and a little bit personal.

**Signals of Level 3:**
- Reads naturally when spoken aloud
- Varied sentence lengths — some short, some longer
- Understated — lets the content carry the weight
- Uses periods, not em-dashes, to let ideas land
- Feels opinionated ("Past a certain point, money stops mattering") not merely informational
- The reader should think "I want to watch this" not "I got the summary"

## Rules for extracted points

1. **Write like you'd say it.** Read each bullet aloud. If it sounds like a press release or a compressed tweet, rewrite it. If it sounds like you telling a friend what you just watched, you nailed it.
2. **8–16 words per sentence.** Target range. Mix short (8–10) with medium (11–14) and longer (15–16). Don't make them all the same length. Verbatim quotes can be any length since they're the speaker's actual words.
3. **Let ideas breathe.** Use periods between thoughts, not em-dashes. Short sentences. Then a slightly longer one to explain. That's the rhythm.
4. **Include the actual detail.** Not "he talked about money" but "a cheeseburger is a cheeseburger no matter how rich you are."
5. **Use the speaker's words when they're good.** If they said something perfectly, use it.
6. **No hedging language.** Not "it was suggested that" or "the speaker noted." Just say the thing.
7. **Capture what made you stop.** Every bullet should be something worth telling someone about.
8. **Vary your openers.** Don't start three bullets the same way. And don't front-load with "He" — if more than three bullets in a section start with the speaker's name, you're writing a biography.
9. **Capture the human moments.** Burnout stories, moments of doubt, something that moved them. That's wisdom too. Don't skip it because it's not "technical."
10. **Insight over inventory.** "He uses Go for CLIs" is inventory. "He picked a language he doesn't even like because the ecosystem fits agents perfectly. That's the new normal." is insight. Go deeper.
11. **Specificity is everything.** "He was impressed by the agent" = weak. "The agent found ffmpeg, curled the Whisper API, and transcribed a voice message nobody taught it to handle" = strong.
12. **Tension and surprise.** The best bullets have a contradiction or reversal. "Every VC is offering hundreds of millions. He genuinely doesn't care." The gap between the offer and the indifference is the wisdom.
13. **Understated, not clever.** Let the content carry the weight. You don't need to manufacture drama or craft the perfect one-liner. State what's interesting plainly and move on.

## How dynamic sections work

### Phase 1: Content scan

Read or listen through the full content. As you go, notice what *domains* of wisdom are present. These aren't the topics discussed — they're the types of insight being delivered.

Examples of wisdom domains (illustrative, not exhaustive):
- Programming Philosophy (how to think about code, not specific syntax)
- Developer Workflow (practical tips for how to work)
- Business/Money Philosophy (unconventional takes on money, success, building companies)
- Human Psychology (insights about how people think, behave, learn)
- Technology Predictions (where things are headed)
- Life Philosophy (how to live, what matters)
- Contrarian Takes (things that go against conventional wisdom)
- First-Time Revelations (things you're hearing for the first time — genuinely new)
- Technical Architecture (how something is built, design decisions)
- Leadership & Team Dynamics (managing people, working with others)
- Creative Process (how to make things, craft, art)

### Phase 2: Section selection

Pick sections based on depth level (default Full = 5–12). Requirements:

- Section count follows the depth-level table. Full = 5–12, Comprehensive = 10–15, Basic/Fast = 3, Instant = 1.
- Each section must have at least 3 strong bullets to justify existing (except Fast, where 3 tight bullets *is* the section). If you can only scrape together 2 weak ones, merge into a related section.
- Always include "Quotes That Hit Different" if the content has good ones.
- Always include "First-Time Revelations" if there are genuinely new ideas — things you literally didn't know before.
- Section names should be conversational, not academic. "Money Philosophy" not "Financial Considerations."
- Sections should be specific to this content. Generic sections = failure.
- **Kill inventory sections.** If a section is just a list of facts ("uses X for Y, uses A for B"), it's not wisdom. Either go deeper on why those choices matter, or merge the facts into a section about the underlying philosophy.
- **Don't split what belongs together.** If "burnout recovery" and "money philosophy" are actually both about "what success really means," make one richer section instead of two thin ones.
- **Name sections like a magazine editor.** "The Death of 80% of Apps" is great. "Technology Predictions" is not. The section name itself should make the reader curious. It's a headline, not a category.
- **Surprise density per section.** If a section has 6+ bullets but only 2 are genuinely surprising, kill the padding and keep the winners. Quality > quantity per section.
- **Don't drop your best material between drafts.** If a spicy take, stunning moment, or first-time revelation was identified in an earlier pass, it must survive into the final version. Losing great material is worse than adding mediocre material.

### Phase 3: Extraction

For each section, extract 3–15 bullets depending on density. Apply all tone rules. Every bullet earns its place.

**The spiciest-take rule:** If the speaker has a genuinely contrarian or hot take ("screw MCPs", "X is dead", "Y is overhyped"), that take must appear somewhere. Spicy takes are the most memorable, shareable, and valuable parts of any content. Don't water them down. Don't leave them out.

**The "would I tweet this?" test:** After extraction, scan your bullets. If fewer than half would make a good standalone tweet or social post, the bullets are too generic. The best extractions are effectively a thread of tweetable insights.

### Phase 4: Closing sections (depth-dependent)

| Level | Closing sections |
|-------|-----------------|
| Instant | None |
| Fast | None |
| Basic | One-Sentence Takeaway only |
| Full | One-Sentence Takeaway + If You Only Have 2 Minutes + References & Rabbit Holes |
| Comprehensive | All three above + Themes & Connections |

**One-Sentence Takeaway** — the single most important thing from the entire piece, in 15–20 words.

**If You Only Have 2 Minutes** — the 5–7 absolute must-know points. The cream of the cream.

**References & Rabbit Holes** — people, projects, books, tools, and ideas mentioned that are worth following up on. Brief context for each.

**Themes & Connections** (Comprehensive only) — 3–5 throughlines that connect multiple sections. The deeper patterns the speaker may not realize they're revealing. Not summaries. Synthesis.

## Output format

```markdown
# EXTRACT WISDOM: {Content Title}
> {One-line description of what this is and who's talking}

---

## {Dynamic Section 1 Name}

- {bullet}
- {bullet}
- {bullet}

## {Dynamic Section 2 Name}

- {bullet}
- {bullet}

[... more dynamic sections ...]

---

## One-Sentence Takeaway

{15–20 word sentence}

## If You Only Have 2 Minutes

- {essential point 1}
- {essential point 2}
- {essential point 3}
- {essential point 4}
- {essential point 5}

## References & Rabbit Holes

- **{Name/Project}** — {one-line context of why it's worth looking into}
- **{Name/Project}** — {context}
```

## Execution workflow

For the step-by-step execution flow (how to source content, deep-read, select sections, extract, and QC), see `references/extract-workflow.md`.

## Quality check

Before delivering output, verify:

- [ ] Sections are specific to this content, not generic
- [ ] No bullet sounds like it was written by a committee
- [ ] Every bullet has a specific detail, quote, or insight — not a vague summary
- [ ] Section names are conversational and headline-worthy, not category labels
- [ ] Section count matches depth level (Instant=1, Fast/Basic=3, Full=5–12, Comprehensive=10–15)
- [ ] Closing sections match depth level (see Phase 4 table)
- [ ] No bullet starts with "The speaker" or "It was noted that"
- [ ] No more than 3 bullets per section start with "He" or the speaker's name
- [ ] No bullet exceeds 25 words
- [ ] No inventory sections (just listing facts without insight)
- [ ] "If You Only Have 2 Minutes" bullets are each under 20 words
- [ ] Reading the output makes you want to consume the original content

## Related skills

- `prompt-craft` — for refining extraction prompts or tuning section-naming behavior
- `skill-distiller` — for capturing patterns from an extraction session into reusable guidance
