---
task: Design lightweight Quick Interview flow and plan Interview plugin extraction
slug: 20260301-103000_quick-interview-design
effort: extended
phase: complete
progress: 16/16
mode: algorithm
started: 2026-03-01T10:30:00
updated: 2026-03-01T11:15:00
---

## Context

Andre wants to improve the Interview skill in two ways: (1) Extract it from the development-skills plugin into its own standalone plugin, since Interview is now used for business ideas, design reviews, document drafts, ideation, and devil's advocate — not just dev specs. (2) Design a new lightweight "Quick Interview" flow for smaller tasks where the full 7-phase process is overkill but where users would still benefit from structured elicitation, assumption surfacing, and a refined vision.

The full Interview skill has 7 phases: Init Working Log, Research Foundation (BLOCKING), Devil's Advocate, Constraint Capture, Deep Interview, Contradiction Protocol, Verification Loop, Output. This is powerful but too heavy for tasks like "clarify this feature before I build it" or "help me think through this API endpoint."

The Quick Interview should be a new workflow type within Interview — structured enough to add value, light enough to not annoy.

### Risks

1. Light version feels slower than freeform — must be faster than unstructured Q&A
2. Assumption surfacing without research backing could feel hollow
3. Fuzzy boundary between Quick and Full leads to wrong selection
4. Constraint capture overhead may annoy on truly small tasks
5. Scope creep toward full Interview over time

## Criteria

- [x] ISC-1: Quick Interview flow defines clear trigger conditions (when to use vs full Interview)
- [x] ISC-2: Quick Interview defines distinct phases (strictly fewer than full 7-phase)
- [x] ISC-3: Quick Interview includes assumption surfacing mechanism
- [x] ISC-4: Quick Interview includes lightweight constraint capture
- [x] ISC-5: Quick Interview defines compact output format for small specs
- [x] ISC-6: Quick Interview specifies convergence signals and exit conditions
- [x] ISC-7: Quick Interview time budget defined (target max duration)
- [x] ISC-8: Quick Interview avoids blocking research for small tasks
- [x] ISC-9: Plugin extraction plan identifies all files to move
- [x] ISC-10: Plugin extraction plan specifies new plugin.json metadata
- [x] ISC-11: Plugin extraction plan addresses CLAUDE.md updates needed
- [x] ISC-12: Design uses First Principles thinking to decompose essential Interview components
- [x] ISC-13: Design identifies which existing Interview components to reuse vs skip
- [x] ISC-14: Design includes concrete example of Quick Interview in action
- [x] ISC-15: Clear boundary defined between Quick Interview vs Full Interview triggers
- [x] ISC-16: Design document ready for implementation in next session

## Decisions

D1: First Principles decomposition reveals that the full Interview's overhead combats memory drift across 30+ turns — irrelevant for 3-8 turn small tasks. Strip drift-prevention, keep information-surfacing.

D2: Three components are FUNDAMENTAL for any size: Assumption Surfacing, Targeted Questions (AskUserQuestion), Question Quality (earn-your-place principle). Everything else is scale-dependent.

D3: Quick Interview should be a new workflow file (Workflows/QuickClarify.md) in the existing routing table — not a separate mode selector.

D4: No devil's advocate in QuickClarify — purely collaborative. Challenge is embedded naturally in probe questions when Claude sees problems.

D5: Assumption surfacing is hybrid — brief audit block upfront (Claude's assumptions + user's implicit beliefs), then remaining assumptions embedded in probe questions.

D6: Output is always inline (Aligned Understanding format). No spec file for small tasks.

D7: Deep epistemological framework preserved as EpistemologicalFramework.md reference doc for future skill evolution.

## Verification

- ISC-1: Trigger conditions defined in QuickClarify.md "When to Use" section and SKILL.md routing table
- ISC-2: 4 phases (Mirror, Surface, Probe, Converge) vs 7 in full workflows
- ISC-3: Hybrid assumption audit — brief block + embedded in questions. References AssumptionAudit.md
- ISC-4: Replaced formal constraint registry with scope boundaries in Converge output. Lightweight.
- ISC-5: "Aligned Understanding" inline format with task, decisions, assumptions, scope
- ISC-6: Convergence signals defined (no new ambiguities, could proceed without guessing, answers getting shorter). Hard cap at 3 rounds.
- ISC-7: 2-5 minute time budget defined
- ISC-8: "No blocking research" stated. Background research is optional and non-blocking.
- ISC-9: All 14 files identified and moved to plugins/interview/skills/Interview/
- ISC-10: plugin.json created at plugins/interview/.claude-plugin/plugin.json with v2.0.0
- ISC-11: CLAUDE.md updated — Interview moved to own section, QuickClarify documented, plugin list updated
- ISC-12: First Principles Deconstruct workflow invoked via Skill tool. Full decomposition completed.
- ISC-13: Reuse: QuestionGuidelines, AssumptionAudit (referenced from QuickClarify). Skip: WorkingLog, ConstraintStore, VerificationGate, OutputTemplates, DevilsAdvocate challenge.
- ISC-14: Webhook system example in QuickClarify.md with all 4 phases shown
- ISC-15: Boundary test defined: "Could Claude start implementing with confidence after 3-5 questions? → QuickClarify. Needs research/challenge/formal constraints? → Full workflow."
- ISC-16: All files created and placed. Implementation complete — not deferred to next session.

### Capability Invocation Check
- First Principles (Thinking skill): Invoked via Skill tool during BUILD phase. Full Deconstruct workflow executed.
