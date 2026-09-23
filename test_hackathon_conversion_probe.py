"""Offline tests for the combined hackathon conversion proof command."""
from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import hackathon_conversion_probe


class HackathonConversionProbeTests(unittest.TestCase):
    def test_missing_nebius_gate_fails_before_any_provider_call(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            with patch.object(hackathon_conversion_probe.nebius_feedback_probe, "build_runtime_feedback") as neb:
                with patch.object(hackathon_conversion_probe.tavily_probe, "build_probe") as tav:
                    with self.assertRaisesRegex(RuntimeError, "ALLOW_LIVE_NEBIUS"):
                        hackathon_conversion_probe.run_conversion_probe(include_tavily=True)
                    neb.assert_not_called()
                    tav.assert_not_called()

    def test_missing_tavily_key_fails_before_nebius_call(self) -> None:
        env = {
            "ALLOW_LIVE_NEBIUS": "1",
            "NEBIUS_API_KEY": "approved-nebius-key",
            "ALLOW_LIVE_TAVILY": "1",
        }
        with patch.dict(os.environ, env, clear=True):
            with patch.object(hackathon_conversion_probe.nebius_feedback_probe, "build_runtime_feedback") as neb:
                with self.assertRaisesRegex(RuntimeError, "TAVILY_API_KEY"):
                    hackathon_conversion_probe.run_conversion_probe(include_tavily=True)
                neb.assert_not_called()

    def test_nebius_only_calls_once_and_writes_secret_free_manifest(self) -> None:
        secret = "never-write-nebius-secret"
        neb = {
            "live_call_observed": True,
            "provider": "Nebius Token Factory",
            "model": "nvidia/nemotron-3-super-120b-a12b",
            "elapsed_ms": 321.0,
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = Path(tmpdir) / "manifest.json"
            with patch.dict(
                os.environ,
                {
                    "ALLOW_LIVE_NEBIUS": "1",
                    "NEBIUS_API_KEY": secret,
                    "CONVERSION_EVIDENCE_OUT": str(manifest_path),
                },
                clear=True,
            ):
                with patch.object(
                    hackathon_conversion_probe.nebius_feedback_probe,
                    "build_runtime_feedback",
                    return_value=neb,
                ) as build_neb:
                    with patch.object(
                        hackathon_conversion_probe.nebius_feedback_probe,
                        "write_runtime_feedback",
                        return_value=Path(".nebius-evidence/runtime-feedback.json"),
                    ) as write_neb:
                        payload = hackathon_conversion_probe.run_conversion_probe(False)

            build_neb.assert_called_once_with()
            write_neb.assert_called_once_with(neb)
            self.assertFalse(payload["tavily"]["requested"])
            saved = manifest_path.read_text(encoding="utf-8")
            self.assertNotIn(secret, saved)
            self.assertEqual(json.loads(saved)["nebius"]["elapsed_ms"], 321.0)

    def test_combined_mode_calls_each_provider_once_after_all_gates_pass(self) -> None:
        neb = {
            "live_call_observed": True,
            "provider": "Nebius Token Factory",
            "model": "nvidia/nemotron-3-super-120b-a12b",
            "elapsed_ms": 456.0,
        }
        tav = {
            "live_call_observed": True,
            "provider": "Tavily Search API",
            "result_count": 3,
        }
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(
                os.environ,
                {
                    "ALLOW_LIVE_NEBIUS": "1",
                    "NEBIUS_API_KEY": "approved-nebius-key",
                    "ALLOW_LIVE_TAVILY": "1",
                    "TAVILY_API_KEY": "approved-tavily-key",
                    "CONVERSION_EVIDENCE_OUT": str(Path(tmpdir) / "manifest.json"),
                },
                clear=True,
            ):
                with patch.object(
                    hackathon_conversion_probe.nebius_feedback_probe,
                    "build_runtime_feedback",
                    return_value=neb,
                ) as build_neb:
                    with patch.object(
                        hackathon_conversion_probe.nebius_feedback_probe,
                        "write_runtime_feedback",
                        return_value=Path(".nebius-evidence/runtime-feedback.json"),
                    ):
                        with patch.object(
                            hackathon_conversion_probe.tavily_probe,
                            "build_probe",
                            return_value=tav,
                        ) as build_tav:
                            with patch.object(
                                hackathon_conversion_probe.tavily_probe,
                                "write_probe",
                                return_value=Path(".tavily-evidence/search.json"),
                            ):
                                payload = hackathon_conversion_probe.run_conversion_probe(True)

            build_neb.assert_called_once_with()
            build_tav.assert_called_once_with()
            self.assertTrue(payload["nebius"]["live_call_observed"])
            self.assertTrue(payload["tavily"]["live_call_observed"])
            self.assertEqual(payload["tavily"]["result_count"], 3)


if __name__ == "__main__":
    unittest.main()
