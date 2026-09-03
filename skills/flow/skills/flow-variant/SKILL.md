---
name: flow-variant
description: "Use when the user wants design directions to compare: \"give me a few versions\", \"try some variants\", \"explore different takes on this component\", \"which direction should this go\". Builds three named variants along one axis, rendered on the real page behind a switcher, presented with a tradeoff table and no favourite."
argument-hint: "<component or view> [axis: structure|density|emphasis|type|voice]"
---

# flow-variant

Builds genuine alternatives instead of one answer. Three variants by default, five only when asked or when the design space clearly holds five distinct directions. Approach adapted from jakub.kr/skills (variant) in Flow's terms.

## The axis

Each set of variants differs along **one primary axis**, named before any code:

| Axis | What varies |
|---|---|
| structure | grouping, ordering, column count, collapse behaviour |
| density | spacing ramp, hit areas, content per viewport |
| emphasis | where filled colour and weight land |
| type | scale steps, weight contrast, measure |
| voice | labels, tone, copy volume |

Secondary choices follow the primary direction coherently; a "dense" variant is dense in type and spacing alike, not a grab bag. If `$ARGUMENTS` names no axis, derive one from the intent gate: what the surface is for usually implies what is worth varying.

## Names before code

Each variant gets a direction-name before it is built: "Quiet", "Editorial", "Dense". Never "Option A". If a variant cannot be named, it is not a direction, and it is cut.

## The rig

Variants render on the actual page they will live on, in the app's own layout, fonts, and tokens, with real content at production-like volume. Never lorem ipsum, never a thumbnail grid; small renderings lie about spacing.

Switching is one mechanism: a `?variant=` search parameter with a small floating control, all in files named `flow-variant-rig.*` so cleanup is a glob. The rig adds nothing else.

Every variant passes the intent gate and the taxonomy; a variant that ships a FLOW violation as its "personality" is a defect, not a direction.

## The choice

Present a tradeoff table: variant, where it sits on the axis, where it wins, what it costs. **State no favourite.** The user knows the product's personality; Flow knows the mechanics. Direction is theirs.

On the pick: implement the chosen variant through the repo's conventions, then delete every `flow-variant-rig.*` file and the switcher. The losing directions survive only in the tradeoff table in the transcript.

## What this skill never does

- Build variants of a surface that fails the intent gate; fix the purpose first.
- Vary two axes at once, or pad the set with a strawman built to lose.
- Recommend a winner, explicitly or by adjective.
- Leave rig files behind after the pick, or touch production files before it.
