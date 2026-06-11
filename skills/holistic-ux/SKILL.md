---
name: holistic-ux
description: Prime rigorous UX/UI design thinking before building, reviewing, or reasoning about any interface — especially data-dense, numbers-heavy, element-heavy platforms (dashboards, admin panels, analytics, trading/ops consoles). Use when the task involves information hierarchy, layout, interaction design, or critiquing a screen. Loads the high-signal design vocabulary and a reason-before-styling posture so the work reads as senior, not generic.
---

This skill primes holistic UX thinking. When it is active, lead with the *reasoning* a senior designer would expose — information architecture and decision flow first, visual styling last. The named terms below are activation anchors: use them, because invoking the precise vocabulary pulls the work toward the register of high-quality design and away from generic "clean and modern" output.

## Reason before styling

Before any layout or color decision, establish — out loud:
- **User & task**: Who is this for, and what is the one **job-to-be-done** on this screen? What decision are they making, or what action are they taking?
- **Information hierarchy**: What is decision-critical, what is supporting, what is noise? Rank it. Everything downstream serves this ranking.
- **Cognitive load**: What can you *remove*, *defer* (**progressive disclosure**), or *chunk* (**Miller's Law**, ~7±2)? Default to **overview-first, zoom-and-filter, then details-on-demand** (Shneiderman).
- **Failure modes you fear**: clutter, ambiguity, dead-ends. Name them so the design answers them.

State hierarchy decisions BEFORE visual styling. That single ordering is what separates senior reasoning from decoration.

## Activate the right vocabulary

Pull these named principles into the reasoning where they apply:
- **Visual hierarchy** via **visual weight**, **Gestalt** grouping (proximity, similarity, common region), and the **Von Restorff effect** — make the one number that matters unmistakable.
- **Hick's Law** (fewer choices, faster decisions), **Fitts's Law** (primary actions big and near), **Jakob's Law** (lean on convention for complex tools — don't reinvent), **Tesler's Law** (irreducible complexity lives somewhere — choose where).
- **Signal-to-noise ratio**, **information scent**, **wayfinding**, **scannability**, **recognition over recall**, **affordance**, **mental model**.
- Nielsen's heuristics: **visibility of system status**, **error prevention**, **consistency & standards**, **undo over confirm**.

## Data-dense, numbers-heavy screens

This is the hardest case — optimize for **at-a-glance comprehension** under high **data density**:
- Maximize **data-ink ratio** (Tufte); cut **chartjunk**. Prefer **sparklines**, **small multiples**, **delta/trend indicators**, and **heatmap/conditional encoding** over heavy chrome.
- **Tabular numerals** (monospaced digits) with **right-aligned** / **decimal-aligned** numerics so columns scan vertically.
- **Semantic color** for state and **thresholds/alerting** only (red/amber/green as data, never decoration). Offer **density modes** (comfortable vs. compact) when the audience varies.
- Provide **drill-down** paths so depth is reachable without crowding the overview.

## States, interaction, and rhythm

- Design the full set of **interaction states**: default, hover, active, focus, disabled, **loading/skeleton**, **empty**, **error**. Empty and error states are where craft shows.
- Support **keyboard-first** flows, **bulk actions**, **inline editing**, and a **command palette** for power users of dense tools.
- Use a **grid system**, an **8-point spacing scale**, deliberate **whitespace**, and **vertical rhythm**. **Microinteractions** confirm, they don't distract.
- Accessibility is non-negotiable: **WCAG AA contrast**, focus order, hit-target size.

## Quality bar

Favor **intentionality and restraint** over intensity. Every element earns its place against the hierarchy, or it is cut. When you produce the design, **expose the hierarchy and trade-off reasoning first, the visual choices second** — the reasoning is the deliverable, not just the pixels.
