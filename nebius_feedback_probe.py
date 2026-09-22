"""One-call runtime probe for Nebius hackathon feedback evidence.

This intentionally reuses the same single authorized Nemotron completion needed
for runtime proof, then records measured latency plus a few submission-safe facts.
It does not make a second provider call, expose credentials, accept terms, submit
anything, or claim possible prize money as earnings.
"""
from __future__ import annotations

import json
import os
import time
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from core import rank
from demo import sample_opportunities
from nebius_model import TokenFactoryConfig, explain_ranking

DEFAULT_FEEDBACK_PATH = Path(".nebius-evidence/runtime-feedback.json")


def build_runtime_feedback() -> dict[str, object]:
    """Run exactly one authorized live completion and capture measured feedback."""
    config = TokenFactoryConfig.from_env()
    deterministic = [asdict(item) for item in rank(sample_opportunities())]

    started = time.perf_counter()
    completion = explain_ranking(deterministic, config=config)
    elapsed_ms = round((time.perf_counter() - started) * 1000, 1)

    qualified = [item["title"] for item in deterministic if item["eligible"]]
    blocked = [item["title"] for item in deterministic if not item["eligible"]]

    return {
        "live_call_observed": True,
        "completed_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "provider": "Nebius Token Factory",
        "model": config.model,
        "endpoint_host": urlparse(config.base_url).netloc,
        "elapsed_ms": elapsed_ms,
        "qualified_titles": qualified,
        "blocked_titles": blocked,
        "completion": completion,
        "feedback_prompts": {
            "latency_observation": (
                f"The measured end-to-end completion time for this exact Nemotron call was "
                f"{elapsed_ms} ms."
            ),
            "constraint_review": (
                "Human review required: confirm the response did not reverse deterministic "
                "qualification, invent payout certainty, call hypothetical prizes earnings, "
                "or propose new spending."
            ),
            "product_improvement_question": (
                "What single Token Factory documentation or response-detail change would have "
                "made this bounded-agent integration faster or safer?"
            ),
        },
        "truth_boundary": (
            "This records one successful model call and measured latency only. It is not "
            "evidence of earnings, payout, scale, contest acceptance, or prize eligibility."
        ),
    }


def write_runtime_feedback(
    feedback: dict[str, object],
    output_path: str | os.PathLike[str] | None = None,
) -> Path:
    destination = Path(
        output_path
        or os.environ.get("NEBIUS_FEEDBACK_OUT")
        or DEFAULT_FEEDBACK_PATH
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(f".{destination.name}.tmp")
    temporary.write_text(
        json.dumps(feedback, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, destination)
    return destination


def main() -> None:
    feedback = build_runtime_feedback()
    write_runtime_feedback(feedback)
    print(json.dumps(feedback, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
