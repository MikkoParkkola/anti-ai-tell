# anti-ai-tell

This plugin keeps prose and interface work from collapsing into one machine voice. It lints the draft you point at, stores a style fingerprint you choose, and runs that lint again when Claude writes a file.

Use it on investor notes, public READMEs, customer email, and UI code. A clean report means the cheap tells are gone. You still read the draft.

### Example: Lint prose

Name a file and the prose linter reports measured tells: banned vocabulary, flat sentence rhythm, em dashes, and vague attribution. The run exits nonzero when the draft fails. Add `--json` when a script needs the same findings as data.

```sh
python3 "${CLAUDE_PLUGIN_ROOT}/skills/anti-ai-tell/lint.py" draft.md --prose
```

In Claude, `/aat-lint draft.md` runs that pass and groups the hits by severity. Fix the lines it names, then run it again.

### Example: Style fingerprint

Derive a fingerprint from a site, stylesheet, or writing sample you already like. The derive step fills the slots it can read, such as font, accent, and radius. You answer only the gaps. The result is a local `fingerprint.json` in the project. Later lint runs allow that accent and font instead of calling them defaults.

```sh
python3 "${CLAUDE_PLUGIN_ROOT}/skills/anti-ai-tell/fingerprint.py" derive site.css
python3 "${CLAUDE_PLUGIN_ROOT}/skills/anti-ai-tell/fingerprint.py" gaps
```

`/aat-fingerprint` asks those gap questions and writes the file. Nothing in that file is uploaded.

### Example: Lint on write

After you install the plugin, the PostToolUse hook listens for Write and Edit. It reads the file just saved, picks the prose linter or the visual linter from the suffix, and prints a warning when it finds tells. The write still succeeds. If `fingerprint.json` is in the working directory, the hook passes it through, so a font you chose is not flagged.

No extra command is required for that pass. `/aat-lint` remains the way to scan a path on demand. Session start also reads the same local fingerprint and tells the agent which accent, font, and voice are set.
