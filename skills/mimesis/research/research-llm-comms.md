# Token-Efficient Instruction Design for Frontier LLMs — 2026 Edition

> **Scope and epistemic policy:** This report covers GPT-4.1, GPT-5.x, Claude Opus 4.x, and Gemini 3.x as of June 2026. Claims sourced from official provider documentation or peer-reviewed papers are labeled **[Evidence: strong]**. Claims from rigorous practitioner benchmarks are **[Evidence: moderate]**. Claims that are practitioner-consensus or anecdotal are explicitly flagged as such. Advice that is now outdated or counterproductive is flagged **[OUTDATED]**.

***

## Executive Summary

Effective instruction design for frontier LLMs in 2026 is no longer about finding clever wordings or tricks. It is about **architecture**: where information sits, how it is delimited, what is left out, and how system prompts are constructed for agentic persistence. All three frontier provider families (OpenAI GPT-5.x, Anthropic Claude Opus 4.x, Google Gemini 3.x) have converged on being highly literal instruction followers — meaning the cost of under-specification is now higher than it was in 2023–24, while many workarounds from that era (caps-lock emphasis, personality tricks, "DAN"-style persona exploits, and sycophancy-inducing role frames) either no longer work or are actively counterproductive.

The biggest structural shift: **context engineering has superseded prompt phrasing as the highest-leverage variable**. What information you include, how you structure it, and where you place critical constraints now matters more than the exact wording of any single sentence.[^1][^2]

***

## Part A: Prompt Structure and Formatting

### A.1 The Convergent Template

OpenAI's official GPT-4.1 Prompting Guide (April 2025) recommends a canonical section order that has become the cross-provider de facto standard:[^3][^4]

```
# Role and Objective

# Instructions
## Sub-instructions (for detail)

# Reasoning Steps

# Output Format

# Examples
## Example 1

# Context

# Final instructions / "think step by step" cue
```

This structure is not arbitrary. Anthropic's Claude 4.x best-practices documentation recommends an analogous breakdown — role, context, instructions with XML structure, examples in `<examples>` tags, then the task. Google's Gemini 3 prompting guide (updated June 2026) advises placing context and source material first, then main task instructions, then negative/formatting/quantitative constraints last. **Evidence: strong** for all three providers via official documentation.[^5][^6]

### A.2 Delimiters: XML, Markdown, and JSON

The three delimiter systems perform measurably differently, and provider guidance is now explicit:

| Delimiter | Recommended by | Best for | Avoid for |
|-----------|---------------|----------|-----------|
| **Markdown headings** (`##`, `###`) | OpenAI (starting point)[^4] | Section structure, system prompts | Long-context document wrapping |
| **XML tags** (`<instructions>`, `text>`) | Anthropic (strong preference)[^7] | Multi-component prompts, nested content, document corpora | Prompts that already contain lots of XML content |
| **JSON** | Not recommended for long context | Coding contexts, structured output specs | Document collections, long-context wrapping |

OpenAI tested multiple delimiter formats against long-context evaluations and found that XML and the "Lee et al. format" (`ID: 1 | TITLE: ... | CONTENT: ...`) performed well, while **JSON performed particularly poorly** for document collections[^4]. This is a direct reversal of earlier advice from 2023 that recommended JSON as a universal structured-data wrapper. **[OUTDATED: Using JSON to wrap document corpora in long-context prompts.]**

Anthropic trains Claude on XML and explicitly recommends it as the primary delimiter: `<instructions>`, `<example>`, `text>`, `<thinking>`, and `<answer>` tags help Claude parse multi-component prompts more accurately, reduce misinterpretation of instruction vs. content, and enable clean post-processing extraction of structured outputs. Claude 4.x best-practices documentation explicitly states that wrapping examples in `<examples>` tags prevents Claude from confusing them with instructions.[^7][^8][^5]

For Gemini 3, Google recommends using structured instructions (numbered or bulleted steps) with important negative constraints placed **at the end** of the instruction block rather than mixed in with positive instructions.[^6]

**Cross-provider practical rule (Evidence: moderate):** Use Markdown headings for the top-level skeleton of your system prompt; use XML tags to delimit variable content, document chunks, and examples; avoid JSON for anything not explicitly structured data output.[^9][^4]

### A.3 Instruction Ordering and Constraint Position

Multiple independent sources corroborate that **position of instructions within a prompt causally affects adherence**:[^10][^11][^12]

- **"Lost in the Middle" effect (Liu et al., TACL 2023):** Performance degrades significantly when critical information is buried in the middle of long contexts. Models perform best when key information appears at the start or end of the input. This was established on earlier models but remains relevant for all frontier models — confirmed by OpenAI's own long-context guidance for GPT-4.1.[^4][^12]

- **Constraint order bias (Zeng et al., ACL Findings 2025):** An empirical study on multi-constraint instruction following found that LLMs show "dramatic performance fluctuation" when constraint order is changed. The optimal order is **hard-to-easy**: place the most specific, restrictive, or complex constraints first. This generalizes across model architectures and sizes. **Evidence: strong** (peer-reviewed, ACL 2025).[^13][^14]

- **Instruction sandwich for long context:** OpenAI explicitly recommends placing critical instructions at **both the beginning and the end** of long-context prompts, rather than only once. Placing instructions above context works better than below context when you can only place them once. **This differs from older Anthropic guidance** that recommended putting instructions after the context.[^3][^4]

- **Gemini 3 constraint placement:** Google's official Gemini 3 prompting guide states that negative constraints and formatting/quantitative constraints placed **too early** in the prompt may be dropped; they should be the **final line(s)** of the instruction. **Evidence: strong** (official provider documentation, June 2026).[^6]

### A.4 Formatting Tokens: What Costs What

Markdown is approximately 15% more token-efficient than JSON for equivalent structured information. XML sits between them — more verbose than raw prose but significantly less so than JSON for nested structures.[^9]

Anthropic's Opus 4.8 documentation introduces a specific caution: if your **prompt is heavily formatted with markdown**, Claude will mirror that formatting in outputs. If you want prose output, write your prompt in prose; if you want markdown output, structure your prompt with markdown. This bidirectional formatting mirror is now documented behavior, not anecdote.[^5]

***

## Part B: Compaction Techniques That Preserve Fidelity

### B.1 Algorithmic Prompt Compression

The most rigorously evaluated compaction approaches as of 2026:

| Method | Compression Ratio | Performance Impact | Evidence Level |
|--------|------------------|-------------------|----------------|
| **LLMLingua** (Microsoft, 2023) | Up to 20x | Minimal loss at 3–5x; degrades above 10x | Strong — peer-reviewed[^15][^16] |
| **LLMLingua-2** (Microsoft, 2024) | 2x–5x | 1.6x–2.9x end-to-end latency reduction; 3–6x faster than LLMLingua | Strong — arXiv 2403.12968[^17][^18] |
| **LongLLMLingua** | 4x with +17.1% performance improvement | Query-aware, reorganizes context | Moderate — Microsoft Research[^16] |
| **Selective Context** | ~2x | 32% inference time reduction, 50% context cost reduction | Moderate — original paper[^18] |
| **TOON (Token-Oriented Object Notation)** | 40–55% fewer tokens than JSON | 76.4% accuracy vs. JSON's 75.0% | Moderate — arXiv 2603.03306, but with caveats[^19][^20] |

**How LLMLingua works:** Uses a small language model (SLM) to score token information entropy in the prompt, then iteratively drops low-information tokens via a budget controller. LLMLingua-2 reformulates this as a token classification problem (preserve/discard) using a bidirectional encoder (XLM-RoBERTa-large or mBERT), enabling task-agnostic compression and 3–6x speed improvement over the original.[^17]

**TOON caveats (Evidence: moderate with important caveats):** TOON combines YAML-style nested objects with CSV-style flat arrays to save tokens. It achieves ~40% token savings vs. compact JSON and ~55% vs. pretty-printed JSON. However, since TOON is absent from most model training data, it requires an overhead "prompt tax" of instructional explanation, which eliminates gains for shorter prompts. The efficiency advantage only materializes for longer structured data contexts where cumulative savings exceed the prompt overhead. TOON is currently experimental; JSON with constrained decoding outperforms it for simple structures.[^19][^21]

### B.2 Manual / Structural Compaction

For practitioners who do not want to run a compression pipeline, the following techniques are evidence-backed:

**Use abbreviations and schemas consistently.** Instead of repeating full field names across a structured data dump, declare a schema once and use abbreviated row notation. Teams commonly report 30–60% token reductions without accuracy loss using combined techniques (schema declaration + TOON-like row notation + compressed user history). **Evidence: moderate** (practitioner reports; no controlled benchmark cited).[^22]

**Batch multiple data points per prompt.** The BatchPrompt technique processes multiple inference requests in a single prompt rather than individually, with Batch Permutation and Ensembling (BPE) used to counteract positional bias in batched outputs. This reduces per-item prompt overhead significantly but requires ensemble logic.[^23]

**Reference static instructions instead of repeating them.** In agentic workflows with repeated calls, storing large instruction blocks in a persistent system prompt and referencing them symbolically (or using a memory/tool call) rather than injecting them into every context turn is the highest-leverage compaction technique.[^22]

**Be specific about length, not vague.** "Be concise" is an underspecified instruction and causes variance. "Limit your response to 2–3 sentences" is specific and consistently obeyed. Specifying sentence or word counts is more token-efficient than hedging instructions like "be brief but thorough." **Evidence: strong** — cited in Anthropic's Zack Witten talk (2024) and consistent with Claude 4.x documentation.[^24]

**Eliminate filler and social preamble.** Instructions like "Please kindly consider..." add no semantic value. Frontier models in 2026 do not perform better with polite phrasing — they are trained on instruction-following, not social dynamics. Stripping preamble is pure token savings with zero fidelity cost. **Evidence: strong** (OpenAI internal testing cited in GPT-4.1 guide).[^4]

### B.3 What NOT to Compress

Do not compress:
- **Few-shot examples** — removing examples from complex or domain-specific tasks measurably degrades output quality[^25][^26]
- **Tool descriptions in agentic contexts** — vague tool names and descriptions are a primary failure mode in agentic workflows; OpenAI found a 2% SWE-bench score increase from using properly described tools vs. schema-injected descriptions[^4]
- **Critical constraints** — particularly negative constraints and quantitative constraints, which are the first to be dropped when compressed away from their optimal position in the prompt

***

## Part C: What Newer Models Reward vs. Penalise — Stale 2023–24 Advice

### C.1 GPT-4.1 and GPT-5.x (OpenAI)

**GPT-4.1** (released April 2025) and the subsequent GPT-5.x series represent a qualitative shift in instruction adherence behavior:[^27][^4]

**What changed:**
- GPT-4.1 and later models **follow instructions literally and precisely** rather than inferring intent. Prompts tuned for GPT-4o that relied on the model to "fill in the blanks" may produce unexpected results when ported to GPT-4.1+[^28][^4]
- GPT-5 is described by OpenAI as "significantly better at instruction following" and more sensitive to instruction style — it will follow an instruction tightly once the pattern is established[^27]
- GPT-5.5 Instant (rolled out May 2026) defaults to **fewer bullets and fewer overly long responses**, directly as a policy update to reduce over-formatting[^29]

**What works now:**
- Explicit, direct sentences. "Do X in Y format." Not "You might want to consider doing X."
- Instructing both what TO do and what NOT to do, since literalism means the model will not infer implicit prohibitions[^28][^4]
- Single clear corrective sentences. OpenAI reports that one firm sentence is almost always sufficient to steer the model back on track[^4]

**What no longer works (GPT-4.1+):**
- **[OUTDATED]** All-caps emphasis (e.g., "NEVER DO X"). OpenAI explicitly states: "It's generally not necessary to use all-caps or other incentives like bribes or tips." If your existing prompt contains heavy caps emphasis, it may cause GPT-4.1 to over-attend to those instructions at the expense of others[^4]
- **[OUTDATED]** "Tip incentives" or reward framing ("I'll tip you $100 if..."). These originated in GPT-3.5 era tricks; they are counterproductive on GPT-4.1+[^4]
- **[OUTDATED]** Over-permissive implicit rules. If a rule was implicit and GPT-4o respected it anyway, GPT-4.1 likely will not unless stated explicitly[^28]

### C.2 Claude Opus 4.x (Anthropic)

Anthropic's Claude Opus 4.x series (including 4.5, 4.6, 4.7, and 4.8 as of mid-2026) has iterated significantly on agentic behavior, adaptive thinking, and literal instruction following:[^5]

**Claude Opus 4.8 specific changes:**
- **Adaptive thinking** (off by default; enable with `thinking: {type: "adaptive"}`). The model dynamically decides when and how much to think. This has replaced the older `budget_tokens` extended thinking parameter, which is now deprecated[^5]
- **Effort parameter** replaces manual thinking budget. Scale: `low`, `medium`, `high`, `xhigh`, `max`. For coding and agentic tasks, start with `xhigh`; for most intelligence-sensitive tasks, minimum `high`[^5]
- **More literal interpretation** at lower effort levels. Claude 4.8 at `low` effort does not silently generalize an instruction from one item to another. If you need Claude to apply a rule broadly, state the scope explicitly[^5]

**What works now:**
- XML tags for structural separation of content types (officially documented and trained behavior)[^7]
- Positive instructions over negative instructions. "Write in flowing prose paragraphs" outperforms "Do not use bullet points." The latter triggers compliance anxiety; the former provides a positive target[^5]
- Providing **why** behind instructions, not just what. Anthropic documentation states that Claude is "smart enough to generalize from the explanation," and the rationale improves targeted response quality[^5]

**What no longer works (Claude 4.x):**
- **[OUTDATED]** Aggressive forcing language. Prompts written for Claude 3.x with "CRITICAL: You MUST use this tool when..." will now cause over-triggering. Replace with normal language: "Use this tool when..."[^5]
- **[OUTDATED]** Explicit `budget_tokens` extended thinking configuration. This API parameter is deprecated; use the effort parameter and adaptive thinking instead[^5]
- **[OUTDATED]** Prefilled assistant responses. Starting with Claude 4.6, prefilled responses on the last assistant turn return a 400 error. This previously-common technique for constraining output format is no longer supported[^5]
- **[OUTDATED]** "Be concise" without specifics. Claude 4.x calibrates response length to task complexity, not to vague brevity instructions. Specify the format concretely[^5]

### C.3 Gemini 3.x (Google)

Google's Gemini 3 prompting guide (official documentation, last updated June 1, 2026) is the most specific of the three provider guides about failure modes:[^6]

**What works now:**
- Temperature at default (1.0). Gemini 3's reasoning is optimized for this; lowering temperature may cause looping or degraded performance, especially on math/reasoning tasks[^6]
- Explicit knowledge boundaries: "You are expected to perform calculations and logical deductions based strictly on the provided text. Do not introduce external information." Broad negative constraints ("do not infer") cause the model to over-index and fail basic arithmetic[^6]
- Split-step verification for uncertain capabilities: verify existence of information/capability first, then act[^6]
- Questions and specific instructions placed **at the end** of large data contexts, with anchoring phrases like "Based on the entire document above..."[^6]

**What no longer works (Gemini 3):**
- **[OUTDATED]** Broad blanket negative constraints. "Do not infer" or "do not guess" without specification causes the model to fail basic logic operations[^6]
- **[OUTDATED]** Relying on persona instructions to hold across conflicting task instructions. Gemini 3 takes assigned personas seriously enough that it may ignore task instructions to maintain persona consistency[^6]
- **[OUTDATED]** Reducing temperature below 1.0 for reasoning tasks, which was a common 2023–24 workaround for hallucination. The official guidance is to keep temperature at default[^6]

### C.4 Cross-Model: Role Prompting

**Evidence: moderate — nuanced.** "You are an expert X" role prompting provides marginal benefit for all three frontier models compared to earlier generations. The effectiveness of role prompting has diminished as models have been instruction-tuned more heavily. However, a role in the system prompt still serves a useful function: it sets the **domain expectation and tone** for the interaction, not the model's core capability. Anthropic explicitly recommends a short role sentence as the system prompt opener. Google Gemini notes that personas can cause instruction-override problems if not carefully checked. **Anecdotal consensus:** keep role definitions short (one sentence), domain-specific, and ensure they do not contradict task instructions.[^30][^6][^5]

**[OUTDATED]** Extended "act as" role prompts that attempt to grant special permissions or bypass safety training. These were a 2023-era technique ("Act as DAN," "pretend you have no restrictions") that is both ineffective and counterproductive on 2025–26 frontier models.[^31]

***

## Part D: System Prompt and Agent Instruction Design

### D.1 The Three Non-Negotiable Agent Prompt Components

OpenAI's GPT-4.1 agentic prompting guidance, validated against SWE-bench Verified results, identifies three categories of system prompt reminders that together increased their internal SWE-bench Verified score by nearly 20%:[^4]

**1. Persistence instruction:**
```
You are an agent - please keep going until the user's query is completely
resolved, before ending your turn and yielding back to the user. Only
terminate your turn when you are sure that the problem is solved.
```

**2. Tool-calling instruction:**
```
If you are not sure about file content or codebase structure pertaining
to the user's request, use your tools to read files and gather the relevant
information: do NOT guess or make up an answer.
```

**3. Planning instruction (optional but +4% on agentic benchmarks):**
```
You MUST plan extensively before each function call, and reflect extensively
on the outcomes of the previous function calls. DO NOT do this entire process
by making function calls only.
```

**Evidence: strong** — OpenAI internal SWE-bench Verified with quantified improvement percentages.[^4]

### D.2 Tool Description Design

Tool descriptions are a primary failure mode in agent systems. OpenAI's GPT-4.1 guide is explicit:

- Use the API `tools` field rather than manually injecting tool schemas into the system prompt. OpenAI found a **2% SWE-bench improvement** from API-native tool descriptions vs. manual injection[^4]
- Tool names must clearly indicate purpose
- `description` field: thorough but concise
- Place complex usage **examples in a `# Examples` section of the system prompt**, not in the tool description field
- Each tool parameter needs clear naming and description

For Claude 4.x: the tool-triggering balance has shifted. Claude Opus 4.5–4.6 may over-trigger tools if your prompts contain aggressive forcing language from earlier models. Back off to normal language; the models now trigger tools appropriately without heavy prompting. At `high` or `xhigh` effort, Claude Opus 4.8 shows substantially more tool usage in agentic search and coding scenarios.[^5]

### D.3 System Prompt Architecture for Long-Running Agents

Key principles derived from official provider documentation:

**Context window awareness:** Claude 4.6+ implements explicit context awareness (token budget tracking). If your agent harness compacts context, explicitly tell the model: "Your context window will be automatically compacted as it approaches its limit. Do not stop tasks early due to token budget concerns."[^5]

**State management format:** Use JSON for structured state data (test results, task status); use freeform prose for progress notes. Use git for state tracking across sessions — Claude 4.x models are particularly strong at git-based state tracking.[^5]

**Multi-window workflows:** OpenAI recommends using the first context window to build scaffolding (tests, setup scripts) and subsequent windows to iterate. Instruct the model explicitly on what to review at the start of a new window ("Review progress.txt, tests.json, and git logs").[^5]

**Instruction conflict resolution:**
- GPT-4.1: when instructions conflict, it tends to follow the one **closer to the end** of the prompt[^4]
- Claude: explicit scope statements take precedence over implicit rules[^5]
- Gemini 3: negative constraints placed before the core request are the most likely to be dropped[^6]

### D.4 Agentic Safety Guardrails

Anthropic's Claude Opus 4.6 documentation provides explicit guidance on preventing irreversible actions in agentic contexts:[^5]

```
Consider the reversibility and potential impact of your actions.
Take local, reversible actions by default. For actions that are hard to
reverse (git push --force, rm -rf, dropping database tables) or affect
shared systems, ask the user before proceeding.
```

This type of reversibility-awareness instruction is not needed on chat prompts but is a best practice for any system prompt governing an agent with real-world tool access. **Evidence: strong** (official Anthropic documentation).

### D.5 Sub-agent and Orchestration Prompting

Claude Opus 4.8 tends to spawn fewer subagents by default — but this is steerable. Provide explicit guidance on when to spawn vs. not spawn:

```
Do not spawn a subagent for work you can complete directly in a single
response. Spawn multiple subagents in the same turn when fanning out
across items or reading multiple files.
```

For parallel tool calling: Claude 4.x models excel at parallel tool execution but can be constrained or expanded via prompting. The `<use_parallel_tool_calls>` pattern documented by Anthropic boosts parallel execution to nearly 100%. GPT-4.1 notes some rare failure modes in parallel tool calls; test these paths and consider setting `parallel_tool_calls: false` if issues arise.[^4][^5]

***

## Part E: Evidence Quality Assessment and Outdated Advice Compendium

### E.1 Evidence Quality by Claim

| Claim | Evidence Level | Source |
|-------|---------------|--------|
| XML outperforms JSON for document wrapping | **Strong** | OpenAI Cookbook, GPT-4.1 guide[^4] |
| Constraint order matters (hard-to-easy) | **Strong** | Zeng et al., ACL Findings 2025[^13][^14] |
| Instructions at both ends of long context | **Strong** | OpenAI GPT-4.1 guide[^4] |
| Gemini 3: constraints at end of prompt | **Strong** | Official Google docs, June 2026[^6] |
| LLMLingua-2 3–6x faster compression | **Strong** | arXiv 2403.12968[^17] |
| Agent prompts: 3 components = +20% SWE-bench | **Strong** | OpenAI internal, GPT-4.1 guide[^4] |
| Claude XML tags are trained behavior | **Strong** | Anthropic docs[^7] |
| TOON 40% token savings vs. JSON | **Moderate** | arXiv 2603.03306 with caveats[^19] |
| Markdown ~15% more efficient than JSON | **Moderate** | Community testing[^9] |
| 30–60% token reductions via combined techniques | **Anecdotal** | Practitioner reports[^22] |
| Role prompting marginal benefit on frontier models | **Moderate** | Practitioner consensus[^30] |
| Prompt formatting mirror effect (Claude) | **Moderate** | Official Anthropic docs[^5] |

### E.2 Consolidated List of Outdated 2023–24 Advice

The following techniques were widely recommended in 2023–24 but are now counterproductive or obsolete on frontier models:

1. **[OUTDATED — GPT-4.1+]** ALL-CAPS emphasis for critical instructions. Now causes over-attention and may destabilize other instructions[^4]
2. **[OUTDATED — GPT-4.1+]** Tip/bribe/reward framing ("I'll give you $200 if you do this perfectly"). No effect or negative effect on instruction adherence[^4]
3. **[OUTDATED — Claude 4.x]** Prefilled assistant turns for output control. Returns 400 error on Claude 4.6+[^5]
4. **[OUTDATED — Claude 4.x]** `budget_tokens` extended thinking. Replaced by effort parameter and adaptive thinking[^5]
5. **[OUTDATED — Claude 4.x]** Aggressive forcing language ("CRITICAL: You MUST..."). Causes over-triggering in tool use[^5]
6. **[OUTDATED — Gemini 3]** Temperature reduction below 1.0 for reasoning. Now causes looping and degraded performance[^6]
7. **[OUTDATED — Gemini 3]** Broad blanket negative constraints ("Do not infer"). Over-indexes and prevents basic logic[^6]
8. **[OUTDATED — all models]** JSON for long-context document wrapping. OpenAI explicitly identifies this as a poor-performing pattern[^4]
9. **[OUTDATED — all models]** "Act as DAN" / extended jailbreak persona prompts. Ineffective and counterproductive on 2025–26 models[^31]
10. **[OUTDATED — all models]** Relying on GPT-4o-era implicit rule inference with GPT-4.1+. The model no longer fills in unspecified rules[^28]
11. **[OUTDATED — all models]** Manual injection of tool schemas into system prompt body. API-native tool definitions outperform injected schemas by measurable margins[^4]
12. **[OUTDATED — all models]** Context-first, instructions-last ordering for long prompts (the pattern where you dump a long document then add instructions at the very end). OpenAI now recommends instructions both before and after; Google recommends instructions with constraints at end specifically[^6][^4]

### E.3 The "Context Engineering" Reframe

The term "context engineering" — coined in wide use by Andrej Karpathy in mid-2025 — captures the shift in what matters: the LLM is the CPU, the context window is RAM, and the developer's job is operating system: loading exactly the right information for each task. Practical sweet spot for general instructions: 150–300 words. Beyond that, additional instructions increase the risk of conflict and distraction without proportional benefit.[^10][^1]

**What this means for practitioners:**
- Treat information selection and curation as higher-priority than instruction phrasing
- A smaller, well-ordered context frequently produces better results than a large, unstructured one[^10]
- Build evals that measure constraint adherence and grounding — these are the metrics most sensitive to prompt architecture decisions[^10]

***

## Part F: Quick-Reference Cross-Model Matrix

| Consideration | GPT-4.1 / GPT-5.x | Claude Opus 4.x | Gemini 3.x |
|--------------|-------------------|-----------------|------------|
| **Primary delimiter** | Markdown headings | XML tags | Structured steps |
| **Instruction position** | Both ends of long context[^4] | After context (for long docs)[^5] | Constraints at end[^6] |
| **Constraint order** | Hard-to-easy (research-backed)[^13] | Hard-to-easy (research-backed)[^13] | Hard-to-easy (research-backed)[^13] |
| **Role prompting** | Brief, one sentence | Brief, one sentence | Brief; avoid persona-task conflicts |
| **Chain of thought** | Must be explicitly requested[^4] | Adaptive thinking at `high`+ effort[^5] | Set thinking level explicitly[^6] |
| **Tool description** | API field, not injected[^4] | Explicit trigger language[^5] | Native API[^6] |
| **Output length control** | Explicit format + example | Positive instruction + format spec[^5] | Explicit verbosity steering[^6] |
| **Temperature** | Default | Default | Keep at 1.0 — critical[^6] |
| **Avoid** | ALL-CAPS, tips, JSON wrappers[^4] | `budget_tokens`, prefill, CRITICAL:[^5] | Broad negatives, reduced temp[^6] |

***

## Conclusion and Actionable Priorities

For any team building on frontier LLMs in 2026, the highest-leverage changes from 2023–24 practice are:

1. **Audit your delimiter strategy.** Switch document wrapping from JSON to XML or the Lee et al. pipe-delimited format.
2. **Reorder constraints hard-to-easy.** Empirical research is clear: place specific/restrictive constraints before general ones.[^13]
3. **Implement the instruction sandwich for long context.** Critical rules at the start AND end of the context block.[^4]
4. **Strip aggressive emphasis from agent system prompts.** ALL-CAPS and "CRITICAL/MUST" language is counterproductive on GPT-4.1+, and over-triggers tool use on Claude 4.x.[^4][^5]
5. **Use native API tool definitions.** Never manually inject tool schemas into the system prompt body.[^4]
6. **Add the three agent reminders.** Persistence, tool-calling, and planning — for any production agent using GPT-4.1+, these are no longer optional given their measured impact.[^4]
7. **Build evals.** The practitioner-consensus claim that "the best prompt depends on your use case" is genuinely true at this level of model capability. Measure constraint adherence, grounding, and coverage; treat prompt architecture as a versioned artifact.

> **Ongoing monitoring note:** GPT-5.x is still being actively updated (GPT-5.5 Instant as of May 2026); Claude Opus 4.8 is the current Anthropic flagship as of mid-2026; Gemini 3 prompting guide was last updated June 1, 2026. All three families are iterating rapidly. Any specific parameter (effort levels, API fields, thinking modes) should be cross-referenced against the current official documentation before production deployment.[^29][^6][^5]

---

## References

1. [Context Engineering Guide 2026: GPT-5, Claude 4.6, Gemini ...](https://www.the-ai-corner.com/p/context-engineering-guide-2026) - Prompt Engineering Is Dead. Context Engineering Is What Matters Now. The techniques that worked in 2...

2. [Context engineering vs. prompt engineering: Key differences ...](https://www.glean.com/perspectives/context-engineering-vs-prompt-engineering-key-differences-explained) - While prompt engineering focuses on crafting precise input to elicit desired responses from AI model...

3. [How to use GPT-4.1: 13 tips from OpenAI's guide - LinkedIn](https://www.linkedin.com/posts/gisenberg_openai-published-their-official-gpt-41-prompting-activity-7318092631102640128-7BLl) - OpenAI published their official GPT-4.1 prompting guide, and I summarized it into these 13 practical...

4. [gpt4-1_prompting_guide.md](https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide.md)

5. [Corporate clairvoyant](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) - Comprehensive guide to prompt engineering techniques for Claude's latest models, covering clarity, e...

6. [Gemini 3 prompting guide | Gemini Enterprise Agent Platform](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/start/gemini-3-prompting-guide) - Learn prompting strategies and best practices for using Gemini 3 models on Gemini Enterprise Agent P...

7. [Use XML tags to structure your prompts - Claude Docs](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags) - Claude API Documentation

8. [Gunakan tag XML untuk menyusun prompt Anda](https://docs.anthropic.com/id/docs/build-with-claude/prompt-engineering/use-xml-tags)

9. [XML vs Markdown for high performance tasks - Prompting](https://community.openai.com/t/xml-vs-markdown-for-high-performance-tasks/1260014) - Use XML tags to structure my prompts. Markdown is 15% more token efficient than JSON Prompting outpu...

10. [How does context ordering influence LLM responses? - Deepchecks](https://deepchecks.com/question/context-ordering-impact-on-llm-responses/) - There's also a known long-context effect sometimes described as 'lost in the middle,' where models m...

11. [Why Instruction Order Matters for LLMs: New Evidence From Long ...](https://www.linkedin.com/pulse/why-instruction-order-matters-llms-new-evidence-from-testing-roth-8iuic) - Views expressed here are my own and do not express the views or opinions of my employer. TL;DR GPT-5...

12. [Lost in the Middle: How Language Models Use Long Contexts - arXiv](https://arxiv.org/abs/2307.03172) - We analyze the performance of language models on two tasks that require identifying relevant informa...

13. [Order Matters: Investigate the Position Bias in Multi-constraint Instruction Following](https://arxiv.org/abs/2502.17204) - Real-world instructions with multiple constraints pose a significant challenge to existing large lan...

14. [Investigate the Position Bias in Multi-constraint Instruction Following](https://aclanthology.org/2025.findings-acl.646/) - Through the experimental results, we find that LLMs are more performant when presented with the cons...

15. [LLMLingua: Compressing Prompts for Accelerated Inference ... - arXiv](https://arxiv.org/html/2310.05736v2)

16. [LLMLingua Series - Microsoft Research](https://www.microsoft.com/en-us/research/project/llmlingua/) - A series of works that try to build a language for LLMs via prompt compression. This approach accele...

17. [[2403.12968] LLMLingua-2: Data Distillation for Efficient ...](https://arxiv.org/abs/2403.12968) - This paper focuses on task-agnostic prompt compression for better generalizability and efficiency. C...

18. [Three prompt compression methods to save time and money](https://shchegrikovich.substack.com/p/three-prompt-compression-methods) - Microsoft's LLMLingua can compress prompts by 20x. LLMLingua is based on the same idea as the Select...

19. [Token-Oriented Object Notation vs JSON: A Benchmark of Plain and ...](https://arxiv.org/abs/2603.03306) - Key findings: TOON shows promising accuracy/token consumption ratio for in-domain generation tasks, ...

20. [New Token-Oriented Object Notation (TOON) Hopes to Cut LLM ...](https://www.infoq.com/news/2025/11/toon-reduce-llm-cost-tokens/) - TOON hits 99.4% accuracy on GPT 5 Nano while using 46% fewer tokens. Tested across ~160 questions an...

21. [TOON – Token Oriented Object Notation | Hacker News](https://news.ycombinator.com/item?id=45715632) - My expectation is that accuracy will take a hit on mid or longer context prompts: I'd bet that the h...

22. [A Practical Guide to Reducing LLM Token Costs: Techniques That ...](https://www.linkedin.com/pulse/practical-guide-reducing-llm-token-costs-techniques-actually-mahmoud-kousc) - Token efficiency can be pushed further through ideas such as hierarchical compression, adaptive summ...

23. [How to Optimize Token Efficiency When Prompting - Portkey](https://portkey.ai/blog/optimize-token-efficiency-in-prompts) - Discover practical techniques to reduce token usage in AI prompts. Learn how to craft concise, effic...

24. [Prompt Engineering with Anthropic Claude | by Jared Zoneraich](https://medium.com/promptlayer/prompt-engineering-with-anthropic-claude-5399da57461d) - Tips on how to prompt Claude more effectively. Take-aways from a talk by Anthropic’s “Prompt Doctor”...

25. [Few-Shot Prompting - Prompt Engineering Guide](https://www.promptingguide.ai/techniques/fewshot) - When zero-shot prompting and few-shot prompting are not sufficient, it might mean that whatever was ...

26. [Prompt engineering for accurate statistical reasoning with large ...](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2025.1658316/full) - Prompt design is a critical determinant of output quality in AI-assisted statistical analysis. Hybri...

27. [Introducing GPT-5 - OpenAI](https://openai.com/index/introducing-gpt-5/) - GPT‑5 is significantly better at instruction following, and we see a corresponding improvement in it...

28. [OpenAI dropped a prompting guide for GPT-4.1, here's what's most ...](https://www.reddit.com/r/LLMDevs/comments/1k6yi75/openai_dropped_a_prompting_guide_for_gpt41_heres/) - Since the model follows instructions more literally, developers may need to include explicit specifi...

29. [ChatGPT — Release Notes - OpenAI Help Center](https://help.openai.com/en/articles/6825453-chatgpt-release-notes) - Starting today, we're rolling out memory improvements to ChatGPT Plus and Pro users that make respon...

30. [Google Gemini 2.5 Pro Prompts | Shushant Lakhyani | 126 comments](https://www.linkedin.com/posts/shushant-lakhyani_google-gemini-25-pro-prompts-activity-7376842930046701568-IAhW) - Learn how to find, install, and use Google Gemini CLI extensions. This guide shows you how to connec...

31. [ChatGPT-Dan-Jailbreak.md · GitHub](https://gist.github.com/coolaj86/6f4f7b30129b0251f61fa7baaa881516?permalink_comment_id=5702445) - They all exploit the "role play" training model. The Jailbreak Prompt Hello, ChatGPT. From now on yo...

