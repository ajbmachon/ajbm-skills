# Cursor and Windsurf Rules Patterns Research

**Research Date:** 2026-02-02
**Researcher:** Ava Sterling (Claude Researcher)

---

## Executive Summary

This research documents best practices, patterns, and anti-patterns for AI coding assistant rules systems, focusing on Cursor and Windsurf. Key findings include a taxonomy from academic research, context engineering strategies, the "linter over guide" principle, and incremental rule adoption patterns.

---

## 1. Academic Taxonomy of Rules (MSR '26 Study)

**Source:** [Beyond the Prompt: An Empirical Study of Cursor Rules](https://arxiv.org/abs/2512.18925)

The first large-scale empirical study of 401 open-source repositories identified five high-level themes that developers consider essential for LLM-powered coding assistants.

### 1.1 Five Core Categories

| Category | Prevalence | Description |
|----------|------------|-------------|
| **Guidelines** | 89% | Quality assurance, testing, debugging, error handling, modularity |
| **Project Information** | 85% | Tech stack, architecture, build commands, functionality |
| **Conventions** | 84% | Code style, naming, formatting, directory structure |
| **LLM Directives** | 50% | Behavior instructions, workflow, persona, output formatting |
| **Examples** | 50% | Demonstrations, templates, code snippets |

### 1.2 Detailed Sub-Categories

**Project Information:**
- Environment: Technology stack, libraries, build/test commands
- Functionality: Architecture, purpose, component descriptions
- Change: Recent updates, deprecated features

**Conventions:**
- Code Style: Naming, formatting, stylistic choices
- Language/Framework: Idioms, patterns, preferred constructs
- Structure: Directory organization, file naming

**Guidelines:**
- Quality Assurance: Testing, debugging, error handling
- General Programming: Modularity, separation of concerns
- Communication: Documentation, commit messages
- Performance, Consistency, UI, Security, Dependency management

**LLM Directives:**
- Behavior: How models should respond, verification steps
- Workflow: Multi-step processes, conditional sequences
- Persona: Adopting specific roles
- Formatting & Granularity: Output structure and detail level

### 1.3 Key Statistics

- **37.16%** of repositories include all four core content categories
- **28.70%** line duplication rate across repositories (indicating common patterns)
- **80.55%** contain 3-15 unique context codes
- Dynamic languages (PHP, JavaScript) receive more context than statically typed (Go, Java)

### Application to Claude Code Skills

> Write SKILL.md files that address all five categories: provide project context, establish conventions, include actionable guidelines, add LLM-specific directives, and include concrete examples. The taxonomy shows what developers actually need from AI assistants.

---

## 2. Rule Maturity Framework

While no formal "four-level maturity framework" exists in the community, several progression models emerged from the research.

### 2.1 Google's Four-Phase Framework

**Source:** [How to adopt Gemini Code Assist](https://cloud.google.com/blog/products/application-development/how-to-adopt-gemini-code-assist-and-measure-its-impact)

| Phase | Focus | Timeframe |
|-------|-------|-----------|
| **Adoption** | Evaluation and proof of concept | Weeks 1-2 |
| **Trust** | Establish confidence in AI output | Weeks 3-4 |
| **Acceleration** | Assess speed improvements | Weeks 5-6 |
| **Impact** | Confirm business performance gains | Weeks 6-8+ |

### 2.2 AI Development Maturity Model (AIDMM)

**Source:** [AI Development Maturity Model](https://dev.to/ggondim/ai-development-maturity-model-4i47)

Five levels from purely human to fully autonomous AI-driven codebases:
1. **Manual** - Human coding with no AI assistance
2. **Assisted** - AI suggestions, human writes
3. **Collaborative** - AI generates, human reviews
4. **Orchestrated** - Human directs, AI executes
5. **Autonomous** - AI-driven with human oversight

### 2.3 GitHub AI Maturity Model

**Source:** [AI-Maturity-Model](https://github.com/Gigacore/AI-Maturity-Model)

Six core dimensions:
- Skills, Processes, Platforms, Governance, Collaboration, Outcomes

Five maturity levels:
1. **Exploratory** - Unstructured, individual experiments
2. **Pilot** - Team-level pilots with some guidelines
3. **Scaling** - Standardization and governance frameworks
4. **Optimizing** - Metrics-driven refinement
5. **Transformational** - AI fully integrated into workflows

### Application to Claude Code Skills

> Design skills with a maturity progression in mind. Start with basic guidance, allow teams to customize, provide hooks for measurement, and build toward full automation. Consider creating "starter" and "advanced" versions of complex skills.

---

## 3. Context Engineering Strategies

### 3.1 Cursor's Official Approach

**Source:** [Cursor Working with Context](https://docs.cursor.com/guides/working-with-context)

**Core Principle:** Context = Intent (what you want) + State (what exists)

**Best Practices:**
- Use surgical context with @-symbols (@code, @file, @folder)
- Let agents discover context autonomously through grep and semantic search
- Start new conversations when switching tasks
- Long conversations accumulate noise; reset when effectiveness decreases

**Quote:** "Think of rules as long-term memory that you want you or other members of your team to have access to."

### 3.2 Rules as Encyclopedia Articles

**Source:** [9 Lessons From Cursor's System Prompt](https://byteatatime.dev/posts/cursor-prompt-analysis/)

**Key Insight:** Rules are not appended to the system prompt. The LLM sees a list of names and descriptions and can make tool calls to fetch_rules() to read content.

**Implication:** "Your mindset should be writing rules as encyclopedia articles rather than commands."

### 3.3 Context Chunk Management

**Source:** [How Cursor (AI IDE) Works](https://blog.sshh.io/p/how-cursor-ai-ide-works)

Cursor's read_file tool views 250 lines maximum, 200 lines minimum. This manages:
- LLM context window limits
- Cognitive load on the model
- Relevance of information

### 3.4 Windsurf's Memory System

**Source:** [Windsurf Memories Documentation](https://docs.windsurf.com/windsurf/cascade/memories)

| Memory Type | Source | Scope | Cost |
|-------------|--------|-------|------|
| Auto Memories | Cascade generates | Workspace only | Free |
| User Memories | User prompts | Workspace only | Free |
| Global Rules | global_rules.md | All workspaces | Free |
| Workspace Rules | .windsurf/rules/ | Current workspace | Free |

### Application to Claude Code Skills

> Structure skills as reference documents that can be fetched on demand, not as massive prompts. Use clear headers and sections so agents can navigate to relevant content. Keep individual sections focused and under 500 lines.

---

## 4. Linter-Over-Guide Pattern

### 4.1 The Core Principle

**Source:** [Making AI Code Consistent with Linters](https://dev.to/fhaponenka/making-ai-code-consistent-with-linters-27pl)

**Key Quote:** "The difference is critical: AI can choose to ignore documentation, but it cannot ignore linting errors in your CI pipeline."

### 4.2 Why Enforcement Works Better

| Approach | Enforcement | Consistency | Feedback Speed |
|----------|-------------|-------------|----------------|
| Documentation | Suggestions only | Variable | Manual review |
| Linting | Hard blocks | Uniform | Instant |

**Benefits of automated enforcement:**
- Instant feedback (seconds, not days)
- Consistency across all developers and AI
- Rules enforced uniformly in CI pipeline

### 4.3 Cursor's Official Guidance

**Source:** [Cursor Agent Best Practices](https://cursor.com/blog/agent-best-practices)

**Anti-Pattern:** "Copying entire style guides (use linters instead)"

**Best Practice:** "Develop verification signals through typed languages, linters, and comprehensive tests so agents know when changes succeed."

### 4.4 Implementation Strategy

**Source:** [Ship Clean Code Faster](https://newmathdata.com/blog/cursor-ai-coding-guide-speed-quality-guardrails/)

> "Cursor can 2x your delivery speed if you install hard guardrails. This guide shows how rule files, checkpoint-and-restore, test-driven development, and ruthless pruning let you bank that speed without inflating technical debt."

### Application to Claude Code Skills

> The setup-linter skill embodies this pattern perfectly. Prefer automated enforcement over documentation. Skills should configure tools (linters, formatters, pre-commit hooks) rather than just describe best practices. If a rule can be enforced automatically, it should be.

---

## 5. Rules Incrementalism

### 5.1 The "Start Small" Principle

**Source:** [Cursor Agent Best Practices](https://cursor.com/blog/agent-best-practices)

**Official Guidance:** "Start simple. Add rules only when you notice the agent making the same mistake repeatedly."

**Quote:** "Over-thinking rules initially is unnecessary, as Cursor's models already possess vast knowledge."

### 5.2 Incremental Adoption Pattern

**Source:** Multiple forum posts and guides

**Process:**
1. Begin with no custom rules (rely on model knowledge)
2. Observe agent mistakes in real usage
3. Add a rule when the same mistake occurs twice
4. Review and prune rules periodically
5. Check rules into git for team-wide benefits

### 5.3 Rule Evolution Over Time

**Source:** [MSR '26 Study](https://arxiv.org/abs/2512.18925)

**Finding:** Newly created repositories (within 7 months) provide less context overall. Older repositories show declining LLM-specific instructions, suggesting developers initially prioritize documentation over LLM-targeted guidance.

**Implication:** Rules should evolve with the project, not be created upfront.

### 5.4 Avoiding "Context Rot"

**Source:** [Cursor Rules Best Practices](https://cursor.fan/tutorial/HowTo/using-cursor-rules-effectively/)

> "Rules can become stale as your project evolves. Schedule periodic reviews to remove outdated instructions or links to avoid 'context rot' and ensure the AI remains focused."

### Application to Claude Code Skills

> Skills should be minimal by default and grow based on real needs. The authoring-skills guideline of "under 500 lines" enforces this. Consider creating "core" and "extended" versions of skills. Include instructions for when to add custom rules rather than providing everything upfront.

---

## 6. Trigger/Activation Patterns

### 6.1 Cursor Rule Types

**Source:** [Cursor Rules Documentation](https://docs.cursor.com/context/rules)

| Type | Trigger | Use Case |
|------|---------|----------|
| **Always** | `alwaysApply: true` | Universal project rules |
| **Auto-Attach** | File matches glob pattern | File-type specific rules |
| **Agent Requested** | AI decides based on description | Context-dependent rules |
| **Manual** | Explicit @-mention | Specialized rules |

### 6.2 MDC Frontmatter Structure

```yaml
---
description: "Rule description for AI to read (max 1024 chars)"
globs: ["src/**/*.ts", "tests/**/*.ts"]
alwaysApply: false
---
```

### 6.3 Windsurf Activation Modes

**Source:** [Windsurf Memories Documentation](https://docs.windsurf.com/windsurf/cascade/memories)

| Mode | Description |
|------|-------------|
| **Manual** | Activated via @mention |
| **Always On** | Always applied |
| **Model Decision** | AI decides based on natural language description |
| **Glob** | Applied to files matching pattern |

### 6.4 Glob Pattern Best Practices

**Source:** [Cursor Forum Discussions](https://forum.cursor.com/t/correct-way-to-specify-rules-globs/71752)

- Use YAML arrays: `globs: ['src/**/*.ts', 'tests/**/*.ts']`
- Rules only trigger when files are opened or referenced in chat
- Don't combine globs and description in the same rule

**Key Insight:** "If no file is opened - or the file isn't part of the workspace - glob-matching rules won't activate."

### Application to Claude Code Skills

> Skills should have clear trigger descriptions. Use the "USE WHEN" prefix pattern for clarity. The description field is how Claude Code discovers skills - make it specific with keywords that match user intent. Consider file-type triggers for language-specific guidance.

---

## 7. Common Anti-Patterns

### 7.1 Rules That Are Too Obvious

**Source:** [Cursor Rules Best Practices](https://cursor.fan/tutorial/HowTo/using-cursor-rules-effectively/)

**Avoid:**
- "Write readable code"
- "Use meaningful variable names"
- "Add comments when necessary"
- "Follow best practices"
- "Use design patterns"

**Why:** These are already baked into model training.

### 7.2 Rules That Are Too Restrictive

**Source:** [Cursor Rules Guide](https://cursorrules.org/article)

**Avoid:**
- "Never use any third-party libraries"
- "Always write everything from scratch"
- "Every function must be under 5 lines"

### 7.3 Providing Identity in Rules

**Source:** [9 Lessons From Cursor's System Prompt](https://byteatatime.dev/posts/cursor-prompt-analysis/)

**Anti-Pattern:** "Do not provide an identity in the rule like 'You are a senior frontend engineer that is an expert in typescript' like you may find in cursor.directory. This might look like it works but is weird for the agent to follow when it already has an identity provided by the built-in prompts."

### 7.4 Copying File Contents

**Source:** [Cursor Agent Best Practices](https://cursor.com/blog/agent-best-practices)

**Anti-Pattern:** "Copying entire style guides (use linters instead)"

**Anti-Pattern:** "Keeping rules stale by copying code instead of referencing files"

**Better:** Reference files by path so rules stay in sync.

### 7.5 Using Deprecated Formats

**Source:** [Cursor Forum](https://forum.cursor.com/t/you-re-using-cursor-rules-the-wrong-way/62530)

**.cursorrules is deprecated** in favor of .mdc rules in .cursor/rules/ directory.

### 7.6 Not Updating Rules

**Source:** [Cursor Rules Best Practices](https://cursor.fan/tutorial/HowTo/using-cursor-rules-effectively/)

- Rules become stale as projects evolve
- Schedule periodic reviews
- Remove outdated instructions
- Keep rules aligned with project evolution

### 7.7 Over-Optimizing Too Early

**Source:** [Cursor Agent Best Practices](https://cursor.com/blog/agent-best-practices)

**Anti-Pattern:** "Adding instructions for rarely-occurring edge cases"

**Better:** "Add rules only when you notice the agent making the same mistake repeatedly."

### Application to Claude Code Skills

> Avoid generic advice in skills. Don't provide identities (Claude Code has its own). Reference files instead of copying content. Keep skills actionable and specific. Include anti-patterns in skill documentation to prevent common mistakes. Design for evolution, not perfection on day one.

---

## 8. Community Resources

### 8.1 Cursor Resources

| Resource | URL | Description |
|----------|-----|-------------|
| **Cursor Directory** | [cursor.directory](https://cursor.directory/) | Community rules collection |
| **awesome-cursorrules** | [GitHub](https://github.com/PatrickJS/awesome-cursorrules) | 879+ rule templates |
| **awesome-cursor-rules-mdc** | [GitHub](https://github.com/sanjeed5/awesome-cursor-rules-mdc) | MDC format collection |
| **dotCursorRules** | [dotcursorrules.com](https://dotcursorrules.com/) | Curated rules |
| **Cursor Forum** | [forum.cursor.com](https://forum.cursor.com/) | Community discussions |

### 8.2 Windsurf Resources

| Resource | URL | Description |
|----------|-----|-------------|
| **Windsurf Rules Directory** | [windsurf.com/editor/directory](https://windsurf.com/editor/directory) | Official templates |
| **awesome-windsurfrules** | [GitHub](https://github.com/balqaasem/awesome-windsurfrules) | Community collection |
| **Windsurf University** | [windsurf.com/university](https://windsurf.com/university) | Official tutorials |

### 8.3 Cross-Platform Resources

| Resource | URL | Description |
|----------|-----|-------------|
| **vibe-coding-ai-rules** | [GitHub](https://github.com/obviousworks/vibe-coding-ai-rules) | Works with both |
| **rules-for-ai** | [GitHub](https://github.com/hashiiiii/rules-for-ai) | Windsurf + Cursor |

---

## 9. Cursor vs Windsurf Comparison

| Feature | Cursor | Windsurf |
|---------|--------|----------|
| **Rule Location** | .cursor/rules/*.mdc | .windsurf/rules/ |
| **Global Rules** | User settings | global_rules.md |
| **Rule Format** | MDC with YAML frontmatter | Markdown |
| **Activation Types** | Always, Auto-Attach, Agent, Manual | Always On, Glob, Model Decision, Manual |
| **Memory System** | Memories via /Generate | Auto + User memories |
| **Context Persistence** | Per-chat | Flows (persistent sessions) |
| **Workflows** | Slash commands + Skills | Workflows feature |

---

## 10. Summary: Best Practices for Claude Code Skills

Based on this research, here are the key takeaways for authoring Claude Code skills:

### Do:

1. **Structure skills around the five taxonomy categories** - Project info, conventions, guidelines, LLM directives, examples
2. **Start minimal and iterate** - Add guidance when you see repeated mistakes
3. **Prefer automated enforcement** - Linters over documentation
4. **Write clear trigger descriptions** - Use "USE WHEN" prefix pattern
5. **Keep skills under 500 lines** - Reference files for details
6. **Include concrete examples** - Good and bad patterns
7. **Design for evolution** - Rules should grow with projects
8. **Reference files, don't copy** - Keeps content in sync

### Don't:

1. **Don't include obvious advice** - "Write good code" is already known
2. **Don't provide identity** - Claude has its own
3. **Don't over-optimize early** - Wait for real problems
4. **Don't copy style guides** - Use linters instead
5. **Don't use deprecated formats** - Stay current with tooling
6. **Don't forget maintenance** - Review and prune periodically
7. **Don't be too restrictive** - Allow agent flexibility
8. **Don't dump everything in one file** - Use modular organization

---

## Sources

### Academic

- [Beyond the Prompt: An Empirical Study of Cursor Rules (MSR '26)](https://arxiv.org/abs/2512.18925)

### Official Documentation

- [Cursor Rules Documentation](https://docs.cursor.com/context/rules)
- [Cursor Agent Best Practices](https://cursor.com/blog/agent-best-practices)
- [Cursor Working with Context](https://docs.cursor.com/guides/working-with-context)
- [Windsurf Memories Documentation](https://docs.windsurf.com/windsurf/cascade/memories)
- [Windsurf Getting Started](https://docs.windsurf.com/windsurf/getting-started)

### Community Guides

- [How to Write Great Cursor Rules (Trigger.dev)](https://trigger.dev/blog/cursor-rules)
- [9 Lessons From Cursor's System Prompt](https://byteatatime.dev/posts/cursor-prompt-analysis/)
- [How Cursor (AI IDE) Works](https://blog.sshh.io/p/how-cursor-ai-ide-works)
- [Using Windsurf Rules, Workflows, and Memories](https://www.paulmduvall.com/using-windsurf-rules-workflows-and-memories/)
- [Ship Clean Code Faster](https://newmathdata.com/blog/cursor-ai-coding-guide-speed-quality-guardrails/)

### Community Resources

- [Cursor Directory](https://cursor.directory/)
- [awesome-cursorrules (GitHub)](https://github.com/PatrickJS/awesome-cursorrules)
- [Windsurf Rules Directory](https://windsurf.com/editor/directory)
- [Cursor Forum](https://forum.cursor.com/)

### Maturity Models

- [AI-Maturity-Model (GitHub)](https://github.com/Gigacore/AI-Maturity-Model)
- [AI Development Maturity Model](https://dev.to/ggondim/ai-development-maturity-model-4i47)
- [Google: How to adopt Gemini Code Assist](https://cloud.google.com/blog/products/application-development/how-to-adopt-gemini-code-assist-and-measure-its-impact)

---

*Research conducted using Claude's WebSearch and Exa MCP tools. Strategic analysis by Ava Sterling.*
