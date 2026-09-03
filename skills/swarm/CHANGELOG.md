# Changelog

All notable changes to swarm are recorded here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning follows [SemVer](https://semver.org/).

## [0.2.1] — 2026-09-03

### Fixed

- `swarm-execute`'s frontmatter description is now quoted, so strict YAML parsers (the `npx skills` CLI among them) stop rejecting it.

## [0.2.0] — 2026-07-08

### Added

- The capability ladder in `swarm-principles`: native parallel subagents, then headless CLI fan-out (`claude -p`, `codex exec`, or equivalent), then sequential in-context emulation. Every skill dispatches per the ladder, and `model: haiku` reads as "your harness's cheapest capable model".
- `scripts/install.sh` — cross-tool installer. Symlinks each skill into `~/.agents/skills/` and any per-tool user skill dirs present (`~/.codex/skills`, `~/.cursor/skills`, `~/.gemini/skills`). `--project`, `--copy`, `--uninstall`.
- README section on cross-tool use, honest about which ladder rung each tool reaches.

### Changed

- `swarm-execute` and `swarm-improve` headless fallbacks generalised beyond `claude -p` to whichever agent CLI is on PATH.

## [0.1.0] — 2026-07-08

### Added

- `swarm-principles` — shared rules for every swarm, auto-loaded: sequential by default, the three conditions for fanning out, the hard cost ceiling (5 concurrent, confirm to 10, refuse above), and the judging procedure.
- `swarm-plan` — decomposes one task into parallel waves with dependencies and a named merge. Plans only; never spawns.
- `swarm-explore` — read-only parallel investigation. Maps a codebase or question space fast; subagents return findings, never code dumps.
- `swarm-bulldoze` — best-of-N generation. Independent candidates, a rubric fixed before judging, one winner with salvage from the losers.
- `swarm-refine` — one artefact, parallel critics on disjoint axes, merged into a single coherent revision.
- `swarm-improve` — capable-model audit that writes self-contained plans (`plans/<slug>.md`) executable by an agent with zero prior context. Modes: `quick`, `deep`, focus categories, `branch`, `next`, `reconcile`; `--issues` publishes to GitHub.
- `swarm-execute` — dispatches those plans to a cheaper model, one subagent per plan, sequential by default and parallel only for disjoint plans. Verifies each plan's acceptance criteria; plan-format failures are reported back, never patched over with session context.
