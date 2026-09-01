# Changelog

## 0.4.0

Safeguards and self-grading.

- **The craft check**: a self-grading pass after every rewrite or generate.
  Five dimensions (rhythm, earned vocabulary, stance, register fit,
  specificity), each pass or fail, at most two revision loops, reported as one
  line. Deliberately not a score; tells.md section 8 explains why there is no
  number.
- **The register axis**: `--register professional|casual` on `mimesis-human`
  and `mimesis-tone`, with `reference/register.md` defining what casual permits
  (occasional fragments, And-openers, the rare comma splice, capped at one
  looseness move per paragraph) and forbids (typos, txt-speak, forced errors).
  Inferred from the text or artefact when unspecified. Orthogonal to tone.
- **The earned-word rule**: craft.md Principle 7 and the swap test. Big words
  stay only when they carry meaning no plain word does. Mirrored in the linter
  as the advisory `earned-word` category (commence, ascertain, facilitate,
  prior to, in order to, and kin), locked in step with the table in tells.md.
- **Typos never**: an explicit absolute rule across the writing skills and the
  standing principles. Casual is chosen grammar, never manufactured error.
- **The north star**: craft.md now names the target pattern, short paragraphs,
  plain words, sparing fragments, first person, honest about limitations.
- Linter "fix until clean" wording now carves out advisory findings: an
  advisory hit may stand when judged earned, said out loud.

## 0.3.0

Named voices.

- `mimesis-tone`: write or recast prose in one of five human voices, persuasive,
  practitioner, warm, blunt or plain. Composes with the linter, so a tone never
  reintroduces a tell.
- `reference/tones.md`: the five voice profiles. Persuasive, practitioner and warm
  are distilled from dedicated 2026 research; blunt and plain are seeded from the
  craft. Each defines its own AI-slop twin and a tone-specific kill-list.
- `linter`: folded in the high-confidence marketing slop the research surfaced
  (supercharge, revolutionise, world-class, enterprise-grade, best-in-class,
  game-changing, groundbreaking, holistic, visionary, unparalleled, unprecedented,
  synergy, paradigm, propel, unlock) plus dead outreach phrases ("hope this finds
  you well", "I'd love to connect", "at the forefront of").
- `research/`: the three voice research docs kept as provenance.

## 0.2.0

Second domain, machine-facing. mimesis is now two opposite jobs kept cleanly
apart.

- `mimesis-design`: read-only audit of markup, CSS or a described UI against the
  design tells. Reference plus ripgrep, no new dependency.
- `mimesis-compile`: Domain B. Compiles dense, token-efficient instructions for an
  LLM. Bypasses the humanisation linter by design; shares no machinery with
  Domain A.
- `reference/design-tells.md`: AI design fingerprints, each tagged grep or
  judgement.
- `reference/compile.md`: machine-facing instruction guidance, version-keyed to
  GPT-4.1 / GPT-5.x, Claude Opus 4.x and Gemini 3.x, with stale advice flagged.
- `reference/tells.md`: merged the 2026 writing-detection research. Refreshed era
  buckets, added the deep signals that survive humanisation and the false-positive
  guidance.
- `linter`: added `hedging`, plus two length-gated heuristics, `low-burstiness`
  and `low-lexical-diversity`.
- `research/`: the three new research inputs kept as provenance.

## 0.1.0

First release.

- `mimesis-human`: audit, rewrite and generate modes for removing AI tells and
  adding human texture.
- `mimesis-concise`: tighten prose to what does work, preserving every claim.
- `mimesis-principles`: standing auto-load rules so prose comes out clean by
  default.
- `reference/tells.md` and `reference/craft.md`: the L1 guideline corpus, with
  the kill list versioned by model era.
- `linter`: the L2 deterministic pass. Em dashes and their workarounds, smart
  quotes, kill-list words, negative parallelism, participle tails, repeated
  openers. Python 3 stdlib, no dependencies.
- `codex.md`: the optional L3 generator, gated behind `--gen codex`.
