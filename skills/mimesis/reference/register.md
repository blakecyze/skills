# The register

Professional or casual: how buttoned-up the grammar is. This is L1, read by
`mimesis-human` and `mimesis-tone` whenever a register is specified or worth
inferring.

Register is not tone. Tone is *which* human voice ([tones.md](tones.md));
register is how relaxed that voice's grammar gets. The two compose freely: a
warm-professional support reply, a warm-casual community post, a
practitioner-casual blog post, a blunt-professional decision memo. Every tone
takes either register.

## The flag

```
--register professional|casual
```

Accepted by `/mimesis-human` and `/mimesis-tone`, in rewrite and generate modes.

## Defaults when unspecified

Register is an adjustment, never a blocker. Do not stop to ask for it.

- **Rewrite:** preserve the register of the input. Do not formalise a casual
  note, do not loosen a formal one.
- **Generate:** infer from the artefact. Documentation, a case study, outreach to
  a stranger: professional. A personal blog post, a community reply, a message to
  a colleague: casual. Ambiguous: professional.

## Professional

Complete sentences, standard grammar and punctuation throughout. Contractions
stay (craft.md Principle 6 applies in every register); professional means
grammatical, not stiff. Everything else in the corpus still holds: varied
rhythm, plain words, a stance.

## Casual

Casual permits small, endearing grammatical looseness. Each move is occasional
and chosen, never mandatory:

- A sentence fragment for emphasis. "Two props. That's it."
- Starting a sentence with And, But or So.
- Contractions throughout.
- The rare comma splice, when the two clauses genuinely run together.
- A lowercase aside in parentheses (like this one, sort of).
- Ending on a preposition.

**The frequency cap.** This is the anti-tell. Looseness must read as a writer
relaxing, not a machine performing relaxation. At most one looseness move per
paragraph, and zero is fine. Uniform looseness is its own tell, exactly like
uniform formality.

## What casual forbids

- **Never a typo.** No misspellings, no dropped apostrophes, no forced errors of
  any kind. A deliberate typo is the cheapest and most detectable humanisation
  trick, and it costs the reader's trust the moment it is spotted. Casual is
  loose grammar chosen on purpose, never a spelling error.
- No txt-speak: "u", "ur", "gonna" (unless quoting someone who said it).
- No slang the source text or the user has not already used.

## The north star

The reference point sits between the two registers: casual-leaning professional.
See "The north star" in [craft.md](craft.md) for the pattern. Short paragraphs,
plain words, the odd fragment, first person, honest about limitations. Most
writing that needs to sound human lands near there.
