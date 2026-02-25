# Structured Output

Constrain model output to a specific format (JSON, XML, schema). Achieves near-perfect format compliance.

## Mechanism

**Why it works:** Clear structural constraints reduce ambiguity in what the model should produce. JSON/XML schemas act as templates that guide token generation. Many APIs support native structured output modes (JSON mode, function calling). Parseable output enables reliable downstream processing.

**The impact:** 99%+ format compliance when using native JSON modes or strict schemas.

## When to Use

- API integrations, data extraction, function calling
- Multi-field responses needing several distinct pieces of information
- Consistency requirements and automated pipelines

**Rule of thumb:** If you're going to parse the output programmatically, use structured output.

## When NOT to Use

- Creative writing (structure constrains creativity)
- Conversational responses or simple single-value answers
- Exploratory tasks where you don't know what structure you need yet

## Deep Example

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

**Why it works:** Explicit schema with types, null handling for missing fields, type specification (number not string), clear rules, output-only instruction.

## Implementation Pattern: JSON with Schema

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
    model="gpt-5.2-chat-latest",
    messages=[...],
    response_format={"type": "json_schema", "json_schema": {"schema": schema}}
)

# Claude (in prompt)
prompt = f"""Analyze the sentiment. Return JSON matching this schema:
{json.dumps(schema, indent=2)}

Text: {text}

Respond with only the JSON."""
```

## Model-Specific Notes

| Model | Best Approach |
|-------|---------------|
| **Claude** | XML tags work excellently; JSON also good |
| **GPT-5.x** | Native JSON mode; use `strict: true` for functions; Responses API preferred |
| **o1/o3** | Add "Formatting re-enabled" for markdown; JSON works |
| **DeepSeek** | Standard JSON; no special modes |
| **Gemini** | Native JSON mode available |
| **Qwen** | Standard JSON; careful with ChatML formatting |

---

**Impact:** 99%+ format compliance
**Cost:** Slight prompt overhead
**Best for:** APIs, data extraction, function calling, automated pipelines
