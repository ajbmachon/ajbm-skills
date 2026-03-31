# Workflow: Search & Save Bookmarks by Topic

Use when the user says "find my bookmarks about X" or "search my bookmarks for Y" or "save everything about Z from my bookmarks."

This is a **semantic search** problem. The user's topic description may not match exact keywords in the tweets. Claude reads the content and judges relevance by meaning.

## Step 1: Pull All Bookmarks

```bash
twitter bookmarks --json -n 200 -o /tmp/bookmarks_all.json
```

If the user specifies a date range, filter after pulling:
```python
# The main bookmarks command has no --since flag
# Filter by createdAtISO in the JSON after retrieval
```

For folder-specific search, use the folder variant (which DOES support --since):
```bash
twitter bookmarks folders <folder_id> --json --since 2026-02-01
```

## Step 2: Semantic Filtering (Claude IS the Filter)

Read the JSON. For each bookmark, evaluate relevance to the user's topic by reading:
- Tweet text (full content, not just first line)
- Article title (if present — 30%+ of bookmarks are link-only)
- Author handle and name (sometimes signals topic)
- Quoted tweet content (if present)

**Do NOT use keyword matching, regex, or jq for filtering.** These miss contextual references and produce false positives. Read each tweet and judge: "Is this about what the user asked for?"

For link-only tweets (text is just a t.co URL), use the `articleTitle` field. If that's also empty, fetch the tweet individually for more context:
```bash
twitter -c tweet <id>
```

**Batch strategy for large sets:** If 200+ bookmarks, process in batches of 50. For each batch, list the relevant ones with a 1-line reason. This prevents context overflow.

## Step 3: Present Candidates for Review

Show the user what you found. Format as a numbered list:

```
Found 18 bookmarks about "Polymarket trading bots":

1. @LunarResearcher (2026-03-19) — Polymarket bot math guide, Kelly Criterion formulas
2. @zerqfer (2026-03-13) — OpenClaw bot woke up at 3:47AM for $12K deployment
3. @Argona0x (2026-03-14) — US govt dataset trading, $67K/month claim
...

Confidence: 14 strong matches, 4 borderline. Want me to include the borderlines?
```

## Step 4: Self-Correct Based on Feedback

If the user says "no, #7 isn't relevant" or "you missed the one about X," adjust:
- Remove false positives
- Search again with the new understanding of what they're looking for
- Re-present the refined list

This step is critical. First-pass classification is never perfect. The review loop IS the quality mechanism.

## Step 5: Save as Obsidian Notes

For each confirmed relevant bookmark, create an Obsidian-compatible markdown file:

```markdown
---
id: "<tweet_id>"
author: "@handle"
date: YYYY-MM-DD
url: https://x.com/handle/status/<tweet_id>
tags:
  - <topic-tag>
  - <subtopic-tag>
  - <author-tag-if-notable>
cluster: <primary-category>
likes: N
bookmarks: N
source: twitter-bookmarks
---

# @handle — <brief title>

<full tweet text>

## Context
<any article title, thread context, or summary>

## Related
- [[<related_tweet_id>]] — <why it's related>
```

Save to a user-specified directory (default: `twitter-saves/<topic>/`).

Create an `_index.md` linking all saved notes for this search session.

## When to Use Search vs Classify

| User says... | Use this workflow |
|-------------|-------------------|
| "Find bookmarks about X" | Search (this file) |
| "What did I bookmark about Y?" | Search (this file) |
| "Organize all my bookmarks" | Classify (classify-workflow.md) |
| "Tag and categorize everything" | Classify (classify-workflow.md) |
| "Save tweets about Z" | Search (this file) |
