"""Optional model provider configuration for Earn Before Spend.

The deterministic economic gate remains provider-independent. This module only
selects the LLM used by Strands when an explicitly configured provider is
requested.

No API key is stored in source. Nebius access requires the human-controlled
NEBIUS_API_KEY environment variable and is restricted to Nebius Token Factory
HTTPS endpoints plus NVIDIA model IDs.
"""
from __future__ import annotations

import os
from urllib.parse import urlparse

DEFAULT_NEBIUS_BASE_URL = "https://api.tokenfactory.us-central1.nebius.com/v1/"
DEFAULT_NEBIUS_MODEL_ID = "nvidia/nemotron-3-super-120b-a12b"
DEFAULT_MAX_TOKENS = 1200
MAX_ALLOWED_TOKENS = 2000


def _validated_nebius_target(base_url: str, model_id: str) -> tuple[str, str]:
    """Validate provider identity before an API key is handed to an SDK."""
    base_url = base_url.strip()
    model_id = model_id.strip()
    parsed = urlparse(base_url)
    host = (parsed.hostname or "").lower()
    labels = host.split(".")

    valid_host = (
        len(labels) >= 5
        and labels[0] == "api"
        and labels[1] == "tokenfactory"
        and labels[-2:] == ["nebius", "com"]
    )
    valid_url = (
        parsed.scheme == "https"
        and valid_host
        and parsed.username is None
        and parsed.password is None
        and parsed.port in (None, 443)
        and parsed.path in ("/v1", "/v1/")
        and not parsed.params
        and not parsed.query
        and not parsed.fragment
    )
    if not valid_url:
        raise RuntimeError(
            "Blocked: NEBIUS_BASE_URL must be a Nebius Token Factory HTTPS /v1 endpoint"
        )
    if not model_id.lower().startswith("nvidia/"):
        raise RuntimeError("Blocked: NEBIUS_MODEL_ID must identify an NVIDIA model")

    normalized_base_url = base_url.rstrip("/") + "/"
    return normalized_base_url, model_id


def _bounded_max_tokens(raw_value: str) -> int:
    try:
        value = int(raw_value)
    except ValueError as exc:
        raise RuntimeError("MODEL_MAX_TOKENS must be an integer") from exc
    if not 1 <= value <= MAX_ALLOWED_TOKENS:
        raise RuntimeError(
            f"Blocked: MODEL_MAX_TOKENS must be between 1 and {MAX_ALLOWED_TOKENS}"
        )
    return value


def configured_model():
    """Return an explicitly configured Strands model, or None for SDK default.

    Supported provider:
      MODEL_PROVIDER=nebius
      NEBIUS_API_KEY=...
      NEBIUS_MODEL_ID=nvidia/nemotron-3-super-120b-a12b   # optional override
      NEBIUS_BASE_URL=https://api.tokenfactory.us-central1.nebius.com/v1/ # optional
    """
    provider = os.environ.get("MODEL_PROVIDER", "").strip().lower()
    if not provider:
        return None

    if provider != "nebius":
        raise ValueError(f"Unsupported MODEL_PROVIDER: {provider}")

    api_key = os.environ.get("NEBIUS_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("MODEL_PROVIDER=nebius requires NEBIUS_API_KEY")

    base_url, model_id = _validated_nebius_target(
        os.environ.get("NEBIUS_BASE_URL", DEFAULT_NEBIUS_BASE_URL),
        os.environ.get("NEBIUS_MODEL_ID", DEFAULT_NEBIUS_MODEL_ID),
    )
    max_tokens = _bounded_max_tokens(
        os.environ.get("MODEL_MAX_TOKENS", str(DEFAULT_MAX_TOKENS))
    )
    try:
        temperature = float(os.environ.get("MODEL_TEMPERATURE", "0.2"))
    except ValueError as exc:
        raise RuntimeError("MODEL_TEMPERATURE must be numeric") from exc
    if not 0 <= temperature <= 2:
        raise RuntimeError("Blocked: MODEL_TEMPERATURE must be between 0 and 2")

    # Imported lazily so the deterministic demo still works without the optional
    # OpenAI-compatible provider dependency installed.
    from strands.models.openai import OpenAIModel

    return OpenAIModel(
        client_args={
            "api_key": api_key,
            "base_url": base_url,
        },
        model_id=model_id,
        params={
            "max_tokens": max_tokens,
            "temperature": temperature,
        },
    )
