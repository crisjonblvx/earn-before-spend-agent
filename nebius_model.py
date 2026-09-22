"""Nebius Token Factory adapter for Earn Before Spend.

This module deliberately gives the model explanation authority, not economic
authority. The deterministic ranking produced by core.py remains canonical.
No request is made unless NEBIUS_API_KEY is explicitly configured by a human.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Callable

DEFAULT_BASE_URL = "https://api.tokenfactory.us-central1.nebius.com/v1/"
DEFAULT_MODEL = "nvidia/nemotron-3-super-120b-a12b"


class TokenFactoryError(RuntimeError):
    """Raised when Token Factory configuration or response validation fails."""


@dataclass(frozen=True)
class TokenFactoryConfig:
    api_key: str
    base_url: str = DEFAULT_BASE_URL
    model: str = DEFAULT_MODEL
    timeout_seconds: float = 30.0

    @classmethod
    def from_env(cls) -> "TokenFactoryConfig":
        api_key = os.environ.get("NEBIUS_API_KEY", "").strip()
        if not api_key:
            raise TokenFactoryError(
                "NEBIUS_API_KEY is required for an intentional Token Factory runtime call."
            )
        base_url = os.environ.get("NEBIUS_BASE_URL", DEFAULT_BASE_URL).strip()
        model = os.environ.get("NEBIUS_MODEL", DEFAULT_MODEL).strip()
        if not base_url.endswith("/"):
            base_url += "/"
        return cls(api_key=api_key, base_url=base_url, model=model)


def explain_ranking(
    ranking: list[dict],
    *,
    config: TokenFactoryConfig | None = None,
    opener: Callable = urllib.request.urlopen,
) -> str:
    """Ask NVIDIA Nemotron on Nebius to explain a deterministic ranking.

    The prompt explicitly forbids the model from re-ranking blocked options or
    claiming that hypothetical payouts are earnings. The only model output used
    by the application is explanatory text.
    """
    config = config or TokenFactoryConfig.from_env()
    endpoint = config.base_url + "chat/completions"

    system = (
        "You are the explanation layer for Earn Before Spend. The JSON ranking "
        "was produced by deterministic economic guardrails and is authoritative. "
        "Do not reverse qualification decisions, invent payout certainty, call "
        "possible prizes earnings, or propose spending money. Explain the top "
        "qualified option, the bounded next action, the single most important "
        "human approval gate, and why the runner-up remains useful. Be concise."
    )
    payload = {
        "model": config.model,
        "temperature": 0.2,
        "messages": [
            {"role": "system", "content": system},
            {
                "role": "user",
                "content": "Explain this deterministic ranking:\n" + json.dumps(ranking, sort_keys=True),
            },
        ],
    }

    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )

    try:
        with opener(request, timeout=config.timeout_seconds) as response:
            raw = response.read().decode("utf-8")
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise TokenFactoryError(f"Token Factory request failed: {exc}") from exc

    try:
        body = json.loads(raw)
        content = body["choices"][0]["message"]["content"]
    except (json.JSONDecodeError, KeyError, IndexError, TypeError) as exc:
        raise TokenFactoryError("Token Factory returned an unexpected response shape.") from exc

    if not isinstance(content, str) or not content.strip():
        raise TokenFactoryError("Token Factory returned an empty explanation.")
    return content.strip()
