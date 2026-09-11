# Flow

Refine interface layout, type, colour, controls, accessibility, copy, and motion in one scoped pass.

## Install

```bash
npx skills@latest add blakecyze/skills --skill flow
```

For a local clone, replace `blakecyze/skills` with `.` from the repository root. Claude Code can install the library with `/plugin marketplace add blakecyze/skills` followed by `/plugin install flow@cyze`.

## Use

```text
$flow settings page
$flow review checkout
$flow apply dashboard type,layout
```

[The flow skill](skills/flow/SKILL.md) accepts optional scope, `review` or `apply`, and focus. Ordinary language works too. Reviews stay read-only; build and refinement requests authorise improvements within scope. A broad pass considers relevant areas without requiring changes everywhere.

Implicit selection is enabled: an agent can use the skill during relevant work without an explicit command. Selection depends on the host and task, so this is not a guaranteed background process. Supporting guidance loads only as needed, and the skill installs independently.

## Migration from 2.x

`flow` replaces the old broad and domain passes. `flow-motion` and `flow-access` remain as rewritten specialists. Use `review` for audits and an optional focus for domain passes. When upgrading, retain the new `flow`, `flow-motion`, and `flow-access` folders and remove obsolete Flow skill folders if the installer leaves them behind. Remove legacy Flow adapter blocks or rules that still point to `flow-principles`; the standalone skill now carries its references, scanners, and defaults. The old adapter installer is retired.

## Focused skills

Use the broad pass for ordinary refinement. These independently installable skills serve distinct tasks; they are not additional required steps.

| Skill | Use for |
|---|---|
| [flow-motion](skills/flow-motion/SKILL.md) | Build or diagnose a specific animation or gesture |
| [flow-access](skills/flow-access/SKILL.md) | Run a focused accessibility review or repair |

MIT. See [LICENSE](LICENSE).
