# Build prompt — `mimesis` / `humanise` skill

Paste this into Claude Code from the directory holding the three research docs
(`01-the-tells.html`, `02-the-craft.html`, `03-the-skill.html`). Adjust the
suite name if you settled on something other than `mimesis`.

---

Read `01-the-tells.html`, `02-the-craft.html` and `03-the-skill.html` in full
before writing anything. They are the spec. Then scaffold a Claude Code skill
that follows our kanso conventions (match the structure and tone of the existing
`kanso-*` skills already on this machine).

## What to build

A skill named **mimesis** that humanises writing and removes modern AI tells.
Command verb: `/humanise`.

### Non-negotiable design: guidelines outrank the model

Implement the three-layer precedence stack from doc 03, in this order:

1. **L1 guideline corpus** — distil docs 01 and 02 into `reference/tells.md` and
   `reference/craft.md`. The skill reads these on every run. Primary,
   model-independent, never skipped. Keep `tells.md` versioned by model era
   (GPT-4 / GPT-4o / GPT-5) since the kill list drifts.
2. **L2 deterministic linter** — a script that flags, regardless of model:
   em dashes (and the spaced-hyphen and en-dash-as-em workarounds), smart quotes,
   every blacklist word from `tells.md`, and "not X but Y" / "it's not X it's Y"
   patterns. This runs on all output, including anything a generator produced.
3. **L3 generator (optional, swappable)** — Claude by default. Detect `codex` on
   `PATH`; only if present AND the user passes `--gen codex` do we route the
   generate step to GPT-5.5. Never auto-route. Default path stays predictable.
   Whatever generates, L1 and L2 always run afterwards.

### Three modes

- `audit` — read-only. Report every tell with location, category and severity.
- `rewrite` — meaning-preserving humanisation of existing text. Never change a
  factual claim. Never fabricate experience or anecdotes.
- `generate` — draft new, already-humanised text.

Detect mode from the user's phrasing; default to `audit` when ambiguous.

### Two absolute rules

- **Zero em dashes, ever.** The linter strips and restructures into commas, full
  stops, parentheses or two sentences. Not a swap, a restructure.
- **Catch the merely-perceived.** Flag and rewrite tricolons, participle tails
  ("highlighting...", "underscoring..."), dutiful sign-offs and antithesis even
  when grammatically fine. Apply the final-pass checklist from doc 02.

### File shape (mirror the kanso skills)

```
mimesis/
├─ SKILL.md            # description, triggers, the three modes
├─ reference/
│  ├─ tells.md         # from doc 01, versioned by model era
│  └─ craft.md         # from doc 02 + the final-pass checklist
├─ linter              # the deterministic pass (L2)
└─ codex.md            # optional generator: detection + opt-in gate
```

### SKILL.md description / triggering

Tune the description to fire on: "make this sound human", "humanise this",
"does this read as AI", "remove AI tells", "de-slop this", "make this less
ChatGPT". Match the precision of our existing kanso descriptions. Do not fire on
generic writing requests that are not about de-AI-ing text.

## Constraints

- UK spelling throughout the skill and its output.
- No em dashes anywhere in the skill files themselves (we eat our own cooking).
- Prefer a behaviour-preserving, restrained implementation. No dependencies the
  kanso suite does not already use.

## Before you start

Ask me anything ambiguous, then propose the `SKILL.md` description and the
linter's pattern list for my sign-off before writing the rest.
