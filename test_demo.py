import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
from scenarios import report
from nebius_once import run_once


class DemoTests(unittest.TestCase):
    def test_paid_and_unverified_never_qualify(self):
        rows = report()["ranking"]
        self.assertEqual([r["title"] for r in rows if r["eligible"]], ["Owned automation pack"])
        self.assertTrue(rows[0]["requires_human_decision"])

    def test_editing_each_critical_requirement_blocks_owned_asset(self):
        for args in [{"cash": 1}, {"payout_verified": False}, {"owner_minutes": 31}]:
            with self.subTest(args=args):
                self.assertFalse(any(r["eligible"] for r in report(**args)["ranking"]))

    def test_missing_authorization_never_opens_network(self):
        with patch.dict(os.environ, {}, clear=True), patch("urllib.request.build_opener") as network:
            with self.assertRaises(RuntimeError):
                run_once()
            network.assert_not_called()

    def test_failed_call_is_not_retried_and_second_run_is_blocked(self):
        env = {"ALLOW_LIVE_NEBIUS_TEST": "YES", "NEBIUS_PROMO_COVERAGE_CONFIRMED": "YES", "NEBIUS_API_KEY": "fake-test-key"}
        with tempfile.TemporaryDirectory() as folder, patch.dict(os.environ, env, clear=True), patch("urllib.request.build_opener") as network:
            network.return_value.open.side_effect = TimeoutError("fake-test-key")
            result = run_once(Path(folder))
            self.assertEqual(result["status"], "failed")
            with self.assertRaises(RuntimeError):
                run_once(Path(folder))
            self.assertEqual(network.return_value.open.call_count, 1)
            self.assertNotIn("fake-test-key", (Path(folder) / "nebius-run.json").read_text())

    def test_success_records_real_response_without_key(self):
        env = {"ALLOW_LIVE_NEBIUS_TEST": "YES", "NEBIUS_PROMO_COVERAGE_CONFIRMED": "YES", "NEBIUS_API_KEY": "fake-test-key"}
        with tempfile.TemporaryDirectory() as folder, patch.dict(os.environ, env, clear=True), patch("urllib.request.build_opener") as network:
            response = network.return_value.open.return_value.__enter__.return_value
            response.read.return_value = json.dumps({"choices": [{"message": {"content": "Prepare the pack; human approval is required."}, "finish_reason": "stop"}], "usage": {"total_tokens": 99}, "model": "test"}).encode()
            result = run_once(Path(folder))
            self.assertEqual(result["status"], "completed")
            self.assertEqual(result["usage"]["total_tokens"], 99)
            request = network.return_value.open.call_args.args[0]
            self.assertEqual(json.loads(request.data)["max_tokens"], 350)
            self.assertEqual(network.return_value.open.call_count, 1)


if __name__ == "__main__":
    unittest.main()
