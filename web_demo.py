"""Local, no-dependency test build. No browser action can invoke a paid API."""
import argparse
import json
import math
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from scenarios import report

ROOT = Path(__file__).resolve().parent


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path)
        if path.path == "/":
            self.reply(200, (ROOT / "web/index.html").read_bytes(), "text/html; charset=utf-8")
        elif path.path == "/api/evaluate":
            try:
                q = parse_qs(path.query)
                cash = float(q.get("cash", ["0"])[0])
                minutes = int(q.get("minutes", ["5"])[0])
                if not math.isfinite(cash) or not 0 <= cash <= 10000 or not 0 <= minutes <= 10000:
                    raise ValueError()
                result = report(cash, q.get("verified", ["true"])[0] == "true", minutes)
                self.reply(200, json.dumps(result).encode(), "application/json")
            except (ValueError, OverflowError):
                self.reply(400, b'{"error":"Enter a nonnegative cash amount and whole minutes, up to 10000."}', "application/json")
        elif path.path == "/api/inference":
            # Only this explicit evidence file is exposed; never serve the repository or .env.
            evidence = ROOT / "evidence/nebius-run.json"
            data = json.loads(evidence.read_text()) if evidence.exists() else {"status": "pending"}
            self.reply(200, json.dumps(data).encode(), "application/json")
        else:
            self.reply(404, b"Not found", "text/plain")

    def reply(self, status, body, content_type):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    print(f"Earn Before Spend: http://127.0.0.1:{args.port} — no model calls", flush=True)
    ThreadingHTTPServer(("127.0.0.1", args.port), Handler).serve_forever()
