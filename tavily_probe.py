"""One-call Tavily runtime proof for the Nebius hackathon bonus lane.

This is intentionally inert unless a human has configured BOTH TAVILY_API_KEY and
ALLOW_LIVE_TAVILY=1. It performs one bounded Search call and writes a sanitized,
gitignored evidence artifact. Search results remain unverified evidence candidates;
they are not counted as opportunities, payouts, or earnings.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from tavily_discovery import discover_opportunities

DEFAULT_OUT = Path(".tavily-evidence/search.json")
DEFAULT_QUERY = (
    "no-fee grants competitions bounties or paid opportunities for creators, "
    "software builders, or small businesses with verifiable payout"
)


def build_probe() -> dict[str, object]:
    results = discover_opportunities(DEFAULT_QUERY, max_results=3)
    return {
        "live_call_observed": True,
        "provider": "Tavily Search API",
        "completed_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "query": DEFAULT_QUERY,
        "result_count": len(results),
        "results": results,
        "truth_boundary": (
            "This proves one runtime Tavily search call only. Results are unverified evidence "
            "candidates and are not qualified opportunities, payouts, or earnings."
        ),
    }


def write_probe(payload: dict[str, object], output_path: str | os.PathLike[str] | None = None) -> Path:
    destination = Path(output_path or os.environ.get("TAVILY_EVIDENCE_OUT") or DEFAULT_OUT)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(f".{destination.name}.tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, destination)
    return destination


def main() -> None:
    payload = build_probe()
    write_probe(payload)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
