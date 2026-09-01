# Flow

A design skill library for AI coding agents. Point it at a Flutter page, a React component, a stylesheet, or a screenshot, and it works out what the surface is for, then finds where the interface contradicts its own purpose.

Flow is diagnostic, not generative. It will not invent a visual identity for you. It finds the twelve ways interfaces routinely undermine themselves, cites each one by ID, and repairs it with the smallest change available.

Works with Claude Code, Cursor, Codex, Copilot, and anything else that reads a file.

## Why it works

Most design guidance given to language models is prose about gestalt principles. Models already know the words. Reciting them changes nothing, because a principle without a check is an opinion, and opinions do not survive contact with a diff.

Flow makes three moves instead:

**The intent gate.** No styling change is allowed before the model states the surface's purpose, its single primary action, its reading order, and its density class. Hierarchy is derived from those four answers, not chosen. This is what stops a model from prettifying a screen it does not understand.

**A named taxonomy.** Twelve violations, each with an ID, a check that can be evaluated against the source, and a specific fix. Findings are searchable, consistent across sessions, and consistent across tools. `FLOW-06` means the same thing in Cursor as it does in Claude Code.

**Computed numbers.** Contrast ratios, scale membership, and line measure come from scripts. A model-estimated contrast ratio is a fabricated one, and fabricated accessibility numbers are worse than none.

## The taxonomy

| ID | Violation |
|---|---|
| FLOW-01 | Uniform spacing |
| FLOW-02 | Flat hierarchy |
| FLOW-03 | Orphaned label |
| FLOW-04 | Off-scale value |
| FLOW-05 | Decoration without function |
| FLOW-06 | Competing emphasis |
| FLOW-07 | Broken optical alignment |
| FLOW-08 | Density mismatch |
| FLOW-09 | Unearned colour |
| FLOW-10 | Container theatre |
| FLOW-11 | Unstyled state |
| FLOW-12 | Runaway measure |

Full definitions, checks, and fixes: [`skills/flow-principles/SKILL.md`](skills/flow-principles/SKILL.md).

## The skills

| Skill | Does | Edits files |
|---|---|---|
| `flow-principles` | Standing context. Taxonomy and intent gate. Auto-loads. | no |
| `flow-audit` | Read-only review, tiered findings report | no |
| `flow-apply` | Repairs violations, appearance only | yes |
| `flow-tokens` | Discovers a project's real scale, writes `flow.config.json` | one file |

Run `flow-tokens` first on an unfamiliar codebase. Without it, Flow measures your project against its own defaults, and every finding becomes noise.

## Install

### Claude Code (recommended)

```
/plugin marketplace add blakecyze/skills
/plugin install flow@cyze
```

`flow-principles` then loads automatically for UI work. The other three are invoked by name: `/flow-audit`, `/flow-apply`, `/flow-tokens`.

To develop against a local checkout instead:

```bash
claude --plugin-dir ./flow
claude plugin validate ./flow --strict
```

### Everything else

One command, any agent that supports skills:

```bash
npx skills@latest add blakecyze/skills
```

Or clone and run the installer:

```bash
git clone https://github.com/blakecyze/skills.git
./skills/skills/flow/install.sh
```

The installer detects what the project already uses and writes only the adapters that apply. Or be explicit:

```bash
./flow/install.sh --cursor     # .cursor/rules/flow.mdc
./flow/install.sh --agents     # appends to AGENTS.md, for Codex, Amp, Zed
./flow/install.sh --copilot    # .github/copilot-instructions.md
./flow/install.sh --all
./flow/install.sh --check      # verify an existing install
```

Each adapter is a short pointer at the canonical skills, so there is one source of truth and nothing to keep in sync.

### Anything with no config mechanism at all

Paste `skills/flow-principles/SKILL.md` into whatever standing-context box the tool provides. Everything else is Markdown, JSON, and stdlib Python, reachable by file path.

## Layout

```
flow/
  .claude-plugin/       # plugin manifest and marketplace catalogue
  skills/               # tier 1: the always-loaded rules
    flow-principles/    # taxonomy and intent gate, canonical
    flow-audit/         # read-only review
    flow-apply/         # repair, appearance only
    flow-tokens/        # scale discovery
  references/           # tier 2: loaded on demand, one per domain
    spacing.md  type.md  colour.md  interaction.md
    flutter.md  web.md
  tokens/               # tier 3: never paraphrased, only read
    flow.defaults.json
  scripts/              # tier 3: never estimated, only run
    contrast.py  scan_tokens.py
  adapters/             # thin pointers for non-Claude tools
  install.sh            # one command for tools without a plugin system
```

Three tiers, and the tier decides the format. Tier 1 costs tokens on every call, so it is kept to roughly a page. Tier 2 holds judgement calls, which need prose, and loads only when a finding needs it. Tier 3 holds numbers, which a model must never write from memory.

## Configuration

`flow-tokens` writes `flow.config.json` at your project root. It is merged over `tokens/flow.defaults.json`, so it only needs to contain what differs. A short config is a healthy sign.

```json
{
  "density": "dense",
  "spacing": { "base": 4, "ramp": [4, 8, 12, 16, 24, 32, 48] },
  "type": { "ratio": 1.125, "measure": 68 },
  "notes": "Legacy 13px body size retained in settings/*; migration tracked in #104."
}
```

The `notes` field records deliberate exceptions so the next audit does not re-flag them.

## Scripts

Stdlib Python 3, no dependencies.

```bash
# One pair, WCAG 2.1
python3 scripts/contrast.py "#A1A1AA" "#FFFFFF"

# Every colour in a tree, against the extreme backgrounds
python3 scripts/contrast.py --scan lib/ --config flow.config.json

# Values that escape the scale
python3 scripts/scan_tokens.py lib/

# What the scale actually is, as opposed to what the theme file claims
python3 scripts/scan_tokens.py lib/ --report frequency
```

## What Flow will not do

- Change behaviour, state, routing, or data flow. Appearance only.
- Invent a brand, a typeface, or a colour identity.
- Flag a coherent house style as an error because it is not to its taste.
- Estimate a number a script can compute.
- Produce a finding without an ID, a location, and a specific fix.

## Related

Part of [blakecyze/skills](https://github.com/blakecyze/skills), a set of skill libraries built on the same idea: name the failure, give it a check, keep the always-loaded layer short.

- [kanso](../kanso) — anti-dilution code principles
- [mimesis](../mimesis) — human prose out, machine prose in
- [swarm](../swarm) — agent orchestration with a cost ceiling

## Licence

MIT.

Flow encodes design reasoning in its own words. It does not vendor, mirror, or redistribute any commercial component library's source or token files.
