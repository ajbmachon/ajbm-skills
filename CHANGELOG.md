# Changelog

All notable changes to this repository. Versions are per-plugin; see each plugin's `.claude-plugin/plugin.json` for current version.

## Unreleased (branch: `review/opus-4-7-tightens`)

### `ajbm-dev` 1.2.0 → 1.3.0

**Added**
- `be-creative` — Verbalized Sampling (Zhang et al. 2024) skill. Full rework of the previous 12-file version; now 3 files focused on the technique with worked examples.
- `thinking` — 5-mode analytical thinking router (first-principles, iterative-depth, council, red-team, science). Transferred from PAI with PAI-specifics stripped.
- `pai-skill-transfer` — methodology for porting PAI skills into plugins. Test-driven: hardened after a real ContentAnalysis transfer surfaced 4 gaps.
- `content-analysis` — content-adaptive wisdom extraction from videos/podcasts/articles. Transferred from PAI.

**Changed**
- `prompt-craft/reference/models/claude.md` — refreshed for Opus 4.7 (new `xhigh` effort tier, adaptive thinking, sampling params removed, new tokenizer, prefill removal, task budgets beta).
- `prompt-craft/SKILL.md` — anti-overtriggering section updated for 4.7's literal-instruction bias.
- `test-driven-development/SKILL.md` — compressed 4.6-era execution preamble from 8 lines to 3; kept the skill-specific nudge.
- `testing-best-practices/SKILL.md` — same preamble compression (7 → 3 lines).
- `setup-linter/SKILL.md` — description rewritten with USE WHEN trigger cluster.
- `systematic-debugging/SKILL.md` — fixed stilted heading.

### `ajbm-agent-align` — no version bump (fixes only)
- Normalized skill directory and frontmatter naming (`AgentAlign` → `agent-align`).

### `ajbm-business` — no version bump (fixes only)
- Normalized x-post-writer: frontmatter name matches directory, references moved to `references/`, description adds USE WHEN cluster.
- Removed orphan line-count comment from `hormozi-pitch/SKILL.md`.

### `ajbm-social` — no version bump (fixes only)
- `twitter-cli` references: `-c` flag consistency (global flag precedes subcommand), post-permission callout before write commands (`post`, `reply`, `quote`).

### Repository-wide
- All skills tuned for Opus 4.7 compatibility. Changes compatible with Opus 4.6 and Sonnet 4.6.
- Plugin versions recorded in README per-section for visibility.

## Previous history

See `git log` for commits prior to this branch.
