from __future__ import annotations

import unittest

from nebius_submission_finalize import EvidenceError, build_feedback, validate_evidence


GOOD = {
    "live_call_observed": True,
    "completed_at_utc": "2026-10-01T20:00:00+00:00",
    "provider": "Nebius Token Factory",
    "model": "nvidia/nemotron-3-super-120b-a12b",
    "endpoint_host": "api.tokenfactory.us-central1.nebius.com",
    "elapsed_ms": 812.4,
    "completion": "Pursue the qualified no-cash option. Human approval is still required before accepting terms.",
}


class FinalizerTests(unittest.TestCase):
    def test_valid_evidence_produces_paste_ready_feedback(self) -> None:
        text = build_feedback(GOOD)
        self.assertIn("Nebius Token Factory", text)
        self.assertIn("nvidia/nemotron-3-super-120b-a12b", text)
        self.assertIn("812.4 ms", text)
        self.assertIn("Final review checklist", text)

    def test_nonlive_evidence_fails_closed(self) -> None:
        with self.assertRaises(EvidenceError):
            validate_evidence(dict(GOOD, live_call_observed=False))

    def test_non_nvidia_model_fails_closed(self) -> None:
        with self.assertRaises(EvidenceError):
            validate_evidence(dict(GOOD, model="other/model"))

    def test_non_nebius_host_fails_closed(self) -> None:
        with self.assertRaises(EvidenceError):
            validate_evidence(dict(GOOD, endpoint_host="example.com"))

    def test_missing_measured_latency_fails_closed(self) -> None:
        with self.assertRaises(EvidenceError):
            validate_evidence(dict(GOOD, elapsed_ms=0))


if __name__ == "__main__":
    unittest.main()
