---
name: litmus-flakes
description: Investigate intermittent test failures, order dependence, timing races, and environment instability. Use to reproduce or repair flakes and assess quarantine; a deterministic product failure belongs in ordinary debugging or QA.
---

# Litmus flakes

Find why the same expectation sometimes fails. Preserve the failure before trying to make the run green.

## Establish the variation

Collect the test, build or revision, runner configuration, initial state, failing assertion, and available successful and failed artifacts. Mixed results at one revision identify intermittency, not its cause: product races, shared data, infrastructure, and the test itself are all candidates.

Infer investigation versus repair from the request. Investigation stays read-only apart from running scoped tests and collecting evidence. Repair may change the responsible code or test but must preserve the behaviour being asserted.

## Isolate the cause

Reproduce with a bounded run or experiment chosen to distinguish hypotheses. Start with the failing test and relevant setup rather than looping the whole suite. Stop repeated runs that add no evidence; report attempts and conditions, not a selectively green sample.

Compare one meaningful variable at a time: isolated versus suite order, serial versus parallel, fresh disposable data versus reused state, local versus CI configuration, or real versus controlled time/network. Preserve comparability of build and expectation.

Trace the failure to its owning layer. Check readiness signals, stale locators, animation interruption, leaked state, data collisions, unseeded randomness, service responses, resource contention, and device health only where evidence points. A longer sleep or blanket retry does not establish a cause.

## Repair or contain

Prefer a real readiness condition, isolated data, controlled nondeterminism, or a product race fix. Do not silently weaken assertions, swallow errors, disable coverage, or refresh a baseline to hide the symptom.

Quarantine changes coverage and may change a merge gate. Apply it only when that change is authorised and consistent with project policy; otherwise recommend it. Preserve the failing case and record the known impact, ownership if established, and condition for restoring coverage. Do not invent a ticket, owner, deadline, or blanket retry limit. Report any retries already performed.

Re-run the original failure conditions after repair, then the relevant order or concurrency scenario. A bounded clean sample supports the fix under those conditions; it does not prove the failure rate is zero. Report the cause supported by evidence, the repair or unresolved hypotheses, and what was actually exercised.
