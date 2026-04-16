# Workflow: Trading Research

Use these patterns when the user wants to find, track, or act on trading information from Twitter/X. FinTwit (financial Twitter) is one of the fastest sources of trading ideas, sentiment shifts, and market-moving information.

## Signal Discovery

Find what traders are talking about right now:

```bash
# What's hot in trading Twitter
twitter -c search "trading strategy" -t latest -n 30
twitter -c search "$SPY $QQQ" -t latest --min-likes 50

# Specific asset or strategy
twitter -c search "$TSLA options" -t latest --has links
twitter -c search "mean reversion" --min-likes 100 --since <recent-date-ISO>

# Filter noise — skip retweets and replies to get original takes
twitter -c search "momentum strategy" -t latest --exclude retweets --exclude replies
```

## Track Specific Traders

When the user names a trader or analyst they follow:

```bash
# Recent posts from a trader
twitter -c user-posts tradername -n 30

# What are they saying about a specific topic?
twitter -c search "options" --from tradername -t latest

# Save their recent output for analysis
twitter user-posts tradername --json -n 50 -o trader_posts.json
```

## Bookmark Mining for Trading Ideas

The user bookmarks tweets throughout the day. Help them extract value:

```bash
# Pull recent bookmarks
twitter -c bookmarks -n 50

# Save for structured analysis
twitter bookmarks --json -n 100 -o bookmarks.json
```

After pulling bookmarks, **read the JSON and categorize** by:
- Asset class (equities, options, crypto, forex)
- Strategy type (momentum, mean reversion, breakout, macro)
- Actionability (immediate setup, watchlist, educational)
- Source quality (track record, follower count, engagement)

Present a summary: "You bookmarked 47 tweets. Here's the breakdown..."

## Save a Trading Idea

When the user finds a tweet or thread worth preserving:

```bash
# Pull the full tweet with replies (often has follow-up context)
twitter -c tweet <id_or_url> -n 20

# Save as JSON for structured storage
twitter tweet <id_or_url> --json -o saved_tweet.json

# For Twitter Articles (long-form analysis)
twitter -c article <id_or_url> -m -o analysis.md
```

After saving, summarize what was saved and why it might be valuable: the setup, the thesis, any specific levels or timeframes mentioned.

## Market Sentiment Scan

Quick read on what trading Twitter thinks about a topic:

```bash
# Broad sentiment on an asset
twitter -c search "$AAPL" -t latest -n 50 --exclude retweets

# Bearish/bullish signal words
twitter -c search "$SPY puts" -t latest -n 30
twitter -c search "$SPY calls" -t latest -n 30

# Macro sentiment
twitter -c search "fed rate cut" -t latest --min-likes 20
twitter -c search "recession" -t latest --min-likes 50
```

After pulling, analyze: What's the dominant sentiment? Are there contrarian voices? Any specific levels or dates being discussed? Any consensus trades forming (which can be a contrarian signal)?

## Acting Fast

When speed matters — the user sees something and wants to capture or share immediately:

> **⚠️ Permission required for posting.** Any `twitter post`, `reply`, or `quote` command publishes to the user's Twitter account. Ask for explicit confirmation before running write commands — never infer permission from a prior read command. When in doubt, show the drafted tweet and wait for "yes, post it".

```bash
# Quick save a tweet they just saw
twitter bookmark <tweet_id>

# Quick share/amplify a signal
twitter retweet <tweet_id>
twitter -c quote <tweet_id> "Adding to watchlist — setup looks clean"

# Post their own take
twitter -c post "$TSLA breaking above 200 SMA on volume. Watching for retest."
```

## Combining with Other Tools

The real power is using twitter-cli output as input for analysis:

1. **Pull data** → `twitter search "$SPY" --json -n 100 -o spy_sentiment.json`
2. **Analyze** → Read the JSON, extract themes, count bullish vs bearish
3. **Cross-reference** → Compare Twitter sentiment with price action data
4. **Save findings** → Write a structured analysis file the user can reference later
5. **Discuss** → Present findings and ask the user what they want to dig into

Always offer to save interesting findings to a file the user can reference later.
