"""Zero-dependency judge web demo for Earn Before Spend.

The deterministic ranking is always available. A live Nebius call is possible only
when BOTH NEBIUS_API_KEY is configured and ALLOW_LIVE_NEBIUS=1 is explicitly set.
That double gate prevents a hosted preview from silently consuming inference.
"""
from __future__ import annotations

import json
import os
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Callable

from core import rank
from demo import sample_opportunities


HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Earn Before Spend — Judge Demo</title>
<style>
body{font-family:system-ui,-apple-system,sans-serif;background:#0b0d12;color:#f7f7fb;margin:0;padding:32px;max-width:980px;margin:auto}
h1{font-size:clamp(2rem,6vw,4.8rem);line-height:.95;margin:.2em 0}.k{color:#9ee86f}.card{background:#151923;border:1px solid #303747;border-radius:18px;padding:18px;margin:14px 0}.row{display:grid;grid-template-columns:1fr auto;gap:16px}.ok{color:#9ee86f}.blocked{color:#ff8f8f}button{background:#9ee86f;color:#10140d;border:0;border-radius:12px;padding:12px 18px;font-weight:800;cursor:pointer}button:disabled{opacity:.5}pre{white-space:pre-wrap;background:#090b10;border-radius:12px;padding:14px;overflow:auto}.small{color:#aeb7c8;font-size:.92rem}.pill{display:inline-block;border:1px solid #3b465b;border-radius:999px;padding:5px 10px;margin:3px}</style>
</head><body>
<div class="small">Nebius x NVIDIA Global AI Hackathon test build</div>
<h1>Earn <span class="k">Before</span> Spend</h1>
<p>A bounded economic agent: deterministic code decides what is eligible; NVIDIA Nemotron on Nebius Token Factory explains the next move without overriding the money rules.</p>
<div><span class="pill">$0 new seed capital</span><span class="pill">deterministic gate</span><span class="pill">Nemotron 3 Super</span><span class="pill">Token Factory</span></div>
<h2>Authoritative ranking</h2><div id="ranking" class="card">Loading…</div>
<h2>Nemotron explanation</h2>
<p class="small">The hosted demo is fail-closed. A live inference call requires an explicitly authorized server-side key plus <code>ALLOW_LIVE_NEBIUS=1</code>.</p>
<button id="explain">Run bounded explanation</button><pre id="model">No model call made yet.</pre>
<script>
const esc=s=>String(s).replace(/[&<>\"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;'}[c]));
async function load(){const r=await fetch('/api/ranking');const d=await r.json();document.querySelector('#ranking').innerHTML=d.ranking.map((x,i)=>`<div class="row"><div><b>${i+1}. ${esc(x.title)}</b><div class="small">${esc(x.reason)}</div></div><div class="${x.eligible?'ok':'blocked'}">${x.eligible?'QUALIFIED':'BLOCKED'} · ${x.score}</div></div>`).join('<hr style="border-color:#2a3140">');}
document.querySelector('#explain').onclick=async e=>{e.target.disabled=true;document.querySelector('#model').textContent='Requesting…';try{const r=await fetch('/api/explain',{method:'POST'});const d=await r.json();document.querySelector('#model').textContent=d.explanation||d.error||JSON.stringify(d,null,2);}finally{e.target.disabled=false;}};
load();
</script></body></html>"""


def deterministic_snapshot() -> dict:
    ranking = [asdict(item) for item in rank(sample_opportunities())]
    return {
        "mode": "deterministic_authority",
        "warning": "Planning priors are illustrative; they are not promised odds or earnings.",
        "ranking": ranking,
    }


def live_nebius_enabled() -> bool:
    return os.environ.get("ALLOW_LIVE_NEBIUS") == "1" and bool(os.environ.get("NEBIUS_API_KEY", "").strip())


def explanation_snapshot(*, explainer: Callable[[list[dict]], str] | None = None) -> tuple[int, dict]:
    if not live_nebius_enabled():
        return 503, {
            "error": "Live Nebius inference is fail-closed on this deployment. An authorized server-side key and ALLOW_LIVE_NEBIUS=1 are both required.",
            "provider_call_made": False,
        }

    if explainer is None:
        from nebius_model import explain_ranking
        explainer = explain_ranking

    ranking = deterministic_snapshot()["ranking"]
    try:
        explanation = explainer(ranking)
    except Exception as exc:  # Do not leak configuration or transport internals to judges.
        return 502, {"error": f"Bounded model explanation failed: {type(exc).__name__}", "provider_call_made": True}
    return 200, {
        "mode": "nebius_token_factory_nemotron",
        "model": "nvidia/nemotron-3-super-120b-a12b",
        "economic_authority": "deterministic ranking",
        "explanation": explanation,
        "provider_call_made": True,
    }


class Handler(BaseHTTPRequestHandler):
    server_version = "EarnBeforeSpend/1.0"

    def _send_json(self, status: int, payload: dict) -> None:
        raw = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self) -> None:  # noqa: N802 - stdlib handler API
        path = self.path.split("?", 1)[0]
        if path == "/":
            raw = HTML.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(raw)
            return
        if path == "/api/ranking":
            self._send_json(200, deterministic_snapshot())
            return
        if path == "/healthz":
            self._send_json(200, {"ok": True, "live_nebius_enabled": live_nebius_enabled()})
            return
        self._send_json(404, {"error": "not_found"})

    def do_POST(self) -> None:  # noqa: N802 - stdlib handler API
        path = self.path.split("?", 1)[0]
        if path != "/api/explain":
            self._send_json(404, {"error": "not_found"})
            return
        status, payload = explanation_snapshot()
        self._send_json(status, payload)

    def log_message(self, fmt: str, *args) -> None:
        print(f"judge-demo: {fmt % args}")


def main() -> None:
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"Judge demo listening on http://0.0.0.0:{port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
