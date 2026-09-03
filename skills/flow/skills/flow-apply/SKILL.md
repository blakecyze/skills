---
name: flow-apply
description: Use when the user asks to restyle, tidy, polish, or fix the design of an interface, or to act on findings from a flow-audit report. Appearance-only; never changes behaviour.
argument-hint: "[scope: file path | audit-report | current-file]"
disable-model-invocation: true
allowed-tools: Bash(rg *) Bash(find *) Bash(python3 *)
---

# flow-apply

Behaviour-preserving repair. Fixes taxonomy violations in place using the smallest change that resolves each one.

The taxonomy and intent gate from `flow-principles` govern this skill. Load it first if it is not already loaded.

## The hard rule

**Styling changes must not alter behaviour. Behaviour changes must not ride along with styling.**

Before every edit, ask: does this change what the interface *does* for any input, or only what it *looks like*? If it changes what it does, stop and surface it as a question.

Cases where the boundary is tested:

- Changing a padding value → appearance. Proceed.
- Raising a touch target from 32 to 44 → appearance, unless it reflows siblings. Check the parent, then proceed.
- Adding a focus outline → appearance. Proceed.
- Adding an empty state that did not exist → **behaviour**. It introduces a new branch. Ask.
- Removing a container for FLOW-10 → appearance only if it carries no gesture handler, scroll, semantics node, or key. Grep before deleting.
- Demoting a second primary button → appearance. If it changes which action users take, say so in the summary.
- Changing a colour token globally → appearance, with product-wide blast radius. Ask before touching the token file.

When in doubt, treat it as behaviour and ask.

## Resolve the scope

`$ARGUMENTS` is one of:

- a file path → that file
- `audit-report` → act on a prior `flow-audit` report's Tier 1 and Tier 2 findings, in that order
- `current-file` → whatever is in focus

If no scope is given and there is no obvious focus, ask.

## Working process

1. **Resolve tokens first.** Every value written comes from the resolved token set. If a fix needs a value the set lacks, do not invent it: report a `flow-tokens` gap and skip that fix.
2. **Pass the intent gate.** Restated in the summary.
3. **List candidates before editing.** Grouped by taxonomy ID with a count. Past about ten changes, confirm scope with the user first.
4. **Fix in tier order.** Stop when the remaining findings are cosmetic and the user has not asked for cosmetics.
5. **One taxonomy ID per logical change group.** Each group independently revertible.
6. **Verify each edit.** Same behaviour for the same input, and the cited violation resolved. If not resolved, revert rather than layering on.
7. **Re-run the scanners on the touched files.** A fix that introduces a new off-scale value has traded one finding for another.

## Fix discipline

- **Subtract first.** The first candidate is removal.
- **Smallest resolving change.** A FLOW-01 finding is not licence to rewrite the layout. Change the gaps.
- **No drive-by improvements.** Note anything outside the cited findings as deferred. Do not fix it silently.
- **Preserve voice.** Match the file's formatting, property order, and naming. A restyle that also reformats is a diff nobody can read.
- **Comment optical corrections only.** FLOW-07 fixes get a one-line reason. Nothing else gets a comment.

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

## Guardrails

- Never add or remove an element that carries a gesture handler, key, or semantics node.
- Never edit the shared token file without explicit confirmation.
- Never rewrite copy, except an empty or error state that has none and the user has approved.
- Never fix Tier 3 first because it is easier.
- Check light-mode fixes against dark mode.
- Keep the diff narrow enough that appearance changes are distinguishable from accidental behaviour changes.
