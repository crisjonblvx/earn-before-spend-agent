"""Offline tests for the one-call Nebius runtime feedback probe."""
from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import nebius_feedback_probe


class NebiusFeedbackProbeTests(unittest.TestCase):
    def test_missing_key_fails_before_provider_call(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            with patch.object(nebius_feedback_probe, "explain_ranking") as explain:
                with self.assertRaisesRegex(RuntimeError, "NEBIUS_API_KEY"):
                    nebius_feedback_probe.build_runtime_feedback()
                explain.assert_not_called()

    def test_one_call_captures_measured_feedback_without_secret(self) -> None:
        secret = "do-not-write-this-key"
        completion = "Use the top qualified path and keep the human terms gate."

        with patch.dict(os.environ, {"NEBIUS_API_KEY": secret}, clear=True):
            with patch.object(
                nebius_feedback_probe,
                "explain_ranking",
                return_value=completion,
            ) as explain:
                with patch.object(
                    nebius_feedback_probe.time,
                    "perf_counter",
                    side_effect=[10.0, 10.842],
                ):
                    feedback = nebius_feedback_probe.build_runtime_feedback()

        self.assertTrue(feedback["live_call_observed"])
        self.assertEqual(feedback["provider"], "Nebius Token Factory")
        self.assertEqual(feedback["model"], "nvidia/nemotron-3-super-120b-a12b")
        self.assertEqual(feedback["elapsed_ms"], 842.0)
        self.assertEqual(feedback["completion"], completion)
        self.assertIn("842.0 ms", feedback["feedback_prompts"]["latency_observation"])
        self.assertNotIn(secret, json.dumps(feedback))
        explain.assert_called_once()

    def test_feedback_is_written_atomically(self) -> None:
        feedback = {
            "live_call_observed": True,
            "elapsed_ms": 123.4,
            "truth_boundary": "one call only",
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "proof" / "feedback.json"
            written = nebius_feedback_probe.write_runtime_feedback(feedback, destination)
            self.assertEqual(written, destination)
            self.assertEqual(
                json.loads(destination.read_text(encoding="utf-8")),
                feedback,
            )
            self.assertFalse(
                destination.with_name(f".{destination.name}.tmp").exists()
            )


if __name__ == "__main__":
    unittest.main()
