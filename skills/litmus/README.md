# Litmus

Test the behaviour that matters, reproduce failures, and report what the evidence supports. One broad QA pass and one specialist for intermittent failures.

## Install

```bash
npx skills@latest add blakecyze/skills --skill litmus litmus-flakes
```

For a local clone, replace `blakecyze/skills` with `.` from the repository root. Claude Code can use `/plugin marketplace add blakecyze/skills` followed by `/plugin install litmus@cyze`.

## Use

| Skill | Example |
|---|---|
| [litmus](skills/litmus/SKILL.md) | `$litmus check checkout regression` |
| [litmus-flakes](skills/litmus-flakes/SKILL.md) | `$litmus-flakes investigate the intermittent login timeout` |

The broad pass accepts optional scope, `plan`, `check`, or `fix`, and focus. Ordinary language works too. It can be selected during relevant feature verification; invocation depends on the host and task. A check exercises the product without editing it. A fix request includes reproduction, repair, and verification.

Litmus reuses the project's tools and keeps coverage proportional to risk. It does not require a new runner, evidence-pack pipeline, or approval ritual. Both skills install independently.

Flow refines interface presentation; Litmus exercises behaviour and recovery. Dedicated accessibility repair belongs with Flow's access specialist. Litmus can report a failed access path without turning every QA pass into a full accessibility audit.

Validation scenarios live in `evals/evals.json`. They require judging actual agent work; static validation does not execute them.

MIT. See [LICENSE](LICENSE).
