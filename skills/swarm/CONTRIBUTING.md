# Contributing

swarm is deliberately small. Modes are arguments, not new skills. A new skill has to earn its place against the cost of every session reading its description.

## Proposing a new skill

Open an issue first. A skill proposal should fit in one sentence: the trigger condition and the job it does. If you can't write that sentence, the skill probably isn't a skill yet.

Before proposing, check that the job isn't already an argument to an existing skill. `review-plan` is `/swarm-refine` pointed at a plan file, not a new skill. Overlap is worse than a gap.

## Testing

Use the skill on a real codebase before opening a PR. Fan out against something large enough that a swarm actually earns its keep; if a single sequential pass would have been cheaper, the example proves the opposite of what you want.

Respect the cost ceiling while testing. Load the plugin locally with `claude --plugin-dir .` and exercise every trigger path in the description.

## PR expectations

Match the voice of the existing skills and this README. UK spelling. No filler, no hedging, no corporate prose. If you're unsure, read an existing `SKILL.md` and imitate.

Keep PRs focused. One skill per PR. Refactor and behaviour change don't share a commit.
