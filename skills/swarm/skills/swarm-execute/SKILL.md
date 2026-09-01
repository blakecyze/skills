---
name: swarm-execute
description: Use when the user wants to run plans written by /swarm-improve, execute a plans/ backlog, or dispatch mechanical work to a cheaper model. The pair of /swarm-improve: it planned, this executes.
argument-hint: "[plans/<slug>.md | plans/ | --model <alias>]"
disable-model-invocation: true
allowed-tools: Bash(git *) Bash(rg *) Bash(find *)
---

# swarm-execute

Dispatch plans written by `/swarm-improve` to a cheaper model. The judgement was spent when the plan was written; what remains is mechanical, so it runs on the cheapest model that can follow instructions. One subagent per plan, briefed with the plan file and nothing else.

The principles from `swarm-principles` apply. This is the execution half of tier-and-time delegation: capable model planned then, cheap model executes now.

## The hard rule

**The executor gets the plan file and nothing else.** No session context, no audit summary, no "as we discussed". The plan was written to be executable cold; executing it cold is the only honest test of that. If the executor gets stuck on something the plan does not answer, that is a plan-format defect. Report it back as `/swarm-improve` feedback and stop. Do not patch the gap with orchestrator knowledge, because that hides the defect until the day nobody is watching.

## Model choice

Dispatch each plan on a cheap model: pass `model: haiku` (or the cheapest available alias) when spawning the subagent. `--model <alias>` overrides. If the harness cannot set a per-subagent model, say so and dispatch at the session model; the plans still pay off, they are just not cheaper.

Without this plugin, the same dispatch works headless: `claude -p "Execute the plan in plans/<slug>.md exactly. Touch nothing outside its Files and Out of scope sections." --model haiku`.

## Process

1. **Resolve the target.** One plan file, or a `plans/` directory. For a directory, list the plans and their priorities; execute in priority order. Skip plans marked done or blocked.
2. **Pre-flight each plan.** It must have Why, Files, Steps, Acceptance, Out of scope, and every path in Files must be absolute. A relative path is ambiguous to a context-free executor and has caused real misfires: it searches for a matching filename and can silently edit the wrong tree. A plan missing any of these, or using relative paths, goes back to `/swarm-improve reconcile`, not to an executor.
3. **Sequence by file overlap.** Plans whose `Files` sections are disjoint may run in parallel, up to the cost ceiling. Any overlap means sequential, in priority order. When unsure, sequential; parallel writes to shared files corrupt each other.
4. **Dispatch.** Each executor is briefed: the plan file path, "execute it exactly", the boundary ("touch nothing outside Files; respect Out of scope"), and the instruction to run the Acceptance checks and report their actual output.
5. **Verify.** A plan is done when its Acceptance criteria pass, with the output to prove it. "Looks right" is not done. A failed acceptance check means the plan stays open and the failure is reported verbatim.
6. **Report.** Per plan: done (acceptance output), failed (where and why), or bounced (plan-format defect). Update the backlog accordingly.

## Executor brief template

```
Execute the plan in <path> exactly.
You have no other context; the plan is complete on its own.
Touch only the files in its Files section. Respect Out of scope.
When the steps are done, run the Acceptance checks and report their real output.
If a step is ambiguous or impossible as written, STOP and report which step
and what was missing. Do not improvise around it.
```

## Output format

```markdown
## Execute: <target>

**Model:** <alias> | session model (per-subagent dispatch unavailable)
**Dispatched:** <N> plans, <sequential | M parallel (disjoint files)>

### Done
- <title> — acceptance: <check> → <actual output> (`plans/<slug>.md`)

### Failed
- <title> — choked at step <n>: <verbatim failure> — plan stays open

### Bounced (plan-format defects)
- <title> — <what the plan failed to answer> → feed back to /swarm-improve

### Cost
<N> cheap-model runs; capable model spent only on dispatch and verification.
```

## Failure modes to avoid

- **Leaking session context into the executor.** It hides plan defects and makes the backlog untrustworthy. The plan file is the whole brief.
- **Patching a stuck executor by hand.** You are now the expensive model doing mechanical work. Bounce the plan instead.
- **Parallel executors on overlapping files.** Disjoint `Files` sections or sequential. No exceptions.
- **Marking done without acceptance output.** The check ran and passed, or the plan is still open.
- **Executing a malformed plan anyway.** Pre-flight exists so defects surface before tokens are spent.
