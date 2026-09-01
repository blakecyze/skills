---
name: mimesis-design
description: "Use when the user wants to know if an interface looks AI-generated, or wants the machine-made design tells stripped: \"is this design AI-generated\", \"de-slop this UI\", \"does this look vibe-coded\", \"why does this look like every AI site\". Read-only audit of supplied markup, CSS, or a described UI against the design-tells reference: purple gradients, Inter 700, three-card feature rows, glassmorphism, emoji bullets, centred everything, gradient pills. Flags each with location and severity. Not for general design critique or visual feedback unrelated to de-AI-ing an interface."
argument-hint: "[file/dir path | described UI]"
allowed-tools: Bash(rg *) Bash(find *) Read
---

# mimesis-design

Domain A, machine-design side. Flag the aesthetic defaults that mark an interface
as AI-built. Read-only: this skill reports, it does not edit. It never runs the
prose humanisation linter; that is a different medium and a different domain.

## How a run works

1. Read [reference/design-tells.md](../../reference/design-tells.md) on every run.
   It is the L1 corpus and it outranks any taste call.
2. If given markup or CSS files, run the grep set. The reference tags each tell
   `[grep]` or `[judgement]`. Use ripgrep for the `[grep]` ones, for example:

   ```
   rg -n --no-heading -e 'from-purple' -e 'to-indigo' -e '#7C3AED' \
     -e 'bg-clip-text' -e 'font-bold' -e 'rounded-\[?2[4-9]' \
     -e 'hover:scale-' -e 'transition-all' -e 'ease-elastic' \
     -e 'streamline|supercharge|world-class|enterprise-grade' <path>
   ```

   Tune the patterns to what the reference lists. grep finds the candidates; you
   confirm each is an actual tell in context, not a false hit.
3. Apply judgement to the `[judgement]` tells the grep set cannot see: centred
   everything, the three-card row, nested cards, oversized hero headline,
   monotonous spacing rhythm, modal abuse, redundant UX writing.
4. If given a described UI rather than code, skip the grep step and work entirely
   from the reference by judgement.

## The slop test

The framing question, from the research: would a viewer's first reaction be
"which AI made this" rather than "how was this made". A tell only matters if it
pushes the interface toward the first reaction. Do not flag a purple accent that
is clearly a deliberate brand choice; flag the reflexive defaults.

## Output

A tight report. No preamble.

```
# Design audit: <short scope>

**Tells:** <n> blocker, <n> important, <n> polish

[1] hero.tsx:14 (important) purple-to-indigo gradient hero: the headline tell
[2] globals.css:3 (important) Inter 700 as the only display face
[3] features.tsx:40 (judgement) three identical feature cards in a row
```

One line per tell. Use `path:line` for grep hits, a component or section name for
judgement calls. Lead with the loudest tells (gradient hero, Inter, three-card
row). Group the structural causes at the end in one line: the shared root is
almost always the shadcn and Tailwind defaults, so name the fix at the token
level, not the element level.

## What this skill never does

- Edit files. It is read-only, like an audit.
- Run the prose humanisation linter. Body copy tells live in
  [reference/tells.md](../../reference/tells.md); route copy to `/mimesis-human`.
- Flag a deliberate, context-specific choice as a tell. Intentional asymmetry,
  tinted neutrals and a real font pairing are the opposite of slop.
- Promise a redesign. It diagnoses; the fix is the user's, or a follow-up.
