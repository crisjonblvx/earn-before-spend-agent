"""Offline tests for sanitized Nebius live-evidence capture."""
from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import nebius_smoke


class NebiusSmokeEvidenceTests(unittest.TestCase):
    def test_missing_api_key_fails_before_live_call(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            with patch.object(nebius_smoke, "explain_ranking") as explain:
                with self.assertRaisesRegex(RuntimeError, "NEBIUS_API_KEY"):
                    nebius_smoke.build_live_evidence()
                explain.assert_not_called()

    def test_live_evidence_is_sanitized_and_persisted(self) -> None:
        secret = "nebius-secret-that-must-never-be-written"
        completion = "Use the qualified no-fee path; human terms gate remains."

        with patch.dict(os.environ, {"NEBIUS_API_KEY": secret}, clear=True):
            with patch.object(
                nebius_smoke,
                "explain_ranking",
                return_value=completion,
            ) as explain:
                evidence = nebius_smoke.build_live_evidence()

        self.assertTrue(evidence["live_call_observed"])
        self.assertEqual(evidence["provider"], "Nebius Token Factory")
        self.assertEqual(evidence["completion"], completion)
        self.assertEqual(evidence["model"], "nvidia/nemotron-3-super-120b-a12b")
        self.assertEqual(
            evidence["endpoint_host"],
            "api.tokenfactory.us-central1.nebius.com",
        )
        self.assertNotIn(secret, json.dumps(evidence))
        explain.assert_called_once()

        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "evidence" / "live.json"
            written = nebius_smoke.write_live_evidence(evidence, destination)
            payload = written.read_text(encoding="utf-8")
            parsed = json.loads(payload)

            self.assertEqual(written, destination)
            self.assertEqual(
                parsed["completion_sha256"],
                evidence["completion_sha256"],
            )
            self.assertNotIn(secret, payload)
            self.assertFalse(
                destination.with_name(f".{destination.name}.tmp").exists()
            )

    def test_env_override_selects_output_path(self) -> None:
        evidence = {
            "live_call_observed": True,
            "provider": "Nebius Token Factory",
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "custom.json"
            with patch.dict(
                os.environ,
                {"NEBIUS_EVIDENCE_OUT": str(destination)},
                clear=True,
            ):
                written = nebius_smoke.write_live_evidence(evidence)
            self.assertEqual(written, destination)
            self.assertEqual(
                json.loads(destination.read_text(encoding="utf-8")),
                evidence,
            )


if __name__ == "__main__":
    unittest.main()
