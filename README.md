# AJBM Skills for Claude Code

A collection of generally useful Claude Code skills that work across all Anthropic surfaces. These skills are not workflow-specific—they're universal productivity boosters for anyone using Claude Code.

## Skills Included

| Skill | Description |
|-------|-------------|
| **interview** | Transform rough ideas into implementation-ready specs through rigorous research and questioning. Evolves from Critical Challenger to Expert Partner. |
| **systematic-debugging** | Four-phase debugging framework: root cause → pattern analysis → hypothesis → implementation. No fixes without understanding. |
| **testing-anti-patterns** | Prevents common testing mistakes: testing mocks, test-only production methods, mocking without understanding dependencies. |
| **setup-linter** | Auto-detect, install, and configure project-specific linting with a Stop hook. Supports JS/TS, Python, Rust, Go, Deno. |
| **authoring-skills** | Complete guide for writing skills—covers SKILL.md best practices, plugin development, triggers, hooks, and Anthropic guidelines |
| **prompt-craft** | 19 research-backed prompting techniques with model-specific guidance (Claude, GPT-4o, o1/o3, DeepSeek, Gemini, Kimi, Qwen, Grok). Modes: Analyze, Craft, Teach, Quick Fix |
| **hormozi-pitch** | Alex Hormozi's $100M Offers methodology for creating irresistible offers, pricing, guarantees, and value propositions |
| **x-post-writer** | Twitter/X copywriting system for high-engagement social media content with viral frameworks and examples |

---

## Installation

### Prerequisites

- Claude Code installed (`npm install -g @anthropic-ai/claude-code` or via the [official installer](https://docs.anthropic.com/en/docs/claude-code/quickstart))
- Basic familiarity with Claude Code CLI

### Option 1: Install from GitHub (Recommended)

```bash
# Start Claude Code
claude

# Add the marketplace
/plugin marketplace add ajbmachon/ajbm-skills

# Install development skills (debugging, testing, specs, linting, prompts)
/plugin install ajbm-dev@ajbm

# Install business skills (offers, copywriting) - optional
/plugin install ajbm-business@ajbm
```

After installation, restart Claude Code to activate the skills.

### Option 2: Install from Local Clone

```bash
# Clone the repository
git clone https://github.com/ajbmachon/ajbm-skills.git

# Start Claude Code
claude

# Add as local marketplace
/plugin marketplace add ./ajbm-skills

# Install the plugins
/plugin install ajbm-dev@ajbm
/plugin install ajbm-business@ajbm
```

### Verify Installation

After restarting Claude Code:

```bash
# Ask Claude about available skills
What skills are available?
```

---

## Automatic Skill Suggestions

The ajbm-dev plugin includes **smart hooks** that automatically suggest relevant skills based on context:

### Prompt-Based Suggestions (UserPromptSubmit)

When you type a prompt, the hook analyzes it and suggests skills:

```
You: "help me plan this authentication feature"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 SKILL ACTIVATION CHECK
📚 RECOMMENDED SKILLS:
  ⚡ interview (score: 41)
ACTION: Use Skill tool BEFORE responding
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

| Trigger Keywords | Suggested Skill |
|------------------|-----------------|
| "plan", "idea", "spec", "design", "scope" | interview |
| "test", "mock", "coverage", "TDD" | testing-anti-patterns |
| "debug", "bug", "fix", "error", "broken" | systematic-debugging |
| "prompt", "llm", "system prompt" | prompt-craft |
| "skill", "hook", "plugin", "SKILL.md" | authoring-skills |

### Error Detection (PostToolUse)

When a command fails (tests, builds, servers), the hook detects it and warns Claude:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  ERROR DETECTED IN OUTPUT
Detected: Test failure

📚 RECOMMENDED SKILLS:
  ⚡ systematic-debugging (investigate root cause FIRST)
  ⚡ testing-anti-patterns (avoid common testing mistakes)

⛔ DO NOT attempt quick fixes without investigation!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

This prevents Claude from jumping straight to fixes without understanding the root cause.

---

## Usage Guide

Skills are **model-invoked**—Claude automatically uses them based on context. You can also invoke them explicitly using `/skill-name` or by asking Claude to use a specific skill.

### Interview Skill

**Best for:** Planning features, writing specs, fleshing out ideas, requirements gathering

```
I want to build a caching layer for our API - can you help me spec this out?
```

Or invoke directly:
```
/interview
```

**What to expect:**
1. **Research Phase** — Claude does BLOCKING research on your codebase and technologies before asking questions
2. **Devil's Advocate Phase** — Claude challenges your idea: Does this need to exist? Is there a library? What could fail?
3. **Deep Interview Phase** — Once the idea passes challenge, Claude becomes a collaborative partner, asking detailed questions while fact-checking in the background
4. **Output** — A self-contained spec with Problem Statement, Objective, Success Criteria, Interview Record (Q&A), and any corrected assumptions

**Key features:**
- Always verifies technology assumptions against current docs (training data may be stale)
- Surfaces contradictions between your claims and research findings
- Captures Q&A in the spec so future Claude instances can implement without asking questions

### Systematic Debugging Skill

**Best for:** Any bug, test failure, or unexpected behavior - BEFORE attempting fixes

```
This test is failing and I don't know why
```

Or when you've already tried fixes:
```
I've tried 3 fixes and nothing is working
```

**The Iron Law:** No fixes without root cause investigation first.

**Four phases:**
1. **Root Cause Investigation** — Read errors, reproduce, trace data flow
2. **Pattern Analysis** — Find working examples, compare differences
3. **Hypothesis Testing** — Single hypothesis, minimal change, verify
4. **Implementation** — Failing test first, single fix, verify

**Key features:**
- Stops "quick fix" instinct that causes thrashing
- After 3+ failed fixes, questions architecture instead of attempting more fixes
- Integrates with test-driven-development and root-cause-tracing skills

### Testing Anti-Patterns Skill

**Best for:** Writing tests, adding mocks, or when tempted to add test-only methods

```
I need to write tests for this component
```

Or when tests are getting complex:
```
My test mocks are getting really complicated
```

**The Iron Laws:**
1. NEVER test mock behavior
2. NEVER add test-only methods to production classes
3. NEVER mock without understanding dependencies

**Catches common mistakes:**
- Asserting on mock elements instead of real behavior
- Adding `destroy()` methods only used in tests
- Over-mocking that breaks test logic
- Incomplete mocks that hide bugs

### Setup Linter Skill

**Best for:** Setting up automatic code linting/formatting when Claude finishes writing code

```
Set up automatic linting for this project
```

Or invoke directly:
```
/setup-linter
```

**What it does:**
1. Auto-detects your project type (JS/TS, Python, Rust, Go, Deno)
2. Installs the appropriate linter if not present
3. Creates config files with sensible defaults
4. Sets up a Stop hook so linting runs automatically after every Claude response

**Supported projects:**
- JavaScript/TypeScript → ESLint (with React detection)
- Python → Ruff
- Rust → rustfmt + clippy
- Go → golangci-lint
- Deno → built-in lint/fmt

### Prompt Craft Skill

**Best for:** Improving prompts, learning prompting techniques, writing prompts for LLMs

```
Help me improve this prompt: "Write a blog post about AI"
```

Or ask for a specific mode:
```
Analyze this prompt and tell me what's weak about it
```

### Authoring Skills Skill

**Best for:** Creating new Claude Code skills, understanding plugin architecture, configuring triggers and hooks

```
I want to create a new Claude Code skill for database migrations
```

### Hormozi Pitch Skill

**Best for:** Creating offers, pricing strategies, marketing copy, value propositions

```
I need to create a compelling offer for my SaaS product
```

### X Post Writer Skill

**Best for:** Twitter/X content, social media copywriting, viral hooks

```
Write a Twitter thread about automation workflows
```

---

## Skill Details

### interview

A rigorous interview system that produces implementation-ready specs:

**Two-Phase Identity:**
- **Critical Challenger (Phases 1-2)** — Skeptical, probing. Challenges the idea's right to exist. Uses BLOCKING research.
- **Expert Partner (Phase 3+)** — Collaborative, thorough. Helps refine implementation. Uses BACKGROUND research.

**Research Protocol:**
- Pre-challenge: BLOCKING research on codebase, technologies, existing solutions
- During interview: BACKGROUND research to verify claims asynchronously
- Pre-output: Verification research to ensure spec accuracy

**Output includes:**
- Problem Statement, Objective, Success Criteria
- Interview Record (Q&A that led to decisions)
- Assumption Corrections (what user/Claude got wrong)
- Edge Cases, Tradeoffs, Open Questions (when relevant)

### systematic-debugging

Four-phase framework that ensures understanding before fixes:

**The Four Phases:**
| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Root Cause** | Read errors, reproduce, check changes, gather evidence | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare | Identify differences |
| **3. Hypothesis** | Form theory, test minimally | Confirmed or new hypothesis |
| **4. Implementation** | Create test, fix, verify | Bug resolved, tests pass |

**Key rules:**
- No fixes without completing Phase 1
- One variable at a time in Phase 3
- If 3+ fixes failed → question architecture, don't attempt fix #4
- 95% of "no root cause" cases are incomplete investigation

**Red flags that trigger this skill:**
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- Each fix reveals new problem in different place

### testing-anti-patterns

Prevents common testing mistakes that cause false confidence:

**Anti-patterns caught:**
| Anti-Pattern | What's Wrong | Fix |
|--------------|--------------|-----|
| Testing mock behavior | Verifies mock exists, not real behavior | Test real component or unmock |
| Test-only production methods | Pollutes production with test code | Move to test utilities |
| Mocking without understanding | Over-mocking breaks test logic | Understand dependencies first |
| Incomplete mocks | Partial mocks hide structural assumptions | Mirror real API completely |
| Tests as afterthought | Can't claim complete without tests | TDD - tests first |

**Gate functions:** Each anti-pattern has a "gate function" - questions to ask BEFORE taking action that would introduce the anti-pattern.

### setup-linter

Automated linting setup with Stop hook integration:

**Auto-detection:**
| Project | Detection | Linter | Config Created |
|---------|-----------|--------|----------------|
| JavaScript/React | `package.json` | ESLint | `eslint.config.js` |
| Python | `pyproject.toml`, `*.py` | Ruff | `ruff.toml` |
| Rust | `Cargo.toml` | rustfmt + clippy | (built-in) |
| Go | `go.mod` | golangci-lint | (optional) |
| Deno | `deno.json` | deno lint/fmt | (built-in) |

**Features:**
- Detects package manager (yarn, pnpm, bun, npm)
- Detects React projects and adds react-hooks plugin
- Creates flat config format for ESLint
- Hook runs `<linter> 2>&1 || true` (never blocks Claude)

### authoring-skills

Complete guide for creating Claude Code skills and plugins:
- SKILL.md best practices (conciseness, 500-line rule, progressive disclosure)
- Plugin development (directory structure, manifests, distribution)
- Trigger configuration (keywords, intent patterns, file paths)
- Hook architecture (PreToolUse, PostToolUse, SessionStart)
- Testing and troubleshooting workflows

### prompt-craft

**19 research-backed prompting techniques** (10 core + 9 extended) with measured impact metrics.

**Core techniques:**
Chain-of-Thought (+40%), Structured Output (99%+), Few-Shot Examples (+15-30%), Placement (+50%), Salience (+23-31%), Roles (+10-20%), Positive Framing (+15-20%), Reasoning-First (-20-30% hallucination), Verbalized Sampling (+1.6-2.1x), Self-Reflection (+15-25%)

**Extended techniques:**
Decomposition, Compression, Sufficiency, Scope, Format-Spec, Uncertainty, Chaining, Self-Consistency, Tree-of-Thoughts

**Model-specific guidance:**
Includes tailored prompting strategies for Claude, OpenAI (GPT-4o, o1/o3), DeepSeek R1, Gemini 3, Kimi K2, Qwen 2.5, and Grok.

### hormozi-pitch

Alex Hormozi's $100M Offers methodology:
- **Value Equation**: Dream Outcome × Perceived Likelihood / Time Delay × Effort
- **MAGIC Naming**: Compelling product/service names
- **Guarantee Types**: Unconditional, conditional, anti-guarantee, implied
- **Value Stacking**: Justify any price point

### x-post-writer

Twitter/X copywriting expertise:
- Hook fundamentals and patterns
- Engagement triggers (social proof, urgency, exclusivity)
- High-performing examples (100K+ views)
- Before/after editing feedback

---

## Managing Plugins

```bash
# Disable without uninstalling
/plugin disable ajbm-dev@ajbm
/plugin disable ajbm-business@ajbm

# Re-enable
/plugin enable ajbm-dev@ajbm
/plugin enable ajbm-business@ajbm

# Completely remove
/plugin uninstall ajbm-dev@ajbm
/plugin uninstall ajbm-business@ajbm

# Update to latest version
/plugin marketplace update ajbmachon
/plugin uninstall ajbm-dev@ajbm
/plugin install ajbm-dev@ajbm
```

---

## Tips for Best Results

### Interview Skill
- **Provide context upfront** — The more detail in your initial message, the smarter Claude's research and challenges will be
- **Defend your ideas** — When Claude challenges, explain your reasoning. Ideas that survive become stronger specs
- **Trust the research** — If Claude says "I found library X that does this," consider it seriously
- **Review the spec** — The Interview Record should capture your key decisions. If something's missing, ask to add it

### Debugging & Testing Skills
- **Use systematic-debugging BEFORE attempting fixes** — Even if the fix seems obvious, the process is fast and prevents thrashing
- **If 3+ fixes failed, stop** — This signals an architectural problem, not a bug. Question the pattern.
- **Run tests with real implementations first** — Before mocking, see what actually needs to happen
- **Gate functions prevent mistakes** — Ask the questions before adding mocks or test methods

### General
- **Let skills activate naturally** — You don't need to explicitly invoke skills; Claude uses them based on context
- **Combine skills** — You can use interview to spec a feature, then prompt-craft to write prompts for that feature
- **Check for updates** — Skills improve over time. Run `/plugin marketplace update` periodically

---

## Contributing

Contributions welcome! When adding or modifying skills:

1. Follow the 500-line rule for SKILL.md files
2. Use progressive disclosure (reference files for details)
3. Write specific descriptions with trigger keywords
4. Test with 3+ real scenarios before committing
5. Use `<mandatory_read>` blocks for critical reference files

---

## License

MIT

## Author

Andre Machon ([@ajbmachon](https://github.com/ajbmachon))
