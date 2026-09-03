---
name: flow-copy
description: "Use when the user wants interface strings polished: vague buttons, blaming error messages, dead-end empty states, inconsistent capitalisation or terminology, toggles labelled backwards. Also \"fix the microcopy\", \"better error messages\", \"the labels are confusing\". One domain: interface strings, and the only Flow skill allowed to change them."
argument-hint: "[scope: diff|module-path|all]"
---

# flow-copy

The polish pass for words in the interface, and the one Flow skill with licence to change a string. Runs under the contract in `references/polish.md`; the rules live in `references/copy.md`. Load both now.

## The checks

1. **Verb-less buttons.** "OK", "Yes", "Submit" on consequential actions; confirmations that do not repeat the consequence.
2. **Unhelpful errors.** Messages that name the failure but not the fix, blame the user, sit far from the failed field, or end in an exclamation mark.
3. **Dead-end empty states.** "No results" with no orientation and no action.
4. **Context-blind links.** "Click here" and bare "Learn more".
5. **Backwards toggles.** Labels describing the OFF state.
6. **Drift.** Two capitalisation policies for one element type; two terms for one concept; "we" in error messages.
7. **Misplaced tone.** Playfulness in error or destructive paths; ceremony in routine ones.
8. **Placeholder abuse.** Format hints doing a label's job; the structural half of that finding belongs to `flow-access`.

## Boundaries

- Interface strings only: labels, errors, empty states, tooltips, confirmations. Marketing prose, docs, and long-form content are out of scope; for those, point at a writing tool, not this skill.
- Meaning is preserved. A copy fix changes wording, never what the action does or which options exist.
- Voice matching: read the product's existing strings first; a coherent voice that is not to Flow's taste is not a finding (the core preserve-voice rule).
- Idempotent: a clean second run reports "copy clean" in one line and stops.
