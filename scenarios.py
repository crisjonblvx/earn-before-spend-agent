"""Illustrative inputs shared by the interactive demo and one-call evaluation."""
from dataclasses import asdict, replace
from core import Opportunity, Pathway, rank


def candidates(cash=0.0, payout_verified=True, owner_minutes=5):
    owned = Opportunity(
        title="Owned automation pack", pathway=Pathway.DIGITAL_PRODUCT,
        payout_usd=19, new_cash_required_usd=cash,
        cj_minutes_required=owner_minutes, deadline_hours=720,
        payout_probability=.15, legitimacy_score=95, fit_score=94,
        rights_clear=True, eligibility_clear=True,
        payout_verifiable=payout_verified, terms_require_human_acceptance=True,
        source_url="https://example.com/illustrative-product",
    )
    return [owned, replace(owned, title="Paid-entry contest", pathway=Pathway.COMPETITION,
        payout_usd=10000, new_cash_required_usd=50, payout_probability=.01),
        replace(owned, title="Unverified bounty", pathway=Pathway.BOUNTY,
        payout_usd=500, new_cash_required_usd=0, payout_verifiable=False,
        legitimacy_score=50)]


def report(cash=0.0, payout_verified=True, owner_minutes=5):
    return {"mode": "deterministic", "illustrative": True,
            "verified_earnings_usd": 0,
            "ranking": [asdict(x) for x in rank(candidates(cash, payout_verified, owner_minutes))]}
