# Nebius x NVIDIA Submission Readiness

Deadline: **October 30, 2026 at 10:00 AM PDT**.

## Verified complete on this branch

- [x] Public repository: https://github.com/crisjonblvx/earn-before-spend-agent
- [x] MIT license visible in the repository
- [x] README includes setup and run instructions
- [x] Pre-existing-project disclosure drafted in `DEVPOST-NEBIUS.md`
- [x] Nebius Token Factory runtime integration implemented
- [x] NVIDIA Nemotron 3 Super configured as the default NVIDIA open model
- [x] Deterministic economic guardrails remain authoritative
- [x] Missing credentials fail closed before network activity
- [x] Mocked Token Factory integration tests pass
- [x] Zero-provider-call demo remains runnable without credentials
- [x] Repository CI compiles sources, runs tests, and runs the deterministic demo without provider inference
- [x] `nebius_live_evidence.py` reduces the first live-inference gate to one bounded command and writes only sanitized evidence to a gitignored local artifact
- [x] Live-evidence tests verify missing-key fail-closed behavior, exactly one injected inference call, evidence hashing, atomic persistence, and secret exclusion without consuming provider credits

## Next technical gate

With an already-approved, bounded Nebius Token Factory credential configured locally, run exactly:

```bash
NEBIUS_API_KEY='...' python nebius_live_evidence.py
```

A successful run will perform one Nemotron completion, print a sanitized record, and write `.nebius-evidence/live-evidence.json`. The file contains provider/model/endpoint host, UTC completion time, hashes of the deterministic context and model completion, the completion text, and an explicit truth boundary. It never writes the API key.

After that evidence exists, use the observed Token Factory/Nemotron behavior to complete the feedback paragraph, confirm judge-facing run instructions, record the under-three-minute YouTube demo, and supply a working demo/test-build URL. Those later artifacts must describe only behavior actually observed.

## Final human gates

- [ ] Review eligibility and official rules.
- [ ] Accept any required Devpost / sponsor terms personally.
- [ ] Make any required identity, tax, residency, or legal attestations personally.
- [ ] Submit the Devpost entry before the deadline.

## Evidence boundary

Do not claim the Nebius integration is live-tested until `.nebius-evidence/live-evidence.json` is created by a successful real Token Factory call. Do not count prizes, credits, test activity, owner deposits, or pending awards as verified earnings.

## Zero-capital scoreboard

Starting new seed capital: **$0.00**  
New cash spent: **$0.00**  
Verified external earnings: **$0.00**
