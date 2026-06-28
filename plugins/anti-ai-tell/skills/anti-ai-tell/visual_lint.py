#!/usr/bin/env python3
"""anti-ai-tell visual linter — Tier-1 mechanical tells in code/markup/docs.

Sibling of lint.py (prose). Scans the *lintable subset* of the visual catalog
(research/visual-ai-tells.md): CSS/Tailwind, markdown, .docx, and SVG. It cannot
see the Tier-2 gestalt (hierarchy, the AI sheen, logo concept) — that needs eyes
or a vision model. Clean lint != good design.

Reads fingerprint.json as an allow-list: a user-CHOSEN accent/font is not a tell;
the centroid default still is. Zero dependencies (stdlib only) so the plugin hooks
run anywhere.

Usage:
    python3 visual_lint.py FILE [FILE...] [--json] [--fingerprint path]
    python3 visual_lint.py DIR --json
Exit code: 0 = clean, 1 = tells found (CI-gateable).
"""
from __future__ import annotations

import json
import re
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
VOCAB = json.loads((HERE / "visual-vocabulary.json").read_text(encoding="utf-8"))

EXT_KIND = {
    ".css": "css", ".scss": "css", ".sass": "css", ".less": "css",
    ".tsx": "css", ".jsx": "css", ".vue": "css", ".svelte": "css", ".html": "css",
    ".md": "markdown", ".mdx": "markdown",
    ".docx": "docx",
    ".svg": "svg",
}

# Use-mention masking: a doc ABOUT the tells (code spans / fenced blocks) must pass.
_FENCED = re.compile(r"^```.*?^```", re.M | re.S)
_INLINE = re.compile(r"`[^`\n]+`")


def _mask(text: str) -> str:
    text = _FENCED.sub(lambda m: "\n".join(" " * len(l) for l in m.group(0).splitlines()), text)
    return _INLINE.sub(lambda m: " " * len(m.group(0)), text)


def _read_docx(path: Path) -> str:
    """Pull visible text from word/document.xml — that's where bleed would render."""
    try:
        with zipfile.ZipFile(path) as z:
            xml = z.read("word/document.xml").decode("utf-8", "replace")
    except Exception:
        return ""
    return re.sub(r"<[^>]+>", " ", xml)  # strip tags, keep text runs


def _allowed(fp: dict) -> set[str]:
    """Pattern IDs the user explicitly opts into.

    The deny-list is the floor: indigo/Inter ALWAYS flag (they are the centroid
    defaults). A chosen accent like #B5472A is never in the deny-list, so it is
    never flagged — no special-casing needed. The only way to silence a default
    tell is a deliberate `lint_allow` entry in the fingerprint (a brand that
    genuinely uses Inter writes lint_allow: ["V-CSS-4"]).
    """
    return set(fp.get("lint_allow", []))


def _scan(text: str, kind: str, allowed: set[str]) -> list[dict]:
    masked = _mask(text)
    lines = masked.splitlines()
    findings: list[dict] = []
    groups = VOCAB.get(kind, {})
    for sev, group in groups.items():
        if sev.startswith("_"):
            continue
        for pat in group.get("patterns", []):
            if pat["id"] in allowed:
                continue
            rx = re.compile(pat["rx"], re.M)
            hits = 0
            first_line = None
            for i, ln in enumerate(lines, 1):
                if rx.search(ln):
                    hits += 1
                    if first_line is None:
                        first_line = i
            if hits:
                findings.append({
                    "id": pat["id"], "severity": sev, "count": hits,
                    "line": first_line, "msg": pat["msg"],
                })
    return findings


def lint_file(path: Path, fp: dict) -> list[dict]:
    kind = EXT_KIND.get(path.suffix.lower())
    if not kind:
        return []
    text = _read_docx(path) if kind == "docx" else path.read_text(encoding="utf-8", errors="replace")
    return _scan(text, kind, _allowed(fp))


def _iter_targets(args: list[str]):
    for a in args:
        p = Path(a)
        if p.is_dir():
            for f in p.rglob("*"):
                if f.is_file() and f.suffix.lower() in EXT_KIND:
                    yield f
        elif p.is_file():
            yield p


def main(argv: list[str]) -> int:
    as_json = "--json" in argv
    fp_path = None
    if "--fingerprint" in argv:
        i = argv.index("--fingerprint")
        fp_path = Path(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    files = [a for a in argv if not a.startswith("--")]
    if not files:
        print(__doc__)
        return 0

    import importlib.util
    spec = importlib.util.spec_from_file_location("fingerprint", HERE / "fingerprint.py")
    fpmod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fpmod)
    fp = fpmod.load(fp_path)

    report = {}
    total = 0
    for f in _iter_targets(files):
        found = lint_file(f, fp)
        if found:
            report[str(f)] = found
            total += len(found)

    if as_json:
        print(json.dumps({"clean": total == 0, "files": report}, indent=1))
        return 0 if total == 0 else 1

    if total == 0:
        print("OK: visual Tier-1 clean. Tier-2 (hierarchy, intent, the gestalt) still needs eyes.")
        return 0
    print(f"FAIL: {total} visual tell(s) across {len(report)} file(s):")
    for f, found in report.items():
        print(f"  {f}")
        for x in found:
            loc = f"L{x['line']}" if x["line"] else "-"
            print(f"    - [{x['severity']}] {x['id']} {loc} x{x['count']}: {x['msg']}")
    print("\nFix these, or opt in via fingerprint.json if the choice was deliberate.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
