# Devpost Submission Draft

## Project name

Earn Before Spend

## Tagline

A Strands agent that helps people find legitimate ways to earn before they spend.

## Track

Professional Agents

## Inspiration

Creators, independent professionals, small businesses, and community organizations routinely spend money before they have validated whether an idea can earn anything. They buy software, ads, domains, APIs, courses, and subscriptions first, then hope revenue shows up later.

We wanted to reverse that sequence.

The challenge behind Earn Before Spend is simple: start with $0 in new seed capital and identify the smallest lawful, ethical path to verified positive cash contribution. The answer does not have to be “start a business.” It could be a bounty, a paid service, a license, a competition, a referral commission, a digital product, or an award.

## What it does

Earn Before Spend accepts a small set of candidate earning opportunities and uses a Strands agent to reason about them. The model does not get to decide whether an opportunity is economically safe by itself. Deterministic Python tools enforce hard zero-capital rules.

The system asks:

- Does the opportunity require new cash before the earning event?
- Is the owner secretly being turned into the fulfillment worker?
- Are rights and eligibility clear?
- Is the counterparty credible enough?
- Can the payout be independently verified?
- How soon does the option expire?
- Does pursuing it require a human to accept third-party terms or make a legal/identity commitment?

Blocked opportunities are rejected even if their headline payout is enormous. Qualified opportunities are ranked by expected value, legitimacy, fit, urgency, and owner dependence.

The agent then recommends the smallest bounded next action. Consequential actions such as accepting contest rules, signing agreements, publishing private code, moving money, or spending remain human-controlled.

## How we built it

The project uses the Strands Agents SDK for the agentic reasoning and tool-use layer.

Two Strands tools expose deterministic Python functions:

- `evaluate_opportunity`: evaluates one structured opportunity against the zero-new-cash gate.
- `rank_opportunities`: evaluates and ranks up to three candidates after applying the hard gate.

The model can explain and orchestrate, but it cannot override blockers from the deterministic layer.

The default demo makes no provider call, so anyone can run the core ranking behavior without AWS spend. When a Strands-supported model is configured, the agent uses the same deterministic tools to produce a natural-language recommendation.

## Challenges we ran into

The most important design challenge was avoiding “AI optimism.” A language model is very good at making possibilities sound actionable. That is dangerous when the goal involves money.

We therefore separated reasoning from authority. A model can say that a $10,000 contest looks exciting, but deterministic code still blocks it if it requires upfront cash, has unclear eligibility, lacks a verifiable payout path, or exceeds the allowed owner labor.

We also needed to distinguish possible money from earned money. Credits, owner deposits, test payments, loans, gifts, and potential prizes do not count as earnings.

## Accomplishments we’re proud of

- A Strands-based agent whose economic guardrails are outside the model and cannot be overridden by model persuasion.
- A pathway model that does not assume entrepreneurship is the only way to create income.
- Explicit human escalation for terms, identity, legal commitments, publication, and spending.
- A deterministic no-provider-call demo that preserves the zero-capital premise.
- Focused tests covering hidden cash requirements, hidden owner fulfillment, unclear rights/payout proof, terms acceptance, urgency, and attempts to let a huge but blocked opportunity outrank a clean one.

## What we learned

Autonomy works better when authority is narrow and legible.

Instead of asking an agent to “make money,” we learned to decompose that goal into discovery, qualification, ranking, bounded execution, payout verification, and cost reconciliation. The LLM is strongest at context and judgment. Deterministic code is stronger at enforcing non-negotiable economic constraints.

## What’s next

The next layer is a trusted reconciliation service that verifies real payout events and subtracts fees, refunds, reserves, taxes, and attributable costs before recording positive cash contribution.

We also want to add event-driven opportunity discovery and an owner dashboard showing:

- starting capital;
- money received;
- pre-earning cash spent;
- net cash contribution;
- owner minutes required;
- pathway used;
- what the agent learned;
- the next bounded experiment.

Longer term, Earn Before Spend can become a reusable economic discipline for autonomous agents: do not silently burn owner money; prove value before asking for more capital.

## Built with

- Python
- Strands Agents SDK
- Standard library deterministic guardrails

## Disclosure

AI coding assistance was used to help develop the project. The public submission is a new standalone implementation created during the hackathon submission period. It was conceptually informed by earlier private work on autonomous-agent economics, but no private BLVX/Bonita source code, user data, customer data, private prompts, or proprietary cultural datasets are included in the public project.
