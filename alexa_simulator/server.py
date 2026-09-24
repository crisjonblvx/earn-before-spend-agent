"""Local Alexa+ style simulator for Earn Before Spend.

Default mode is fully deterministic and makes no network or model-provider call.
It exists to demonstrate the user experience without consuming AWS or other
credits. A future contest demo may add an explicitly authorized Strands-backed
narration layer, but the economic gate remains authoritative.
"""
from __future__ import annotations

import json
import sys
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from core import Opportunity, Pathway, rank  # noqa: E402


class Handler(BaseHTTPRequestHandler):
    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path in {"/", "/index.html"}:
            body = (ROOT / "index.html").read_bytes()
            self._send(200, body, "text/html; charset=utf-8")
            return
        if path == "/health":
            self._send(200, b'{"ok":true,"mode":"deterministic"}', "application/json")
            return
        self._send(404, b'{"error":"not_found"}', "application/json")

    def do_POST(self) -> None:  # noqa: N802
        if urlparse(self.path).path != "/api/rank":
            self._send(404, b'{"error":"not_found"}', "application/json")
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = json.loads(self.rfile.read(length) or b"{}")
            candidates = raw.get("opportunities", [])[:3]
            opportunities: list[Opportunity] = []
            for item in candidates:
                item = dict(item)
                item["pathway"] = Pathway(item["pathway"])
                opportunities.append(Opportunity(**item))

            results = [asdict(item) for item in rank(opportunities)]
            qualified = [item for item in results if item["eligible"]]
            top = qualified[0] if qualified else None
            response = {
                "mode": "deterministic_no_provider_call",
                "voice": (
                    "I found a qualified zero-cash path. I can prepare the next bounded action, "
                    "but any terms, identity, publication, or money step stays with you."
                    if top
                    else "I did not find a candidate that passes the zero-cash rules."
                ),
                "top_candidate": top,
                "ranking": results,
                "scoreboard": {
                    "starting_capital_usd": 0,
                    "new_cash_spent_usd": 0,
                    "verified_earnings_usd": 0,
                },
            }
            body = json.dumps(response, indent=2).encode()
            self._send(200, body, "application/json")
        except (ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
            body = json.dumps({"error": "invalid_request", "detail": str(exc)}).encode()
            self._send(400, body, "application/json")

    def log_message(self, format: str, *args) -> None:  # noqa: A002
        return


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 8765), Handler)
    print("Alexa+ simulator: http://127.0.0.1:8765")
    print("Mode: deterministic; no provider calls or paid resources")
    server.serve_forever()


if __name__ == "__main__":
    main()
