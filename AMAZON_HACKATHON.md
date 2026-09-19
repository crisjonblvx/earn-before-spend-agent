# Amazon Build, Ship, Shape Adaptation

Status: PRE-SUBMISSION RESEARCH BRANCH. No hackathon registration, terms acceptance, paid resource use, or submission has been performed by this branch.

## Opportunity

Primary track: Alexa+ simulated experience.

Mini challenges to target:

- AWS Builder, because Earn Before Spend already uses the Strands Agents SDK.
- Open Source, because this repository is MIT licensed and was created during the hackathon submission period.

## Why this passes the zero-capital gate

The competition states that no purchase or payment is necessary to enter. The Alexa+ rules explicitly permit a simulated Alexa+ experience in a web app using an entrant's preferred agentic tools, so no proprietary Alexa hardware is required for this path.

Earn Before Spend was created on September 14, 2026, after the Amazon hackathon submission period opened on August 31, 2026. It is already a public MIT-licensed repository and uses Strands Agents SDK.

No new cash is required to prepare the simulation, documentation, or demo assets. Any optional AWS runtime call must remain disabled until CJ explicitly authorizes use of an existing capped credit balance or another $0-new-cash route.

## Proposed Alexa+ experience

Voice-style prompt:

> "Alexa, find the fastest legitimate way to make money without spending new cash."

The experience then:

1. accepts up to three candidate opportunities;
2. runs each through the deterministic zero-cash gate;
3. rejects hidden-cost, excessive-owner-labor, unclear-rights, unclear-eligibility, or unverifiable-payout candidates;
4. ranks only qualified candidates;
5. explains the smallest bounded next action;
6. explicitly calls out any terms, identity, publication, or payment step that requires a human decision;
7. keeps the scoreboard at $0 earned until an external payout is verified.

The Alexa-style UI is only an interaction layer. The LLM cannot override the deterministic economic rules.

## Bounded build plan

Prepared without external account action:

- add a small local web simulator for the Alexa+ experience;
- keep deterministic mode as the default, with no model-provider call;
- allow optional Strands mode only behind an explicit environment flag;
- add a contest-specific demo script and friction log template;
- do not add Amazon credentials, payment methods, or paid runtime dependencies.

## Human gates

CJ approval is required before any of the following:

- joining the Amazon/Devpost hackathon or accepting official rules;
- enabling AWS runtime usage or consuming promotional/paid credits;
- publishing a contest-specific demo video;
- submitting the entry;
- providing tax, identity, prize, or payout documentation.

## Expected payout

Possible, not earned:

- Alexa+ track prizes: up to the current published track award amounts.
- AWS Builder mini challenge: $5,000 cash plus AWS credits.
- Open Source mini challenge: $5,000 cash plus AWS credits.

Competition prizes remain $0 on the earnings scoreboard unless an external cash payment actually clears.

## Deadline

Current published submission deadline: October 23, 2026 at 12:00 PM PDT.

## Evidence URLs

- https://amazonappdev2026.devpost.com/
- https://amazonappdev2026.devpost.com/rules
