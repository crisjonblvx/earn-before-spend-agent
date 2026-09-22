# Amazon Build, Ship, Shape — product feedback + friction log

This file is submission preparation only. It records feedback from the implementation path actually used and does not claim access to Alexa+ Preview, a live Alexa+ runtime, or an Amazon device.

## Product feedback

### Path used

Official Alexa+ **simulated experience** route: a working web app using the project's own deterministic agent logic.

### What worked well

The simulated route is a strong onboarding bridge. It gives builders a compliant way to prove interaction design and agent behavior without hardware or Preview-only access.

The repository requirement is also valuable: it forces a simulated entry to be inspectable and runnable, not only narrated in a video.

### What needs work

The simulated route would benefit from a single dedicated quickstart that combines:
- the exact eligibility wording;
- a minimal runnable example;
- the evidence judges expect in the video;
- guidance on labeling a simulation so it is not confused with live Alexa+ integration;
- a short checklist for Devpost fields.

### Onboarding

Once the simulated option is found in the requirements, implementation is lightweight. The uncertainty is primarily interpretive rather than technical: understanding what a compliant simulated experience needs to show.

### Would we build with it again?

Yes. Simulation-first is a good way to validate whether a conversational workflow deserves deeper platform investment.

## Optional friction log

**Task:** Find the lowest-cost compliant Alexa+ track route for an existing agent.

**Steps taken:** Read the official overview, Alexa+ track requirements, repo requirements, demo requirements, and judging criteria.

**Expected:** One simulation-focused starter with minimum architecture plus submission evidence.

**Observed:** The simulation path is clearly allowed, but its guidance is embedded inside broader track requirements.

**Severity:** Medium-low.

**Workaround:** Built a self-contained, zero-dependency web simulation labeled explicitly as simulated Alexa+ and paired it with tests and a submission checklist.

**Suggestion:** Publish a “Simulated Alexa+ in 15 minutes” starter plus a sample Devpost evidence block.
