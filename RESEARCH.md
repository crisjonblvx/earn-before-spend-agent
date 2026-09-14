# Beyond the first dollar: zero-capital agent research

## Status and scope

**The R&D instrumentation described here is an active research direction; not all telemetry and comparative-learning features are implemented in the current hackathon prototype.**

This document describes the research protocol for the current two-agent zero-capital experiment and the intended next phase of Earn Before Spend. It is not a results report, proof of live scheduling, or a claim that this repository runs both agents.

The public prototype implements deterministic opportunity qualification and ranking, a Strands agent wrapper, and a demonstration with guardrail tests. It accepts supplied candidates; it does not implement an autonomous search service, external transaction execution, payout reconciliation, persistent research ledgers, scheduled reports, or comparative learning. The wrapper cannot spend, submit, sign, or accept third-party terms. Research activities outside this repository must be evidenced separately.

## Current experiment

Two separately operated agents, **Bonita** and **GPT**, pursue the same question:

> How effectively can an agent turn $0 in new seed capital into verified economic value using legitimate opportunities and resources already available?

Both operate under a zero-new-seed-capital constraint. They may propose new products or reuse authorized existing products, content, tools, and workflows. Reuse is evaluated alongside new creation; novelty alone is not success. Candidate pathways include bounties, competitions, services, licenses, digital products, affiliate commissions, and grants or awards.

Zero new cash does not mean zero economic cost. Record existing subscriptions, compute, infrastructure, asset usage, and human time even when already paid for. A potential prize, acceptance, invoice, credit, test payment, owner deposit, loan, or gift is not verified earnings. Any later reinvestment must be separately authorized and recorded; it must not silently change the experiment's starting constraint.

Each agent discovers, evaluates, and records its decisions independently before comparative review. Human decisions remain necessary for terms, identity, legal commitments, publication, and money movement. The protocol does not authorize access to private assets or consequential actions.

## Research architecture

**Discover → Evaluate → Act → Verify → Learn → Research Ledger**

- **Discover:** identify opportunities and record search coverage, including runs with no useful candidates.
- **Evaluate:** apply eligibility gates and record estimates, choices, and rejection reasons before outcomes are known.
- **Act:** record a concrete attempt and any human decision required. A recommendation or draft alone is not an external attempt.
- **Verify:** establish outcomes from evidence and reconcile cash and costs; preserve pending or unknown states.
- **Learn:** connect a result to an explicit lesson and check whether a later decision applies it.
- **Research Ledger:** retain dated observations and comparisons so that claims can be audited over time.

This is the proposed end-to-end research workflow. The current prototype principally supports Evaluate; the remaining stages require operational processes or future implementation.

## Three ledgers

| Ledger | Intended contents | Independence rule |
| --- | --- | --- |
| Bonita Ledger | Bonita's runs, candidates, rejections, decisions, attempts, interventions, costs, outcomes, and lessons | Record decisions before viewing the other agent's results. |
| GPT Ledger | GPT's runs, candidates, rejections, decisions, attempts, interventions, costs, outcomes, and lessons | Use the same schema and accounting rules, with separate attribution. |
| Shared Research Ledger | Deduplicated comparisons, patterns, failures, intervention rates, economic summaries, hypotheses, and protocol changes | Compare recorded observations; label any lesson or opportunity subsequently shared with either agent. |

These are logical ledger specifications, not databases supplied by this repository. Keep corrections as dated amendments linked to the original record. A shared opportunity receives one canonical ID and agent-specific observations. Count a payout once in systemwide totals; record any attribution split rather than crediting the full amount to both agents.

## Research instrumentation to track

Use one run record, linked opportunity observations, and dated action/outcome updates. The following fields are proposed additions to a research dataset; some opportunity inputs and evaluation outputs already exist in `core.py`, but persistent telemetry does not.

| Field group | Fields to record |
| --- | --- |
| Identity and timing | Agent, run ID, opportunity ID, protocol version, model/tool configuration where disclosable, scheduled time, actual start/end time, UTC timestamp, reporting timezone |
| Discovery | Sources searched, source categories, queries or sanitized search strategy, search duration, opportunities inspected, unique candidates, duplicates, empty runs, errors, missed runs |
| Opportunity | Public source URL, first seen, last confirmed available, first confirmed unavailable, deadline, pathway type, eligibility and rights evidence, payout terms |
| Judgment | Expected payout and currency, payout probability, estimate rationale and uncertainty, expected time-to-cash, legitimacy, fit, rank, selected/rejected/deferred state |
| Rejections | Rejection reason such as hidden cost, unclear rights, ineligibility, weak payout evidence, expiration, saturation, or excessive owner labor; supporting evidence |
| Creativity and resources | Existing asset considered or reused using a safe alias, new idea generated, whether a pathway was prompted or independently proposed, reuse rationale |
| Human involvement | Intervention required, type and reason, estimated owner minutes, actual CJ/other human minutes, decision and timestamp, waiting time |
| Costs | New cash consumed, existing-resource use, attributable compute/subscription/infrastructure cost, transaction fees, refunds, reserves, labor rate, allocation method, currency, measured/estimated/unknown status |
| Execution | Action proposed, action actually taken, attempt ID and timestamp, approval reference if needed, preparation versus submission/delivery status |
| Outcome and money | Pending/no response/rejected/accepted/delivered/paid/refunded status, verification date, restricted evidence reference, verified revenue, verified net earnings, net contribution |
| Learning | Lesson ID, triggering evidence, proposed strategy change, next run that used or did not use the lesson, observed behavior change, result, exposure to shared research |

Do not replace missing information with zero. Preserve estimates separately from observed values. Log failures and rejected opportunities as well as successes to reduce survivorship bias. Store concise decision rationales, not private prompts or hidden reasoning traces.

## Key research questions and measures

| Question | Proposed measure |
| --- | --- |
| **Creativity:** does an agent find pathways it was not explicitly given? | Share of unique candidates with independently proposed pathways; record the prior suggestions and apply a consistent human review rubric. |
| **Resourcefulness:** does it make effective use of available resources? | Share of attempts reusing authorized assets, preparation time, attributable costs, and verified outcomes compared with new creation. |
| **Economic judgment:** are its estimates useful? | Compare pre-action payout probabilities and time-to-cash estimates with resolved outcomes; distinguish high potential prizes from likely near-term cash. |
| **Independence:** how much human help is required? | Intervention count and human minutes per attempt and per verified dollar earned. Mark per-dollar measures undefined when no revenue is verified. |
| **Learning velocity:** does failure change later behavior? | Elapsed time and number of runs from a documented lesson to its first evidenced application; then track whether outcomes improve. A written lesson alone is not demonstrated learning. |
| **Search diversity:** do agents converge or explore different paths? | Distribution across source categories and pathways; overlap of canonical opportunity IDs within the same observation window. |
| **Opportunity half-life:** how quickly does a discovered option disappear? | Estimate time from discovery until half of a discovery cohort is confirmed unavailable; record last available/first unavailable bounds, observation gaps, and still-open cases. If fewer than half close, report half-life as not yet observed. |
| **Execution ratio:** how often does discovery become action? | Unique opportunities with at least one actual attempt / unique opportunities identified in the cohort. Also report attempts / qualified opportunities to expose the effect of filtering. |
| **Conversion:** where does progress stop? | Track attempt → acceptance → delivery → verified payout, reporting numerator, denominator, and elapsed follow-up at each applicable stage. Label non-applicable stages for pathways with different workflows. |
| **Autonomous Economic Efficiency:** what value results from the resources used? | Verified Net Earnings / (Agent Resource Cost + Human Labor Cost), using the accounting rules below. |

### Autonomous Economic Efficiency

```text
Autonomous Economic Efficiency = Verified Net Earnings / (Agent Resource Cost + Human Labor Cost)
```

For this protocol, use one declared reporting period and currency:

- **Verified revenue:** actual externally earned payouts supported by trusted evidence, excluding hypothetical value and non-earning inflows.
- **Verified Net Earnings:** verified revenue less fees, refunds, reserves, and other direct fulfillment costs, excluding costs assigned to the two denominator categories below.
- **Agent Resource Cost:** attributable model, search, compute, subscription, infrastructure, and existing-resource costs, including allocated prepaid resources. Record the allocation method and distinguish estimates from measured costs.
- **Human Labor Cost:** actual human minutes / 60 × a declared hourly rate. Count research, supervision, approvals, fulfillment, and intervention time; disclose any excluded time.
- **Net contribution after all costs:** Verified Net Earnings − Agent Resource Cost − Human Labor Cost. Report this alongside the ratio and the separate new-cash-spend ledger.

Assign each cost once. The ratio compares net receipts before agent/labor costs with those costs; a value of 1 means those costs are covered, not that the project made additional profit. If the denominator is zero, report **undefined**, not infinity. If required cost or payout data is unknown, report **not yet measurable**, not a fabricated score. Keep losses visible. For aggregate reports, divide summed earnings by summed costs rather than averaging per-run ratios.

Report sample size, unresolved outcomes, cost assumptions, and follow-up duration alongside all comparisons. This document makes no earnings or performance claims.

## Intended cadence

| Frequency | Research activity |
| --- | --- |
| Hourly per agent | Each agent independently searches, evaluates, and records a run. |
| Staggered 30 minutes systemwide | Target Bonita at `:00` and GPT at `:30`, yielding one scheduled observation every half-hour. |
| Daily rollup | Summarize coverage, candidates, rejections, attempts, interventions, cash, resource use, outcomes, missing data, and pending follow-ups. |
| Weekly analysis | Compare behavior and outcomes, test emerging hypotheses, and document any strategy or protocol changes. |
| Monthly report | Produce an economic and behavioral report with verified results, costs, efficiency, limitations, and research questions for the next period. |

This is the intended operating rhythm, not a scheduler implemented or verified by this documentation. Actual starts, failures, limits, and missed runs must be recorded. Do not treat scheduled slots as completed observations. Daily, weekly, and monthly boundaries should use a declared reporting timezone while raw timestamps remain in UTC.

## Comparison limits and learning controls

Two agents are an exploratory longitudinal comparison, not a controlled study that establishes general superiority. Different models, tools, access, human support, and the 30-minute timing offset can affect results. Track these conditions and compare matched pathways and discovery cohorts with comparable follow-up periods.

Keep initial decisions independent. Release shared lessons only at documented review points, record which agent saw them and when, and distinguish independent discovery from shared-learning phases. Do not silently rewrite earlier estimates after an outcome or describe correlation as a causal improvement. Short observation windows and delayed payouts require explicit pending states.

## Public/private boundary

This public repository documents a standalone prototype and a research direction. It does not publish or require private Bonita/BLVX source code, prompts, internal architecture, proprietary datasets, credentials, customer information, personal identifiers, payment details, or private operational logs.

Keep raw ledgers and payout evidence in appropriately restricted storage. Public reporting should use reviewed aggregates, sanitized examples, safe asset aliases, and non-sensitive evidence summaries. Bonita and GPT are participant labels, not disclosure of their private implementations. No live ledger data or private implementation material is included with this protocol.
