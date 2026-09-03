---
name: mimesis-concise
description: "Use when the user wants prose made shorter, tighter, or denser without losing meaning: \"make this concise\", \"tighten this\", \"cut the fluff\", \"too wordy\", \"trim this down\", \"say it in fewer words\". Strips throat-clearing, dutiful summaries, hedging, puffery and redundancy, keeping only what does work. Also removes em dashes and AI tells in passing. Not for expanding, explaining, or re-toning text where length is not the point."
argument-hint: "[text | file path] [--mode audit|rewrite] [--target N words]"
allowed-tools: Bash(python3 *) Read Edit Write
---

# mimesis-concise

Cut prose down to what does work. Where `mimesis-human` removes the machine
*fingerprint*, this removes the *bulk*: throat-clearing, dutiful summaries,
hedging, puffery and redundancy. The same instinct that keeps code tight, applied
to copy. Say the claim once and stop.

## Shared machinery

This command rests on the same three-layer stack as `mimesis-human`.

- **L1.** Read [reference/craft.md](../../reference/craft.md) (Principle 5,
  Restraint, is the spine here) and [reference/tells.md](../../reference/tells.md)
  on every run.
- **L2.** Run the linter on the input and on your output:

  ```
  python3 "$CLAUDE_PLUGIN_ROOT/linter" --json path/to/draft.md
  ```

  (Outside Claude Code, the linter is at `<this-skill-dir>/../../linter`.)

  Tightening is not an excuse to leave an em dash or a kill-list word behind. A
  concise pass still ends on a clean linter result.
- **L3.** Optional generator, same gate as `mimesis-human`. See
  [codex.md](../../codex.md). Rarely relevant here, since concise works on text
  that already exists.

## What concise cuts

In rough priority order:

- **Throat-clearing.** The first sentence that warms up instead of starting.
- **Dutiful summaries.** The closing line that repeats what was just said.
- **Hedging.** "It's worth noting that", "in many cases", "generally speaking",
  reflexive qualifiers that lower the temperature without adding information.
- **Puffery.** "a pivotal moment", "a seismic shift". State what happened.
- **Redundancy.** Two sentences making one point, doubled adjectives, a clause
  that restates its own subject.
- **Filler connectives.** "Furthermore", "in order to" for "to", "due to the fact
  that" for "because".

What concise keeps: every factual claim, the one specific that carries the point,
a varied rhythm, and the input's register. Shortening is not re-registering: a
casual note stays casual, a formal one stays formal (see
[reference/register.md](../../reference/register.md); this skill takes no
`--register` flag). Trimming is not flattening. Do not turn three differently
shaped sentences into three identical short ones; that trades wordiness for a new
tell. See Principle 1 in craft.md. And concise never introduces a typo or forced
error; cutting words never means breaking spelling.

## Two modes

Detect from phrasing. Default to **rewrite**, since "make this concise" is almost
always a request to act, not just to measure.

- **audit.** Read-only. Report where the bulk is, by category and location, with
  a rough word-count saving for each. No edits.
- **rewrite.** Produce the tightened text. If the user gave `--target N words`,
  hit it or get close and say the final count. Otherwise cut hard but preserve
  every claim.

## Output

**audit.**

```
# Concise audit: <short description> (<n> words)

[1] line 1 (throat-clearing): opening sentence adds nothing (~12 words)
[2] line 6 (redundancy): restates line 4 (~20 words)
[3] line 9 (hedging): "it's worth noting that" (~5 words)

Rough saving: ~37 words (<n> to <n>).
```

**rewrite.** Return the tightened text only, unless the user asked what changed.
If they did, add one line with the before and after word counts and a short list
of what you cut. End on a clean linter pass.

## What this skill never does

- Drop a factual claim to save words. Concise preserves meaning; it removes
  padding.
- Flatten every sentence to the same length. Brevity is not monotony.
- Leave an em dash or kill-list word in place because the task was "just length".
- Edit text in audit mode.
- Pad a too-short draft. That is not this command's job.
