---
name: flow-motion
description: Build or diagnose a specific animation, transition, or gesture interaction. Use for choreography, interruptible motion, or runtime performance work; general interface refinement belongs to flow.
---

# Flow motion

Resolve the motion interaction itself. Infer build versus review from the request; reviews stay read-only. Preserve existing visual identity and business behaviour.

## Establish the contract

Inspect the trigger, initial and final states, moving elements, and existing animation facilities. Identify whether motion communicates feedback, spatial continuity, explanation, or expression. Repetition and attention cost determine how restrained it should be; keyboard input alone is not a ban on motion.

Define interruption before implementation: what happens on reversal, rapid retrigger, navigation, and completion? Gestures should track input and preserve continuity when released. Do not queue stale responses or make essential controls wait for decoration.

## Build or repair

Reuse the project's motion tokens and components. Use a transition for a retargetable state change, authored keyframes for a fixed sequence, or a spring when velocity and direct manipulation matter. Add a runtime only when the existing stack cannot reasonably deliver the requested interaction.

Tune timing to distance and purpose using observed playback. Treat numeric choices as design decisions, not measured facts. Align origins and destinations with the objects involved; staggering and bounce need a reason beyond filling a sequence.

Prefer properties that avoid layout work where they fit. Profile when performance is the problem: a property or library name does not prove compositor execution. Inspect affected layout, paint, and main-thread work before replacing the mechanism.

Provide a meaningful reduced-motion result, including a static result when suitable. Maintain keyboard and touch access to hover-driven content. Stop work on dismissal or when hidden. Preserve focus and hit testing through overlays and transitions.

## Verify

Exercise normal playback, reversal, rapid input, unmount or navigation, and reduced motion as applicable. Check the actual target input and device where gesture or performance claims depend on it. Source review alone cannot establish feel.

Return the interaction changed, the reason for the mechanism, and observed checks. A finished motion request should produce working motion, not only a timing plan.
