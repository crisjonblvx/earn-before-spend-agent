from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from submission_readiness import LOCAL_REQUIREMENTS, audit


class SubmissionReadinessTests(unittest.TestCase):
    def make_root(self, *, feedback: bool = True, evidence: bool = False) -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        for relative in LOCAL_REQUIREMENTS.values():
            (root / relative).write_text("placeholder\n", encoding="utf-8")
        draft = "## What changed during the hackathon period\n"
        if feedback:
            draft += "\n## Tooling feedback draft\n"
        (root / "NEBIUS-DEVPOST.md").write_text(draft, encoding="utf-8")
        if evidence:
            evidence_dir = root / ".nebius-evidence"
            evidence_dir.mkdir()
            (evidence_dir / "live-evidence.json").write_text("{}", encoding="utf-8")
        return root

    def test_preflight_distinguishes_human_gates_from_missing_work(self) -> None:
        report = audit(self.make_root(), env={})
        self.assertTrue(report["automation_ready"])
        self.assertFalse(report["submission_ready"])
        self.assertEqual(report["counts"]["missing"], 0)
        self.assertEqual(report["counts"]["human_gate"], 4)

    def test_urls_and_live_evidence_close_three_human_gates(self) -> None:
        report = audit(
            self.make_root(evidence=True),
            env={
                "NEBIUS_DEMO_URL": "https://example.test/demo",
                "NEBIUS_VIDEO_URL": "https://youtube.com/watch?v=example",
            },
        )
        self.assertEqual(report["counts"]["missing"], 0)
        self.assertEqual(report["counts"]["human_gate"], 1)
        self.assertFalse(report["submission_ready"])

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
