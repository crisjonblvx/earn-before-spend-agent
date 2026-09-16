"""Nebius Token Factory / NVIDIA Nemotron reasoning adapter for Earn Before Spend.

The deterministic economic gate remains authoritative. Nemotron receives only
the gate's evaluations and is asked to explain the safest next action; it
cannot turn a blocked opportunity into an eligible one.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import asdict
from typing import Callable, Iterable

from core import Opportunity, rank

DEFAULT_BASE_URL = "https://api.tokenfactory.nebius.com/v1"
DEFAULT_MODEL = "nvidia/nemotron-3-super-120b-a12b"

SYSTEM_PROMPT = """You are the reasoning layer for Earn Before Spend.
The deterministic economic gate has already decided eligibility. Never
override blockers, never convert hypothetical value into earnings, and never
claim a payment happened unless the input explicitly says an external payout
cleared. Choose one bounded next action that reduces distance to verified cash.
If terms, identity, tax, legal commitments, publication, or spending are
required, identify that exact human gate and stop there."""


def ranked_snapshot(opportunities: Iterable[Opportunity]) -> list[dict]:
    """Return the deterministic ranking that Nemotron is allowed to explain."""
    return [asdict(item) for item in rank(list(opportunities))]


def build_request_payload(evaluations: list[dict], model: str = DEFAULT_MODEL) -> dict:
    """Create an OpenAI-compatible Token Factory chat-completions payload."""
    return {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    "Here is the deterministic ranking. Explain the best "
                    "conversion-first next action in <=180 words. Preserve all "
                    "blockers and human-decision gates exactly. Do not invent "
                    "earnings or new opportunities.\n\n"
                    + json.dumps(evaluations, indent=2)
                ),
            },
        ],
        "temperature": 0.2,
        "max_tokens": 350,
    }


def call_token_factory(
    evaluations: list[dict],
    *,
    api_key: str | None = None,
    base_url: str | None = None,
    model: str | None = None,
    timeout: int = 45,
    opener: Callable = urllib.request.urlopen,
) -> str:
    """Make the required runtime call to Nebius Token Factory."""
    key = api_key or os.environ.get("NEBIUS_API_KEY")
    if not key:
        raise RuntimeError("NEBIUS_API_KEY is required for the live Nemotron path.")

    root = (base_url or os.environ.get("NEBIUS_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
    chosen_model = model or os.environ.get("NEBIUS_MODEL") or DEFAULT_MODEL
    payload = build_request_payload(evaluations, chosen_model)

    request = urllib.request.Request(
        f"{root}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with opener(request, timeout=timeout) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Token Factory HTTP {exc.code}: {detail[:500]}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Token Factory connection failed: {exc.reason}") from exc

    try:
        return body["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError("Unexpected Token Factory response shape.") from exc


def reason_with_nemotron(opportunities: Iterable[Opportunity], **kwargs) -> dict:
    """Rank deterministically, then ask Nemotron to explain one next action."""
    evaluations = ranked_snapshot(opportunities)
    explanation = call_token_factory(evaluations, **kwargs)
    return {
        "provider": "Nebius Token Factory",
        "model": kwargs.get("model") or os.environ.get("NEBIUS_MODEL") or DEFAULT_MODEL,
        "ranking": evaluations,
        "nemotron_explanation": explanation,
    }


if __name__ == "__main__":
    from demo import sample_opportunities

    result = reason_with_nemotron(sample_opportunities())
    print(json.dumps(result, indent=2))
