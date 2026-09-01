---
name: mimesis-human
description: "Use when the user wants prose to sound human or to stop reading as AI: \"humanise this\", \"make this sound human\", \"does this read as AI\", \"remove AI tells\", \"de-slop this\", \"make it less ChatGPT\". Runs read-only audit (flag every tell with location and severity), rewrite (meaning-preserving humanisation of existing text), or generate (draft new, already-human text). Removes every em dash without exception. Not for general drafting or copy-editing unrelated to removing the machine-written texture."
argument-hint: "[text | file path] [--mode audit|rewrite|generate] [--register professional|casual] [--gen codex]"
allowed-tools: Bash(python3 *) Read Edit Write
---

# mimesis-human

Humanise writing and strip the modern AI tells. The guidelines outrank the
model: quality is a property of the reference corpus and the linter, not of
whichever model is writing.

## The precedence stack

Every run goes through three layers, top to bottom. The lower a layer sits, the
more optional it is.

- **L1, the guideline corpus.** Read [reference/tells.md](../../reference/tells.md)
  and [reference/craft.md](../../reference/craft.md) on every run before doing
  anything. Primary, model-independent, never skipped. In rewrite and generate
  modes, also read [reference/register.md](../../reference/register.md).
- **L2, the deterministic linter.** Run the linter on the input, and again on
  anything you produce. It catches em dashes, smart quotes, kill-list words,
  negative parallelism and participle tails regardless of which model wrote the
  text.
- **L3, the generator (optional).** Claude by default. Codex / GPT-5.5 only if
  installed and opted into via `--gen codex`. See [codex.md](../../codex.md).
  Whatever generates, L1 and L2 always run afterwards.

Run the linter like this, against a file or stdin:

```
python3 "$CLAUDE_PLUGIN_ROOT/linter" --json path/to/draft.md
```

Use `--json` when you need to act on findings, or omit it for a readable report.
The linter reports; it never rewrites. Restructuring is your job under L1.

## Three modes

Detect the mode from the user's phrasing. Default to **audit** when ambiguous, so
the skill never edits text the user only wanted checked.

- **audit.** Read-only. Run L1 and L2, report every tell with location, category
  and severity. No rewriting. This is the diagnostic pass.
- **rewrite.** Meaning-preserving humanisation of existing text. Apply the craft
  principles and the final pass from craft.md. Never change a factual claim,
  never invent experience or anecdotes.
- **generate.** Draft new text that is already humanised, rather than writing
  clean prose and cleaning it twice.

`--mode` overrides detection.

## Three absolute rules

1. **Zero em dashes, ever.** When the linter flags one, restructure into commas,
   full stops, parentheses or two sentences. A restructure, not a swap. This also
   covers the en-dash-as-em-dash, double-hyphen and spaced-hyphen workarounds.
2. **Catch the merely perceived.** Flag and fix constructions that read as AI
   even when grammatically fine: tricolons, participle tails, dutiful sign-offs,
   antithesis. These get rewritten or downgraded, not waved through on a
   technicality. The linter handles the regexable ones; you handle the rest using
   tells.md and the final-pass checklist.
3. **Never a typo.** Humanising never means a misspelling, a dropped apostrophe
   or a forced grammatical error. Casual register loosens grammar on purpose
   (see register.md); it never breaks spelling.

## How a run works

1. Read tells.md and craft.md (plus register.md when writing).
2. Run the linter on the input.
3. Mode **audit**: stop here and emit the report.
4. Mode **rewrite** or **generate**: resolve the register first. `--register`
   wins; otherwise rewrite preserves the input's register and generate infers
   from the artefact, falling back to professional (see register.md). Then
   produce the text, applying the craft principles and the final pass. If
   `--gen codex` and Codex is present, route the draft through it per codex.md,
   then continue.
5. Run the linter on your output. Fix and re-run until it is clean of all
   non-advisory findings. An advisory finding (`earned-word`, `low-burstiness`,
   `low-lexical-diversity`) may stand only when you judge it earned, and you say
   so. Never hand back text with a non-advisory flag.
6. Run the craft check from craft.md: five dimensions, each pass or fail
   (rhythm, earned vocabulary, stance, register fit, specificity). On any fail,
   revise the failing dimensions only, re-lint, re-grade. Maximum two revision
   loops, then ship the best version and name the shortfall. End the output with
   the one-line result, for example `Craft check: pass.`

## Output

**audit.** A tight report. No preamble, no sign-off.

```
# Humanise audit: <short description>

**Tells:** <n> blocker, <n> important, <n> polish

[1] line 4 (blocker) em dash: restructure into two sentences
[2] line 4 (important) negative parallelism: "it's not X, it's Y"
[3] line 9 (important) kill-list "leverage": use a plain verb
```

One line per finding, highest severity first. Lead with the em dashes; they are
non-negotiable. Group the L2 findings, then add any [judgement] tells from
tells.md the linter cannot see (flat rhythm, dutiful closing, neutrality).

**rewrite / generate.** Return the cleaned text, then the one-line craft check
result, and nothing else, unless the user asked what changed. If they did,
follow with a short bullet list of the categories you addressed, not a
line-by-line diff. End the turn on a clean linter pass and a reported craft
check.

## Limits to state when relevant

- Detectors false-positive. This skill writes for signal and voice. It does not
  promise to beat any given detector.
- Meaning preservation is mandatory in rewrite mode. No claim changes, no
  fabricated anecdotes.
- The kill list is versioned, not eternal. It drifts as models drift.

## What this skill never does

- Edit text in audit mode.
- Change a factual claim or invent experience to sound human.
- Swap an em dash for a comma without restructuring the sentence.
- Hand back output the linter still flags with anything non-advisory.
- Introduce a typo, misspelling or forced grammatical error to look human.
- Report a humanity score. The craft check is pass/fail per dimension and one
  line of output; there is no number to chase.
- Auto-route to Codex. Codex runs only on an explicit `--gen codex`.
