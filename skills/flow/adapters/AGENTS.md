<!-- Flow adapter: Codex, Amp, Jules, Zed, and anything else reading AGENTS.md -->

# Design rules

Any work that touches user interface code follows **Flow**.

**Before changing any styling**, read `flow/skills/flow-principles/SKILL.md`. It contains the intent gate and the twelve-item violation taxonomy. Do not restyle anything before stating the surface's purpose, its single primary action, its reading order, and its density class.

Cite findings by taxonomy ID (`FLOW-01` through `FLOW-12`). A styling change with no ID behind it is personal preference and does not ship.

## Task routing

| Task | Read |
|---|---|
| Review or critique an interface | `flow/skills/flow-audit/SKILL.md` |
| Restyle, tidy, or fix a design | `flow/skills/flow-apply/SKILL.md` |
| Establish or audit the design scale | `flow/skills/flow-tokens/SKILL.md` |

Load files under `flow/references/` only when a specific finding needs them. The table at the end of `flow-principles` says which file serves which violation.

## Numbers

Never estimate a contrast ratio, a character count, or whether a value is on the scale. Run the scripts:

```
python3 flow/scripts/contrast.py "#18181B" "#FFFFFF"
python3 flow/scripts/scan_tokens.py lib/ --config flow.config.json
```

Values come from `flow.config.json` if it exists, otherwise `flow/tokens/flow.defaults.json`. If a fix needs a value that is not in the resolved set, do not invent one: report it as a token gap.
