# Demo Video Script

Target length: 2:30 to 3:30. Maximum allowed by the hackathon: 5:00.

## 0:00–0:20 — Hook / problem

**Visual:** Title card, then a simple screen showing subscriptions, ads, domains, tools, and “$0 revenue.”

**Voiceover:**

“Most people trying to make money online start by spending it. Another subscription. Another domain. Another ad campaign. Another AI tool. Earn Before Spend flips that sequence. The question is simple: can an agent help you find a legitimate path from zero new seed capital to verified positive cash contribution?”

## 0:20–0:40 — Who it is for

**Visual:** Creator, independent professional, small business, nonprofit/community organization labels.

**Voiceover:**

“It’s for creators, independent professionals, small businesses, and community organizations that need resourcefulness before they need another expense.”

## 0:40–1:05 — Architecture

**Visual:** Architecture diagram from `ARCHITECTURE.md`.

**Voiceover:**

“Strands Agents handles the reasoning and tool orchestration. But the model does not control the economic rules. Deterministic Python tools evaluate each opportunity for new cash requirements, owner labor, rights, eligibility, legitimacy, and payout verification. If a hard rule fails, the model cannot talk its way around it.”

## 1:05–1:45 — Working demo

**Visual:** Terminal.

Run:

```bash
python demo.py
```

Show the JSON ranking.

Then run:

```bash
python -m unittest test_core.py -v
```

**Voiceover:**

“Here are three candidate earning paths. The default demo runs without a model call, so the zero-capital premise is preserved. Each opportunity is passed through the deterministic gate before ranking. We also test the behavior directly: even a million-dollar opportunity cannot win if it requires new cash. Hidden owner fulfillment blocks a candidate. Unclear rights or payout verification block it too.”

## 1:45–2:20 — Strands behavior

**Visual:** `agent.py`, highlighting `@tool`, `evaluate_opportunity`, `rank_opportunities`, and the system policy. If a configured zero-cost Strands provider is available, show a real `RUN_STRANDS=1 python demo.py` response. If not, show code + deterministic run only and do not pretend a model was invoked.

**Voiceover:**

“The Strands agent has two tools: one to qualify an opportunity and one to rank up to three candidates. The model explains tradeoffs and recommends the next bounded action, but consequential steps like accepting third-party terms, making legal representations, publishing private code, or spending money are surfaced to the human.”

## 2:20–2:50 — Why it matters

**Visual:** Scoreboard animation:

- Starting capital: $0
- Possible opportunity: not earnings
- Test payment: not earnings
- Owner deposit: not earnings
- Verified payout minus real costs: earnings

**Voiceover:**

“The design makes one distinction that autonomous agents need badly: possible money is not money. Credits are not earnings. Owner deposits are not earnings. A prize you might win is not earnings. Success only happens after a trusted payout is reconciled against the real costs.”

## 2:50–3:15 — Close

**Visual:** Earn Before Spend logo/title + architecture.

**Voiceover:**

“Earn Before Spend is an experiment in economically responsible autonomy. Instead of giving an agent a budget and hoping it creates value, we ask it to prove value before asking for more capital. Find the opportunity. Respect the rules. Escalate the consequential decision. Verify the money. Then learn and repeat.”

## Recording notes

- Keep the terminal font large enough for judges to read.
- Do not show private repositories, API keys, browser bookmarks, customer data, or Bonita/BLVX internals.
- If a real Strands model run is not available under a verified zero-new-cash route, say so plainly. The deterministic demo still demonstrates the tool logic, but the final submission should ideally include a real Strands invocation because Strands usage is a primary judging criterion.
- Upload final video publicly to YouTube or Vimeo before submission.
