---
name: flow-apply
description: Use when the user asks to restyle, tidy, polish, or fix the design of an interface, or to act on findings from a flow-audit report. Appearance-only; never changes behaviour.
argument-hint: "[scope: file path | audit-report | current-file]"
disable-model-invocation: true
allowed-tools: Bash(rg *) Bash(find *) Bash(python3 *)
---

# flow-apply

Appearance-preserving-of-behaviour repair. Fixes taxonomy violations in place using the smallest change that resolves each one.

The taxonomy and intent gate from `flow-principles` govern this skill.
Paths are relative to the Flow root: `${CLAUDE_PLUGIN_ROOT}` in Claude Code, otherwise the project's `flow/` directory.


## The hard rule

**Styling changes must not alter behaviour. Behaviour changes must not ride along with styling.**

Before every edit, ask: does this change what the interface *does* for any input, or only what it *looks like*? If it changes what it does, stop and surface it as a question.

Cases where the boundary is tested:

- Changing a padding value → appearance. Proceed.
- Raising a touch target from 32 to 44 → appearance, unless it changes layout enough to reflow siblings. Check the parent, then proceed.
- Adding a focus outline → appearance. Proceed.
- Adding an empty state that did not exist → **behaviour**. It introduces a new branch. Ask.
- Removing a container to fix FLOW-10 → appearance only if the container carries no gesture handler, no scroll, no semantics node, and no key. Grep before deleting.
- Demoting a second primary button to secondary → appearance. But if it changes which action users take, say so in the summary.
- Changing a colour token value globally → appearance, with product-wide blast radius. Ask before touching the token file itself.

When in doubt, treat it as behaviour and ask.

## Resolve the scope

`$ARGUMENTS` is one of:

- a file path → that file
- `audit-report` → act on a prior `flow-audit` report's Tier 1 and Tier 2 findings, in that order
- `current-file` → whatever is in focus

If no scope is given and there is no obvious focus, ask.

## Working process

1. **Resolve tokens first.** Every value written must come from the resolved token set. If a fix needs a value the set does not contain, do not invent it: report it as a `flow-tokens` gap and skip that fix.
2. **Pass the intent gate.** Purpose, primary action, reading order, density. Restated in the summary.
3. **List candidates before editing.** Grouped by taxonomy ID with a count. If the list runs past about ten changes, confirm scope with the user before proceeding.
4. **Fix in tier order.** Tier 1, then Tier 2, then Tier 3. Stop when the remaining findings are cosmetic and the user has not asked for cosmetics.
5. **One taxonomy ID per logical change group.** Each group should be independently revertible.
6. **Verify each edit.** Does it produce the same behaviour for the same input, and does it resolve the cited violation? If it does not resolve the violation, revert rather than layering another change on top.
7. **Re-run the scanners.** A fix that introduces a new off-scale value has traded one finding for another.

## Fix discipline

**Subtract first.** For each finding, the first candidate is removal. Only add when nothing can be removed.

**Smallest resolving change.** Do not take a FLOW-01 spacing finding as licence to rewrite the layout. Change the gaps.

**No drive-by improvements.** If you notice something outside the cited findings, note it in the summary as deferred. Do not fix it silently. Scope creep in a styling pass is unreviewable.

**Preserve voice.** Match the file's existing formatting, ordering of style properties, and naming. A restyle that also reformats is a diff nobody can read.

**Comment optical corrections only.** FLOW-07 fixes get a one-line comment giving the reason. Nothing else gets a comment; the diff explains itself.

## Output format

After editing, produce:

```markdown
## Flow summary

**Scope:** <files touched>
**Tokens:** <source of the resolved set>

### Intent
**Purpose:** … **Primary action:** … **Density:** …

### Changes made

- **FLOW-01** (4×) Tightened label-to-field gaps to `space.1`, raised group gaps to `space.6` — `checkout.dart:44,61,78,95`
- **FLOW-06** (1×) Demoted "Save for later" from filled to outline — `checkout.dart:132`
- **FLOW-05** (3×) Removed borders from cards that already carry elevation — `cart_item.dart:20`

### Deferred — needs your decision

- `checkout.dart:210` has no empty state. Adding one introduces a new branch, which is a behaviour change. What should it say?
- Fixing FLOW-04 at `theme.dart:18` requires changing `space.3` from 13 to 12 globally. That affects 40+ call sites. Confirm before I touch the token file.

### Next steps

- Review the diff visually in both light and dark themes
- Re-run `flow-audit` to confirm the findings cleared
```

## What this skill never does

- Change logic, state, routing, data fetching, or props that are not purely visual.
- Add or remove a widget or element that carries a gesture handler, key, or semantics node.
- Edit the shared token file without explicit confirmation.
- Rewrite copy, except where an empty or error state has none and the user has approved adding it.
- Introduce a new typeface, brand colour, or animation.
- Reformat files beyond the lines it changes.

## Failure modes to avoid

- Rewriting a screen when three padding values were the actual problem.
- Fixing the audit's Tier 3 findings first because they are easier.
- Inventing a token value because the ramp did not have the one you wanted.
- Deleting a wrapper for FLOW-10 without grepping for what depended on it.
- Applying light-mode fixes that break dark mode contrast. Check both.
- Producing a diff so wide that the user cannot tell appearance changes from accidental behaviour changes.
