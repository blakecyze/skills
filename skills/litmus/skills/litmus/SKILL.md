---
name: litmus
description: Run a focused QA pass during feature verification or when asked to test a web or mobile flow, check regressions, or assess release readiness. Plan, execute, or repair within scope, with results tied to observed behaviour; visual restyling alone belongs elsewhere.
---

# Litmus

Find consequential failures with the smallest useful set of checks, and say exactly what the evidence establishes.

## Controls

`[scope] [plan|check|fix] [focus]`

Infer scope from the current feature, flow, or change. `plan` recommends checks without running them. Testing and review requests use `check`: exercise the target without editing product code or weakening tests. An explicit repair request uses `fix`: reproduce, repair, then verify. Focus such as `smoke`, `regression`, `web`, `mobile`, or `release` narrows the pass. These controls are optional; use ordinary language and existing task context.

## Pass

Identify the expected result, build or revision, environment, and relevant starting state. Infer expectations from the brief, product contract, and existing tests. Do not silently treat current behaviour as correct when it is the subject of the report. Resolve ambiguity only when it changes the test or verdict.

Choose checks by changed behaviour and consequence: the primary journey, likely failure or recovery, and adjacent regression risks. Reuse existing deterministic tests when they answer the question. Add live interaction or bounded exploration for gaps those tests cannot cover. A broad pass need not exhaust every screen, browser, or device.

Load only the relevant detail:

| Work | Reference |
|---|---|
| Selecting tests, planning regression or release coverage | [coverage.md](references/coverage.md) |
| Browser journeys and meaningful automation | [web.md](references/web.md) |
| Mobile journeys and device-dependent claims | [mobile.md](references/mobile.md) |
| Observations, bug reports, and coverage limits | [evidence.md](references/evidence.md) |

Use the available project runner and tools; do not replace a working stack merely to standardise on a favourite. Verify unfamiliar commands against installed help or current official documentation. Use an existing test environment and disposable data where available. A QA request does not itself authorise purchases, public messages, production deletion, or resets of shared accounts and devices.

Compare an observed result with the expected outcome. A command completing or a screen appearing does not prove the whole journey succeeded. Preserve initial failure evidence before retrying. If an environment failure blocks the check, report that gap and continue independent useful checks; do not mislabel the product as passing or broken.

In fix mode, establish the cause, make the scoped repair, rerun the failing case and relevant regression checks. Do not lower an assertion or replace a visual baseline merely to obtain green. Intermittent failures may warrant `litmus-flakes` when installed; routine QA does not depend on it.

Stop when requested checks are covered or further progress needs unavailable evidence. Report failures, verified coverage, and unresolved risks separately. A scoped pass is not a claim that the application has no defects, and a readiness assessment does not deploy or approve a release automatically.
