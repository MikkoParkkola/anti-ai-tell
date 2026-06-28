#!/usr/bin/env python3
"""Self-checks for the cross-media extension. Stdlib assert-based, no framework.

    python3 tests/test_extension.py   # exit 0 = all pass

Covers: fingerprint (derive/gaps/validate/seed), visual_lint (flag/allow/use-mention),
variance_floor (collapse/refuse/no-per-item), lint upgrades (concreteness/score/voice),
and the phase0 scorer math.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "anti-ai-tell"
EXP = ROOT / "experiments"
sys.path.insert(0, str(SKILL))
sys.path.insert(0, str(EXP))

import fingerprint as fp  # noqa: E402
import visual_lint as vl  # noqa: E402
import variance_floor as vf  # noqa: E402

PASS = 0


def ok(cond, label):
    global PASS
    assert cond, f"FAIL: {label}"
    PASS += 1
    print(f"  ok: {label}")


def _tmp(content: str, suffix: str) -> Path:
    f = tempfile.NamedTemporaryFile("w", suffix=suffix, delete=False, encoding="utf-8")
    f.write(content)
    f.close()
    return Path(f.name)


# ── fingerprint ───────────────────────────────────────────────────────────────
print("fingerprint:")
seed = fp.seed()
ok(fp.validate(seed) == [], "seed validates clean")
ok(fp.gaps(seed) == [], "seed has no gaps")
css = _tmp(":root{--font-body:'Fraunces';--accent:#B5472A;}\n.x{border-radius:4px}", ".css")
d = fp.derive(css)
ok(fp._get(d, "fonts.body") == "Fraunces", "derive reads non-default font")
ok(fp._get(d, "palette.accent_hex") == "#B5472A", "derive reads accent hex")
ok(len(fp.gaps(d)) > 0, "partial derive leaves gaps to ask")
ok(fp.validate({"distinctiveness_dial": "nonsense"}), "invalid dial rejected")

# ── visual_lint ─────────────────────────────────────────────────────────────
print("visual_lint:")
slop = _tmp(".b{background:indigo-500;color:#6366f1;font-family:'Inter'}"
            "\n.h{background-clip:text}", ".css")
found = vl.lint_file(slop, fp.seed())
ids = {x["id"] for x in found}
ok("V-CSS-1" in ids and "V-CSS-2" in ids, "indigo flagged even with non-indigo fingerprint")
ok("V-CSS-4" in ids, "Inter flagged")
found_allow = vl.lint_file(slop, {"lint_allow": ["V-CSS-4"]})
ok("V-CSS-4" not in {x["id"] for x in found_allow}, "lint_allow opts out of Inter")
ok("V-CSS-1" in {x["id"] for x in found_allow}, "indigo still flags despite allow-list")
about = _tmp("Avoid the `indigo-500` default and `Inter`.", ".md")
ok(vl.lint_file(about, fp.seed()) == [], "use-mention: doc about tells passes")

# ── variance_floor ─────────────────────────────────────────────────────────
print("variance_floor:")
collapsed = ["Unlock seamless AI productivity now."] * 6
varied = ["The harbor froze in 1987.", "Compile times hit 4 seconds.",
          "She moved to Lisbon.", "Churn rose two points.",
          "Burnt sienna, sharp corners.", "Three servers, zero pages."]
ok(vf.diversity(collapsed) < vf.diversity(varied), "collapsed batch scores lower diversity")
with tempfile.TemporaryDirectory() as td:
    p = Path(td)
    (p / "a.txt").write_text("only one")
    res = vf.score_batch(p, None, 5)
    ok(res["ok"] is False, "batch below min_n is refused")
    for i in range(6):
        (p / f"b{i}.txt").write_text(f"distinct sentence number {i} about {i*7} things")
    res2 = vf.score_batch(p, None, 5)
    ok("verdict" not in res2 or "items" not in res2, "no per-item verdict emitted")
    ok(all(k not in res2 for k in ("items", "per_item", "verdicts")), "never labels an artifact")

# ── lint.py upgrades (via subprocess to exercise the real CLI) ───────────────
print("lint upgrades:")
abstract = ("We believe synergy enables transformation across the organization and "
            "our vision empowers stakeholders to realize potential through alignment "
            "collaboration and a shared sense of purpose driving meaningful outcomes "
            "for everyone involved in this journey forward together as one team always.")
r = subprocess.run([sys.executable, str(SKILL / "lint.py"), "-", "--json"],
                   input=abstract, capture_output=True, text=True)
data = json.loads(r.stdout)
ok(any("S14" in f for f in data["findings"]), "S14 flags a no-concrete-anchor paragraph")
ok("machine_likeness" in data and isinstance(data["machine_likeness"], int),
   "machine_likeness score emitted in --json")
fpf = _tmp(json.dumps(fp.seed()), ".json")
r2 = subprocess.run([sys.executable, str(SKILL / "lint.py"), "-", "--fingerprint", str(fpf)],
                    input="This is librarian mode hedge-stacking.", capture_output=True, text=True)
ok("S15" in r2.stdout, "S15 flags fingerprint voice.avoid terms")

# ── phase0 scorer math ──────────────────────────────────────────────────────
print("phase0 scorer:")
import phase0_anchor_distance as p0  # noqa: E402
sc = p0.score(["same centroid text"] * 5,
              ["wildly different one 4", "another distinct two 9", "third unlike three 1",
               "fourth apart four 7", "fifth away five 2"])
ok(sc["mean_dist_to_centroid_B_anchored"] > sc["mean_dist_to_centroid_A_unanchored"],
   "anchored set measured farther from unanchored centroid")
ok(sc["verdict"] in ("GO", "KILL/PIVOT"), "verdict emitted")

print(f"\nALL {PASS} CHECKS PASSED")
