---
name: swarm-explore
description: Use when the user wants to map a large codebase, gather context from many files at once, or investigate a problem space in parallel. Read-only fan-out. Never writes.
argument-hint: "[what to investigate: codebase|question|path]"
disable-model-invocation: true
allowed-tools: Bash(git *) Bash(rg *) Bash(find *)
---

# swarm-explore

Fan out read-only investigation across many slices at once, then synthesise. This is the highest-value swarm pattern and the safest, because reading in parallel has no side effects. Use it to build context fast: map an unfamiliar codebase, trace how a feature works across many files, or gather evidence for a question from many sources.

The principles from `swarm-principles` apply. This skill is strictly read-only.

## The hard rule

**Explore never writes.** No edits, no commits, no file creation beyond the synthesis report. Each subagent is briefed read-only. If the investigation reveals work to do, that is a separate skill's job: `/swarm-improve` to capture it as plans, or `/swarm-refine` to harden a specific artefact.

## When this earns its keep

Reading is embarrassingly parallel. Ten agents each mapping a different module return in the time one agent maps one. The merge (synthesising findings) is usually cheap because findings are additive, not competing. This is the pattern where fan-out most reliably wins.

## Process

1. **Define the question.** What are we trying to learn? "How does auth work here" is answerable. "Look at the code" is not. Sharpen it.
2. **Slice the search space.** By module, by directory, by concern, by source. Each slice should be investigable without the others.
3. **Check the cost ceiling.** More than 5 slices means confirm or batch into waves.
4. **Brief each subagent read-only.** Give it: the question, its slice (explicit paths), the report format, and the read-only boundary. Ask each to report findings, not raw dumps. A subagent that returns 2000 lines of pasted code has failed. It should return what it learned.
5. **Synthesise.** Collect the reports, reconcile overlaps, resolve contradictions (two agents disagree means dig in), and produce one coherent map.

## Subagent brief template

```
Read-only investigation. Do not edit, create, or commit anything.
Question: <the sharpened question>
Your slice: <explicit paths or sources>
Report back:
- Key findings relevant to the question (prose, not code dumps)
- Specific file:line references for anything important
- Anything surprising or contradictory
- What you could NOT determine from your slice
Keep it under <N> lines. Learnings, not transcripts.
```

## Output format

```markdown
## Exploration: <the question>

**Slices:** <N> agents across <what>

### What we found
<synthesised answer to the question, in prose>

### Map
- <area> — <what it does> (`file:line`)
- <area> — <...>

### Contradictions / open questions
- <where agents disagreed, or what none could determine>

### Cost
<N> agents, roughly <M>x a single read pass.
```

## Failure modes to avoid

- Slices that overlap heavily. You pay N times to read the same files. Slice by disjoint paths.
- Subagents returning raw code instead of findings. Brief them to synthesise.
- Letting an "explore" quietly become an "edit". The moment a change is warranted, stop and hand off.
- Fanning out a question one agent could answer by reading three files. Not everything needs a swarm.
