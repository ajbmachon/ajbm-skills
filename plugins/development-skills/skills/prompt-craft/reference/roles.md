# Roles (Persona Assignment)

Assign the model a persona with relevant expertise. Activates domain-appropriate knowledge and behaviors.

## Table of Contents
1. [Mechanism](#mechanism)
2. [When to Use](#when-to-use)
3. [When NOT to Use](#when-not-to-use)
4. [Shallow vs Deep Examples](#shallow-vs-deep-examples)
5. [Role Components](#role-components)
6. [Common Mistakes](#common-mistakes)
7. [Self-Check](#self-check)

---

## Mechanism

**Why it works:**
1. Activates domain-specific knowledge clusters in the model
2. Sets appropriate tone, vocabulary, and approach
3. Creates consistent character across multi-turn conversations
4. Primes the model for the expected type of response

**The research:** Role assignment shows +10-20% improvement on domain-specific tasks. Effect is stronger when the role includes expertise relevant to the task.

**The mechanism in one sentence:** Telling the model "who it is" activates relevant knowledge and sets appropriate behaviors.

---

## When to Use

- **Domain expertise needed** - Legal, medical, technical topics
- **Specific tone required** - Formal, casual, empathetic, direct
- **Consistent character** - Multi-turn interactions needing consistency
- **Teaching scenarios** - "Act as a teacher explaining to a beginner"
- **Specialized perspectives** - "As a security auditor, review..."
- **Audience targeting** - Adjust explanation level for audience

**Rule of thumb:** If a human expert would handle this differently than a generalist, assign a role.

---

## When NOT to Use

- **Simple factual queries** - "What's the capital of France?"
- **When neutrality matters** - Analysis requiring objectivity
- **Generic tasks** - Basic summarization, translation
- **Over-specification** - Adding roles to everything dilutes impact

---

## Shallow vs Deep Examples

### Shallow (What to Avoid)

```
Prompt: "You are a helpful assistant. Answer this question about Python."
```

**Why it's shallow:**
- "Helpful assistant" is the default; adds nothing
- No specific expertise activated
- No behavioral guidance beyond "be helpful"

### Deep (What to Aim For)

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

**Why it's deep:**
- Specific expertise (performance, clean code)
- Clear behavioral guidelines (what to focus on)
- Communication style defined
- Relevant standards mentioned (PEP 8, PEP 20)

---

## Role Components

### 1. Identity

Who is the model?
```
You are a [title/profession] with [experience level] in [domain].
```

Examples:
- "You are a pediatric nurse explaining medical concepts to worried parents"
- "You are a tax accountant specializing in small business finances"
- "You are a senior data scientist at a tech startup"

### 2. Expertise Areas

What specific knowledge should they draw on?
```
Your expertise includes:
- [Specific area 1]
- [Specific area 2]
- [Relevant frameworks/tools/methods]
```

### 3. Behavioral Guidelines

How should they approach problems?
```
When handling requests:
- [Approach 1]
- [Approach 2]
- [What to prioritize/avoid]
```

### 4. Communication Style

How should they communicate?
```
Your communication style is:
- [Tone: formal/casual/empathetic]
- [Length: concise/detailed]
- [Approach: direct/diplomatic]
```

### 5. Constraints

What should they NOT do?
```
Important boundaries:
- Do not provide [specific advice type] without disclaimers
- Always recommend [consulting professionals] for [serious matters]
- Stay within your expertise; admit when something is outside your scope
```

---

## Common Mistakes

### 1. Vague Roles
**Mistake:** "You are an expert"
**Problem:** Expert in what? No domain activation
**Fix:** "You are an expert in [specific domain] with [specific experience]"

### 2. Contradictory Roles
**Mistake:** "You are a conservative investor who loves high-risk opportunities"
**Problem:** Model gets confused about which behavior to exhibit
**Fix:** Ensure role components are internally consistent

### 3. Role Without Task Alignment
**Mistake:** "You are a marine biologist" for a coding question
**Problem:** Irrelevant role doesn't help; may hurt
**Fix:** Match role expertise to the task at hand

### 4. Over-Detailed Backstory
**Mistake:** "You are Sarah, born in 1985 in Ohio, who studied at..."
**Problem:** Irrelevant details waste tokens; may distract
**Fix:** Include only details that affect behavior

### 5. Forgetting Boundaries
**Mistake:** "You are a doctor" with no medical advice disclaimers
**Problem:** Model may give advice that should come from real professionals
**Fix:** Include appropriate disclaimers and referral suggestions

### 6. Default Roles
**Mistake:** "You are a helpful, harmless, and honest assistant"
**Problem:** This is already the default; adds nothing
**Fix:** Either skip role assignment or add specific expertise

---

## Self-Check

Before assigning a role:

- [ ] Is the role relevant to the task?
- [ ] Have I specified domain expertise (not just "expert")?
- [ ] Are behavioral guidelines clear?
- [ ] Is the communication style defined?
- [ ] Have I included appropriate boundaries/disclaimers?
- [ ] Is the role internally consistent (no contradictions)?
- [ ] Would this task benefit from a role? (Not always needed)

---

## Patterns

### Pattern 1: Expert Consultant

```
You are a senior [field] consultant with 15+ years of experience
advising [type of clients] on [specific area].

Your approach:
- Ask clarifying questions before giving recommendations
- Consider both short-term and long-term implications
- Provide actionable, specific advice (not vague platitudes)
- Cite relevant frameworks, standards, or research when applicable

Communication style: Professional but approachable. Use clear
language without unnecessary jargon.

[User's question]
```

### Pattern 2: Teacher/Explainer

```
You are an experienced [subject] teacher known for making complex
topics accessible to beginners.

When explaining:
- Start with the big picture before details
- Use analogies to familiar concepts
- Check for understanding with simple questions
- Build complexity gradually

Explain [topic] to someone with no background in [field].
```

### Pattern 3: Specialized Reviewer

```
You are a [type] auditor reviewing [artifact type] for [organization type].

Your review should focus on:
- [Priority 1]
- [Priority 2]
- [Priority 3]

Output format: For each issue found, provide:
- Severity (High/Medium/Low)
- Description
- Recommendation

Review the following:
[content]
```

### Pattern 4: Audience-Specific Communicator

```
You are a science communicator who specializes in explaining
[technical field] to [target audience].

Adjust your explanations to:
- Use vocabulary appropriate for [education level]
- Relate concepts to [familiar domain for audience]
- Avoid [terms/concepts to skip]

Answer this question for your audience:
[question]
```

### Pattern 5: Multi-Perspective Role

```
You will analyze this situation from three perspectives:

1. As a CFO: Focus on financial implications
2. As a CTO: Focus on technical feasibility
3. As a CPO: Focus on user/customer impact

For each perspective, provide:
- Key concerns
- Opportunities
- Recommended actions

Situation: [situation]
```

---

## Model-Specific Notes

| Model | Role Assignment Notes |
|-------|----------------------|
| **Claude** | Responds well; use specific expertise and behavioral guidelines |
| **GPT-4o** | Responds well; system message is ideal location for roles |
| **o1/o3** | Use `developer` message; keep role concise |
| **DeepSeek R1** | Put role in user message (no system prompt) |
| **Gemini** | Works well; system instruction slot available |
| **Kimi K2** | Keep role goal-oriented; don't over-specify steps |
| **Qwen** | Default system prompt works; can customize |

### Role in System vs User Message

**System message (when available):**
- Persistent across conversation
- Sets baseline behavior
- Good for identity, style, constraints

**User message:**
- Can change per request
- Good for task-specific roles
- Required when system message not supported (DeepSeek R1)

---

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

### Support

```
You are a patient, empathetic customer support specialist.
You acknowledge frustration, explain solutions clearly,
and follow up to ensure issues are resolved.
```

---

**Impact:** +10-20% on domain-specific tasks
**Cost:** Token overhead for role description
**Best for:** Domain expertise, consistent character, audience targeting
