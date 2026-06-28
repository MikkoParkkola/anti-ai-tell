---
description: Lint a file or directory for visual + prose AI-tells (Tier-1 mechanical pass).
---

Run the anti-ai-tell linters on `$ARGUMENTS` (a file or directory; default: the
current directory's changed files).

1. For prose (`.md`, `.txt`): `python3 ${CLAUDE_PLUGIN_ROOT}/skills/anti-ai-tell/lint.py <file> --prose`
2. For code/markup (`.css`, `.tsx`, `.svg`, `.docx`, ...): `python3 ${CLAUDE_PLUGIN_ROOT}/skills/anti-ai-tell/visual_lint.py <file_or_dir>`
3. If a `fingerprint.json` exists, pass `--fingerprint fingerprint.json` so the
   user's chosen accent/font is not flagged.

Report the findings grouped by severity (Hard-tell / Strong-flag / Density-watch),
then remind: a clean lint is the floor, not the ceiling — do the Tier-2 hand-pass
(hierarchy, point of view, a rough edge) the linter can't see.
