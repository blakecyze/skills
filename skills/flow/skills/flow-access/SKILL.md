---
name: flow-access
description: "Use when the user wants accessibility checked or repaired: focus states, keyboard paths, ARIA, form labels, target sizes, screen reader output, zoom behaviour. Also \"a11y pass\", \"is this accessible\", \"WCAG check\". One domain: the full accessibility surface, most of it Tier 1 by nature."
argument-hint: "[scope: diff|module-path|all]"
---

# flow-access

The polish pass for access. Runs under the contract in `references/polish.md`; the state rules and the little things live in `references/interaction.md`. Load both now. Most findings here are Tier 1 by nature: an interface a user cannot operate has failed them outright.

## The checks

1. **Fake elements.** `<div onClick>` doing a button's job, styled spans navigating. Native first; no ARIA beats bad ARIA.
2. **Focus.** Missing or removed `:focus-visible`, rings under 2px, rings that vanish against an adjacent colour or in forced-colors mode. Overlaps FLOW-11; cite both.
3. **Keyboard gaps.** Pointer interactions with no keyboard path, positive `tabindex`, composite widgets without roving focus.
4. **Small targets.** Under 24px square is Tier 1; under the 44px/40px preference is Tier 3. Fix via `flow-surface`'s padding rule.
5. **Unlabelled forms.** Placeholder-as-label, missing `<label for>`, missing `autocomplete`/`inputmode`, blocked paste, submit disabled before the request starts, errors not wired through `aria-invalid` and `aria-describedby`.
6. **Silent updates.** Toasts and validation with no live region, `role="alert"` on things that are not urgent, regions created at update time.
7. **Colour-only status.** Any state carried by hue alone; the second cue is this skill's finding even though the hue is `flow-colour`'s.
8. **Structure.** Heading order, one `<main>`, skip link, 200% zoom and 320px width without horizontal scroll.
9. **Motion and media.** Missing reduced-motion branches (cite FLOW-M7), autoplay without pause, alt text describing the picture instead of the purpose.

## Boundaries

- Contrast numbers come from `flow-colour`'s measured pass; this skill owns the requirement, not the measurement.
- Fixes here may touch attributes and element choice, which is behaviour-adjacent: flag anything beyond styling explicitly in the gate so the user approves it knowingly.
- Idempotent: a clean second run reports "access clean" in one line and stops.
