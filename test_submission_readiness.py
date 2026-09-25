from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from submission_readiness import LOCAL_REQUIREMENTS, audit


class SubmissionReadinessTests(unittest.TestCase):
    def make_root(self, *, feedback: bool = True, evidence: str | None = None) -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        for relative in LOCAL_REQUIREMENTS.values():
            (root / relative).write_text("placeholder\n", encoding="utf-8")
        draft = "## What changed during the hackathon period\n"
        if feedback:
            draft += "\n## Tooling feedback draft\n"
        (root / "NEBIUS-DEVPOST.md").write_text(draft, encoding="utf-8")

        payload = {
            "live_call_observed": True,
            "provider": "Nebius Token Factory",
            "model": "nvidia/nemotron-3-super-120b-a12b",
        }
        if evidence == "smoke":
            evidence_dir = root / ".nebius-evidence"
            evidence_dir.mkdir()
            (evidence_dir / "live-evidence.json").write_text(
                json.dumps(payload), encoding="utf-8"
            )
        elif evidence == "feedback":
            evidence_dir = root / ".nebius-evidence"
            evidence_dir.mkdir()
            (evidence_dir / "runtime-feedback.json").write_text(
                json.dumps(payload), encoding="utf-8"
            )
        elif evidence == "manifest":
            evidence_dir = root / ".conversion-evidence"
            evidence_dir.mkdir()
            (evidence_dir / "nebius-tavily.json").write_text(
                json.dumps({"nebius": payload}), encoding="utf-8"
            )

        return root

    def test_preflight_distinguishes_human_gates_from_missing_work(self) -> None:
        report = audit(self.make_root(), env={})
        self.assertTrue(report["automation_ready"])
        self.assertFalse(report["submission_ready"])
        self.assertEqual(report["counts"]["missing"], 0)
        self.assertEqual(report["counts"]["human_gate"], 4)

    def test_urls_and_smoke_evidence_close_three_human_gates(self) -> None:
        report = audit(
            self.make_root(evidence="smoke"),
            env={
                "NEBIUS_DEMO_URL": "https://example.test/demo",
                "NEBIUS_VIDEO_URL": "https://youtube.com/watch?v=example",
            },
        )
        self.assertEqual(report["counts"]["missing"], 0)
        self.assertEqual(report["counts"]["human_gate"], 1)
        self.assertFalse(report["submission_ready"])

    def test_preferred_feedback_probe_evidence_counts_as_live_proof(self) -> None:
        report = audit(self.make_root(evidence="feedback"), env={})
        evidence = next(
            item for item in report["items"] if item["name"] == "live_token_factory_evidence"
        )
        self.assertEqual(evidence["status"], "ready")
        self.assertEqual(evidence["detail"], ".nebius-evidence/runtime-feedback.json")
        self.assertEqual(report["counts"]["human_gate"], 3)

    def test_combined_conversion_manifest_counts_as_live_proof(self) -> None:
        report = audit(self.make_root(evidence="manifest"), env={})
        evidence = next(
            item for item in report["items"] if item["name"] == "live_token_factory_evidence"
        )
        self.assertEqual(evidence["status"], "ready")
        self.assertEqual(evidence["detail"], ".conversion-evidence/nebius-tavily.json")

    def test_empty_or_malformed_evidence_does_not_clear_gate(self) -> None:
        root = self.make_root()
        evidence_dir = root / ".nebius-evidence"
        evidence_dir.mkdir()
        (evidence_dir / "runtime-feedback.json").write_text("{}", encoding="utf-8")
        report = audit(root, env={})
        evidence = next(
            item for item in report["items"] if item["name"] == "live_token_factory_evidence"
        )
        self.assertEqual(evidence["status"], "human_gate")

    def test_missing_feedback_is_an_automation_blocker(self) -> None:
        report = audit(self.make_root(feedback=False), env={})
        self.assertFalse(report["automation_ready"])
        self.assertEqual(report["counts"]["missing"], 1)

    def test_missing_local_file_is_an_automation_blocker(self) -> None:
        root = self.make_root()
        (root / "judge_demo.py").unlink()
        report = audit(root, env={})
        self.assertFalse(report["automation_ready"])
        self.assertEqual(report["counts"]["missing"], 1)


if __name__ == "__main__":
    unittest.main()
