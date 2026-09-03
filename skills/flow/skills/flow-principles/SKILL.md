---
name: flow-principles
description: Use when generating, reviewing, restyling, or discussing any user interface. Sets standing design rules for all UI work. Loads for UI work; not directly invoked by the user.
user-invocable: false
---

# flow-principles

Standing context for any interface task: UI you write, review, or restyle.

The single governing principle: **hierarchy is derived, not chosen**. Once you know what a surface is for and what its primary action is, most visual decisions stop being taste. If you are picking a font size because it "looks better", you have skipped a step.

Flow is diagnostic, not generative. It does not invent a visual identity. It finds where an interface contradicts itself and repairs the contradiction with the smallest change available.

Paths below are relative to the Flow root: `${CLAUDE_PLUGIN_ROOT}` in Claude Code, otherwise the project's `flow/` directory.

## The intent gate

**No styling change may be proposed or made before this gate is passed.** State the answers explicitly, in the response, before touching anything:

1. **Purpose.** What is this surface for, in one sentence, from the user's point of view.
2. **Primary action.** The single thing a user most often needs to do here. Exactly one. If you cannot pick one, the screen has an information architecture problem, and that is the finding.
3. **Reading order.** The sequence a user should scan, as a short ordered list.
4. **Density class.** `dense` (data tables, forms, dashboards), `standard` (app screens, settings, modals), or `spacious` (marketing, onboarding, empty states). This selects the spacing ramp.

If the source material does not supply enough to answer these, ask. One question costs less than a confidently restyled screen that fights its own purpose.

## Severity tiers

Every finding carries a tier. Tiers drive ordering and drive what gets fixed first.

**Tier 1 — Blocking.** The interface fails a user outright. Contrast below WCAG AA, touch targets under the platform minimum, no visible focus state, text truncated with no recovery, an action that gives no feedback.

**Tier 2 — Structural.** The interface works but misleads. Hierarchy inverted, grouping contradicts meaning, primary action indistinguishable from secondary, reading order fights layout order.

**Tier 3 — Consistency.** The interface is coherent but untidy. Off-scale values, duplicate near-identical styles, inconsistent radii or weights.

**The signal rule:** if Tier 1 and Tier 2 findings are fewer than 60% of the total, the review is generating noise. Cut Tier 3 until the ratio holds, or drop the Tier 3 section.

## The taxonomy

Twelve named violations. Cite the ID in every finding. Each carries a check that can be evaluated against the source; a rule without a check is an opinion.

| ID | Name | Check | Fix |
|---|---|---|---|
| FLOW-01 | Uniform spacing | More than three consecutive siblings share an identical gap and are not a homogeneous list | Tighten related items one ramp step below the group gap; target a 2:1 minimum between intra-group and inter-group spacing |
| FLOW-02 | Flat hierarchy | No element scores meaningfully higher than the rest on combined size, weight, and contrast within the primary viewport | Raise the primary element by two type steps or one weight step. Lower everything else before raising anything |
| FLOW-03 | Orphaned label | `gap(label, its control) >= gap(label, nearest other element)` | Tighten label to control at the smallest ramp step; field-group gap at least twice that |
| FLOW-04 | Off-scale value | Value absent from the resolved token set and not a commented optical correction | Snap to the nearest ramp step. If the nearest step is visibly wrong, the ramp is wrong: a `flow-tokens` finding |
| FLOW-05 | Decoration without function | Removing the border, divider, shadow, or gradient changes no grouping, state, or affordance | Delete it. If two devices do one job (border plus shadow plus tint), keep one |
| FLOW-06 | Competing emphasis | More than one element in a view uses the highest-emphasis treatment | One primary per view. Demote the rest to secondary, tertiary, then plain link |
| FLOW-07 | Broken optical alignment | Icon or shape sharing a baseline with text at identical padding all round; centred text with equal top and bottom padding in a fixed-height control | Correct optically and leave a one-line comment. The only place an off-scale value may survive |
| FLOW-08 | Density mismatch | Ramp in use does not match the density class declared at the gate | Re-derive spacing from the correct ramp. Do not average the two |
| FLOW-09 | Unearned colour | A hue used both semantically (success, error, primary) and decoratively in the same view | Semantic colours are reserved. Decoration uses the neutral ramp, or a neutral tint for warmth |
| FLOW-10 | Container theatre | Nesting depth of visually distinct containers greater than two | Flatten. Spacing can carry grouping, and spacing is cheaper than a border |
| FLOW-11 | Unstyled state | Interactive element with no focus-visible style, or a data-bound region with no empty and no error branch | Focus and disabled are Tier 1, never optional. Empty and error states need real copy |
| FLOW-12 | Runaway measure | Body text over roughly 75 characters per line, or line height under 1.4 on multi-line body copy | Constrain the container, not the font size. Longer measures need proportionally more line height |

## Guidance

- **Read the room.** The repo's existing scale wins over Flow's defaults. Run `flow-tokens` first on unfamiliar code.
- **Subtract before adding.** The first candidate fix is deletion. If a fix adds an element, say why nothing could be removed.
- **One change, one reason.** Every edit traces to a taxonomy ID. No ID, no edit.
- **Preserve voice.** A coherent style that is not to your taste is not a finding.
- **Numbers come from `scripts/`, never memory.** A model-guessed contrast ratio is a fabricated one.
- **Appearance only.** Never change behaviour, state, routing, data flow, copy, or brand identity.

## Reference layer

Load only when a finding needs it. Do not read speculatively.

| File | Load when |
|---|---|
| `references/spacing.md` | FLOW-01, 03, 08, 10 |
| `references/type.md` | FLOW-02, 12 |
| `references/colour.md` | FLOW-05, 06, 09 |
| `references/interaction.md` | FLOW-11, and any Tier 1 accessibility finding |
| `references/flutter.md` | the target is Flutter or Dart |
| `references/web.md` | the target is HTML, CSS, React, or similar |
| `references/motion.md` | the target animates, or any FLOW-M finding (see `flow-motion`) |
| `tokens/flow.defaults.json` | no project token set was found |
