"""Vercel Python Function for the explicitly authorized Nebius explanation call."""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler

from judge_demo import explanation_snapshot


class handler(BaseHTTPRequestHandler):
    def _send(self, status: int, body: dict) -> None:
        payload = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(payload)

    def do_POST(self) -> None:  # noqa: N802 - stdlib/Vercel handler API
        status, body = explanation_snapshot()
        self._send(status, body)

    def do_GET(self) -> None:  # noqa: N802
        self._send(405, {"error": "method_not_allowed", "provider_call_made": False})
