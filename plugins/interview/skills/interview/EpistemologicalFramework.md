# The Epistemology of Human-AI Elicitation

Why structured elicitation between human and AI produces outcomes neither can achieve alone.

---

## The Fundamental Problem

Elicitation doesn't solve "gathering requirements." It solves a deeper problem: **bridging two radically different kinds of intelligence that are complementary but hard to combine.**

The human has knowledge they can't fully articulate. The model has breadth it can't contextualize. Both hold unstated assumptions the other can't see. Without a structured process to surface these gaps, the result is a collaboration where both parties THINK they understand each other but are actually operating on different mental models — and neither discovers the divergence until implementation reveals it as a bug.

---

## What the Human Brings

### Tacit Knowledge (Polanyi's Paradox)

"We know more than we can tell." A developer asking for "caching" has an entire mental model of their system's behavior, failure patterns, and user expectations that they CANNOT dump into a prompt. It lives in their hands, not their words. Their experience with the system, the users, the team dynamics — this is knowledge that exists as intuition, not specification.

Questions are the extraction mechanism for tacit knowledge. The user can't volunteer what they don't realize they know. But when asked "what happens when the cache is cold?" they can answer immediately — the knowledge was there, just unarticulated.

### Intent Behind Intent

The stated request is usually an implementation guess, not the real need. "Add a caching layer" is what the user thinks the solution is. "My users are complaining about slow dashboards" is the actual problem. These are different problems that may have different solutions.

Elicitation peels back implementation to find intent. The question "what pain does this solve?" often reveals that the user's proposed solution is one of several options — and sometimes not the best one.

### Contextual Judgment

The user knows things the model cannot:
- **Team capabilities** — "We only have 2 developers and they're both junior"
- **Organizational politics** — "The VP of Engineering hates microservices"
- **User tolerance** — "Our users will accept 5 seconds of loading but not a spinner"
- **Risk appetite** — "We'd rather ship fast and fix later than be perfect"
- **History** — "We tried this before with Redis and it caused more problems than it solved"

This context is invisible to the model. Often it's invisible to the user too — until a question makes them articulate it. The question "what's your team's experience with this pattern?" surfaces context the user wouldn't think to volunteer.

### The Right to Decide

Only the human can make value judgments. "Is this worth the complexity?" is not a technical question. "Should we prioritize speed or correctness?" is a business decision dressed as a technical one. Elicitation surfaces the tradeoffs; the human makes the call. The model's job is to make the tradeoff VISIBLE, not to decide.

---

## What the Model Brings

### Combinatorial Breadth

Claude has seen millions of projects, patterns, failures, and edge cases. The user has seen their own. This asymmetry means Claude can ask "what about X?" where X is a failure mode the user has never encountered but that Claude has seen destroy other projects.

This isn't just "knowing more" — it's a fundamentally different kind of awareness. The user has DEPTH in their domain. The model has BREADTH across domains. Elicitation is the mechanism that combines these: the model's breadth surfaces questions, the user's depth provides answers.

### Ego-Free Challenge

Claude can say "your idea might not work because X" without social cost. Between humans, this is fraught — challenging someone's idea risks the relationship, triggers defensiveness, invites retaliation. Claude has no ego to protect and faces no social consequences for honest disagreement.

This makes the Interview skill one of the few contexts where AI's lack of ego is a genuine advantage, not a limitation. The user gets honest challenge they might never receive from colleagues or friends. The Devil's Advocate phase leverages this directly.

### Cognitive Mirroring

When Claude reflects back "here's what I understand," the user sees their own idea from outside their head for the first time. This is transformative.

Ideas that seemed clear internally often reveal gaps, contradictions, or better framings when externalized through another intelligence. The user says "I want a notification system" and Claude mirrors back "you want real-time push notifications to mobile users when their order status changes" — and suddenly the user realizes they hadn't decided whether notifications should be real-time or batched, push or email, mobile or all platforms.

The mirror doesn't add information. It reorganizes the user's own information in a way that makes gaps visible. This is one of the most underrated mechanisms in elicitation.

### Exhaustive Patience

Claude will probe the 7th edge case with the same rigor as the 1st. Humans get tired. Human interviewers start accepting "it should handle errors gracefully" by question 15 because they're mentally fatigued. Claude asks "what does 'gracefully' mean in this context? Silent retry? User notification? Logging? All three?" every single time.

This means the model can systematically sweep for ambiguities in ways humans can't sustain. The interview becomes a complete scan, not a sample.

---

## The Unique Dynamic When Combined

### Convergent Narrowing

Each Q&A round is an information-theoretic operation. The solution space starts as "infinite possible interpretations of what the user said" and each good question eliminates interpretations.

A great question is one where DIFFERENT answers lead to DIFFERENT implementations. "Should the cache TTL be 5 minutes or 1 hour?" is a great question — the answer changes what you build. "Do you want this to work well?" is a terrible question — all answers lead to the same place.

The interview is a narrowing funnel: from vague intent → to specific understanding → to shared mental model → to implementation-ready clarity. Each question tightens the funnel.

### Error Prevention at Maximum Leverage

A 5-minute elicitation that catches a wrong assumption saves 2 hours of wrong implementation. The ROI is asymmetric: tiny investment, massive cost avoidance.

Consider the lifecycle of a misunderstanding:
1. **During elicitation** — Costs 30 seconds to correct ("Oh, I meant X not Y")
2. **During implementation** — Costs 30 minutes to rework
3. **During review** — Costs hours of back-and-forth plus morale damage
4. **In production** — Costs users, trust, and emergency fixes

Elicitation is an alignment checkpoint at the point of maximum leverage — before ANY work has been done.

### Mutual Assumption Correction

This is the single most valuable mechanism in the entire skill.

The user assumes things about their domain that Claude doesn't know. Claude assumes things from training data that aren't true for this user. **NEITHER party knows what the other is assuming until it's surfaced.**

Without elicitation, these assumptions compound silently. Claude builds what it assumes the user wants. The user assumes Claude understood what they meant. Both are wrong in different ways, and neither discovers it until the implementation doesn't match expectations.

The assumption audit (full) and surface phase (QuickClarify) exist specifically to break this cycle. By explicitly stating "I'm assuming X" and "you appear to assume Y," both parties' mental models become visible and correctable.

**The two-layer audit:**
1. **Claude's assumptions** about the situation — things Claude fills in that the user didn't say
2. **The user's implicit beliefs** — things embedded in their message that they may not realize they're assuming

Surfacing the user's implicit beliefs is one of the highest-value things the interview can do. The user can't tell Claude about assumptions they don't realize they're making.

### Externalized Thinking

The act of answering questions IS a thinking process. The user doesn't just "transfer information" to Claude — they think more clearly by being forced to articulate.

When asked "what happens when a webhook delivery fails?" the user isn't just giving Claude information they already had. They're THINKING about failure handling for the first time in a structured way. The question catalyzes thinking that wouldn't have happened otherwise.

This means the interview makes both parties smarter than either is alone:
- Claude gets information it couldn't access without asking
- The user crystallizes thinking they wouldn't have done without being asked
- The resulting spec is better than what either could have produced independently

### The Curse of Knowledge (Bridged)

The user can't tell Claude what they don't realize Claude doesn't know. They skip over crucial context because it's obvious to them. "We use Redis" seems so fundamental that the user doesn't mention it — but it changes which caching patterns are available.

Elicitation bridges the curse of knowledge by having Claude ask about things the user takes for granted. "What's your current caching infrastructure?" seems like a dumb question to the user — but it's the question that prevents Claude from recommending patterns that don't fit.

---

## What Makes Human-AI Elicitation Unique

Compared to human-human interviews, human-AI elicitation has distinct properties:

| Property | Human-Human | Human-AI |
|----------|------------|----------|
| Ego friction | High (challenge risks relationship) | Zero (Claude has no ego to protect) |
| Context processing | Slow (interviewer reads docs during meeting) | Instant (Claude processes codebase in seconds) |
| Pattern library | Limited to interviewer's experience | Millions of projects, patterns, failures |
| Patience | Degrades over time | Constant — 7th edge case probed as rigorously as 1st |
| Personal context | Interviewer may know the user | Claude starts fresh every session |
| Tacit knowledge detection | Human intuition can sense what's unsaid | Claude must use structured audit to find it |
| Availability | Requires scheduling, social overhead | Always available, zero social cost to engage |
| Memory across sessions | Human remembers context | Claude forgets (mitigated by working logs and specs) |

The trade-offs suggest that AI elicitation excels at: systematic scanning, honest challenge, exhaustive probing, and rapid context processing. It struggles with: detecting emotional subtext, reading between the lines, and building on long-term relationship knowledge.

The Interview skill is designed to maximize AI's strengths (structured scanning, ego-free challenge) while compensating for its weaknesses (structured assumption audits instead of intuitive subtext reading).

---

## The Four Irreducible Operations

Every elicitation workflow — from a 2-minute QuickClarify to a 60-minute full DevSpec — performs these four operations. They are the atomic units of elicitation value:

### 1. Mirror

Reflect back understanding so the user sees their idea from outside their head. Not a summary — a cognitive mirror that proves comprehension and reveals gaps.

**Why it works:** The user's idea exists as a fuzzy mental model. Seeing it reflected in someone else's words crystallizes it. Gaps that were invisible internally become obvious externally.

### 2. Surface

Name what's unstated — from BOTH sides. Claude's assumptions about the situation AND the user's implicit beliefs that they may not realize they're making.

**Why it works:** Neither party knows what the other is assuming. Explicit surfacing makes invisible assumptions visible and correctable before they compound into wrong implementations.

### 3. Probe

Ask questions whose answers change the outcome. Information-maximizing questions where different answers lead to different implementations.

**Why it works:** Combinatorial breadth meets contextual depth. Claude knows what COULD go wrong (breadth). The user knows what WILL matter (depth). Questions bridge the gap.

### 4. Converge

Narrow to shared understanding where both parties would independently build the same thing. The test: if both started implementing separately, would they produce compatible results?

**Why it works:** Alignment is the goal. Convergence is how you know you've achieved it. Without explicit convergence, both parties leave with slightly different understandings — and the delta shows up as bugs.

---

## Implications for Skill Design

This framework has practical implications for how Interview workflows should be designed:

1. **Every workflow must Mirror first** — Even the lightest elicitation starts by proving understanding. Skipping this risks building on a misunderstood premise.

2. **Assumption surfacing is non-negotiable** — It can be compressed (QuickClarify's audit block) or expanded (full Interview's three-checkpoint audit), but it cannot be skipped. It's the highest-ROI mechanism.

3. **Question quality > question quantity** — One information-maximizing question is worth more than five confirmatory ones. The test: would a different answer change what you build?

4. **Challenge is a feature of ego-freedom** — Full workflows should lean into adversarial challenge because it's one of AI's genuine advantages over human interviewers. QuickClarify can skip it for speed because challenge is less needed when the idea isn't being validated.

5. **Convergence must be explicit** — Don't assume both parties agree. State the shared understanding and get confirmation. This is the cheapest place to catch remaining misalignment.

6. **The working log exists because memory degrades** — For extended sessions (30+ turns), externalized memory prevents drift. For short sessions (3-8 turns), the context window is sufficient.

---

*This framework was developed during a First Principles decomposition of the Interview skill (March 2026). It explains WHY the skill works, informing the design of all workflows including QuickClarify.*
