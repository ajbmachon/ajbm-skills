# Tool Guide

How Claude uses the SkillDistiller toolbox. These tools are **on-demand utilities**, not a fixed pipeline. Claude decides which tools to use based on the situation.

---

## Core Principle

**Tools augment Claude's intelligence for context efficiency. They do NOT replace Claude's judgment.**

For the **current session** (primary use case), no tools are needed — Claude reads its own in-memory context directly. If the conversation was compacted, recover from the disk transcript (transcripts are always saved regardless of compaction).

For **stored transcripts**, Claude uses whichever tools are appropriate to filter noise and structure data before applying analytical intelligence.

---

## The Toolbox

### transcript-filter.ts

**Purpose:** Strip non-conversational noise from raw JSONL transcript files.

**Removes:** `tool_use` blocks, `tool_result` blocks, system messages, hook output, progress events, thinking blocks.

**Keeps:** User messages (text content), assistant messages (text content).

**When to use:** When loading a stored transcript that contains tool calls, system prompts, and other noise that would waste context window without adding analytical value.

```bash
# Filter a transcript, output to stdout
bun run Tools/transcript-filter.ts <input.jsonl>

# Filter and save to file
bun run Tools/transcript-filter.ts <input.jsonl> --output <clean.jsonl>
```

### turn-extractor.ts

**Purpose:** Extract clean user/assistant turn pairs from JSONL.

**Input:** Filtered JSONL (or raw — it can filter internally).

**Output:** JSON array of turn objects:
```json
[
  {
    "turn_number": 1,
    "assistant_context": "What Claude said/did before the user responded",
    "user_action": "What the user said"
  }
]
```

**When to use:** When you need structured turn pairs for analysis.

```bash
bun run Tools/turn-extractor.ts <input.jsonl>
bun run Tools/turn-extractor.ts <input.jsonl> --output <turns.json>
```

### qmd (External)

**Purpose:** Semantic search across ALL conversation transcripts using hybrid BM25 + vector search.

**When to use:** Cross-conversation pattern confirmation — finding similar corrections, questions, or quality gates across multiple sessions.

```bash
# Index transcripts
qmd index ~/.claude/

# Search for patterns
qmd search "error handling at API boundaries"
```

**Install:** `brew install qmd` (required dependency, see SKILL.md prerequisites).

---

## Decision Guide: Which Tools When?

| Situation | Tools to Use |
|-----------|-------------|
| Analyzing **current session** | None — read in-memory context |
| Analyzing **current session** (compacted) | Read disk transcript, then no tools needed |
| Analyzing **stored transcript** (short, clean) | Maybe just Read — assess if filtering is needed |
| Analyzing **stored transcript** (long, noisy) | transcript-filter → turn-extractor |
| **Cross-conversation** pattern search | qmd search |
| **Verifying** a skill works | None — Claude reads skill + transcript directly |

**Remember:** You're the intelligent analyst. The tools handle data plumbing. Don't use tools when reading the data directly is faster and sufficient.
