# Nebius x NVIDIA Devpost submission draft

> Status: **prepared, not submitted**. This file is a conversion packet only. Joining/submitting the hackathon, accepting rules, making identity/legal attestations, and entering payout details remain human-controlled.

## Submission target

- **Project:** Earn Before Spend
- **Track:** Best Apps and Agents
- **Public repository:** https://github.com/crisjonblvx/earn-before-spend-agent
- **License:** MIT
- **Nebius runtime:** Token Factory inference API
- **NVIDIA model:** `nvidia/nemotron-3-super-120b-a12b`
- **Deadline:** October 30, 2026 at 10:00 AM PDT

## Short description

**Earn Before Spend is a bounded AI agent that helps creators, independent professionals, small businesses, and community organizations find the smallest credible path from $0 in new seed capital to verified positive cash contribution.** A deterministic Python economic gate rejects opportunities that require new cash, unclear rights or eligibility, hidden owner labor, unverifiable payout, or negative-margin economics. NVIDIA Nemotron on Nebius Token Factory then explains the qualified choices and proposes the smallest bounded next action without being allowed to override those hard economic rules.

## What the project does

Earn Before Spend evaluates candidate earning opportunities such as fixed-fee work, digital products, bounties, grants, no-fee competitions, licensing, affiliate commissions, and marketplace channels. Before an LLM can reason about an option, the deterministic gate checks whether the opportunity is economically and procedurally eligible. It blocks paid-entry speculation, hidden costs, unclear rights, weak legitimacy, invalid probability inputs, and paths that cannot produce verifiable external money.

For the Nebius x NVIDIA build, the reasoning layer routes through NVIDIA Nemotron 3 Super on Nebius Token Factory. The model receives the already-qualified deterministic context, explains the tradeoffs, and selects a bounded next action. Terms acceptance, public submission, payout setup, identity/tax/legal attestations, spending, and money movement stay behind explicit human gates.

The scoreboard is deliberately conservative: possible prizes, owner deposits, credits, test payments, and hypothetical value never count as earnings. Money becomes verified only after an external payout clears and attributable costs are reconciled.

## Why Nebius + NVIDIA matter to the architecture

The model is not decoration. The project separates **economic authority** from **language reasoning**:

1. Python deterministically qualifies and ranks opportunities.
2. That structured context is sent at runtime to NVIDIA Nemotron through Nebius Token Factory.
3. Nemotron turns the qualified state into an intelligible decision and next bounded action.
4. The model is explicitly prohibited from reversing an ineligible deterministic decision.
5. Human-only gates remain visible instead of being silently crossed by the agent.

This makes the AI useful where it is strong, comparison, explanation, prioritization, and action framing, while keeping money and authority boundaries testable in ordinary code.

## Significant update during the hackathon period

Earn Before Spend existed before the Nebius x NVIDIA submission period. The significant hackathon-period update is a new Nebius Token Factory execution path using NVIDIA Nemotron 3 Super, plus network-free adapter tests, a sanitized one-command live evidence tool, updated judge-facing architecture/setup documentation, and this submission packet.

The earlier AWS/Strands path remains visible in the repository for provenance. It is not represented as the Nebius execution layer. The material Nebius/NVIDIA changes are isolated in `nebius_agent.py`, `nebius_smoke.py`, `test_nebius_agent.py`, `NEBIUS-NVIDIA.md`, and the updated `README.md`.

## How it was built

- Python deterministic qualification/ranking engine in `core.py`
- Nebius Token Factory adapter in `nebius_agent.py`
- NVIDIA Nemotron 3 Super as the reasoning/explanation model
- `nebius_smoke.py` for one bounded live inference call and sanitized evidence output
- Network-free unit tests validating that deterministic blockers remain authoritative
- Human decision gates for terms, identity/legal attestations, public submission, paid resources, payout setup, and money movement

## Judge setup / testing instructions

```bash
git clone https://github.com/crisjonblvx/earn-before-spend-agent.git
cd earn-before-spend-agent
pip install -r requirements.txt
python demo.py
python -m unittest test_core.py test_nebius_agent.py -v
```

A live Nebius/Nemotron run requires a Nebius Token Factory API key supplied by the tester:

```bash
export NEBIUS_API_KEY="..."
python nebius_smoke.py
```

The live smoke command performs one Token Factory completion and prints a sanitized record containing provider/model, endpoint host, UTC completion time, deterministic-context hash, completion hash, completion text, and an explicit truth boundary. It never prints the API key.

## Judging-criteria map

### Technological Implementation

The project uses a real runtime call to Nebius Token Factory with NVIDIA Nemotron. Deterministic qualification remains authoritative, so the LLM cannot alter hard economic eligibility decisions. Offline tests verify the handoff structure without requiring network access; the live smoke path provides bounded runtime proof after the API-key gate.

### Design

The product experience is intentionally opinionated: users do not receive an endless idea list. They receive qualified options, rejected options with reasons, a ranked next action, and a visible human gate when authority is required. The product is designed around decision clarity rather than chatbot novelty.

### Potential Impact

Creators and small organizations often spend before validating whether an idea can earn. Earn Before Spend reverses that sequence. It is aimed at users for whom another subscription, ad spend, or speculative build can create real financial downside, and it treats verified external money, not activity, as the success metric.

### Quality of the Idea

The non-obvious part is the split between a deterministic economic constitution and an LLM reasoning layer. Nemotron is useful because the opportunity set is messy and contextual, while the deterministic gate keeps the model from rewriting eligibility, cost, payout, and authority rules when it reasons persuasively.

## Demo video plan, under 3 minutes

**0:00-0:20 — Problem.** Show the question: “What is the smallest credible way to get from $0 new seed capital to verified positive cash contribution?” Explain that most AI agents optimize for activity; this one optimizes for verified external money under a hard no-new-cash constraint.

**0:20-0:55 — Deterministic gate.** Run the provider-free demo. Show at least one opportunity rejected for an economic blocker and one qualified opportunity. Make clear that this decision happens before Nemotron.

**0:55-1:35 — Nebius/Nemotron live path.** Run `python nebius_smoke.py` with the API key already configured outside the recording frame. Show the Token Factory provider/model, endpoint host, context hash, completion hash, and completion. Do not reveal secrets.

**1:35-2:05 — Why the model cannot cheat.** Open the architecture or relevant code and show that Nemotron receives deterministic context and cannot reverse an ineligible decision.

**2:05-2:35 — Real-user value.** Explain the target users and how the agent surfaces one bounded next action rather than another brainstorm.

**2:35-2:50 — Hackathon update.** State that the pre-existing project was significantly updated during the submission period with the Nebius Token Factory + NVIDIA Nemotron execution path, tests, evidence command, and judge documentation.

**2:50-2:59 — Close.** “Earn Before Spend: prove the path to money before you spend money chasing it.”

## Required URLs still gated

- **Working demo / hosted app / test build:** `[HUMAN GATE: add free judge-access URL or test-build URL]`
- **Public YouTube demo:** `[HUMAN GATE: add public YouTube URL after recording the live run]`

The public repository URL is already available and contains the MIT license and setup instructions.

## Nebius / NVIDIA feedback field

Do **not** fill this with invented product feedback. Complete it only after the live Token Factory run. Capture concise observations under these headings:

- What was straightforward about Token Factory setup or inference
- What was confusing or slowed implementation
- What would make model discovery/configuration easier
- What was useful or limiting about Nemotron output for bounded agent reasoning
- One concrete product improvement that would materially help this workflow

This preserves eligibility for the feedback bonus without manufacturing experience we have not observed.

## Final pre-submission checklist

- [x] Public repository exists
- [x] MIT license exists in repository
- [x] README contains setup/run instructions
- [x] Significant-update explanation prepared
- [x] Best Apps and Agents track selected in draft packet
- [x] Nebius Token Factory + NVIDIA Nemotron architecture documented
- [x] Offline deterministic/adapter test path documented
- [x] One-command live smoke path prepared
- [ ] Live Nebius smoke run completed successfully with an approved API key
- [ ] Free working demo / test-build URL available through the judging period
- [ ] Public YouTube demo under three minutes published
- [ ] Honest Nebius/NVIDIA feedback written from observed use
- [ ] Human reviews official rules and explicitly submits the Devpost entry

## Truth boundary

Do not claim a successful Nebius runtime call until `nebius_smoke.py` actually completes against Token Factory. Do not claim verified earnings until an actual external payout clears. Do not expose API keys, payout data, tax information, or private credentials in the repository, video, screenshots, or Devpost fields.
