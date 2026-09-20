"""One-command, judge-safe live evidence for Nebius Token Factory.

This script performs exactly one intentional Nemotron completion using an
already-authorized NEBIUS_API_KEY, prints a sanitized evidence record, and
persists the same safe record locally for later demo/submission packaging. It
never prints or writes the API key, provisions resources, accepts terms,
submits an entry, or moves money.
"""
from __future__ import annotations

import hashlib
import json
import os
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from core import rank
from demo import sample_opportunities
from nebius_model import TokenFactoryConfig, explain_ranking

DEFAULT_EVIDENCE_PATH = Path(".nebius-evidence/live-evidence.json")


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def build_live_evidence() -> dict[str, object]:
    """Run one live completion and return a sanitized evidence payload."""
    config = TokenFactoryConfig.from_env()
    deterministic = [asdict(item) for item in rank(sample_opportunities())]
    deterministic_json = json.dumps(
        deterministic,
        default=str,
        sort_keys=True,
        separators=(",", ":"),
    )

    completion = explain_ranking(deterministic, config=config)
    completed_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    return {
        "live_call_observed": True,
        "completed_at_utc": completed_at,
        "provider": "Nebius Token Factory",
        "model": config.model,
        "endpoint_host": urlparse(config.base_url).netloc,
        "deterministic_context_sha256": _sha256_text(deterministic_json),
        "completion_sha256": _sha256_text(completion),
        "completion": completion,
        "truth_boundary": (
            "This proves one successful model call only. It is not evidence of "
            "earnings, payout, deployment scale, or contest acceptance."
        ),
    }


def write_live_evidence(
    evidence: dict[str, object],
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
    write_live_evidence(evidence)
    print(json.dumps(evidence, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
