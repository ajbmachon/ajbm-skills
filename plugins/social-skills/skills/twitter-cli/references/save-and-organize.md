# Workflow: Save and Organize Twitter Content

Use these patterns when the user wants to capture, reference, and organize information from Twitter. The goal is making Twitter knowledge persistent and searchable rather than ephemeral.

## Save a Single Tweet

```bash
twitter tweet <id_or_url> --json -o saved_tweet.json
```

After saving, create a readable summary with: author, date, full text, any links, key metrics. Include the original URL for reference.

## Save a Full Thread

Threads often contain the real insight. Pull the tweet with all replies from the author:

```bash
twitter -c tweet <id_or_url> -n 100
```

Read the output, reconstruct the thread (same author's sequential replies), and save as a clean markdown file:

```markdown
# Thread by @author — Topic
**Date:** 2026-03-20 | **URL:** https://x.com/...

1/N: First tweet text...
2/N: Second tweet text...
...

## Key Takeaways
- [summarize the main points]
```

## Organize by Topic

When saving multiple tweets, organize into topic directories:

```
twitter-saves/
├── trading-strategies/
│   ├── momentum-setup-20260320.md
│   └── options-flow-analysis-20260318.md
├── market-analysis/
│   ├── spy-sentiment-20260320.json
│   └── macro-outlook-20260315.md
└── people/
    ├── trader-x-best-posts.md
    └── analyst-y-research.md
```

## Bookmark Export and Categorization

For periodic bookmark review:

```bash
twitter bookmarks --json -n 200 -o bookmarks_export.json
```

Read the export, then categorize each bookmark and present as a structured summary. Group by theme, flag high-value items, and suggest which ones deserve deeper investigation.

## Reference Pattern

When the user mentions something they saw on Twitter, or you need to pull context from a tweet into a conversation:

```bash
# Pull the tweet
twitter -c tweet <url>

# Or search for it if they describe it loosely
twitter -c search "the keywords they mentioned" --from possible_author -t latest
```

Present the content inline so the user can discuss it without switching to their browser.
