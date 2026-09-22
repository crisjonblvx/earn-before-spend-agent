"""Zero-cost simulated Alexa+ experience for Earn Before Spend.

This is intentionally a *simulation* for the Amazon Build, Ship, Shape Alexa+ track.
The official track allows a simulated Alexa+ experience in a web app using a
preferred agentic tool. No Amazon runtime, paid API, or device is required by
this module.

Economic authority remains deterministic in core.py.
"""
from __future__ import annotations

import json
import os
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from core import Opportunity, Pathway, rank


def alexa_opportunities() -> list[Opportunity]:
    """Small demo set that makes the zero-capital safety boundary visible."""
    return [
        Opportunity(
            title="Paid-entry growth accelerator",
            pathway=Pathway.COMPETITION,
            payout_usd=50_000,
            new_cash_required_usd=99,
            cj_minutes_required=15,
            deadline_hours=48,
            payout_probability=0.02,
            legitimacy_score=90,
            fit_score=92,
            rights_clear=True,
            eligibility_clear=True,
            payout_verifiable=True,
            terms_require_human_acceptance=True,
            source_url="https://example.com/paid-accelerator",
        ),
        Opportunity(
            title="Expiring no-fee agent competition",
            pathway=Pathway.COMPETITION,
            payout_usd=10_000,
            new_cash_required_usd=0,
            cj_minutes_required=15,
            deadline_hours=12,
            payout_probability=0.02,
            legitimacy_score=95,
            fit_score=98,
            rights_clear=True,
            eligibility_clear=True,
            payout_verifiable=True,
            terms_require_human_acceptance=True,
            source_url="https://example.com/competition",
        ),
        Opportunity(
            title="Fixed-scope code bounty",
            pathway=Pathway.BOUNTY,
            payout_usd=100,
            new_cash_required_usd=0,
            cj_minutes_required=10,
            deadline_hours=168,
            payout_probability=0.70,
            legitimacy_score=82,
            fit_score=95,
            rights_clear=True,
            eligibility_clear=True,
            payout_verifiable=True,
            terms_require_human_acceptance=True,
            source_url="https://example.com/bounty",
        ),
    ]


def ranked_snapshot() -> list[dict]:
    return [asdict(item) for item in rank(alexa_opportunities())]


def simulate_alexa_plus(utterance: str) -> dict:
    """Return a speakable, auditable simulated Alexa+ response."""
    text = (utterance or "").strip()
    normalized = text.lower()
    ranking = ranked_snapshot()
    blocked = [item for item in ranking if not item["eligible"]]
    qualified = [item for item in ranking if item["eligible"]]

    if not text:
        return {
            "voice": (
                "Try asking: What is my best zero-capital earning move? "
                "Or: Should I pay ninety-nine dollars to enter the accelerator?"
            ),
            "intent": "help",
            "economic_authority": "deterministic core.py",
            "provider_call_made": False,
        }

    pay_intent = any(token in normalized for token in ("pay", "spend", "$99", "99 dollars", "ninety-nine"))
    accelerator_intent = "accelerator" in normalized or "50,000" in normalized or "50000" in normalized

    if pay_intent and accelerator_intent:
        candidate = next(item for item in blocked if item["title"] == "Paid-entry growth accelerator")
        return {
            "voice": (
                "No. I would not advance that option. It requires new cash, "
                "so the zero-capital gate blocks it before payout size is considered."
            ),
            "intent": "evaluate_spend_request",
            "candidate": candidate,
            "human_gate": "none; deterministic policy blocks the spend",
            "economic_authority": "deterministic core.py",
            "provider_call_made": False,
        }

    if any(token in normalized for token in ("best", "next", "earn", "money", "opportunity", "zero capital", "zero-capital")):
        top = qualified[0]
        gate = (
            "Human approval is still required before accepting third-party terms."
            if top["requires_human_decision"]
            else "No human terms gate detected in the demo record."
        )
        return {
            "voice": (
                f"Your best qualified demo move is {top['title']}. "
                f"It scores {top['score']}. {gate} "
                "I am not counting a possible prize as earned money."
            ),
            "intent": "recommend_next_move",
            "candidate": top,
            "human_gate": gate,
            "economic_authority": "deterministic core.py",
            "provider_call_made": False,
        }

    return {
        "voice": (
            "I can rank zero-capital earning options or explain why a spending request is blocked. "
            "Try asking for the best next move."
        ),
        "intent": "help",
        "economic_authority": "deterministic core.py",
        "provider_call_made": False,
    }


HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Earn Before Spend — Simulated Alexa+ Experience</title>
<style>
body{font-family:system-ui,-apple-system,sans-serif;background:#090b10;color:#f5f7fb;margin:0;max-width:900px;padding:32px;margin:auto}
h1{font-size:clamp(2.4rem,7vw,5.5rem);line-height:.92;margin:.2em 0}
.a{color:#62d8ff}.card{background:#141923;border:1px solid #303a4b;border-radius:20px;padding:20px;margin:16px 0}
input{width:100%;box-sizing:border-box;padding:15px;border-radius:12px;border:1px solid #39465d;background:#0c1017;color:#fff;font-size:1rem}
button{padding:12px 16px;border:0;border-radius:12px;font-weight:800;cursor:pointer;margin:8px 6px 0 0}
.primary{background:#62d8ff;color:#071018}.ghost{background:#222b38;color:#eef}
pre{white-space:pre-wrap;background:#07090d;padding:16px;border-radius:12px;min-height:110px}.small{color:#aeb7c8}
.pill{display:inline-block;padding:5px 9px;border:1px solid #39465d;border-radius:999px;margin:3px}
</style></head><body>
<div class="small">Amazon Build, Ship, Shape — simulated Alexa+ experience</div>
<h1>Earn <span class="a">Before</span> Spend</h1>
<p>Ask a voice-assistant-style question. The simulated Alexa+ layer explains the decision; deterministic code keeps authority over money rules.</p>
<div><span class="pill">$0 new cash</span><span class="pill">no device required</span><span class="pill">no paid API</span><span class="pill">human terms gate</span></div>
<div class="card">
<label for="u"><b>Say to Alexa+</b></label>
<input id="u" value="What is my best zero-capital earning move?">
<button class="primary" id="ask">Ask</button>
<button class="ghost" data-q="Should I pay $99 to enter the $50,000 accelerator?">Test the spend guardrail</button>
<button class="ghost" data-q="What should I do next to earn money without spending any?">Find the next move</button>
</div>
<h2>Alexa+ response</h2>
<pre id="out">Ready.</pre>
<script>
async function ask(q){document.querySelector('#u').value=q;const r=await fetch('/api/alexa',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({utterance:q})});const d=await r.json();document.querySelector('#out').textContent=d.voice+"\n\n"+JSON.stringify(d,null,2);}
document.querySelector('#ask').onclick=()=>ask(document.querySelector('#u').value);
document.querySelectorAll('[data-q]').forEach(b=>b.onclick=()=>ask(b.dataset.q));
</script></body></html>"""


class Handler(BaseHTTPRequestHandler):
    server_version = "EarnBeforeSpendAlexaSim/1.0"

    def _json(self, status: int, payload: dict) -> None:
        raw = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self) -> None:  # noqa: N802
        path = self.path.split("?", 1)[0]
        if path == "/":
            raw = HTML.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(raw)
            return
        if path == "/healthz":
            self._json(200, {"ok": True, "mode": "simulated_alexa_plus", "paid_provider_calls": False})
            return
        self._json(404, {"error": "not_found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path.split("?", 1)[0] != "/api/alexa":
            self._json(404, {"error": "not_found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length) or b"{}")
        except (ValueError, json.JSONDecodeError):
            self._json(400, {"error": "invalid_json"})
            return
        self._json(200, simulate_alexa_plus(str(payload.get("utterance", ""))))

    def log_message(self, fmt: str, *args) -> None:
        print(f"alexa-sim: {fmt % args}")


def main() -> None:
    port = int(os.environ.get("PORT", "8010"))
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"Simulated Alexa+ experience listening on http://0.0.0.0:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
