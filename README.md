# skills

Four skill libraries for AI coding agents, built on one idea: name the failure, give it a check, keep the always-loaded layer short.

Models already know the words for good code, good prose, and good design. Reciting principles at them changes nothing, because a principle without a check is an opinion, and opinions do not survive contact with a diff. So each library here turns its domain's judgement calls into named, checkable violations that a model can be held to. They work in Claude Code, Cursor, Codex, and anything else that reads a file.

## Install

```bash
npx skills@latest add blakecyze/skills
```

Or, in Claude Code, install any library as a plugin:

```
/plugin marketplace add blakecyze/skills
/plugin install kanso@cyze
/plugin install mimesis@cyze
/plugin install swarm@cyze
/plugin install flow@cyze
```

Each library also stands alone. Its own README covers tool-specific installers and configuration.

## Why use it?

- **Named failures.** `FLOW-06` means the same thing in every session and every tool, so findings stay searchable across weeks of work.
- **A check per rule.** Every rule can be evaluated against the source. If it can't, it doesn't ship.
- **A short standing layer.** The always-loaded principles fit on a page. Everything else loads on demand, when a finding needs it.
- **Computed numbers.** Contrast ratios and scale membership come from scripts. A guessed number is a fabricated one.

## Reference

### [kanso](skills/kanso)

Code. Keeps AI-written output short and honest: delete before you add, earn every line.

| Skill | Does |
|---|---|
| [kanso-principles](skills/kanso/skills/kanso-principles/SKILL.md) | Standing anti-dilution rules for all code work. Auto-loads. |
| [kanso-audit](skills/kanso/skills/kanso-audit/SKILL.md) | Code review and pattern analysis of a diff, branch, or codebase |
| [kanso-council](skills/kanso/skills/kanso-council/SKILL.md) | The audit run by every agent CLI on the machine, merged by consensus |
| [kanso-refactor](skills/kanso/skills/kanso-refactor/SKILL.md) | Clean up, tighten, and de-bloat code |
| [kanso-nuclear](skills/kanso/skills/kanso-nuclear/SKILL.md) | Deep structural audit of a whole codebase |
| [kanso-task](skills/kanso/skills/kanso-task/SKILL.md) | Sharpen a rough request before running it, carefully |
| [kanso-commit](skills/kanso/skills/kanso-commit/SKILL.md) | Stage work and split it into logical commits |
| [kanso-pr](skills/kanso/skills/kanso-pr/SKILL.md) | Pull request descriptions and branch summaries |
| [kanso-context](skills/kanso/skills/kanso-context/SKILL.md) | Create and prune AGENTS.md / CLAUDE.md files |
| [kanso-handoff](skills/kanso/skills/kanso-handoff/SKILL.md) | Packs the session into one file so `/clear` costs nothing |
| [kanso-prompting](skills/kanso/skills/kanso-prompting/SKILL.md) | Rules for writing better prompts for frontier models |

### [mimesis](skills/mimesis)

Prose. Strips AI tells from writing meant for people, and compiles token-efficient instructions for machines. This README went through it.

| Skill | Does |
|---|---|
| [mimesis-principles](skills/mimesis/skills/mimesis-principles/SKILL.md) | Standing anti-tell rules for all generated prose. Auto-loads. |
| [mimesis-human](skills/mimesis/skills/mimesis-human/SKILL.md) | Audit, rewrite, or generate text that reads as human |
| [mimesis-concise](skills/mimesis/skills/mimesis-concise/SKILL.md) | Shorter and denser without losing meaning |
| [mimesis-tone](skills/mimesis/skills/mimesis-tone/SKILL.md) | Five named voices: persuasive, practitioner, warm, blunt, plain |
| [mimesis-design](skills/mimesis/skills/mimesis-design/SKILL.md) | Spot and strip machine-made design tells from an interface |
| [mimesis-compile](skills/mimesis/skills/mimesis-compile/SKILL.md) | Dense, structured instructions for machine readers |

### [swarm](skills/swarm)

Orchestration. Fans work out to parallel agents, picks winners, and delegates execution to cheaper models, all under a hard cost ceiling.

| Skill | Does |
|---|---|
| [swarm-principles](skills/swarm/skills/swarm-principles/SKILL.md) | Standing rules for when to fan out and when not to. Auto-loads. |
| [swarm-explore](skills/swarm/skills/swarm-explore/SKILL.md) | Read-only parallel fan-out over a large codebase |
| [swarm-plan](skills/swarm/skills/swarm-plan/SKILL.md) | Break a large task into parallel workstreams |
| [swarm-improve](skills/swarm/skills/swarm-improve/SKILL.md) | Audit a codebase for latent work and capture it as a backlog |
| [swarm-execute](skills/swarm/skills/swarm-execute/SKILL.md) | Run planned work through cheaper models |
| [swarm-bulldoze](skills/swarm/skills/swarm-bulldoze/SKILL.md) | Best-of-N: try several approaches, keep the winner |
| [swarm-refine](skills/swarm/skills/swarm-refine/SKILL.md) | Parallel critics attack one artefact from several angles |

### [flow](skills/flow)

Design. Diagnostic, not generative: it passes an intent gate before touching styling, cites findings from a twelve-item taxonomy, and computes contrast and scale adherence rather than estimating them.

| Skill | Does |
|---|---|
| [flow-principles](skills/flow/skills/flow-principles/SKILL.md) | Intent gate and the twelve-item violation taxonomy. Auto-loads. |
| [flow-audit](skills/flow/skills/flow-audit/SKILL.md) | Read-only design review with a tiered findings report |
| [flow-apply](skills/flow/skills/flow-apply/SKILL.md) | Repairs violations, appearance only |
| [flow-tokens](skills/flow/skills/flow-tokens/SKILL.md) | Discovers a project's real scale, writes `flow.config.json` |
| [flow-motion](skills/flow/skills/flow-motion/SKILL.md) | Builds and audits animation via a gate and the FLOW-M taxonomy |
| [flow-polish](skills/flow/skills/flow-polish/SKILL.md) | Runs every domain polish pass over one scope, one gate |
| [flow-surface](skills/flow/skills/flow-surface/SKILL.md) | Radii, optical alignment, depth, icons, press feedback, hit areas |
| [flow-type](skills/flow/skills/flow-type/SKILL.md) | Size floors, wrapping, tabular numbers, truncation, underlines |
| [flow-colour](skills/flow/skills/flow-colour/SKILL.md) | Ramps, tokens, OKLCH, gradients, measured contrast, dark mode |
| [flow-layout](skills/flow/skills/flow-layout/SKILL.md) | Edges, control affordance, disclosure cues, adaptivity |
| [flow-access](skills/flow/skills/flow-access/SKILL.md) | Focus, keyboard parity, targets, forms, live regions, structure |
| [flow-copy](skills/flow/skills/flow-copy/SKILL.md) | Buttons, errors, empty states, toggles; the only string editor |
| [flow-variant](skills/flow/skills/flow-variant/SKILL.md) | Three named design directions on one axis, rendered in situ |
| [flow-stress](skills/flow/skills/flow-stress/SKILL.md) | One component across every realistic scenario on a throwaway page |
| [flow-explain](skills/flow/skills/flow-explain/SKILL.md) | Takes an interface apart in words; teaches, changes nothing |

## Layout

```
skills/
  kanso/      code
  mimesis/    prose
  swarm/      agents
  flow/       design
```

Each library is a complete Claude Code plugin with its own README, changelog, and licence. The standalone repos ([kanso](https://github.com/blakecyze/kanso), [mimesis](https://github.com/blakecyze/mimesis), [swarm](https://github.com/blakecyze/swarm)) remain live. This repo is the front door.

## Licence

MIT.
