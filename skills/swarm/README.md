# swarm

> Run the swarm on purpose. It has to earn its keep.

Fanning a task out to a dozen agents feels powerful. Most of the time it just burns tokens for a result one careful pass would've given you. swarm is seven skills that treat parallelism as a cost, not a reflex. It goes sequential by default and only spreads out when the work is truly independent and the merge is cheap. There's a hard ceiling so it can't run away, and no agent ever grades its own homework.

## Get it

In Claude Code:

```
/plugin marketplace add blakecyze/swarm
/plugin install swarm
```

Anywhere else (Codex, Cursor, Gemini CLI, Grok Build), the skills follow the open Agent Skills standard, so one script installs them for every tool at once:

```bash
git clone https://github.com/blakecyze/swarm && swarm/scripts/install.sh
```

That symlinks each skill into `~/.agents/skills/`, plus each tool's own user dir (`~/.codex/skills`, `~/.cursor/skills`, `~/.gemini/skills`) where one exists; restart the tool afterwards. `--project`, `--copy` and `--uninstall` do what they say. Fair warning on fidelity: swarm is about parallel agents, and not every tool has them. The skills carry a capability ladder for that: native subagents where they exist (Claude Code, Grok Build), headless CLI fan-out where an agent CLI is on PATH, and honest one-at-a-time execution everywhere else. The plan and brief formats were built to survive the bottom rung.

## The skills

| Skill | What it does | How you call it |
|---|---|---|
| `swarm-principles` | The rules every swarm follows: when to fan out, the cost ceiling, who judges. | auto |
| `swarm-plan` | Breaks one task into parallel waves with a named merge. Plans, never spawns. | `/swarm-plan [task]` |
| `swarm-explore` | Read-only parallel recon. Maps a codebase or a question fast, writes nothing. | `/swarm-explore [what]` |
| `swarm-bulldoze` | Best-of-N. Several takes at the same task, one winner picked against a fixed rubric. | `/swarm-bulldoze [task] [N]` |
| `swarm-refine` | One piece, critics on separate angles, merged into a single clean revision. | `/swarm-refine [artefact]` |
| `swarm-improve` | A capable model writes plans a cheaper model can run cold. | `/swarm-improve [mode]` |
| `swarm-execute` | Hands those plans to the cheaper model and checks the work. | `/swarm-execute [plan]` |

## What it looks like

`/swarm-plan` on a chunky migration:

```markdown
## Swarm plan: migrate REST handlers to the v2 error envelope

**Verdict:** worth swarming (14 handler files, no shared state, cheap merge)

### Wave 1 (parallel, 4 slices)
- inventory: list every handler and its current error shape
- auth handlers: migrate `api/auth/*` (3 files)
- billing handlers: migrate `api/billing/*` (5 files)
- catalogue handlers: migrate `api/catalogue/*` (6 files)

### Wave 2 (needs wave 1)
- contract tests across all migrated handlers

### Cost
Roughly 4x a single pass, 4 agents at peak.
```

It tells you the cost up front, and it'll happily tell you a task isn't worth swarming at all.

## How it behaves

- **Sequential wins by default.** Fan-out only pays when the work is independent, the briefs are self-contained, and the merge is cheap. Otherwise the skills tell you to just do it straight.
- **Hard cost ceiling.** 5 agents at once by default, 6 to 10 if you confirm, above 10 refused. The cap is on concurrent agents, not total work.
- **Judging is procedural.** The rubric is fixed before any candidate is read, and every candidate is scored alone before any comparison. Agents never vote on their own work.
- **Read wide, write narrow.** Critics and explorers fan out. Edits land in one pass.
- **Plans are written for strangers.** `/swarm-improve` spends the smart model on judgement and bottles it into plans a context-free cheap model can run. If the executor gets stuck, that's a bug in the plan, not the executor.
- **Nothing spawns on its own.** Only `swarm-principles` auto-loads. The six verbs are all manual.

## The family

Same "earn your keep" idea, aimed at different work:

- [kanso](https://github.com/blakecyze/kanso) does it for code. It cuts the slop out of what Claude writes.
- [mimesis](https://github.com/blakecyze/mimesis) does it for writing and design. It strips the tells that read as AI.

## Chip in

Modes are arguments, not new skills. If you can't say a skill's trigger in one sentence, it's a note, not a skill. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Licence

MIT.
