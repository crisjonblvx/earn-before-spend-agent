# Nebius x NVIDIA Hackathon Adaptation

Status: PRE-SUBMISSION RESEARCH BRANCH. No hackathon registration, terms acceptance, API key, paid resource, or submission has been performed by this branch.

## Why this is a fit

Earn Before Spend is already a public MIT-licensed agent project with deterministic economic guardrails and a provider-agnostic Strands layer. The Nebius x NVIDIA Global AI Hackathon permits pre-existing projects when the submission clearly documents significant updates made during the submission period.

The competition requires a working project using an NVIDIA open-source model on Nebius Token Factory or Nebius AI Cloud, plus a public repository, demo, project description, and feedback.

## Significant update prepared here

This branch adds an explicit Strands OpenAI-compatible provider path for Nebius Token Factory while preserving the deterministic zero-cash gate as the source of truth.

Default proposed model:

`nvidia/nemotron-3-super-120b-a12b`

Default proposed endpoint:

`https://api.tokenfactory.us-central1.nebius.com/v1/`

The adapter reads `NEBIUS_API_KEY` only from the environment. No credential is committed.

## Zero-capital constraint

Do not enable pay-as-you-go usage for this experiment without human approval.

The intended test path is:

1. Human reviews and, if desired, joins the hackathon and Nebius Builder Program.
2. Human accepts the applicable third-party terms and obtains promotional Token Factory credits.
3. Human provides an environment-scoped API key.
4. Run a small capped evaluation using the promotional credit balance.
5. Record cost and behavior before any broader run.

Credits are resources, not earnings, and must never be added to the mission revenue scoreboard.

## Candidate competition angle

Track: Best Apps and Agents.

Demonstration: Earn Before Spend compares real or replayed opportunity candidates, invokes the deterministic qualification/ranking tools, explains rejections, and surfaces terms/identity/legal steps as human gates. Nemotron supplies reasoning and orchestration; deterministic Python retains final authority over the economic rules.

Research value: compare provider behavior on the same opportunity set, including rejection accuracy, resource-reuse reasoning, human-gate compliance, and cost per qualified action.

## Human gates

Human approval is required before any of the following:

- joining the Nebius or Devpost program;
- accepting Nebius, NVIDIA, Tavily, Devpost, or other third-party terms;
- creating or supplying an API credential;
- enabling any paid or uncapped cloud usage;
- publishing a demo video or final competition materials;
- submitting an entry or tax/identity/payout documentation.

## Earnings treatment

Competition prizes are possible payouts, not earned revenue. Count $0 until an independently verified external prize payment actually clears.
