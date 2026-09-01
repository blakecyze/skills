---
name: swarm-refine
description: Use when the user has one artefact (code, doc, design, plan) and wants it hardened by attacking it from several angles at once. Parallel critics, then merge. Not to be confused with bulldoze, which generates many solutions.
argument-hint: "[the artefact to refine]"
disable-model-invocation: true
allowed-tools: Bash(git *) Bash(rg *) Bash(find *)
---

# swarm-refine

Take one artefact and improve it by fanning out critics, each attacking a different axis at once, then merging their findings into a single revision. Where `/swarm-bulldoze` generates many solutions and keeps one, refine starts from one solution and makes it better. Use it to harden something that already exists: a function, a document, a design, an API. A plan document is an artefact too; reviewing a plan is this skill pointed at the plan file, not a separate skill.

The principles from `swarm-principles` apply. The artefact is shared, so critics read in parallel but changes are applied sequentially.

## bulldoze vs refine

Easy to conflate, so be clear which you want:

- **bulldoze** — many candidates for the same task, pick the best. Use when you have no solution yet.
- **refine** — one existing artefact, many critics, one improved version. Use when you have a solution and want it stronger.

If the user has a draft, it is almost always refine.

## The hard rule

**Critics run in parallel and read-only. Changes apply sequentially.** Multiple agents editing the same artefact at once corrupt each other. Critics produce critiques, not edits. The orchestrator (or a single editing pass) applies the merged critique afterwards, resolving conflicts between critics on the way.

## Process

1. **Pick the axes.** Each critic attacks one concern, so they do not overlap. Typical axes: correctness, performance, security, readability, edge cases, style/consistency. Choose the ones that matter for this artefact. Three to five is usually right.
2. **Check the cost ceiling.** One critic per axis. Above 5 axes, prune to the ones that matter or batch.
3. **Brief each critic on its single axis.** Give it the full artefact, its one concern, and a read-only boundary. Ask for specific, actionable findings with locations, not vibes. "This could be cleaner" is useless. "Line 40 swallows the error; propagate it" is actionable.
4. **Collect and de-conflict.** Critics will sometimes contradict (the performance critic wants caching, the readability critic wants the caching gone). Resolve these explicitly against the artefact's actual priorities. Do not blindly apply every suggestion.
5. **Apply as one coherent revision.** Merge the accepted findings into a single improved version. Preserve the artefact's voice. A refined artefact should read as though one careful author wrote it, not as a patchwork of five critics.

## Critic brief template

```
Read-only critique. Do not edit the artefact.
Artefact: <inline or path>
Your axis: <correctness | performance | security | readability | edge cases | ...>
Attack ONLY your axis. Ignore concerns outside it; another critic owns them.
Report back:
- Specific findings with locations (file:line or section)
- For each: what is wrong and the concrete fix
- Severity (blocking | worth fixing | nitpick)
Actionable only. No vague impressions.
```

## Output format

```markdown
## Refine: <artefact>

**Axes:** <list of critics run>

### Applied
- **[correctness]** <finding> → <fix applied> (`file:line`)
- **[security]** <...>

### Conflicts resolved
- <critic A wanted X, critic B wanted Y; chose X because ...>

### Declined
- <finding not applied, and why>

### Result
<the refined artefact, or a pointer to it>

### Cost
<N> critics, roughly <M>x a single review pass.
```

## Failure modes to avoid

- Critics with overlapping axes. They report the same issues and you pay twice. Keep axes disjoint.
- Applying every suggestion blindly. Critics contradict; judgement is required. Decline what does not fit.
- Parallel edits to the artefact. Critique in parallel, edit in one pass.
- Losing the artefact's voice under a pile of patches. Merge coherently.
- Reaching for refine when there is no artefact yet. That is bulldoze.
