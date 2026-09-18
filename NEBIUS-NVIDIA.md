# Nebius x NVIDIA Global AI Hackathon adaptation

This branch adapts the existing **Earn Before Spend** prototype to the Nebius x NVIDIA Global AI Hackathon without changing its core zero-capital safety model.

## Track fit

Primary fit: **Best Apps and Agents**.

Earn Before Spend is a bounded agent for creators, independent professionals, small businesses, and community organizations. It evaluates earning paths, rejects options that require new cash or unclear rights/eligibility, ranks the remaining options, and surfaces legal/identity/terms decisions to a human.

The deterministic Python gate remains authoritative. NVIDIA Nemotron is used for the reasoning/explanation layer, so the model can explain tradeoffs and pick the smallest bounded next action but cannot override economic blockers.

## Material update during the submission period

The project existed before the Nebius submission period. The significant hackathon-period update on this branch is a new **Nebius Token Factory inference path using NVIDIA Nemotron 3 Super**, plus offline tests, a sanitized live-evidence command, and judge-ready setup documentation. The original Strands/AWS path remains intact for provenance; the Nebius adapter is additive.

Files added/changed for this adaptation:

- `nebius_agent.py` — OpenAI-compatible Token Factory client using `nvidia/nemotron-3-super-120b-a12b`.
- `nebius_smoke.py` — one-command live smoke run that prints judge-safe evidence without exposing the API key.
- `test_nebius_agent.py` — network-free tests proving deterministic blockers survive into the model context and the Nemotron route is selected.
- `README.md` — setup/run instructions and explicit Nebius/NVIDIA architecture for judging.
- `requirements.txt` — adds the OpenAI-compatible Python client used by Token Factory.

## Run locally

Install dependencies, then run the provider-free demo and offline tests:

```bash
pip install -r requirements.txt
python demo.py
python -m unittest test_core.py test_nebius_agent.py -v
```

A live Nebius run requires an existing, approved Token Factory API key. No resource is provisioned by this repository.

```bash
export NEBIUS_API_KEY="..."
python nebius_smoke.py
```

The smoke command performs one live Nemotron completion and prints a sanitized record containing the provider, model, endpoint host, UTC completion time, deterministic-context hash, completion hash, and completion text. It does not print the API key.

Optional environment overrides:

```bash
export NEBIUS_MODEL="nvidia/nemotron-3-super-120b-a12b"
export NEBIUS_BASE_URL="https://api.tokenfactory.us-central1.nebius.com/v1/"
```

## Submission evidence to capture after the human key gate

1. Run the offline tests.
2. Run `python nebius_smoke.py` with `NEBIUS_API_KEY` configured.
3. Preserve the sanitized output as proof of one observed Token Factory/Nemotron call.
4. Record a <=3 minute public YouTube demo showing the project functioning and explaining that Token Factory hosts the NVIDIA Nemotron reasoning layer while deterministic Python retains final economic eligibility authority.
5. Provide the public repository URL, MIT license, README setup steps, and this material-update explanation.
6. Include honest product feedback on Nebius Token Factory/Nemotron based only on the observed live run.

## Truth boundary

Do not claim verified earnings unless an actual external payout clears. Do not claim a successful Nebius run until `nebius_smoke.py` completes against Token Factory. Do not expose API keys in screenshots, terminal history, GitHub, or Devpost fields. A successful smoke record proves one model call only; it is not evidence of earnings, payout, scale, or contest acceptance.
