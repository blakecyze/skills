---
name: swarm-plan
description: Use when the user wants to break a large task into parallel workstreams, plan a multi-agent job, or decide what can run concurrently. Produces an orchestration plan, does not execute it.
argument-hint: "[the task to decompose]"
disable-model-invocation: true
allowed-tools: Bash(git *) Bash(rg *) Bash(find *)
---

# swarm-plan

Decompose a large task into an orchestration plan: which work is parallel, which is sequential, and where the merge happens. This skill plans. It does not spawn agents. Handing execution to `/swarm-bulldoze`, `/swarm-explore`, or manual orchestration is a separate step the user takes after seeing the plan.

The principles from `swarm-principles` apply. In particular: sequential is the default, and each parallel slice must be independent and self-contained.

## The job

Turn one big ask into a dependency graph of workstreams, tagged by what can run at once. The output is a plan the user can eyeball before spending a single subagent token.

## Process

1. **Restate the task in one line.** If you cannot, it is too vague to plan. Ask.
2. **List the atomic workstreams.** The smallest units of work that produce something usable on their own.
3. **Draw the dependencies.** For each workstream, what must finish before it can start? A workstream with no upstream dependency is a candidate for the first parallel wave.
4. **Group into waves.** Wave 1 is everything with no dependencies. Wave 2 is everything that depends only on wave 1. And so on. Within a wave, work runs concurrently.
5. **Check each wave against the cost ceiling.** If a wave has more than 5 concurrent slices, either confirm with the user or split the wave.
6. **Name the merge.** After the last wave, how do the outputs combine into the deliverable? If you cannot name a cheap merge, the decomposition is wrong. Reconsider.

## Honesty check

Before presenting the plan, ask: is this actually faster than one sequential pass? If the waves are deep (lots of sequential dependency) and the parallel width is thin, the swarm buys almost nothing. Say so. A good outcome of this skill is sometimes "don't swarm this, just do it straight."

## Output format

```markdown
## Swarm plan: <task in one line>

**Verdict:** <worth swarming | marginal | just do it sequentially, because ...>

### Wave 1 (parallel, N slices)
- **<slice name>** — <what it does, what it outputs>
- **<slice name>** — <...>

### Wave 2 (depends on wave 1)
- **<slice name>** — <needs: slice X output>

### Merge
<how the wave outputs combine into the deliverable, and who judges if selection is involved>

### Cost
Roughly <N>x a single pass, peak <M> concurrent agents.

### Next step
Run `/swarm-explore` for the read-heavy slices, or spawn wave 1 manually with these briefs: <one-line brief per slice>
```

## Failure modes to avoid

- Planning parallelism that does not exist. If everything depends on everything, it is a sequential task wearing a swarm costume.
- Ignoring the merge until the end and discovering it is the expensive part.
- Producing waves wider than the cost ceiling without flagging it.
- Executing. This skill stops at the plan. It never spawns.
