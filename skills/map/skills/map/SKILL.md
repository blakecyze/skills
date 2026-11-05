---
name: map
description: "Use when the user wants a repo mapped for agents, or context, reuse, and duplication kept under control: \"map this repo\", \"index our components\", \"we keep rebuilding the same helper\", \"find the duplication\", \"keep image references in one place\", \"refresh the map\". Also for keeping research and reference images as linked pages agents read progressively. Not for generated API docs, a single README, or always-loaded instruction files."
argument-hint: "[scope] [build|refresh|check|dedupe|research] [apply]"
---

# Map

Keep what search cannot answer in a git-ignored `map/` folder: computed duplicates, one register of images, the choices search gets wrong, and pages that say when they have gone stale.

## Controls

`[scope] [build|refresh|check|dedupe|research] [apply]`

All optional. No map means build; an existing map means refresh. `check` is read-only. `dedupe` decides duplicates and edits source only with `apply` or an equivalent request. `research` keeps findings as pages: read [research.md](references/research.md).

## What a map holds

```text
map/
  README.md      routes by task: "adding UI: reuse.md". Under 80 lines.
  reuse.md       | Name | Where | Use when |, only where search misleads
  dupes.md       generated; you fill its Decision column
  images.md      generated; you fill its Shows column
  images/        reference images only
  notes/<area>.md  reasons, invariants, traps, "changing X means also changing Y"
  research/      optional
  .ignore        globs to leave out, one per line: vendored and generated code
```

Each page you write below the root opens with a title, an `Up:` line linking its parent, and a `Covers:` line naming the code it describes, such as `Covers: src/billing/**, lib/tax.ts`. Cover only the files a page makes claims about: a page covering all of `src/` goes stale on every change and teaches agents to ignore the warning. The root covers nothing. `check` warns about broad globs and rejects ones that match nothing. Name paths and symbols. Line numbers and copied code rot, so leave them out.

Write a page only for facts a fresh agent would otherwise miss. A small repo may have no notes at all, and directories never get a page each: [overviews did not help agents reach the right files, and context raised cost by over 20%](https://arxiv.org/abs/2602.11988).

Product images stay where the build expects them, because nothing that ships can depend on an ignored folder. `images.md` is the one place that indexes them.

## Commands

Run `python3 <skill>/scripts/map.py <command>` inside the repo, with `<skill>` resolved from this file's folder. These numbers are computed; use them over your own estimates.

| Command | Gives |
|---|---|
| `init` | Creates and ignores `map/`. Refuses a folder it did not make: stop and ask |
| `scan` | Code by area |
| `symbols [glob]` | Exports ranked by how many files mention them |
| `dupes --write`, `images --write` | Regenerate a register, keeping its last column |
| `stamp [pages]` | Records a page as true of the code now |
| `check` | Lint and stale pages, naming what changed. Exit 0 means clean |

## Build

1. `init`, then `scan`. Create `map/.ignore` if vendored or generated paths need leaving out.
2. `dupes --write` and `images --write`. Leave Decision blank until a dedupe pass.
3. Write `reuse.md` from `dupes` and `symbols`, reading the files it names. Add a row only where a searching agent could still go wrong: which of several similar things is canonical, or a helper whose name hides its job. Agents already find most code by searching, so this is a short list, not an index of exports. Drop fan-in hits that are only name matches.
4. Add `notes/` only where reading the code would not reveal the trap.
5. Fill Shows for images agents will need to pick between, opening each one you describe.
6. Write the root README, linking every page.
7. Add this line to `AGENTS.md`, or `CLAUDE.md` if that is what exists; create neither:

   `Project map: map/README.md (git-ignored, may be absent; in a worktree, see the main checkout). Before adding a component, helper, or image, check map/reuse.md and map/images.md.`
8. `stamp`, then `check`. Fix everything it reports.

## Refresh

Run `check`, then read only the pages and files it names. Correct those pages, `stamp` each one, regenerate the registers, and run `check` again. Stamping says the page is true now, so stamp only what you re-read.

## Dedupe

Run `dupes --write`. For each undecided row, largest first, read every location and write `canonical: <path>` (most used, best tested, or best placed) or `accepted: <why>`. A same-name row can be coincidence. Report the proposed consolidations.

With `apply`, consolidate one group at a time, update callers, run the project's tests, then `dupes --write`. Stop at a failure you cannot explain.

## Reading a map

Search it by naming the path, `rg term map/`, because search tools skip ignored folders. From a linked worktree the map is in the main checkout; the script finds it there.

## Report

State what was built or refreshed, the largest duplicates, the `check` result, and any line added to a tracked file. Say plainly what could not be verified.
