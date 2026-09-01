# Contributing

kanso is deliberately small. The bias is toward deletion. A new skill has to earn its place.

## Proposing a new skill

Open an issue first. A skill proposal should fit in one sentence: the trigger condition and the job it does. If you can't write that sentence, the skill probably isn't a skill yet.

Before proposing, check that the job isn't already covered by an existing skill. Overlap is worse than a gap.

## Testing

Use the skill on a real codebase before opening a PR. Dogfood on something messy, not a toy example. If the skill only works on clean code, it doesn't work.

Load the plugin locally with `claude --plugin-dir .` and exercise every trigger path in the description. The dogfood scenarios in `evals/evals.json` are the baseline: run the ones for any skill you touched.

Run `scripts/lint-skills.sh` before opening a PR. It checks frontmatter, trigger-shaped descriptions, line ceilings, and house style.

## PR expectations

Match the voice of the existing skills and this README. UK spelling. No em dashes. No filler, no hedging, no corporate prose. If you're unsure, read an existing `SKILL.md` and imitate.

Keep PRs focused. One skill per PR. Refactor and behaviour change don't share a commit.

Frontmatter changes without body changes are fine. Body changes without frontmatter changes are fine. Both together get more scrutiny.
