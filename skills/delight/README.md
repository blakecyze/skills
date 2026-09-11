# Delight

Refine product feedback, celebrations, characters, and progress in one scoped pass.

## Install

```bash
npx skills@latest add blakecyze/skills --skill delight
```

For a local clone, replace `blakecyze/skills` with `.` from the repository root. Claude Code can install the library with `/plugin marketplace add blakecyze/skills` followed by `/plugin install delight@cyze`.

## Use

```text
$delight onboarding
$delight review publish flow
$delight apply save feedback
```

[The delight skill](skills/delight/SKILL.md) accepts optional scope, `review` or `apply`, and focus. Ordinary language works too. Reviews stay read-only; build and refinement requests authorise improvements within scope. A broad pass considers relevant areas without requiring changes everywhere.

Implicit selection is enabled: an agent can use the skill during relevant work without an explicit command. Selection depends on the host and task, so this is not a guaranteed background process. Supporting guidance loads only as needed, and the skill installs independently.

## Focused skills

Use the broad pass for ordinary refinement. These independently installable skills serve distinct tasks; they are not additional required steps.

| Skill | Use for |
|---|---|
| [delight-character](skills/delight-character/SKILL.md) | Produce character assets and reaction states |
| [delight-habits](skills/delight-habits/SKILL.md) | Design progress qualification, rewards, and recovery |

MIT. See [LICENSE](LICENSE).
