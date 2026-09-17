"""Nebius Token Factory adapter for Earn Before Spend.

This module keeps the project's deterministic economic gate authoritative while
routing the explanation/orchestration layer through an NVIDIA Nemotron model on
Nebius Token Factory. It does not submit entries, spend money, or accept terms.
"""
from __future__ import annotations

import json
import os
from dataclasses import asdict
from typing import Any

from core import Opportunity, rank

NEBIUS_BASE_URL = os.environ.get(
    "NEBIUS_BASE_URL",
    "https://api.tokenfactory.us-central1.nebius.com/v1/",
)
NEBIUS_MODEL = os.environ.get(
    "NEBIUS_MODEL",
    "nvidia/nemotron-3-super-120b-a12b",
)

SYSTEM_PROMPT = """
You are the reasoning layer for Earn Before Spend, a bounded zero-capital
opportunity agent. The deterministic Python ranking supplied to you is the
authoritative economic gate.

Rules:
- Never reverse an ineligible decision from the deterministic gate.
- Never describe a prize, credit, owner deposit, test payment, loan, gift, or
  hypothetical value as earned money.
- Never recommend gambling, paid-entry speculation, securities/crypto trading,
  deceptive outreach, or unlicensed resale.
- Never sign terms, submit an entry, publish private code, move money, connect a
  payout account, or spend money.
- Surface identity, legal, payout, terms, and public-commitment decisions as a
  human gate.
- Prefer one bounded action that most reduces distance to verified cash.
- Be explicit about uncertainty and hidden labor.
""".strip()


def deterministic_context(opportunities: list[Opportunity]) -> list[dict[str, Any]]:
    """Return the immutable gate/ranking evidence sent to the model."""
    return [asdict(item) for item in rank(opportunities)]


def build_user_prompt(opportunities: list[Opportunity]) -> str:
    """Create a grounded prompt without asking the model to redo qualification."""
    context = deterministic_context(opportunities)
    return (
        "Use the authoritative deterministic evaluation below. Pick the single "
        "highest-value bounded next action that can be completed without new cash "
        "or prohibited commitments. If a human gate is the only remaining step, "
        "state exactly one gate. Do not invent payout evidence.\n\n"
        + json.dumps(context, indent=2)
    )


def _completion_text(response: Any) -> str:
    choices = getattr(response, "choices", None)
    if not choices:
        raise RuntimeError("Nebius returned no completion choices")
    message = getattr(choices[0], "message", None)
    content = getattr(message, "content", None)
    if not content:
        raise RuntimeError("Nebius returned an empty completion")
    return str(content)


def run_nebius(opportunities: list[Opportunity], client: Any | None = None) -> str:
    """Run the bounded reasoning layer on NVIDIA Nemotron via Token Factory.

    Pass a compatible client in tests. In production/demo mode the API key must
    already exist in NEBIUS_API_KEY; this function never provisions resources.
    """
    if client is None:
        api_key = os.environ.get("NEBIUS_API_KEY")
        if not api_key:
            raise RuntimeError("NEBIUS_API_KEY is required for a live Nebius run")
        from openai import OpenAI

        client = OpenAI(base_url=NEBIUS_BASE_URL, api_key=api_key)

    response = client.chat.completions.create(
        model=NEBIUS_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(opportunities)},
        ],
        temperature=0.2,
    )
    return _completion_text(response)
