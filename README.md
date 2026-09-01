# skills

Four skill libraries for AI coding agents, built on one idea: name the failure, give it a check, keep the always-loaded layer short.

A principle without a check is an opinion, and opinions do not survive contact with a diff. Every library here turns its domain's judgement calls into named, searchable violations that a model can be held to — across Claude Code, Cursor, Codex, and anything else that reads a file.

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

Each library also stands alone — see its own README for tool-specific installers and configuration.

## Why use it?

Models already know the words for good code, good prose, and good design. Reciting principles at them changes nothing. These libraries work because each one:

- **Names its failures.** `FLOW-06` means the same thing in every session and every tool.
- **Gives every rule a check** that can be evaluated against the source, not vibes.
- **Keeps the standing layer short.** The always-loaded principles fit on a page; everything else loads on demand.
- **Computes what can be computed.** Contrast ratios and scale membership come from scripts, never from memory.

## Reference

### [kanso](skills/kanso) — code

Keeps AI-written code short and honest. Delete before you add, earn every line.

| Skill | Does |
|---|---|
| [kanso-principles](skills/kanso/skills/kanso-principles/SKILL.md) | Standing anti-dilution rules for all code work. Auto-loads. |
| [kanso-audit](skills/kanso/skills/kanso-audit/SKILL.md) | Code review and pattern analysis of a diff, branch, or codebase |
| [kanso-refactor](skills/kanso/skills/kanso-refactor/SKILL.md) | Clean up, tighten, and de-bloat code |
| [kanso-nuclear](skills/kanso/skills/kanso-nuclear/SKILL.md) | Deep structural audit of a whole codebase |
| [kanso-task](skills/kanso/skills/kanso-task/SKILL.md) | Sharpen a rough request before running it, carefully |
| [kanso-commit](skills/kanso/skills/kanso-commit/SKILL.md) | Stage work and split it into logical commits |
| [kanso-pr](skills/kanso/skills/kanso-pr/SKILL.md) | Pull request descriptions and branch summaries |
| [kanso-context](skills/kanso/skills/kanso-context/SKILL.md) | Create and prune AGENTS.md / CLAUDE.md files |
| [kanso-prompting](skills/kanso/skills/kanso-prompting/SKILL.md) | Rules for writing better prompts for frontier models |

### [mimesis](skills/mimesis) — prose

Strips AI tells from writing for human readers, and compiles token-efficient instructions for machine readers.

| Skill | Does |
|---|---|
| [mimesis-principles](skills/mimesis/skills/mimesis-principles/SKILL.md) | Standing anti-tell rules for all generated prose. Auto-loads. |
| [mimesis-human](skills/mimesis/skills/mimesis-human/SKILL.md) | Audit, rewrite, or generate text that reads as human |
| [mimesis-concise](skills/mimesis/skills/mimesis-concise/SKILL.md) | Shorter and denser without losing meaning |
| [mimesis-tone](skills/mimesis/skills/mimesis-tone/SKILL.md) | Five named voices: persuasive, practitioner, warm, blunt, plain |
| [mimesis-design](skills/mimesis/skills/mimesis-design/SKILL.md) | Spot and strip machine-made design tells from an interface |
| [mimesis-compile](skills/mimesis/skills/mimesis-compile/SKILL.md) | Dense, structured instructions for machine readers |

### [swarm](skills/swarm) — orchestration

Fans work out to parallel agents, picks winners, and delegates execution to cheaper models, under a hard cost ceiling.

| Skill | Does |
|---|---|
| [swarm-principles](skills/swarm/skills/swarm-principles/SKILL.md) | Standing rules for when to fan out and when not to. Auto-loads. |
| [swarm-explore](skills/swarm/skills/swarm-explore/SKILL.md) | Read-only parallel fan-out over a large codebase |
| [swarm-plan](skills/swarm/skills/swarm-plan/SKILL.md) | Break a large task into parallel workstreams |
| [swarm-improve](skills/swarm/skills/swarm-improve/SKILL.md) | Audit a codebase for latent work and capture it as a backlog |
| [swarm-execute](skills/swarm/skills/swarm-execute/SKILL.md) | Run planned work through cheaper models |
| [swarm-bulldoze](skills/swarm/skills/swarm-bulldoze/SKILL.md) | Best-of-N: try several approaches, keep the winner |
| [swarm-refine](skills/swarm/skills/swarm-refine/SKILL.md) | Parallel critics attack one artefact from several angles |

### [flow](skills/flow) — design

Diagnostic, not generative. Passes an intent gate before touching styling, cites findings from a twelve-item taxonomy, and computes contrast and scale adherence rather than estimating them.

| Skill | Does |
|---|---|
| [flow-principles](skills/flow/skills/flow-principles/SKILL.md) | Intent gate and the twelve-item violation taxonomy. Auto-loads. |
| [flow-audit](skills/flow/skills/flow-audit/SKILL.md) | Read-only design review with a tiered findings report |
| [flow-apply](skills/flow/skills/flow-apply/SKILL.md) | Repairs violations, appearance only |
| [flow-tokens](skills/flow/skills/flow-tokens/SKILL.md) | Discovers a project's real scale, writes `flow.config.json` |

## Layout

```
skills/
  kanso/      code   — anti-dilution principles, audits, refactors
  mimesis/    prose  — anti-tell rules, humanising, prompt compiling
  swarm/      agents — parallel fan-out, winner-picking, delegation
  flow/       design — intent gate, violation taxonomy, computed checks
```

Each library is a complete Claude Code plugin with its own README, changelog, and licence. The standalone repos ([kanso](https://github.com/blakecyze/kanso), [mimesis](https://github.com/blakecyze/mimesis), [swarm](https://github.com/blakecyze/swarm)) remain live; this repo is the front door.

## Licence

MIT.
