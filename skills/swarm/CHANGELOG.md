# Changelog

All notable changes to swarm are recorded here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning follows [SemVer](https://semver.org/).

## [0.1.0] — 2026-07-08

### Added

- `swarm-principles` — shared rules for every swarm, auto-loaded: sequential by default, the three conditions for fanning out, the hard cost ceiling (5 concurrent, confirm to 10, refuse above), and the judging procedure.
- `swarm-plan` — decomposes one task into parallel waves with dependencies and a named merge. Plans only; never spawns.
- `swarm-explore` — read-only parallel investigation. Maps a codebase or question space fast; subagents return findings, never code dumps.
- `swarm-bulldoze` — best-of-N generation. Independent candidates, a rubric fixed before judging, one winner with salvage from the losers.
- `swarm-refine` — one artefact, parallel critics on disjoint axes, merged into a single coherent revision.
- `swarm-improve` — capable-model audit that writes self-contained plans (`plans/<slug>.md`) executable by an agent with zero prior context. Modes: `quick`, `deep`, focus categories, `branch`, `next`, `reconcile`; `--issues` publishes to GitHub.
- `swarm-execute` — dispatches those plans to a cheaper model, one subagent per plan, sequential by default and parallel only for disjoint plans. Verifies each plan's acceptance criteria; plan-format failures are reported back, never patched over with session context.
