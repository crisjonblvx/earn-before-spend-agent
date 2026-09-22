"""Nebius Token Factory runtime adapter for Earn Before Spend.

The deterministic economic gate remains authoritative. NVIDIA Nemotron is used
only to explain the already-ranked results and identify the smallest bounded
next action. This keeps the hackathon runtime requirement meaningful without
letting the model bypass zero-capital blockers.
"""
from __future__ import annotations

import json
import os
from dataclasses import asdict
from typing import Any
from urllib import error, request

from core import Opportunity, rank

DEFAULT_BASE_URL = "https://api.tokenfactory.us-central1.nebius.com/v1"
DEFAULT_MODEL = "nvidia/Nemotron-3-Ultra-550b-a55b"


class NebiusRuntimeError(RuntimeError):
    """Raised when Token Factory is not configured or returns an invalid response."""


def _chat_completions_url(base_url: str) -> str:
    return base_url.rstrip("/") + "/chat/completions"


def explain_ranked_results(
    opportunities: list[Opportunity],
    *,
    api_key: str | None = None,
    base_url: str | None = None,
    model: str | None = None,
    timeout_seconds: int = 30,
) -> dict[str, Any]:
    """Rank opportunities deterministically, then ask Nemotron to explain them.

    Returns both the deterministic evaluations and the model explanation so a
    judge can see exactly which part is authoritative.
    """
    resolved_key = api_key or os.getenv("NEBIUS_API_KEY")
    if not resolved_key:
        raise NebiusRuntimeError("NEBIUS_API_KEY is required for the Token Factory runtime call")

    resolved_base = base_url or os.getenv("NEBIUS_BASE_URL", DEFAULT_BASE_URL)
    resolved_model = model or os.getenv("NEBIUS_MODEL", DEFAULT_MODEL)

    evaluations = rank(opportunities)
    evaluation_payload = [asdict(item) for item in evaluations]

    system_prompt = (
        "You are the explanation layer for Earn Before Spend. The JSON evaluations were produced "
        "by deterministic zero-capital rules and are authoritative. Never override blockers, never "
        "call hypothetical prizes earnings, and never recommend spending, accepting terms, moving "
        "money, publishing private code, or making identity/legal attestations. Explain the best "
        "qualified option and the smallest bounded next action. If the top qualified option requires "
        "human approval, say exactly what the human must approve."
    )
    user_prompt = "Explain these deterministic evaluations in under 180 words:\n" + json.dumps(
        evaluation_payload, indent=2
    )

    body = json.dumps(
        {
            "model": resolved_model,
            "temperature": 0.2,
            "max_tokens": 350,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }
    ).encode("utf-8")

    req = request.Request(
        _chat_completions_url(resolved_base),
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {resolved_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )

    try:
        with request.urlopen(req, timeout=timeout_seconds) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise NebiusRuntimeError(f"Token Factory HTTP {exc.code}: {detail}") from exc
    except (error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise NebiusRuntimeError(f"Token Factory request failed: {exc}") from exc

    try:
        explanation = payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise NebiusRuntimeError("Token Factory response did not contain choices[0].message.content") from exc

    return {
        "provider": "Nebius Token Factory",
        "model": resolved_model,
        "evaluations": evaluation_payload,
        "explanation": explanation,
    }
