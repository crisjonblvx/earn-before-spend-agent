"""Optional model provider configuration for Earn Before Spend.

The deterministic economic gate remains provider-independent. This module only
selects the LLM used by Strands when an explicitly configured provider is
requested.

No API key is stored in source. Nebius access requires the human-controlled
NEBIUS_API_KEY environment variable and should be run only with approved
promotional credits or another capped, authorized budget.
"""
from __future__ import annotations

import os


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

    # Imported lazily so the deterministic demo still works without the optional
    # OpenAI-compatible provider dependency installed.
    from strands.models.openai import OpenAIModel

    return OpenAIModel(
        client_args={
            "api_key": api_key,
            "base_url": os.environ.get(
                "NEBIUS_BASE_URL",
                "https://api.tokenfactory.us-central1.nebius.com/v1/",
            ),
        },
        model_id=os.environ.get(
            "NEBIUS_MODEL_ID",
            "nvidia/nemotron-3-super-120b-a12b",
        ),
        params={
            "max_tokens": int(os.environ.get("MODEL_MAX_TOKENS", "1200")),
            "temperature": float(os.environ.get("MODEL_TEMPERATURE", "0.2")),
        },
    )
