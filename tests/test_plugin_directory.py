#!/usr/bin/env python3
"""Directory-bundle checks against the shipped plugin folder. Stdlib only.

    python3 tests/test_plugin_directory.py   # exit 0 = all pass

Reads plugins/anti-ai-tell in place. Does not copy the plugin tree.
Release tags in this repo are "v" plus semver; plugin.json stores the semver.
"""
from __future__ import annotations

import json
import os
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins" / "anti-ai-tell"
RELEASES_LATEST = "https://api.github.com/repos/MikkoParkkola/anti-ai-tell/releases/latest"
SUPPORT = "https://github.com/MikkoParkkola/anti-ai-tell/issues"

PASS = 0


def ok(cond, label):
    global PASS
    assert cond, f"FAIL: {label}"
    PASS += 1
    print(f"  ok: {label}")


def plugin_manifests(root: Path) -> list[Path]:
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        if Path(dirpath).name == ".claude-plugin" and "plugin.json" in filenames:
            found.append(Path(dirpath) / "plugin.json")
    return found


def words_outside_fences(text: str) -> int:
    kept = []
    fenced = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if not fenced:
            kept.append(line)
    return len(" ".join(kept).split())


def latest_release_tag() -> str:
    req = urllib.request.Request(
        RELEASES_LATEST,
        headers={
            "User-Agent": "anti-ai-tell-plugin-directory-test",
            "Accept": "application/vnd.github+json",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    tag = payload["tag_name"]
    assert isinstance(tag, str) and tag, "releases/latest returned no tag_name"
    return tag


def version_matches_tag(version: str, tag: str) -> bool:
    if version == tag:
        return True
    return tag.startswith("v") and version == tag[1:]


print("plugin directory bundle:")
manifests = plugin_manifests(ROOT)
ok(manifests == [PLUGIN / ".claude-plugin" / "plugin.json"],
   "exactly one .claude-plugin/plugin.json, the shipped plugin")

manifest = json.loads(manifests[0].read_text(encoding="utf-8"))
tag = latest_release_tag()
ok(version_matches_tag(manifest["version"], tag),
   f"plugin.json version {manifest['version']!r} equals release tag {tag!r}")

readme = (PLUGIN / "README.md").read_text(encoding="utf-8")
ok(words_outside_fences(readme) >= 40,
   f"README has {words_outside_fences(readme)} words outside code fences")
examples = [ln for ln in readme.splitlines() if re.match(r"^### Example", ln)]
ok(len(examples) >= 3, f"{len(examples)} headings match ^### Example")

ok((PLUGIN / "LICENSE").read_bytes() == (ROOT / "LICENSE").read_bytes(),
   "plugin LICENSE bytes equal the repo root LICENSE")

privacy = (PLUGIN / "PRIVACY.md").read_text(encoding="utf-8")
ok(SUPPORT in privacy, "PRIVACY.md contains the GitHub issues support line")
ok("text is not sent to the author" in privacy.lower(),
   "PRIVACY.md says text is not sent to the author")
ok("@" not in privacy and not re.search(r"(?i)[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}", privacy),
   "PRIVACY.md contains no email")

print(f"\nALL {PASS} CHECKS PASSED")
