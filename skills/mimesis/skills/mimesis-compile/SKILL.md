---
name: mimesis-compile
description: Use when the user wants text written for a machine reader, not a human: "write a prompt for", "compress this for an LLM", "turn this into instructions for an agent", "make this a system prompt", "compile this into a prompt". Produces dense, structured, token-efficient instructions tuned to current frontier models, with the right delimiters, constraint ordering and the instruction sandwich. AI tells are acceptable here. Bypasses the humanisation linter by design. Not for human-facing prose, which is mimesis-human's job.
argument-hint: "[intent or draft] [--model gpt|claude|gemini]"
allowed-tools: Read Edit Write
---

# mimesis-compile

Domain B: the machine-facing side, and the deliberate opposite of the rest of
mimesis. The reader here is a model, not a person. Density, structure and literal
precision win. AI tells are fine. Em dashes are fine. The humanisation linter
must never run on this output, and this skill shares no machinery with the Domain
A skills. That separation is the whole design; breaking it is a bug.

## How a run works

1. Read [reference/compile.md](../../reference/compile.md) on every run. It is the
   L1 corpus, keyed to GPT-4.1 / GPT-5.x, Claude Opus 4.x and Gemini 3.x as of
   mid-2026, and it flags advice that has gone stale.
2. Establish the target. If the user named a model (`--model`, or "for Claude",
   "for an OpenAI agent"), apply that family's notes from the matrix. If not, ask
   once, or write to the cross-provider common denominator and say so.
3. Compile. Two modes, detected from phrasing:
   - **rewrite**: tighten an existing prompt or instruction block. Strip
     preamble, reorder constraints hard-to-easy, fix delimiters, apply the
     instruction sandwich for long context.
   - **draft**: build a new prompt from a loose intent, using the section
     skeleton in compile.md.
4. Hand back the compiled prompt. Do not run the prose linter on it.

## The rules that matter most

From compile.md, in priority order:

- Context engineering beats phrasing. Decide what goes in and where before
  polishing any sentence.
- Hard-to-easy constraint order. Most specific and restrictive first.
- The instruction sandwich. Critical rules at the start and the end of long
  context.
- Right delimiter for the job: Markdown skeleton, XML for fenced content and
  examples, not JSON for document wrapping.
- Be specific about length. "Limit to 2 to 3 sentences", never "be concise".
- Strip preamble and politeness. Zero semantic value, pure token cost.
- Do not compress examples, tool descriptions or critical constraints.

## Guard against stale advice

compile.md carries an `[outdated]` list keyed to the version where each technique
broke. Actively avoid them when compiling: all-caps emphasis, tip and bribe
framing, `CRITICAL: you MUST` forcing language, prefilled assistant turns,
`budget_tokens`, JSON document wrapping, temperature below 1.0 for Gemini
reasoning, blanket negatives, and hand-injected tool schemas. If the user's draft
contains any of these, fix it and say what you changed and why.

## Output

Return the compiled prompt in a fenced block so it copies clean. If you made
non-obvious structural choices (constraint reorder, delimiter switch, sandwiching),
add a short list underneath of what you changed and the reason, since the user may
want to keep or revert a specific decision. Keep that note brief.

## What this skill never does

- Run the humanisation linter or apply Domain A craft rules. This is the wrong
  domain for them.
- Strip em dashes or kill-list words from the output. They are not tells here.
- Humanise. If the user actually wanted human-facing prose, hand off to
  `/mimesis-human`.
- Invent capabilities or parameters. Tie model-specific advice to the version it
  was validated against, and flag when something needs checking against current
  provider docs.
