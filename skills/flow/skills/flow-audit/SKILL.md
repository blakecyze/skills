---
name: flow-audit
description: Use when the user asks for a design review, UI critique, accessibility check, or wants to know why a screen feels off. Works on a Flutter page, a React component, a stylesheet, a screenshot, or a Figma description. Read-only.
argument-hint: "[scope: file path | component | screenshot | description]"
allowed-tools: Bash(rg *) Bash(find *) Bash(python3 *)
---

# flow-audit

Read-only interface review. Produces a structured findings report. Makes no edits.

The taxonomy, tiers, and intent gate from `flow-principles` govern this skill. Load it first if it is not already loaded.

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
2. **Run the scanners on the target file and its style imports only.** `python3 scripts/scan_tokens.py <file>` and `python3 scripts/contrast.py --scan <file>`. Tree-wide scanning is `flow-tokens`' job. Read the summary line first; stop there if it is clean.
3. **Check the house style.** Grep two or three sibling screens for the specific pattern you are about to flag. Do not read them whole. A pattern that repeats across the product is a convention, not a violation.

## Pass the intent gate

State purpose, primary action, reading order, and density class before any finding. If the source cannot support it, stop and ask.

## Produce findings

Walk the taxonomy in order, FLOW-01 through FLOW-12. For each violation found:

- Locate it precisely. `file:line`, or a described region for images.
- Assign a tier.
- Give evidence. The measured gap, the computed ratio, the actual value. Not "feels cramped".
- Give one specific fix. A value, not a direction.

One entry per violation per location. If the same violation appears eleven times in one file, that is one finding with a count and two example locations. Above roughly a dozen findings the report stops being read; group and prioritise.

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

## Guardrails

- Critique the interface, not the designer. "This screen", never "you".
- Every finding carries a fix. A finding without one is a complaint.
- Do not flag what a linter or formatter already handles, or a coherent house style.
- If a finding depends on information you do not have, ask rather than assume.
- Check both themes if the project defines both.
- A screenshot audit is not a source audit. Say what was not checkable.
- Never edit files, redesign the layout, run the app, or estimate a number a script can compute.
