# Web

Loaded when the target is HTML, CSS, React, or similar.

## Where tokens live

CSS custom properties on `:root`, or a Tailwind theme extension. Both are fine; mixing both without a single source of truth is not.

```css
:root {
  --space-1: 4px;  --space-2: 8px;  --space-3: 12px;
  --radius-md: 10px;
  --text-base: 1rem;
}
```

Use `rem` for type and `px` for borders and hairlines. Spacing can be either, consistently. A raw `13px` in a component is FLOW-04.

For Tailwind, arbitrary values (`p-[13px]`, `text-[#3a3a3a]`) are the exact signature of scale escape. `scripts/scan_tokens.py` flags them.

## Layout

Prefer `gap` on a flex or grid parent over margins on children. This is the same argument as the Flutter one: margins compose in ways nobody can compute, `gap` is declared once and visible.

Use logical properties (`padding-inline`, `margin-block`) where the product may be localised into right-to-left languages. Retro-fitting direction later is expensive.

Constrain measure with `max-width: 65ch` on prose containers rather than a pixel width. It tracks the font automatically.

## Selector discipline

Style specificity conflicts are a frequent cause of "the value is right in the code and wrong on screen". Before diagnosing a spacing finding, confirm the value in the source is the value actually computed. A section-level rule cancelling a component-level rule looks identical to a wrong value.

Do not fix specificity conflicts with `!important`. That is a Tier 2 finding of its own.

## Focus

```css
:focus-visible {
  outline: 2px solid var(--colour-focus);
  outline-offset: 2px;
}
```

Never `outline: none` without an immediate replacement in the same rule. Resets that strip focus globally are the most common Tier 1 finding on the web.

`outline-offset` matters: an outline flush against a filled button is hard to see against the button's own colour.

## Dark mode

Prefer `light-dark()` or a `[data-theme]` attribute over `prefers-color-scheme` alone, so the user can override the system. Run contrast checks against both computed themes. A pair that passes on white commonly fails on the dark surface.

## Common web-specific findings

- `line-height` set in `px`, which breaks when the user zooms text only
- Fixed `height` on a button containing text, which clips at larger text sizes
- `overflow: hidden` used to tidy a layout, which silently truncates content
- Hover-only affordances that are unreachable on touch devices
- Transitions on `all`, which animate properties nobody intended and cost frames
