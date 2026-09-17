# Nebius x NVIDIA Global AI Hackathon adaptation

This branch adapts the existing **Earn Before Spend** prototype to the Nebius x NVIDIA Global AI Hackathon without changing its core zero-capital safety model.

## Track fit

Primary fit: **Best Apps and Agents**.

Earn Before Spend is a bounded agent for creators, independent professionals, small businesses, and community organizations. It evaluates earning paths, rejects options that require new cash or unclear rights/eligibility, ranks the remaining options, and surfaces legal/identity/terms decisions to a human.

The deterministic Python gate remains authoritative. NVIDIA Nemotron is used for the reasoning/explanation layer, so the model can explain tradeoffs and pick the smallest bounded next action but cannot override economic blockers.

## Material update during the submission period

The project existed before the Nebius submission period. The significant hackathon-period update on this branch is a new **Nebius Token Factory inference path using NVIDIA Nemotron 3 Super**, plus offline tests and run documentation. The original Strands/AWS path remains intact for provenance; the Nebius adapter is additive.

Files added/changed for this adaptation:

- `nebius_agent.py` — OpenAI-compatible Token Factory client using `nvidia/nemotron-3-super-120b-a12b`.
- `test_nebius_agent.py` — network-free tests proving deterministic blockers survive into the model context and the Nemotron route is selected.
- `requirements.txt` — adds the OpenAI-compatible Python client used by Token Factory.

## Run locally

The default project demo is still provider-free:

```bash
python demo.py
python -m unittest test_core.py test_nebius_agent.py -v
```

A live Nebius run requires a human-created Token Factory API key. No resource is provisioned by this repository.

```bash
export NEBIUS_API_KEY="..."
python - <<'PY'
from demo import sample_opportunities
from nebius_agent import run_nebius
print(run_nebius(sample_opportunities()))
PY
```

Optional environment overrides:

```bash
export NEBIUS_MODEL="nvidia/nemotron-3-super-120b-a12b"
export NEBIUS_BASE_URL="https://api.tokenfactory.us-central1.nebius.com/v1/"
```

## Submission evidence to capture after the human key gate

1. Run the offline tests.
2. Run the live Nemotron path with `NEBIUS_API_KEY` configured.
3. Capture terminal output showing the deterministic ranking plus the bounded Nemotron recommendation.
4. Record a <=3 minute public demo explaining that Token Factory hosts the NVIDIA Nemotron reasoning layer while deterministic Python retains final economic eligibility authority.
5. Provide the public repository URL, MIT license, setup steps, and this material-update explanation.

## Truth boundary

Do not claim verified earnings unless an actual external payout clears. Do not claim Nebius deployment until a successful live Token Factory call has been observed. Do not expose API keys in screenshots, terminal history, GitHub, or Devpost fields.
