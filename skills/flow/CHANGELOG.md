# Changelog

## 2.0.0

The polish layer. Ten new skills adapting the craft substance of [jakub.kr/skills](https://jakub.kr/skills) into Flow's diagnostic form, in Flow's own words.

- Domain passes, independently invocable and idempotent, under one contract (`references/polish.md`): `flow-surface`, `flow-type`, `flow-colour`, `flow-layout`, `flow-access`, `flow-copy`. `flow-polish` runs them all with one merged report and gate.
- Workflow skills: `flow-variant` (three named directions on one axis, rendered in situ, user picks, rig deleted after), `flow-stress` (one component across every realistic scenario on a throwaway page that stays as half the report), `flow-explain` (read-only construction teardown).
- References: new `polish.md`, `surface.md`, `copy.md`; "The little things" sections appended to `type.md`, `colour.md`, `spacing.md`, `interaction.md`.
- `flow-principles`: copy boundary moved from "never rewrite copy" to "copy changes belong to `flow-copy` alone"; reference table extended. Major version for that boundary change.

## 1.2.0

- `flow-motion`: builds and audits animation. A motion gate (frequency tier plus a named purpose) that can and should produce zero lines of code, eight named violations (`FLOW-M1` to `FLOW-M8`), and a build path whose curves, durations, and spring configs are quoted from the reference, never recalled. Adapts Emil Kowalski's animation philosophy (animations.dev) into Flow's diagnostic form.
- `references/motion.md`: frequency tiers, tool ladder, easing curves, duration budgets, springs, choreography, reduced-motion and hover gates.
- `flow-principles`: one reference-layer row for motion; nothing else touched.

## 1.1.0

Context cost cut roughly in half per audit. No CLI breakage.

- `flow-principles`: taxonomy is a table; body halved
- Skills: shared boilerplate removed; `flow-audit` scans the target file, not the tree, and greps siblings instead of reading them
- Scanners: paths relative to the scanned root, `--top` cap (default 15), summary line first, singletons counted not listed
- `scan_tokens.py`: code files (`.ts`, `.js`, `.vue`, `.svelte`) need a unit or Tailwind arbitrary value before a number counts as spacing; Dart matches `EdgeInsets`, `SizedBox`, `Gap` rather than any `width:`; values under 3 are ignored as hairlines
- `contrast.py`: merges `#000`, `#000000`, `0xFF000000`, and `rgb()` into one colour; failures listed first
- `scripts/flowlib.py`: shared walk and colour parsing, prunes `node_modules` and friends before descending

## 1.0.0

First release.

- `flow-principles`: intent gate, twelve-item violation taxonomy, severity tiers
- `flow-audit`: read-only review producing a tiered findings report
- `flow-apply`: appearance-only repair with a hard behaviour boundary
- `flow-tokens`: scale discovery, writes `flow.config.json`
- Six on-demand reference files: spacing, type, colour, interaction, Flutter, web
- `contrast.py` and `scan_tokens.py`, stdlib Python, no dependencies
- Adapters for Cursor, AGENTS.md readers, and GitHub Copilot
