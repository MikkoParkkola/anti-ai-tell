#!/usr/bin/env python3
"""Phase 0 — does a style anchor move output OFF the AI centroid? (MIK-6618)

The gate for the whole epic. The (c) novelty claim is: one persistent style anchor
measurably de-genericizes output. We test the clean version of that: anchored
outputs sit FARTHER from the unanchored centroid than unanchored outputs do.

Method:
  A = N generations from a bare prompt (these collapse toward the centroid).
  B = N generations from prompt + a one-line style anchor.
  centroid = mean bag-of-bigrams vector of A (A's own centre).
  Compare {dist(a_i, centroid)} vs {dist(b_i, centroid)} with Cohen's d.
  GO if mean(B-dist) > mean(A-dist) at d >= 0.5.

Generation shells out to `claude -p` (sanctioned auth path; no REST keys). Use
--files A_dir B_dir to score pre-generated text instead (one artifact per file),
so the experiment is reproducible without spending tokens.

Usage:
    python3 phase0_anchor_distance.py --run --n 10 [--model haiku]
    python3 phase0_anchor_distance.py --files A_dir B_dir
"""
from __future__ import annotations

import json
import math
import statistics
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent / "skills" / "anti-ai-tell"
sys.path.insert(0, str(SKILL))
from variance_floor import _vec, _cos  # noqa: E402  (reuse the stdlib vectorizer)

BASE = "Write a single-sentence hero tagline for a SaaS startup. Output only the tagline."
ANCHOR = (" Style anchor: blunt and concrete, cite one real number, zero buzzwords, "
          "name a specific person or place. No 'seamless', 'empower', 'unlock', 'elevate'.")


def _centroid(vecs: list) -> dict:
    c: dict = {}
    for v in vecs:
        for k, n in v.items():
            c[k] = c.get(k, 0) + n
    return c


def _dist_to(vec, centroid) -> float:
    return 1.0 - _cos(vec, centroid)


def cohens_d(x: list[float], y: list[float]) -> float:
    nx, ny = len(x), len(y)
    if nx < 2 or ny < 2:
        return 0.0
    vx, vy = statistics.pvariance(x), statistics.pvariance(y)
    pooled = math.sqrt(((nx * vx) + (ny * vy)) / (nx + ny)) or 1e-9
    return (statistics.mean(y) - statistics.mean(x)) / pooled


def gen(prompt: str, model: str, i: int) -> str | None:
    """Generate one sample. Returns None on ANY failure (nonzero exit, empty
    output, exception) so a broken generation is NEVER scored as a real sample —
    otherwise a quota/auth/CLI failure silently corrupts the GO/KILL verdict."""
    p = f"{prompt} (variant {i}, be original)"
    try:
        out = subprocess.run(["claude", "-p", p, "--model", model],
                             capture_output=True, text=True, timeout=90)
    except Exception:
        return None
    if out.returncode != 0:
        return None
    return out.stdout.strip() or None


def score(a_texts: list[str], b_texts: list[str]) -> dict:
    a_texts = [t for t in a_texts if t and t.strip()]
    b_texts = [t for t in b_texts if t and t.strip()]
    if len(a_texts) < 2 or len(b_texts) < 2:
        return {"ok": False,
                "error": f"need >=2 non-empty samples per arm; got A={len(a_texts)} B={len(b_texts)}"}
    a_vecs = [_vec(t) for t in a_texts]
    b_vecs = [_vec(t) for t in b_texts]
    centroid = _centroid(a_vecs)  # the unanchored centre
    a_d = [_dist_to(v, centroid) for v in a_vecs]
    b_d = [_dist_to(v, centroid) for v in b_vecs]
    d = cohens_d(a_d, b_d)
    go = statistics.mean(b_d) > statistics.mean(a_d) and d >= 0.5
    return {
        "ok": True,
        "n_a": len(a_texts), "n_b": len(b_texts),
        "mean_dist_to_centroid_A_unanchored": round(statistics.mean(a_d), 4),
        "mean_dist_to_centroid_B_anchored": round(statistics.mean(b_d), 4),
        "cohens_d": round(d, 3),
        "verdict": "GO" if go else "KILL/PIVOT",
        "claim": "anchor moves output OFF the unanchored centroid (de-generic)",
    }


def main(argv: list[str]) -> int:
    if "--files" in argv:
        i = argv.index("--files")
        adir, bdir = Path(argv[i + 1]), Path(argv[i + 2])
        a = [f.read_text(encoding="utf-8", errors="replace") for f in sorted(adir.glob("*")) if f.is_file()]
        b = [f.read_text(encoding="utf-8", errors="replace") for f in sorted(bdir.glob("*")) if f.is_file()]
        print(json.dumps(score(a, b), indent=1))
        return 0
    if "--run" in argv:
        n = int(argv[argv.index("--n") + 1]) if "--n" in argv else 10
        model = argv[argv.index("--model") + 1] if "--model" in argv else "haiku"
        a = [t for t in (gen(BASE, model, i) for i in range(n)) if t]
        b = [t for t in (gen(BASE + ANCHOR, model, i) for i in range(n)) if t]
        if len(a) < 2 or len(b) < 2:
            print(json.dumps({"ok": False,
                              "error": f"generation failed (quota/auth/CLI?): "
                                       f"A={len(a)}/{n} B={len(b)}/{n} valid samples"}, indent=1))
            return 1
        res = score(a, b)
        res["samples"] = {"A0": a[0][:80], "B0": b[0][:80], "n_valid": [len(a), len(b)]}
        print(json.dumps(res, indent=1))
        return 0 if res.get("ok") else 1
    print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
