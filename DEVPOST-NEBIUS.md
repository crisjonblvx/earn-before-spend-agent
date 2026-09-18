# Nebius x NVIDIA Global AI Hackathon submission draft

## Project name
Earn Before Spend

## Track
Best Apps and Agents

## Tagline
A zero-capital agent that refuses to spend first and uses NVIDIA Nemotron on Nebius to explain the safest next earning move.

## What it does
Earn Before Spend helps creators, independent professionals, small businesses, and community organizations rank legitimate ways to move from $0 in new seed capital toward verified positive cash contribution.

The core design separates reasoning from authority. Deterministic Python guardrails decide whether an opportunity is economically admissible. They block options that require new cash, hide excessive owner labor, have unclear rights or eligibility, lack a verifiable payout path, or fall below the legitimacy threshold. NVIDIA Nemotron on Nebius Token Factory receives only the already-evaluated ranking and explains the smallest bounded next action. It cannot override the deterministic decision.

Consequential actions remain human-controlled: accepting third-party terms, making identity or tax attestations, submitting binding applications, publishing private code, moving money, and enabling paid resources.

## Why we built it
AI agents are very good at making possibilities sound exciting. That is dangerous when the goal is money. A conventional agent can easily recommend buying software, running ads, opening paid infrastructure, or chasing a high-headline prize before proving any value.

Earn Before Spend reverses that sequence. It treats a possible prize as possible money, not revenue; credits as credits, not earnings; and test payments or owner deposits as non-earnings. The goal is a disciplined path from discovery to qualification to bounded action to verified payout.

## How Nebius + NVIDIA are used
The hackathon integration adds an explicit Nebius Token Factory runtime path using the OpenAI-compatible chat-completions endpoint and NVIDIA Nemotron 3 Super (`nvidia/nemotron-3-super-120b-a12b`).

Runtime flow:
1. Candidate opportunities are evaluated and ranked by deterministic Python rules.
2. The resulting JSON is passed to the Token Factory integration.
3. NVIDIA Nemotron explains the ranking, preserves every blocker and human gate, and names one smallest bounded next action.
4. The application displays both the deterministic ranking and the model explanation so the authority boundary is visible to the user.

The default demo remains no-provider-call. A live Nebius call is opt-in via `RUN_NEBIUS=1` and requires `NEBIUS_API_KEY`. This avoids silently consuming paid inference.

## Significant updates during the Nebius x NVIDIA submission period
Earn Before Spend existed before this hackathon as a standalone public agent-economics prototype. During the Nebius x NVIDIA submission period, the project was significantly extended with:

- a new Nebius Token Factory runtime integration;
- NVIDIA Nemotron 3 Super as the explanation/reasoning model;
- an explicit authority boundary that prevents model output from changing deterministic economic blockers;
- an opt-in Nebius demo path that fails closed when no API key is configured;
- tests that verify the runtime target, selected NVIDIA model, authorization header behavior, blocker preservation in the prompt, and fail-closed handling of malformed responses.

No private BLVX/Bonita source code, user data, customer data, private prompts, or proprietary cultural datasets are included.

## Technical implementation
- Python
- Nebius Token Factory OpenAI-compatible API
- NVIDIA Nemotron 3 Super
- Strands Agents SDK (existing agentic layer)
- Standard-library deterministic economic guardrails
- `unittest` regression coverage

Relevant files:
- `core.py` - deterministic economic qualification and ranking
- `nebius_reasoner.py` - bounded Token Factory / Nemotron integration
- `demo.py` - deterministic demo plus opt-in Nebius runtime path
- `test_core.py` - economic guardrail tests
- `test_nebius.py` - Token Factory integration tests

## Judging-case summary
### Technological Implementation
Nebius/Nemotron is not a decorative API call. The model is placed deliberately after deterministic economic qualification, where it adds reasoning and communication without being allowed to weaken safety-critical money rules.

### Design
The product exposes a legible two-layer experience: hard economic decisions first, model explanation second. Users can see exactly why an opportunity is blocked and what still needs human approval.

### Potential Impact
Creators and small organizations often burn money before proving demand. The same failure mode becomes more dangerous with autonomous agents. Earn Before Spend offers a reusable pattern for agents that must prove value before asking an owner for more capital.

### Quality of the Idea
Instead of asking an agent to "make money," the system decomposes the problem into discovery, qualification, ranking, bounded execution, payout verification, and reconciliation. The core novelty is narrow agent authority around economics, not a generic financial chatbot.

## Demo plan (3 minutes max)
1. Show three candidate opportunities, including one attractive but blocked option.
2. Run the deterministic ranking and point out the blocked option cannot win regardless of headline payout.
3. Run the same evaluated JSON through Nebius Token Factory with NVIDIA Nemotron.
4. Show Nemotron explaining the top choice while preserving the deterministic blocker and human approval gate.
5. End on the scoreboard: starting capital $0, new cash spent $0, verified external earnings only after a real payout clears.

## Setup
Default no-provider-call demo:

```bash
python demo.py
```

Live Nebius/NVIDIA demo after a bounded API key is configured:

```bash
export NEBIUS_API_KEY="..."
RUN_NEBIUS=1 python demo.py
```

Optional model override:

```bash
NEBIUS_MODEL="nvidia/nemotron-3-super-120b-a12b" RUN_NEBIUS=1 python demo.py
```

## Feedback section
Complete this only after a real Token Factory run. Record concrete observations about API setup, response latency, model behavior, documentation clarity, and any issue encountered. Do not invent feedback before live use.

## Remaining submission gates
- Perform and capture at least one real Token Factory runtime call using NVIDIA Nemotron.
- Confirm the public repository setup instructions match the tested environment.
- Provide a working demo URL or test build for judging.
- Record a public YouTube demo of 3 minutes or less with audio explaining Nebius Token Factory and NVIDIA Nemotron usage.
- Complete the Devpost feedback fields from actual use.
- Human reviews and submits the entry and accepts any required competition terms.
