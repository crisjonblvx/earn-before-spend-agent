"""Turn one verified Nebius runtime receipt into paste-ready Devpost feedback.

This script performs no network calls and never reads or writes API keys. It only
accepts evidence produced by the existing human-authorized runtime probe. It is
fail-closed: malformed, placeholder, non-Nebius, or non-NVIDIA evidence is
rejected rather than turned into submission copy.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

DEFAULT_EVIDENCE = Path(".nebius-evidence/runtime-feedback.json")
DEFAULT_OUTPUT = Path(".nebius-evidence/devpost-runtime-feedback.md")
EXPECTED_PROVIDER = "Nebius Token Factory"


class EvidenceError(RuntimeError):
    """Raised when runtime evidence is not strong enough for submission copy."""


def _load_evidence(path: Path) -> dict[str, object]:
    if not path.is_file():
        raise EvidenceError(f"Runtime evidence not found: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EvidenceError("Runtime evidence is not valid JSON.") from exc
    if not isinstance(payload, dict):
        raise EvidenceError("Runtime evidence must be a JSON object.")
    return payload


def validate_evidence(payload: dict[str, object]) -> None:
    if payload.get("live_call_observed") is not True:
        raise EvidenceError("Evidence does not prove a live provider call.")
    if payload.get("provider") != EXPECTED_PROVIDER:
        raise EvidenceError("Evidence provider is not Nebius Token Factory.")

    model = str(payload.get("model", "")).strip()
    if not model.startswith("nvidia/"):
        raise EvidenceError("Evidence model is not an NVIDIA model.")

    endpoint_host = str(payload.get("endpoint_host", "")).strip().lower()
    if "tokenfactory" not in endpoint_host or not endpoint_host.endswith("nebius.com"):
        raise EvidenceError("Evidence endpoint is not a Nebius Token Factory host.")

    elapsed = payload.get("elapsed_ms")
    if not isinstance(elapsed, (int, float)) or isinstance(elapsed, bool) or elapsed <= 0:
        raise EvidenceError("Evidence is missing a positive measured elapsed_ms value.")

    completed = str(payload.get("completed_at_utc", "")).strip()
    if not completed:
        raise EvidenceError("Evidence is missing the UTC completion time.")

    completion = str(payload.get("completion", "")).strip()
    if not completion:
        raise EvidenceError("Evidence is missing the observed model completion.")


def build_feedback(payload: dict[str, object]) -> str:
    """Build truthful feedback using only measured evidence plus implementation facts."""
    validate_evidence(payload)

    model = str(payload["model"])
    endpoint_host = str(payload["endpoint_host"])
    elapsed_ms = payload["elapsed_ms"]
    completed_at = str(payload["completed_at_utc"])
    completion = str(payload["completion"]).strip()

    return f"""# Nebius x NVIDIA runtime feedback — paste-ready draft

## What I used
I used **Nebius Token Factory** to run **{model}** as the explanation layer for Earn Before Spend. Deterministic Python remains authoritative over opportunity eligibility and ranking; the model receives an already-qualified ranking and explains the best bounded next action and human approval gate.

## What worked well
The OpenAI-compatible Token Factory interface let me add an NVIDIA model without replacing the application's deterministic economic core. The provider boundary stayed easy to audit in source because the runtime path points explicitly at `{endpoint_host}` and the model identifier is explicit.

For the recorded qualifying call completed at **{completed_at}**, measured end-to-end completion time was **{elapsed_ms} ms**. That is a measurement from this one call only, not a latency SLA or benchmark claim.

## What could improve
For a zero-capital or safety-sensitive agent, I would like a hackathon-oriented quickstart that puts the regional Token Factory endpoint, current NVIDIA model IDs, server-side environment-key handling, per-request usage/cost visibility, and hard budget/cap guidance in one place. Those details are part of safe onboarding when a prototype is intentionally designed not to create uncapped spend.

## Zero-to-hello-world onboarding
The integration itself was lightweight once the endpoint and model ID were known: the existing Python application could use the chat-completions request shape while leaving its deterministic policy layer untouched. The larger onboarding task was verifying the cost and credential boundary strongly enough that local tests could remain offline and live inference could stay explicitly human-gated.

## Would I build with it again?
Yes, for bounded agents where model reasoning should stay separate from irreversible authority. Token Factory let this project use an NVIDIA model for explanation while ordinary code kept control over spending, eligibility, payout claims, and human approvals.

## Observed model output for final human constraint review
The text below is copied from the sanitized runtime evidence so it can be reviewed before submission. It is **not** automatically endorsed as a factual or financial claim.

> {completion.replace(chr(10), chr(10) + '> ')}

### Final review checklist
- [ ] The model did not reverse deterministic qualification.
- [ ] The model did not invent payout certainty.
- [ ] The model did not call a hypothetical prize or opportunity "earned money."
- [ ] The model did not propose new spending.
- [ ] The demo/video names Nebius Token Factory and the NVIDIA model out loud.

**Truth boundary:** This draft proves one recorded runtime call and its measured latency only. It does not prove earnings, payout, contest acceptance, or prize eligibility.
"""


def finalize(evidence_path: Path = DEFAULT_EVIDENCE, output_path: Path = DEFAULT_OUTPUT) -> Path:
    payload = _load_evidence(evidence_path)
    rendered = build_feedback(payload)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temp = output_path.with_name(f".{output_path.name}.tmp")
    temp.write_text(rendered, encoding="utf-8")
    temp.replace(output_path)
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, default=DEFAULT_EVIDENCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()

    try:
        payload = _load_evidence(args.evidence)
        validate_evidence(payload)
        if args.check_only:
            print("Nebius runtime evidence is valid for feedback finalization.")
            return 0
        destination = finalize(args.evidence, args.output)
    except EvidenceError as exc:
        print(f"BLOCK: {exc}")
        return 2

    print(f"Wrote paste-ready feedback: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
