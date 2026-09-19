"""Bounded Nebius Token Factory / NVIDIA Nemotron explanation layer.

The deterministic economic gate remains authoritative. This module receives
already-evaluated results and asks Nemotron only to explain the ranking and the
smallest safe next action. It never submits entries, accepts terms, spends
money, or changes eligibility decisions.
"""
from __future__ import annotations

import json
import os
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

DEFAULT_BASE_URL = "https://api.tokenfactory.us-central1.nebius.com/v1"
DEFAULT_MODEL = "nvidia/nemotron-3-super-120b-a12b"

SYSTEM_PROMPT = """You are the explanation layer for Earn Before Spend.
The JSON you receive was produced by deterministic economic guardrails and is
authoritative. Never change an eligible/blocked decision, invent earnings, or
imply that third-party terms have been accepted. Explain the ranking, name the
smallest bounded next action, and surface any human approval gate. Possible
prizes and test activity are not verified earnings."""


class TokenFactoryError(RuntimeError):
    """Raised when a bounded Token Factory inference call cannot be completed."""


def _extract_content(payload: dict[str, Any]) -> str:
    try:
        content = payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise TokenFactoryError("Token Factory returned an unexpected response shape") from exc
    if not isinstance(content, str) or not content.strip():
        raise TokenFactoryError("Token Factory returned an empty response")
    return content.strip()


def explain_ranked_evaluations(
    ranking: list[dict[str, Any]],
    *,
    api_key: str | None = None,
    model: str | None = None,
    base_url: str | None = None,
    opener: Callable[..., Any] = urlopen,
    timeout_seconds: int = 30,
) -> str:
    """Ask NVIDIA Nemotron on Nebius to explain deterministic ranking output.

    This is intentionally opt-in. No request is made unless a Nebius API key is
    supplied directly or through ``NEBIUS_API_KEY``.
    """
    key = api_key or os.environ.get("NEBIUS_API_KEY")
    if not key:
        raise TokenFactoryError("NEBIUS_API_KEY is required for a live Token Factory call")

    selected_model = model or os.environ.get("NEBIUS_MODEL") or DEFAULT_MODEL
    root = (base_url or os.environ.get("NEBIUS_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
    endpoint = f"{root}/chat/completions"

    body = {
        "model": selected_model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    "Explain this deterministic zero-capital ranking. Keep the answer concise, "
                    "preserve every blocker and human gate, and choose only one smallest next action.\n\n"
                    + json.dumps(ranking, indent=2, sort_keys=True)
                ),
            },
        ],
        "temperature": 0.2,
        "max_tokens": 450,
    }

    request = Request(
        endpoint,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with opener(request, timeout=timeout_seconds) as response:
            raw = response.read().decode("utf-8")
    except HTTPError as exc:
        raise TokenFactoryError(f"Token Factory HTTP error: {exc.code}") from exc
    except URLError as exc:
        raise TokenFactoryError("Token Factory network error") from exc

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise TokenFactoryError("Token Factory returned invalid JSON") from exc

    return _extract_content(payload)
