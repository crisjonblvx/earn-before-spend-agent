"""Sanitized preflight checks for one bounded Nebius Token Factory call."""
from __future__ import annotations

import os
from urllib.parse import urlparse

DEFAULT_BASE_URL = "https://api.tokenfactory.us-central1.nebius.com/v1/"
DEFAULT_MODEL_ID = "nvidia/nemotron-3-super-120b-a12b"


def evaluate(env=None):
    env = os.environ if env is None else env
    base_url = (env.get("NEBIUS_BASE_URL", "") or DEFAULT_BASE_URL).strip().rstrip("/")
    model_id = (env.get("NEBIUS_MODEL_ID", "") or DEFAULT_MODEL_ID).strip()
    parsed = urlparse(base_url)
    host = (parsed.hostname or "").lower()

    checks = {
        "nebius_https_endpoint": parsed.scheme == "https" and "tokenfactory" in host and host.endswith(".nebius.com"),
        "nvidia_model_requested": model_id.lower().startswith("nvidia/"),
        "api_key_present": bool(env.get("NEBIUS_API_KEY", "").strip()),
        "single_live_call_authorized": env.get("ALLOW_LIVE_NEBIUS_TEST") == "YES",
        "promo_coverage_confirmed": env.get("NEBIUS_PROMO_COVERAGE_CONFIRMED") == "YES",
    }
    return {
        "ready_for_single_live_call": all(checks.values()),
        "base_url": base_url,
        "model_id": model_id,
        "checks": checks,
    }


def require_live_config(env=None):
    result = evaluate(env)
    failed = [name for name, passed in result["checks"].items() if not passed]
    if failed:
        raise RuntimeError("Blocked: Nebius live-call preflight failed: " + ", ".join(failed))
    return result


if __name__ == "__main__":
    result = evaluate()
    print("Nebius preflight:", "READY" if result["ready_for_single_live_call"] else "BLOCKED")
    print("Model:", result["model_id"])
    print("Endpoint:", result["base_url"])
    for name, passed in result["checks"].items():
        print(f"- {name}: {'ok' if passed else 'missing/invalid'}")
