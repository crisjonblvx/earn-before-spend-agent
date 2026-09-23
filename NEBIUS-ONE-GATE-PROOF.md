# Nebius x NVIDIA — one human proof gate

This runbook exists to reduce the remaining runtime-evidence work to one deliberate, bounded human-approved session.

It does **not** accept Devpost, Nebius, NVIDIA, or Tavily terms. It does not create credentials, enable billing, move money, submit the project, or claim prize eligibility. Starting capital remains $0 and the command is designed to use only an already-approved free or hard-capped credential path.

## Baseline Nebius/NVIDIA proof

After the applicable terms/account access have been approved by the entrant and an authorized free or hard-capped Token Factory key exists:

```bash
ALLOW_LIVE_NEBIUS=1 \
NEBIUS_API_KEY="..." \
python hackathon_conversion_probe.py
```

The command makes exactly one Nebius Token Factory / NVIDIA Nemotron runtime call through the existing feedback probe, records measured latency and sanitized runtime evidence, and writes a combined manifest to:

`.conversion-evidence/nebius-tavily.json`

## Baseline + $3,000 Tavily bonus proof

Only if Tavily terms/account access have also been approved and a free or hard-capped Tavily credential exists:

```bash
ALLOW_LIVE_NEBIUS=1 \
NEBIUS_API_KEY="..." \
ALLOW_LIVE_TAVILY=1 \
TAVILY_API_KEY="..." \
python hackathon_conversion_probe.py --with-tavily
```

Before making either provider call, the wrapper verifies **all requested gates and credentials are present**. If Tavily is requested but its gate/key is missing, the command exits before consuming the Nebius call.

The combined mode makes:

- one Nebius Token Factory + NVIDIA Nemotron call, using the existing `nebius_feedback_probe.py` path;
- one bounded Tavily Search call, using the existing `tavily_probe.py` path;
- zero contest submissions;
- zero payout actions;
- zero identity/tax/legal attestations.

Evidence remains local and gitignored through the existing `.nebius-evidence`, `.tavily-evidence`, and `.conversion-evidence` paths. Credentials are never written into the manifest.

## What the proof closes

A successful baseline pass supplies the real runtime observation needed to support the Nebius/NVIDIA eligibility story and finish the feedback section truthfully. A successful `--with-tavily` pass additionally supplies the runtime call required before the submission may truthfully claim the Best Use of Tavily bonus lane.

A successful call is **not** external earnings. Verified external earnings remain $0 until money actually clears outside the user's own accounts.
