#!/usr/bin/env python3
"""UserPromptSubmit hook: nudge the gap-quiz when a design task lacks a fingerprint.

This is the home for the operator's "ask the user about the style when needed"
(active-ask). The hook cannot ask directly; it detects (a) a design intent in the
prompt and (b) unfilled fingerprint slots, and nudges the agent to run the
derive-then-confirm quiz via AskUserQuestion before generating centroid defaults.

Fires only when both conditions hold, so it stays quiet on non-design turns.
Zero deps.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent / "skills" / "anti-ai-tell"
DESIGN_RX = re.compile(
    r"\b(design|ui|landing page|website|logo|brand|deck|slide|presentation|"
    r"component|dashboard|hero|css|tailwind|theme|mockup|style|color|palette|font)\b",
    re.I,
)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    prompt = payload.get("prompt") or payload.get("user_prompt") or ""
    if not DESIGN_RX.search(prompt):
        return 0

    sys.path.insert(0, str(SKILL))
    try:
        import fingerprint as fpmod  # noqa
    except Exception:
        return 0
    fp_path = Path.cwd() / "fingerprint.json"
    fp = fpmod.load(fp_path if fp_path.exists() else None)
    gaps = fpmod.gaps(fp)
    if not gaps:
        return 0

    qs = "; ".join(q for _, q in gaps[:3])
    nudge = ("anti-ai-tell: this looks like a design task and the style fingerprint "
             f"has {len(gaps)} unset slot(s). Before generating defaults, ask the user "
             f"via AskUserQuestion: {qs}. Persist answers to fingerprint.json so you "
             "never re-ask.")
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": nudge,
    }}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
