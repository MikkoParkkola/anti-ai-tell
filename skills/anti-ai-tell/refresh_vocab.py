#!/usr/bin/env python3
"""refresh_vocab — keep the AI-tell wordlists from rotting (AAT.TXT.2).

The blocklist is a depreciating asset: 'delve' era gave way to 'showcasing' era.
This refreshes vocabulary.json's `updated` stamp and merges in new markers from a
snapshot of WP:AISIGNS / corpus studies. Run quarterly (cron); --dry-run for CI so
the diff is deterministic and reviewable before it lands.

The network scrape is intentionally NOT built in here — it's a trust boundary and
a moving target. Feed a vetted snapshot file (one term per line, '#' comments ok).
ponytail: the mechanism is the deliverable; the data source stays human-vetted.

Usage:
    python3 refresh_vocab.py --snapshot new_terms.txt [--dry-run] [--bucket strong_flag]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VOCAB = HERE / "vocabulary.json"
STAMP_DATE = "see --date"  # passed in; no Date.now in this environment by policy


def refresh(snapshot: Path, bucket: str, date: str, dry_run: bool) -> dict:
    vocab = json.loads(VOCAB.read_text(encoding="utf-8"))
    existing = {w.lower() for b in vocab.values()
                if isinstance(b, dict) for w in b.get("words", [])}
    new_terms = []
    for line in snapshot.read_text(encoding="utf-8").splitlines():
        t = line.split("#")[0].strip()
        if t and t.lower() not in existing:
            new_terms.append(t)
    summary = {"bucket": bucket, "added": new_terms, "added_count": len(new_terms),
               "prev_updated": vocab.get("_meta", {}).get("updated"), "new_updated": date}
    if not dry_run and new_terms:
        vocab.setdefault(bucket, {}).setdefault("words", []).extend(new_terms)
        vocab.setdefault("_meta", {})["updated"] = date
        VOCAB.write_text(json.dumps(vocab, indent=2) + "\n", encoding="utf-8")
        summary["written"] = True
    else:
        summary["written"] = False
    return summary


def main(argv: list[str]) -> int:
    if "--snapshot" not in argv:
        print(__doc__); return 0
    snap = Path(argv[argv.index("--snapshot") + 1])
    bucket = argv[argv.index("--bucket") + 1] if "--bucket" in argv else "strong_flag"
    date = argv[argv.index("--date") + 1] if "--date" in argv else "0000-00-00"
    dry = "--dry-run" in argv
    print(json.dumps(refresh(snap, bucket, date, dry), indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
