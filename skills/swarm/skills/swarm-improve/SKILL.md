---
name: swarm-improve
description: Use when the user wants to audit a whole codebase for latent work (bugs, performance, tech debt, missing tests, what to build next) and capture it as self-contained plans a cheaper agent can execute later. Spends the capable model on judgement, not execution. Read-only over code; writes plans only.
argument-hint: "[mode: quick|deep|<focus>|branch|next|reconcile] [--issues]"
disable-model-invocation: true
allowed-tools: Bash(git *) Bash(gh *) Bash(rg *) Bash(find *)
---

# swarm-improve

Use the most capable model available to study a codebase and write plans that a cheaper model executes later. The scarce resource is judgement: knowing what is wrong, what matters, and how to fix it. Execution is mechanical. This skill front-loads all the judgement into durable artefacts so the expensive model is never spent on work a cheap one could do.

The principles from `swarm-principles` apply. Note the seam: the rest of this library is about parallel fan-out. This skill is about tier-and-time delegation (capable now, cheap later). The audit phase can borrow fan-out from `/swarm-explore`; the planning phase is deliberately sequential capable-model work. The execution half is `/swarm-execute`.

## The hard rule

**Audit and plan. Never execute.** The moment this skill starts fixing things, it is spending capable-model tokens on mechanical work, which is the exact waste it exists to prevent. It produces plans. Something cheaper runs them.

And the corollary that makes the plans worth anything:

**Every plan must be executable by an agent with zero prior context.** The executor did not sit through the audit. It cannot see your reasoning. A plan that says "fix the caching issue we found" is worthless to it. A plan that says "in `src/cache.ts:40`, the TTL is set in seconds but read as milliseconds; change the read on line 52 to divide by 1000; verify with the test in `cache.test.ts`" is executable. The plan carries the judgement so the executor needs none. This is the same "brief a stranger" discipline as `/swarm-explore`, applied to deferred work.

## Modes

`$ARGUMENTS` selects scope and depth. Default (no argument) is a full audit across all categories.

- `quick` — cheap pass. Hotspots and top findings only. For when you have a few minutes of capable-model time.
- `deep` — exhaustive. Every package, every category. For when you have a real window.
- `<focus>` — one category only: `security`, `perf`, `tests`, `debt`, `bugs`. Narrow the audit to what matters now.
- `branch` — audit only what the current branch changes (`git diff` against the base). Pre-PR sweep.
- `next` — generative, not corrective. Not "what is broken" but "where should this project go." Feature suggestions and direction. Keep these separate from fixes; they are proposals, not defects.
- `reconcile` — backlog hygiene, not a new audit. Walk the existing plans: mark done ones done, unblock stale ones, retire ones the code has moved past. Run this before a fresh audit so you are not re-planning finished work.

`--issues` (modifier): after writing plans, publish each as a GitHub issue. Requires `gh` to be available and authenticated. Without it, plans stay as local files.

## Process

1. **Reconcile first if a backlog exists.** Do not audit into a pile of stale plans. Clear the deck.
2. **Scope the audit** per the mode. For a large codebase, fan the read-only audit out via `/swarm-explore` (respect the cost ceiling). For a focused or `branch` audit, a single pass is usually enough.
3. **Categorise findings.** bugs, performance, tech debt, missing tests, features (`next`). Keep corrective and generative findings apart.
4. **Prioritise.** Not everything found is worth a plan. Rank by impact against effort. A finding that is real but trivial or low-value does not earn a plan; note it in the summary and move on. Capable-model attention is the budget here too.
5. **Write one self-contained plan per work item** that clears the priority bar. Use the plan format below. This is the core output and where the capable model earns its cost.
6. **Publish** if `--issues`, else leave plans as files. Report the backlog.

## Plan format

Each plan is one file, executable cold. Write to `plans/<short-slug>.md`:

```markdown
# <imperative title: "Fix cache TTL unit mismatch">

**Category:** bugs | perf | debt | tests | feature
**Priority:** P0 blocking | P1 soon | P2 eventually
**Est. effort:** S | M | L

## Why
<the judgement the executor cannot reconstruct: what is wrong, why it matters,
what breaks if ignored. Two or three sentences.>

## Files
- `/absolute/path/to/file.ts` — <what changes here>
- `/absolute/path/to/other.ts` — <...>

## Steps
1. <concrete, ordered, unambiguous. Name symbols and line references.>
2. <...>

## Acceptance
- <how the executor knows it worked: a test passes, a behaviour changes>

## Out of scope
- <what NOT to touch, so the executor does not wander>
```

The `Why` and `Out of scope` sections are what separate a plan a cheap agent can run from a vague ticket that produces drift. Do not skip them.

**Paths in `Files` are absolute, never repo-relative.** An executor has no notion of "repo root" unless told, and a relative path like `README.md` is ambiguous the moment more than one reachable file matches it — the executor will search and may resolve it against the wrong tree entirely, silently editing something outside the intended scope. This is not a hypothetical: it is the exact failure mode this format exists to close off. Write every path in `Files` as an absolute path.

## Output format

```markdown
## Improve: <scope> (<mode>)

**Audited:** <what, how, N agents if fanned out>
**Plans written:** <N> → `plans/`

### Backlog
- **P0** <title> — `plans/<slug>.md` (<category>, <effort>)
- **P1** <title> — `plans/<slug>.md`
- ...

### Found but not planned
- <real findings below the priority bar, one line each, so they are on record>

### Next step
Run `/swarm-execute plans/<slug>.md` to dispatch a cheaper agent, one plan per run.
Without the plugin: `claude -p "Execute the plan in plans/<slug>.md exactly" --model haiku`, or `codex exec` / your harness's equivalent with the same brief.
<if --issues: "Published N issues: <links>">

### Cost
Audit: <N>x if fanned out. Planning: sequential capable-model pass.
```

## Failure modes to avoid

- **Plans that assume audit context.** The cardinal sin. If the executor needs to have read the audit, the plan has failed. Write for a stranger.
- **Fixing during the audit.** You are burning the expensive model on execution. Stop. Write the plan and move on.
- **Planning everything found.** Triviata does not earn a plan. Prioritise or the backlog becomes noise.
- **Mixing `next` proposals into the defect backlog.** Fixes and feature ideas have different bars and different consumers. Keep them apart.
- **Auditing over a stale backlog.** Reconcile first.
- **Cloning a product's whole command surface.** Modes are arguments, not skills. Resist the sprawl.
