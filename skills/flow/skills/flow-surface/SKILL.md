---
name: flow-surface
description: "Use when the user wants the visual surface polished: rounded corners that clash, icons that feel off, buttons with weak press feedback, cards with too much depth, misaligned icon-and-text rows. Also \"polish the UI details\", \"the corners look wrong\", \"tighten the surface\". One domain: radii, optical alignment, depth, icons, press feedback, hit areas."
argument-hint: "[scope: diff|module-path|all]"
---

# flow-surface

The polish pass for what a component is made of: corner radii, optical alignment, elevation, icons, press feedback, hit areas. Runs under the contract in `references/polish.md`; the values live in `references/surface.md`. Load both now.

## The checks

Sweep the scope for these, in order of harm:

1. **Clashing radii.** Nested rounded corners where outer ≠ inner + padding. The fix is the formula, applied to whichever value the repo's scale can absorb.
2. **Undersized hit areas.** Interactive targets under 24px square (Tier 1); under the 44px touch or 40px desktop preference (Tier 3). Grow with padding or a pseudo-element, never the glyph.
3. **Double depth.** A surface using two or more of border, shadow, and background shift for one job: cite FLOW-05, keep one.
4. **Dead press.** Interactive elements with no press feedback, or a press scale outside the 0.95 to 0.98 band. Set 0.96.
5. **Mechanical centring.** Pointed glyphs, icon-text rows, and fixed-height text sitting at mathematical centre. Correct optically, comment the correction (FLOW-07's rule).
6. **Icon drift.** Mixed icon sets, stroke weights that ignore the neighbouring text weight, hard icon swaps that should cross-fade.
7. **Edgeless media.** User-supplied images with no inset outline, invisible against a matching surface.

## Boundaries

- Radii, depth, icons, press, alignment, hit areas. Colour values go to `flow-colour`, type to `flow-type`, motion beyond the press interaction to `flow-motion`.
- Accessible names for icon-only controls are noted for `flow-access`, not fixed here.
- Idempotent: a clean second run reports "surface clean" in one line and stops.
