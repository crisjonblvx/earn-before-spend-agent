"""Single human-gated proof pass for the Nebius x NVIDIA submission.

The command stays inert unless live use is explicitly approved in environment
variables. It can run the required Nebius/Nemotron proof by itself, or perform
that call plus one Tavily runtime call for the conditional bonus lane.

No credential is written to evidence. No Devpost action, terms acceptance,
billing change, payout action, or earnings claim occurs here.
"""
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import nebius_feedback_probe
import tavily_probe

DEFAULT_MANIFEST = Path(".conversion-evidence/nebius-tavily.json")


def _require_live_env(include_tavily: bool) -> None:
    if os.environ.get("ALLOW_LIVE_NEBIUS") != "1":
        raise RuntimeError("Live Nebius proof is locked. Set ALLOW_LIVE_NEBIUS=1 only after human approval.")
    if not os.environ.get("NEBIUS_API_KEY", "").strip():
        raise RuntimeError("NEBIUS_API_KEY is required for the authorized live proof.")

    if include_tavily:
        if os.environ.get("ALLOW_LIVE_TAVILY") != "1":
            raise RuntimeError("Live Tavily proof is locked. Set ALLOW_LIVE_TAVILY=1 only after human approval.")
        if not os.environ.get("TAVILY_API_KEY", "").strip():
            raise RuntimeError("TAVILY_API_KEY is required when --with-tavily is selected.")


def _write_manifest(payload: dict[str, object], output_path: str | os.PathLike[str] | None = None) -> Path:
    destination = Path(output_path or os.environ.get("CONVERSION_EVIDENCE_OUT") or DEFAULT_MANIFEST)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(f".{destination.name}.tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(temporary, destination)
    return destination


def run_conversion_probe(include_tavily: bool = False) -> dict[str, object]:
    """Run the authorized evidence pass.

    Environment validation happens before any provider call so selecting Tavily
    cannot consume a Nebius call and then fail on a missing Tavily gate/key.
    """
    _require_live_env(include_tavily)

    nebius_feedback = nebius_feedback_probe.build_runtime_feedback()
    nebius_path = nebius_feedback_probe.write_runtime_feedback(nebius_feedback)

    tavily_payload: dict[str, object] | None = None
    tavily_path: Path | None = None
    if include_tavily:
        tavily_payload = tavily_probe.build_probe()
        tavily_path = tavily_probe.write_probe(tavily_payload)

    manifest = {
        "completed_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "nebius": {
            "live_call_observed": bool(nebius_feedback.get("live_call_observed")),
            "provider": nebius_feedback.get("provider"),
            "model": nebius_feedback.get("model"),
            "elapsed_ms": nebius_feedback.get("elapsed_ms"),
            "evidence_path": str(nebius_path),
        },
        "tavily": (
            {
                "requested": True,
                "live_call_observed": bool(tavily_payload and tavily_payload.get("live_call_observed")),
                "provider": tavily_payload.get("provider") if tavily_payload else None,
                "result_count": tavily_payload.get("result_count") if tavily_payload else None,
                "evidence_path": str(tavily_path) if tavily_path else None,
            }
            if include_tavily
            else {"requested": False, "live_call_observed": False}
        ),
        "truth_boundary": (
            "This manifest proves only the recorded runtime calls. It does not prove earnings, "
            "payout, contest acceptance, prize eligibility, or permission to spend money."
        ),
    }
    _write_manifest(manifest)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the final human-authorized Nebius proof pass.")
    parser.add_argument(
        "--with-tavily",
        action="store_true",
        help="Also make exactly one gated Tavily runtime call for the conditional bonus lane.",
    )
    args = parser.parse_args()
    payload = run_conversion_probe(include_tavily=args.with_tavily)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
