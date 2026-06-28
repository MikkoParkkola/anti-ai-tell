#!/usr/bin/env python3
"""Style fingerprint: load, derive-then-confirm, and the seed.

The fingerprint is the cure for genericness (the (c) mechanism): one persistent
off-mode anchor that injects positive constraints into generation AND configures
the linters' allow-list. Seeded DERIVE-THEN-CONFIRM (operator decision 2026-06-28):
extract from the user's existing artifacts, then ask only about the gaps.

Zero dependencies (stdlib only) so the plugin hooks run anywhere. Validation is a
small hand-rolled check, not jsonschema — ponytail: a few lines beat a dependency.

CLI:
    python3 fingerprint.py derive <file.css|file.md|sample.txt>   # extract slots
    python3 fingerprint.py gaps  [fingerprint.json]               # list null slots to ask
    python3 fingerprint.py validate <fingerprint.json>
    python3 fingerprint.py seed                                   # print the ELITE seed
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCHEMA = HERE / "fingerprint.schema.json"

# Slots we elicit. Dotted path -> human question for the gap-quiz (active-ask).
SLOTS = {
    "fonts.body": "Body typeface? (anything but Inter/Roboto is already a win)",
    "palette.accent_hex": "Brand accent color? Pick a lane: warm / cool / mono / bold",
    "palette.mode": "Default mode: light, dark, or either?",
    "shape.radius": "Corner personality: sharp, soft (~4px), or round?",
    "imagery.type": "Imagery: photography, illustration, abstract, or none?",
    "voice.spec": "Prose voice in one line?",
    "distinctiveness_dial": "Should this blend-in, be balanced, or stand-out?",
}

# Tailwind/AI defaults we treat as "unset" even when present — the centroid.
_DEFAULT_FONTS = {"inter", "roboto", "arial", "system-ui", "-apple-system"}
_DEFAULT_ACCENTS = {"#6366f1", "#6366ff", "indigo", "#4f46e5"}  # indigo-500/600-ish


def _get(d: dict, dotted: str):
    cur = d
    for k in dotted.split("."):
        if not isinstance(cur, dict) or k not in cur:
            return None
        cur = cur[k]
    return cur if cur not in ("", None) else None


def _set(d: dict, dotted: str, val) -> None:
    keys = dotted.split(".")
    cur = d
    for k in keys[:-1]:
        cur = cur.setdefault(k, {})
    cur[keys[-1]] = val


def derive(path: Path) -> dict:
    """Extract whatever slots we can read from an existing artifact.

    CSS/SCSS/TSX: font-family + hex/named accents + border-radius.
    Markdown/text: leaves visual slots empty (voice could be inferred but we ask).
    """
    text = path.read_text(encoding="utf-8", errors="replace")
    fp: dict = {}

    fonts = re.findall(r"font-family\s*:\s*([^;}\n]+)", text, re.I)
    fonts += re.findall(r"--font[\w-]*\s*:\s*([^;}\n]+)", text, re.I)
    for decl in fonts:
        first = decl.split(",")[0].strip().strip("'\"")
        if first and first.lower() not in _DEFAULT_FONTS:
            _set(fp, "fonts.body", first)
            break

    # Accent: first hex that isn't an indigo default, else a named non-default.
    for hexc in re.findall(r"#[0-9a-fA-F]{3,8}\b", text):
        if hexc.lower() not in _DEFAULT_ACCENTS:
            _set(fp, "palette.accent_hex", hexc)
            break

    radii = re.findall(r"border-radius\s*:\s*([^;}\n]+)", text, re.I)
    if radii:
        _set(fp, "shape.radius", radii[0].strip())

    if re.search(r"prefers-color-scheme\s*:\s*dark|\bdark:bg-|\.dark\b", text):
        _set(fp, "palette.mode", "dark")

    return fp


def gaps(fp: dict) -> list[tuple[str, str]]:
    """Slots still unset -> the questions the active-ask quiz should pose."""
    return [(slot, q) for slot, q in SLOTS.items() if _get(fp, slot) is None]


def validate(fp: dict) -> list[str]:
    """Minimal structural validation against the schema's shape. Returns errors."""
    errs: list[str] = []
    schema = json.loads(SCHEMA.read_text())
    props = schema["properties"]
    for key, val in fp.items():
        if key in props and props[key].get("type") == "object" and not isinstance(val, dict):
            errs.append(f"{key}: expected object, got {type(val).__name__}")
    acc = _get(fp, "palette.accent_hex")
    if acc is not None and not re.match(r"^#?[0-9a-fA-F]{3,8}$", str(acc)):
        errs.append(f"palette.accent_hex: '{acc}' is not a hex color")
    dial = fp.get("distinctiveness_dial")
    if dial is not None and dial not in ("blend-in", "balanced", "stand-out"):
        errs.append(f"distinctiveness_dial: '{dial}' not in blend-in|balanced|stand-out")
    mode = _get(fp, "palette.mode")
    if mode is not None and mode not in ("light", "dark", "either"):
        errs.append(f"palette.mode: '{mode}' not in light|dark|either")
    return errs


def seed() -> dict:
    """The first working fingerprint: Mikko's ELITE voice + a non-default visual stance.

    Proves the loop end-to-end and gives the text skill a positive voice constraint
    on day one (AAT.FP.4 / AAT.TXT.4).
    """
    return {
        "name": "mikko-elite",
        "fonts": {"body": "Fraunces", "heading": "Fraunces", "mono": "Berkeley Mono"},
        "palette": {"accent_hex": "#B5472A", "neutral_ramp": "warm-stone", "mode": "either"},
        "shape": {"radius": "4px", "shadow": "hard"},
        "imagery": {"type": "photography", "grade": "muted-warm (not orange-teal)"},
        "voice": {
            "spec": "James Bond x Silicon Valley x von Neumann. Surgical honesty, "
            "committed verdicts, tables with teeth. Sharp but never cryptic.",
            "avoid": ["hedge-stacking", "librarian mode", "em-dash overuse"],
        },
        "distinctiveness_dial": "stand-out",
    }


def load(path: Path | None = None) -> dict:
    """Load a fingerprint.json; fall back to the seed if none exists."""
    if path and path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return seed()


def _main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 0
    cmd = argv[0]
    if cmd == "seed":
        print(json.dumps(seed(), indent=2))
        return 0
    if cmd == "derive":
        fp = derive(Path(argv[1]))
        g = gaps(fp)
        print(json.dumps({"derived": fp, "gaps": [s for s, _ in g]}, indent=2))
        return 0
    if cmd == "gaps":
        fp = load(Path(argv[1]) if len(argv) > 1 else None)
        for slot, q in gaps(fp):
            print(f"{slot}\t{q}")
        return 0
    if cmd == "validate":
        errs = validate(json.loads(Path(argv[1]).read_text()))
        if errs:
            print("INVALID:\n  - " + "\n  - ".join(errs))
            return 1
        print("OK: fingerprint valid")
        return 0
    print(f"unknown command: {cmd}")
    return 2


if __name__ == "__main__":
    sys.exit(_main(sys.argv[1:]))
