---
name: swarm-principles
description: Use when orchestrating subagents, fanning work out in parallel, or running any /swarm-* skill. Sets standing rules for when to fan out, when not to, cost ceilings, and who judges. Auto-loads; not directly invoked by the user.
user-invocable: false
---

# swarm-principles

The shared spine for the swarm library. Where kanso restrains, this library spends. That is deliberate. But brute force without discipline is just waste, so these rules decide when the spend is worth it and keep it from running away.

Every `/swarm-*` skill inherits this. Read it once per session before fanning out.

## The one honest premise

Fan-out is not magic and it is not always faster. It trades tokens and coordination overhead for wall-clock time and breadth. It only wins when the work is genuinely parallel and the merge is cheap. If either of those fails, a single sequential pass beats a swarm on every axis. Assume sequential is the default and make the swarm earn its keep.

## When to fan out

Fan out only when all three hold:

1. **The work decomposes into independent slices.** No slice needs another slice's output mid-flight. Shared mutable state kills parallelism.
2. **The slices are self-contained.** Each subagent can be handed a brief that stands alone, with no assumption about context the orchestrator holds. Subagents do not share your context window. Spell out everything they need.
3. **The merge is cheaper than the work.** Synthesising N reports, or picking one winner from N candidates, must cost less than doing the work sequentially. If merging is the hard part, you have not saved anything.

## When not to fan out

- **Coherent writing or editing.** One voice, one artefact. Fan-out fragments it and you spend the savings stitching seams. Sequential.
- **Cheap tasks.** If the whole job is a few thousand tokens sequential, a swarm's coordination overhead costs more than it saves.
- **Tight data dependencies.** If slice B needs slice A's result, they are not parallel. Chain them.
- **Anything with side effects on shared resources.** Parallel writes to the same file, table, or branch corrupt each other. Read-parallel, write-sequential.

## The cost ceiling

Swarms burn tokens fast. Every skill in this library respects a hard ceiling:

- **Default cap: 5 concurrent subagents.** Below this, proceed.
- **6 to 10: confirm with the user first.** State the rough cost multiple ("this is roughly 8x a single pass").
- **Above 10: refuse unless the user has explicitly set a higher cap this session.** Suggest they narrow the task instead.

The ceiling is on *concurrent* agents. A plan that runs 4 agents in three sequential waves is 12 total but never breaches the cap. That is fine. The cap protects context and cost blow-ups, not total work.

## Who judges

`/swarm-bulldoze` (best-of-N) and `/swarm-refine` (parallel critics) both produce multiple outputs that must be reduced to one. Selection, not fan-out, is the hard part. Decide up front:

- **Orchestrator judges** when N is small (<=4) and every candidate is short (roughly 150 lines or less). Cheaper, no extra agent, and the orchestrator already has the task context. Default.
- **Dedicated evaluator agent** when any candidate is long, when N is 5 or more, when the orchestrator has already voiced a preferred approach this session (its judgement is anchored), or when candidates must be run or tested to compare. Spawn one evaluator, hand it all candidates plus the rubric, take its ranking.

Whoever judges follows the same procedure, because judge sloppiness is a procedure failure, not a threshold failure:

1. **Fix the rubric before reading any candidate.** Criteria chosen after seeing the field are rationalisation, not judgement.
2. **Score each candidate against the rubric on its own, before any side-by-side comparison.** Holistic "which do I like" comparison rewards whichever came first and whichever is longest. Scorecards first, comparison second.
3. **Justify the pick against the rubric**, and say why the others lost.

Never let the generating agents vote on their own work. Either the orchestrator judges from outside, or a fresh evaluator does.

## Briefing subagents

A subagent is a stranger. It has none of your context. A good brief states: the exact task, the inputs (inline or by path, never "the file we discussed"), the output format expected, and the boundary (read-only? which paths? what not to touch). Vague briefs produce divergent junk that the merge step cannot reconcile.

## Reporting back

Every swarm skill ends with a short synthesis: what was fanned out, how many agents, what came back, what was kept or discarded and why, and the rough cost. The user is spending real tokens on this. Show them what they bought.
