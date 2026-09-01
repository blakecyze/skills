---
name: swarm-bulldoze
description: Use when the user wants to try several independent approaches to the same problem and keep the best one. Best-of-N generation. Expensive by design; respects the cost ceiling.
argument-hint: "[the task, and optionally N]"
disable-model-invocation: true
allowed-tools: Bash(git *) Bash(rg *) Bash(find *)
---

# swarm-bulldoze

Best-of-N. Spawn N independent agents on the *same* task, let each produce a full candidate solution, then select the winner. Use it when you do not know the best approach and would rather generate several and pick, than commit to one and hope. This is the most expensive pattern in the library. It is worth it when the task is high-stakes, the approaches genuinely diverge, and a wrong single-shot answer is costly to discover later.

The principles from `swarm-principles` apply. Selection is the hard part, so read the "Who judges" section before starting.

## The hard rule

**Candidates are generated in isolation. The winner is chosen from outside.** Each generating agent works without seeing the others, so the candidates are genuinely independent rather than variations on the first one. No generating agent judges its own or a sibling's work. Either the orchestrator judges, or a dedicated evaluator does.

## When this earns its keep

Best-of-N wins when the variance between attempts is high and the cost of a bad answer is real. A tricky algorithm, an architectural approach with several viable shapes, a piece of copy where tone is hard to nail first try. If every attempt would come out roughly the same, N attempts is N times the cost for nothing. Do not bulldoze low-variance tasks.

## Process

1. **Fix N.** Default 3. The user may set it. Above 5 concurrent, honour the cost ceiling (confirm, or batch into waves). More than 5 candidates rarely beats 3 to 5, so push back on large N.
2. **Write one brief, used N times.** Every agent gets the identical, self-contained task. Do not seed them differently unless the user wants deliberately varied strategies, in which case say so in each brief.
3. **Generate in parallel.** Each agent returns a complete candidate plus a one-line rationale for its approach.
4. **Decide who judges** (see `swarm-principles`). Small N and short candidates: orchestrator judges. Long candidates, large N, or bias risk: spawn one evaluator with an explicit rubric.
5. **Select and justify.** Score each candidate against the rubric on its own, then compare. Say why the winner won and why the others lost. The losing candidates sometimes contain a good idea worth grafting on. Note it if so.

## The rubric

Selection needs criteria fixed *before* seeing candidates, or you rationalise a favourite after the fact. State them up front: correctness first, then whatever the task values (simplicity, performance, readability, tone). Hand the same rubric to the evaluator if you spawn one.

## Output format

```markdown
## Bulldoze: <task>

**N:** <number> candidates
**Judge:** orchestrator | dedicated evaluator
**Rubric:** <criteria, in priority order>

### Winner
<the chosen candidate, or a pointer to where it was written>
**Why it won:** <against the rubric>

### Also considered
- **Candidate 2:** <one line on its approach and why it lost>
- **Candidate 3:** <...>

### Salvage
<any good idea from a losing candidate worth grafting onto the winner>

### Cost
<N>x a single pass, plus <evaluator cost if any>.
```

## Failure modes to avoid

- Bulldozing a low-variance task. If the attempts converge, you paid N times for one answer.
- Judging without a rubric fixed in advance. You will just pick the first one and backfill reasons.
- Comparing candidates side by side before scoring each alone. Position and length win instead of quality.
- Letting candidates see each other. They converge and the independence is lost.
- Large N. Diminishing returns set in fast and the cost ceiling exists for a reason.
- Discarding losers wholesale. Check them for a salvageable idea before binning.
