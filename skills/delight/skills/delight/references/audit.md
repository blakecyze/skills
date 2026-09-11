# Delight audit

Review a defined interaction or flow. Default to read-only; apply repairs when the user has asked for them.

Inspect the available code, screens, recordings, or live behaviour. Establish what event the effect represents and how often a user encounters it. A screenshot can show obstruction or tone, but cannot prove timing, replay, reduced-motion support, or the success trigger.

## Findings taxonomy

| ID | Failure | Concrete check |
|---|---|---|
| DELIGHT-01 | Attention exceeds the event | Repeat the ordinary action; inspect obstruction, queues, and competition with the next task |
| DELIGHT-02 | Feedback misstates the outcome | Trigger pending, failure, and rollback; trace celebration to the actual success signal |
| DELIGHT-03 | Decoration blocks control | Interrupt, navigate, and use keyboard actions; check focus, hit testing, and cleanup |
| DELIGHT-04 | Meaning depends on an unavailable channel | Reduce motion, mute sound, remove haptics; confirm the outcome stays understandable |
| DELIGHT-05 | Personality pressures the user | Inspect skip, absence, error, cancellation, and exit for shame or artificial obstruction |
| DELIGHT-06 | Reward displaces the real goal | Compare the easiest rewarded action with useful progress; inspect recovery and metric framing |

Use these identifiers only for demonstrated findings. Lack of access is a verification gap, not a violation. Distinguish an observed effect from an inference about how users might feel. Prefer a reproducible failure over an aesthetic judgement presented as fact.

## Output and repair

For each actionable finding, give the ID, location or state, evidence, user impact, and smallest repair. Prioritise misleading outcomes, lost control, and inaccessible meaning before intensity or tone preferences. Report no findings when none are supported; do not fill a quota.

If fixing, preserve business rules unless changing them is in scope. Prefer correcting the event trigger, reducing the competing effect, or restoring an equivalent status over creating a new system. Re-run the affected scenario and its alternate channel path.

Keep the report proportional: findings first, then coverage and unresolved checks. Passing a code inspection does not establish comfortable motion or correct device haptics.
