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
ok("Mikko Parkkola" in privacy, "PRIVACY.md names Mikko Parkkola")
ok("text is not sent to the author" in privacy.lower(),
   "PRIVACY.md says text is not sent to the author")
ok("reads the files" in privacy and "fingerprint" in privacy and "stores" in privacy.lower(),
   "PRIVACY.md says what the plugin reads and stores")
ok("https://telemetry.revaluator.ai/v1/heartbeat" in privacy,
   "PRIVACY.md names the heartbeat URL")
ok("telemetry.trvl.app" not in privacy, "PRIVACY.md does not name the old host")
ok("install_id" in privacy and "city name and country code" in privacy,
   "PRIVACY.md states the stored heartbeat fields")
ok("Coordinates and the IP are not written" in privacy,
   "PRIVACY.md states that coordinates and the IP are not stored")
ok("ANTI_AI_TELL_NO_TELEMETRY" in privacy and "NO_TELEMETRY" in privacy
   and "DO_NOT_TRACK" in privacy, "PRIVACY.md names the opt-out switches")
ok("do not open a network connection" not in privacy.lower(),
   "PRIVACY.md no longer claims the tools open no network connection")
hb = (PLUGIN / "hooks" / "heartbeat.py").read_text(encoding="utf-8")
ok(f'VERSION = "{manifest["version"]}"' in hb, "heartbeat version matches plugin.json")
ok((ROOT / "hooks" / "heartbeat.py").read_bytes() == (PLUGIN / "hooks" / "heartbeat.py").read_bytes(),
   "repo heartbeat.py matches the plugin copy")
session = (PLUGIN / "hooks" / "session_fingerprint_inject.py").read_text(encoding="utf-8")
ok("heartbeat.maybe_send()" in session, "session hook attempts the daily heartbeat")
email = re.compile(r"(?i)[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}")
for path in PLUGIN.rglob("*"):
    if path.is_file():
        ok(email.search(path.read_text(encoding="utf-8")) is None, f"{path.relative_to(ROOT)} has no email")
ok("mcpServers" not in manifest, "plugin is skills and hooks, not an MCP server")
ok(not (PLUGIN / ".mcp.json").exists(), "plugin folder has no .mcp.json")

print(f"\nALL {PASS} CHECKS PASSED")
