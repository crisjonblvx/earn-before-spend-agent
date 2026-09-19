"""One-command, judge-safe live evidence capture for Nebius Token Factory.

This script performs exactly one NVIDIA Nemotron completion using an already-
approved ``NEBIUS_API_KEY``. It prints and persists only sanitized evidence for
later demo/submission packaging. It never provisions resources, accepts terms,
submits an entry, moves money, or writes the API key.
"""
from __future__ import annotations

import hashlib
import json
import os
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlparse

from core import rank
from demo import sample_opportunities
from nebius_reasoner import DEFAULT_BASE_URL, DEFAULT_MODEL, explain_ranked_evaluations

DEFAULT_EVIDENCE_PATH = Path(".nebius-evidence/live-evidence.json")


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def build_live_evidence(
    *,
    api_key: str | None = None,
    reasoner: Callable[..., str] = explain_ranked_evaluations,
) -> dict[str, Any]:
    """Run one live completion and return a sanitized evidence payload."""
    key = api_key or os.environ.get("NEBIUS_API_KEY")
    if not key:
        raise RuntimeError("NEBIUS_API_KEY is required for live Nebius evidence")

    deterministic = [asdict(item) for item in rank(sample_opportunities())]
    deterministic_json = json.dumps(
        deterministic,
        sort_keys=True,
        separators=(",", ":"),
    )

    completion = reasoner(deterministic, api_key=key)
    selected_model = os.environ.get("NEBIUS_MODEL", DEFAULT_MODEL)
    root = os.environ.get("NEBIUS_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
    completed_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    return {
        "live_call_observed": True,
        "completed_at_utc": completed_at,
        "provider": "Nebius Token Factory",
        "model": selected_model,
        "endpoint_host": urlparse(root).netloc,
        "deterministic_context_sha256": _sha256_text(deterministic_json),
        "completion_sha256": _sha256_text(completion),
        "completion": completion,
        "truth_boundary": (
            "This proves one successful Nebius/NVIDIA model call only. It is not "
            "evidence of earnings, payout, contest acceptance, or deployment scale."
        ),
    }


def write_live_evidence(
    evidence: dict[str, Any],
    output_path: str | os.PathLike[str] | None = None,
) -> Path:
    """Persist sanitized evidence atomically without writing credentials."""
    destination = Path(
        output_path
        or os.environ.get("NEBIUS_EVIDENCE_OUT")
        or DEFAULT_EVIDENCE_PATH
    )
    destination.parent.mkdir(parents=True, exist_ok=True)

    payload = f"{json.dumps(evidence, indent=2, sort_keys=True)}\n"
    temporary = destination.with_name(f".{destination.name}.tmp")
    temporary.write_text(payload, encoding="utf-8")
    os.replace(temporary, destination)
    return destination


def main() -> None:
    evidence = build_live_evidence()
    output = write_live_evidence(evidence)
    print(json.dumps(evidence, indent=2, sort_keys=True))
    print(f"Sanitized evidence written to {output}")


if __name__ == "__main__":
    main()
