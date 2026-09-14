"""Deterministic guardrails for the Earn Before Spend hackathon prototype."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Pathway(str, Enum):
    BOUNTY = "bounty"
    COMPETITION = "competition"
    SERVICE = "service"
    DIGITAL_PRODUCT = "digital_product"
    LICENSE = "license"
    AFFILIATE = "affiliate"
    GRANT_OR_AWARD = "grant_or_award"


@dataclass(frozen=True)
class Opportunity:
    title: str
    pathway: Pathway
    payout_usd: float
    new_cash_required_usd: float
    cj_minutes_required: int
    deadline_hours: int
    payout_probability: float
    legitimacy_score: int
    fit_score: int
    rights_clear: bool
    eligibility_clear: bool
    payout_verifiable: bool
    terms_require_human_acceptance: bool
    source_url: str


@dataclass(frozen=True)
class Evaluation:
    title: str
    eligible: bool
    score: float
    blockers: tuple[str, ...]
    requires_human_decision: bool
    reason: str


def evaluate(opportunity: Opportunity) -> Evaluation:
    blockers: list[str] = []
    if opportunity.new_cash_required_usd > 0:
        blockers.append("requires_new_cash")
    if opportunity.cj_minutes_required > 30:
        blockers.append("too_much_cj_fulfillment")
    if not opportunity.rights_clear:
        blockers.append("rights_unclear")
    if not opportunity.eligibility_clear:
        blockers.append("eligibility_unclear")
    if not opportunity.payout_verifiable:
        blockers.append("payout_not_verifiable")
    if opportunity.legitimacy_score < 70:
        blockers.append("legitimacy_below_threshold")
    if not 0 <= opportunity.payout_probability <= 1:
        blockers.append("invalid_probability")

    eligible = not blockers
    urgency = 100 if opportunity.deadline_hours <= 12 else 70 if opportunity.deadline_hours <= 72 else 35
    expected_value = opportunity.payout_usd * opportunity.payout_probability
    score = (
        min(expected_value, 10_000) / 100
        + opportunity.legitimacy_score * 0.30
        + opportunity.fit_score * 0.30
        + urgency * 0.20
        - opportunity.cj_minutes_required * 0.25
    ) if eligible else 0.0

    if blockers:
        reason = "Blocked: " + ", ".join(blockers)
    elif opportunity.terms_require_human_acceptance:
        reason = "Qualified, but a human must approve the third-party terms before entry or submission."
    else:
        reason = "Qualified for the next bounded action."

    return Evaluation(
        title=opportunity.title,
        eligible=eligible,
        score=round(score, 2),
        blockers=tuple(blockers),
        requires_human_decision=opportunity.terms_require_human_acceptance,
        reason=reason,
    )


def rank(opportunities: list[Opportunity]) -> list[Evaluation]:
    evaluations = [evaluate(item) for item in opportunities]
    return sorted(evaluations, key=lambda item: (item.eligible, item.score), reverse=True)
