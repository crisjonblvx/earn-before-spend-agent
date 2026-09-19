import json
import threading
import unittest
from urllib.request import Request, urlopen

from alexa_simulator.server import Handler, ThreadingHTTPServer


class AlexaSimulatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.base_url = f"http://127.0.0.1:{cls.server.server_address[1]}"
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def test_health_is_deterministic_and_local(self):
        with urlopen(f"{self.base_url}/health", timeout=2) as response:
            payload = json.loads(response.read())
        self.assertEqual(payload, {"ok": True, "mode": "deterministic"})

    def test_rank_endpoint_preserves_human_gate_and_zero_cash_scoreboard(self):
        payload = {
            "opportunities": [
                {
                    "title": "No-fee competition",
                    "pathway": "competition",
                    "payout_usd": 5000,
                    "new_cash_required_usd": 0,
                    "cj_minutes_required": 10,
                    "deadline_hours": 48,
                    "payout_probability": 0.1,
                    "legitimacy_score": 95,
                    "fit_score": 90,
                    "rights_clear": True,
                    "eligibility_clear": True,
                    "payout_verifiable": True,
                    "terms_require_human_acceptance": True,
                    "source_url": "https://example.com/competition"
                }
            ]
        }
        body = json.dumps(payload).encode()
        request = Request(
            f"{self.base_url}/api/rank",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=2) as response:
            result = json.loads(response.read())

        self.assertEqual(result["mode"], "deterministic_no_provider_call")
        self.assertTrue(result["top_candidate"]["eligible"])
        self.assertTrue(result["top_candidate"]["requires_human_decision"])
        self.assertEqual(
            result["scoreboard"],
            {
                "starting_capital_usd": 0,
                "new_cash_spent_usd": 0,
                "verified_earnings_usd": 0,
            },
        )


if __name__ == "__main__":
    unittest.main()
