# Earn Before Spend — Amazon Build, Ship, Shape demo script

Target runtime: **2:20–2:40**  
Primary track: **Alexa+ simulated experience**  
Mini challenge: **Open Source**

## 0:00–0:15 — Hook

**Screen:** Open the simulated Alexa+ web app.

**Voiceover:**  
“Most assistants are designed to help you do more. Earn Before Spend is designed to stop you from spending money before the earning path is credible.”

## 0:15–0:35 — Architecture

**Screen:** Briefly show the UI labels: `$0 new cash`, `no device required`, `no paid API`, `human terms gate`.

**Voiceover:**  
“This is the official simulated Alexa+ path: a working web experience. The conversational layer explains decisions, but deterministic Python keeps authority over the money rules.”

## 0:35–1:05 — Positive request

**Screen:** Ask: `What is my best zero-capital earning move?`

**Voiceover:**  
“The assistant ranks only qualified paths. It returns the highest-scoring eligible move, tells me that third-party terms still require human approval, and explicitly refuses to count a possible prize as earned money.”

Pause long enough for the structured response to be visible.

## 1:05–1:40 — Safety proof

**Screen:** Click `Test the spend guardrail`.

Prompt shown: `Should I pay $99 to enter the $50,000 accelerator?`

**Voiceover:**  
“This is the point of the project. The $50,000 headline sounds better, but the mission starts with zero new capital. Because the accelerator requires ninety-nine dollars up front, the deterministic gate blocks it before payout size is considered. The assistant cannot talk itself around the rule.”

Show `requires_new_cash` and `eligible: false`.

## 1:40–2:00 — Code + tests

**Screen:** Show `alexa_sim.py`, then terminal:

```bash
python -m unittest test_alexa_sim.py -v
```

**Voiceover:**  
“The Amazon-specific contribution is open source and tested. The tests prove the paid-entry option stays blocked, the best move remains qualified, and human terms approval is preserved.”

## 2:00–2:20 — Existing-project truth boundary

**Screen:** Show the Amazon pull request.

**Voiceover:**  
“Earn Before Spend existed before this hackathon. The Alexa+ simulation, spend-refusal interaction, tests, feedback, and demo package are the new Amazon-period contribution. I’m not presenting the whole repo as newly built.”

## 2:20–2:35 — Close

**Screen:** Return to app.

**Voiceover:**  
“Earn Before Spend: before an assistant helps you spend faster, it should prove the earning path deserves the money.”

End card:  
`Starting capital: $0 | New cash spent: $0 | Verified external earnings: $0`
