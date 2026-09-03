---
name: flow-tokens
description: Use when a project has no design tokens, has an inconsistent scale, or before running flow-audit on an unfamiliar codebase. Extracts the scale that a codebase actually uses and writes flow.config.json.
argument-hint: "[scope: repo root | source directory]"
allowed-tools: Bash(rg *) Bash(find *) Bash(python3 *)
---

# flow-tokens

Discovers the design scale a codebase is actually using, reconciles it against the Flow defaults, and writes `flow.config.json` at the project root. Every other Flow skill resolves its values through that file.

Run this before auditing an unfamiliar codebase. A project's real scale is whatever its code does, not whatever its theme file claims. A theme declaring an 8pt grid while 200 call sites hardcode `13` has a 13 in its scale, and pretending otherwise produces 200 false findings.

## Process

### 1. Find declared tokens

In order of authority:

- `flow.config.json` (already run; offer to refresh instead of overwrite)
- Design token files: `tokens.json`, `*.tokens.json`, Style Dictionary output
- `tailwind.config.*` theme extension
- CSS custom properties in `:root`
- Flutter `ThemeData`, `TextTheme`, and any `AppSpacing`-style constants class
- A Figma export, if the user supplies one

### 2. Find used values

`python3 scripts/scan_tokens.py <path> --report frequency`

Counts every literal spacing, size, radius, and colour value in the source. Scan the source directory, not the repo root, so generated files and vendored code stay out.

### 3. Reconcile

Compare declared against used. Four outcomes:

- **Declared and used often** → real token. Keep.
- **Declared and never used** → dead token. Propose deletion.
- **Undeclared and used often** → de facto token. Promote it into the scale or plan a migration, and say which. Do not silently treat it as a violation.
- **Undeclared and used once or twice** → drift. Snap to the nearest real token.

### 4. Judge the ramp

A healthy spacing ramp is geometric-ish, not linear: `4, 8, 12, 16, 24, 32, 48, 64`. A healthy type scale steps by a consistent ratio, commonly between 1.125 and 1.25 for interfaces.

Flag, but do not auto-fix:

- More than ten distinct spacing values in active use
- Two values within 2px of each other both used more than five times
- A type scale with steps under 2px apart
- More than three border radii
- More than about a dozen distinct colours outside a defined neutral ramp

### 5. Write the config

Write `flow.config.json` at the project root, merged over `tokens/flow.defaults.json`. Only include what differs from the defaults. A short config is a good sign.

```json
{
  "$schema": "https://flow.cyze.dev/schema/v1.json",
  "density": "standard",
  "spacing": { "base": 4, "ramp": [4, 8, 12, 16, 24, 32, 48, 64] },
  "radius": { "sm": 6, "md": 10, "lg": 16, "full": 9999 },
  "type": {
    "ratio": 1.2,
    "scale": { "xs": 12, "sm": 14, "base": 16, "lg": 18, "xl": 24, "2xl": 32 },
    "measure": 72
  },
  "colour": {
    "neutral": ["#FFFFFF", "#FAFAFA", "#F4F4F5", "#E4E4E7", "#A1A1AA", "#52525B", "#27272A", "#18181B"],
    "semantic": { "primary": "#2563EB", "success": "#16A34A", "warning": "#D97706", "danger": "#DC2626" }
  },
  "targets": { "minTouch": 44, "minFocusRing": 2 },
  "notes": "Legacy 13px body size retained in settings/*; migration tracked in FLOW-104."
}
```

The `notes` field records deliberate exceptions so the next audit does not re-flag them.

## Output format

```markdown
## Token report

**Declared source:** `lib/theme/app_theme.dart`
**Files scanned:** 84
**Config written:** `flow.config.json`

### The scale as used

| Value | Count | Status |
|---|---|---|
| 16 | 412 | token |
| 8 | 388 | token |
| 13 | 47 | de facto — promote or migrate |
| 22 | 3 | drift — snap to 24 |

### Health

- 14 distinct spacing values in use. Above the threshold of 10.
- `12` and `13` both in heavy use. One of them should go.
- 4 border radii. One more than the guideline.

### Recommendations

1. <Ordered by call sites affected, cheapest first.>

### Decisions needed

- Is `13px` intentional, or drift from a `12px` ramp? It appears 47 times, so it is now load-bearing either way.
```

## Guardrails

- Writes exactly one file, `flow.config.json`. Never edits source.
- Never overwrites an existing `flow.config.json` without showing the diff first.
- Never auto-migrates values across a codebase. That is a `flow-apply` job, after the config exists and the user has approved the target.
- Discovery precedes opinion. Do not invent a scale for a project that has one.
- Do not recommend a full migration when the cost is hundreds of call sites and the benefit is tidiness.
