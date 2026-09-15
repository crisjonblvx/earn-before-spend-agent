"""One-run live smoke test for the Nebius adapter.

This script intentionally refuses to run unless the human operator explicitly
sets ALLOW_LIVE_NEBIUS_TEST=YES and provides NEBIUS_API_KEY in the environment.
It never creates credentials, enables billing, or changes cloud settings.
"""
from __future__ import annotations

import os


def require_gate() -> None:
    if os.environ.get("ALLOW_LIVE_NEBIUS_TEST", "NO").strip().upper() != "YES":
        raise SystemExit(
            "Live Nebius test blocked. Set ALLOW_LIVE_NEBIUS_TEST=YES only after "
            "human approval and confirmation that usage is covered by promotional "
            "credits or another explicitly authorized capped budget."
        )
    if not os.environ.get("NEBIUS_API_KEY", "").strip():
        raise SystemExit("Live Nebius test blocked: NEBIUS_API_KEY is missing.")


def main() -> None:
    require_gate()
    os.environ.setdefault("MODEL_PROVIDER", "nebius")
    os.environ.setdefault("NEBIUS_MODEL_ID", "nvidia/nemotron-3-super-120b-a12b")
    os.environ.setdefault("MODEL_MAX_TOKENS", "350")
    os.environ.setdefault("MODEL_TEMPERATURE", "0")

    from agent import run_demo

    opportunities = [
        {
            "title": "Reuse an owned automation pack on a no-upfront-fee marketplace",
            "pathway": "digital_product",
            "payout_usd": 19.0,
            "new_cash_required_usd": 0.0,
            "cj_minutes_required": 5,
            "deadline_hours": 720,
            "payout_probability": 0.15,
            "legitimacy_score": 95,
            "fit_score": 94,
            "rights_clear": True,
            "eligibility_clear": True,
            "payout_verifiable": True,
            "terms_require_human_acceptance": True,
            "source_url": "https://example.com/marketplace",
        },
        {
            "title": "Paid-entry speculative contest",
            "pathway": "competition",
            "payout_usd": 10000.0,
            "new_cash_required_usd": 50.0,
            "cj_minutes_required": 0,
            "deadline_hours": 24,
            "payout_probability": 0.01,
            "legitimacy_score": 80,
            "fit_score": 80,
            "rights_clear": True,
            "eligibility_clear": True,
            "payout_verifiable": True,
            "terms_require_human_acceptance": True,
            "source_url": "https://example.com/paid-contest",
        },
        {
            "title": "Unverified bounty with unclear payout",
            "pathway": "bounty",
            "payout_usd": 500.0,
            "new_cash_required_usd": 0.0,
            "cj_minutes_required": 0,
            "deadline_hours": 48,
            "payout_probability": 0.4,
            "legitimacy_score": 50,
            "fit_score": 90,
            "rights_clear": True,
            "eligibility_clear": True,
            "payout_verifiable": False,
            "terms_require_human_acceptance": False,
            "source_url": "https://example.com/unverified-bounty",
        },
    ]

    print(run_demo(opportunities))


if __name__ == "__main__":
    main()
