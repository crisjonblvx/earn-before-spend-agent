# Nebius x NVIDIA Submission Draft

Status: DRAFT ONLY. Do not submit without human approval.

## Project title

Earn Before Spend

## Tagline

A bounded economic agent that starts with $0, reuses authorized assets, rejects bad opportunities, and pursues the smallest credible path to verified outside revenue.

## Track

Best Apps and Agents

## What problem does it solve?

AI agents are increasingly able to browse, code, plan, and act, but economic autonomy creates a dangerous incentive problem: an agent can appear productive while quietly spending the owner's money, inventing hypothetical revenue, chasing unverifiable bounties, or crossing contractual and legal boundaries.

Earn Before Spend tests a stricter idea. Start at $0. Spend $0 in new cash. Reuse what is already authorized. Count money only when an external payout is verified. Surface terms, identity, payout, publication, and legal commitments as explicit human gates.

## What it does

The agent evaluates up to three current earning opportunities across pathways such as digital products, competitions, licensing, bounties, affiliate/referral programs, and grants or awards.

Each opportunity is passed through deterministic Python guardrails. The language model may research, compare, and explain, but it cannot override the economic gate.

An opportunity is rejected when it requires new cash, excessive CJ fulfillment, unclear rights or eligibility, unverifiable payout, or insufficient legitimacy. Qualified opportunities are ranked using expected payout, fit, legitimacy, urgency, and owner labor.

The system then prepares only the next bounded action and stops at human-controlled gates such as accepting third-party terms, submitting an entry, publishing private code, connecting payout accounts, enabling paid usage, or moving money.

## Significant updates made during the submission period

The original Earn Before Spend prototype was prepared for AWS Agents for Humans. The public repository begins September 14, 2026, inside the Nebius submission period; earlier private conceptual work does not establish a pre-August-26 implementation. Confirm the exact new/existing classification before submission. This adaptation updates the prototype by:

1. adding an explicit Nebius Token Factory model-provider adapter for NVIDIA Nemotron;
2. routing Strands through Nebius's OpenAI-compatible API;
3. keeping API credentials environment-only;
4. adding fail-closed provider configuration and tests;
5. adding an explicit one-request live-test gate, no retries or redirects, a 350-token limit, a persistent attempt lock, and a promotional-credit confirmation requirement;
6. adding a Nebius-specific evaluation plan for cost, rejection accuracy, resource-reuse reasoning, and human-gate compliance;
7. preserving deterministic Python as the final economic authority even when Nemotron provides reasoning and orchestration.

## NVIDIA / Nebius usage

Proposed model:

`nvidia/nemotron-3-super-120b-a12b`

Nebius Token Factory endpoint:

`https://api.tokenfactory.us-central1.nebius.com/v1/`

The project has a prepared runtime inference path to NVIDIA Nemotron through Nebius Token Factory; a successful live result remains pending. The model is used for opportunity comparison, explanation, and agent orchestration. Deterministic tools remain responsible for final qualification and ranking so the model cannot waive the zero-capital rules.

## Why Nemotron

Earn Before Spend needs more than text generation. It needs disciplined multi-step reasoning around incomplete opportunity data, tool outputs, competing expected values, and explicit human boundaries. Nemotron 3 Super is designed for agentic and complex reasoning workloads, making it a strong fit for the orchestration layer while deterministic code retains the hard financial constraints.

## Architecture

Current web / GitHub opportunity evidence
        |
        v
Nemotron on Nebius Token Factory
(research interpretation + orchestration)
        |
        v
Strands tools
        |
        +--> evaluate_opportunity()
        +--> rank_opportunities()
        |
        v
Deterministic Python economic gate
        |
        +--> Reject
        |
        +--> Qualified next bounded action
                 |
                 v
             Human gate

## Zero-capital scoreboard

- Starting capital: $0
- New cash spent: $0 unless explicitly authorized
- Promotional/cloud credits: resources, never earnings
- Competition prizes: possible money, never earnings until paid
- Revenue: counted only after independently verified external payout

## Example behavior

Candidate A is a self-serve digital product made from already-owned automation assets. It costs $0 to prepare, requires minimal owner effort, and has verifiable marketplace payout mechanics.

Candidate B is a paid-entry contest with a larger headline prize.

Candidate C is a bounty with an attractive payout but no reliable evidence that the reward is funded.

The agent should reject B because it violates the zero-new-cash rule and reject C because payout is unverifiable. It should rank A first but still stop before accepting marketplace terms or connecting a payout account.

## Product experience

The demo presents a small set of opportunities, shows the deterministic gate's accept/reject decisions, then asks Nemotron to explain the ranked result and identify the exact next action and human approval boundary.

The important UX moment is not simply that the agent finds an opportunity. It is that it can say no to attractive but invalid money-making paths and keep an auditable ledger that refuses to count hypothetical value as earnings.

## Judging criteria alignment

### Technological implementation

Nebius Token Factory hosts the NVIDIA model used for runtime reasoning. Strands provides the agent/tool layer. Deterministic Python implements the financial safety boundary.

### Design

The project is intentionally constrained around a clear mental model: Search -> Verify -> Gate -> Rank -> Prepare -> Human approval -> Verify payout.

### Potential impact

The same pattern can help creators, small businesses, nonprofits, and autonomous agents experiment with economic agency without silently turning an AI system into an uncapped spending mechanism.

### Quality of the idea

Most autonomous-agent demos optimize for how much an agent can do. Earn Before Spend measures whether an agent can pursue economic value while refusing actions that violate capital, legitimacy, rights, or human-control constraints.

## Demo video outline (<3 minutes)

1. 0:00-0:20 - The challenge: "Can an AI start with $0 and earn without spending the owner's money?"
2. 0:20-0:45 - Show the $0 scoreboard and deterministic rules.
3. 0:45-1:20 - Feed three opportunity candidates into the agent.
4. 1:20-1:50 - Show the deterministic rejection of paid-entry and unverifiable payout paths.
5. 1:50-2:20 - Show Nemotron reasoning over the qualified candidate and surfacing the human gate.
6. 2:20-2:40 - Show the audit trail and unchanged $0 verified-earnings ledger.
7. 2:40-2:55 - Explain the research question: can bounded agents become economically useful before becoming economically dangerous?

## Working-demo requirement

Before submission, the project must demonstrate at least one real runtime call to NVIDIA Nemotron on Nebius Token Factory and expose a working demo or test build for judges.

## Feedback section placeholder

Complete only after the live Nebius test. Record:

- model used;
- setup friction;
- response latency;
- tool-use quality;
- approximate token/cost behavior;
- any OpenAI-compatibility issues;
- what worked well;
- what would make Token Factory easier for agent builders.

Do not invent feedback before actual use.

## Remaining human gates

CJ must explicitly approve before:

- joining the hackathon / accepting official rules;
- joining Nebius Builder Program or accepting associated terms;
- supplying a Nebius API key;
- enabling any paid or uncapped usage;
- publishing or changing public competition materials;
- submitting the project;
- providing identity, tax, prize, or payout information.

## September 15 test-build update

A runnable, dependency-free Python web demo now exercises the actual gate with editable cash, labor and payout-evidence assumptions. `TEST_BUILD.md` provides judge setup instructions. `nebius_once.py` records a single real model response only after credentials, authorization and promotional-credit coverage are configured. The local narrated walkthrough is interim material, not a completed live-model video.
