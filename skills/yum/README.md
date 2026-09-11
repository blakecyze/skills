# Yum

Find, compare, and adapt relevant design references in one scoped pass.

## Install

```bash
npx skills@latest add blakecyze/skills --skill yum
```

For a local clone, replace `blakecyze/skills` with `.` from the repository root. Claude Code can install the library with `/plugin marketplace add blakecyze/skills` followed by `/plugin install yum@cyze`.

## Use

```text
$yum refine landing page
$yum review these references
$yum find settings-page inspiration
```

[The yum skill](skills/yum/SKILL.md) accepts optional scope, `review` or `apply`, and focus. Ordinary language works too. Reviews stay read-only; build and refinement requests authorise improvements within scope. A broad pass considers relevant areas without requiring changes everywhere.

Implicit selection is enabled: an agent can use the skill during relevant work without an explicit command. Selection depends on the host and task, so this is not a guaranteed background process. Supporting guidance loads only as needed, and the skill installs independently.

The source router checks [on.design](https://on.design/) Popular only in an already signed-in browser session. Otherwise it skips that source without starting login.

MIT. See [LICENSE](LICENSE).
