# FlowConAI Skills

A collection of generally useful Claude Code skills that work across all Anthropic surfaces. These skills are not workflow-specific—they're universal productivity boosters for anyone using Claude Code.

## Skills Included

| Skill | Description |
|-------|-------------|
| **authoring-skills** | Best practices for writing SKILL.md files—covers conciseness, progressive disclosure, naming conventions, and the 500-line rule |
| **hormozi-pitch** | Alex Hormozi's $100M Offers methodology for creating irresistible offers, pricing, guarantees, and value propositions |
| **prompt-craft** | Research-backed prompt engineering with 10 core techniques. Modes: Analyze, Craft, Teach, Quick Fix |
| **skill-developer** | Complete guide for creating Claude Code skills—triggers, hooks, enforcement levels, and Anthropic best practices |
| **x-post-writer** | Twitter/X copywriting system for high-engagement social media content with viral frameworks and examples |

## Installation

### Prerequisites

- Claude Code installed (`npm install -g @anthropic-ai/claude-code` or via the [official installer](https://docs.anthropic.com/en/docs/claude-code/quickstart))
- Basic familiarity with Claude Code CLI

### Option 1: Install from GitHub (Recommended)

```bash
# Start Claude Code
claude

# Add the marketplace
/plugin marketplace add andremachon/claude-skills

# Install the plugin
/plugin install flowconai-skills@claude-skills
```

After installation, restart Claude Code to activate the skills.

### Option 2: Install from Local Clone

```bash
# Clone the repository
git clone https://github.com/andremachon/claude-skills.git

# Start Claude Code
claude

# Add as local marketplace
/plugin marketplace add ./claude-skills

# Install the plugin
/plugin install flowconai-skills@claude-skills
```

### Verify Installation

After restarting Claude Code:

```bash
# Check available commands
/help

# Ask Claude about available skills
What skills are available?
```

## Usage

Skills are **model-invoked**—Claude automatically uses them based on context. You don't need to explicitly call them.

### Examples

**Prompt engineering help:**
```
Help me improve this prompt: "Write a blog post about AI"
```
→ Claude uses `prompt-craft` to analyze and enhance your prompt

**Creating offers:**
```
I need to create a compelling offer for my SaaS product
```
→ Claude uses `hormozi-pitch` to guide you through the Value Equation

**Writing tweets:**
```
Write a Twitter thread about automation workflows
```
→ Claude uses `x-post-writer` with viral copywriting frameworks

**Building skills:**
```
I want to create a new Claude Code skill for database migrations
```
→ Claude uses `skill-developer` for structure and best practices

## Skill Details

### authoring-skills

Condensed best practices from Anthropic's official skill authoring guide:
- Conciseness principles (context window is shared)
- YAML frontmatter conventions
- Progressive disclosure patterns
- Quality checklist for skills

### hormozi-pitch

Alex Hormozi's $100M Offers methodology:
- **Value Equation**: Dream Outcome × Perceived Likelihood / Time Delay × Effort
- **MAGIC Naming**: Compelling product/service names
- **Guarantee Types**: Unconditional, conditional, anti-guarantee, implied
- **Value Stacking**: Justify any price point

### prompt-craft

10 core prompting techniques with research-backed impact metrics:
1. Chain-of-Thought (+40% accuracy)
2. Structured Output (99%+ compliance)
3. Few-Shot Examples (+15-30% specificity)
4. Placement (+50% retrieval)
5. Salience (+23-31% compliance)
6. Roles (+10-20% domain accuracy)
7. Positive Framing (+15-20% compliance)
8. Reasoning-First (-20-30% hallucination)
9. Verbalized Sampling (+1.6-2.1x diversity)
10. Self-Reflection (+15-25% accuracy)

### skill-developer

Complete skill development guide:
- Two-hook architecture (UserPromptSubmit, PostToolUse)
- Trigger types (keywords, intent patterns, file paths, content)
- Enforcement levels (block, suggest, warn)
- Testing and debugging workflows

### x-post-writer

Twitter/X copywriting expertise:
- Hook fundamentals and patterns
- Engagement triggers (social proof, urgency, exclusivity)
- High-performing examples (100K+ views)
- Before/after editing feedback

## Managing the Plugin

```bash
# Disable without uninstalling
/plugin disable flowconai-skills@claude-skills

# Re-enable
/plugin enable flowconai-skills@claude-skills

# Completely remove
/plugin uninstall flowconai-skills@claude-skills

# Update marketplace (fetch latest)
/plugin marketplace update claude-skills
```

## Contributing

Contributions welcome! When adding or modifying skills:

1. Follow the 500-line rule for SKILL.md files
2. Use progressive disclosure (reference files for details)
3. Write specific descriptions with trigger keywords
4. Test with 3+ real scenarios before committing

## License

MIT

## Author

Andre Machon ([@andremachon](https://github.com/andremachon))
