"""Earn Before Spend demonstration.

Default execution is deterministic and makes no provider call. Set RUN_NEBIUS=1
only after a human has configured an authorized, capped Nebius Token Factory key.
RUN_STRANDS=1 remains available for the earlier Strands demonstration.
"""
from __future__ import annotations

import json
import os
from dataclasses import asdict

from core import Opportunity, Pathway, rank


def sample_opportunities() -> list[Opportunity]:
    # `payout_probability` is an explicit planning prior for prototype ranking,
    # not a factual prediction of contest odds or payment certainty.
    return [
        Opportunity(
            title="Expiring no-fee agent competition",
            pathway=Pathway.COMPETITION,
            payout_usd=10_000,
            new_cash_required_usd=0,
            cj_minutes_required=15,
            deadline_hours=12,
            payout_probability=0.02,
            legitimacy_score=95,
            fit_score=98,
            rights_clear=True,
            eligibility_clear=True,
            payout_verifiable=True,
            terms_require_human_acceptance=True,
            source_url="https://example.com/competition",
        ),
        Opportunity(
            title="Fixed-scope code bounty",
            pathway=Pathway.BOUNTY,
            payout_usd=100,
            new_cash_required_usd=0,
            cj_minutes_required=10,
            deadline_hours=168,
            payout_probability=0.70,
            legitimacy_score=82,
            fit_score=95,
            rights_clear=True,
            eligibility_clear=True,
            payout_verifiable=True,
            terms_require_human_acceptance=True,
            source_url="https://example.com/bounty",
        ),
        Opportunity(
            title="New-app competition",
            pathway=Pathway.COMPETITION,
            payout_usd=20_000,
            new_cash_required_usd=0,
            cj_minutes_required=20,
            deadline_hours=360,
            payout_probability=0.015,
            legitimacy_score=95,
            fit_score=90,
            rights_clear=True,
            eligibility_clear=True,
            payout_verifiable=True,
            terms_require_human_acceptance=True,
            source_url="https://example.com/app-challenge",
        ),
    ]


def main() -> None:
    opportunities = sample_opportunities()
    deterministic = [asdict(item) for item in rank(opportunities)]
    print(json.dumps({
        "mode": "deterministic_no_provider_call",
        "warning": "Planning priors are illustrative; they are not promised odds.",
        "ranking": deterministic,
    }, indent=2))

    if os.environ.get("RUN_NEBIUS") == "1":
        from nebius_model import explain_ranking

        print(json.dumps({
            "mode": "nebius_token_factory_nemotron",
            "model_output": explain_ranking(deterministic),
        }, indent=2))

    if os.environ.get("RUN_STRANDS") == "1":
        from agent import run_demo
        payload = []
        for item in opportunities:
            row = asdict(item)
            row["pathway"] = item.pathway.value
            payload.append(row)
        print(run_demo(payload))


if __name__ == "__main__":
    main()
