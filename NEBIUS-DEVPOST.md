# Nebius x NVIDIA Global AI Hackathon — submission draft

Status: **not submitted**. This file is preparation only. Joining/submitting on Devpost, accepting rules, identity/tax attestations, and any paid resource remain human-controlled.

Official deadline: **October 30, 2026 at 10:00 AM PDT**  
Rules: https://nebiusglobalaihackathon.devpost.com/rules

## Proposed project

**Project name:** Earn Before Spend  
**Track:** Best Apps and Agents  
**Code repository:** https://github.com/crisjonblvx/earn-before-spend-agent  
**License:** MIT

### Tagline

A bounded AI agent that finds the smallest credible path from zero new capital to verified earned money without letting the model override economic guardrails.

## What changed during the hackathon period

The project existed before the Nebius x NVIDIA submission period, so this entry must rely on the rules' **significantly updated** path, not pretend it is a brand-new project.

Significant Nebius-period update on this branch:

- added a runtime Nebius Token Factory inference path;
- uses NVIDIA Nemotron 3 Super (`nvidia/nemotron-3-super-120b-a12b`);
- added a hard separation between deterministic economic authority and model explanation;
- added fail-closed key handling so no Token Factory request happens without an explicit `NEBIUS_API_KEY`;
- added offline adapter tests that validate endpoint, model selection, prompt boundary, and malformed-response handling without spending tokens;
- added `nebius_smoke.py`, a one-command live-proof path that performs one intentional Nemotron completion and writes a sanitized local evidence artifact without storing the API key;
- updated the demo so judges can see deterministic qualification first and the Nemotron explanation second.

## Why Best Apps and Agents

Earn Before Spend is an agent a creator, freelancer, small business, or community organization could use in a real workflow. The product is not a generic chatbot: it combines deterministic money/risk qualification with open-model reasoning for explanation and next-action selection.

The deterministic layer rejects opportunities that require new cash, have unclear rights/eligibility, hide excessive owner labor, or lack a verifiable payout path. Nemotron receives the already-qualified ranking and explains the best bounded next action plus the human approval gate. This preserves useful model reasoning without giving the model financial authority.

## Required Nebius/NVIDIA technology

**Nebius Token Factory** is used at runtime through its OpenAI-compatible chat completions API.

Default endpoint in code:

`https://api.tokenfactory.us-central1.nebius.com/v1/chat/completions`

Default model:

`nvidia/nemotron-3-super-120b-a12b`

Interactive runtime command after an authorized API key is configured:

```bash
NEBIUS_API_KEY="..." RUN_NEBIUS=1 python demo.py
```

Judge-evidence command after an authorized API key is configured:

```bash
NEBIUS_API_KEY="..." python nebius_smoke.py
```

The smoke script performs one live Token Factory + Nemotron call and writes `.nebius-evidence/live-evidence.json`, which is gitignored. The artifact contains provider/model, endpoint host, UTC completion time, a deterministic-context hash, a completion hash, the completion text, and an explicit truth boundary. It never records the API key and does not represent the call as earnings, payout, scale, or contest acceptance.

The no-key default remains offline. This is intentional zero-capital safety, not the final judging proof. Final submission must include a real recorded Token Factory call using the NVIDIA model.

## Draft description

Earn Before Spend is a bounded economic agent built around one discipline: **prove value before asking for more capital**.

A user supplies possible earning opportunities such as a service, bounty, digital product, competition, grant, license, or referral. Deterministic Python evaluates each option for upfront cash, owner labor, rights, eligibility, legitimacy, payout verification, urgency, and expected value. Blocked opportunities stay blocked even if their headline payout is huge.

The qualified ranking is then sent at runtime to NVIDIA Nemotron 3 Super on Nebius Token Factory. Nemotron is used where a large model is strongest: context, explanation, tradeoffs, and communicating the next bounded action. It is not allowed to reverse the deterministic gate or call hypothetical prizes, credits, owner deposits, loans, gifts, or test payments "earnings."

This architecture addresses a failure mode common to autonomous agents: models are very good at making possibilities sound actionable, but financial authority needs harder boundaries. Earn Before Spend separates reasoning from authority and escalates terms acceptance, identity/legal commitments, publication, and spending to a human.

## Demo plan (<3 minutes)

1. **0:00–0:25 — Problem:** Show three opportunities with very different headline payouts. Explain that largest payout must not automatically win.
2. **0:25–1:05 — Deterministic gate:** Run `python demo.py`. Show one candidate blocked/qualified based on objective constraints and the ranking output.
3. **1:05–1:50 — Nebius runtime:** Run `python nebius_smoke.py` using an authorized key. Show NVIDIA Nemotron 3 Super on Token Factory explaining the authoritative ranking, then show the sanitized evidence artifact proving the live call without exposing the key.
4. **1:50–2:20 — Safety proof:** Briefly show `nebius_model.py`: explicit model, Token Factory endpoint, no request without key, and prompt language forbidding re-ranking or invented earnings.
5. **2:20–2:45 — Tests:** Show adapter and smoke-evidence tests passing without network usage.
6. **2:45–2:59 — Impact:** Starting capital $0; possible prizes are not counted as earned money; the product exists to reduce wasteful spend before validation.

## Judging-criteria mapping

### Technological implementation

Token Factory is in the actual runtime path rather than being mentioned in copy only. NVIDIA Nemotron explains a deterministic ranking that the model cannot override. The smoke-evidence path makes the qualifying call independently auditable without leaking credentials.

### Design

The product has a coherent workflow: discover/enter opportunities → deterministic qualification → ranking → Nemotron explanation → human gate → bounded action → future payout reconciliation.

### Potential impact

Target users routinely spend on tools, ads, APIs, courses, or infrastructure before validating a revenue path. Earn Before Spend gives them a disciplined first-dollar workflow.

### Quality of idea

The non-obvious choice is **not** asking the model to decide what is economically safe. The open model handles ambiguity and communication while deterministic code enforces non-negotiable money rules.

## Bonus lanes

- **Most Valuable Feedback:** eligible only if the actual Devpost feedback section is completed truthfully. Do not claim until done.
- **Best Use of Tavily:** **not targeted in this iteration**. The rules require a functional runtime Tavily call. Do not add Tavily merely to chase a prize unless discovery/search becomes genuinely useful to the product and can be run at zero new cash.
- **City Winner:** do not claim without actual attendance at an eligible Builders & Brews city event.

## Evidence checklist

- [x] Public GitHub repository
- [x] Open-source MIT license
- [x] README setup/run guidance
- [x] Significant post-August-26 Nebius/NVIDIA code update staged on branch
- [x] Nebius Token Factory runtime adapter implemented
- [x] NVIDIA Nemotron model explicitly selected
- [x] Offline adapter tests pass
- [x] One-command sanitized live-evidence capture implemented and gitignored
- [ ] Human-authorized `NEBIUS_API_KEY` configured under a capped/free-credit route
- [ ] Real Token Factory + Nemotron runtime call captured in `.nebius-evidence/live-evidence.json`
- [ ] Working demo/test URL prepared if required by the final form
- [ ] <3 minute public demo video uploaded
- [ ] Devpost project created/joined by human
- [ ] Feedback section completed truthfully if pursuing the $100 feedback bonus
- [ ] Final submission reviewed and submitted by human

## Zero-capital scoreboard

Starting new seed capital: **$0.00**  
New cash spent: **$0.00**  
Verified external earnings: **$0.00**

Nebius credits, possible prizes, test calls, or pending awards do not count as earnings.
