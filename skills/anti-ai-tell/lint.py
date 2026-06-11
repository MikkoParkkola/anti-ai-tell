#!/usr/bin/env python3
"""anti-ai-tell linter — flags mechanical tells that text was written by AI.

Tier-1 ONLY. A clean run means the cheap, machine-detectable tells are gone.
It cannot judge reasoning, sycophancy, or concreteness; that is the Tier-2
hand-pass in SKILL.md. Clean lint != reads human.

Checks (IDs referenced by SKILL.md):
  S1  em-dash overuse                 S8  banned vocabulary (era-aware)
  S2  negative parallelism            S9  copulative avoidance (serves as...)
  S3  uniform sentence rhythm         S10 rule-of-three runs
  S4  uniform paragraph length        S11 vague attribution
  S5  throat-clearing openers         S12 markdown in prose
  S6  connective filler               S13 density-watch vocabulary clusters
  S7  closing-bow wrap-ups

Usage:
    python3 lint.py FILE [--json] [--prose]
    cat FILE | python3 lint.py
    --prose: enable S12 (markdown flagging) for plain-prose targets
             (emails, posts); leave off for READMEs/docs where markdown
             is the medium.

Exit code: 0 = clean, 1 = tells found (CI-gateable).

Vocabulary lives in data/vocabulary.json next to this repo's root; the linter
finds it relative to its own location so the skill works installed anywhere.
"""
from __future__ import annotations

import json
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

# ── vocabulary loading ───────────────────────────────────────────────────────


def load_vocab() -> dict:
    here = Path(__file__).resolve().parent
    for candidate in (
        here / "vocabulary.json",
        here / "data" / "vocabulary.json",
        here.parent / "data" / "vocabulary.json",
        here.parent.parent / "data" / "vocabulary.json",
    ):
        if candidate.exists():
            return json.loads(candidate.read_text(encoding="utf-8"))
    return {}


VOCAB = load_vocab()


def word_pattern(words: list[str]) -> re.Pattern | None:
    if not words:
        return None
    alts = "|".join(re.escape(w) for w in sorted(words, key=len, reverse=True))
    return re.compile(rf"\b({alts})\b", re.I)


HARD_BAN = word_pattern(VOCAB.get("hard_ban", {}).get("words", []))
STRONG_FLAG = word_pattern(VOCAB.get("strong_flag", {}).get("words", []))
DENSITY_WATCH = word_pattern(VOCAB.get("density_watch", {}).get("words", []))
COPULATIVE = word_pattern(VOCAB.get("copulative_avoidance", {}).get("phrases", []))

# ── structural patterns ──────────────────────────────────────────────────────

ANTITHESIS = [
    re.compile(r"\bit'?s not (just )?\w[\w\s]{0,40}?[;,]?\s+it'?s\b", re.I),
    re.compile(r"\bnot just \w[\w\s]{0,40}?,?\s+but\b", re.I),
    re.compile(r"\bnot only \w[\w\s]{0,40}?,?\s+but(\s+also)?\b", re.I),
    re.compile(r"\bisn'?t (about|just) \w[\w\s]{0,40}?,?\s+(it'?s|but)\b", re.I),
    re.compile(r"\bnot (merely|simply) \w[\w\s]{0,40}?,?\s+but\b", re.I),
]
OPENERS = re.compile(
    r"^\s*(in today'?s [\w\s-]*world|it'?s worth noting|at its core|in the (ever-)?evolving|"
    r"in the realm of|when it comes to|in an era|needless to say|first and foremost|"
    r"it is important to (note|remember|understand)|in the world of|have you ever wondered)",
    re.I,
)
FILLER = re.compile(
    r"\b(moreover|furthermore|additionally|ultimately|that said|in essence|"
    r"it'?s important to note|notably|crucially)\b",
    re.I,
)
CLOSERS = re.compile(
    r"^\s*(in conclusion|overall|in summary|to sum up|all in all|at the end of the day|"
    r"in closing|wrapping up|to conclude)\b",
    re.I,
)
VAGUE_ATTRIBUTION = re.compile(
    r"\b(studies (show|suggest|indicate)|experts (say|agree|believe)|"
    r"research (shows|suggests|indicates)|many (critics|observers|analysts) (argue|believe|note)|"
    r"industry reports suggest|it is widely (believed|acknowledged|recognized))\b",
    re.I,
)
EMDASH = re.compile(r"—|\s--\s")
SENT_SPLIT = re.compile(r"[.!?]+(?:\s+|$)")
TRIAD = re.compile(r"\b\w+(?:\s\w+){0,2},\s+\w+(?:\s\w+){0,2},\s+and\s+\w+")
MARKDOWN = re.compile(r"(\*\*[^*]+\*\*|^#{1,6}\s|^\s*[-*]\s|^\s*\d+\.\s)", re.M)


def paragraphs(text: str) -> list[str]:
    return [p for p in re.split(r"\n\s*\n", text) if p.strip()]


# Use-mention distinction: words inside fenced code blocks, code spans,
# italics, or double quotes are MENTIONED (discussed), not USED. Mask them
# before vocabulary/parallelism scans so a document ABOUT AI tells can pass
# its own lint.
FENCED_BLOCK = re.compile(r"^```.*?^```", re.M | re.S)
MENTION_SPANS = [
    re.compile(r"`[^`\n]+`"),
    re.compile(r"\*[^*\n]+\*"),
    re.compile(r"“[^”\n]+”"),
    re.compile(r'"[^"\n]+"'),
]


def mask_mentions(text: str) -> str:
    # fenced code blocks first (multi-line; preserve line structure)
    text = FENCED_BLOCK.sub(
        lambda m: "\n".join(" " * len(ln) for ln in m.group(0).splitlines()), text
    )
    for pat in MENTION_SPANS:
        text = pat.sub(lambda m: " " * len(m.group(0)), text)
    return text


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    as_json = "--json" in sys.argv
    prose_mode = "--prose" in sys.argv

    if args and args[0] not in ("-",):
        text = open(args[0], encoding="utf-8", errors="replace").read()
        label = args[0]
    else:
        text = sys.stdin.read()
        label = "<stdin>"

    findings: list[str] = []
    lines = text.splitlines()
    paras = paragraphs(text)
    # vocabulary + parallelism scans run on mention-masked text (use-mention)
    masked = mask_mentions(text)
    masked_lines = masked.splitlines()
    masked_paras = paragraphs(masked)

    # S1 em-dash density (soft cap ~1 per 3 paragraphs)
    emdash_count = len(EMDASH.findall(text))
    cap = max(1, len(paras) // 3)
    if emdash_count > cap:
        findings.append(
            f"S1 em-dash overuse: {emdash_count} found, soft cap ~{cap} "
            f"({len(paras)} paragraphs). Swap most for periods/commas/parens."
        )

    # S2 negative parallelism / antithesis reflex
    for i, ln in enumerate(masked_lines, 1):
        for pat in ANTITHESIS:
            if pat.search(ln):
                findings.append(f"S2 negative parallelism L{i}: {ln.strip()[:90]}")
                break

    # S3 rhythm uniformity (low variance in sentence length = robotic cadence)
    sent_lens = [len(s.split()) for s in SENT_SPLIT.split(text) if len(s.split()) > 2]
    if len(sent_lens) >= 6:
        stdev = statistics.pstdev(sent_lens)
        mean = statistics.mean(sent_lens)
        cv = stdev / mean if mean else 0
        if cv < 0.45:
            findings.append(
                f"S3 uniform rhythm: sentence-length CV={cv:.2f} (<0.45 = robotic). "
                f"mean={mean:.0f}w stdev={stdev:.0f}. Mix short punches with long builds."
            )
        # also: runs of 3+ near-identical-length sentences
        run = 1
        for a, b in zip(sent_lens, sent_lens[1:]):
            run = run + 1 if abs(a - b) <= 3 else 1
            if run >= 4:
                findings.append(
                    "S3 length run: 4+ consecutive sentences within ±3 words of "
                    "each other. Break the meter."
                )
                break

    # S4 paragraph uniformity
    para_lens = [len(p.split()) for p in paras if len(p.split()) > 5]
    if len(para_lens) >= 4:
        pstdev = statistics.pstdev(para_lens)
        pmean = statistics.mean(para_lens)
        pcv = pstdev / pmean if pmean else 0
        if pcv < 0.30:
            findings.append(
                f"S4 evenly paced paragraphs: CV={pcv:.2f} (<0.30). Vary: mix a "
                "one-sentence paragraph into the longer blocks."
            )

    # S5 throat-clearing openers (paragraph starts)
    for p in paras:
        if OPENERS.match(p):
            findings.append(f"S5 throat-clearing opener: {p.strip()[:80]}")

    # S6 connective filler
    fil = FILLER.findall(text)
    if fil:
        c = Counter(w.lower() for w in fil)
        findings.append(
            "S6 connective filler: " + ", ".join(f"{w}×{n}" for w, n in c.most_common())
        )

    # S7 closing bow
    for p in paras:
        if CLOSERS.match(p):
            findings.append(f"S7 closing-bow wrap-up: {p.strip()[:80]}")

    # S8 banned vocabulary
    if HARD_BAN:
        hits = HARD_BAN.findall(masked)
        if hits:
            c = Counter(w.lower() for w in hits)
            findings.append(
                "S8 hard-ban vocabulary (measured AI markers — replace): "
                + ", ".join(f"{w}×{n}" for w, n in c.most_common())
            )
    if STRONG_FLAG:
        hits = STRONG_FLAG.findall(masked)
        if len(hits) >= 2:  # one may be deliberate; a cluster is a tell
            c = Counter(w.lower() for w in hits)
            findings.append(
                "S8 strong-flag vocabulary cluster: "
                + ", ".join(f"{w}×{n}" for w, n in c.most_common())
            )

    # S9 copulative avoidance
    if COPULATIVE:
        hits = COPULATIVE.findall(masked)
        if hits:
            c = Counter(h.lower() for h in hits)
            findings.append(
                "S9 copulative avoidance (prefer plain is/are/has): "
                + ", ".join(f"'{w}'×{n}" for w, n in c.most_common())
            )

    # S10 rule-of-three compulsion
    triads = TRIAD.findall(text)
    if len(triads) >= 3 and len(paras) > 0 and len(triads) / max(len(paras), 1) > 0.5:
        findings.append(
            f"S10 rule-of-three compulsion: {len(triads)} comma-triads in "
            f"{len(paras)} paragraphs. Vary list lengths (2 items, 4 items, none)."
        )

    # S11 vague attribution
    for i, ln in enumerate(masked_lines, 1):
        m = VAGUE_ATTRIBUTION.search(ln)
        if m:
            findings.append(f"S11 vague attribution L{i}: '{m.group(0)}' — name the source.")

    # S12 markdown in prose contexts (opt-in)
    if prose_mode:
        md = MARKDOWN.findall(text)
        if md:
            findings.append(
                f"S12 markdown artifacts in prose: {len(md)} (bold/headers/bullets). "
                "Strip for plain-prose targets."
            )

    # S13 density-watch clusters (common words, AI-elevated)
    if DENSITY_WATCH:
        for idx, p in enumerate(masked_paras, 1):
            hits = DENSITY_WATCH.findall(p)
            words_in_p = len(p.split())
            if words_in_p > 30 and len(hits) >= 4:
                c = Counter(w.lower() for w in hits)
                findings.append(
                    f"S13 density-watch cluster in paragraph {idx}: "
                    + ", ".join(f"{w}×{n}" for w, n in c.most_common())
                )

    # ── report ──
    if as_json:
        print(json.dumps({"file": label, "clean": not findings, "findings": findings}, indent=1))
        return 0 if not findings else 1

    if not findings:
        print(
            f"OK {label}: Tier-1 clean. Now do the Tier-2 hand-pass (visible "
            "reasoning, anti-sycophancy, concreteness, committed judgment) — "
            "the linter can't see those."
        )
        return 0

    print(f"FAIL {label}: {len(findings)} Tier-1 tell(s):")
    for f in findings:
        print(f"  - {f}")
    print("\nFix these, then the Tier-2 hand-pass (SKILL.md). Clean lint != reads human.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
