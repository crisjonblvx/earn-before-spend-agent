"""Nebius Token Factory / NVIDIA Nemotron model configuration.

This module deliberately contains no automatic network call. A live call is made
only when the operator explicitly runs the demo with RUN_NEBIUS=1 and provides a
Nebius API key. The deterministic economic gate remains authoritative.
"""
from __future__ import annotations

import os
from dataclasses import dataclass

DEFAULT_NEBIUS_MODEL = "nvidia/nemotron-3-super-120b-a12b"
MAX_OUTPUT_TOKENS = 700
DEFAULT_OUTPUT_TOKENS = 500


@dataclass(frozen=True)
class NebiusConfig:
    api_key: str
    model_id: str = DEFAULT_NEBIUS_MODEL
    max_tokens: int = DEFAULT_OUTPUT_TOKENS
    temperature: float = 0.2

    @classmethod
    def from_env(cls) -> "NebiusConfig":
        api_key = os.environ.get("NEBIUS_API_KEY", "").strip()
        if not api_key:
            raise RuntimeError("NEBIUS_API_KEY is required; no paid-provider fallback is allowed.")
        model_id = os.environ.get("NEBIUS_MODEL_ID", DEFAULT_NEBIUS_MODEL).strip()
        if not model_id.lower().startswith("nvidia/"):
            raise RuntimeError("NEBIUS_MODEL_ID must select an NVIDIA open model for this hackathon build.")
        raw_tokens = os.environ.get("NEBIUS_MAX_TOKENS", str(DEFAULT_OUTPUT_TOKENS)).strip()
        try:
            max_tokens = int(raw_tokens)
        except ValueError as exc:
            raise RuntimeError("NEBIUS_MAX_TOKENS must be an integer.") from exc
        if not 1 <= max_tokens <= MAX_OUTPUT_TOKENS:
            raise RuntimeError(f"NEBIUS_MAX_TOKENS must be between 1 and {MAX_OUTPUT_TOKENS}.")
        return cls(api_key=api_key, model_id=model_id, max_tokens=max_tokens)

    @property
    def strands_model_id(self) -> str:
        return f"nebius/{self.model_id}"

    def public_summary(self) -> dict[str, object]:
        return {
            "provider": "Nebius Token Factory",
            "model": self.model_id,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "api_key_present": bool(self.api_key),
        }


def build_nebius_model(config: NebiusConfig | None = None):
    """Create the Strands LiteLLM model without making an inference call."""
    config = config or NebiusConfig.from_env()
    try:
        from strands.models.litellm import LiteLLMModel
    except ImportError as exc:
        raise RuntimeError(
            "Nebius mode needs the Strands LiteLLM extra. Install requirements.txt first."
        ) from exc
    return LiteLLMModel(
        client_args={"api_key": config.api_key},
        model_id=config.strands_model_id,
        params={"max_tokens": config.max_tokens, "temperature": config.temperature},
    )
