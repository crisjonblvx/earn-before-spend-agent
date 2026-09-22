# Nebius x NVIDIA Global AI Hackathon submission draft

## Project

**Earn Before Spend**

## Track

**Best Apps and Agents**

## One-line pitch

A zero-capital decision agent that rejects unsafe earning paths deterministically, then uses NVIDIA Nemotron on Nebius Token Factory to explain the best legitimate next action without letting the model override the money guardrails.

## What it does

Earn Before Spend evaluates candidate earning opportunities for creators, independent professionals, small businesses, and community organizations. It blocks opportunities that require new cash before the earning event, hide too much owner labor, have unclear rights or eligibility, lack a verifiable payout path, or fall below a legitimacy threshold.

The ranking layer is deterministic Python. The NVIDIA model is deliberately not allowed to decide whether an opportunity is economically safe. Instead, the Nebius runtime sends the already-ranked evaluations to NVIDIA Nemotron and asks it to explain the best qualified option, surface any human approval gate, and identify the smallest bounded next action.

That separation is the product idea: use the model for judgment and explanation, but keep non-negotiable economic authority outside the model.

## Nebius + NVIDIA implementation

- Runtime provider: **Nebius Token Factory**
- Runtime API: OpenAI-compatible chat completions endpoint
- NVIDIA open-source model: **`nvidia/Nemotron-3-Ultra-550b-a55b`**
- Default regional endpoint: **`https://api.tokenfactory.us-central1.nebius.com/v1`**
- `nebius_runtime.py`: performs the Token Factory runtime call and returns both deterministic evaluations and the model explanation
- `nebius_demo.py`: end-to-end demo using three earning candidates
- `test_nebius_runtime.py`: verifies API-key gating, endpoint construction, model selection, response parsing, and that a paid-entry candidate remains blocked before Nemotron explains anything

## Why the model use is material

The NVIDIA model is not decorative. It receives the structured results of the economic gate and turns them into a human-readable decision that preserves urgency, explains tradeoffs, and identifies exactly where a person must step in for terms, identity, legal, publication, or spending decisions.

This is intentionally different from asking an LLM to "make money." The system decomposes the problem into deterministic qualification plus bounded model reasoning.

## How to run

The deterministic tests do not require a provider call:

```bash
python -m unittest test_core.py test_nebius_runtime.py -v
```

The live Nebius path requires a Token Factory API key:

```bash
export NEBIUS_API_KEY="..."
python nebius_demo.py
```

Optional overrides:

```bash
export NEBIUS_BASE_URL="https://api.tokenfactory.us-central1.nebius.com/v1"
export NEBIUS_MODEL="nvidia/Nemotron-3-Ultra-550b-a55b"
```

## Current validation status

- Original deterministic guardrail tests: passing
- Nebius adapter unit tests: passing with mocked network I/O
- Combined local suite: **9 tests passing**
- Live Token Factory inference: **not yet claimed**; requires a human-authorized Token Factory account/API key and must be validated before submission
- Public hosted demo: **not yet claimed**
- Public YouTube demo: **not yet claimed**

## Submission-period status

The repository's visible commit history begins on September 14, 2026, after the Nebius x NVIDIA submission period opened on August 26, 2026. The Nebius-specific runtime integration is being added during the submission period as a separate conversion branch.

## Demo video plan, under 3 minutes

1. Show one clean no-fee earning path, one urgent contest that requires human terms approval, and one high-payout paid-entry option.
2. Run the deterministic gate and show the paid-entry option blocked regardless of headline payout.
3. Run the same ranked results through NVIDIA Nemotron on Nebius Token Factory.
4. Show Nemotron explaining the best next action without overriding the blockers.
5. Close on the scoreboard: starting capital $0, new cash spent $0, hypothetical prizes do not count as earnings.

## Nebius/NVIDIA feedback field

**Do not finalize this field until a real runtime test has been completed.** Capture concrete observations from the actual Token Factory call, including setup friction, latency, model behavior, and whether the OpenAI-compatible endpoint made the integration simpler.

## Human-only gates before submission

- Join/accept the hackathon and Nebius/Devpost terms
- Obtain or authorize the Token Factory API key/credits
- Run and capture a real Token Factory inference with the NVIDIA model
- Make the working demo publicly accessible for judging through the end of the judging period
- Record and publish the under-three-minute YouTube demo
- Review final eligibility/IP/identity attestations and press Submit

No entry, terms acceptance, spend, payout setup, identity attestation, or submission is performed by this branch.
