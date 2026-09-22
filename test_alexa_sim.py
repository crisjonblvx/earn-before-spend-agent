import unittest

from alexa_sim import ranked_snapshot, simulate_alexa_plus


class AlexaSimulationTests(unittest.TestCase):
    def test_paid_entry_is_blocked_even_with_large_payout(self):
        response = simulate_alexa_plus("Should I pay $99 to enter the $50,000 accelerator?")
        self.assertEqual(response["intent"], "evaluate_spend_request")
        self.assertFalse(response["candidate"]["eligible"])
        self.assertIn("requires_new_cash", response["candidate"]["blockers"])
        self.assertFalse(response["provider_call_made"])

    def test_best_move_is_qualified_and_preserves_human_terms_gate(self):
        response = simulate_alexa_plus("What is my best zero-capital earning move?")
        self.assertEqual(response["intent"], "recommend_next_move")
        self.assertTrue(response["candidate"]["eligible"])
        self.assertTrue(response["candidate"]["requires_human_decision"])
        self.assertIn("Human approval", response["human_gate"])
        self.assertFalse(response["provider_call_made"])

    def test_blocked_option_cannot_outrank_qualified_options(self):
        ranking = ranked_snapshot()
        self.assertTrue(ranking[0]["eligible"])
        blocked = [row for row in ranking if not row["eligible"]]
        self.assertEqual(len(blocked), 1)
        self.assertEqual(blocked[0]["score"], 0.0)

    def test_empty_utterance_returns_help_without_provider_call(self):
        response = simulate_alexa_plus("")
        self.assertEqual(response["intent"], "help")
        self.assertFalse(response["provider_call_made"])


if __name__ == "__main__":
    unittest.main()
