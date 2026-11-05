# Map

Keep what search cannot answer in one git-ignored folder: what is duplicated, where images are, which of several similar things to use, and which pages have gone stale.

A tour of the repo is not on that list. [Gloaguen et al.](https://arxiv.org/abs/2602.11988) found repository overviews did not get agents to the right files any faster, and context files raised cost by over 20%. So a map holds facts a fresh agent would otherwise miss or rebuild, and nothing loads until a task needs it.

## Install

```bash
npx skills@latest add blakecyze/skills --skill map
```

For a local clone, replace `blakecyze/skills` with `.` from the repository root. Claude Code can use `/plugin marketplace add blakecyze/skills` followed by `/plugin install map@cyze`.

## Use

```text
$map
$map check
$map dedupe
$map dedupe apply src/billing
$map research how Linear handles triage
```

With no map, it builds one. With a map, it refreshes only the pages whose files changed.

## What you get

```text
map/
  README.md       routes by task
  reuse.md        which of several similar things to use, a short list
  dupes.md        generated: repeated code, same-named exports, identical files
  images.md       generated: every image, its users, exact copies, what it shows
  images/         reference images only
  notes/          traps and reasons, only for areas that have them
  research/       optional evidence-labelled research
```

[map.py](skills/map/scripts/map.py) computes the facts using Python 3.9+ and git, with no packages. It took under a second on a 21,000-file repo. Each page lists the files it covers, so `check` can say exactly which pages went stale and why, across uncommitted work, rebases, and branch switches.

The Claude Code plugin adds a session-start line when pages are out of date, and stays silent otherwise. Other tools get the same answer from `map.py status`.

## Limits

- Duplicates means identical code after whitespace, same-named exports, and identical files. Renamed copies are not caught.
- It will not make agents find code faster. Asked to add a label needing a helper whose name hid its job, in a 212-file repo, Haiku reused it in all three runs without a map, as it did with one. So `reuse.md` stays short, and the value is in the computed registers and staleness.
- `map/` is local. A fresh clone has no map until someone runs the skill, and nothing that ships may depend on it.
- Search tools skip ignored folders, so search it by naming the path: `rg term map/`.

Validation scenarios live in `evals/evals.json`. They require judging actual agent work; static validation does not execute them.

MIT. See [LICENSE](LICENSE).
