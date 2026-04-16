# Workflow: Classify & Organize Bookmarks

Use when the user wants to organize, categorize, tag, or structure their bookmarks into a searchable knowledge base. This is a **pattern recognition and classification** task — not a filing task.

The output is an Obsidian-compatible vault of tagged, linked markdown notes. The taxonomy emerges from the data, not from a predefined list.

## Mental Model

This is dimensionality reduction:

```
tweets (200 unique items)
  → tags (3-8 per tweet, high-dimensional)
    → clusters (tags that co-occur form natural groups)
      → categories (human-readable names for clusters)
        → vault (Obsidian notes with frontmatter + wikilinks)
```

Tags are the ground truth. Categories are a lossy compression for human navigation. A tweet can have many tags but lives in one primary category with secondary categories noted.

---

## Phase 1: Pull & Inspect

```bash
# Pull all bookmarks
twitter bookmarks --json -n 200 -o /tmp/bookmarks_all.json

# Also pull folder contents if folders exist
twitter -c bookmarks folders                 # list folders
twitter bookmarks folders <id> --json        # per folder
```

Read the JSON. Get a feel for the data:
- How many bookmarks total?
- What date range do they cover?
- How many are link-only (just a t.co URL)?
- Any obvious clusters visible from scanning author names or keywords?

Present a quick summary to the user: "You have N bookmarks spanning DATE to DATE. Here's a rough sense of what's there..."

## Phase 2: Tag (Pattern Recognition)

For each bookmark, generate **3-8 semantic tags** across these dimensions:

| Dimension | Examples | Purpose |
|-----------|---------|---------|
| **Topic** | `polymarket`, `trading-strategy`, `agent-memory` | What it's about |
| **Tool/Product** | `claude-code`, `openclaw`, `qwen-3.5` | Specific tools mentioned |
| **Person** | `karpathy`, `brian-roemmele` | Notable authors/subjects |
| **Type** | `tutorial`, `announcement`, `think-piece`, `thread` | Content format |
| **Intent** | `to-build`, `to-learn`, `reference`, `inspiration` | Why the user likely saved it |

**Tagging principles:**
- Tags should be specific enough to be useful. `ai` is too broad. `ai-agent-memory-systems` is about right.
- Use lowercase kebab-case for consistency.
- The same concept should always get the same tag — don't use both `trading-bots` and `trade-bot`.
- Link-only tweets: use the `articleTitle` field. If unavailable, fetch with `twitter -c tweet <id>` for context. If still ambiguous, tag as `needs-context` and flag for user review.

**Batch processing:** For 200 bookmarks, process in batches of ~30. For each batch, output a compact table:

```
| # | @author | tags |
|---|---------|------|
| 0 | @LunarResearcher | polymarket, trading-strategy, kelly-criterion, tutorial |
| 1 | @trq212 | claude-code, skills, announcement |
```

Do NOT present every batch to the user — this is intermediate work. Aggregate first.

## Phase 3: Cluster (Emergent Structure)

After tagging all bookmarks:

1. **Aggregate tags** — Count frequency of each tag across all bookmarks
2. **Find co-occurrence** — Which tags appear together? (`polymarket` + `trading-strategy` co-occur frequently → they form a cluster)
3. **Identify natural groups** — Clusters are sets of frequently co-occurring tags. Look for 6-12 natural clusters. Too few (<5) means categories are too broad. Too many (>15) means you're over-splitting.
4. **Name each cluster** — Give it a human-readable name that captures the theme. Good names are 2-3 words, specific but not too narrow.

Present the proposed taxonomy to the user:

```
## Proposed Categories (8 clusters found)

1. **Trading Bots** (18 tweets) — Polymarket, prediction markets, trading strategies
   Top tags: polymarket, trading-strategy, kelly-criterion, clawdbot
   Examples: @LunarResearcher's math guide, @Argona0x's $50→$2980 bot

2. **Claude Code** (35 tweets) — Official features, tips, integrations
   Top tags: claude-code, skills, cowork, announcement
   Examples: @trq212's feature releases, @bcherny's code review

3. **Local Models** (20 tweets) — Running LLMs on consumer hardware
   Top tags: qwen-3.5, local-inference, quantization, rtx-3090
   Examples: @sudoingX's benchmarks, @UnslothAI's releases

...

⚠️ 7 tweets don't fit any cluster well (outliers):
   - @0xQuasark: psilocybin research (not AI related)
   - @SterlingCooley: microtubule consciousness (neuroscience)
   ...

Does this taxonomy match how you think about these bookmarks? Adjust?
```

## Phase 4: User Calibration

This is the most important step. The taxonomy must match the USER's mental model.

**Ask specifically:**
- "Should I merge any of these? Split any?"
- "Are the names right, or would you call them something different?"
- "Where should the outliers go — misc folder, or leave uncategorized?"
- "Any categories missing that you expected to see?"

Apply their feedback. This calibration step is what separates good classification from technically-correct-but-personally-wrong classification.

## Phase 5: Generate Obsidian Vault

For each bookmark, create a markdown file:

**Filename:** `<tweet_id>.md` (numeric ID ensures uniqueness)

**Template:**
```markdown
---
id: "<tweet_id>"
author: "@handle"
author_name: "Display Name"
date: YYYY-MM-DD
url: https://x.com/handle/status/<tweet_id>
tags:
  - tag-one
  - tag-two
  - tag-three
category: primary-category
secondary_categories:
  - secondary-one
confidence: high|medium|low
likes: N
retweets: N
bookmarks: N
has_media: true|false
has_article: true|false
source: twitter-bookmarks
---

# @handle — <descriptive title derived from content>

<full tweet text, preserving line breaks>

## Article
<article title if present, with URL>

## Media
<list media URLs if present>

## Related
- [[<related_tweet_id>]] — <brief reason>
```

**Vault structure:**
```
twitter-vault/
├── _index.md              # Master index: all tweets sorted by category
├── _tags.md               # Tag frequency list for quick reference
├── tweets/                # One file per tweet
│   ├── 2034254160556667215.md
│   ├── 2034616654613672180.md
│   └── ...
└── categories/            # Category overview pages
    ├── trading-bots.md    # Lists all tweets in this category
    ├── claude-code.md
    └── ...
```

**Category pages** (`categories/trading-bots.md`):
```markdown
---
type: category
tweet_count: 18
top_tags: [polymarket, trading-strategy, kelly-criterion]
---

# Trading Bots

Prediction market trading bots, strategies, and results.

## Tweets
- [[2034254160556667215]] — @LunarResearcher: Polymarket math guide
- [[2034616654613672180]] — @LunarResearcher: Bot making $400
...
```

**_index.md:**
```markdown
# Twitter Bookmark Vault

Generated: YYYY-MM-DD | Total: N tweets | Categories: M

## By Category
### Trading Bots (18)
- [[2034254160556667215]] — @LunarResearcher: Polymarket math guide
...

### Claude Code (35)
...

## Uncategorized (7)
- [[tweet_id]] — @author: content preview
```

## Phase 6: Quality Self-Check

Before declaring done, verify:
- [ ] Every bookmark has a file in the vault
- [ ] Every file has complete YAML frontmatter
- [ ] No empty `tags:` arrays — every tweet has at least 2 tags
- [ ] Category pages exist for each category
- [ ] `_index.md` links to all tweets
- [ ] Related links (`[[wikilinks]]`) connect tweets that share 3+ tags
- [ ] Outliers are explicitly handled (uncategorized section or user-chosen category)

Present a summary: "Vault created at `<path>` with N tweets across M categories. Open in Obsidian to see the graph view."

---

## Incremental Updates

When the user runs this workflow again later (new bookmarks accumulated):
1. Pull fresh bookmarks
2. Diff against existing vault (by tweet ID)
3. Tag and classify only the NEW bookmarks
4. Use the existing taxonomy — only propose new categories if new bookmarks cluster differently
5. Update `_index.md` and category pages
