# Surface

Loaded for `flow-surface` and any radius, depth, or icon finding. Values are quoted, never recalled. Craft substance adapted from jakub.kr/skills (better-ui) in Flow's words.

## Concentric radii

Nested rounded corners share a centre or they clash. The rule is arithmetic:

```
outer radius = inner radius + padding between them
```

A card with 8px padding around a 8px-radius thumbnail needs a 16px outer radius. An outer radius equal to the inner one reads as a mistake at every size.

## Optical alignment

Mathematical centring lies for asymmetric shapes.

- Play icons and other pointed glyphs nudge 1 to 2px toward their visual weight.
- Icon-beside-text rows align to the text's cap height, not the line box.
- Text in a fixed-height control sits 1px above true centre; descenders make true centre look low.
- Every optical correction gets a one-line comment, because it will otherwise be "fixed" back.

## Press feedback

- Press scale is `0.96`. Below `0.95` reads as exaggerated; above `0.98` reads as broken.
- Opacity and colour transitions on high-frequency interactions stay at or under 150ms.

## Icons

- Stroke width pairs with the neighbouring text weight: `1.5px` beside regular (400), `2px` beside semibold (600).
- One icon set per product. A second set is a finding, not a preference.
- Icon-only controls carry an accessible name; that check belongs to `flow-access`.
- Icon swaps (play to pause, menu to close) cross-fade rather than pop: opacity 0 to 1 with a small scale rise, curve `cubic-bezier(0.2, 0, 0, 1)`.

## Depth

- One elevation device per surface: border, or shadow, or background shift. Two of the three on one card is FLOW-05.
- Shadows are for things that float (menus, dialogs, dragged items), not for static cards seeking importance.
- Images and user-supplied media get a 1px inset outline so light images hold an edge on light surfaces: `oklch(0 0 0 / 0.1)` in light mode, `oklch(1 0 0 / 0.1)` in dark.

## Hit areas

- Interactive targets: 24px square minimum, 44px preferred on touch, 40px on desktop.
- Grow the target with padding or a pseudo-element, never by inflating the glyph.
- Adjacent targets must not overlap once grown.
