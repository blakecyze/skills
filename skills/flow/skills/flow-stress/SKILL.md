---
name: flow-stress
description: "Use when the user wants a component stress-tested: \"break this component\", \"test it with weird data\", \"what happens with long text / zero items / no image\", \"stress the card\". Renders one component across every realistic scenario on a throwaway page and reports where it visibly breaks."
argument-hint: "<one component>"
---

# flow-stress

Renders one component across everything production will eventually feed it, and reports what visibly breaks. Approach adapted from jakub.kr/skills (break) in Flow's terms. Diagnostic: it never fixes.

## Scope

One component per run, granular: "the profile form's text input", not "the settings page". Restate it in one line: what it accepts, what it renders, where it lives. Too broad, ask the user to narrow.

## Scenarios

Infer from what the component actually accepts; test only axes with a matching cue:

| It accepts | Stress with |
|---|---|
| Text | Empty, very long, no-space strings, special characters, whitespace-only |
| Collections | Zero items, one, many, wildly mixed lengths |
| Media | Missing, slow, oversized, extreme aspect ratios |
| State props | Disabled, loading, error, active, every boolean both ways |
| A container | Narrow, wide, constrained side by side |
| Theme | Light and dark, when the app has both |

Write the scenario list as one-liners before building, and name the dropped axes with reasons. A static icon never gets the long-text treatment.

## The rig

A throwaway route rendering the real component from the project, inside the app's own layout, fonts, and global styles. Files named `flow-stress-rig.*`. The page adds labels, fixed-width containers, and fixture props; no custom styling, no theme forks, no instrumentation. Width variations render side by side so one load shows everything. In split client/server frameworks, mark the page client-side so fixtures survive.

## The pass

Load once, skim top to bottom, record only what visibly broke: "text escapes the field edge", never "spacing feels tight". Aesthetic judgement belongs to `flow-audit`. If the app cannot be launched here, build the rig, hand over the URL, and say the looking is the user's half.

## The report

| Scenario | Observed | Owner |

Broken scenarios first. Owner names the rule that explains the break: a FLOW or FLOW-M ID, or the domain skill (`flow-type` for truncation, `flow-access` for a lost focus ring). Nothing broken: say so and list what was tested. No fixes unless asked.

**The rig stays.** It is half the report; the user deletes it, or asks for it deleted, when done. Every file matches `flow-stress-rig.*` so removal is one glob.

## What this skill never does

- Test more than one component per run, or axes with no matching cue.
- Restyle, debug, or resize between scenarios.
- Report an aesthetic opinion as a break.
- Fix anything, even an obvious one-liner, without being asked.
