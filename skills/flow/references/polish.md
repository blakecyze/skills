# The polish contract

Loaded whenever a polish-layer skill runs. Every domain skill (`flow-surface`, `flow-type`, `flow-colour`, `flow-layout`, `flow-access`, `flow-copy`) works under these terms, stated once here so the skills stay short.

**Scope.** Same grammar as `flow-audit`: `diff` (default), a module path, or `all`. Resolve it before reading anything else.

**Idempotent.** A second run over already-polished code proposes nothing and says so in one line. If a run keeps finding work in the same file, the rules and the repo disagree; surface that instead of re-editing.

**Findings before fixes.** Each pass emits Flow-format findings first (`[n] path:line, ID or domain, tier, one-line fix`), then the standard approval gate. Cite a FLOW or FLOW-M ID when one applies; otherwise the domain name is the ID. Fixes land only after approval, and are appearance-only, except `flow-copy`, which touches interface strings alone.

**The repo wins.** Existing tokens, scales, and conventions beat the values in these references. A codebase with a coherent 6px radius system does not get 8px imposed on it; the finding is internal inconsistency, never disagreement with Flow's defaults.

**Numbers are quoted.** Every value comes from the domain's reference file. Contrast is computed with `scripts/contrast.py`, scale membership with `scripts/scan_tokens.py`. A remembered number is a fabricated one.

**Small diffs.** One domain per skill, one concern per edit, no drive-by fixes from another domain. If a `flow-type` pass notices a colour problem, it names it for `flow-colour` and moves on.

**The signal rule holds.** Tier 1 and 2 below 60% of findings means the pass is generating noise; cut Tier 3.
