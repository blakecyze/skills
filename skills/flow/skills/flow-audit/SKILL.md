---
name: flow-audit
description: Use when the user asks for a design review, UI critique, accessibility check, or wants to know why a screen feels off. Works on a Flutter page, a React component, a stylesheet, a screenshot, or a Figma description. Read-only.
argument-hint: "[scope: file path | component | screenshot | description]"
allowed-tools: Bash(rg *) Bash(find *) Bash(python3 *)
---

# flow-audit

Read-only interface review. Produces a structured findings report. Makes no edits.

The taxonomy and the intent gate from `flow-principles` govern this skill. Read that first if it is not already loaded.

## Resolve the scope

`$ARGUMENTS` is one of:

- a file path → that widget, component, or stylesheet, plus anything it imports for styling
- a component or page name → locate it, then treat as above
- a screenshot or image → audit what is visible, and say plainly that token-level checks were skipped
- a prose description → audit the described structure, and flag that findings are structural only

If `$ARGUMENTS` is empty, ask what to review. Do not default to scanning the whole repo; design findings do not aggregate usefully at that scale.

## Gather context before judging

In order:

1. **Resolve tokens.** Look for a theme file, a design token file, Tailwind config, `ThemeData`, CSS custom properties, or `flow.config.json`. If found, that scale is the standard. If not, load `tokens/flow.defaults.json` and say in the report that defaults were assumed.
2. **Run the scanners.** `python3 scripts/scan_tokens.py <path>` for off-scale and hardcoded values. `python3 scripts/contrast.py --scan <path>` for colour pairs it can resolve.
Paths are relative to the Flow root: `${CLAUDE_PLUGIN_ROOT}` in Claude Code, otherwise the project's `flow/` directory.

3. **Read the surrounding surfaces.** Two or three sibling screens. A pattern that repeats across the product is a convention, not a violation. Flagging a house style as an error is the fastest way to make this skill untrusted.

## Pass the intent gate

State purpose, primary action, reading order, and density class before any finding. This appears at the top of the report. If the source cannot support it, stop and ask.

## Produce findings

Walk the taxonomy in order, FLOW-01 through FLOW-12. For each violation found:

- Locate it precisely. `file:line`, or a described region for images.
- Assign a tier using the `flow-principles` severity rules.
- Give evidence. The measured gap, the computed ratio, the actual value. Not "feels cramped".
- Give one specific fix. A value, not a direction.

One entry per violation per location. If the same violation appears eleven times in one file, that is one finding with a count and two example locations.

Do not pad. A screen with two Tier 1 findings and nothing else produces a report with two findings.

## Report format

Emit a single markdown document. No preamble, no closing offer of further help.

```markdown
# Design audit: <surface name>

**Scope:** <what was reviewed>
**Tokens:** <resolved from project | Flow defaults assumed>
**Findings:** <n> blocking, <n> structural, <n> consistency

## Intent

**Purpose:** <one sentence>
**Primary action:** <one action>
**Reading order:** 1. … 2. … 3. …
**Density:** <dense | standard | spacious>

## Summary

<Two or three sentences. Lead with the highest-severity finding. If the surface is sound, say so and stop.>

## Blocking

### [1] FLOW-11 — No visible focus state on primary action
**Location:** `lib/screens/checkout.dart:88`
**Evidence:** `ElevatedButton` with `focusColor` unset and no `FocusNode` styling. Keyboard users get no indication.
**Fix:** add a 2px outline in `colour.focus` at 2px offset. Applies to all six buttons in this file.

## Structural

(same shape)

## Consistency

(same shape, omitted entirely if the signal ratio would fall below 60%)

## What is working

<One or two sentences. Not flattery. Name what a future editor should not break.>
```

## Framing

- Critique the interface, not the designer. "This screen", never "you".
- Every finding carries a fix. A finding without one is a complaint.
- Never flag something merely because it is not to your taste. If it is coherent and intentional, it belongs in "what is working".
- Do not flag what a linter or formatter already handles.
- If a finding depends on information you do not have, such as what the empty state contains, ask rather than assume.

## What this skill never does

- Edit files. The audit is read-only, including the token files.
- Redesign. Suggesting a different layout entirely is out of scope; that is a separate conversation.
- Run the app, take screenshots, or install dependencies.
- Estimate contrast, character counts, or scale membership. Run the script.

## Failure modes to avoid

- Reciting gestalt principles as prose instead of citing a violated ID with a location.
- Auditing a component in isolation and flagging the product's house style as an inconsistency.
- Producing forty findings on one screen. Above roughly a dozen the report stops being read; group and prioritise.
- Assuming light mode. Check both themes if the project defines both.
- Treating a screenshot audit as equivalent to a source audit. Say what was not checkable.
