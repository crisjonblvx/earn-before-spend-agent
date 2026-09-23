# Tavily bonus prep for Nebius x NVIDIA Global AI Hackathon

Status: preparation only. This does **not** accept Tavily or Devpost terms, create an account, provision paid resources, make a live third-party call, submit the hackathon, or claim prize eligibility.

Fresh rules check: September 23, 2026.

## Why this now improves expected value

The official Nebius x NVIDIA rules list **Best Use of Tavily: $3,000 cash** for an otherwise eligible submission that makes a functional runtime Tavily API call. The judges also say Best Apps and Agents entries stand out when they chain tools through a multi-step workflow rather than stopping at a single model call.

Tavily is not being bolted on only for a prize. It closes Earn Before Spend's missing **FIND** step:

1. Tavily discovers current candidate opportunities from live web sources.
2. Candidate results remain explicitly unverified evidence.
3. Deterministic Earn Before Spend rules verify and rank only opportunities whose economics, rights, eligibility, payout path, labor, and legitimacy are known.
4. NVIDIA Nemotron on Nebius Token Factory explains the bounded next action without overriding the deterministic gate.
5. Human-controlled terms, identity, payment, publication, and submission steps remain gated.

That creates a coherent **FIND -> VERIFY -> RANK -> EXPLAIN -> HUMAN GATE -> EARN** workflow.

## What is staged in this branch

- `tavily_discovery.py`: zero-dependency Search API adapter using the documented `POST https://api.tavily.com/search` endpoint.
- Double fail-closed runtime gate: both `ALLOW_LIVE_TAVILY=1` and `TAVILY_API_KEY` are required before any call.
- Basic Search only, maximum five results, no Tavily-generated answer, no raw page content, and no images. This bounds credit use and data collection.
- Every result is labeled `unverified_evidence_only`; Tavily results cannot bypass deterministic economic qualification.
- `tavily_probe.py`: one-call evidence path that writes a sanitized `.tavily-evidence/search.json` artifact.
- `.tavily-evidence/` is gitignored so keys or future raw evidence are not accidentally published.
- Offline tests cover the explicit human gate, auth header, bounded request body, normalization, evidence writing, and the max-results ceiling without calling Tavily.

## Human gate before the bonus becomes real

Only after a human approves the applicable Tavily terms and confirms a free or hard-capped credential may this run once:

```bash
ALLOW_LIVE_TAVILY=1 TAVILY_API_KEY="..." python tavily_probe.py
```

That is the only step that can turn this branch from **bonus-ready code** into actual runtime evidence for the $3,000 lane. A successful API response still does not guarantee bonus eligibility or prize money.

## Scoreboard boundary

Starting new seed capital: **$0.00**

New cash spent by this prep: **$0.00**

Verified external earnings: **$0.00**

Free API credits, hypothetical awards, and test results are not earnings.
