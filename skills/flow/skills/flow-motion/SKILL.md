---
name: flow-motion
description: "Use when the user asks to animate something, add motion, build a transition, review animation code, or asks why an interface feels sluggish or lifeless. Covers building new motion and auditing existing motion. Cites findings from the FLOW-M taxonomy; every curve, duration, and spring value comes from the motion reference, never from memory."
argument-hint: "[build <what> | audit <scope>]"
---

# flow-motion

Motion, in Flow's form: a gate before any code, a named taxonomy for what goes wrong, and numbers that come from a reference table rather than memory. The substance adapts Emil Kowalski's animation philosophy (animations.dev) into Flow's diagnostic idiom; the craft bar is his, the checks are Flow's.

This is the one Flow skill allowed to write new motion, because the most important motion decision produces zero lines of code: most things should not animate, and saying so is the job. Everything else in Flow's rules still binds: appearance only, smallest change available, repo conventions win.

## The motion gate

No animation may be proposed, built, or approved before both answers are stated in the response.

1. **Frequency tier.** How often does one user see this in a day?
   - `constant` (100+ a day, or anything keyboard-initiated): no animation, ever. Stop. A command palette that animates open is a defect, and this outcome is a success, not a dodge.
   - `frequent` (tens a day: hover, list navigation): near-imperceptible or nothing.
   - `occasional` (modals, drawers, toasts): standard motion.
   - `rare` (onboarding, first-run, success moments): the delight budget lives here, and only here.
2. **Purpose.** One of: feedback, spatial continuity, state indication, bridging a jarring change, explanation (marketing and onboarding only), delight (rare tier only). If no word fits, the animation has no reason to exist. "It looks cool" on a frequently seen element fails the gate.

Data the user is reading or acting on never moves for style. A mouse-tracking flourish belongs on a marketing page, not on a chart.

## The taxonomy

Eight named violations, `FLOW-M1` through `FLOW-M8`. Cite the ID in every finding, same as the core twelve. Severity tiers are Flow's: Tier 1 fails the user, Tier 2 misleads, Tier 3 is untidy.

| ID | Name | Check | Fix | Tier |
|---|---|---|---|---|
| FLOW-M1 | Unearned motion | Animation fails the gate: constant-tier or keyboard-triggered element animates, or no purpose word fits | Delete the animation. Offer the instant state change | 1 if keyboard or constant tier, else 2 |
| FLOW-M2 | Backwards easing | `ease-in` on any UI enter or exit, or a built-in browser easing on deliberate motion | `ease-out` or a strong custom curve from the reference | 2 |
| FLOW-M3 | Overlong duration | UI animation over 300ms with no stated reason, or over its per-element budget in the reference | Cut to budget. A 180ms dropdown feels faster than a 400ms one because it is | 2 |
| FLOW-M4 | Nowhere entrance | Entrance from `scale(0)` or bare fade with no transform, or a trigger-anchored popover scaling from centre | `scale(0.95)` plus opacity; `transform-origin` at the trigger. Modals are exempt: they are not anchored | 2 |
| FLOW-M5 | Restart on retrigger | Keyframes on toasts, toggles, or anything a user can fire twice in a second | CSS transitions, which retarget from the current value; springs for gestures, which carry velocity | 2 |
| FLOW-M6 | Layout-bound motion | Animating `width`, `height`, `margin`, `padding`, `top`, `left`; Motion `x`/`y`/`scale` shorthands on load-sensitive motion; a parent CSS variable driving child transforms | `transform` and `opacity` only. Full transform strings in Motion. `height` is tolerated for accordions alone | 2 |
| FLOW-M7 | Ungated motion | Movement with no `prefers-reduced-motion` branch, or hover motion not gated behind `(hover: hover) and (pointer: fine)` | Add both gates. Reduced motion means gentler, not zero: keep opacity and colour, drop movement | 1 |
| FLOW-M8 | Flat choreography | A group entering all at once where a stagger belongs, symmetric timing on a deliberate-then-respond interaction, or an exit that ignores the entrance path | Stagger 30 to 80ms; slow the deliberate phase and snap the response; exit the way it entered | 3 |

## Building motion

Run the gate first. Then walk the decision order; each step's values live in `references/motion.md`, which is loaded now, not recalled:

1. **Tool, cheapest that works.** CSS transition, then `@starting-style`, then CSS animation, then WAAPI, then a motion library. Never install a library for a fade. If the request is really a component (toast, drawer, command menu), say so; hand-rolling those loses focus management.
2. **Properties.** `transform` and `opacity`. The check for everything else is FLOW-M6.
3. **Curve and duration, or a spring.** From the reference tables. A hand-rolled cubic-bezier is a fabricated number, the same sin as a guessed contrast ratio.
4. **Interruption.** Anything rapidly triggered uses transitions; anything gesture-driven uses a spring.
5. **Gates ship with the code.** Reduced-motion and hover gating are part of the animation, not a follow-up.

Never present motion options as a menu. Make the call, state the gate result and the ingredients in one line each, write the code.

Output ends with the gate result (tier and purpose word), the ingredients (tool, properties, curve, duration), and, when feel cannot be judged from code, one line naming the check: play it at quarter speed in the DevTools animation inspector and look again with fresh eyes.

## Auditing motion

Findings use Flow's report format and the signal rule. Scan for the eight checks; each finding is `[n] path:line, FLOW-Mx, tier, one-line fix`. The remedial order when proposing fixes: delete, reduce, fix the curve, fix the origin, make it interruptible, move it to the GPU, then polish. Earlier moves beat later ones; the strongest fix for weak motion is usually less of it.

## Reference layer

| File | Load when |
|---|---|
| `references/motion.md` | Building anything, or any FLOW-M finding needing a value |
| `references/web.md` | The target is HTML, CSS, React, or similar |
| `references/flutter.md` | The target is Flutter or Dart |

## What this skill never does

- Write an animation that fails the gate, whoever asked.
- Estimate a curve, duration, or spring config that the reference defines.
- Animate layout properties outside the accordion exemption.
- Ship motion without its reduced-motion and hover gates.
- Add a motion library the repo does not already have without naming the cost and getting a yes.
- Restyle non-motion properties. That is `flow-audit` and `flow-apply` territory.
