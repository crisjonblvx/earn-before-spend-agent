"""Strands wrapper for the Earn Before Spend prototype.

The model may explain or compare; deterministic Python decides whether an
opportunity passes the zero-cash gate. This agent cannot spend, submit, sign,
or accept third-party terms.
"""
from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any

from strands import Agent, tool

from core import Opportunity, Pathway, evaluate, rank


@tool
def evaluate_opportunity(payload_json: str) -> str:
    """Evaluate one earning opportunity against strict zero-new-cash rules."""
    raw = json.loads(payload_json)
    raw["pathway"] = Pathway(raw["pathway"])
    result = evaluate(Opportunity(**raw))
    return json.dumps(asdict(result), indent=2)


@tool
def rank_opportunities(payload_json: str) -> str:
    """Rank a JSON array of earning opportunities after deterministic gating."""
    rows = json.loads(payload_json)
    opportunities = []
    for raw in rows[:3]:
        raw["pathway"] = Pathway(raw["pathway"])
        opportunities.append(Opportunity(**raw))
    return json.dumps([asdict(item) for item in rank(opportunities)], indent=2)


SYSTEM_PROMPT = """
You are Earn Before Spend, a bounded professional agent.

Goal: help a creator, small business, or community organization move from zero
new seed capital toward verified positive cash contribution.

Rules:
- Never call owner deposits, credits, test payments, loans, gifts, or hypothetical value earnings.
- Never recommend gambling, paid-entry speculation, securities/crypto trading, deceptive outreach, or unlicensed resale.
- Never hide existing-resource or labor costs.
- Never sign terms, submit an entry, publish private code, move money, or spend money.
- Use the deterministic tools for qualification and ranking. Do not override their blockers.
- Surface third-party terms, identity, payout, or legal commitments as a human decision.
- Prefer the smallest credible path to verified cash, but preserve expiring options when the downside is zero.
- State uncertainty. A competition prize is possible money, not earned money.
""".strip()


def build_agent(model: Any | None = None) -> Agent:
    kwargs: dict[str, Any] = {
        "system_prompt": SYSTEM_PROMPT,
        "tools": [evaluate_opportunity, rank_opportunities],
    }
    if model is not None:
        kwargs["model"] = model
    return Agent(**kwargs)


def run_demo(opportunities: list[dict], model: Any | None = None) -> str:
    agent = build_agent(model=model)
    payload = json.dumps(opportunities)
    return str(agent(
        "Rank these three opportunities using the deterministic tool. Explain the best next action, "
        "what requires human approval, and why the runner-up remains valuable. Opportunities: " + payload
    ))
