# Time Estimate — Sergio's Active Work

## Bottom line

A credible submission is **10–13 hours of active human work**, plus **4–8 hours of Codex/deployment wall-clock time** that can run with intermittent supervision. Add a two-hour contingency for Indigo import or deployment problems.

Claiming this can be finished properly in four or five personal hours would be fantasy. The video, manual agent configuration, adversarial testing, and README judgment alone consume most of that.

## Active human estimate

| Phase | Sergio active time | What you personally do |
| --- | ---: | --- |
| Read and approve specifications | 0.5–0.75 h | Confirm scope, non-goals, architecture, and success criteria. |
| CSV/data mapping review | 0.5–0.75 h | Inspect real examples; approve ID, category, currency, price, stock, and missing-data rules. |
| Codex milestone review | 1.0–1.5 h | Review plans/diffs/OpenAPI, answer gates, reject scope creep, verify decisions. |
| API and OpenAPI QA | 0.75–1.0 h | Read schema as an LLM, run local smoke calls, inspect error/recovery behavior. |
| Git/Render deployment | 0.5–1.0 h | Create/connect service, set secret, deploy, verify HTTPS and cold start. |
| Indigo configuration | 1.25–1.75 h | Tool Collection, secret header, global settings, Product Discovery, fallback, Welcome, Web Chat. |
| Manual adversarial testing/tuning | 1.5–2.25 h | Run P0/P1 matrix, inspect tool arguments, change prompts/descriptions, rerun. |
| README personalization | 0.75–1.0 h | Rewrite AI method, real misstep, client challenge, non-goals, measured time. |
| Video preparation and recording | 1.5–2.25 h | Replace placeholders, prepare tabs, dry run, record, trim, upload, access check. |
| Final QA and submission | 0.5–0.75 h | Secret scan, dead links, signed-out access, final published spot checks. |
| **Total active human time** | **8.75–13.0 h** | Plan for **10–13 h**, not the optimistic minimum. |

## Non-human / waiting time

| Activity | Wall-clock estimate | Attention needed |
| --- | ---: | --- |
| Codex implementation and repair loops | 3–6 h | Check at human gates and after test failures. |
| Render builds/redeploys | 0.5–1.5 h | Mostly waiting; verify each result. |
| Indigo iteration latency | 0.5–1.0 h | Included partly in manual testing. |
| Video upload/processing | 0.25–1.0 h | Access check after processing. |

## Recommended three-day schedule

### Day 1 — Truth layer and contract

Personal time: 3–4 hours.

1. Review spec and CSV mapping.
2. Start Codex inspection-only phase.
3. Approve mapping.
4. Let Codex implement milestones 2–5.
5. Review the OpenAPI and reject ambiguity before deployment.

End-of-day gate: tests and OpenAPI pass locally. No Indigo work yet.

### Day 2 — Deployment and Indigo

Personal time: 3–4.5 hours.

1. Final backend QA.
2. Deploy to Render and run smoke tests.
3. Import Tool Collection and configure Indigo Draft.
4. Run the full P0 matrix once.
5. Fix defects at the correct layer.

End-of-day gate: all P0 scenarios can pass; agent still need not be published.

### Day 3 — Evidence and presentation

Personal time: 3–4.5 hours.

1. Rerun P0 twice after the last change.
2. Publish and spot-check.
3. Rewrite README personal sections.
4. Replace video placeholders with real evidence.
5. Dry run, record, upload, verify links, submit.

## Time log to keep from the first minute

Create a simple table in your notes:

| Date | Phase | Human active minutes | Codex/waiting minutes | Decision or output |
| --- | --- | ---: | ---: | --- |

At submission, report:

- human active time;
- AI-assisted implementation wall time;
- elapsed calendar time;
- the major phases.

This is more credible than one vague number and directly supports the README requirement.

## Contingency rule

If more than two hours are lost to deployment or Indigo issues, cut bonuses immediately. Never cut:

- OpenAPI review;
- stock/budget tests;
- out-of-scope tests;
- README personal evidence;
- video dry run.
