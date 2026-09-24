"""Vercel Python Function exposing the deterministic ranking authority."""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler

from judge_demo import deterministic_snapshot


class handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802 - stdlib/Vercel handler API
        payload = json.dumps(deterministic_snapshot()).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(payload)

    def do_POST(self) -> None:  # noqa: N802
        self.send_response(405)
        self.send_header("Allow", "GET")
        self.end_headers()
