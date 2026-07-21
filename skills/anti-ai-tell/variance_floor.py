#!/usr/bin/env python3
"""variance-floor — population-level AI-sameness detector (INV-4).

The discovery: AI-tell is a *variance deficit*, and reliable detection only exists
at the population level (per-sample detection is capped by the Sadasivan bound,
arXiv 2303.11156, and falsely flags humans). So this tool scores a SET and NEVER
judges a single artifact. It cannot tell you "this file is AI"; it can tell you
"this batch occupies suspiciously little of the space a varied human cohort would."

Mechanic: each artifact -> bag-of-token-bigrams vector (stdlib, no embeddings dep)
-> mean pairwise cosine distance = the diversity score. Low diversity = variance
collapse = the population tell. Relative by design: compare to a reference batch or
report the raw score with that caveat. Refuses when n < MIN_N.

Known limitation (2026-07-21): this tool measures SOURCE-CODE sameness (token
bigrams), not rendered-output sameness. It also cannot distinguish "AI-sameness"
from a disciplined, intentional design system -- low variance describes both.
Treat a low score as "investigate," never as a standalone verdict; corroborate
with the Tier-2 human judgment pass before concluding genericness. Note too that
this repo's own prescribed fix for genericness -- a consistently-applied style
fingerprint -- will itself produce low population variance across a body of work
that uses it correctly; a low score is not automatically a defect (see the
project issue tracker for the open design question this raises). A
rendered-output mode (screenshot -> embeddings -> cosine distance) is a tracked,
separate, opt-in extra -- see the project issue tracker -- because it measures a
different thing (what a viewer sees) and carries a real dependency cost the
default linter should not pay.

Usage:
    python3 variance_floor.py FILE_OR_DIR [--reference DIR] [--json] [--min-n 5]
Exit code: 0 always for a valid batch (this is a measurement, never a gate/verdict).
           2 if the batch is too small to score (refusal).
"""
from __future__ import annotations

import json
import math
import re
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

MIN_N = 5
_TOK = re.compile(r"[a-z0-9]+")


def _vec(text: str) -> Counter:
    toks = _TOK.findall(text.lower())
    return Counter(zip(toks, toks[1:])) or Counter([("", "")])  # bigrams; guard empty


def _cos(a: Counter, b: Counter) -> float:
    common = set(a) & set(b)
    dot = sum(a[k] * b[k] for k in common)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0


def diversity(texts: list[str]) -> float:
    """Mean pairwise cosine DISTANCE (1 - similarity). Higher = more varied."""
    vecs = [_vec(t) for t in texts]
    dists = [1.0 - _cos(a, b) for a, b in combinations(vecs, 2)]
    return sum(dists) / len(dists) if dists else 0.0


def _load_batch(target: Path) -> list[tuple[str, str]]:
    if target.is_dir():
        files = [f for f in sorted(target.rglob("*")) if f.is_file() and f.suffix in
                 (".txt", ".md", ".css", ".tsx", ".html", ".json")]
        return [(f.name, f.read_text(encoding="utf-8", errors="replace")) for f in files]
    # a single file: each non-empty line / paragraph is an artifact
    blocks = re.split(r"\n\s*\n", target.read_text(encoding="utf-8", errors="replace"))
    return [(f"block{i}", b) for i, b in enumerate(blocks) if b.strip()]


def score_batch(target: Path, reference: Path | None, min_n: int) -> dict:
    items = _load_batch(target)
    n = len(items)
    if n < min_n:
        return {"ok": False, "reason": f"batch too small (n={n} < {min_n}); "
                "population detection needs a set, by design — single artifacts are "
                "undetectable (Sadasivan). No verdict.", "n": n}
    texts = [t for _, t in items]
    div = diversity(texts)
    out = {
        "ok": True, "n": n, "diversity": round(div, 4),
        # NOTE: deliberately NO per-item field. This tool never labels an artifact.
        "interpretation": "higher diversity = more varied = less mode-collapsed",
    }
    if reference is not None:
        ref_items = _load_batch(reference)
        if len(ref_items) >= min_n:
            ref_div = diversity([t for _, t in ref_items])
            out["reference_diversity"] = round(ref_div, 4)
            out["relative"] = round(div / ref_div, 3) if ref_div else None
            out["flag"] = bool(ref_div and div < 0.6 * ref_div)
            out["verdict"] = (
                "VARIANCE COLLAPSE: this batch is markedly less varied than the "
                "reference cohort — a population-level AI-sameness signal."
                if out["flag"] else
                "within the variance range of the reference cohort."
            )
    else:
        out["note"] = ("no --reference given; diversity is relative by nature. "
                       "Compare to a comparable human cohort or the author's own past batch.")
    return out


def main(argv: list[str]) -> int:
    as_json = "--json" in argv
    min_n = MIN_N
    if "--min-n" in argv:
        i = argv.index("--min-n"); min_n = int(argv[i + 1]); argv = argv[:i] + argv[i + 2:]
    reference = None
    if "--reference" in argv:
        i = argv.index("--reference"); reference = Path(argv[i + 1]); argv = argv[:i] + argv[i + 2:]
    files = [a for a in argv if not a.startswith("--")]
    if not files:
        print(__doc__); return 0

    res = score_batch(Path(files[0]), reference, min_n)
    if as_json:
        print(json.dumps(res, indent=1))
        return 0 if res["ok"] else 2
    if not res["ok"]:
        print(f"REFUSED: {res['reason']}")
        return 2
    print(f"batch n={res['n']}  diversity={res['diversity']}  ({res['interpretation']})")
    if "verdict" in res:
        print(f"vs reference {res['reference_diversity']} (x{res['relative']}): {res['verdict']}")
    else:
        print(res["note"])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
