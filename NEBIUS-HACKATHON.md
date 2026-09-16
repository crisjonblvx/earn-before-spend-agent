# Earn Before Spend — Nebius x NVIDIA Global AI Hackathon build note

## Target track

**Best Apps and Agents** is the strongest fit. Earn Before Spend is a bounded economic agent for creators, independent professionals, small businesses, and community organizations. It ranks legitimate zero-new-cash earning paths, preserves hard safety/economic blockers, and identifies the smallest next action that can move toward verified external cash.

## Significant update during the submission period

The original public prototype used a deterministic economic gate plus a Strands-based explanation layer for the AWS Agents for Humans hackathon. The Nebius build adds a new provider path in `nebius_reasoner.py` that:

1. runs every candidate through the existing deterministic zero-cash gate;
2. serializes only the resulting evaluations, including blockers and human-decision flags;
3. makes a runtime OpenAI-compatible chat-completions call to **Nebius Token Factory**;
4. uses **NVIDIA Nemotron 3 Super 120B** by default (`nvidia/nemotron-3-super-120b-a12b`);
5. constrains Nemotron to explain one conversion-first next action without overriding blockers or inventing earnings.

This is a functional architecture change, not a rebrand: the reasoning layer now has a dedicated Nebius/NVIDIA runtime route while the deterministic economic policy remains provider-independent.

## Run locally

The offline deterministic demo still costs nothing:

```bash
python demo.py
```

Run the Nebius/Nemotron path only after a human has configured approved hackathon/free credits and an API key:

```bash
export NEBIUS_API_KEY="..."
python nebius_reasoner.py
```

Optional overrides:

```bash
export NEBIUS_BASE_URL="https://api.tokenfactory.nebius.com/v1"
export NEBIUS_MODEL="nvidia/nemotron-3-super-120b-a12b"
```

No API key is committed to this repository. The live path fails closed when `NEBIUS_API_KEY` is absent.

## Zero-cost verification

The Token Factory integration has an offline unit-test seam so request construction, model selection, endpoint targeting, deterministic-gate preservation, and missing-key behavior can be tested without consuming credits:

```bash
python -m unittest test_core.py test_nebius_reasoner.py -v
```

A real Token Factory call is still required before claiming the project satisfies the hackathon runtime requirement. Do not describe the Nebius integration as live-tested until that call succeeds against an approved account/credit allocation.

## Submission requirement map

- **Working project:** existing deterministic engine + Nebius Nemotron reasoning adapter.
- **Nebius runtime:** `POST /v1/chat/completions` through Token Factory.
- **NVIDIA open model:** Nemotron 3 Super 120B by default.
- **Public repository:** this repository is already public and MIT licensed.
- **README/setup:** existing README plus this build note; merge the Nebius run instructions into README before final submission.
- **Demo URL:** still required before submission.
- **Demo video:** still required; must be public on YouTube and 3 minutes or shorter.
- **Feedback:** still required in the Devpost submission.
- **Pre-existing project disclosure:** use the significant-update explanation above.

## Conversion-first demo story

Show three earning opportunities entering the system. The deterministic gate blocks any item with new required cash, unclear rights/eligibility, unverifiable payout, or excessive owner labor. The surviving ranking is passed to Nemotron on Token Factory. Nemotron explains one next bounded action and identifies any exact human gate. The scoreboard remains $0 earned until a trusted external payout clears.

## Human gate before a live provider test

Configure an approved Nebius Token Factory API key/credit allocation. This branch intentionally does not create accounts, accept third-party terms, enable paid resources, or place credentials in code.
