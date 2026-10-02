#!/usr/bin/env python3
"""Heartbeat client checks. Talks only to a local server."""

from __future__ import annotations

import json
import os
import stat
import sys
import tempfile
import threading
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "hooks"))

import heartbeat  # noqa: E402


def main() -> int:
    opt_out_writes_nothing()
    slot_is_claimed_before_the_second_call()
    endpoint_rules()
    post_hits_local_server()
    print("heartbeat ok")
    return 0


def opt_out_writes_nothing() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        posts: list[bytes] = []
        for env, version in (
            ({}, "dev"),
            ({"NO_TELEMETRY": "1"}, "2.1.0"),
            ({"DO_NOT_TRACK": "yes"}, "2.1.0"),
            ({"ANTI_AI_TELL_NO_TELEMETRY": "1"}, "2.1.0"),
            ({"CI": "true"}, "2.1.0"),
        ):
            heartbeat.maybe_send(
                version,
                env=env,
                home=home,
                now=datetime(2026, 10, 2, tzinfo=timezone.utc),
                poster=lambda _url, body: posts.append(body),
            )
        assert posts == []
        assert not (home / ".anti-ai-tell").exists()
        heartbeat.maybe_send(
            "2.1.0",
            env={"NO_TELEMETRY": "0", "DO_NOT_TRACK": "false"},
            home=home,
            now=datetime(2026, 10, 2, 12, tzinfo=timezone.utc),
            poster=lambda _url, body: posts.append(body),
        )
        assert len(posts) == 1
        payload = json.loads(posts[0])
        assert set(payload) == {
            "project",
            "event",
            "version",
            "runtime",
            "install_id",
            "install_date",
            "machine_id",
        }
        assert payload["project"] == "anti-ai-tell"
        assert payload["event"] == "heartbeat"
        assert payload["version"] == "2.1.0"
        assert payload["install_date"] == "2026-10-02"
        assert len(payload["install_id"]) == 32
        assert len(payload["machine_id"]) == 32
        assert (home / ".revaluator" / "machine-id").read_text(encoding="utf-8") == payload["machine_id"]


def slot_is_claimed_before_the_second_call() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        posts: list[str] = []
        now = datetime(2026, 10, 2, 12, tzinfo=timezone.utc)

        def record(url: str, body: bytes) -> None:
            assert url.startswith("https://telemetry.revaluator.ai/")
            assert (home / ".anti-ai-tell" / "telemetry" / "heartbeat").is_file()
            posts.append("one")
            assert b"hostname" not in body

        heartbeat.maybe_send("2.1.0", env={}, home=home, now=now, poster=record)
        assert posts == ["one"]
        stamp = (home / ".anti-ai-tell" / "telemetry" / "heartbeat").read_text(encoding="utf-8")
        assert stamp == "2026-10-02T12:00:00Z"
        mode = (home / ".anti-ai-tell" / "telemetry" / "install-id").stat().st_mode
        assert stat.S_IMODE(mode) == 0o600
        heartbeat.maybe_send(
            "2.1.0",
            env={},
            home=home,
            now=now + timedelta(hours=6),
            poster=lambda _url, _body: posts.append("two"),
        )
        assert posts == ["one"]
        heartbeat.maybe_send(
            "2.1.0",
            env={},
            home=home,
            now=now + timedelta(hours=24),
            poster=lambda _url, _body: posts.append("three"),
        )
        assert posts == ["one", "three"]


def endpoint_rules() -> None:
    assert heartbeat.resolve_endpoint({}) == heartbeat.DEFAULT_ENDPOINT
    assert heartbeat.resolve_endpoint({heartbeat.ENDPOINT_ENV: ""}) == heartbeat.DEFAULT_ENDPOINT
    assert heartbeat.resolve_endpoint({heartbeat.ENDPOINT_ENV: "ftp://example.test"}) == ""
    assert (
        heartbeat.resolve_endpoint({heartbeat.ENDPOINT_ENV: "http://127.0.0.1:9/v1/heartbeat"})
        == "http://127.0.0.1:9/v1/heartbeat"
    )
    assert heartbeat.suppressed("2.1.0", {"NO_TELEMETRY": "0"}) is False
    assert heartbeat.suppressed("2.1.0", {"NO_TELEMETRY": "false"}) is False


def post_hits_local_server() -> None:
    seen: list[bytes] = []

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self) -> None:  # noqa: N802
            length = int(self.headers.get("Content-Length", "0"))
            seen.append(self.rfile.read(length))
            self.send_response(204)
            self.end_headers()

        def log_message(self, _fmt: str, *_args) -> None:
            return

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.handle_request, daemon=True)
    thread.start()
    body = heartbeat.build_body("2.1.0", "0123456789abcdef0123456789abcdef")
    assert body is not None
    previous = os.environ.get("NO_PROXY")
    os.environ["NO_PROXY"] = "*"
    try:
        heartbeat.post(f"http://127.0.0.1:{port}/v1/heartbeat", body)
    finally:
        if previous is None:
            os.environ.pop("NO_PROXY", None)
        else:
            os.environ["NO_PROXY"] = previous
    thread.join(timeout=3)
    server.server_close()
    assert seen == [body]


if __name__ == "__main__":
    sys.exit(main())
