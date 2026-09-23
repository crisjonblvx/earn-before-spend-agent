# Nebius x NVIDIA Global AI Hackathon — submission draft

Status: **not submitted**. This file is preparation only. Joining/submitting on Devpost, accepting rules, identity/tax attestations, and any paid resource remain human-controlled.

Official deadline: **October 30, 2026 at 10:00 AM PDT**  
Rules: https://nebiusglobalaihackathon.devpost.com/rules

## Proposed project

**Project name:** Earn Before Spend  
**Track:** Best Apps and Agents  
**Code repository:** https://github.com/crisjonblvx/earn-before-spend-agent  
**License:** MIT

### Final prize-lane configuration

- **Overall awards:** eligible through the primary submission if the project passes baseline eligibility.
- **Best Apps and Agents:** primary track.
- **Most Valuable Feedback:** target with truthful implementation/runtime feedback.
- **Best Use of Tavily:** **conditional target** only after one successful human-authorized live Tavily runtime call is captured. Do not claim the bonus before that proof exists.
- **City Winner:** do not claim without actual attendance at an eligible Builders & Brews city event.

### Tagline

A bounded AI agent that finds the smallest credible path from zero new capital to verified earned money without letting the model override economic guardrails.

## What changed during the hackathon period

The project existed before the Nebius x NVIDIA submission period, so this entry must rely on the rules' **significantly updated** path, not pretend it is a brand-new project.

Significant Nebius-period updates:

- added a runtime Nebius Token Factory inference path;
- uses NVIDIA Nemotron 3 Super (`nvidia/nemotron-3-super-120b-a12b`);
- added a hard separation between deterministic economic authority and model explanation;
- added fail-closed key handling so no Token Factory request happens without an explicit `NEBIUS_API_KEY`;
- added offline adapter tests that validate endpoint, model selection, prompt boundary, and malformed-response handling without spending tokens;
- added `nebius_smoke.py`, a one-command live-proof path that performs one intentional Nemotron completion and writes a sanitized local evidence artifact without storing the API key;
- added a bounded Tavily discovery adapter and one-call evidence probe so the workflow can discover current candidate opportunities before deterministic verification;
- Tavily results are labeled unverified evidence and cannot bypass the economics, rights, eligibility, payout, labor, or legitimacy gates;
- added an explicit double gate for Tavily (`ALLOW_LIVE_TAVILY=1` plus `TAVILY_API_KEY`) and capped basic search to at most five results with no generated Tavily answer, raw-content pull, or image retrieval;
- updated the demo so judges can see discovery, deterministic qualification, and Nemotron explanation as separate responsibilities.

## Why Best Apps and Agents

Earn Before Spend is an agent a creator, freelancer, small business, or community organization could use in a real workflow. The product is not a generic chatbot: it combines current-opportunity discovery, deterministic money/risk qualification, and open-model reasoning for explanation and next-action selection.

The deterministic layer rejects opportunities that require new cash, have unclear rights/eligibility, hide excessive owner labor, or lack a verifiable payout path. Nemotron receives the already-qualified ranking and explains the best bounded next action plus the human approval gate. This preserves useful model reasoning without giving the model financial authority.

When Tavily is enabled through the explicit human-controlled live gate, it fills the **FIND** step only. Search results remain unverified until the deterministic layer accepts them. The resulting product chain is:

**FIND → VERIFY → RANK → EXPLAIN → HUMAN GATE → EARN**

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

## Conditional Tavily bonus path

The official rules list **Best Use of Tavily** as a $3,000 cash bonus for an otherwise eligible submission that makes a functional runtime Tavily API call as part of the solution.

The implementation is already staged in the product rather than added as prize bait:

- `tavily_discovery.py` performs a bounded basic Tavily Search request;
- `tavily_probe.py` performs one live discovery call and writes a sanitized `.tavily-evidence/search.json` artifact;
- both `ALLOW_LIVE_TAVILY=1` and `TAVILY_API_KEY` are required before the call;
- at most five results are requested;
- results are labeled `unverified_evidence_only` and cannot override deterministic qualification.

Only after a human approves the applicable Tavily terms and confirms a free or hard-capped credential may this run once:

```bash
ALLOW_LIVE_TAVILY=1 TAVILY_API_KEY="..." python tavily_probe.py
```

A successful live response is required before selecting or claiming the Tavily bonus on Devpost. Bonus readiness is not prize eligibility, and a successful API call is not earnings.

## Draft description

Earn Before Spend is a bounded economic agent built around one discipline: **prove value before asking for more capital**.

A user can supply possible earning opportunities directly, or the optional Tavily discovery layer can surface current candidates from the live web. Discovery never equals approval: every Tavily result remains unverified evidence until deterministic Python evaluates the option for upfront cash, owner labor, rights, eligibility, legitimacy, payout verification, urgency, and expected value. Blocked opportunities stay blocked even if their headline payout is huge.

The qualified ranking is then sent at runtime to NVIDIA Nemotron 3 Super on Nebius Token Factory. Nemotron is used where a large model is strongest: context, explanation, tradeoffs, and communicating the next bounded action. It is not allowed to reverse the deterministic gate or call hypothetical prizes, credits, owner deposits, loans, gifts, or test payments "earnings."

This architecture addresses a failure mode common to autonomous agents: models are very good at making possibilities sound actionable, but financial authority needs harder boundaries. Earn Before Spend separates discovery, reasoning, and authority, and escalates terms acceptance, identity/legal commitments, publication, and spending to a human.

## Demo plan (<3 minutes)

Use the Tavily segment only if the live runtime proof exists before recording. Otherwise keep the core Nebius/NVIDIA demo and do not claim the bonus.

1. **0:00–0:20 — Problem:** Show three opportunities with very different headline payouts. Explain that largest payout must not automatically win.
2. **0:20–0:45 — FIND (conditional Tavily bonus):** Run the bounded Tavily discovery probe and show live current candidates entering as `unverified_evidence_only`. If Tavily proof is not authorized, skip this segment and start with supplied candidates.
3. **0:45–1:15 — VERIFY + RANK:** Run the deterministic engine. Show candidates blocked or qualified based on objective constraints and the ranking output.
4. **1:15–1:55 — EXPLAIN:** Run `python nebius_smoke.py` using an authorized key. Show NVIDIA Nemotron 3 Super on Token Factory explaining the authoritative ranking, then show the sanitized evidence artifact proving the live call without exposing the key.
5. **1:55–2:25 — Safety proof:** Briefly show that Tavily cannot promote evidence to qualified status and Nemotron cannot re-rank or invent earnings; human-controlled terms/spending remain gated.
6. **2:25–2:45 — Tests:** Show adapter, evidence, judge-demo, Tavily, and submission-readiness tests passing without network usage by default.
7. **2:45–2:59 — Impact:** Starting capital $0; possible prizes are not counted as earned money; the product exists to reduce wasteful spend before validation.

## Judging-criteria mapping

### Technological implementation

Token Factory is in the actual runtime path rather than being mentioned in copy only. NVIDIA Nemotron explains a deterministic ranking that the model cannot override. The smoke-evidence path makes the qualifying call independently auditable without leaking credentials. If the Tavily bonus proof is completed, Tavily contributes a genuine runtime discovery tool in a multi-step agent workflow rather than a superficial one-off call.

### Design

The product has a coherent workflow: discover/enter opportunities → deterministic qualification → ranking → Nemotron explanation → human gate → bounded action → future payout reconciliation.

### Potential impact

Target users routinely spend on tools, ads, APIs, courses, or infrastructure before validating a revenue path. Earn Before Spend gives them a disciplined first-dollar workflow.

### Quality of idea

The non-obvious choice is **not** asking the model or search provider to decide what is economically safe. Search finds evidence, deterministic code decides what qualifies, and the open model handles ambiguity and communication.

## Bonus lanes

- **Most Valuable Feedback:** target this bonus only with truthful implementation/runtime feedback. The official rules list ten $100 awards plus NVIDIA swag for eligible submissions that complete the feedback section.
- **Best Use of Tavily:** **conditional target, implementation complete, runtime proof still gated**. Select/claim this lane only after `.tavily-evidence/search.json` has been produced by a real authorized Tavily call and the recorded demo shows Tavily participating in the solution.
- **City Winner:** do not claim without actual attendance at an eligible Builders & Brews city event.

## Tooling feedback draft

This draft is intentionally split between observations that are already supported by implementation work and runtime observations that must wait for the first authorized Token Factory call.

### What worked well during integration

Nebius Token Factory's OpenAI-compatible chat-completions interface made the integration unusually lightweight. Earn Before Spend could add Nemotron without replacing its deterministic Python core or introducing a provider-specific framework. The regional base URL and explicit NVIDIA model ID also make the qualifying runtime path easy to audit in source code.

The hackathon rules now clearly state that a runtime Token Factory inference call satisfies the "runs on Nebius" requirement for this track and that Serverless hosting is encouraged rather than mandatory. That clarity matters for existing applications that need to add a genuine Nebius/NVIDIA runtime path without migrating unrelated infrastructure just for eligibility.

### Highest-impact documentation/product improvements

1. Add a hackathon-oriented Token Factory quickstart that puts the regional base URL, current Nemotron model IDs, server-side environment-key pattern, one minimal chat-completions request, and a safe smoke-test pattern on one page.
2. Show a first-class example for bounded or safety-sensitive agents where deterministic policy remains authoritative and the model is used for explanation/planning. That would help builders avoid accidentally giving a generative layer authority over irreversible actions.
3. Make per-request usage/cost telemetry and project-level budget/cap guidance easy to find from the Token Factory quickstart. For zero-capital or cost-sensitive agents, being able to prove that a test cannot silently become uncapped usage is part of product safety, not just billing administration.
4. Include structured-output examples for Nemotron in the same quickstart so builders can validate machine-consumable action plans without reverse-engineering response conventions.

### Runtime observations still required before submission

Do **not** fabricate these. After the first human-authorized capped/free Token Factory call, add concise measured observations for:

- time to first/complete response for the exact Nemotron 3 Super call;
- whether the model obeyed the no-re-ranking / no-invented-earnings constraints;
- whether any error message, usage metadata, or response field was unclear;
- one concrete change that would most improve the next integration pass.

This preserves eligibility for the feedback bonus without turning preflight assumptions into fake product feedback.

## Evidence checklist

- [x] Public GitHub repository
- [x] Open-source MIT license
- [x] README setup/run guidance
- [x] Significant post-August-26 Nebius/NVIDIA code update staged
- [x] Nebius Token Factory runtime adapter implemented
- [x] NVIDIA Nemotron model explicitly selected
- [x] Offline adapter tests pass
- [x] One-command sanitized Nebius live-evidence capture implemented and gitignored
- [x] Tavily discovery adapter implemented with fail-closed human gate
- [x] One-command sanitized Tavily evidence probe implemented and gitignored
- [x] Devpost-required tooling feedback draft staged with unverified runtime claims clearly gated
- [x] Machine-readable submission readiness audit added (`python submission_readiness.py`)
- [ ] Human-authorized `NEBIUS_API_KEY` configured under a capped/free-credit route
- [ ] Real Token Factory + Nemotron runtime call captured in `.nebius-evidence/live-evidence.json`
- [ ] Human-authorized free or hard-capped Tavily credential approved (only if pursuing bonus)
- [ ] Real Tavily runtime call captured in `.tavily-evidence/search.json` (required before claiming bonus)
- [ ] Working demo/test URL prepared
- [ ] <3 minute public demo video uploaded
- [ ] Devpost project created/joined by human
- [ ] Feedback runtime-observation blanks completed truthfully
- [ ] Final submission reviewed and submitted by human

## Zero-capital scoreboard

Starting new seed capital: **$0.00**  
New cash spent: **$0.00**  
Verified external earnings: **$0.00**

Nebius credits, possible prizes, Tavily free credits, test calls, or pending awards do not count as earnings.
