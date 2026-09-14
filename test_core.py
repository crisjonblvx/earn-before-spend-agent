import unittest

from core import Opportunity, Pathway, evaluate, rank


def opportunity(**changes):
    base = dict(
        title="Test",
        pathway=Pathway.BOUNTY,
        payout_usd=100.0,
        new_cash_required_usd=0.0,
        cj_minutes_required=0,
        deadline_hours=48,
        payout_probability=0.8,
        legitimacy_score=90,
        fit_score=90,
        rights_clear=True,
        eligibility_clear=True,
        payout_verifiable=True,
        terms_require_human_acceptance=False,
        source_url="https://example.com/opportunity",
    )
    base.update(changes)
    return Opportunity(**base)


class EarnBeforeSpendTests(unittest.TestCase):
    def test_new_cash_blocks_candidate(self):
        result = evaluate(opportunity(new_cash_required_usd=0.01))
        self.assertFalse(result.eligible)
        self.assertIn("requires_new_cash", result.blockers)

    def test_hidden_cj_job_blocks_candidate(self):
        result = evaluate(opportunity(cj_minutes_required=31))
        self.assertFalse(result.eligible)
        self.assertIn("too_much_cj_fulfillment", result.blockers)

    def test_missing_rights_or_payment_proof_blocks(self):
        for changes in (dict(rights_clear=False), dict(payout_verifiable=False)):
            with self.subTest(changes=changes):
                self.assertFalse(evaluate(opportunity(**changes)).eligible)

    def test_terms_never_self_approve(self):
        result = evaluate(opportunity(terms_require_human_acceptance=True))
        self.assertTrue(result.eligible)
        self.assertTrue(result.requires_human_decision)

    def test_urgent_option_can_outrank_slightly_higher_expected_value(self):
        urgent = opportunity(title="Urgent", payout_usd=500, payout_probability=.15, deadline_hours=4)
        later = opportunity(title="Later", payout_usd=600, payout_probability=.2, deadline_hours=240)
        self.assertEqual(rank([later, urgent])[0].title, "Urgent")

    def test_blocked_candidate_never_wins(self):
        huge_but_paid = opportunity(title="Paid", payout_usd=1_000_000, new_cash_required_usd=1)
        clean = opportunity(title="Clean", payout_usd=50)
        self.assertEqual(rank([huge_but_paid, clean])[0].title, "Clean")


if __name__ == "__main__":
    unittest.main()
