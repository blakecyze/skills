---
name: flow-principles
description: Use when generating, reviewing, restyling, or discussing any user interface. Sets standing design rules for all UI work. Auto-loads; not directly invoked by the user.
user-invocable: false
---

# flow-principles

Standing context for any interface task. These rules apply to UI you write, UI you review, and UI you restyle. They override the default habit of decorating a screen before understanding it.

The single governing principle: **hierarchy is derived, not chosen**. Once you know what a surface is for and what its primary action is, most visual decisions stop being taste. If you are picking a font size because it "looks better", you have skipped a step.

Flow is diagnostic, not generative. It does not invent a visual identity. It finds where an existing interface contradicts itself and repairs the contradiction using the smallest change available.

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

Twelve named violations. Cite them by ID in every finding so they are searchable and consistent across sessions and tools.

Each carries a **check** that can be evaluated against the source. A rule without a check is an opinion, and opinions do not belong here.

### FLOW-01 — Uniform spacing
*Gestalt: proximity.* Equal gaps between everything, so nothing reads as a group.
**Check:** more than three consecutive sibling elements separated by an identical gap value, where the content is not a homogeneous list.
**Fix:** related items tighten to one ramp step below the group gap. Target a 2:1 minimum ratio between intra-group and inter-group spacing.

### FLOW-02 — Flat hierarchy
No single element wins the first glance. Three or more elements share the same weight, size, and colour treatment while competing for attention.
**Check:** no element scores meaningfully higher than the rest on combined size, weight, and contrast within the primary viewport.
**Fix:** raise the primary action or headline by at least two type-scale steps or one weight step. Lower everything else before raising anything.

### FLOW-03 — Orphaned label
*Gestalt: proximity.* A label sits nearer to something other than the control it describes.
**Check:** `gap(label, its control) >= gap(label, nearest other element)`.
**Fix:** tighten the label to its control to the smallest ramp step. Push the gap between field groups to at least twice that.

### FLOW-04 — Off-scale value
A spacing, size, or radius value that belongs to no scale. `13px`, `7px`, `22px` amid a 4pt ramp.
**Check:** value is not present in the resolved token set and is not an intentional optical correction with a comment saying so.
**Fix:** snap to the nearest ramp step. If the nearest step is visibly wrong, the ramp is wrong, and that is a `flow-tokens` finding.

### FLOW-05 — Decoration without function
*Gestalt: figure and ground.* Borders, dividers, shadows, and gradients that encode no information.
**Check:** removing the element changes no grouping, no state, and no affordance.
**Fix:** delete it. If two devices do the same job (a card that has both a border and a shadow and a background tint), keep one.

### FLOW-06 — Competing emphasis
Two or more elements claim primary status. Two filled buttons side by side, or an accent colour used both for the call to action and for a decorative heading.
**Check:** more than one element in a view uses the highest-emphasis treatment defined by the token set.
**Fix:** one primary per view. Demote the rest to secondary, tertiary, or plain text link, in that order of remaining weight.

### FLOW-07 — Broken optical alignment
Values are mathematically equal, and the result still looks wrong. Icons beside text, capital letters against lowercase, circular shapes against rectangles.
**Check:** icon or shape sharing a baseline with text and using identical padding on all sides; centred text with equal top and bottom padding in a fixed-height control.
**Fix:** correct optically, then leave a comment giving the reason. This is the one place an off-scale value is allowed to survive.

### FLOW-08 — Density mismatch
Spacing borrowed from the wrong density class. Marketing whitespace inside a data table, or form-grade tightness on a landing page.
**Check:** the ramp in use does not match the density class declared at the intent gate.
**Fix:** re-derive spacing from the correct ramp. Do not average the two.

### FLOW-09 — Unearned colour
*Gestalt: similarity.* Colour carrying no meaning, or the same colour carrying two meanings.
**Check:** a hue used both semantically (success, error, primary action) and decoratively in the same view.
**Fix:** semantic colours are reserved. Decoration uses the neutral ramp. If a surface needs warmth without meaning, use a neutral tint, not a brand hue.

### FLOW-10 — Container theatre
*Gestalt: common region.* Nested regions where one region would do. A card, inside a panel, inside a section, each with its own background, border, and padding.
**Check:** nesting depth of visually distinct containers greater than two.
**Fix:** flatten. Grouping can be carried by spacing alone, and spacing is cheaper than a border.

### FLOW-11 — Unstyled state
A component that only exists in its ideal state. No hover, focus, active, disabled, loading, empty, or error treatment.
**Check:** an interactive element with no focus-visible style, or a data-bound region with no empty and no error branch.
**Fix:** focus and disabled are Tier 1 and never optional. Empty and error states need real copy, not a spinner and a shrug.

### FLOW-12 — Runaway measure
*Typography.* Line length beyond comfortable reading, or line height that ignores it.
**Check:** body text exceeding roughly 75 characters per line, or line height below 1.4 on multi-line body copy.
**Fix:** constrain the container, not the font size. Longer measures need proportionally more line height.

## Positive guidance

**Read the room before changing it.** A repo's existing scale wins over Flow's defaults. Run `flow-tokens` first on unfamiliar code. Imposing a foreign ramp on a coherent system creates more inconsistency than it removes.

**Subtract before adding.** The first candidate fix for almost every finding is deletion. Fewer borders, fewer weights, fewer hues, fewer containers. If a fix adds an element, say why nothing could be removed instead.

**One change, one reason.** Every edit traces back to a taxonomy ID. An edit with no ID behind it is personal preference and does not ship.

**Preserve voice.** A product with an established look keeps it. Flow fixes contradictions inside a visual language, and does not replace the language. If the existing style is genuinely coherent and merely not to your taste, that is not a finding.

**Numbers come from tools, not memory.** Contrast ratios, scale membership, and character counts are computed by `scripts/`, never estimated. A model-guessed contrast ratio is a fabricated one.

## Reference layer

Load these only when a finding needs them. Do not read them speculatively.

Paths below are relative to the Flow root. In Claude Code that root is
`${CLAUDE_PLUGIN_ROOT}`; anywhere else it is the `flow/` directory in the project.


| File | Load when |
|---|---|
| `references/spacing.md` | FLOW-01, 03, 08, 10 |
| `references/type.md` | FLOW-02, 12 |
| `references/colour.md` | FLOW-05, 06, 09 |
| `references/interaction.md` | FLOW-11, and any Tier 1 accessibility finding |
| `references/flutter.md` | the target is Flutter or Dart |
| `references/web.md` | the target is HTML, CSS, React, or similar |
| `tokens/flow.defaults.json` | no project token set was found |

## What this skill never does

- Change behaviour, state, logic, routing, or data flow. Appearance only.
- Introduce a new visual identity, typeface, or brand colour.
- Rewrite copy, unless the finding is FLOW-11 and the state has no copy at all.
- Estimate a number that a script can compute.
- Produce a finding without a taxonomy ID and a specific fix.
