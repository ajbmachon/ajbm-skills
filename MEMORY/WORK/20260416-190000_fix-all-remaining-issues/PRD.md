---
task: Fix all remaining audit-surfaced issues
slug: 20260416-190000_fix-all-remaining-issues
effort: deep
phase: observe
progress: 0/0
mode: interactive
started: 2026-04-16T18:24:57Z
updated: 2026-04-16T18:24:57Z
---

## Context

User asked to fix everything in the backlog from 4 late-arriving subagent audits. Explicitly requested Algorithm mode with task tracking. Branch `review/opus-4-7-tightens` (draft PR #10) already has 11 commits; this run will add fixes for the surfaced-but-unexecuted issues and then decide whether the interview-skill dedup ships with this PR or a separate one.

### What was explicitly requested
- Fix all remaining issues from the audits
- Use Algorithm so I don't forget anything
- Track tasks

### What was explicitly not requested
- Don't rewrite from scratch
- Don't fold all work into one mega-commit (keep diff reviewable)

### Known backlog (from 4 audits)

**A. twitter-cli flag/content issues**
- 7 more missing `-c` flags across classify-workflow.md, save-and-organize.md, search-workflow.md, trading-research.md
- Undocumented `-m` flag (verify exists in twitter-cli or remove)
- Stale hardcoded date `--since 2026-03-01`
- Permission callout needed for write commands

**B. testing-best-practices references**
- Unsourced citations: "68%" (principles.md:335), "50x" (testing-trophy.md:62), "19x" (testing-trophy.md:95)
- Decision tree vs override table contradiction (testing-trophy.md:33-57)
- anti-patterns.md:3 claims "15 anti-patterns with code examples" but only 5/15 have code
- anti-patterns.md:285 forces reader back to main SKILL.md (breaks progressive disclosure)

**B2. tactical-empathy references**
- voss-framework.md:3 Sonnet-era self-framing opener
- dossier-template.md:7 outer code-fence may cause doubly-fenced output

**C. agent-align level4-deep**
- overview.md:83 TeamCreate spawn needs 4.7 justification
- decision-policy.md missing evaluation order (which criterion to check first)
- spec-refinement-workflow.md references P6/P5/P7 from non-included synthesis doc
- interviewer.md + spec-refinement-workflow.md duplicate challenge angles

**E. Interview skill (largest, judgment call on scope)**
- Hard/Soft/Boundary constraint schema duplicated verbatim in 3 files
- AI-Decided-Items schema duplicated verbatim in 3 files
- "Standard Pattern Trap" repeated in 4 files
- EpistemologicalFramework.md (202 lines) largely duplicates SKILL.md:69-92
- QuestionGuidelines.md (506 lines) NON-NEGOTIABLE rules conflict with SKILL.md "Q&A rounds: HIGH"
- QuickClarify.md claims self-contained but has 2 mandatory_read blocks
- DocumentDraft/BusinessIdea/DesignReview workflows use generic questions violating skill's own "no canned questions" rule
- No domain-specific Tier 1 examples in 3 workflow files (VerificationGate protocol expects them)

**F. Cosmetic**
- x-post-writer high-performing-examples.md:199 typo (ingore → ignore)
- hormozi-pitch workflow.md:32 ASCII art (28 lines decorative)
- hormozi-pitch frameworks-reference.md:650-692 Quick Reference Card duplicates headers
- x-post-writer: writing-principles.md duplicates copywriting-principles.md significantly
- Example provenance disclaimer for high-performing-examples.md

## Criteria

**A. twitter-cli (8 ISC)**
- [ ] ISC-1: classify-workflow.md line 30 has `twitter -c bookmarks folders`
- [ ] ISC-2: save-and-organize.md line 8 has `twitter -c tweet`
- [ ] ISC-3: save-and-organize.md line 57 has `twitter -c bookmarks`
- [ ] ISC-4: trading-research.md line 46 has `twitter -c bookmarks`
- [ ] ISC-5: trading-research.md line 66 has `twitter -c tweet`
- [ ] ISC-6: trading-research.md stale `--since 2026-03-01` replaced with relative guidance
- [ ] ISC-7: trading-research.md `-m` flag verified against CLI and kept or removed
- [ ] ISC-8: twitter-cli refs grep for `^twitter (bookmarks|tweet|article|feed|search|post|thread)` returns zero matches without `-c`

**B. testing-best-practices refs (6 ISC)**
- [ ] ISC-9: principles.md 68% citation has source URL or softened
- [ ] ISC-10: testing-trophy.md 50x citation has source URL or softened
- [ ] ISC-11: testing-trophy.md 19x citation has source URL or softened
- [ ] ISC-12: testing-trophy.md decision tree and override table reconciled with explicit precedence rule
- [ ] ISC-13: anti-patterns.md:3 opening claim matches actual content (either add examples or rewrite claim)
- [ ] ISC-14: anti-patterns.md Oracle Guard protocol inlined (no forced back-jump to main SKILL.md)

**B2. tactical-empathy refs (2 ISC)**
- [ ] ISC-15: voss-framework.md opener rewritten without Sonnet-era self-framing
- [ ] ISC-16: dossier-template.md outer code-fence removed or structure changed so no double-fencing risk

**C. agent-align level4-deep (4 ISC)**
- [ ] ISC-17: overview.md TeamCreate spawn has explicit 4.7 justification
- [ ] ISC-18: decision-policy.md specifies evaluation order for criterion checking
- [ ] ISC-19: spec-refinement-workflow.md P6/P5/P7 refs either inlined or explicitly linked
- [ ] ISC-20: challenge angles deduplicated between interviewer.md and spec-refinement-workflow.md

**E. Interview skill dedup (8 ISC)**
- [ ] ISC-21: constraint schema has single authoritative location
- [ ] ISC-22: AI-Decided-Items schema has single authoritative location
- [ ] ISC-23: Standard Pattern Trap has single authoritative location
- [ ] ISC-24: EpistemologicalFramework.md either deleted or operationally trimmed
- [ ] ISC-25: QuestionGuidelines.md NON-NEGOTIABLE rules reconciled with SKILL.md freedom-designations
- [ ] ISC-26: QuickClarify.md self-containment claim matches mandatory_read actuality
- [ ] ISC-27: DocumentDraft/BusinessIdea/DesignReview generic canned questions removed or reframed
- [ ] ISC-28: Workflow files have domain-specific Tier 1 examples or VerificationGate protocol relaxed

**F. Cosmetic (5 ISC)**
- [ ] ISC-29: x-post-writer typo `ingore` fixed
- [ ] ISC-30: hormozi-pitch workflow.md ASCII art replaced with compact list
- [ ] ISC-31: hormozi-pitch frameworks-reference.md Quick Reference Card collision resolved
- [ ] ISC-32: x-post-writer writing-principles.md duplication with copywriting-principles.md reduced
- [ ] ISC-33: x-post-writer high-performing-examples.md has provenance disclaimer

**Post-execution (4 ISC)**
- [ ] ISC-34: All changes committed in logically-grouped commits (at minimum: one per category A/B/B2/C/F; E may be split)
- [ ] ISC-35: `grep -r "ingore\|twitter bookmarks --\|twitter tweet "` returns zero hits outside the -c-prefixed versions
- [ ] ISC-36: All modified SKILL.md files still under 500 lines
- [ ] ISC-37: Branch pushed and PR #10 updated

**Verification anti-criteria**
- [ ] ISC-A1: No new scaffolding added beyond what fixes required
- [ ] ISC-A2: No time-sensitive dates introduced
- [ ] ISC-A3: No `<` or `>` wrapping added to URLs that weren't there before
- [ ] ISC-A4: Cosmetic fixes don't rewrite substantive content

## Decisions

**D1 (A category rescope):** The audit claim of "7 more `-c` flag violations" was based on a flawed reading. Per twitter-cli SKILL.md:55 — "`-c` is for readable output. Use `--json` when you need to parse." All 9 remaining non-`-c` invocations are `--json` output commands meant for parsing, which correctly omit `-c`. No fixes needed for ISC-1 through ISC-5, ISC-8 — they're already correct.
  - Evidence: `twitter bookmarks --help` shows `-c` is global compact-output flag; `--json` overrides output format.
  - ISC-1 through ISC-5, ISC-8 → mark as verified-correct, not "fix needed"
  - ISC-7 `-m` flag: verified real via `twitter article --help` — `-m, --markdown` exists. Keep.
  - ISC-6 stale date: real issue, will fix.

**D2 (Interview skill scope):** E category is big enough that it warrants its own branch/PR. Will handle A-D + F on this PR, then open `review/interview-skill-dedup` for E separately. Reason: keeps diff reviewable, E is judgment-heavy, and the main PR is already 11+ commits.

**D3 (Citation recovery):** For unsourced citations, attempt web search first before softening. If source recoverable, add URL. If not, replace quantified claim with a qualitative one ("significantly more" vs "19x more").

## Verification

(will be populated during work)
