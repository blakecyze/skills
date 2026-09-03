---
name: flow-polish
description: "Use when the user wants the full polish treatment in one command: \"polish this page\", \"make it feel finished\", \"run all the flow passes\", \"the details pass\". Runs every domain polish skill over one scope, merges the findings into one report and one approval gate."
argument-hint: "[scope: diff|module-path|all] [domains: e.g. surface,type]"
---

# flow-polish

The whole polish layer in one run. Resolves the scope once, passes it through each domain skill's checks, and merges everything into a single Flow-format report with a single approval gate. Nothing here is new: this skill sequences, it does not add rules.

## The run

1. **Gate once.** The intent gate from `flow-principles`, answered once for the scope; every domain pass inherits the answers.
2. **Load once.** `references/polish.md`, then each domain's reference as its pass begins.
3. **Sequence.** `flow-access`, `flow-layout`, `flow-type`, `flow-colour`, `flow-surface`, `flow-copy`: access first because its findings are Tier 1 by nature, copy last because wording settles once structure has. `$ARGUMENTS` may name a subset (`surface,type`); order within the subset is preserved.
4. **Merge.** One findings list, deduplicated: a finding two domains both see (an unlabelled icon button is `flow-surface`'s naming note and `flow-access`'s Tier 1) appears once, owned by the domain whose fix is structural. Tiers ordered, signal rule enforced across the merged list, one approval gate at the end.
5. **Apply by domain.** On approval, fixes land grouped by domain, one commit-able group each, so a partial `pick` stays clean.

## Boundaries

- Domain subsets exist for a reason: a copy-frozen product runs `flow-polish diff surface,type,colour,layout,access`.
- Motion is not in the default sequence; add it by name (`...,motion`) and `flow-motion`'s gate applies unchanged.
- Idempotent like its parts: a polished scope yields "polish clean, six domains checked" and stops.
- This skill never overrides a domain skill's boundary. What `flow-copy` will not touch, `flow-polish` will not touch either.
