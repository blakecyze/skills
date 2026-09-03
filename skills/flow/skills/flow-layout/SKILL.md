---
name: flow-layout
description: "Use when the user wants layout polished: stray alignment edges, controls that look like text, cramped or floating groups, hidden overflow with no cue, breakpoints that fight the content, RTL breakage. Also \"tidy the layout\", \"the page feels messy\", \"fix the alignment\". One domain: edges, grouping, control affordance, disclosure, adaptivity."
argument-hint: "[scope: diff|module-path|all]"
---

# flow-layout

The polish pass for arrangement. Runs under the contract in `references/polish.md`; the ramp rules and the little things live in `references/spacing.md`. Load both now.

## The checks

1. **Stray edges.** Elements aligned to no shared edge. Pick the edges the design already implies and hold them; every exception is a finding or a comment.
2. **Ambiguous grouping.** Core Flow already owns this (FLOW-01, FLOW-03); cite those IDs rather than restating them. This pass adds the control-spacing detail: bordered controls at around 12px apart, borderless at around 24px.
3. **Invisible controls.** Interactive elements with no background shape, border, or consistent placement zone.
4. **Physical properties.** `padding-left` and friends where logical properties belong; the RTL mirror breaks silently otherwise.
5. **Cue-less disclosure.** Scrollable or collapsible content with no peek and no affordance.
6. **Edge confusion.** Controls running to the viewport edge, or media stopping at the layout margin; full-width mobile buttons not inset.
7. **Rigid adaptivity.** Fixed widths on text containers, device-name breakpoints where the content dictates otherwise, components that ignore container queries the repo already uses.

Verification for any fix: the affected widths, 200% zoom, and the RTL mirror where the product supports one.

## Boundaries

- Spacing scale membership stays FLOW-04 via `scripts/scan_tokens.py`.
- Reading-order-versus-layout-order contradictions are Tier 2 core findings; cite them, do not fork them.
- Idempotent: a clean second run reports "layout clean" in one line and stops.
