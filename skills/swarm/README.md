# swarm

> Deliberate agent orchestration. Sequential by default; the swarm has to earn its keep.

Seven Claude Code skills for running agent swarms on purpose. Where [kanso](https://github.com/blakecyze/kanso) restrains, swarm spends: it fans work out in parallel or hands execution to a cheaper model, but only when a single sequential pass would cost you more. A hard ceiling keeps it from running away, and nothing judges its own work.

```
/plugin marketplace add blakecyze/swarm
/plugin install swarm
```

&nbsp;

## The skills

| Skill | What it does | Invocation |
|---|---|---|
| `swarm-principles` | Standing rules for every swarm: when to fan out, the cost ceiling, who judges. Loaded automatically. | auto |
| `swarm-plan` | Decomposes one task into parallel waves with dependencies and a named merge. Plans, never spawns. | `/swarm-plan [task]` |
| `swarm-explore` | Read-only parallel investigation. Maps a codebase or question space fast. Never writes. | `/swarm-explore [what]` |
| `swarm-bulldoze` | Best-of-N. Independent candidates for the same task, one winner picked against a pre-fixed rubric. | `/swarm-bulldoze [task] [N]` |
| `swarm-refine` | One artefact, parallel critics on disjoint axes, merged into one coherent revision. | `/swarm-refine [artefact]` |
| `swarm-improve` | Capable-model audit that writes self-contained plans a cheaper model can execute cold. | `/swarm-improve [mode]` |
| `swarm-execute` | Dispatches those plans to a cheaper model, one subagent per plan, and verifies acceptance. | `/swarm-execute [plan]` |

&nbsp;

## What it looks like

**`/swarm-plan` output:**

```markdown
## Swarm plan: migrate the REST handlers to the v2 error envelope

**Verdict:** worth swarming (14 handler files, no shared state, cheap merge)

### Wave 1 (parallel, 4 slices)
- **inventory**: list every handler and its current error shape
- **auth handlers**: migrate `api/auth/*` (3 files)
- **billing handlers**: migrate `api/billing/*` (5 files)
- **catalogue handlers**: migrate `api/catalogue/*` (6 files)

### Wave 2 (depends on wave 1)
- **contract tests**: needs all migrated handlers

### Merge
Additive; one review pass over the combined diff. No selection involved.

### Cost
Roughly 4x a single pass, peak 4 concurrent agents.
```

&nbsp;

**The improve → execute pair:**

```
/swarm-improve branch        # capable model audits, writes plans/<slug>.md
/swarm-execute plans/        # cheap model executes them cold, verifies acceptance
```

Every plan has to run cold, with zero prior context. If the executor gets stuck, that's a defect in the plan, not the executor. Fix the format and send it back; don't patch it with knowledge only the session had.

&nbsp;

## Install

Plugin (recommended):

```
/plugin marketplace add blakecyze/swarm
/plugin install swarm
```

Manual, personal scope:

```bash
git clone https://github.com/blakecyze/swarm ~/swarm
mkdir -p ~/.claude/skills
cp -r ~/swarm/skills/* ~/.claude/skills/
```

Manual, project scope:

```bash
mkdir -p .claude/skills
cp -r path/to/swarm/skills/* .claude/skills/
```

Skills load on next session, or immediately via the file watcher.

&nbsp;

## How it behaves

- **Sequential is the default.** Fan-out trades tokens for wall-clock time and breadth; it only wins when the work is independent, the briefs are self-contained, and the merge is cheap. Otherwise the skills tell you to just do it straight.
- **Hard cost ceiling.** 5 concurrent subagents by default, 6–10 with your confirmation, above 10 refused. The cap is on concurrent agents, not total work.
- **Judging is procedural.** Rubric fixed before any candidate is read; each candidate scored alone before any side-by-side comparison. Generating agents never vote on their own work.
- **Read-parallel, write-sequential.** Critics and explorers fan out; edits land in one pass. Executors only run in parallel when their plans touch disjoint files.
- **Plans are written for strangers.** `/swarm-improve` spends the capable model on judgement and captures it in plans a context-free cheap model can run; `/swarm-execute` proves it by dispatching them cold.
- **Everything that spawns is manual-only.** Only `swarm-principles` auto-loads; the six verbs never auto-invoke.

&nbsp;

## Contributing

Modes are arguments, not new skills. If you can't describe a skill's trigger in one sentence, it's a note, not a skill. See [CONTRIBUTING.md](CONTRIBUTING.md).

&nbsp;

## License

MIT.
