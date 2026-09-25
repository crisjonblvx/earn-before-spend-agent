"""Fail-closed readiness audit for the Nebius x NVIDIA submission.

This script separates automation-completable requirements from human-controlled
submission gates. It never joins a hackathon, accepts terms, provisions cloud
resources, or performs a provider call.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Mapping

LOCAL_REQUIREMENTS = {
    "open_source_license": "LICENSE",
    "readme_setup": "README.md",
    "token_factory_adapter": "nebius_model.py",
    "judge_demo": "judge_demo.py",
    "container_package": "Dockerfile",
    "submission_draft": "NEBIUS-DEVPOST.md",
}

NEBIUS_EVIDENCE_CANDIDATES = (
    ".nebius-evidence/live-evidence.json",
    ".nebius-evidence/runtime-feedback.json",
    ".conversion-evidence/nebius-tavily.json",
)


def _valid_nebius_evidence(root: Path) -> str | None:
    """Return the first trusted local evidence path that proves a live Nebius call."""
    for relative in NEBIUS_EVIDENCE_CANDIDATES:
        path = root / relative
        if not path.is_file():
            continue

        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue

        record = payload.get("nebius") if relative.startswith(".conversion-evidence/") else payload
        if not isinstance(record, dict):
            continue

        if (
            record.get("live_call_observed") is True
            and record.get("provider") == "Nebius Token Factory"
            and str(record.get("model", "")).startswith("nvidia/")
        ):
            return relative

    return None


def audit(root: Path = Path("."), env: Mapping[str, str] | None = None) -> dict:
    env = env or os.environ
    items: list[dict[str, str]] = []

    for name, relative in LOCAL_REQUIREMENTS.items():
        path = root / relative
        items.append(
            {
                "name": name,
                "status": "ready" if path.is_file() else "missing",
                "detail": relative,
            }
        )

    draft = root / "NEBIUS-DEVPOST.md"
    draft_text = draft.read_text(encoding="utf-8") if draft.is_file() else ""
    items.append(
        {
            "name": "significant_update_explanation",
            "status": "ready" if "## What changed during the hackathon period" in draft_text else "missing",
            "detail": "Required for a project that existed before the submission period.",
        }
    )
    items.append(
        {
            "name": "tooling_feedback_draft",
            "status": "ready" if "## Tooling feedback draft" in draft_text else "missing",
            "detail": "Required Devpost feedback field; runtime observations must remain truthful.",
        }
    )

    evidence_path = _valid_nebius_evidence(root)
    items.append(
        {
            "name": "live_token_factory_evidence",
            "status": "ready" if evidence_path else "human_gate",
            "detail": (
                evidence_path
                if evidence_path
                else "Requires one human-authorized capped/free Token Factory call with validated local evidence."
            ),
        }
    )

    for name, variable, detail in (
        ("working_demo_url", "NEBIUS_DEMO_URL", "Public judge-accessible demo/test URL."),
        ("public_youtube_demo", "NEBIUS_VIDEO_URL", "Public YouTube demo under three minutes."),
    ):
        value = env.get(variable, "").strip()
        items.append(
            {
                "name": name,
                "status": "ready" if value else "human_gate",
                "detail": value or detail,
            }
        )

    items.append(
        {
            "name": "devpost_join_and_submit",
            "status": "human_gate",
            "detail": "Joining/submitting accepts third-party rules and remains human-controlled.",
        }
    )

    counts = {status: sum(item["status"] == status for item in items) for status in ("ready", "human_gate", "missing")}
    return {
        "project": "Earn Before Spend",
        "target": "Nebius x NVIDIA Global AI Hackathon — Best Apps and Agents",
        "items": items,
        "counts": counts,
        "automation_ready": counts["missing"] == 0,
        "submission_ready": counts["missing"] == 0 and counts["human_gate"] == 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--final",
        action="store_true",
        help="Fail unless human-controlled gates are also complete.",
    )
    args = parser.parse_args()

    report = audit()
    print(json.dumps(report, indent=2, sort_keys=True))
    if report["counts"]["missing"]:
        return 1
    if args.final and report["counts"]["human_gate"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
