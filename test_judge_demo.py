import unittest
from unittest.mock import patch

import judge_demo


class JudgeDemoTests(unittest.TestCase):
    def test_deterministic_snapshot_is_ranked_and_honest(self):
        payload = judge_demo.deterministic_snapshot()
        self.assertEqual(payload["mode"], "deterministic_authority")
        self.assertEqual(len(payload["ranking"]), 3)
        self.assertTrue(payload["ranking"][0]["eligible"])
        self.assertIn("not promised odds", payload["warning"])

    def test_live_nebius_is_double_gated(self):
        with patch.dict("os.environ", {"NEBIUS_API_KEY": "test-key"}, clear=True):
            self.assertFalse(judge_demo.live_nebius_enabled())
        with patch.dict("os.environ", {"ALLOW_LIVE_NEBIUS": "1"}, clear=True):
            self.assertFalse(judge_demo.live_nebius_enabled())
        with patch.dict(
            "os.environ",
            {"ALLOW_LIVE_NEBIUS": "1", "NEBIUS_API_KEY": "test-key"},
            clear=True,
        ):
            self.assertTrue(judge_demo.live_nebius_enabled())

    def test_disabled_explanation_makes_no_model_call(self):
        calls = []

        def explainer(ranking):
            calls.append(ranking)
            return "should not run"

        with patch.dict("os.environ", {}, clear=True):
            status, payload = judge_demo.explanation_snapshot(explainer=explainer)
        self.assertEqual(status, 503)
        self.assertFalse(payload["provider_call_made"])
        self.assertEqual(calls, [])

    def test_enabled_explanation_preserves_deterministic_authority(self):
        def explainer(ranking):
            self.assertTrue(ranking[0]["eligible"])
            return "Take the top qualified bounded action."

        with patch.dict(
            "os.environ",
            {"ALLOW_LIVE_NEBIUS": "1", "NEBIUS_API_KEY": "test-key"},
            clear=True,
        ):
            status, payload = judge_demo.explanation_snapshot(explainer=explainer)
        self.assertEqual(status, 200)
        self.assertTrue(payload["provider_call_made"])
        self.assertEqual(payload["economic_authority"], "deterministic ranking")
        self.assertEqual(payload["model"], "nvidia/nemotron-3-super-120b-a12b")

    def test_page_names_required_runtime_technology(self):
        self.assertIn("Nebius Token Factory", judge_demo.HTML)
        self.assertIn("Nemotron 3 Super", judge_demo.HTML)


if __name__ == "__main__":
    unittest.main()
