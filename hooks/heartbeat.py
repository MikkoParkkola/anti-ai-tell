#!/usr/bin/env python3
"""Daily heartbeat. Failure is ignored. Importing does no I/O."""

from __future__ import annotations

import json
import os
import platform
import secrets
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

PROJECT = "anti-ai-tell"
VERSION = "2.1.0"
EVENT = "heartbeat"
DEFAULT_ENDPOINT = "https://telemetry.revaluator.ai/v1/heartbeat"
MAX_BODY = 2048
DAY_SECONDS = 24 * 60 * 60
OPT_OUT = ("DO_NOT_TRACK", "NO_TELEMETRY", "ANTI_AI_TELL_NO_TELEMETRY")
ENDPOINT_ENV = "ANTI_AI_TELL_TELEMETRY_ENDPOINT"
CI_ENVS = (
    "CI",
    "CONTINUOUS_INTEGRATION",
    "GITHUB_ACTIONS",
    "GITLAB_CI",
    "CIRCLECI",
    "TRAVIS",
    "BUILDKITE",
    "DRONE",
    "JENKINS_URL",
    "TEAMCITY_VERSION",
    "BITBUCKET_BUILD_NUMBER",
    "APPVEYOR",
    "CODEBUILD_BUILD_ID",
)


def _truthy(value: str | None) -> bool:
    return bool(value) and value not in ("0", "false")


def suppressed(version: str, env: dict[str, str] | None = None) -> bool:
    current = os.environ if env is None else env
    if not version or version == "dev":
        return True
    if any(_truthy(current.get(name)) for name in CI_ENVS):
        return True
    if any(_truthy(current.get(name)) for name in OPT_OUT):
        return True
    return False


def resolve_endpoint(env: dict[str, str] | None = None) -> str:
    current = os.environ if env is None else env
    override = current.get(ENDPOINT_ENV) or ""
    if not override:
        return DEFAULT_ENDPOINT
    if override.startswith("https://") or override.startswith("http://"):
        return override
    return ""


def state_dir(home: Path | None = None) -> Path | None:
    if home is None:
        home_text = os.environ.get("HOME") or ""
        if not home_text:
            return None
        home = Path(home_text)
    return home / ".anti-ai-tell" / "telemetry"


def _stamp(when: datetime) -> str:
    return when.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_stamp(text: str) -> datetime | None:
    cleaned = text.strip()
    if "." in cleaned and cleaned.endswith("Z"):
        cleaned = cleaned.split(".", 1)[0] + "Z"
    try:
        parsed = datetime.strptime(cleaned, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return None
    return parsed.replace(tzinfo=timezone.utc)


def due(directory: Path, now: datetime) -> bool:
    try:
        last = _parse_stamp((directory / "heartbeat").read_text(encoding="utf-8"))
    except OSError:
        return True
    if last is None:
        return True
    return (now - last).total_seconds() >= DAY_SECONDS


def mark_sent(directory: Path, now: datetime) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    try:
        directory.chmod(0o700)
    except OSError:
        pass
    dest = directory / "heartbeat"
    tmp = directory / "heartbeat.tmp"
    tmp.write_text(_stamp(now), encoding="utf-8")
    try:
        tmp.chmod(0o600)
    except OSError:
        pass
    tmp.replace(dest)


def install_id(directory: Path) -> str:
    return ensure_install(directory)[0]


def ensure_install(directory: Path) -> tuple[str, bool]:
    path = directory / "install-id"
    try:
        existing = path.read_text(encoding="utf-8").strip()
        if existing:
            return existing, False
    except OSError:
        pass
    value = secrets.token_hex(16)
    try:
        directory.mkdir(parents=True, exist_ok=True)
        directory.chmod(0o700)
        path.write_text(value, encoding="utf-8")
        path.chmod(0o600)
    except OSError:
        return "", False
    return value, True


def _valid_day(value: str) -> bool:
    if len(value) != 10 or value[4] != "-" or value[7] != "-":
        return False
    try:
        parsed = datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return False
    return parsed.strftime("%Y-%m-%d") == value


def install_date(directory: Path, now: datetime, fresh: bool) -> str:
    path = directory / "install-date"
    try:
        existing = path.read_text(encoding="utf-8").strip()
        if _valid_day(existing):
            return existing
    except OSError:
        pass
    day = now.astimezone(timezone.utc).strftime("%Y-%m-%d")
    if not fresh:
        try:
            birth = (directory / "install-id").stat().st_birthtime
            if birth > 86400:
                day = datetime.fromtimestamp(birth, timezone.utc).strftime("%Y-%m-%d")
        except (AttributeError, OSError, OverflowError, ValueError):
            pass
    try:
        directory.mkdir(parents=True, exist_ok=True)
        directory.chmod(0o700)
        path.write_text(day, encoding="utf-8")
        path.chmod(0o600)
    except OSError:
        pass
    return day


def machine_id(home: Path) -> str:
    directory = home / ".revaluator"
    path = directory / "machine-id"
    try:
        existing = path.read_text(encoding="utf-8").strip()
        if len(existing) == 32 and all(ch in "0123456789abcdef" for ch in existing):
            return existing
    except OSError:
        pass
    value = secrets.token_hex(16)
    try:
        directory.mkdir(parents=True, exist_ok=True)
        directory.chmod(0o700)
        path.write_text(value, encoding="utf-8")
        path.chmod(0o600)
    except OSError:
        return ""
    return value


def build_body(version: str, install: str, installed: str = "", machine: str = "") -> bytes | None:
    payload: dict[str, str] = {
        "project": PROJECT,
        "event": EVENT,
        "version": version,
        "runtime": f"{platform.system()}/{platform.machine()}/{platform.python_version()}",
    }
    if install:
        payload["install_id"] = install
    if installed:
        payload["install_date"] = installed
    if machine:
        payload["machine_id"] = machine
    body = json.dumps(payload).encode("utf-8")
    if len(body) > MAX_BODY:
        return None
    return body


def post(url: str, body: bytes, timeout: float = 3.0) -> None:
    request = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={"Content-Type": "application/json", "User-Agent": "heartbeat"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        response.read()


def _detach(url: str, body: bytes, directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    payload_path = directory / "heartbeat-body.tmp"
    payload_path.write_bytes(body)
    try:
        payload_path.chmod(0o600)
    except OSError:
        pass
    code = (
        "import pathlib,sys,urllib.request\n"
        "path=pathlib.Path(sys.argv[1])\n"
        "body=path.read_bytes()\n"
        "path.unlink(missing_ok=True)\n"
        "req=urllib.request.Request(sys.argv[2], data=body, method='POST',"
        " headers={'Content-Type':'application/json','User-Agent':'heartbeat'})\n"
        "urllib.request.urlopen(req, timeout=3).read()\n"
    )
    try:
        subprocess.Popen(
            [sys.executable, "-c", code, str(payload_path), url],
            start_new_session=True,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            close_fds=True,
        )
    except OSError:
        payload_path.unlink(missing_ok=True)


def maybe_send(
    version: str = VERSION,
    *,
    env: dict[str, str] | None = None,
    home: Path | None = None,
    now: datetime | None = None,
    poster=None,
) -> None:
    """Claim today's slot, then POST. Never raises."""
    try:
        _send(version, env=env, home=home, now=now, poster=poster)
    except Exception:
        return


def _send(version: str, *, env, home, now, poster) -> None:
    current = os.environ if env is None else env
    if suppressed(version, current):
        return
    url = resolve_endpoint(current)
    if not url:
        return
    directory = state_dir(home)
    if directory is None:
        return
    clock = now or datetime.now(timezone.utc)
    if not due(directory, clock):
        return
    mark_sent(directory, clock)
    install, fresh = ensure_install(directory)
    root = directory.parents[1] if home is None else home
    body = build_body(
        version,
        install,
        install_date(directory, clock, fresh),
        machine_id(root),
    )
    if body is None:
        return
    if poster is None:
        _detach(url, body, directory)
    else:
        poster(url, body)
