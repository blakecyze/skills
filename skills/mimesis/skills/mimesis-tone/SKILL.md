---
name: mimesis-tone
description: "Use when the user wants text written or recast in a specific named human voice: \"make this sound like an expert / a practitioner\", \"make this warmer\", \"make this blunter / sharper\", \"make this more persuasive / sell this\", \"make this plainer / simpler\", \"give this a [tone] voice\", \"rewrite this in a [tone] tone\". Five tones: persuasive, practitioner, warm, blunt, plain. Shapes voice while still removing AI tells and em dashes. Not for neutral de-slopping (that is mimesis-human) or pure shortening (mimesis-concise)."
argument-hint: "[text | file] --tone persuasive|practitioner|warm|blunt|plain [--register professional|casual]"
allowed-tools: Bash(python3 *) Read Edit Write
---

# mimesis-tone

Domain A. Write or recast prose in a specific named human voice. Tone is which
human voice; de-slopping is the separate job of not sounding like a machine. This
skill does both: it shapes the voice and runs the same humanisation pass, so a
tone never reintroduces a tell.

## Pick the tone

From `--tone`, or detect from phrasing:

- **persuasive** ("sell this", "more persuasive", "landing-page copy")
- **practitioner** ("sound like an expert", "case study", "earned authority")
- **warm** ("warmer", "friendlier", "welcome email", "support reply")
- **blunt** ("blunter", "sharper", "more direct", "cut the hedging")
- **plain** ("plainer", "simpler", "clearer")

If the request names no tone and the right one is not obvious from the format, ask
once rather than guessing.

## How a run works

1. Read the relevant profile in [reference/tones.md](../../reference/tones.md),
   plus [reference/craft.md](../../reference/craft.md) and
   [reference/tells.md](../../reference/tells.md) for the base humanisation. All on
   every run. When writing, also read
   [reference/register.md](../../reference/register.md): register (professional
   or casual grammar) is a separate axis from tone, resolved from `--register`
   or inferred per register.md. Every tone takes either register.
2. Detect the mode:
   - **rewrite** (default when text is supplied): recast existing text into the
     tone, meaning preserved. Never change a factual claim, never invent
     experience, numbers or quotes to fit the voice.
   - **generate** (when drafting from a brief): write new text already in the tone.
   - **audit** (when asked to assess): flag where the text misses the tone and
     where it carries tells, read-only.
3. Apply the tone's craft moves and avoid its slop twin. Remember the master key:
   every tone's authentic version is more specific than its imitation, so the
   strongest move is almost always to get concrete.
4. Run the linter on your output:

   ```
   python3 "$CLAUDE_PLUGIN_ROOT/linter" --json <target>
   ```

   Fix and re-run until clean of all non-advisory findings. An advisory finding
   (`earned-word`, `low-burstiness`, `low-lexical-diversity`) may stand only
   when you judge it earned, and you say so. The tone's own kill-list in
   tones.md goes beyond what the linter catches; apply that by hand.
5. Run the craft check from craft.md: rhythm, earned vocabulary, stance,
   register fit (this dimension checks the tone AND the register), specificity.
   Each pass or fail. On any fail, revise the failing dimensions only, re-lint,
   re-grade, maximum two loops. End the output with the one-line result.

## The hard rules still hold

- Zero em dashes, in every tone.
- No fabricated specifics. The master key is specificity, but in rewrite mode you
  get specifics from the user or the source text, never by inventing them. A warm
  message with a made-up detail or a case study with an invented metric is worse
  than a vague one. If a tone needs a concrete number, name or quote you do not
  have, ask for it or leave a clearly marked placeholder.
- Tone shapes voice, not truth. Persuasive does not mean overstated, blunt does
  not mean cruel, warm does not mean dishonest.
- Never a typo. Casual register loosens grammar on purpose, per register.md; it
  never breaks spelling or forces an error.

## Output

Return the recast text, then the one-line craft check result, and nothing else,
unless the user asked what changed. If they did, add a short note: the tone
applied, and the main moves (for example "swapped buzzwords for the specific
mechanism, matched the awareness stage, cut the dutiful summary"). End on a
clean linter pass and a reported craft check.

## What this skill never does

- Fabricate a number, name, quote or experience to fit a voice.
- Reintroduce an em dash or kill-list word because a tone "wanted" it. The linter
  runs on every tone.
- Do neutral de-slopping with no target voice. That is `/mimesis-human`.
- Just shorten text. That is `/mimesis-concise`.
- Stack all five tones. Pick the dominant one; let at most one other adjust the
  edges.
- Introduce a typo, misspelling or forced grammatical error to look human.
- Report a humanity score. The craft check is pass/fail per dimension, one line.
