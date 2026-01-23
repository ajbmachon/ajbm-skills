# AJBM Skills for Claude Code

A collection of generally useful Claude Code skills that work across all Anthropic surfaces.

**Plugins:** `ajbm-dev`, `ajbm-business`, `ajbm-security`
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

### interview

Use when user mentions spec, requirements, interview, wants to flesh out an idea, or needs help planning a feature.

**Two-Phase Identity:**
- **Phases 1-2:** Critical Challenger (skeptical, probing, BLOCKING research)
- **Phase 3+:** Expert Partner (collaborative, thorough, CONSTRAINT-ENFORCED)

**Key mechanisms:**
- Constraint Registry captures hard/soft constraints at transition
- Verification Gate checks recommendations against constraints
- Self-Challenge Trigger catches assumptions during Partner phase
- Working log for progressive documentation

**Transition rule:** Never proceed to Partner without explicit constraint confirmation.

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

**Iron Law:** NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST

**Four Phases:**
1. Root cause investigation
2. Pattern analysis
3. Hypothesis testing
4. Implementation

**When to use:** Test failures, bugs, unexpected behavior, performance problems.

### testing-anti-patterns

Use when writing or changing tests, adding mocks, or tempted to add test-only methods to production code.

**Three Iron Laws:**
1. NEVER test mock behavior
2. NEVER add test-only methods to production classes
3. NEVER mock without understanding dependencies

**Core principle:** Test what the code does, not what the mocks do.

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

## Contributing

1. Follow the 500-line rule for SKILL.md files
2. Use progressive disclosure (reference files for details)
3. Write specific descriptions with trigger keywords
4. Test with 3+ real scenarios before committing
