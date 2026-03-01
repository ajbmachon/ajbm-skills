# AJBM Skills for Claude Code

A collection of generally useful Claude Code skills that work across all Anthropic surfaces.

**Plugins:** `ajbm-dev`, `ajbm-interview`, `ajbm-agent-align`, `ajbm-business`, `ajbm-communication`, `ajbm-security`
**Install:** `/plugin install ajbm-dev@ajbm`

---

## Development Skills (ajbm-dev)

### authoring-skills

Use when writing or reviewing SKILL.md files.

**Key principles:**
- Keep SKILL.md under 500 lines
- Use progressive disclosure (reference files for details)
- Write descriptions in third person with trigger keywords
- Include both what the skill does AND when to use it

**Quality checklist:**
- [ ] Description specific with triggers (max 1024 chars)
- [ ] SKILL.md under 500 lines
- [ ] No time-sensitive information
- [ ] Consistent terminology
- [ ] Concrete examples

### prompt-craft

Use when writing, analyzing, or improving prompts for LLMs.

**Modes:**
- **A. Analyze**: Critique existing prompt, score techniques
- **B. Craft**: Build optimized prompt from requirements
- **C. Teach**: Deep dive on a specific technique
- **D. Quick Fix**: Fast 3-improvement pass

**19 Research-Backed Techniques:**
- **10 Core**: Chain-of-Thought, Structured Output, Few-Shot, Placement, Salience, Roles, Positive Framing, Reasoning-First, Verbalized Sampling, Self-Reflection
- **9 Extended**: Decomposition, Compression, Sufficiency, Scope, Format-Spec, Uncertainty, Chaining, Self-Consistency, Tree-of-Thoughts

**Model-Specific Guidance:**
Claude 4.x, GPT-5.2/5.1, GPT-4o, o1/o3, DeepSeek V3/R1, Gemini 2.0, Kimi K2, Qwen 2.5

### setup-linter

Use when user asks to set up automatic linting, add a linter hook, or configure code formatting on completion.

**What it does:**
1. Auto-detects project type from config files
2. Installs linter if not present (eslint, ruff, etc.)
3. Creates config file with sensible defaults
4. Adds lint scripts to package.json (JS projects)
5. Sets up Stop hook in `.claude/settings.json`
6. Adds clean-code-reviewer instruction to project `CLAUDE.md`

**Usage:**
```bash
~/.claude/skills/setup-linter/scripts/setup.sh           # Auto-detect
~/.claude/skills/setup-linter/scripts/setup.sh "yarn lint:fix"  # Custom
```

### systematic-debugging

Use when encountering any bug, test failure, or unexpected behavior—BEFORE proposing fixes.

**Iron Law:** Investigate root cause before proposing fixes

**Four Phases:**
1. Root cause investigation
2. Pattern analysis
3. Hypothesis testing
4. Implementation

**When to use:** Test failures, bugs, unexpected behavior, performance problems.

### testing-best-practices

Use when writing, reviewing, or reporting tests. Comprehensive testing quality skill.

**Five Iron Laws:**
1. Investigate when a test passes on first run
2. ALWAYS assert on real system behavior, not mock wiring
3. ALWAYS keep tests as straight-line code
4. ALWAYS execute tests and report concrete evidence
5. ALWAYS keep production APIs clean

**Core principle:** Evidence is the product. Test behavior, not implementation.

### test-driven-development

Use when implementing any feature or bugfix—write the test first, watch it fail, write minimal code to pass.

**The Iron Law:** Write production code only after a failing test exists

**Red-Green-Refactor cycle:**
1. **RED**: Write one minimal failing test
2. **Verify RED**: Run it, confirm it fails for the right reason
3. **GREEN**: Write simplest code to pass
4. **Verify GREEN**: Run it, confirm all tests pass
5. **REFACTOR**: Clean up while staying green

**Red Flags (stop and start over):**
- Code written before test
- Test passes immediately
- Rationalizing "just this once"
- "I already manually tested it"

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

### skill-distiller

Use when user wants to distill, extract skill, capture patterns, teach from conversation, or learn from session.

**Core concept:** Extracts expert guidance patterns from conversations and distills them into permanent, replayable skills that teach Claude behavioral dispositions (not rigid rules).

**Five-step guided flow:**
1. **Source** — Current session (in-memory) or stored transcript (session ID/file path)
2. **Analyze** — Extract patterns across four categories (Corrections, Questions & Probes, Quality Gates, Analysis Modes)
3. **Review & Co-Edit** — Collaborative pattern review with user (Claude proposes, user decides)
4. **Generate** — Write SKILL.md using behavioral dispositions format
5. **Verify** — On-demand behavioral checks via `/distill verify <path>`

**Toolbox:** transcript-filter, turn-extractor (on-demand, not a pipeline)

**Dependency:** qmd for cross-conversation semantic search

### docs-research-specialist (agent)

Use when looking up current documentation, API syntax, library patterns, or best practices. Invoked proactively during interview research phases and general dev work.

**Tool priority:** Exa MCP > Context7 MCP > WebFetch > Local codebase

**Key rules:**
- Every claim must have inline source URL
- 30-day cache with changelog-based staleness detection
- Saves reports with YAML frontmatter (topic, date, expiry, sources)

**When to invoke:** Any time you need current docs for a library, framework, or API.

### clean-code-reviewer (agent)

Use after implementing a working feature to analyze for Clean Code compliance. Activated via project CLAUDE.md instruction added by setup-linter.

**Two-commit workflow:**
1. First commit: working implementation
2. Second commit: clean code improvements from review

**Report tiers:**
- 🟢 SYNTACTIC: Auto-fixable (unused imports, dead code, formatting)
- 🟡 SEMANTIC: Localized changes (naming, extraction, constants)
- 🔴 ARCHITECTURAL: Cross-file design (SRP, coupling, blast radius shown)

**Includes:** TDD-Readiness score, refactoring priority matrix, educational "Why This Matters" per violation.

---

## Interview Plugin (ajbm-interview)

### interview

Use when user mentions spec, requirements, interview, flesh out idea, plan feature, business idea, design review, ideation, document draft, devil's advocate, stress test, brainstorm, clarify, quick spec, scope this, help me think through.

**Core principle:** Structured elicitation that combines human tacit knowledge with AI's combinatorial breadth. The goal is alignment — both parties holding the same mental model with no hidden ambiguities.

**Seven workflows:**

| Workflow | When | Flow |
|----------|------|------|
| **QuickClarify** | Small/medium tasks with ambiguities | Mirror → Surface → Probe → Converge (2-5 min, inline output) |
| **DevSpec** | Software features, implementations | Full 7-phase with codebase research and TDD output |
| **BusinessIdea** | Startups, products, revenue models | Full 7-phase with market research and business case |
| **DocumentDraft** | Written content, proposals, docs | Full 7-phase with audience analysis and style alignment |
| **DesignReview** | UI/UX, system design, architecture | Full 7-phase with visual Showpiece questions |
| **Ideation** | Brainstorming, creative exploration | Diverge-Constrain-Refine-Verify with BeCreative integration |
| **DevilsAdvocate** | Stress-testing, challenging ideas | Standalone challenge with cognitive critique modes |

**Full workflow identity:**
- **Phases 1-2:** Critical Challenger (skeptical, probing, BLOCKING research)
- **Transition:** Capture Constraint Registry, get user confirmation
- **Phase 3+:** Expert Partner (collaborative, CONSTRAINT-ENFORCED)

**QuickClarify** skips challenge and constraints — purely collaborative, 1-3 rounds of questions, inline output. For when the idea doesn't need to defend its right to exist, just needs refinement.

---

## AgentAlign Plugin (ajbm-agent-align)

### agent-align

Use when agents delegate tasks to other agents in multi-agent systems. Triggers: agent alignment, delegation alignment, agent handoff, multi-agent delegation.

**Core principle:** AI-to-AI alignment bridges **context asymmetry** — same intelligence, different information. When a delegator compresses a rich conversation into a prompt, information is lost. AgentAlign verifies that critical context, constraints, and intent survive the handoff.

**Three graduated levels:**

| Level | When | Protocol |
|-------|------|----------|
| **Inline** | Simple, well-specified tasks | Worker echoes understanding in first output (~50 tokens) |
| **Quick** | Moderate tasks with ambiguities | 1 round of SendMessage: ECHO + AUDIT + RECOVER → CONTRACT (~300 tokens) |
| **Full** | Complex tasks, multi-layer chains | Multi-round with shared handoff spec document (~800 tokens) |

**Four operations:** ECHO (verify compression), AUDIT (surface assumptions + constraint inheritance), RECOVER (fill delegation gaps), CONTRACT (confirm execution agreement).

**Constraint inheritance chains:** Explicit chain-of-custody so human principal's constraints survive multi-layer delegation (Leader → Architect → Engineer) without evaporation or drift.

---

## Business Skills (ajbm-business)

### hormozi-pitch

Use when creating offers, pitches, pricing, guarantees, or value propositions.

**Value Equation:**
```
Value = (Dream Outcome × Perceived Likelihood) / (Time Delay × Effort & Sacrifice)
```

**Frameworks:**
- **MAGIC Naming**: Make a name, Announce target, Give results, Indicate timeframe, Call out container
- **Guarantee Types**: Unconditional, Conditional, Anti-guarantee, Implied
- **Value Stack**: Justify any price point by stacking bonuses

**"Stupid Not To" Test:** Prospect should feel irrational saying no.

### x-post-writer

Use when writing tweets, Twitter threads, or social media copy.

**Hook Fundamentals:**
- Target the reader directly ("You can..." not "People are...")
- Lead with benefit first
- Avoid overused patterns ("Most creators...", "Everyone is...")

**Engagement Triggers:**
- Social proof ($31K made, 100k followers)
- Urgency/scarcity (Free for 24hrs)
- Low friction (No email bs, Just comment X)
- Exclusive access (I'll DM you the guide)

**Structure:**
- One clear idea per tweet
- Short paragraphs (1-2 sentences)
- Bullet points for readability
- Clear CTA at end

---

## Communication Skills (ajbm-communication)

### tactical-empathy

Use when negotiating, preparing for difficult conversations, persuading, giving feedback, salary discussions, deal-making, conflict resolution, or practicing negotiation through roleplay.

**Core philosophy:** Chris Voss's "Never Split the Difference" — negotiation as tactical empathy, not argument. Vector activation approach: terminology clusters activate expert behavior rather than dumping knowledge.

**The Big Three techniques:**
- **Mirroring:** Repeat last 1-3 words + silence. Forces elaboration, gathers information, builds connection.
- **Labeling:** "It seems like..." names the emotion underneath. Precision matters — surgical labels get "that's right."
- **Calibrated Questions:** "How am I supposed to do that?" says no without saying no. Makes your problem their problem.

**Two workflows:**

| Workflow | When | Output |
|----------|------|--------|
| **Analyze** | Situation described, preparing for a conversation | Written dossier file with strategy, exact phrases, danger zones |
| **Spar** | "Practice", "roleplay", "rehearse" | Roleplay as counterpart with inline `[COACH:]` annotations |

**Complementary frameworks** (loaded on demand): BATNA Analysis, OFNR (NVC), Safety Monitoring (Crucial Conversations), Three Conversations (Difficult Conversations).

**Quality gate:** Before any recommendation — "Am I suggesting compromise because it serves their interests, or because it avoids discomfort?" Never split the difference.

---

## Security Plugin (ajbm-security)

Blocks dangerous bash commands and sensitive file access via the `smart-guard` PreToolUse hook.

**Blocks:**
- Destructive commands (`rm -rf /`, fork bombs, disk wiping)
- Sensitive file access (`.env`, `.ssh/`, AWS/GCP/Azure credentials, private keys)

**Enable/Disable:** Use `/plugin` menu in Claude Code.

---

## Skills Are Model-Invoked

These skills activate automatically based on context. You don't need to call them explicitly—Claude detects when they're relevant from:
- Keywords in your prompt
- Task type (creating offers, writing prompts, etc.)
- File patterns being worked on

## Background Agent Output Management

**Background agent output management:**

When checking on background agents (Task tool with `run_in_background: true`):

1. **Avoid** reading the full `.output` file directly - it contains the entire conversation transcript
2. **NEVER** use `sleep` commands to poll - you receive automatic notifications when agents complete
3. **DO** use `tail -20` to see just the final messages if needed
4. **DO** use `grep` to find specific patterns in output

**For docs-research-specialist agents specifically:**
- They save their research to `docs/research/` or `.ai/research/`
- Just read the final output file (e.g., `docs/research/topic-name-YYYY-MM-DD.md`) instead of the agent transcript
- The research file is token-efficient; the transcript is not

**Examples:**
```bash
# WRONG - floods context
cat /tmp/claude/.../tasks/agent-id.output

# RIGHT - final messages only
tail -30 /tmp/claude/.../tasks/agent-id.output

# BEST for research agents - read the actual output file
cat docs/research/langfuse-setup-2026-01-20.md
```

---

## Contributing

1. Follow the 500-line rule for SKILL.md files
2. Use progressive disclosure (reference files for details)
3. Write specific descriptions with trigger keywords
4. Test with 3+ real scenarios before committing
