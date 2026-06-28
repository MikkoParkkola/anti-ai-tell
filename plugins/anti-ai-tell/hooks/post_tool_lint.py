#!/usr/bin/env python3
"""PostToolUse hook: lint files the agent just wrote for visual + prose AI-tells.

Wires into Write|Edit. Non-blocking by design (like doom-loop-detect): it WARNS,
never blocks — a guard rail, not a gate. Reads the touched file path from the hook
payload, runs the matching linter, and surfaces any tells as a system message so
the agent self-corrects on the next turn.

Install via the plugin's hooks config (PostToolUse, matcher: Write|Edit).
Zero deps; resolves the linters relative to the plugin so it runs anywhere.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent / "skills" / "anti-ai-tell"
VISUAL = {".css", ".scss", ".tsx", ".jsx", ".vue", ".svelte", ".html", ".svg", ".docx", ".mdx"}
PROSE = {".md", ".txt"}


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    ti = payload.get("tool_input") or {}
    fpath = ti.get("file_path") or ti.get("path")
    if not fpath:
        return 0
    p = Path(fpath)
    ext = p.suffix.lower()
    if ext not in VISUAL and ext not in PROSE:
        return 0
    if not p.exists():
        return 0

    linter = "visual_lint.py" if ext in VISUAL else "lint.py"
    args = [sys.executable, str(SKILL / linter), str(p), "--json"]
    if linter == "lint.py":
        args.append("--prose")
    # Honor the repo's fingerprint.json opt-outs (accent/font allow-list,
    # voice.avoid). Without this the hook lints against the seed and the
    # "opt in via fingerprint.json" advice it prints would be a lie.
    fp_json = Path.cwd() / "fingerprint.json"
    if fp_json.exists():
        args += ["--fingerprint", str(fp_json)]
    try:
        out = subprocess.run(args, capture_output=True, text=True, timeout=20)
        data = json.loads(out.stdout or "{}")
    except Exception:
        return 0

    if data.get("clean", True):
        return 0
    # Build a terse warning.
    if linter == "visual_lint.py":
        tells = [f"{x['id']} {x['msg']}" for v in data.get("files", {}).values() for x in v][:5]
    else:
        tells = data.get("findings", [])[:5]
    if not tells:
        return 0
    msg = (f"anti-ai-tell: {p.name} carries AI-design tells -> "
           + " | ".join(tells)
           + ". Fix, or opt in via fingerprint.json if deliberate.")
    print(json.dumps({"systemMessage": msg}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
