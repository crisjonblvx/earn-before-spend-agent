# Nebius x NVIDIA Devpost draft — Earn Before Spend

Status: draft only. Do not submit until the human entrant reviews the official rules and accepts the submission terms.

## Project name

Earn Before Spend

## Track

Best Apps and Agents

## One-line pitch

A bounded economic agent that ranks zero-new-cash earning paths, preserves hard safety and legitimacy gates, and uses NVIDIA Nemotron on Nebius Token Factory to explain the smallest credible next action toward verified external cash.

## Inspiration

Creators, independent professionals, small businesses, and community organizations often spend before they have evidence that an idea can earn. Earn Before Spend flips that order: qualify the earning path first, reuse existing assets, take one bounded action, and count money only after an external payout actually clears.

## What it does

Earn Before Spend evaluates opportunities such as bounties, competitions, services, digital products, licenses, affiliate commissions, and grants/awards. A deterministic Python layer rejects candidates that require new cash, excessive owner fulfillment, unclear rights or eligibility, low legitimacy, or unverifiable payout.

The surviving evaluations are passed to NVIDIA Nemotron 3 Super 120B through Nebius Token Factory. Nemotron is not allowed to override the deterministic blockers. Its job is to explain one conversion-first next action, surface any human approval gate, and keep the earnings scoreboard honest.

## How we built it

The economic policy is provider-independent Python in `core.py`. The Nebius submission-period update adds `nebius_reasoner.py`, which creates an OpenAI-compatible `/v1/chat/completions` request to Nebius Token Factory and defaults to `nvidia/nemotron-3-super-120b-a12b`.

The model sees the deterministic ranking rather than raw permission to decide eligibility. The system prompt explicitly forbids inventing earnings or bypassing terms, identity, tax, legal, spending, or publication gates. The Token Factory path fails closed without `NEBIUS_API_KEY`, and the repository never stores the credential.

## Significant update during the submission period

The project existed previously as a deterministic zero-capital agent prototype with a Strands-based reasoning path. During the Nebius x NVIDIA submission period, we added a dedicated Nebius Token Factory runtime adapter using NVIDIA Nemotron, an offline test seam for the Token Factory request path, explicit provider/model configuration, and submission-specific documentation. This changes the live reasoning architecture while preserving the original deterministic safety/economic gate.

## Why Nebius + NVIDIA matters here

The deterministic layer is intentionally narrow: it can enforce hard economic rules, but it should not pretend to understand every tradeoff in natural language. Nemotron provides the reasoning and explanation layer after qualification. Token Factory gives the project a direct runtime path to an NVIDIA open model while keeping the policy logic inspectable and independent of the model.

## Challenges

The central design challenge is preventing a capable model from turning persuasive language into an economic fact. A likely prize is not revenue. A test payment is not revenue. A credit is not revenue. The architecture therefore makes eligibility deterministic first and gives the model only the bounded job of explaining what to do next.

## Accomplishments

- Deterministic zero-new-cash qualification and ranking.
- Human gates for terms, identity, legal commitments, publication, and spending.
- Dedicated Nebius Token Factory runtime adapter.
- NVIDIA Nemotron 3 Super as the default reasoning model.
- Offline tests for endpoint targeting, model selection, request construction, gate preservation, and missing-key failure.
- MIT-licensed public repository with no private BLVX/Bonita code or credentials.

## What we learned

Agentic economic systems need two scoreboards: what the agent believes is promising and what the outside world has actually paid. Keeping those separate makes the system less flashy but more useful. It also gives the reasoning model a clearer job: explain the next move without changing the ledger.

## What's next

Complete one approved live Token Factory inference test, capture a judge-accessible working demo, record the sub-3-minute demo video, fold the Nebius setup into the main README, and provide concrete feedback from the real Token Factory/Nemotron run.

## Technologies

Python, Nebius Token Factory, NVIDIA Nemotron 3 Super, Strands Agents SDK, deterministic policy rules, unittest.

## Links to provide before submission

- Code: https://github.com/crisjonblvx/earn-before-spend-agent
- Working demo: TODO after live Token Factory path is deployed/testable
- Demo video: TODO, public YouTube, 3 minutes or shorter

## Feedback field

Do not fabricate this section. Write it only after the live Token Factory test so the submission can include specific feedback about setup, model behavior, latency, API compatibility, or documentation.
