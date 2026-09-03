# Typography

Loaded for FLOW-02, FLOW-12.

## The scale

Type sizes come from a ratio-based scale. For interfaces, a ratio between 1.125 and 1.25 works; below that steps are indistinguishable, above it the jumps are too violent for dense UI.

Default scale at ratio 1.2, base 16:

| Token | Size | Use |
|---|---|---|
| `xs` | 12 | captions, timestamps, legal |
| `sm` | 14 | secondary body, dense UI, table cells |
| `base` | 16 | body |
| `lg` | 18 | lead paragraph, card titles |
| `xl` | 24 | section headings |
| `2xl` | 32 | page titles |
| `3xl` | 40+ | display, marketing only |

Marketing surfaces can carry a wider ratio than app surfaces. If a product needs both, it needs two scales, declared as such, not one stretched scale.

## Hierarchy is made of four levers

Size, weight, colour, and space. Most flat-hierarchy screens (FLOW-02) have reached for size alone and run out of room.

Pull the levers in this order:

1. **Space.** Isolate the important thing. Often sufficient on its own.
2. **Weight.** One step (400 to 600) reads as strongly as two size steps and costs no layout.
3. **Colour.** Not brighter; *quieter* for everything else. Demote the surroundings to a lower-contrast neutral.
4. **Size.** Last, because it changes layout.

The instinct is to enlarge the primary element. The better move is usually to reduce everything else. A screen where three things shout does not need a fourth, louder thing.

## Line height

| Text | Line height |
|---|---|
| Display, 32px+ | 1.1 to 1.2 |
| Headings | 1.2 to 1.3 |
| Body | 1.5 |
| Dense UI, single lines | 1.4 |
| Long-form reading | 1.6 |

Line height and measure move together. A longer line needs more leading for the eye to find the next line's start. This is why FLOW-12 checks both.

## Measure

Body text sits between 45 and 75 characters per line, targeting around 65. Beyond 75 the return sweep starts failing. Below 45 the eye moves more than it reads.

Fix measure by constraining the container, never by shrinking the font. Shrinking the font to fit a wide container makes it worse: smaller text at the same width means *more* characters per line.

For Latin text, a usable approximation of the container width is `measure * 0.5 * fontSize`.

## Weight and case

Use two weights, three at most. A regular, a medium or semibold, and optionally one display weight. More weights means more decisions and less consistency.

All-caps is a signal, not a default. It slows reading and destroys word shape. If everything small is capitalised, capitals no longer signal anything. Where caps are used, add letter spacing of roughly 0.05em, because faces are not spaced for it.

Sentence case for everything by default: labels, buttons, headings, table headers.

## Optical correction

Large type needs tighter letter spacing than small type. A face set at 48px with default tracking looks loose; roughly -0.02em corrects it. Small text sometimes needs the opposite. These are legitimate FLOW-07 corrections and should carry a comment.

## Common failures

- Six type sizes on one screen, four of them within 2px of each other
- Using size to signal importance when the element is already isolated by space
- A heading and its body text at the same weight and the same colour, distinguished only by 2px of size
- Full-width body text in a wide container (FLOW-12)

## The little things

Craft details for `flow-type`. Substance adapted from jakub.kr/skills (better-typography).

- **Floors.** Body 16px for long-form; UI text 14px for inputs and menus, 13px for captions, rarely below 12px. Inputs are 16px on mobile or iOS Safari zooms the page.
- **Weights.** Below 18px stay at 400 or heavier; weights under 300 are display-only at 28px and up.
- **Line height.** Headings around 1.1; body 1.5 to 1.6; anything wrapping to three or more lines at least 1.4. Unitless values only.
- **Letter spacing.** Slightly negative on large headings, slightly positive on small uppercase labels, untouched at body sizes.
- **Wrapping.** `text-wrap: balance` on headings, `text-wrap: pretty` on descriptions, `overflow-wrap: break-word` where long IDs and URLs could escape, `white-space: nowrap` on labels and badges.
- **Numbers.** `font-variant-numeric: tabular-nums` on anything that changes: timers, counters, prices.
- **Truncation.** One line: ellipsis with hidden overflow and nowrap. Several: `line-clamp`. Truncation with no way to reach the full value is FLOW-11 territory.
- **Underlines.** `text-underline-position: from-font`, `text-decoration-thickness: from-font`, `text-decoration-skip-ink: auto`; dotted decoration for extra-info hints; colour is the only underline property that animates reliably.
- **OpenType.** Prefer the dedicated properties (`font-optical-sizing: auto`, `font-variant-numeric`) over raw `font-feature-settings`; raw tags are for custom axes only.
- **Loading.** Ship `.woff2`; load the actual faces the design uses rather than letting the browser synthesise bold or italic.
- **Punctuation.** Curly quotes in prose, straight in code; en dash for ranges (2010–2020); a single ellipsis character; `&nbsp;` keeps a value and its unit together.
