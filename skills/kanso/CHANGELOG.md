# Changelog

All notable changes to kanso are recorded here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning follows [SemVer](https://semver.org/).

## [0.4.1] — 2026-07-08

### Added

- `scripts/install.sh` — cross-tool installer. Symlinks each skill into `~/.agents/skills/` and any per-tool user skill dirs present (`~/.codex/skills`, `~/.cursor/skills`, `~/.gemini/skills`), so any Agent Skills-compatible tool picks them up from the one repo checkout. `--project`, `--copy`, `--uninstall`.
- Cross-harness conventions section in `kanso-principles`: what `/kanso-<name>` references mean outside Claude Code, and how to degrade missing harness features.
- README section on using kanso with Codex, Cursor, Gemini CLI, and Grok Build, including the honest hook caveat.

### Changed

- `--fresh` in `kanso-audit` and `kanso-nuclear` degrades gracefully on harnesses without read-only subagents: Phase A runs inline with a one-line note.
- `kanso-refactor`'s Verify section notes that outside Claude Code no PostToolUse hook ran, so the verify step is the only check.
- `kanso-context`'s init skeleton gains an optional Standing rules pointer block, so tools that load skills on demand still see `kanso-principles`.

## [0.4.0] — 2026-07-07

### Changed

- `kanso-prompting` rewritten version-agnostic. Behavioural guidance stated as current-generation defaults; release-pinned facts quarantined in a dated "Perishable" section.
- Phase D verify procedure and approval-gate routing deduplicated. `kanso-refactor` holds the canonical verify procedure, `kanso-audit` the canonical routing rules; `kanso-nuclear` and `kanso-audit` cross-reference instead of copying. User-facing blocks stay inline.
- Trigger descriptions tuned. `kanso-task`'s description no longer summarises its own workflow (agents were at risk of following the description and skipping the skill body). All descriptions are trigger-conditions-only.
- `kanso-principles` trimmed to 105 lines — it loads on every code task. Examples compressed; no rule changed.
- `--fresh` sections in `kanso-audit` and `kanso-nuclear` name `Explore` as the preferred Phase A agent and record why whole-skill `context: fork` is deliberately not used.
- Verify hook hardened: parses hook JSON with `jq` (sed fallback), reads `tool_input.file_path` specifically, detects biome and oxlint ahead of ESLint. Moved to the standard `hooks/` plugin-root layout.

### Added

- `scripts/lint-skills.sh` — static checks for frontmatter, trigger-shaped descriptions, line ceilings, and house style.
- `evals/evals.json` — dogfood scenarios for the workflow skills, runnable by hand or via the skill-creator eval runner.

## [0.3.0] — 2026-05-27

### Added

- `kanso-nuclear` — structural maintainability review distinct from `/kanso-audit`. Five named smells in priority order: judo, sprawl, spaghetti, theatre, wrong-layer. Defaults to the whole codebase; `diff` mode scopes to branch vs upstream. Same approval gate, refactor handoff, and Phase D verification as `/kanso-audit`.
- `kanso-audit` Phase D — discovers the project's verify command (AGENTS.md, package.json, pyproject, go.mod, Cargo.toml, CI) and pastes the exit code after fixes land. No silent success.
- `kanso-audit --fresh` — push Phase A investigation to a read-only subagent for an unbiased pass on code the session has already touched. Phases B–D stay inline.
- `kanso-audit` test-first requirement for Correctness behaviour-changes when a test suite exists. Skip-reason must be stated when not.
- `kanso-refactor` matching Phase D verification step and a `!git` prelude.
- `kanso-pr` Verification section (replaces Testing) with explicit "what wasn't tested and why" requirement.
- `kanso-context` paste-ready self-update prompt for fixing recurring agent mistakes at the context layer.
- PostToolUse hook (`.claude-plugin/hooks/kanso-verify.sh`) — fast linter or syntax check on every Edit/Write. ESLint, ruff, `go vet`, `cargo check`, with a `py_compile` fallback. Opt out with `KANSO_VERIFY_HOOK=0`.

## [0.2.0] — 2026-05-25

### Added

- `kanso-task` — rewrites a rough request into a sharp prompt and executes it inline with `kanso-principles` loaded. Maintains a running `implementation-notes.md` during execution so judgment calls stay visible.
- `kanso-prompting` — standing rules for prompting current frontier models (Claude 4.x specifically). Loaded by `/kanso-task`.

### Changed

- `kanso-audit` rewritten for a single-command loop: two-line summary + one-line findings, mandatory approval gate when findings exist, plain-language explanation of behaviour changes. Always runs inline; never dispatched as a subagent.
- `kanso-refactor` adds matching "always run inline" rule so the audit handoff stays in the calling chat.

## [0.1.0] — 2026-04-23

### Added

- `kanso-principles` — standing anti-dilution rules, auto-loaded for any code-related task.
- `kanso-audit` — code review via an Explore subagent that produces a structured findings report, proposes concrete fixes tagged by shape (`refactor` or `behaviour-change`), and on approval hands refactors to `/kanso-refactor audit-report` while applying behaviour changes in place.
- `kanso-refactor` — behaviour-preserving cleanup against the anti-pattern taxonomy.
- `kanso-commit` — atomic commits with messages that answer *why*.
- `kanso-pr` — self-contained PR descriptions pulled from commit history.
- `kanso-context` — curation of `AGENTS.md` and `CLAUDE.md`, biased toward pruning.
