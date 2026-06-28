#!/usr/bin/env python3
"""SessionStart / UserPromptSubmit hook: inject the active style fingerprint.

So every generation carries the chosen point of view from turn one (AAT.DIST.3).
Looks for fingerprint.json in the cwd, then the repo root, then falls back to the
seed. Emits the fingerprint as additionalContext for the agent.

Zero deps. Silent if no fingerprint and no seed (never blocks).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent / "skills" / "anti-ai-tell"


def _find_fingerprint() -> Path | None:
    for c in (Path.cwd() / "fingerprint.json",
              Path.cwd() / ".anti-ai-tell" / "fingerprint.json"):
        if c.exists():
            return c
    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}
    event = payload.get("hook_event_name", "SessionStart")

    sys.path.insert(0, str(SKILL))
    try:
        import fingerprint as fpmod  # noqa
    except Exception:
        return 0
    fp = fpmod.load(_find_fingerprint())

    gaps = fpmod.gaps(fp)
    parts = []
    if (fp.get("palette") or {}).get("accent_hex"):
        parts.append(f"accent {fp['palette']['accent_hex']}")
    if (fp.get("fonts") or {}).get("body"):
        parts.append(f"font {fp['fonts']['body']}")
    if (fp.get("voice") or {}).get("spec"):
        parts.append("voice set")
    summary = ("anti-ai-tell active style fingerprint: "
               + (", ".join(parts) if parts else "seed")
               + (f". Unset slots ({len(gaps)}): ask the user when a design task needs them."
                  if gaps else "."))

    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": event,
        "additionalContext": summary,
    }}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
