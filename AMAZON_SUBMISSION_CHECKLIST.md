# Amazon Build, Ship, Shape Submission Checklist

Verified against the live Devpost overview/rules on September 18, 2026.

## Deadline

- [ ] Submit by **October 23, 2026 at 12:00 PM PDT**.
- [ ] Do not accept hackathon terms or submit the entry without CJ's approval.

## Primary track

**Alexa+ — simulated Alexa+ experience**

The hackathon explicitly permits a simulated Alexa+ experience in a web app using an entrant's preferred agentic tools. The repository must include the simulation source code and the demo must clearly show it working.

Current implementation:

- [x] `alexa_simulator/index.html`
- [x] `alexa_simulator/server.py`
- [x] deterministic `/api/rank` endpoint
- [x] direct-run import-path fix
- [x] simulator smoke tests

Run locally:

```bash
python alexa_simulator/server.py
```

Then open:

```text
http://127.0.0.1:8765
```

## Mini challenge: AWS Builder

Official requirement: use an AWS service/tool such as Bedrock, AgentCore, Strands SDK, Kiro Crew, SageMaker, etc., and document the integration.

Current evidence:

- [x] `agent.py` imports and uses the Strands Agents SDK.
- [x] deterministic evaluation/ranking functions are exposed as Strands tools.
- [x] `DEVPOST.md` documents what Strands is used for and its authority boundary.
- [ ] Final demo should show or clearly explain the Strands layer if AWS Builder is selected.

No AWS paid runtime is required merely to preserve this lane. Do not enable uncapped or paid AWS usage without approval.

## Mini challenge: Open Source

Official requirement: ship a new additional open-source project or a contribution to a public repository during the hackathon window and include the contribution URL, repo URL, GitHub username, what changed, how it works, and why it matters.

Current evidence:

- [x] Public repository: `https://github.com/crisjonblvx/earn-before-spend-agent`
- [x] MIT license
- [x] Repository created during the hackathon window.
- [x] Amazon-specific work lives on `bonita/amazon-alexa-zero-capital`.
- [ ] Add final contribution/PR URL to Devpost after the Amazon adaptation PR exists.
- [ ] GitHub username: `crisjonblvx`

## Required Devpost artifacts

- [x] Project description draft: `DEVPOST.md`
- [x] Source repository with code and run instructions
- [x] Pre-existing-project delta disclosure in `DEVPOST.md`
- [x] Product feedback draft for Alexa+ simulated path and Strands SDK
- [ ] Public YouTube or Vimeo demo video in English, **under 3 minutes**
- [ ] Final track selection: Alexa+
- [ ] Final mini challenge selections: AWS Builder and Open Source only if evidence remains valid
- [ ] Final product-feedback field copied from verified draft
- [ ] Optional friction log only if it contains real observed friction; do not invent entries for bonus points

## Code verification

Run before recording the final demo:

```bash
python test_core.py
python test_alexa_simulator.py
```

Expected zero-provider test count on this branch:

- 6 deterministic economic guardrail tests
- 2 Alexa simulator smoke tests
- **8 total tests**

No model-provider call, AWS runtime, payment, or external side effect is required by these tests.

## Demo sequence (<3 minutes)

1. State the problem: people spend before they prove they can earn.
2. Ask the Alexa+-style prompt.
3. Show three candidate opportunities.
4. Show at least one blocked candidate and why it fails.
5. Show a qualified candidate with a human-only terms gate.
6. Show the $0 / $0 / $0 fail-closed scoreboard.
7. Briefly show the deterministic core + Strands tool layer.
8. Close on the principle: possible money is not earned money until an external payout clears.

## Human-only gates

CJ approval is required before:

- joining the hackathon / accepting official rules;
- requesting or consuming AWS promotional credits;
- enabling paid or uncapped AWS/runtime resources;
- publishing the demo video;
- submitting the Devpost entry;
- providing identity, tax, prize, or payout documentation.

## Scoreboard

Starting capital: **$0**  
New cash spent: **$0** unless explicitly authorized  
Verified external earnings: **$0** until an actual external payout clears
