---
name: flow-colour
description: "Use when the user wants colour polished or systematised: one-off hex values everywhere, tokens named after appearance, muddy gradients, a dark mode built by inversion, contrast in doubt. Also \"clean up the colours\", \"tokenise the palette\", \"convert to OKLCH\". One domain: ramps, tokens, notation, gradients, contrast, dark mode."
argument-hint: "[scope: diff|module-path|all]"
---

# flow-colour

The polish pass for colour systems. Runs under the contract in `references/polish.md`; the two-bucket rule, ramp shape, and the little things live in `references/colour.md`. Load both now.

## The checks

1. **Measured contrast.** Every text and UI pair against its actual rendered background via `scripts/contrast.py --scan`. Failures are Tier 1, reported as pair, measured value, threshold missed. Never an estimated ratio.
2. **The token seam.** Components referencing primitives directly, tokens named for appearance (`--color-blue-button`) or first use (`--color-sidebar-gray`), semantic hues moonlighting as decoration (FLOW-09).
3. **Off-ramp values.** One-off colours that are almost a ramp step: merge them. Twelve near-identical greys are one grey with eleven findings.
4. **Mixed notation.** Hex scattered among `oklch()`: one notation per codebase, OKLCH preferred for new systems.
5. **Grey gradients.** Two-hue gradients interpolated in sRGB; move to `in oklab`, or `in oklch` when the midpoint must stay vivid.
6. **Inverted dark mode.** A dark theme that is the light ramp flipped: vividness untamed, dark end cramped, pairs unmeasured. Also two switching mechanisms where one belongs.
7. **Gamut.** P3 colours with no sRGB base declaration.

## Boundaries

- Which element gets the emphasis is FLOW-02/FLOW-06 territory (core audit); this skill polishes the system that expresses it.
- Focus-visible colour checks are shared with `flow-access`; measure here, report there.
- Idempotent: a clean second run reports "colour clean" in one line and stops.
