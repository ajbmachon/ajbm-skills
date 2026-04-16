---
name: pai-skill-transfer
description: USE WHEN transferring a PAI skill to a standard Claude Code plugin, porting skills between environments, strip PAI specifics, adapt PAI skill for marketplace, extract skill from PAI. Guides the transformation of PAI-embedded skills into standalone plugin-compatible skills — strip PAI-specific scaffolding, decouple from the PAI Algorithm and memory system, apply Anthropic skill best practices.
---

# pai-skill-transfer

PAI (Personal AI Infrastructure) ships excellent skills, but they assume the PAI runtime — a specific harness with its own memory system, Algorithm workflow, customization directory, and voice-notification hooks. When you want one of those skills to work as a standard Claude Code plugin skill (marketplace-distributable, portable across environments, usable without PAI installed), you need to transform it.

This skill describes the transformation.

## When to use

- User wants to install a PAI skill into a plugin repo (e.g., ajbm-dev, codebase-insights-skills)
- User is forking a PAI skill to publish independently
- A skill reference like `~/.claude/skills/<name>/` is being pulled into a marketplace plugin
- You see a skill with a `## Customization` block pointing to `~/.claude/PAI/USER/SKILLCUSTOMIZATIONS/…` and it needs to work for users who don't have PAI

## When NOT to use

- User is authoring a *new* PAI skill that will stay inside PAI — keep the PAI conventions
- User just wants to copy a skill file as-is (no adaptation) — this skill is about transformation, not file copying
- The skill in question is already standalone (no PAI markers) — nothing to transform

## The transformation, at a glance

PAI skills typically carry six categories of environment-specific content. Each needs a decision: **strip**, **rewrite generically**, or **keep but document the dependency**.

| PAI element | Default action | Notes |
|---|---|---|
| `## Customization` block referencing `~/.claude/PAI/USER/SKILLCUSTOMIZATIONS/` | **Strip** | Path won't exist for plugin users |
| Voice curl (`curl -s -X POST http://localhost:8888/notify …`) | **Strip** | PAI-specific notifier — not a portable dependency |
| `PAI/Algorithm/` references, phase names (OBSERVE/THINK/PLAN/BUILD/EXECUTE/VERIFY/LEARN) | **Rewrite generically** | e.g., "the calling workflow's planning phase" |
| `MEMORY/WORK/{slug}/PRD.md` | **Rewrite or strip** | Mention a working-log pattern without PAI specifics, or drop |
| ISC (Ideal State Criteria) terminology | **Rewrite generically** | "verifiable criteria", "acceptance checks" |
| `~/.claude/PAI/…` paths | **Rewrite skill-local** | Reference files inside the skill's own directory |
| `{PRINCIPAL.NAME}` or other `{PRINCIPAL.*}` template vars | **Strip or rewrite** | Replace with generic nouns ("the user", "someone") or drop the sentence |
| Canonical-doc references (`PAI/USER/WRITINGSTYLE.md`, `PAI/USER/WORLDVIEW.md`, etc.) | **Drop or inline** | If the referenced content is already present in the skill, drop the reference. If load-bearing, inline the relevant portion. |
| Parent router `SKILL.md` (just a `Route To` table pointing to child skills) | **Often collapse** | One child → flatten. Multiple children → split into separate plugin skills. |
| Hardcoded external CLI tools (`fabric -y`, specific unusual commands) | **Soften** | Rephrase as "if installed" or list alternatives; provide a fallback for users without it. |

## Transformation checklist

Apply this sequentially to each SKILL.md and every reference file in the transfer:

### Strip

- [ ] Remove the `## Customization` block if it references `SKILLCUSTOMIZATIONS` (including the header itself, not just the path)
- [ ] Remove any `curl … localhost:8888/notify` voice commands (and the prose around them)
- [ ] Remove phase-transition voice announcements ("Entering the X phase")
- [ ] Remove `PRDSync` hook references, `work.json` references
- [ ] Remove `implied_sentiment` / `algorithm-reflections.jsonl` write instructions
- [ ] Remove `{PRINCIPAL.NAME}` / `{PRINCIPAL.*}` template variables — replace with generic nouns or drop the sentence
- [ ] Remove references to canonical PAI docs (`PAI/USER/WRITINGSTYLE.md`, `PAI/USER/WORLDVIEW.md`, etc.) unless load-bearing — in which case inline the relevant portion
- [ ] Remove `(CRITICAL)` / `(REQUIRED)` / ALL-CAPS parenthetical suffixes on section headers — use softer language ("non-negotiable", "required") or drop

### Rewrite

- [ ] Replace `PAI/Algorithm/` or "the Algorithm" with "the calling workflow" or drop
- [ ] Replace `ISC criteria` with "verifiable criteria" or "acceptance checks"
- [ ] Replace `MEMORY/WORK/{slug}/PRD.md` pattern with "a working log file in the task's directory" (if the pattern is useful) or drop
- [ ] Replace `~/.claude/PAI/*` paths with `references/` or similar skill-local paths
- [ ] Replace `EFFORT LEVEL` / tier names (Standard, Extended, Advanced, Deep, Comprehensive) with generic effort language

### Keep (but inspect)

- [ ] Core behavioral content — thinking patterns, techniques, mental models
- [ ] Worked examples (drop any that are PAI-specific, keep the generic ones)
- [ ] Research citations
- [ ] Anti-patterns and failure modes
- [ ] Quality gates (but make them skill-local, not Algorithm-global)

### Add

- [ ] YAML frontmatter with `name` (kebab-case) and `description` (with USE WHEN cluster)
- [ ] "When to use" and "When NOT to use" sections if missing
- [ ] References to sibling skills in the destination plugin (not PAI skills)

## Decision heuristics for ambiguous cases

### "The skill references the Algorithm"

If the skill is *part of* the Algorithm (a thinking mode), reframe it as standalone: *"This technique can be invoked during any planning or decision phase"* — describe it as a tool, not as a stage.

If the skill is *called by* the Algorithm (skill-distiller, authoring-skills), rewrite references generically ("when you need to capture patterns from a working session" instead of "during the Algorithm's LEARN phase").

### "The skill writes to MEMORY/WORK"

If the writing is incidental (logging progress), replace with a skill-local working-log pattern (`./working-log.md` in the task's output dir, or drop entirely).

If the writing is the core deliverable (PRD stubs for session tracking), the skill is Algorithm-coupled — consider whether transferring it makes sense at all. Sometimes the right answer is "this skill can't be meaningfully ported without its runtime."

### "The skill uses subagents / TeamCreate"

These work fine in standard Claude Code plugins (Task tool, TeamCreate tool are available). Just remove any PAI-specific references to agent definitions (`~/.claude/agents/Engineer.md` etc.) and let the user spawn standard subagents.

Note Opus 4.7 spawns fewer subagents by default — if the skill relies on parallel subagents, make the spawn triggers explicit in the transferred skill.

### "The skill has a voice curl"

Always strip. The voice is a PAI-user preference, not a skill feature. No curl commands that depend on a specific local service.

### "The skill has customization directory references"

Always strip. Customizations are out of band for plugin skills — if users want to customize, they fork the plugin.

### "The skill is a router (parent `SKILL.md` only has a `Route To` table)"

PAI uses a pattern where a container skill (`ContentAnalysis/`) routes to one or more child skills (`ContentAnalysis/ExtractWisdom/`). For plugin transfer:

- **One child → flatten.** Drop the parent, promote the child's content to the new skill's `SKILL.md`, move child `Workflows/*.md` into `references/`.
- **Multiple children serving distinct use cases → split.** Each child becomes its own plugin skill. Drop the parent router.
- **Multiple children that share state or sequence → keep the router but rewrite it** as a `references/routing.md` or expand the parent `SKILL.md` to describe the whole flow inline.

### "The skill references a canonical PAI doc (WRITINGSTYLE.md, WORLDVIEW.md, etc.)"

These files exist only in PAI. Two options:

- If the referenced content is already fully described inline in the SKILL.md, drop the cross-reference.
- If the cross-reference is load-bearing (the skill assumes you'll read the canonical doc to follow it), extract the relevant portion and inline it, then drop the cross-reference.

Never leave a dangling `PAI/USER/…` path in a plugin skill.

### "The skill shells out to an unusual external CLI (fabric, yt-dlp, etc.)"

Don't assume plugin users have PAI-user tooling installed. Soften:

- "Use `fabric -y` on the URL" → "Use a transcript tool (e.g., `fabric -y` if installed, `yt-dlp --write-auto-sub`, or a captioning service). Fall back to asking the user for the transcript if none are available."

Keep the tool name as a hint, but don't make it a hard dependency.

## Application of Anthropic skill best practices (after stripping)

Once PAI-specifics are stripped, apply the standard checklist:

- **Frontmatter:** YAML with `name` (kebab-case, matches directory) and `description` under 1024 chars with trigger keywords
- **Description voice:** third-person, "USE WHEN" cluster at the start
- **Body length:** under 500 lines for SKILL.md (progressive disclosure via `references/` for more)
- **Progressive disclosure:** SKILL.md triggers and routes; deep content in `references/{name}.md`
- **No time-sensitive content:** no absolute dates, no "as of 2026" claims
- **Positive framing:** "do X" instead of "don't do Y" where possible
- **Concrete examples:** at least one worked example inline; more in `references/`
- **No ALL-CAPS scaffolding:** reserve CAPS for genuine iron laws; drop anti-laziness preambles
- **4.7 fitness:** no "summarize every N tool calls" scaffolding (4.7 does this natively); explicit triggers for subagent/tool use (4.7 uses fewer by default); literal-friendly conditions instead of "Claude decides"

## Worked example: transforming a PAI skill header

### Before (PAI-embedded)

```markdown
---
name: IterativeDepth
description: 2-8 scientific lens passes to surface hidden requirements single-pass analysis misses. USE WHEN iterative depth, deep exploration, multi-angle analysis, multiple perspectives, examine from angles, surface hidden requirements.
---

## Customization

**Before executing, check for user customizations at:**
`~/.claude/PAI/USER/SKILLCUSTOMIZATIONS/IterativeDepth/`

If this directory exists, load and apply any PREFERENCES.md, configurations, or resources found there. These override default behavior. If the directory does not exist, proceed with skill defaults.


# IterativeDepth

**Structured multi-angle exploration of the same problem to extract deeper understanding and richer ISC criteria.**

Grounded in 20 established scientific techniques across cognitive science...

## Core Concept

Instead of analyzing a problem once, run 2-8 structured passes through the same problem, each from a systematically different **lens**. Each pass surfaces requirements, edge cases, and criteria invisible from other angles. The combination yields ISC criteria that no single-pass analysis could produce.
```

### After (plugin-standard)

```markdown
---
name: iterative-depth
description: USE WHEN iterative depth, deep exploration, multi-angle analysis, multiple perspectives, examine from angles, surface hidden requirements. 2-8 scientific lens passes to surface hidden requirements single-pass analysis misses.
---

# iterative-depth

Structured multi-angle exploration of the same problem to extract deeper understanding and richer acceptance criteria.

Grounded in 20 established scientific techniques across cognitive science...

## Core Concept

Instead of analyzing a problem once, run 2-8 structured passes through the same problem, each from a systematically different **lens**. Each pass surfaces requirements, edge cases, and criteria invisible from other angles. The combination yields acceptance criteria that no single-pass analysis could produce.
```

Changes: frontmatter name kebab-cased, customization block dropped, "ISC criteria" → "acceptance criteria" (twice). The substance is untouched.

### Second worked example: collapsing a router parent

Source tree:
```
ContentAnalysis/
├── SKILL.md           (14 lines — just a routing table)
└── ExtractWisdom/
    ├── SKILL.md       (229 lines — the real skill)
    └── Workflows/
        └── Extract.md (60 lines — procedure reference)
```

Destination tree:
```
content-analysis/
├── SKILL.md              (promoted from ExtractWisdom/SKILL.md)
└── references/
    └── extract-workflow.md (moved from Workflows/Extract.md)
```

Router parent dropped entirely — it had one child, so it was dead weight. The child's content becomes the new skill's root. Workflow files move into `references/` (the plugin convention for progressive disclosure).

## Common mistakes

- **Silent-stripping without checking dependencies.** If a skill's Examples.md references the PAI Algorithm, stripping the header but leaving the examples creates a dangling reference. Grep the whole transferred tree for remaining PAI markers after you think you're done.
- **Over-generalization.** Don't replace every "Algorithm" with "system" if it dilutes meaning. Sometimes the right rewrite is to drop the sentence entirely.
- **Copying runtime-coupled skills.** Some PAI skills (those that write to session tracking files, orchestrate the Algorithm phases) don't transfer meaningfully. Recognize these and document the dependency rather than ship a broken port.
- **Not QC-ing after stripping.** Run `grep -r "PAI\|SKILLCUSTOMIZATIONS\|MEMORY/WORK\|Algorithm" <destination>/` — should return zero results (or only legitimately generic mentions).
- **Forgetting the directory name.** If source is `IterativeDepth/`, destination should be `iterative-depth/`. Claude Code works with both but repo convention is kebab-case.

## QC pass

After the transfer, verify:

```bash
DEST=plugins/<plugin>/skills/<skill>

# No PAI markers remaining (includes template vars, canonical docs, Customization headers, voice_id tokens)
grep -rnE 'PAI/|SKILLCUSTOMIZATIONS|MEMORY/WORK|PRD\.md|ISC criteria|Algorithm phase|localhost:8888/notify|\{PRINCIPAL|WRITINGSTYLE|WORLDVIEW|^## Customization|voice_id' "$DEST/" || echo "clean"

# All SKILL.md have frontmatter
for f in $(find "$DEST" -name SKILL.md); do
  head -1 "$f" | grep -q '^---$' || echo "missing frontmatter: $f"
done

# Directory basenames are kebab-case (strips absolute path so uppercase in parent dirs doesn't false-positive)
find "$DEST" -maxdepth 2 -type d | awk -F/ '{print $NF}' | grep -E '[A-Z]' && echo "PascalCase/camelCase dirs found" || echo "naming clean"
```

## Related skills

- `skill-distiller` — for extracting reusable patterns from a working session (not PAI-transfer specific)
- `prompt-craft` — for refining the transferred skill's description after stripping PAI content
- `be-creative` — example of a well-formed post-rework skill in this repo (was originally PAI-adjacent, now standalone)
