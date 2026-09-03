# mimesis

> μίμησις: imitation.

Two jobs, opposite directions. When you're writing for people, mimesis strips out the fingerprints that make text read as AI. When you're writing for a machine, it compiles your intent into a dense, token-thrifty prompt. The name points at what the first job undoes: a machine doing an impression of a person.

The whole bet is one line: **the guidelines beat the model.** A versioned list of tells and a plain Python linter carry the quality, not whichever model happens to be writing. When a future model picks up fresh habits, the list and the linter still hand you clean, em-dash-free text.

## Get it

In Claude Code:

```
/plugin marketplace add blakecyze/mimesis
/plugin install mimesis
```

Anywhere else (Codex, Cursor, Gemini CLI, Grok Build), the skills follow the open Agent Skills standard, so one script installs them for every tool at once:

```bash
git clone https://github.com/blakecyze/mimesis && mimesis/scripts/install.sh
```

That symlinks each skill into `~/.agents/skills/`, plus each tool's own user dir (`~/.codex/skills`, `~/.cursor/skills`, `~/.gemini/skills`) where one exists, and the symlinks resolve back to the reference corpus and the linter in the repo, so nothing is duplicated. Restart the tool afterwards; most cache their skill list. `--project` installs into the current repo instead, `--copy` if your setup can't follow symlinks, `--uninstall` to undo. mimesis ports at full strength: the linter is plain Python and the tells corpus already covers the GPT and Gemini eras, so it cleans any model's output the same way.

## The skills

| Skill | What it does | How you call it |
|---|---|---|
| `mimesis-human` | The main event. Audits, rewrites or generates prose so it reads human. | `/mimesis-human [text or file]` |
| `mimesis-concise` | Cuts prose to what earns its place: throat-clearing, hedging, padding. | `/mimesis-concise [text]` |
| `mimesis-tone` | Recasts writing in a named voice: persuasive, practitioner, warm, blunt, plain. | `/mimesis-tone [text] --tone <name>` |
| `mimesis-design` | Spots the AI tells in a UI: purple gradients, Inter 700, three-card rows. | `/mimesis-design [path]` |
| `mimesis-compile` | The other direction. Compiles tight instructions for an LLM to read. | `/mimesis-compile [intent]` |
| `mimesis-principles` | The anti-tell rules, loaded on their own so prose comes out clean by default. | auto |

## What it looks like

Three ways to point `mimesis-human` at a piece of writing:

- **Audit.** Read-only. Flags every tell with a line, a category and a severity, and changes nothing.
- **Rewrite.** Humanises what you already wrote, meaning kept intact.
- **Generate.** Drafts something fresh that's already clean, so you're not cleaning it twice.

## How it behaves

- **Zero em dashes. Ever.** When one turns up, the skill rewrites the sentence around it. It doesn't just swap in a comma.
- **It catches the stuff that only *feels* like AI.** Tricolons, dutiful sign-offs, that reflexive "not this, but that" swing, all flagged even when they're grammatically fine.
- **Never a typo.** Casual writing loosens the grammar on purpose. It never means a misspelling.
- **The kill list is versioned.** Tells drift as models drift, so the list travels with the era, not carved in stone.

## Run the linter on its own

No plugin needed:

```
python3 linter path/to/draft.md        # readable report
python3 linter --json path/to/draft.md # machine-readable
cat draft.md | python3 linter          # from stdin
```

Exit 0 when it's clean, 1 when something's flagged.

## Honest limits

- Detectors throw false positives at real humans all the time. mimesis writes for signal and voice. It won't promise to beat any given detector.
- Rewrite mode keeps your meaning. No invented facts, no made-up anecdotes.
- Swapping synonyms to game a score changes nothing a detector actually measures. The honest work is structure and stance.

## The family

Same "earn your keep" idea, aimed at different work:

- [kanso](https://github.com/blakecyze/kanso) does it for code. It cuts the slop out of what Claude writes.
- [swarm](https://github.com/blakecyze/swarm) does it for agents. It fans out only when a single pass would cost you more.

## Licence

MIT. See [LICENSE](LICENSE).
