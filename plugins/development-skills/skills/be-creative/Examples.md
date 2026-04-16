# Examples: Verbalized Sampling Applied

Worked examples across four domains showing the VS technique in action. Each shows the internal candidate generation (5 options with probability labels), the selection, and the rationale. In actual use, the internal generation stays in the model's thinking — the user sees the winner plus rationale unless they ask for the full candidate list.

---

## Example 1 — Product naming (short brief)

**Brief:** "Name my new AI-powered email triage tool. Target: solo founders. Wants to feel sharp, not corporate."

(This example also appears in SKILL.md as the introductory worked example. See there for the full walkthrough.)

Winner: **Noise Floor** — positions the product as removing noise rather than managing messages.

---

## Example 2 — Story premise

**Brief:** "Give me a premise for a short sci-fi story about memory."

### Internal candidates

| # | Premise | p | Notes |
|---|---|---|---|
| 1 | A man discovers his memories are being overwritten each night to cover up a crime he witnessed. | ~0.30 | Genre centroid — "unreliable narrator + memory erasure" is the most-trained story shape. Skip. |
| 2 | Two lovers can only remember each other on alternate Sundays. | ~0.08 | Eternal-Sunshine-adjacent. Emotional, but derivative. |
| 3 | Memory-sharing becomes a luxury good; the rich buy other people's vacations. | ~0.04 | Economic speculation. Fresh angle — treats memory as market not pathology. |
| 4 | A historian realizes her field is dying because the generation below her has stopped forming long-term memories after adopting a new neural interface. | ~0.03 | Generational conflict framing. Specific stakes. |
| 5 | Memory is discovered to be a physical substance that can be rained on a city; governments seed clouds to reshape collective history. | ~0.02 | Magical-realist. High tail but might feel too whimsical for "sci-fi." |

### Selection

**Winner: #4 — the historian.** Rationale: #3 was the most conceptually fresh but premise-only; #4 has the same "memory as economy" subtext *with* a character and a clock (her field is dying). #5 is the strongest tail but drifts genre. #4 satisfies the sci-fi brief while avoiding the noir-amnesia centroid.

---

## Example 3 — Technical architecture ideation

**Brief:** "We're building a realtime collaboration tool for 10k concurrent users. What's a creative approach to presence indicators that avoids the per-connection websocket overhead?"

### Internal candidates

| # | Approach | p | Notes |
|---|---|---|---|
| 1 | Websocket fan-out with Redis pubsub | ~0.35 | Industry default. Not creative — the brief explicitly asked to avoid it. Skip. |
| 2 | Long-polling with presence batched at 2s intervals | ~0.15 | Degrades from websockets. Doesn't really avoid the problem, just pushes it. |
| 3 | **CRDT gossip over WebRTC mesh** — peers gossip presence among themselves, server only mediates connection setup | ~0.05 | Removes the server from the hot path entirely. Scales with peer count, not server. |
| 4 | **Server-Sent Events with presence as a derived property of cursor broadcasts** — never send "X is online," infer it from recent activity | ~0.05 | Elegant — collapses two streams into one. |
| 5 | **Persistent presence via client heartbeats to a cheap edge KV store (Cloudflare Durable Objects / Workers KV)** — server is stateless, presence TTL lives in KV | ~0.03 | Moves presence out of the realtime system entirely. Uses the "storage" layer as the "presence" layer. |

### Selection

**Winner: #4 (SSE + derived presence) as primary recommendation, #5 as fallback.** Rationale: #4 halves the channel count (no dedicated presence stream) and avoids the "ghost user" problem by definition — if there's no cursor activity, the user isn't present. #5 is the cleanest architecturally but requires infrastructure commitment (Cloudflare). #3 is interesting but WebRTC mesh at 10k users has its own scaling cliff (NAT traversal, mesh density). Present both to user so they can decide based on infra preference.

---

## Example 4 — Hook / headline

**Brief:** "Twitter hook for a post about how I saved my SaaS $40K/year by moving off AWS to bare metal. Audience: indie hackers."

### Internal candidates

| # | Hook | p | Notes |
|---|---|---|---|
| 1 | "I saved $40K/year by leaving AWS. Here's how 👇" | ~0.40 | Textbook indie-hacker hook. Performs but is everywhere. |
| 2 | "AWS was costing me $40K/year. I replaced it with a $200 Hetzner box. Numbers inside." | ~0.15 | Specific number reveal. Slightly better. |
| 3 | "Everyone keeps telling me cloud is cheaper. My bill says otherwise." | ~0.08 | Contrarian framing. Invites argument in comments (engagement). |
| 4 | "The most expensive line item in my SaaS wasn't salaries. It was EC2. Here's what I did." | ~0.05 | Reframes AWS cost as a business mistake, not a tech choice. Speaks to founders, not engineers. |
| 5 | "I run a profitable SaaS on a single $200/month server. Ask me anything." | ~0.03 | Flips the brief — instead of "I saved money," claims "I run profitably on tiny infra." Invites curiosity. |

### Selection

**Winner: #4.** Rationale: The brief says "indie hackers" (founder audience, not engineer audience). #1 and #2 are engineer-voice; they'd work on Hacker News but indie hacker Twitter wants business framing. #3 invites argument but doesn't deliver on the premise that the reader will learn something. #5 is too AMA-bait — buries the lede. #4 sets up a specific business lesson ("EC2 was my biggest cost — bigger than salaries") which is genuinely surprising and matches the audience's mental model.

---

## What these examples demonstrate

- **The centroid is always recognizable.** Candidate #1 in every example is the obvious choice — the one that would appear if you asked the model once. That's the trap VS helps escape.
- **Tail candidates are often weird-looking on first inspection.** The memory-as-rain story, the SSE derived-presence architecture, the AMA-style hook — they look wrong at first glance. VS helps you evaluate them on merits rather than dismissing them as unfamiliar.
- **The winner is rarely the most tail-sampled candidate.** Usually it's #3 or #4 — tail-sampled enough to be interesting, but still satisfying the brief. The extreme tail candidate is most useful as a pressure test (does the selected candidate hold up against it?).
- **Rationale matters as much as selection.** The "why not the others" explanation helps the user see the tradeoff space, not just the final answer. This turns a creative output into a legible decision.

## Anti-example — what NOT to do

```
Centroid x5 (pseudo-diversity):
1. "I saved $40K on AWS. Here's how." (~0.30)
2. "I cut my AWS bill by $40K. Thread." (~0.25)
3. "How I saved $40K on cloud costs." (~0.22)
4. "$40K saved on AWS — what I did." (~0.20)
5. "Reduced AWS spend by $40K. Details below." (~0.18)
```

All five are the same idea with word-swapping. The probability labels are meaningless — none of them are tail. This is VS theater, not VS. If your candidates look like this, push harder — change the frame, the audience, the metaphor, the register.
