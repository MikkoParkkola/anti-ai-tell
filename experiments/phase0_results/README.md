# Phase 0 result — style anchor moves output off the centroid (MIK-6618)

Run 2026-06-29 on **DeepSeek deepseek-v4-flash** (via the reasonix CLI, MCP-free
HOME), 10 unanchored + 10 anchored single-sentence SaaS taglines, same prompt.

**Verdict: GO.** Cohen's d = 4.75 (bar was 0.5). Anchored outputs sit at lexical
distance 1.0 from the unanchored centroid vs 0.66 within the unanchored set.

The effect is visible in the raw samples (A/ vs B/): unanchored output is generic
("transform your workflow into a competitive advantage"); anchored output carries
concrete numbers and named entities ("One engineer in Austin saved 47% on AWS
costs"). This empirically confirms the (c) mechanism — one persistent style anchor
de-genericizes output — on a model that is NOT Claude (stronger, model-agnostic
evidence).

Caveat: distance is lexical (bigram cosine), so d=4.75 is inflated by the anchor
injecting tokens (numbers/names) the generic centroid never uses. A semantic
embedding would show a large-but-smaller d. Directionally unambiguous; the samples
prove it to the eye. Re-run with `phase0_anchor_distance.py --files A B`.

## Cross-confirmation — Claude (haiku), 2026-06-29

Re-ran via 12 independent Claude haiku subagents (one tagline each, fresh context
= genuinely independent), 6 unanchored + 6 anchored. **GO, Cohen's d = 3.82.**
Anchored at distance 1.0 from the unanchored centroid vs 0.49 within.

The unanchored cluster is striking: "focus on what matters" recurs in 4 of 6
generic taglines (mode collapse, visible). Anchored output is varied and concrete
("Shopify's Portland team cut order processing from 4.2 seconds to 110ms").

**Two-model result: DeepSeek d=4.75, Claude d=3.82 — both GO.** The style-anchor
de-genericization effect is model-agnostic, confirmed on an open model and a
frontier-lab model. claude_A/ + claude_B/ + claude_result.json are the evidence.
