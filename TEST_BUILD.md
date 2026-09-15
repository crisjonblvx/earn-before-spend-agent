# Judge test build

## Run without credentials or package installation

1. Download this branch using GitHub **Code → Download ZIP**, or clone `bonita/nebius-nemotron-adapter`.
2. Unzip, open a terminal in the project folder, and run `python3 web_demo.py`.
3. Open http://127.0.0.1:8765 in your browser. Python 3.10+ is required.

The server listens only on your own computer. This is a downloadable test build, not a hosted production service. It uses the actual Python gate, not a JavaScript reimplementation. It does not call a model or accept secrets in the browser.

## Demo sequence

- Initially the owned automation pack qualifies, with human approval required. The paid-entry contest and unverifiable bounty fail.
- Set new cash to $25 and evaluate: all candidates fail.
- Restore $0, set owner fulfillment to 31 minutes: the owned pack fails the labor gate.
- Restore 5 minutes and select unverified payout: it fails the evidence gate.
- Restore verifiable payout: the pack qualifies again. The verified earnings ledger stays at $0.
- Expand the decision record to inspect the actual Python output.

All sample opportunities and numerical assumptions are illustrative; no external offers or earnings are being claimed.

## One real Nebius request (optional, blocked by default)

Only after the operator has accepted the appropriate provider terms, verified sufficient promotional credits and confirmed paid usage is disabled:

```sh
export ALLOW_LIVE_NEBIUS_TEST=YES
export NEBIUS_PROMO_COVERAGE_CONFIRMED=YES
# Set NEBIUS_API_KEY privately in the environment. Never put it in Git or video.
python3 nebius_once.py
```

This uses Python's standard library: one HTTPS request, no retry, no redirect, no Strands loop, a 45-second timeout and a requested 350-output-token cap. This is a request limit, not a provider-side dollar cap; the credit/billing verification is essential. The local lock prevents a second attempt, including after timeout. After any failure, inspect the provider console before manually clearing `evidence/nebius-request.lock` because a timed-out request may still have consumed credits.

The evaluator sends only fixed illustrative Python results and a bounded explanation prompt to NVIDIA Nemotron 3 Super via Nebius Token Factory. It records model output, finish reason, latency and usage in ignored, mode-0600 `evidence/nebius-run.json`. Inspect it locally and refresh the demo to view the recorded explanation. No response is fabricated when inference is pending or failed. Human review must check the explanation against the deterministic result. A truncated answer is not a passing behavioral evaluation.

This path validates model explanation of precomputed decisions. It does not establish autonomous Strands tool-use performance. The original optional Strands agent is separate and can make multiple model calls; do not use it for the strict one-request experiment.

## Validation

```sh
python3 -m unittest discover -v
python3 -m unittest discover -s tests -v
```

The mocked network tests do not prove runtime NVIDIA/Nebius use. Complete the authorized real test and firsthand feedback before entering final competition claims.

## Remaining submission gates

- Successful live Nebius inference, output review and credit reconciliation.
- Public YouTube video of no more than 3 minutes demonstrating the working model integration with audio. The local deterministic walkthrough is an interim review asset, not that final video.
- Submitter demographics and exact pre-August-26 project-history answer.
- Final competition terms and submission by the owner.
