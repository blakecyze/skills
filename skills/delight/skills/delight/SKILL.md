---
name: delight
description: Refine how product interactions feel during UI creation or a polish pass. Build or review feedback, celebrations, character reactions, and progress mechanics when relevant; improve meaningful responses without adding gratuitous effects.
---

# Delight

Make interactions satisfying through clear outcomes, fitting expression, and uninterrupted control.

## Controls

`[scope] [review|apply] [focus]`

Infer the current interaction or flow when scope is omitted. Reviews stay read-only; build and refinement requests authorise scoped changes. Optional focus includes `feedback`, `celebration`, `character`, or `habits`. A broad pass checks relevant moments, not every possible mechanic.

## Pass

Inspect what users do, what actually succeeds, and how often it repeats. Find where feedback could provide confidence, relief, momentum, or play. Fix misleading status or lost input before decorating it. Satisfaction can come from a quiet, immediate response; an effect is not required.

For each changed interaction resolve:

`trigger → state change → feedback → interruption/repeat behaviour → accessible equivalent`

A press can acknowledge input immediately. Confirmed success follows the real outcome; optimistic updates need pending and rollback handling. Keep ordinary feedback local. Preserve the next action and focus. Rapid input and navigation must not accumulate stale effects, sounds, or timers. Meaning must survive reduced motion, mute, and unavailable hardware.

Load specialist detail only when relevant:

| Focus | Reference |
|---|---|
| Local feedback, channels, empty states, errors | [patterns.md](references/patterns.md) |
| Milestones, confetti, replay and duplicate events | [celebration.md](references/celebration.md) |
| Reviewing excess, misleading feedback, pressure | [audit.md](references/audit.md) |

For existing characters, check consistent reactions, clear status without artwork, and a neutral recovery state. For progress, check honest qualification, understandable recovery, and absence of guilt. These checks belong in the broad pass. Creating a character asset set or redesigning reward rules is a separate scope; `delight-character` and `delight-habits` provide focused workflows when installed. They are optional, and routine refinement does not require them.

Match the product's voice and the event's significance. A general refinement request does not call for inventing a mascot, streak, reward economy, or analytics system. Improve existing mechanics within scope; preserve their rules unless a rule change was requested.

Implement with existing assets and facilities. Exercise the changed moment repeatedly, including applicable failure, interruption, reduced-motion, and silent paths. Inspect rendered behaviour when possible; source review cannot establish feel or hardware haptics. Stop when the response is clear and repetition remains comfortable.

Return the changed moments or review findings and the checks actually run. Do not promise engagement gains from polish.
