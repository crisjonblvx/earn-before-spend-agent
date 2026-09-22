# Nebius runtime proof: one human-authorized call

Status: preparation only. This does not join or submit the hackathon, accept terms, enable billing, create credentials, or claim earnings.

## Why this exists

The remaining Nebius gate is a real runtime call using NVIDIA Nemotron on Nebius Token Factory. The official hackathon also offers a Most Valuable Feedback bonus for eligible submissions that complete the feedback section. We should not require CJ to make separate provider calls just to collect evidence for those two requirements.

## One-call path

After an already-authorized zero-cost or hard-capped `NEBIUS_API_KEY` is configured, run:

```bash
NEBIUS_API_KEY="..." python nebius_feedback_probe.py
```

That command makes exactly one Nemotron completion and writes:

```text
.nebius-evidence/runtime-feedback.json
```

The artifact is gitignored and contains no API key. It captures:

- provider and model;
- endpoint host;
- UTC completion time;
- measured end-to-end completion latency;
- the deterministic qualified/blocked title sets used for the call;
- the model completion;
- a human constraint-review prompt;
- a product-improvement question suitable for turning the actual runtime experience into honest Devpost feedback;
- an explicit truth boundary saying the call is not earnings, payout, scale, contest acceptance, or prize eligibility.

## Final human review after the call

Before using the artifact in the submission, verify that the completion did not:

1. reverse deterministic qualification;
2. invent payout certainty;
3. call hypothetical prizes earned money;
4. propose new spending.

Then use the measured latency and the actual observed model behavior to finish the Most Valuable Feedback field. Do not infer or fabricate observations that the one call did not produce.

## Existing evidence path

`nebius_smoke.py` remains valid for the original sanitized runtime receipt. `nebius_feedback_probe.py` is the conversion-first path because it turns the same one-call human gate into both runtime proof and measured feedback evidence without adding a second provider call.
