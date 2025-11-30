# Structured Output

Constrain model output to a specific format (JSON, XML, schema). Achieves near-perfect format compliance.

## Table of Contents
1. [Mechanism](#mechanism)
2. [When to Use](#when-to-use)
3. [When NOT to Use](#when-not-to-use)
4. [Shallow vs Deep Examples](#shallow-vs-deep-examples)
5. [Common Mistakes](#common-mistakes)
6. [Self-Check](#self-check)
7. [Implementation Patterns](#implementation-patterns)

---

## Mechanism

**Why it works:**
1. Clear structural constraints reduce ambiguity in what the model should produce
2. JSON/XML schemas act as templates that guide token generation
3. Many APIs support native structured output modes (JSON mode, function calling)
4. Parseable output enables reliable downstream processing

**The impact:** 99%+ format compliance when using native JSON modes or strict schemas.

**The mechanism in one sentence:** Structural constraints remove formatting ambiguity and enable programmatic parsing.

---

## When to Use

- **API integrations** - When output feeds into code
- **Data extraction** - Pulling structured info from unstructured text
- **Function calling** - Tool use requires structured arguments
- **Multi-field responses** - When you need several distinct pieces of information
- **Consistency requirements** - Same format across many responses
- **Automated pipelines** - Anything that needs to be parsed

**Rule of thumb:** If you're going to parse the output programmatically, use structured output.

---

## When NOT to Use

- **Creative writing** - Structure constrains creativity
- **Conversational responses** - Feels robotic
- **Simple single-value answers** - Overhead not worth it
- **Exploratory tasks** - When you don't know what structure you need yet
- **Human-only consumption** - Prose is often more readable

---

## Shallow vs Deep Examples

### Shallow (What to Avoid)

```
Prompt: "Extract the person's name and age from this text and return as JSON."

Text: "John Smith, a 34-year-old engineer from Boston, recently..."

Response: {"name": "John Smith", "age": "34"}
```

**Why it's shallow:**
- No schema definition - model guesses field names
- String "34" instead of number 34
- No handling of missing fields
- Will break if text doesn't contain expected info

### Deep (What to Aim For)

```
Prompt: "Extract person information from the text below.

Return a JSON object matching this exact schema:
{
  "name": string | null,        // Full name if present
  "age": number | null,         // Age as integer if present
  "occupation": string | null,  // Job title if mentioned
  "location": string | null     // City/location if mentioned
}

Rules:
- Use null for any field not found in the text
- Age must be a number, not a string
- Extract only explicitly stated information

Text: \"\"\"
John Smith, a 34-year-old engineer from Boston, recently...
\"\"\"

Respond with only the JSON object, no additional text."

Response:
{
  "name": "John Smith",
  "age": 34,
  "occupation": "engineer",
  "location": "Boston"
}
```

**Why it's deep:**
- Explicit schema with types
- Null handling for missing fields
- Type specification (number not string)
- Clear rules for extraction
- Output-only instruction

---

## Common Mistakes

### 1. No Schema Definition
**Mistake:** "Return this as JSON"
**Problem:** Model invents field names; inconsistent structure
**Fix:** Provide explicit schema with field names and types

### 2. Allowing Prose Around JSON
**Mistake:** Not specifying "only the JSON"
**Problem:** Model adds "Here's the JSON:" or explanatory text, breaking parsers
**Fix:** "Respond with only the JSON object, no additional text"

### 3. String Numbers
**Mistake:** Not specifying `age: number`
**Problem:** Get `"age": "34"` instead of `"age": 34`
**Fix:** Explicitly type numeric fields in schema

### 4. No Null Handling
**Mistake:** Assuming all fields will be present
**Problem:** Model omits fields or hallucinates values
**Fix:** Define null behavior: "Use null if not found"

### 5. Overly Complex Schemas
**Mistake:** 50-field nested schema in one prompt
**Problem:** Model loses track; errors compound
**Fix:** Flatten where possible; break into multiple extractions if needed

### 6. Not Using Native JSON Mode
**Mistake:** Relying on prompt instructions alone
**Problem:** Model occasionally breaks format
**Fix:** Use `response_format: { type: "json_object" }` when available

---

## Self-Check

Before requesting structured output:

- [ ] Have I provided an explicit schema with field names?
- [ ] Are types specified (string, number, boolean, null)?
- [ ] Have I defined behavior for missing/unknown values?
- [ ] Did I request "only the JSON/XML, no additional text"?
- [ ] Is the schema complexity reasonable (<10-15 fields)?
- [ ] Am I using native JSON mode if available?

---

## Implementation Patterns

### Pattern 1: JSON with Schema

```python
schema = {
    "type": "object",
    "properties": {
        "sentiment": {"type": "string", "enum": ["positive", "negative", "neutral"]},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "key_phrases": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["sentiment", "confidence"]
}

# OpenAI
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[...],
    response_format={"type": "json_schema", "json_schema": {"schema": schema}}
)

# Claude (in prompt)
prompt = f"""Analyze the sentiment. Return JSON matching this schema:
{json.dumps(schema, indent=2)}

Text: {text}

Respond with only the JSON."""
```

### Pattern 2: XML with Tags

```
Extract entities from the text below.

Format your response as:
<entities>
  <person>
    <name>Full name</name>
    <role>Their role if mentioned</role>
  </person>
  <organization>
    <name>Org name</name>
    <type>Company/Government/NGO/etc</type>
  </organization>
</entities>

Text: """
{text}
"""
```

**Why XML works well:**
- Self-documenting tags
- Handles nested structures naturally
- Claude in particular excels at XML

### Pattern 3: Function Calling (Tool Use)

```python
tools = [{
    "type": "function",
    "function": {
        "name": "record_sentiment",
        "description": "Record the sentiment analysis result",
        "parameters": {
            "type": "object",
            "properties": {
                "sentiment": {"type": "string", "enum": ["positive", "negative", "neutral"]},
                "confidence": {"type": "number"}
            },
            "required": ["sentiment", "confidence"]
        },
        "strict": True  # Enforce schema compliance
    }
}]
```

**Advantages:**
- Schema enforced by API
- Cleanly separates data from prose
- Integrates with tool use workflows

### Pattern 4: Markdown Tables

```
Summarize the comparison in this format:

| Feature | Product A | Product B | Winner |
|---------|-----------|-----------|--------|
| [feature] | [value] | [value] | A/B/Tie |
```

**Use when:**
- Human readability matters more than parsing
- Comparing multiple items
- Output will be displayed, not processed

---

## Model-Specific Notes

| Model | Best Approach |
|-------|---------------|
| **Claude** | XML tags work excellently; JSON also good |
| **GPT-4o** | Native JSON mode available; use `strict: true` for functions |
| **o1/o3** | Add "Formatting re-enabled" for markdown; JSON works |
| **DeepSeek** | Standard JSON; no special modes |
| **Gemini** | Native JSON mode available |
| **Qwen** | Standard JSON; careful with ChatML formatting |

---

**Impact:** 99%+ format compliance
**Cost:** Slight prompt overhead
**Best for:** APIs, data extraction, function calling, automated pipelines
