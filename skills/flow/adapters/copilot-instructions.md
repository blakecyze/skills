<!-- Flow adapter: GitHub Copilot. Place at .github/copilot-instructions.md -->

# Design rules

UI work in this repository follows Flow.

Before changing styling, read `flow/skills/flow-principles/SKILL.md` and state the surface's purpose, its single primary action, its reading order, and its density class.

Cite findings by taxonomy ID (`FLOW-01` to `FLOW-12`). Spacing, type, radius, and colour values come from `flow.config.json`, or from `flow/tokens/flow.defaults.json` if no project config exists. Never introduce a value that is not in the resolved set.

Run `python3 flow/scripts/contrast.py` and `python3 flow/scripts/scan_tokens.py` rather than estimating any number.

Styling changes never alter behaviour.
