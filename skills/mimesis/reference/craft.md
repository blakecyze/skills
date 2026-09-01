# The craft

What to do instead. Distilled from research doc 02. This is L1, read on every
run alongside [tells.md](tells.md).

Removing tells is necessary, not sufficient. You can strip every banned word and
still read as a machine if the rhythm is flat and the stance is absent.
Humanising is additive. Detectors do not only hunt vocabulary; they measure
statistical shape: sentence-length uniformity, word predictability, syntactic
rhythm. The fix is not to write carelessly. It is to put variety, specifics and a
point of view back in.

## Principle 1: Vary the rhythm

Burstiness is the single most effective manual lever. Model prose holds a
near-constant sentence length. Human prose bursts: short declaratives next to
long, clause-heavy sentences that earn their length. Mix simple, compound and
complex shapes deliberately. Break a long rambling line into two punchy ones, or
fuse two stubby ones. Then read it aloud. If the pulse is even, it is not done.

## Principle 2: Earn specifics

Concrete detail is proof of life. Generic abstraction is the texture of
prediction. Names, numbers, times, the specific over the sweeping.

For a writing tool with no lived experience, this inverts into an honest rule:
**prefer concrete nouns and active verbs over prestige abstractions, and ask the
user for specifics rather than inventing them.** "We integrate your stack", not
"we weave a tapestry of solutions". **Never fabricate an anecdote or experience
to pass as human.** A vague claim becomes a specific one by getting a real fact
from the user, not by inventing one.

- Bad: "The culture was a rich tapestry of diverse backgrounds."
- Good: "Half the team had never worked in fintech before, and it showed in the
  questions they asked."

## Principle 3: Affirm, do not negate

The "not X, but Y" reflex is the most recognisable structural tell. Cure it at
the level of the category, not the phrase. Banning a wording leaves the model
free to reach for the next antithesis. Avoiding **thesis-antithesis patterns and
rhetorical equivocation entirely** blocks the statistical pathway and produces
noticeably more direct prose. Keep contrast in the toolbox as a rare, high-impact
move.

## Principle 4: Take a position

Neutrality reads as machine. Perfect balance, courteous hedging and smoothed tone
are tells in their own right. Human writing leans. It emphasises one thing over
another, risks an opinion, and occasionally cuts against the obvious read. Drop
the reflexive "it's understandable that" and the HR-friendly warmth. Asymmetry is
a feature.

## Principle 5: Restraint

Say the claim once. Stop. Cut the throat-clearing first sentence. Cut the dutiful
summary that repeats what you just said. Drop the fake importance ("a pivotal
moment") and the participle tails that fake analysis. Remove everything that is
not doing work, and what remains reads more human, not less.

## Principle 6: Natural connective tissue

Talk, do not transition. Swap the mechanical connectives for the ones people
actually use, or none at all. "Also", "but", "so", or simply start the next
sentence. Use contractions. The aim is the cadence of someone explaining a thing
to a friend, not a report stitched together with "furthermore" and
"consequently".

- Bad: "Furthermore, it is important to note that the results were significant."
- Good: "The results were significant, which surprised us."

## Principle 7: Big words earn their place

Uncommon, Latinate and prestige words are loans, and the interest is reader
trust. A big word is allowed only when it carries meaning no plain word does.
"Ascertain" says nothing "find out" does not, so use "find out". "Idempotent"
says something "repeatable" does not, so keep it. The test: swap in the plain
word. If the sentence loses nothing, the big word was decoration.

This is not dumbing down. Precision sometimes lives in the rare word, and then
the rare word has earned its place. But the default is the word a person would
say out loud.

- Bad: "We commenced the migration subsequent to ascertaining the root cause."
- Good: "We started the migration after we found the root cause."

The linter flags a small earned-word set (commence, ascertain, facilitate,
prior to, in order to, and kin) as advisory. An advisory hit may stand, but
only when the extra meaning is real and you can say what it is.

## The north star

The pattern most human-sounding writing on the web shares, and the target this
corpus aims at:

- Paragraphs of two to four sentences. Skimmable, not walls.
- Plain vocabulary; technical terms only where they carry real meaning.
- Fragments used for emphasis, sparingly. "Two props. That's it."
- First person. The writer built or did the thing and says so.
- Contractions throughout.
- Honest about limitations and what did not work. Honesty about the rough
  edges is proof of life; marketing never volunteers a weakness.

One original exemplar, to hold the shape in mind:

> The whole rig is two props and a phone clamp. Two props. That's it. I'd love
> to tell you there's a clever calibration step, but there isn't, and the
> tracking still drifts if the light changes. It's good enough for rehearsal
> and not good enough for broadcast, and I'm fine with that.

Register (professional or casual grammar) is a separate axis layered on top of
this pattern. See [register.md](register.md). One rule holds in every register:
**never a typo.** Casual means loose grammar chosen on purpose, never a
spelling error.

## The final pass

A silent checklist to run over any draft before it ships. Run it, then send the
cleaner version. Do not narrate the checklist to the user.

1. Cut the first sentence if it is throat-clearing.
2. Replace vague claims with specific ones.
3. Remove fake importance and puffery.
4. Check for repeated sentence shapes and openers.
5. Remove assistant chatter and dutiful sign-offs.
6. Replace bloated verbs with plain ones.
7. Hunt negative parallelism, including across sentence boundaries.
8. Delete rejected-frame and false-range constructions.
9. Cut analogies that do not earn their place.
10. Delete participle tails ("highlighting...", "underscoring...").
11. Strip every em dash. Restructure, do not just swap.
12. Vary sentence length until the pulse is uneven.
13. Cut the ending if it only repeats the point.
14. Ask: does this read as useful, or as overworked?
15. Swap-test every big word: if the plain word loses nothing, use the plain
    word.

## The craft check

The self-grading pass for rewrite and generate modes. It runs after the output
linter pass is clean. Audit mode never grades; it already reports.

Five dimensions, each **pass or fail**. No numbers, ever.

1. **Rhythm.** Sentence lengths genuinely vary; at least one short sentence is
   doing real work.
2. **Earned vocabulary.** Every uncommon or Latinate word survives the swap
   test in Principle 7. If a plain word loses nothing, the big word fails.
3. **Stance.** The text leans somewhere. A reader can tell what the writer
   thinks.
4. **Register fit.** The text matches the requested or inferred register
   ([register.md](register.md)). Casual looseness is occasional, professional
   grammar is complete, and there are zero typos in either.
5. **Specificity.** Claims are concrete, or explicitly marked as needing a real
   fact from the user. Nothing invented.

Pass requires all five. On any fail: one targeted revision of the failing
dimensions only, re-run the linter, re-grade. **Maximum two revision loops**,
then ship the best version and name the shortfall, which is usually
"specificity needs a real number from you".

Report the result as a single line, every time:

```
Craft check: pass.
Craft check: rhythm and specificity revised, now pass.
Craft check: specificity short. Para 2 needs a real figure from you.
```

This is a craft check, not a detector score. It measures whether the writing
does its job, not whether a classifier likes it. It never trades correctness
(spelling, facts, the grammar the register requires) for texture, and it never
optimises against any detector. Chasing a number is the failure mode, which is
why there is no number. See tells.md section 8.

## A warning on shortcuts

Synonym swaps and paraphrasers do not touch the statistical patterns detectors
measure, and recent detectors specifically flag superficially edited AI text. The
honest version of this work changes structure and stance, not just words, and
never invents experience it does not have.
