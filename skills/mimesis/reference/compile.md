# Compiling instructions for machines

The L1 corpus for `mimesis-compile` (Domain B). Distilled from research on
token-efficient instruction design for frontier models. Read on every compile
run.

This domain is the opposite of the humanisation work. The reader is a model, not
a person. AI tells are fine here. Density, structure and literal precision win.
The humanisation linter never runs on Domain B output. Keeping the two domains
apart is the point; sharing machinery between them is a bug.

**Version warning.** This guidance is keyed to GPT-4.1 / GPT-5.x, Claude Opus
4.x, and Gemini 3.x as of mid-2026. Model behaviour drifts fast. Anything tagged
**[outdated]** was standard in 2023 to 2024 and is now counterproductive. Before
shipping a production prompt, cross-check parameter names against current
provider docs.

## The one idea

Context engineering beats phrasing. What you include, how you structure it, and
where you place the critical constraints matters more than the wording of any
sentence. The model is the processor, the context window is memory, your job is
to load exactly the right information. General-instruction sweet spot is about
150 to 300 words; past that, added instructions raise the risk of conflict
without proportional gain.

## Structure

The cross-provider section order, from OpenAI's GPT-4.1 guide and consistent with
Anthropic and Google guidance:

```
# Role and objective
# Instructions
## Sub-instructions
# Reasoning steps
# Output format
# Examples
# Context
# Final instruction
```

Delimiters, by job:

- **Markdown headings** for the top-level skeleton of a system prompt.
- **XML tags** (`<instructions>`, `<example>`, `<document>`) to fence variable
  content, document chunks and examples. Anthropic trains Claude on these and
  recommends them as the primary delimiter; tags stop the model confusing an
  example for an instruction.
- **Avoid JSON** for wrapping document collections in long context. OpenAI found
  it performs poorly there. Use XML or the pipe format (`ID: 1 | TITLE: ... |
  CONTENT: ...`). JSON is still right for structured-output specs and coding
  contexts.

Formatting mirror: a heavily marked-up prompt makes Claude mirror that formatting
in its output. Want prose, write the prompt in prose. Want markdown, structure
the prompt with markdown.

## Ordering and constraint position

- **Hard-to-easy constraints.** Place the most specific, restrictive or complex
  constraints first. Constraint order causes large adherence swings, and
  hard-to-easy is the research-backed optimum across providers.
- **The instruction sandwich.** In long context, put critical rules at both the
  start and the end. If you can place them only once, put them above the context,
  not below.
- **Lost in the middle.** Information buried mid-context is the most likely to be
  missed. Keep the load-bearing content at the edges.
- **Gemini 3 specifically.** Negative, formatting and quantitative constraints
  placed early get dropped. Make them the final lines.

## Compaction that keeps fidelity

- **Be specific about length, not vague.** "Limit to 2 to 3 sentences" is obeyed
  consistently. "Be concise" is underspecified and varies. Naming a sentence or
  word count is both tighter and more token-efficient than hedged "brief but
  thorough" phrasing.
- **Strip preamble.** "Please kindly consider" adds no semantic value. Frontier
  models are trained on instruction following, not social dynamics. Removing
  politeness is pure token saving at zero fidelity cost.
- **Reference static instructions, do not repeat them.** In agentic loops, hold
  large instruction blocks in a persistent system prompt and refer to them rather
  than re-injecting each turn. The highest-leverage compaction move.
- **Declare a schema once.** For repeated structured rows, declare field names
  once and use abbreviated rows rather than repeating keys.

Do **not** compress: few-shot examples, tool descriptions in agentic contexts, or
critical constraints (especially negative and quantitative ones). These are the
first things naive compaction drops and the most expensive to lose.

Algorithmic compressors (LLMLingua-2 and similar) exist for long pipelines and
hold fidelity to roughly 3x to 5x. TOON saves tokens over JSON only on long
structured data, because its novelty costs an explanatory prompt tax; for simple
structures, JSON with constrained decoding beats it. Reach for these only when
the context is genuinely large.

## Agent system prompts

Three reminders raised OpenAI's SWE-bench Verified score by nearly 20%. Include
them in any production agent prompt:

```
Persistence: keep going until the user's query is fully resolved before
yielding. Only stop when the problem is solved.

Tool use: if unsure about file content or codebase structure, use your tools
to read and gather the facts. Do not guess.

Planning: plan before each tool call and reflect on the result of the last
one, rather than running the whole task as a blind chain of calls.
```

Tool descriptions: use the API `tools` field, never hand-injected schemas into
the prompt body (worth about 2% on SWE-bench). Name tools for their purpose, keep
descriptions thorough but tight, put usage examples in a `# Examples` section
rather than the description field.

Reversibility guardrail for agents with real tool access:

```
Take local, reversible actions by default. For actions that are hard to reverse
(force push, rm -rf, dropping tables) or that affect shared systems, ask first.
```

## Per-model notes (mid-2026)

**GPT-4.1 / GPT-5.x.** Literal and precise instruction followers. State what to
do and what not to do, since the model no longer infers unspecified rules. One
firm corrective sentence is usually enough. On conflict, the model favours the
instruction nearer the end. GPT-5.5 Instant defaults to fewer bullets and shorter
answers.

**Claude Opus 4.x.** XML tags are trained behaviour. Prefer positive instructions
("write in flowing prose") over negative ones ("do not use bullets"); the
negative form triggers compliance anxiety. Give the why behind a rule; the model
generalises from it. Use the effort parameter and adaptive thinking. State scope
explicitly at low effort, since the model will not silently generalise a rule
from one item to the next.

**Gemini 3.x.** Keep temperature at the default 1.0; lowering it can cause looping
and degrade reasoning. Bound knowledge precisely ("based strictly on the provided
text") rather than with a blanket "do not infer", which breaks basic logic. Put
the question and constraints at the end of a large data context.

## Outdated, do not use

All keyed to the version where they broke.

- **[outdated, GPT-4.1+]** All-caps emphasis ("NEVER DO X"). Causes over-attention
  and destabilises other instructions.
- **[outdated, GPT-4.1+]** Tip and bribe framing ("I'll tip you $100"). No effect
  or negative.
- **[outdated, GPT-4.1+]** Relying on GPT-4o-era implicit rule inference. State
  rules explicitly.
- **[outdated, Claude 4.x]** Aggressive forcing language ("CRITICAL: you MUST").
  Over-triggers tool use. Use plain "use this tool when".
- **[outdated, Claude 4.x]** Prefilled assistant turns for output control. Returns
  a 400 error on Claude 4.6+.
- **[outdated, Claude 4.x]** The `budget_tokens` extended-thinking parameter.
  Replaced by the effort parameter and adaptive thinking.
- **[outdated, Claude 4.x]** "Be concise" with no specifics. The model calibrates
  length to task complexity, not vague brevity. Name the format.
- **[outdated, Gemini 3]** Temperature below 1.0 for reasoning. Causes looping.
- **[outdated, Gemini 3]** Blanket negatives ("do not infer", "do not guess").
  Over-indexes and blocks basic logic.
- **[outdated, all]** JSON for long-context document wrapping. Use XML or the pipe
  format.
- **[outdated, all]** "Act as DAN" and jailbreak persona prompts. Ineffective and
  counterproductive.
- **[outdated, all]** Manual injection of tool schemas into the prompt body. API
  tool definitions beat it.
- **[outdated, all]** Context first, instructions last for long prompts. Sandwich
  the instructions instead.

## Cross-model quick matrix

| Consideration | GPT-4.1 / 5.x | Claude Opus 4.x | Gemini 3.x |
|---|---|---|---|
| Primary delimiter | Markdown headings | XML tags | Structured steps |
| Instruction position | Both ends of long context | After context for long docs | Constraints at end |
| Constraint order | Hard-to-easy | Hard-to-easy | Hard-to-easy |
| Chain of thought | Request explicitly | Adaptive thinking at high effort+ | Set thinking level |
| Tool description | API field | Plain trigger language | Native API |
| Temperature | Default | Default | Keep at 1.0 |
| Avoid | All-caps, tips, JSON wraps | budget_tokens, prefill, CRITICAL | Broad negatives, reduced temp |

When you compile, build evals. At this capability level the best prompt genuinely
depends on the use case, so treat the prompt as a versioned artefact and measure
constraint adherence, grounding and coverage.
