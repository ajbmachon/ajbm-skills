# Tool Description Craft

How you describe tools determines how well the model uses them. Small refinements yield dramatic improvements.

## Quick Summary

**Impact:** Highest-leverage prompt surface for agentic systems
**When to use:** Any system that provides tools/functions to an LLM
**Mechanism:** Better descriptions reduce tool misuse, hallucinated parameters, and unnecessary calls

## Key Principles

### 1. Make implicit context explicit
```
BAD:  "Search the database"
GOOD: "Search the customer database by name, email, or account ID.
       Returns up to 10 matching records sorted by relevance."
```

### 2. Define niche terminology
```
BAD:  "Get the CR status"
GOOD: "Get the status of a Change Request (CR) -- an internal ticket
       representing a proposed code change."
```

### 3. Return human-readable values
Include display names alongside IDs. Models make better decisions when they can read the data.

### 4. Consolidate tools (fewer is better)
```
BAD:  search_by_name, search_by_email, search_by_id (5 tools)
GOOD: customer_search(query, field="auto") (1 tool)
```

### 5. Namespace consistently
```
GOOD: asana_search, asana_create_task, asana_get_user
```

## Before / After Example

```json
// BEFORE (vague)
{"name": "query", "description": "Query the system",
 "parameters": {"q": {"type": "string"}, "n": {"type": "integer"}}}

// AFTER (precise)
{"name": "knowledge_base_search",
 "description": "Search internal knowledge base for articles matching
  a natural-language query. Use when user asks a question that might
  be answered by documentation.",
 "parameters": {
   "query": {"type": "string", "description": "Natural language search query."},
   "max_results": {"type": "integer", "description": "Results to return (1-20). Default 5."}}}
```

## Meta-Pattern

Use the model to improve its own descriptions. Paste your tool schema and ask it to rewrite following the principles above.

## Tips

- Test by asking the model "which tool would you use for X?" without other context
- If wrong tool is picked, the description is the problem
- Keep descriptions under 200 words
