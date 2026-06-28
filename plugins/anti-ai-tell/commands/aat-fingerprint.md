---
description: Build or update the style fingerprint via derive-then-confirm.
---

Seed or refine the user's `fingerprint.json` — the single source of truth for
their chosen point of view, the cure for generic AI design.

Derive-then-confirm (the chosen seeding flow):

1. **Derive.** If the user points at an existing artifact (a site, CSS, deck, or
   writing sample), run
   `python3 ${CLAUDE_PLUGIN_ROOT}/skills/anti-ai-tell/fingerprint.py derive <file>`
   to extract whatever slots it can read (fonts, accent, radius, mode).
2. **Confirm.** Run
   `python3 ${CLAUDE_PLUGIN_ROOT}/skills/anti-ai-tell/fingerprint.py gaps`
   to list the unset slots, then ask the user about ONLY those, via
   AskUserQuestion (e.g. accent lane: warm/cool/mono/bold). Keep it to 3-5 taps.
3. **Persist.** Write the merged result to `fingerprint.json` in the repo root.
   Validate with `fingerprint.py validate fingerprint.json`. Never re-ask a slot
   that's already set.

If the user has no artifacts and no preferences yet, print the ELITE seed
(`fingerprint.py seed`) as a starting point and let them edit.
