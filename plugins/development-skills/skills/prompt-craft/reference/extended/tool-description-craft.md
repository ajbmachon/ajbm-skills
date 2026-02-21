# Tool Description Craft

How you describe tools determines how well the model uses them. Small refinements yield dramatic improvements.

## Quick Summary

**Impact:** Highest-leverage prompt surface for agentic systems
**When to use:** Any system that provides tools/functions to an LLM
**Mechanism:** Better descriptions reduce tool misuse, hallucinated parameters, and unnecessary calls

## The Pattern

Write tool descriptions as if explaining to a new team member. They are smart but have zero context about your system.

## Key Principles

### 1. Make implicit context explicit
```
BAD:  "Search the database"
GOOD: "Search the customer database by name, email, or account ID.
       Returns up to 10 matching customer records sorted by relevance.
       Use this when the user asks about a specific customer."
```

### 2. Define niche terminology
```
BAD:  "Get the CR status"
GOOD: "Get the status of a Change Request (CR) -- an internal ticket
       representing a proposed code change. Returns: pending, approved,
       or rejected."
```

### 3. Return human-readable values
```
BAD:  Returns: {"id": "550e8400-e29b-41d4-a716-446655440000"}
GOOD: Returns: {"id": "...", "name": "Acme Corp", "status": "active"}
```
Include display names alongside IDs. Models make better decisions when they can read the data.

### 4. Expose response_format parameters
```
Parameters:
  - response_format: "summary" | "detailed" | "raw"
    Default: "summary". Use "detailed" for specifics, "raw" for debugging.
```

### 5. Consolidate tools (fewer is better)
```
BAD (5 tools):
  search_by_name, search_by_email, search_by_id,
  search_by_date, search_by_status

GOOD (1 tool):
  customer_search(query, field="auto")
  "Searches customers. Set field to 'name', 'email', 'id', 'date',
   or 'status'. Default 'auto' detects the field from the query."
```

### 6. Namespace consistently
```
BAD:  search, create_task, getUser, ListProjects
GOOD: asana_search, asana_create_task, asana_get_user, asana_list_projects
```

## Before / After Example

### Before (vague)
```json
{
  "name": "query",
  "description": "Query the system",
  "parameters": {
    "q": {"type": "string"},
    "n": {"type": "integer"}
  }
}
```

### After (precise)
```json
{
  "name": "knowledge_base_search",
  "description": "Search the internal knowledge base for articles matching a natural-language query. Returns ranked results with title, snippet, and URL. Use this when the user asks a question that might be answered by documentation.",
  "parameters": {
    "query": {
      "type": "string",
      "description": "Natural language search query. Be specific: 'how to reset MFA' not 'MFA'."
    },
    "max_results": {
      "type": "integer",
      "description": "Number of results to return (1-20). Default 5. Use 10+ for broad questions."
    }
  }
}
```

## Meta-Pattern: Use the Model to Improve Its Own Descriptions

Paste your tool schema into Claude and ask it to rewrite following the principles above. This works because the model knows what it needs to understand a tool -- let it tell you what is missing.

## When to Use

- Building any agentic system with tool calling
- Debugging unexpected tool selection or parameter errors
- Onboarding a new model to an existing tool set
- Reducing hallucinated tool calls

## When NOT to Use

- Tools with self-explanatory names AND parameters (rare)
- Internal-only tools where the model never selects them directly

## Tips

- Test tool descriptions by asking the model "which tool would you use for X?" without other context
- If the model picks the wrong tool, the description is the problem -- not the model
- Keep descriptions under 200 words; long descriptions get lost in context
- Update descriptions when you add features to the underlying tool

See also: [context-engineering](context-engineering.md) for managing total tool context budget
