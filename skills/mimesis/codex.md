# codex.md: the optional L3 generator

The generator is the last and most swappable layer in the stack. Claude is the
default. Codex / GPT-5.5 is available only if it is installed and the user
explicitly opts in. Whatever generates the draft, L1 (the reference corpus) and
L2 (the linter) always run afterwards, so the output is humanised and em-dash-free
no matter who wrote it.

## When to use it

Only in `generate` mode, and only when **both** of these hold:

1. `codex` is on `PATH`.
2. The user passed `--gen codex`.

Never auto-route. The default path stays Claude, which keeps behaviour
predictable. If the user did not ask for Codex, do not probe for it and do not
mention it.

## Detection

```
command -v codex >/dev/null 2>&1 && echo present || echo absent
```

If the user asked for `--gen codex` and the probe returns `absent`, say so in one
line and fall back to Claude. Do not fail the run over a missing optional
generator.

## Routing

When the gate is satisfied, shell out to Codex for the draft step only, then bring
the result back into the skill:

```
codex exec "<the generation prompt>"
```

Then, without exception:

1. Run the L2 linter on whatever Codex returned.
2. Apply the L1 craft principles and the final-pass checklist.
3. Re-run the linter until it is clean.

So if Codex writes the draft, the Claude-run humanise pass still cleans it. You
get the option without betting quality on it.

## A flag on the premise

The request to route prose to GPT-5.5 because it is "better" runs against the
research. The GPT lineage is the *origin* of most documented tells: the em dash,
"delve", negative parallelism. GPT-5.5 is tuned for agentic coding and tool use,
not prose voice. There is no evidence it humanises better than the model already
running this skill.

That is exactly why the stack is built the way it is. Generation stays
model-agnostic, Codex is strictly optional, and the same L1 and L2 pass runs
afterwards regardless of who generated. The quality lives in the guidelines and
the linter, not in the generator. Treat Codex as a swappable convenience, never
as the thing the output depends on.
