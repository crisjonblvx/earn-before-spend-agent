# Earn Before Spend — Nebius x NVIDIA Global AI Hackathon execution packet

Status: BUILD-IN-PROGRESS, NOT SUBMITTED

Prepared: 2026-09-17

## Verified competition facts

- Submission deadline: October 30, 2026 at 10:00 AM PDT.
- Entry is free; no purchase or payment is required to enter.
- A qualifying project must run on Nebius Token Factory or Nebius AI Cloud and use at least one NVIDIA open source model.
- Submission requires a working demo/test-build URL, a public code repository with an open-source license and setup instructions, a public YouTube demo of three minutes or less, a project description, a selected track, and feedback on Nebius/NVIDIA tooling.
- Earn Before Spend's repository was created September 14, 2026, after the August 26 submission period opened, so it is a new project for this event rather than an older project requiring a significant-update justification.
- The repository is already public and MIT licensed.

Official rules: https://nebiusglobalaihackathon.devpost.com/rules
Official overview: https://nebiusglobalaihackathon.devpost.com/

## Selected track

**Best Apps and Agents Track**

Earn Before Spend is primarily a practical agent for creators, small businesses, and community organizations rather than a coding agent. It uses an LLM for interpretation/orchestration while a deterministic economic gate decides what is actually eligible under the zero-new-cash policy.

## Nebius / NVIDIA implementation

The hackathon branch adds an explicit Nebius Token Factory model route using the Strands Agents SDK's LiteLLM model adapter.

Default NVIDIA model:

`nvidia/nemotron-3-super-120b-a12b`

Strands model id:

`nebius/nvidia/nemotron-3-super-120b-a12b`

The model is used only after the deterministic opportunity gate is available as an agent tool. Nemotron can explain rankings and next actions; it cannot override blockers such as new cash requirements, unclear rights, unverifiable payout, excessive CJ fulfillment, or human-only terms acceptance.

### Cost containment

The provider path is deliberately opt-in:

- no Nebius request occurs in the default demo;
- `RUN_NEBIUS=1` must be set explicitly;
- `NEBIUS_API_KEY` must be present;
- there is no fallback to another paid provider;
- `NEBIUS_MAX_TOKENS` is hard-capped at 700;
- the demo performs exactly one agent invocation with no retry loop.

This keeps the zero-capital experiment honest. Free promotional credits may be used later if CJ explicitly activates them, but credits are not counted as earnings and this branch does not enable paid or uncapped infrastructure.

## Run locally

Deterministic, zero-network demo:

```bash
python demo.py
```

Tests:

```bash
python -m unittest test_core.py test_nebius.py -v
```

Nebius/Nemotron path, only after an approved API key/credit route exists:

```bash
python -m pip install -r requirements.txt
export NEBIUS_API_KEY="..."
export RUN_NEBIUS=1
python demo.py
```

Optional overrides:

```bash
export NEBIUS_MODEL_ID="nvidia/nemotron-3-super-120b-a12b"
export NEBIUS_MAX_TOKENS=500
```

## Devpost draft copy

### Project name

Earn Before Spend

### Tagline

A zero-capital agent that lets open models reason, but never lets them spend first.

### What it does

Earn Before Spend helps creators, independent professionals, small businesses, and community organizations decide what they can legitimately pursue when the starting constraint is zero dollars in new seed capital. It compares pathways such as bounties, competitions, services, licenses, digital products, affiliate commissions, and grants, then blocks candidates that require new cash, hide too much owner labor, have unclear rights or eligibility, or lack a verifiable payout path.

The key design decision is separation of powers. NVIDIA Nemotron on Nebius Token Factory can interpret the situation, call tools, compare qualified options, and explain the next bounded action. A deterministic Python gate remains authoritative over the economic rules, so the model cannot talk its way around a cash requirement or silently approve third-party terms.

### How Nebius and NVIDIA are used

The hackathon build connects the existing Strands agent to NVIDIA Nemotron 3 Super through Nebius Token Factory using the Strands LiteLLM adapter. The model receives tool access to deterministic qualification/ranking functions. This makes Token Factory the reasoning backend while preserving a local, auditable policy layer for the economic constraints.

The provider configuration is intentionally bounded: no automatic provider call, no paid fallback, one model invocation in the demo, and a hard output-token ceiling. That is not only a cost control; it is part of the product thesis. An agent designed to earn before spending should not begin by silently creating an unlimited inference bill.

### Why it matters

Most 'make money with AI' workflows start by buying tools, ads, data, or compute before they know whether the underlying idea can earn. Earn Before Spend reverses the order: qualify first, take the smallest credible action second, and count money only after trusted external payout verification and cost reconciliation.

### Built with

Python, Strands Agents SDK, Nebius Token Factory, NVIDIA Nemotron 3 Super, deterministic dataclass-based policy tools, and unittest.

## Demo-video plan

Keep the public YouTube video under three minutes. The strongest sequence is:

1. State the zero-capital problem and show the deterministic demo.
2. Show three candidate opportunities, including one that is blocked for requiring cash.
3. Run the same workflow with `RUN_NEBIUS=1` using Nemotron on Token Factory.
4. Show Nemotron calling the deterministic ranking tool rather than inventing eligibility.
5. Show the human gate for terms/identity/public commitment.
6. Close on the verified-money rule: prizes and hypothetical value remain $0 until external payout clears.

Do not claim a live Nebius inference run until one has actually been executed and captured.

## Current conversion blockers

The code-side Nebius adapter is prepared, but the submission is not yet test-ready until these external items exist:

- an approved `NEBIUS_API_KEY` using free/capped credits or another explicitly authorized no-new-cash route;
- one captured successful Nemotron inference through Token Factory;
- a stable working demo/test-build URL;
- a public YouTube demo;
- human acceptance of Devpost/Nebius competition terms and the final submission.

No terms have been accepted and no paid resource has been enabled by this branch.
