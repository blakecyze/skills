# Measurement tools

Run tools only when their output answers a relevant question. Paths below are relative to this skill directory; resolve them from the installed SKILL.md, not the target project's working directory.

- [contrast.py](../scripts/contrast.py): `python3 <skill>/scripts/contrast.py '#18181B' '#FFFFFF'` computes a pair; `--scan <path>` finds literal pairs to inspect. Confirm the actual composited colours and applicable requirement before claiming a failure.
- [scan_tokens.py](../scripts/scan_tokens.py): `python3 <skill>/scripts/scan_tokens.py <path> --report frequency` inventories repeated values. Use `--config <project>/flow.config.json` when a project configuration exists.
- [flow.defaults.json](../tokens/flow.defaults.json) supplies scanner defaults. These are example scales, not a standard the project must obey. A value outside them is not automatically a defect.

Run `--help` for supported options. Scanners use Python's standard library and share [flowlib.py](../scripts/flowlib.py). Static extraction can miss computed styles, runtime themes, and framework abstractions. Treat its output as investigation leads and verify the rendered result.

Token discovery need not write configuration. Create or update a token system only when that work is within the brief and offers a concrete benefit.
