# Salience (High-Importance Markers)

Make critical information stand out using XML tags, caps, formatting, and explicit labels. Increases instruction compliance.

## Mechanism

**Why it works:** Visual distinction increases token-level attention weights. XML tags create semantic boundaries the model can parse. CAPS and labels signal relative importance and reduce ambiguity about what matters.

**The research:** Studies show +23-31% improvement in instruction compliance when using salience markers. Claude particularly excels with XML tags; GPT models respond well to markdown structure.

## When to Use

- Critical constraints and safety/policy boundaries
- Output format requirements and section demarcation in long prompts
- Input/output separation (distinguishing user content from instructions)

**Rule of thumb:** If you'd bold or highlight it for a human, mark it for the model.

## When NOT to Use

- Everything (if everything is marked important, nothing is)
- Conversational contexts or short, simple prompts

## Marker Types

### XML Tags (Best for Claude)
```xml
<instructions>What to do</instructions>
<context>Background information</context>
<critical>Must-follow rules</critical>
```

### Markdown Headers
```markdown
## Instructions
## Context
## Output Requirements
```

### CAPS for Emphasis
```
IMPORTANT: Do not include personal names.
```
**Caution:** Overuse dilutes impact. Use sparingly.

### Explicit Labels
```
TASK: Summarize the document
CONSTRAINT: Maximum 100 words
FORMAT: Bullet points
```

## Deep Example

```
Prompt: "<instructions>
Summarize the following text.
- Maximum length: 100 words
- Focus: main argument only
</instructions>

<critical>
DO NOT include any personal names in the summary.
This is a privacy requirement and must not be violated.
</critical>

<text>
[long text here]
</text>

Provide your summary:"
```

**Why it works:** Clear semantic sections via XML tags. Critical constraint explicitly marked and explained. Visual hierarchy guides model attention. Input text clearly separated from instructions.

## Model-Conditional Guidance

| Model Family | Primary Salience | Notes |
|---|---|---|
| Claude 4.x | **Markdown headers** | Prefers markdown over XML. Use ## headers, **bold**, CAPS for critical terms. |
| GPT-5.x | **XML tags or delimiters** | Responds well to `<context>`, `<instructions>` tags. |
| Gemini 3.x | **Markdown or XML** | Both work. Place query at END for long contexts. |
| o1/o3 | **Delimiters and headings** | Use structure to separate task, context, constraints. |
| DeepSeek R1 | **Markdown headers** | All instructions in user message. Use ## headers. |

**Default:** Markdown headers are the most universally effective.

---

**Impact:** +23-31% instruction compliance
**Cost:** Minimal token overhead
**Best for:** Critical constraints, section organization, injection protection
