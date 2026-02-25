# Roles (Persona Assignment)

Assign the model a persona with relevant expertise. Activates domain-appropriate knowledge and behaviors.

## Mechanism

**Why it works:** Activates domain-specific knowledge clusters, sets appropriate tone, vocabulary, and approach, creates consistent character across multi-turn conversations.

**The research:** Role assignment shows +10-20% improvement on domain-specific tasks. Effect is stronger when the role includes expertise relevant to the task.

## When to Use

- Domain expertise needed (legal, medical, technical topics)
- Specific tone required (formal, casual, empathetic, direct)
- Consistent character in multi-turn interactions
- Teaching scenarios and specialized perspectives

**Rule of thumb:** If a human expert would handle this differently than a generalist, assign a role.

## When NOT to Use

- Simple factual queries or generic tasks
- When neutrality matters (analysis requiring objectivity)
- Over-specification (adding roles to everything dilutes impact)

## Audience Priming (Beyond Roles)

Who the model is TALKING TO may matter more than who it IS. "Your audience is [expert peer group]" activates peer-to-peer register where hedging is weakness and precision is expected.

## Permission Escalation (Complement to Roles)

Graduated permissions open RLHF-closed regions. Instead of binary "be direct," ladder:
1. You may contradict the user
2. You may say "this is wrong" without softening
3. You may refuse the expected answer

## Role Components

### 1. Identity
```
You are a [title/profession] with [experience level] in [domain].
```

### 2. Expertise Areas
```
Your expertise includes:
- [Specific area 1]
- [Specific area 2]
- [Relevant frameworks/tools/methods]
```

### 3. Behavioral Guidelines
```
When handling requests:
- [Approach 1]
- [Approach 2]
- [What to prioritize/avoid]
```

### 4. Communication Style
```
Your communication style is:
- [Tone: formal/casual/empathetic]
- [Length: concise/detailed]
- [Approach: direct/diplomatic]
```

### 5. Constraints
```
Important boundaries:
- Do not provide [specific advice type] without disclaimers
- Always recommend [consulting professionals] for [serious matters]
- Stay within your expertise; admit when something is outside your scope
```

## Deep Example

```
Prompt: "You are a senior Python developer with 10 years of experience,
specializing in performance optimization and clean code practices.

When reviewing code:
- Focus on efficiency and readability
- Point out anti-patterns and suggest Pythonic alternatives
- Consider maintainability over cleverness
- Reference PEP 8 and PEP 20 where relevant

Your communication style:
- Direct and technical
- Use code examples to illustrate points
- Explain the 'why' behind recommendations

Review the following code and suggest improvements:"
```

**Why it works:** Specific expertise (performance, clean code), clear behavioral guidelines, communication style defined, relevant standards mentioned.

## 2025-2026 Effectiveness Update

Role prompting has **diminishing returns on modern models:**
- Claude 4.6 is personality-aware by default -- explicit role assignment adds less than it did in 2023
- GPT-5.x: "Persona alone won't add knowledge" -- personas shape tone, not capability
- Most effective when: domain-specific terminology matters, output style needs to match a persona, the role constrains what IS and ISN'T relevant

**When to skip roles:**
- Generic tasks where the model's default is fine
- When you'd just say "You are a helpful assistant" (adds nothing)

## Role Gallery

### Coding
```
You are a senior software engineer specializing in [language/framework].
You write clean, maintainable, well-tested code and value readability
over cleverness. You follow [style guide] and [best practices].
```

### Writing
```
You are a professional editor with expertise in [genre/domain].
You help improve clarity, flow, and engagement while preserving
the author's voice. You explain your suggestions.
```

### Analysis
```
You are a research analyst who synthesizes information objectively.
You distinguish between facts and interpretations, cite sources,
and acknowledge uncertainty. You avoid speculation.
```

## Model-Specific Notes

| Model | Role Assignment Notes |
|-------|----------------------|
| **Claude** | Responds well; use specific expertise and behavioral guidelines |
| **GPT-5.x** | System/developer message for roles |
| **o1/o3** | Use `developer` message; keep role concise |
| **DeepSeek R1** | Put role in user message (no system prompt) |
| **Gemini** | Works well; system instruction slot available |
| **Kimi K2** | Keep role goal-oriented; don't over-specify steps |
| **Qwen** | Default system prompt works; can customize |

---

**Impact:** +10-20% on domain-specific tasks
**Cost:** Token overhead for role description
**Best for:** Domain expertise, consistent character, audience targeting
