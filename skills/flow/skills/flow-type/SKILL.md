---
name: flow-type
description: "Use when the user wants typography polished: sizes below the floors, jumping numbers, ragged headings, broken truncation, ugly underlines, iOS zooming their inputs. Also \"fix the type\", \"the text feels off\", \"polish the typography\". One domain: sizes, weights, line height, wrapping, numerals, truncation, underlines, font loading."
argument-hint: "[scope: diff|module-path|all]"
---

# flow-type

The polish pass for text. Runs under the contract in `references/polish.md`; the scale rules and the little things live in `references/type.md`. Load both now.

## The checks

1. **Floor violations.** Body under 16px in long-form, UI text under its floor, mobile inputs under 16px (iOS zoom; Tier 1 on touch products).
2. **Thin text.** Weights under 400 below 18px, or under 300 outside display sizes.
3. **Cramped lines.** Line height under 1.4 on text wrapping three or more lines; headings far above 1.1 wasting vertical rhythm.
4. **Jittering numbers.** Timers, counters, and prices without `tabular-nums`.
5. **Bad rag.** Headings without `balance`, descriptions orphaning a single word without `pretty`, IDs and URLs escaping their container without `break-word`, labels wrapping where `nowrap` belongs.
6. **Broken truncation.** Clipped text with no ellipsis, or an ellipsis hiding a value the user cannot reach any other way (that second case is FLOW-11).
7. **Crude underlines.** Default decoration where from-font metrics and skip-ink would sit better; animated underline properties other than colour.
8. **Synthesised faces.** Bold or italic the loaded font does not actually ship; raw `font-feature-settings` where a dedicated property exists.
9. **Typographic slips.** Three dots for an ellipsis, hyphens for ranges, straight quotes in prose.

Scale membership questions (a size that belongs to no step) stay FLOW-04 and go through `scripts/scan_tokens.py`, not by eye.

## Boundaries

- Text colour and contrast go to `flow-colour`; measure (FLOW-12) is already core Flow and is cited, not duplicated.
- Copy content is `flow-copy`'s alone; this skill never rewords a string.
- Idempotent: a clean second run reports "type clean" in one line and stops.
