"""End-to-end Nebius Token Factory demo for Earn Before Spend."""
from __future__ import annotations

import json

from core import Opportunity, Pathway
from nebius_runtime import NebiusRuntimeError, explain_ranked_results


def demo_opportunities() -> list[Opportunity]:
    return [
        Opportunity(
            title="Verified no-fee bounty",
            pathway=Pathway.BOUNTY,
            payout_usd=500,
            new_cash_required_usd=0,
            cj_minutes_required=15,
            deadline_hours=48,
            payout_probability=0.55,
            legitimacy_score=92,
            fit_score=90,
            rights_clear=True,
            eligibility_clear=True,
            payout_verifiable=True,
            terms_require_human_acceptance=False,
            source_url="https://example.com/verified-bounty",
        ),
        Opportunity(
            title="Expiring competition",
            pathway=Pathway.COMPETITION,
            payout_usd=20_000,
            new_cash_required_usd=0,
            cj_minutes_required=20,
            deadline_hours=10,
            payout_probability=0.03,
            legitimacy_score=95,
            fit_score=88,
            rights_clear=True,
            eligibility_clear=True,
            payout_verifiable=True,
            terms_require_human_acceptance=True,
            source_url="https://example.com/competition",
        ),
        Opportunity(
            title="Paid-entry shortcut",
            pathway=Pathway.COMPETITION,
            payout_usd=100_000,
            new_cash_required_usd=49,
            cj_minutes_required=5,
            deadline_hours=24,
            payout_probability=0.20,
            legitimacy_score=90,
            fit_score=95,
            rights_clear=True,
            eligibility_clear=True,
            payout_verifiable=True,
            terms_require_human_acceptance=True,
            source_url="https://example.com/paid-entry",
        ),
    ]


def main() -> int:
    try:
        result = explain_ranked_results(demo_opportunities())
    except NebiusRuntimeError as exc:
        print(f"Nebius runtime error: {exc}")
        return 2

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
