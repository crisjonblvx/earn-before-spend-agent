# Amazon Build, Ship, Shape — submission draft

Status: **not submitted**. Preparation only. Joining the hackathon, accepting rules, identity/tax attestations, adding external reviewers, and final submission remain human-controlled.

Official deadline: **October 23, 2026 at 12:00 PM PDT**  
Official page: https://amazonappdev2026.devpost.com/

## Proposed entry

**Project:** Earn Before Spend  
**Primary track:** Alexa+  
**Implementation path:** Official simulated Alexa+ web experience  
**Mini challenge:** Open Source  
**Repository:** https://github.com/crisjonblvx/earn-before-spend-agent  
**License:** MIT

## Why this path

The Alexa+ rules explicitly allow builders who are not using the live Preview stack to build a **simulated Alexa+ experience in a web app using a preferred agentic tool**. This lets Earn Before Spend demonstrate an assistant interaction without buying hardware, enabling paid infrastructure, or pretending to have Alexa+ Preview access.

The Open Source mini challenge is a natural adjacent lane because this Amazon-specific work is being added as a public pull-request contribution during the hackathon window. The primary submission remains Alexa+; the mini challenge is layered onto the same project.

## What the project does

Earn Before Spend helps a creator, freelancer, small business, or community organization answer:

> What is the smallest credible way to move from $0 in new seed capital toward verified earned money?

A deterministic policy layer rejects opportunities that require new cash, hide excessive owner labor, have unclear rights or eligibility, or lack a verifiable payout path. The assistant layer explains the qualified next move while preserving human approval for third-party terms and other binding commitments.

For the Amazon entry, `alexa_sim.py` turns that workflow into a voice-assistant-style web experience:

- “What is my best zero-capital earning move?”
- “Should I pay $99 to enter the $50,000 accelerator?”

The second query is intentionally important. The simulated Alexa+ response refuses the spend because deterministic policy marks the opportunity ineligible before payout size is considered.

## What changed during the Amazon hackathon window

The core project existed before August 31, 2026. This entry therefore does **not** present the whole repository as newly created.

Amazon-period contribution:

- added a zero-dependency simulated Alexa+ web experience;
- added natural-language demo intents for “best next move” and “should I spend?”;
- added a visible zero-capital safety demonstration where a $50,000 headline opportunity is blocked because it requires $99 of new cash;
- preserved deterministic economic authority instead of giving the conversational layer permission to re-rank blocked options;
- preserved human approval for third-party terms;
- added offline unit tests proving the spend guardrail and human-gate behavior;
- added Amazon-specific submission copy, product feedback, friction log, and a sub-3-minute demo script.

No paid Amazon service, Amazon device, or external model call is required for the simulated experience.

## How to run

```bash
python alexa_sim.py
```

Then open:

```text
http://localhost:8010
```

Run the complete offline test suite:

```bash
python -m unittest discover -v
```

## Devpost description draft

**Earn Before Spend is a simulated Alexa+ experience for people who need the next credible earning move, not another reason to spend first.**

The project separates conversation from financial authority. A deterministic Python policy evaluates possible earning paths for new cash required, owner labor, rights, eligibility, legitimacy, payout verification, urgency, and expected value. The assistant can explain the result, but it cannot make a blocked opportunity eligible.

In the Amazon demo, a user can ask for the best zero-capital earning move and receive the top qualified option plus the remaining human approval gate. Then the user can ask whether to pay $99 to enter a $50,000 accelerator. The system rejects it because the mission begins at $0 in new capital. A bigger headline prize does not get to override the rule.

That interaction is delivered as the official Alexa+ simulated-experience path: a working web app, no special device required. The Amazon-specific code is added as a public open-source contribution during the hackathon period, so the same project also targets the Open Source mini challenge.

## Judging criteria mapping

### Tech implementation

The conversational simulation is a working web application, not a mock screenshot. Its POST `/api/alexa` endpoint calls the same deterministic ranking logic used by the project. Unit tests prove that a paid-entry opportunity cannot outrank qualified zero-capital options and that human terms acceptance remains a gate.

### Design

The interaction is intentionally simple: ask a money question, hear a concise answer, and inspect the auditable structured result. The UI includes one-click judge prompts so the safety boundary can be demonstrated in seconds.

### Potential impact

Creators and small organizations routinely buy tools, ads, subscriptions, and infrastructure before proving a revenue path. Earn Before Spend flips that sequence: qualify the earning path first, then allow spending only after evidence justifies it.

### Quality of idea

Most assistant demos optimize for doing more. This one is designed to say **no** when the economics do not satisfy the mission, even when the opportunity sounds exciting.

## Product feedback draft

### What was used

For the primary track, the project uses the official **simulated Alexa+ experience** path described in the hackathon requirements. No Amazon runtime SDK or Preview-only API is claimed.

### What worked well

The simulated path dramatically lowers the barrier to experimenting with Alexa+-style experiences. It lets a builder prove the interaction model and agent behavior before requiring access to a production assistant environment.

The requirement that the simulation source be present in the repository is also useful. It pushes entries toward something judges can inspect rather than a concept video with no runnable implementation.

### What could improve

A dedicated “Simulated Alexa+ in 15 minutes” quickstart would reduce uncertainty. The ideal page would put these items together:

1. confirmation that no Alexa+ Preview access is required for the simulated path;
2. the minimum submission evidence judges expect from a simulation;
3. one tiny web example with a text/voice-style request and assistant response;
4. guidance on how simulated entries are evaluated relative to MCP/Agent Skill entries;
5. a checklist separating “simulated” claims from live Alexa+ integration claims.

### Would we build with it again?

Yes for prototyping and validation. The simulated route is a credible way to test whether an assistant interaction deserves deeper platform integration before incurring more implementation cost.

## Friction log

**Task attempted:** Determine the lowest-cost compliant way to enter the Alexa+ track without claiming Preview access or requiring hardware.

**Steps:** Read the official overview, primary-track requirements, repository requirements, and demo requirements.

**Expected:** A single simulated-experience quickstart with a minimum viable architecture and submission checklist.

**Actual:** The simulated route is explicitly allowed, but builders still need to connect the requirement language to their own web stack and make sure the demo clearly communicates that it is a simulation.

**Severity:** Medium-low.

**Workaround:** Built a zero-dependency web simulation with an explicit “simulated Alexa+ experience” label, auditable JSON responses, and tests.

**Actionable suggestion:** Add a dedicated simulation starter and a sample Devpost evidence checklist. That would reduce accidental over-claiming and make onboarding faster.

## Submission evidence checklist

- [x] Existing public repository
- [x] MIT open-source license
- [x] Amazon-specific code added during hackathon window
- [x] Working simulated Alexa+ source
- [x] Deterministic spend guardrail
- [x] Human terms gate preserved
- [x] Offline unit tests for Amazon simulation
- [x] Product feedback draft
- [x] Friction log draft for optional judging bonus
- [x] Demo script under 3 minutes
- [x] Public contribution / PR URL: https://github.com/crisjonblvx/earn-before-spend-agent/pull/6
- [ ] Public demo URL
- [ ] Public YouTube/Vimeo demo under 3 minutes
- [ ] Devpost project joined by human
- [ ] Final rules/eligibility reviewed and accepted by human
- [ ] Final submission reviewed and submitted by human

## Open Source mini challenge fields

**Contribution URL:** https://github.com/crisjonblvx/earn-before-spend-agent/pull/6  
**Repository URL:** https://github.com/crisjonblvx/earn-before-spend-agent  
**GitHub username:** crisjonblvx

**What changed:** Added a working simulated Alexa+ web experience to an existing zero-capital opportunity agent, including a conversational spend-refusal path, deterministic economic authority, human approval gates, tests, submission documentation, and a judge demo script.

**How it works:** The web simulation sends an utterance to a local `/api/alexa` endpoint. The response is generated from `core.py` evaluations. If an opportunity requires new cash, its score becomes zero and it cannot be recommended by the assistant.

**Why it matters:** Assistant UX becomes more trustworthy when irreversible economic policy is outside the generative/conversational layer.

## Zero-capital scoreboard

Starting new seed capital: **$0.00**  
New cash spent: **$0.00**  
Verified external earnings: **$0.00**

Possible prizes, AWS credits, test data, and pending awards do not count as earnings.
