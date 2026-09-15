"""One explicit HTTPS request, no agent loop, retries, redirects, or billing changes.

This validates the model's explanation of already-computed tool results, not
autonomous Strands tool use. A token cap is not a provider-side spending cap.
"""
import json
import os
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from scenarios import report

ENDPOINT = "https://api.tokenfactory.us-central1.nebius.com/v1/chat/completions"
MODEL = "nvidia/nemotron-3-super-120b-a12b"
ROOT = Path(__file__).resolve().parent


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def require_gate():
    if os.environ.get("ALLOW_LIVE_NEBIUS_TEST") != "YES":
        raise RuntimeError("Blocked: explicit live-test authorization is missing.")
    if os.environ.get("NEBIUS_PROMO_COVERAGE_CONFIRMED") != "YES":
        raise RuntimeError("Blocked: promotional credit coverage and disabled paid usage must be confirmed.")
    key = os.environ.get("NEBIUS_API_KEY", "").strip()
    if not key:
        raise RuntimeError("Blocked: an environment-scoped Nebius key is missing.")
    return key


def run_once(destination=ROOT / "evidence"):
    key = require_gate()
    destination.mkdir(parents=True, exist_ok=True)
    lock = destination / "nebius-request.lock"
    try:
        fd = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        raise RuntimeError("Blocked: a request was already attempted. Review the evidence before manually clearing the lock.")
    os.close(fd)
    result = report()
    body = json.dumps({"model": MODEL, "messages": [
        {"role": "system", "content": "Explain deterministic economic tool results. Never override blockers. Never count hypothetical payouts as earnings. Preserve human approval for terms and payout setup. Answer concisely in under 150 words."},
        {"role": "user", "content": "These are illustrative scenarios, not real offers. Explain which option qualifies, why the others fail, and the next bounded action and human gate. " + json.dumps(result)}],
        "max_tokens": 350, "temperature": 0, "stream": False}).encode()
    request = urllib.request.Request(ENDPOINT, data=body, headers={
        "Authorization": "Bearer " + key, "Content-Type": "application/json"})
    evidence = {"status": "failed", "created_at": datetime.now(timezone.utc).isoformat(),
        "model": MODEL, "endpoint": ENDPOINT, "request_attempts": 1,
        "requested_max_tokens": 350, "scope": "explanation_of_precomputed_python_results",
        "deterministic_results": result, "cash_cost_usd": None,
        "cost_note": "Reconcile actual credit consumption in the provider console; token cap is not a cash cap."}
    started = time.monotonic()
    try:
        with urllib.request.build_opener(NoRedirect).open(request, timeout=45) as response:
            payload = json.loads(response.read(1024 * 1024))
        choice = payload["choices"][0]
        output = choice["message"].get("content")
        if not isinstance(output, str) or not output.strip():
            raise ValueError("No nonempty assistant content returned")
        evidence.update(status="completed", output=output.replace(key, "[REDACTED]"),
            finish_reason=choice.get("finish_reason"), usage=payload.get("usage"),
            returned_model=payload.get("model"), review_required=True)
    except Exception as exc:
        # Do not persist raw exception bodies or headers, which can contain secrets.
        evidence["error_type"] = type(exc).__name__
        if isinstance(exc, urllib.error.HTTPError):
            evidence["http_status"] = exc.code
    evidence["latency_seconds"] = round(time.monotonic() - started, 3)
    path = destination / "nebius-run.json"
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as stream:
        json.dump(evidence, stream, indent=2)
    return evidence


if __name__ == "__main__":
    try:
        result = run_once()
        print("One-request evaluation:", result["status"], "— see local evidence/nebius-run.json")
        raise SystemExit(0 if result["status"] == "completed" else 1)
    except RuntimeError as exc:
        raise SystemExit(str(exc))
