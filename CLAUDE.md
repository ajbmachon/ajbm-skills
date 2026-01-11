# AJBM Skills for Claude Code

A collection of generally useful Claude Code skills that work across all Anthropic surfaces.

**Plugin names:** `ajbm-dev`, `ajbm-business`
**Install:** `/plugin install ajbm-dev@ajbm`

## Quick Reference

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
Claude, OpenAI (GPT-4o, o1/o3), DeepSeek R1, Gemini 3, Kimi K2, Qwen 2.5, Grok

### skill-developer

Use when creating Claude Code skills, hooks, or triggers.

**Two-Hook Architecture:**
- **UserPromptSubmit**: Proactive suggestions before Claude sees prompt
- **PostToolUse**: Gentle reminders after tool execution

**Skill structure:**
```
skill-name/
├── SKILL.md              # Main (loaded when triggered)
├── reference.md          # Loaded as needed
└── scripts/
    └── helper.py         # Executed, not loaded
```

**Enforcement levels:**
- **BLOCK**: Exit code 2, critical only
- **SUGGEST**: Inject context, most common
- **WARN**: Advisory, rarely used

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
