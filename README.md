# skills

Seven skill libraries for AI coding agents: code, prose, orchestration, interface design, product delight, design research, and QA.

Each library turns judgement into a concrete decision or check: which code to delete, what makes a sentence weak, whether an animation blocks the task, or what a design reference actually proves. They work in Claude Code, Cursor, Codex, and other agents that read skill files.

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
/plugin install delight@cyze
/plugin install yum@cyze
/plugin install litmus@cyze
```

Each library also stands alone. Its own README covers tool-specific installers and configuration.

## Why use it?

- **Scoped passes.** Name the surface and the outcome; specialist detail loads when needed.
- **A check per rule.** Every rule can be evaluated against the source. If it can't, it doesn't ship.
- **Context on demand.** Standing principles stay short where a library needs them. Flow, Delight, and Yum load only for the relevant task, with supporting detail read as needed.
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

### Design refinement passes

Each pass accepts optional scope, `review` or `apply`, and focus. Use ordinary language or name the pass. Relevant guidance can activate during design work; a broad pass need not change every domain.

| Pass | Purpose |
|---|---|
| [flow](skills/flow/skills/flow/SKILL.md) | Refine layout, type, colour, controls, accessibility, copy, and motion |
| [delight](skills/delight/skills/delight/SKILL.md) | Refine product feedback, celebrations, character reactions, and progress |
| [yum](skills/yum/skills/yum/SKILL.md) | Find, compare, and adapt relevant design references |

Focused skills: [flow-motion](skills/flow/skills/flow-motion/SKILL.md), [flow-access](skills/flow/skills/flow-access/SKILL.md), [delight-character](skills/delight/skills/delight-character/SKILL.md), and [delight-habits](skills/delight/skills/delight-habits/SKILL.md). Use them for dedicated work; routine refinement stays in the broad pass.

Each includes its own resources. Installation and migration notes: [Flow](skills/flow/README.md), [Delight](skills/delight/README.md), [Yum](skills/yum/README.md).

### [litmus](skills/litmus)

Behavioural QA with evidence tied to the tested build and environment.

| Skill | Purpose |
|---|---|
| [litmus](skills/litmus/skills/litmus/SKILL.md) | Plan, run, or repair a scoped web or mobile QA pass |
| [litmus-flakes](skills/litmus/skills/litmus-flakes/SKILL.md) | Diagnose intermittent failures without retrying until green |

## Layout

```
skills/
  kanso/      code
  mimesis/    prose
  swarm/      agents
  flow/       design
  delight/    product feedback
  yum/        design research
  litmus/     QA
```

Each library is a complete Claude Code plugin with its own README, changelog, and licence. The standalone repos ([kanso](https://github.com/blakecyze/kanso), [mimesis](https://github.com/blakecyze/mimesis), [swarm](https://github.com/blakecyze/swarm)) remain live. This repo is the front door.

## Licence

MIT.
