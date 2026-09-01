# kanso

> 簡素: elimination of clutter.

I kept watching Claude write code that ran fine and still felt puffy. Dead branches, comments that just say what the line already says, a whole helper for something used once. kanso pushes back. Nine skills that delete before they add, match your repo's voice, and earn every line, whether they're reviewing, refactoring, committing or writing a PR. Nothing gets written until you've seen the plan.

## Get it

In Claude Code:

```
/plugin marketplace add blakecyze/kanso
/plugin install kanso
```

Anywhere else (Codex, Cursor, Gemini CLI, Grok Build), the skills follow the open Agent Skills standard, so one script installs them for every tool at once:

```bash
git clone https://github.com/blakecyze/kanso && kanso/scripts/install.sh
```

That symlinks each skill into `~/.agents/skills/`, plus each tool's own user dir (`~/.codex/skills`, `~/.cursor/skills`, `~/.gemini/skills`) where one exists, so a `git pull` updates every tool together. Restart the tool afterwards; most cache their skill list. `--project` installs into the current repo instead, `--copy` if your setup can't follow symlinks, `--uninstall` to undo.

One honest caveat: the edit-verify hook (the thing that lint-checks each edit as it lands) is Claude Code plumbing. Elsewhere the skills tell the model to run your verify command itself before committing, which works, it's just a promise rather than a guarantee.

## The skills

| Skill | What it does | How you call it |
|---|---|---|
| `kanso-principles` | The anti-slop rules for code, loaded on their own. | auto |
| `kanso-prompting` | Rules for turning a rough ask into a sharp prompt. | auto (via task) |
| `kanso-task` | Sharpens your request, then runs it with the principles loaded. | `/kanso-task [request]` |
| `kanso-audit` | Reviews code, shows findings, proposes fixes before touching a thing. | `/kanso-audit [scope]` |
| `kanso-nuclear` | The big structural review: file sprawl, spaghetti, abstraction theatre. | `/kanso-nuclear [scope]` |
| `kanso-refactor` | Cleanup that never changes behaviour. The two never mix. | `/kanso-refactor [scope]` |
| `kanso-commit` | Atomic commits with messages that say *why*. | `/kanso-commit` |
| `kanso-pr` | PR descriptions that stand on their own, drawn from your commits. | `/kanso-pr` |
| `kanso-context` | Keeps `AGENTS.md` / `CLAUDE.md` lean. | `/kanso-context [mode]` |

## What it looks like

Before `/kanso-refactor`:

```python
def get_user(user_id):
    # Fetch user by ID
    try:
        result = db.query(User).filter(User.id == user_id).first()
        if result is not None:
            return result
        else:
            return None
    except Exception as e:
        return None
```

After:

```python
def get_user(user_id):
    return db.query(User).filter(User.id == user_id).first()
```

Five bits of clutter gone: the comment that repeats the signature, the filler variable, the redundant `is not None`, the dead `else`, and the `except` that quietly ate every error.

## How it behaves

- **It reports before it edits.** Findings land in your session first. Fixes only go in once you approve the block (`y/n/edit/pick`).
- **It checks its own work.** Audit and refactor run your lint/typecheck/test command after fixes land and paste the exit code. No silent "looks good".
- **A hook catches regressions inline.** Every edit fires a fast check on the file you touched (biome, oxlint, ESLint, ruff, `go vet`, `cargo check`). Quiet on pass, loud on fail. Turn it off with `KANSO_VERIFY_HOOK=0`.
- **Nothing writes on its own.** Fixes, commits, PRs, refactors and context edits are all manual.
- **Your voice wins.** If the repo is terse, kanso stays terse. It won't push a house style on you.

## The family

Same "earn your keep" idea, pointed at different work:

- [mimesis](https://github.com/blakecyze/mimesis) does it for writing and design. It strips the AI tells out of prose.
- [swarm](https://github.com/blakecyze/swarm) does it for agents. It fans work out only when a single pass would cost you more.

## Chip in

A skill has to earn its spot. If you can't say its trigger in one sentence, it's a note, not a skill. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Licence

MIT.
