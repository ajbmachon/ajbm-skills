---
name: twitter-cli
description: >
  Access Twitter/X data via the `twitter` CLI tool — fetch bookmarks, search tweets,
  read timelines, view profiles, post tweets, and more. Cookie-based auth, no API key needed.
  USE WHEN: twitter, tweets, bookmarks, x.com, tweet search, twitter search, post tweet,
  my bookmarks, twitter feed, liked tweets, user timeline, twitter article, quote tweet,
  reply to tweet, twitter list, who do I follow, my twitter, tweet thread.
  Use this skill whenever the user wants to read from or write to Twitter/X, even if they
  don't explicitly mention a CLI tool. This is the primary interface for all Twitter/X operations.
---

# twitter-cli — Twitter/X Data Access

A lightweight CLI tool (`twitter`) for reading and writing Twitter/X data. Cookie-based authentication — no API keys, no per-request costs.

## Setup

### Install

```bash
# Check if installed
which twitter || uv tool install twitter-cli
```

Package: `twitter-cli` on PyPI. Binary name: `twitter`.

### Authentication

The CLI extracts cookies automatically from your browser (Arc/Chrome/Edge/Firefox/Brave). On first run, macOS will show a Keychain access prompt — click **Always Allow**.

**If auto-extraction fails**, set cookies manually:

1. Open x.com in browser (logged in) → DevTools (F12) → Application → Cookies → `https://x.com`
2. Copy `auth_token` and `ct0` values
3. Export:
```bash
export TWITTER_AUTH_TOKEN="<auth_token>"
export TWITTER_CT0="<ct0>"
```

**Verify:** `twitter status` — should show `ok: true`.

---

## Global Flags

| Flag | Effect |
|------|--------|
| `-c, --compact` | Minimal output, LLM-friendly. **Always use this flag.** |
| `--json` | JSON output. Use when structured data is needed for processing. |
| `--yaml` | YAML output. |
| `-v, --verbose` | Debug logging. Use only for troubleshooting. |

**Rule: Always pass `-c` for readable output. Use `--json` when you need to parse or process the data.**

**IMPORTANT: `-c` is a GLOBAL flag — it must go BEFORE the subcommand, not after.**
```
✅ twitter -c bookmarks        # Correct: global flag before subcommand
❌ twitter bookmarks -c        # Wrong: subcommand doesn't recognize -c
```

---

## Commands Reference

### Reading Data

#### bookmarks — Fetch bookmarked tweets

```bash
twitter -c bookmarks                    # Recent bookmarks (compact)
twitter -c bookmarks -n 50             # Last 50 bookmarks
twitter --json bookmarks -o bm.json    # Save as JSON
twitter bookmarks --filter              # Score-based filtering
twitter bookmarks --full-text           # Full tweet text in table
```

Subcommand: `twitter bookmarks folders` — list bookmark folders or fetch from a specific folder.

#### search — Search tweets

```bash
twitter -c search "Claude Code"                          # Basic search
twitter -c search "AI agents" -t latest                  # Latest tweets
twitter -c search "python" --from elonmusk               # From specific user
twitter -c search "rust" --has links --min-likes 100     # With filters
twitter -c search --from bbc --exclude retweets          # User tweets, no RTs
twitter -c search "AI" --lang en --since 2026-01-01      # Date + language
```

| Option | Values |
|--------|--------|
| `-t, --type` | `top` (default), `latest`, `photos`, `videos` |
| `--from TEXT` | Only tweets from this user |
| `--to TEXT` | Only tweets directed at this user |
| `--lang TEXT` | ISO language code (`en`, `fr`, `ja`) |
| `--since TEXT` | Start date `YYYY-MM-DD` |
| `--until TEXT` | End date `YYYY-MM-DD` |
| `--has` | `links`, `images`, `videos`, `media` (repeatable) |
| `--exclude` | `retweets`, `replies`, `links` (repeatable) |
| `--min-likes N` | Minimum likes |
| `--min-retweets N` | Minimum retweets |
| `-n, --max N` | Max results |

#### feed — Home timeline

```bash
twitter -c feed                         # Algorithmic feed
twitter -c feed -t following            # Chronological feed
twitter -c feed -n 20                   # Last 20 tweets
twitter --json feed -o feed.json        # Save as JSON
```

Types: `for-you` (default, algorithmic) or `following` (chronological).

#### tweet — View tweet + replies

```bash
twitter -c tweet 1234567890             # By tweet ID
twitter -c tweet https://x.com/user/status/1234567890   # By URL
twitter -c tweet 1234567890 -n 50       # With up to 50 replies
```

#### show — View tweet from last results

```bash
twitter -c show 3                       # Show tweet #3 from last search/feed
twitter --json show 3 -o tweet.json     # Save detail as JSON
```

Uses the index from the most recent `feed` or `search` output.

#### user-posts — User's tweet timeline

```bash
twitter -c user-posts elonmusk          # Recent tweets from user
twitter -c user-posts elonmusk -n 50    # Last 50 tweets
twitter --json user-posts elonmusk      # As JSON
```

#### likes — Liked tweets

```bash
twitter -c likes myhandle               # Your own likes only
```

Note: X made all likes private (June 2024). You can only view YOUR OWN likes.

#### user — View profile

```bash
twitter -c user elonmusk                # Profile summary
twitter --json user elonmusk            # Profile as JSON
```

#### followers / following

```bash
twitter -c followers elonmusk -n 50     # First 50 followers
twitter -c following elonmusk -n 50     # First 50 following
```

#### list — Tweets from a Twitter List

```bash
twitter -c list 123456 -n 30           # Tweets from list by ID
```

#### article — Fetch a Twitter Article

```bash
twitter article 1234567890 -m           # As markdown
twitter article 1234567890 -m -o art.md # Save markdown to file
```

### Writing

#### post — Post a tweet

```bash
twitter -c post "Hello world"
twitter -c post "Check this out" -i photo.jpg           # With image
twitter -c post "Gallery" -i a.png -i b.png -i c.jpg    # Up to 4 images
```

#### reply — Reply to a tweet

```bash
twitter -c reply 1234567890 "Great thread!"
twitter -c reply 1234567890 "See this" -i screenshot.png
```

#### quote — Quote tweet

```bash
twitter -c quote 1234567890 "Interesting take"
```

### Engagement

```bash
twitter like 1234567890                 # Like
twitter unlike 1234567890               # Unlike
twitter retweet 1234567890              # Retweet
twitter unretweet 1234567890            # Undo retweet
twitter bookmark 1234567890             # Bookmark
twitter unbookmark 1234567890           # Remove bookmark
twitter follow username                 # Follow
twitter unfollow username               # Unfollow
twitter delete 1234567890               # Delete your tweet
```

### Account

```bash
twitter whoami                          # Your profile info
twitter status                          # Auth status check
```

---

## Output Format Rules

- **Always use `-c`** (compact) for readable, LLM-friendly output — **before the subcommand**
- **Use `--json`** when you need to process, analyze, or save structured data
- **Use `--json -o file.json`** when saving for later reference or cross-session use

## Workflows

For specific use cases, read the relevant workflow file:

- **`references/search-workflow.md`** — Find bookmarks about a topic, semantic filtering, save matching tweets as Obsidian notes
- **`references/classify-workflow.md`** — Tag all bookmarks, discover clusters, build an Obsidian vault with categories and wikilinks
- **`references/trading-research.md`** — Signal discovery, trader tracking, sentiment scans, acting fast on market information
- **`references/save-and-organize.md`** — Save individual tweets/threads, reference Twitter content in conversations

**Quick routing:**

| User wants... | Workflow |
|---------------|----------|
| "Find my bookmarks about X" | `search-workflow.md` |
| "Organize / classify / tag all my bookmarks" | `classify-workflow.md` |
| Find trading ideas, track traders, market sentiment | `trading-research.md` |
| Save a specific tweet/thread, reference content | `save-and-organize.md` |
| Simple CLI command | Use the Commands Reference above directly |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `not_authenticated` error | Re-login to x.com in browser, or set `TWITTER_AUTH_TOKEN` + `TWITTER_CT0` env vars |
| `No such option: -c` | `-c` is a global flag — put it BEFORE the subcommand: `twitter -c bookmarks` not `twitter bookmarks -c` |
| Keychain popups on macOS | Click "Always Allow" once per browser |
| Cookies expire | Re-extract by clearing env vars and restarting, or update env vars with fresh cookie values |
| Rate limited | Wait 15 minutes. Reduce `-n` values. |
