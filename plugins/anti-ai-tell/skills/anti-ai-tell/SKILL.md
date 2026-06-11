---
name: anti-ai-tell
description: Make written prose not read as AI-generated, even when it is. Three-tier discipline. Tier 0 prevents AI-ese at generation time (voice constraints, banned vocabulary, rhythm rules). Tier 1 is a mechanical lint pass (lint.py) catching measured tells - banned words, em-dashes, negative parallelism, uniform rhythm, copulative avoidance, vague attribution. Tier 2 is the judgment pass that actually matters - visible reasoning, anti-sycophancy, concreteness, committed stance, intellectual friction. Use BEFORE shipping any external-facing or human-read prose - investor notes, public READMEs and issue bodies, marketing copy, blog posts, docs, customer email. Triggers - write, draft, edit, rewrite, copy, email, post, blog, README, announcement, "sound human", "doesn't sound like AI", "humanize", ship external prose.
triggers: doesn't sound like ai|sound human|humanize|anti-ai-tell|ai tell|reads like ai|written by ai|external copy|marketing copy|blog post|readme|announcement|ship this prose|edit this draft
effort: medium
version: 2026.06.11-v2
---

# anti-ai-tell — prose that doesn't broadcast its origin

## The doctrine, in three findings

1. **Surface tells are necessary but no longer sufficient.** Readers and tutorials
   already strip em-dashes, colons, and "It's not X; it's Y." What survives the
   scrub is the absence of a mind at work.
   Source: Eve Fairbanks, *The Atlantic*, "The Biggest Tell That Something Was
   Written by AI" (2026-05-29),
   https://www.theatlantic.com/technology/2026/05/how-to-tell-ai-writing/687345/
   — *"writing that can't really be argued with, because it has no underlying
   deliberative reasoning process, no train of thought."* And the editor's view:
   *"every element is equally off: The tone is bland; individual word choices
   are baffling; the structure lacks sense."* Jason Koebler (404 Media) puts the
   same gestalt in one line: *"The tell for AI isn't rhythm, wording, or fact
   errors. It's that problems with all these elements exist equally & at once."*

2. **The vocabulary tell is real and measured.** Corpus studies put hard numbers
   on AI-ese: *delves* at 28× expected frequency, *underscores* 13.8×,
   *showcasing* 10.7× (Kobak et al., Science Advances 2025, arXiv 2406.07016);
   *meticulous* 34.7×, *intricate* 11.2×, *commendable* 9.8× in LLM-assisted
   peer reviews (Liang et al., ICML 2024, arXiv 2403.07183). Adjectives are the
   most stable single signal. The lists drift by model era (delve → showcasing →
   emphasizing), so `data/vocabulary.json` is era-tagged and versioned.

3. **Against robust detectors, only distributional change works.** Word-swapping
   defeats humans and frequency-based detectors; perplexity-ratio detectors
   (Binoculars, arXiv 2401.12070: >90% detection at 0.01% FPR) key on text being
   *too probable and too smooth*. The counters that measurably work are lexical
   diversity + clause reordering (DIPPER, arXiv 2303.13408: DetectGPT 70.3% →
   4.6%) and variance injection — surprising word choices, mixed sentence
   lengths, non-templated structure. Conveniently, those are the same things
   that make prose read human to people.

**Operator directive (2026-06-06)**: portfolio prose must not read as
AI-written, even when it is.

---

## Scope — composes with ELITE voice, does NOT replace it

- **Internal candor (ELITE voice)**: Linear tickets, strategy memos, session
  reasoning, anything operator-only. Em-dashes and antithesis are fine there.
- **External / human-read (this skill)**: investor + partner + recruiting copy,
  public GitHub (READMEs, issue + PR bodies), marketing, blog, docs, customer
  email, outward-facing living-doc sections.
- When in doubt: if a stranger could read it and judge the author, it's
  external. Apply the full ruleset.

---

## Tier 0 — generation-time constraints (prevent, don't repair)

Embed these in the system prompt / instruction block BEFORE drafting. Cheaper
than editing AI-ese out afterward. The block lives in
`adapters/SYSTEM_PROMPT.md` for non-Claude clients.

1. **Banned vocabulary**: never use the `hard_ban` list from
   `data/vocabulary.json` (delve, tapestry, showcase, underscore, meticulous,
   realm, game-changer...). Treat `strong_flag` words as rationed: one per
   document, with cause.
2. **Rhythm**: mix sentences under 10 words with sentences over 20. Never three
   consecutive sentences of similar length. Vary paragraph length; a
   one-sentence paragraph is allowed to land a point.
3. **No em-dashes. No "not X, but Y" constructions.** Use commas, periods,
   parentheses; make the positive assertion directly.
4. **Plain copulas**: write "is", "are", "has" instead of "serves as",
   "stands as", "boasts", "represents".
5. **Concreteness**: every abstract claim gets a number, a name, or an example
   within two sentences. If none exists, flag `[NEEDS EXAMPLE]` rather than
   padding.
6. **No throat-clearing, no closing bows**: delete "It's worth noting",
   "In today's world", "In conclusion". Start where the point starts; stop
   where it ends.
7. **Take a position**: where the material supports a judgment, state it and
   defend it. No symmetric "on the one hand" hedging unless genuinely undecided
   — and then say *why* undecided.
8. **Register match**: these rules tune for directness; formal/academic targets
   keep necessary passives and looser sentence-length rules. Genre overrides
   the defaults, deliberately.
9. **Voice grounding**: when a house voice exists, paste 2-3 paragraphs of real
   prior writing as a few-shot anchor.
10. **Self-review tail**: end the instruction with "Before finishing, re-scan
    the output for em-dashes, banned words, and three similar-length sentences
    in a row; fix what you find." A cheap built-in second pass.

## Tier 1 — mechanical lint (run `lint.py`, fix everything it flags)

```sh
python3 lint.py DRAFT.md            # docs/READMEs (markdown allowed)
python3 lint.py DRAFT.txt --prose   # emails/posts (markdown flagged too)
python3 lint.py DRAFT.md --json     # machine-readable, CI-gateable
```

| ID | Tell | Measured basis |
|----|------|----------------|
| S1 | Em-dash overuse | Fairbanks names it the #1 stripped tell |
| S2 | Negative parallelism ("not just X, but Y") | Russell et al. ACL 2025 via WP:AISIGNS |
| S3 | Uniform sentence rhythm (CV < 0.45; runs of 4) | Muñoz-Ortiz 2024: humans have scattered length distributions |
| S4 | Evenly paced paragraphs (CV < 0.30) | Fairbanks: "uniform in length, with evenly paced paragraphs" |
| S5 | Throat-clearing openers | practitioner consensus |
| S6 | Connective filler (moreover, furthermore...) | Kobak common-set excess |
| S7 | Closing-bow wrap-ups ("In conclusion...") | WP:AISIGNS formulaic conclusions |
| S8 | Banned vocabulary, era-aware | Kobak r=28/13.8/10.7; Liang 34.7×/11.2×/9.8× |
| S9 | Copulative avoidance ("serves as", "boasts") | Geng & Trotta: >10% drop in plain is/are |
| S10 | Rule-of-three compulsion | WP:AISIGNS triad habit |
| S11 | Vague attribution ("studies show") | WP:AISIGNS; name the source instead |
| S12 | Markdown artifacts in prose (opt-in) | practitioner consensus for plain-prose targets |
| S13 | Density-watch clusters (crucial/comprehensive/notably...) | Kobak best-10 marker set, Δ=0.134 |

A clean lint pass means the cheap tells are gone. It does NOT mean the prose
reads human. Proceed to Tier 2.

## Tier 2 — the judgment pass (where the actual tell lives)

Five questions, asked of the draft as a whole. These cannot be linted; they are
the Fairbanks layer.

1. **Is the reasoning visible?** Can a reader reconstruct *why* each claim
   follows? If a paragraph could be deleted without breaking an argument chain,
   it's decoration. Show the work: "X, because Y, despite Z."
2. **Does it ever push back?** Human thought has friction: a doubt voiced, a
   counterargument taken seriously, a premise questioned, an earlier sentence
   corrected. Sycophantic agreement with the reader's assumed view is the
   single deepest tell (models affirm users ~49% more than humans do —
   *Science*, via Fairbanks). One honest "this might be wrong because..."
   outweighs ten scrubbed em-dashes.
3. **Is anything concrete?** Names, numbers, dates, places, one specific
   anecdote. AI pads with abstractions because abstractions can't be wrong.
   Editors rate "inject one concrete example per abstract paragraph" the
   highest-value single edit.
4. **Does it commit?** A verdict, a ranking, a recommendation with a reason.
   Symmetric hedging ("there are pros and cons") is machine neutrality.
5. **Would the author recognize themselves?** Idiosyncrasy is the human
   signature: a pet phrase, an odd-but-apt metaphor (only fresh ones — never
   stock), a structural choice a style guide would frown at. Language-flattening
   is itself a tell (Turk, *The Atlantic*, 2025-04-29).

**Anti-perfection note**: do NOT inject typos as fake authenticity. The honest
version of the same signal is unpolished *structure* — a thought that visibly
develops rather than arrives pre-assembled.

## Workflow

1. Draft with Tier 0 constraints in the prompt (or rewrite an existing draft
   against them).
2. Run `lint.py`; fix every finding; re-run until clean.
3. Do the Tier-2 hand-pass; revise.
4. For high-stakes prose: read it aloud once. The ear catches uniform meter the
   eye forgives.

## Maintenance

The vocabulary lists rot as models change. Refresh `data/vocabulary.json` from
Wikipedia's WP:AISIGNS era tables and new Kobak-style corpus studies; bump the
`updated` field. Era notes in the JSON show the drift history.
