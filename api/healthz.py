"""Vercel Python Function exposing judge-demo health without making provider calls."""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler

from judge_demo import live_nebius_enabled


class handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802 - stdlib/Vercel handler API
        body = {
            "ok": True,
            "live_nebius_enabled": live_nebius_enabled(),
            "provider_call_made": False,
        }
        payload = json.dumps(body).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(payload)
