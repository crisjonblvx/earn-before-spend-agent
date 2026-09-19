import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from nebius_live_evidence import build_live_evidence, write_live_evidence


class NebiusLiveEvidenceTests(unittest.TestCase):
    def test_missing_key_fails_closed(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(RuntimeError):
                build_live_evidence()

    def test_one_call_builds_sanitized_evidence(self):
        calls = []

        def fake_reasoner(ranking, *, api_key):
            calls.append((ranking, api_key))
            return "Choose the bounded next action and preserve the human gate."

        with patch.dict(os.environ, {}, clear=True):
            evidence = build_live_evidence(
                api_key="secret-test-key",
                reasoner=fake_reasoner,
            )

        self.assertEqual(len(calls), 1)
        self.assertTrue(calls[0][0])
        self.assertEqual(calls[0][1], "secret-test-key")
        self.assertTrue(evidence["live_call_observed"])
        self.assertEqual(evidence["provider"], "Nebius Token Factory")
        self.assertIn("nemotron", evidence["model"])
        self.assertEqual(
            evidence["endpoint_host"],
            "api.tokenfactory.us-central1.nebius.com",
        )
        self.assertEqual(len(evidence["deterministic_context_sha256"]), 64)
        self.assertEqual(len(evidence["completion_sha256"]), 64)
        self.assertNotIn("secret-test-key", json.dumps(evidence))

    def test_write_evidence_persists_no_secret(self):
        evidence = {
            "live_call_observed": True,
            "provider": "Nebius Token Factory",
            "completion": "safe",
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            destination = Path(temp_dir) / "evidence.json"
            result = write_live_evidence(evidence, destination)
            payload = result.read_text(encoding="utf-8")

        self.assertEqual(result, destination)
        self.assertEqual(json.loads(payload), evidence)
        self.assertNotIn("NEBIUS_API_KEY", payload)


if __name__ == "__main__":
    unittest.main()
