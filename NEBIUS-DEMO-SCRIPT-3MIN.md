# Nebius x NVIDIA 3-Minute Demo Lock

Hard cap: **3:00**. Target: **2:50–2:55**.

0:00–0:18 — Problem: show three earning opportunities and explain the zero-new-capital objective.

0:18–0:43 — Run `python demo.py`. Show deterministic qualification and ranking. State that the model cannot override the economic gate.

0:43–1:10 — Run `python judge_demo.py`. Show the working browser surface and that live inference is double-gated.

1:10–1:48 — Show `nebius_model.py` and the qualifying runtime path: Nebius Token Factory + NVIDIA Nemotron 3 Super (`nvidia/nemotron-3-super-120b-a12b`). If an authorized bounded credential exists, run:

```bash
ALLOW_LIVE_NEBIUS=1 NEBIUS_API_KEY="..." python hackathon_conversion_probe.py
```

Show only the sanitized evidence artifact, never the key. If no live proof exists yet, do not fake this segment.

1:48–2:12 — Show a blocked high-payout candidate and the human gate for terms, identity/legal attestations, money movement, publication, and paid resources.

2:12–2:32 — Run `python -m unittest discover -v` and `python submission_readiness.py`.

2:32–2:52 — Scoreboard: starting capital $0; new cash spent $0; possible prize is not earnings; verified external payout minus real costs is earnings.

2:52–2:58 — Close: “Find. Verify. Rank. Explain. Human gate. Earn.”

Recording requirements:
- final public YouTube video must be under 3:00;
- show the working project, not only slides;
- explicitly name Nebius Token Factory and NVIDIA Nemotron 3 Super;
- never show API keys, private data, or private Bonita/BLVX material;
- do not claim live Token Factory usage until sanitized runtime evidence exists;
- leave Tavily out unless a real authorized Tavily runtime call has been captured.
