# Spacing

Loaded for FLOW-01, FLOW-03, FLOW-08, FLOW-10. Gestalt: proximity (01, 03) and common region (10).

## The ramp

Spacing comes from a ramp, never from arithmetic at the call site. The default ramp is 4-based and roughly geometric:

`4, 8, 12, 16, 24, 32, 48, 64, 96`

Two properties matter more than the exact numbers:

1. **Steps are distinguishable.** Adjacent values differ enough to read as different. `16` and `18` in the same ramp is two names for one gap.
2. **Steps grow.** Linear ramps (`4, 8, 12, 16, 20, 24, 28`) give too many mid-range options and too few large ones. Growth keeps the ramp short.

A ramp longer than about nine steps is not a ramp, it is a permission slip.

## Density classes

The density declared at the intent gate selects which part of the ramp is in play.

| Class | Intra-group | Group gap | Section gap | Typical |
|---|---|---|---|---|
| `dense` | 4 | 8–12 | 16–24 | tables, forms, dashboards, list rows |
| `standard` | 8 | 16 | 24–32 | app screens, modals, settings |
| `spacious` | 12–16 | 24–32 | 48–96 | marketing, onboarding, empty states |

Mixing classes inside one surface is FLOW-08. A dense table on a spacious page is fine; the table keeps its own class internally, and the page's ramp governs the space around it.

## The proximity ratio

This is the single most useful number in the file.

**Space inside a group must be at most half the space between groups.**

A label 8px from its field and 8px from the next field creates no group at all. Take the intra-group gap down a step, or push the group gap up a step, until the ratio is at least 2:1. 3:1 reads more strongly and is usually worth it in forms.

Grouping by space is always preferable to grouping by border. Space costs nothing, adds no visual weight, and does not need a colour decision.

## Padding

Container padding should relate to the ramp, and to the content inside it. A card with `16` padding holding content on an `8` internal rhythm reads correctly. The same card with `13` padding does not, and nobody can say why, which is the point of FLOW-04.

Symmetric padding is the default. Asymmetry needs a reason: optical correction, a header that sits tight to a top edge, a scroll region that needs bottom breathing room.

## Vertical rhythm

Vertical gaps between text blocks should relate to line height, not just to the ramp. A gap smaller than the line height reads as part of the same block. A gap of roughly 1.5x to 2x line height reads as a new block.

For stacked text, prefer setting the gap on the container rather than adding margin to each child. Margin on children is where uneven spacing comes from.

## Common failures

- Using the same gap between every element on a screen (FLOW-01)
- Nesting three padded containers so the effective inner padding is 48 and nobody intended it (FLOW-10)
- Spacing derived from a component's height rather than the ramp
- Negative margins used to undo padding applied by a parent

## The little things

Craft details for `flow-layout`. Substance adapted from jakub.kr/skills (better-layout).

- **Edges.** Pick alignment edges and hold them; every stray edge reads as noise. Logical properties (`padding-inline-start`) over physical ones, so RTL comes free.
- **Controls look like controls.** Every interactive element carries a background shape, a border, or a consistent placement zone. A control styled like the static text beside it does not read as one.
- **Breathing room.** Bordered or filled controls want around 12px between them; borderless ones want roughly 24px, because nothing else separates them.
- **Edge-to-edge, inset controls.** Backgrounds and media may run to the viewport edge; controls stay inside the layout margins. A full-width mobile button is inset 16px with its radius visible.
- **Disclosure needs an affordance.** Scrollable overflow shows a 16 to 32px peek of the next item or a visible control; hidden content with no cue is FLOW-11's empty-state cousin.
- **Breakpoints come from content**, not device names; components adapt with container queries.
- **Checks.** Every supported width, 200% zoom, and an RTL mirror. Text containers never get fixed widths; translations grow.
