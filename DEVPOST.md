# Amazon Build, Ship, Shape Devpost Draft

## Project name

Earn Before Spend

## Tagline

A zero-capital Alexa+ simulation that ranks legitimate ways to earn before spending.

## Primary track

Alexa+

## Mini challenges

- AWS Builder — the project uses the Strands Agents SDK as its agentic tool layer.
- Open Source — the repository is public, MIT licensed, and the Amazon-specific Alexa+ simulation work is being developed during the hackathon window.

## Inspiration

Creators, independent professionals, small businesses, and community organizations routinely spend money before validating whether an idea can earn anything. They buy software, ads, domains, APIs, courses, and subscriptions first, then hope revenue appears later.

Earn Before Spend reverses that sequence. The goal is to move from $0 in new seed capital toward verified positive cash contribution while refusing hidden costs, excessive owner labor, unclear rights, unclear eligibility, unverifiable payouts, gambling, speculation, or deceptive tactics.

For Build, Ship, Shape, we adapted that workflow into an Alexa+-style simulated experience. A user can ask for the fastest legitimate way to earn without spending new cash, compare a small set of opportunities, and receive a ranked answer that preserves human control over terms, identity, publication, and money movement.

## What it does

The Alexa+ simulation accepts up to three candidate earning opportunities and sends them to a deterministic ranking endpoint. The model is not allowed to decide whether an opportunity is economically safe on its own.

The hard gate checks:

- whether new cash is required before the earning event;
- whether the owner is being turned into hidden fulfillment labor;
- whether rights and eligibility are clear;
- whether the payout can be independently verified;
- whether the counterparty clears a legitimacy threshold;
- whether the payout probability input is valid;
- whether the next step requires a human to accept terms or make a legal, identity, publication, or payment decision.

Blocked opportunities receive a score of zero. Qualified opportunities are ranked by expected value, legitimacy, fit, urgency, and owner dependence.

The user-facing response keeps a fail-closed scoreboard:

- starting capital: $0;
- new cash spent: $0 unless explicitly authorized;
- verified earnings: $0 until an external payout actually clears.

## Alexa+ experience

Primary interaction:

> "Alexa, find the fastest legitimate way to make money without spending new cash."

The simulated Alexa+ web experience then:

1. receives a small set of candidate opportunities;
2. runs each through the deterministic zero-cash gate;
3. rejects blocked options even if their headline payout is large;
4. ranks qualified paths;
5. explains the smallest bounded next action;
6. surfaces any human-only gate;
7. leaves verified earnings at $0 until money is actually received.

This uses the hackathon's permitted simulated Alexa+ experience path. No Alexa hardware is required for the demo.

## How we built it

The project is intentionally split into authority and explanation layers.

### Deterministic economic authority

`core.py` contains the qualification and ranking rules. Those rules cannot be overridden by model persuasion.

### Alexa+ simulation

`alexa_simulator/server.py` exposes a local web experience and a deterministic `/api/rank` endpoint. It makes no provider call in its default mode and therefore does not consume AWS or model-provider credits merely to demonstrate the product.

### Strands Agents SDK

`agent.py` wraps the deterministic functions as Strands tools:

- `evaluate_opportunity`
- `rank_opportunities`

Strands provides the agentic explanation/tool-use layer while deterministic Python remains authoritative. This documented Strands integration is the basis for the AWS Builder mini-challenge lane.

### Tests

The repository includes focused economic guardrail tests plus simulator smoke tests covering:

- no-new-cash enforcement;
- owner-labor limits;
- missing rights/payment proof;
- human-only terms acceptance;
- urgency ranking;
- blocked-candidate suppression;
- deterministic simulator health;
- preservation of the human gate and zero-cash scoreboard through the Alexa-style API.

## Challenges we ran into

The main product challenge was avoiding "AI optimism." A language model can make almost any revenue idea sound actionable. That is unacceptable when an agent is reasoning about money.

We separated reasoning from authority: the agent can explain and compare, but deterministic code controls eligibility and ranking.

During the Amazon adaptation we also found a concrete packaging bug in the Alexa+ simulator: running `python alexa_simulator/server.py` directly could fail because the repository root was not guaranteed to be on Python's import path. We fixed the simulator so the documented direct-run command resolves the shared economic core correctly, and added an automated smoke test for the local experience.

## Accomplishments we're proud of

- A working Alexa+-style simulated experience that can be demonstrated without hardware.
- Economic guardrails outside the model.
- A fail-closed $0 scoreboard that does not treat prizes, credits, owner deposits, loans, gifts, or test payments as earnings.
- Explicit human escalation for terms, identity, legal commitments, publication, and spending.
- A deterministic demo path that does not require paid inference.
- Strands Agents SDK integration for the AWS Builder lane.
- A public MIT-licensed implementation suitable for the Open Source mini-challenge.

## Product feedback

### Alexa+ simulated-experience path

What we used it for: the hackathon's permitted web simulation path let us design and demonstrate an Alexa+-style interaction without requiring proprietary hardware or a production Alexa deployment.

What worked well: the simulation option lowers the barrier to testing interaction design and makes it possible to show the complete decision loop with ordinary web tooling.

What needs work / onboarding friction: it would help to have a single end-to-end reference showing the minimum expected artifacts for a simulated Alexa+ entry, especially the boundary between a convincing interaction simulation and a production Agent Skill or MCP integration.

Would we build with it again: yes, particularly for early-stage interaction validation before committing to a production device integration.

### Strands Agents SDK

What we used it for: exposing deterministic evaluation and ranking functions as agent tools while keeping the hard economic rules outside the model.

What worked well: the tool abstraction maps cleanly onto bounded functions, which made it straightforward to separate agent reasoning from non-negotiable policy.

What needs work / onboarding friction: for zero-capital experiments, provider configuration and cost boundaries should be extremely explicit so a developer can prove when a local or deterministic path makes no model-provider call.

Would we build with it again: yes. The tool model is a strong fit for systems where the LLM can explain and orchestrate but must not own final authority.

## What we learned

Autonomy works better when authority is narrow and legible.

Instead of asking an agent to "make money," we decompose the goal into discovery, qualification, ranking, bounded execution, payout verification, and cost reconciliation. The agent is strongest at context and explanation. Deterministic code is stronger at enforcing non-negotiable economic constraints.

The Alexa+-style interaction also makes the human-gate concept easier to understand: the experience can say what it can safely prepare, then clearly stop where a real person must approve terms, identity, publication, or money movement.

## What was built or changed during this hackathon window

Earn Before Spend existed before this Amazon-specific adaptation, so we are disclosing the delta clearly.

During the Build, Ship, Shape submission window we added or materially updated:

- the Alexa+-style local web simulator;
- the deterministic simulator API;
- Amazon-specific architecture and submission documentation;
- an Amazon-specific demo script;
- a direct-run import fix for the simulator;
- automated Alexa simulator smoke tests;
- Amazon track and mini-challenge positioning;
- Amazon-specific product feedback and submission copy.

The original zero-capital economic core and Strands tool layer predate this Amazon adaptation and are not being represented as newly created for this contest.

## Built with

- Python
- Strands Agents SDK
- Standard-library HTTP server
- HTML/CSS/JavaScript for the local Alexa+ simulation
- Deterministic Python guardrails

## Repository

https://github.com/crisjonblvx/earn-before-spend-agent

## Submission still requires human approval

Before entry, the owner must personally approve joining the hackathon and accepting its official rules. The demo video must then be published to YouTube or Vimeo and the final Devpost entry submitted before the deadline.

No contest registration, terms acceptance, payout setup, or submission is performed by this draft.
