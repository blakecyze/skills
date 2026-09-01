# The tells

A diagnostic catalogue of the fingerprints that mark text as machine-written.
Distilled from research doc 01. This is L1: the skill reads it on every run. It
outranks the model.

No single item here proves a machine wrote something. Each one nudges the
probability. Detectors lean on two measures: **perplexity** (how predictable the
next word is) and **burstiness** (how much sentence length varies). Human prose
scores high on both. Model prose scores low on both, and leans on a narrow set of
habits a trained eye spots in seconds.

Items tagged **[linter]** are caught deterministically by the L2 pass. Items
tagged **[judgement]** read as machine even when grammatically fine, so they need
the model to weigh them in context. Both get flagged. Neither gets waved through.

## 1. Lexical tells: the kill list

The most studied signal. A small set of words spiking in frequency since late
2022. "Delve" is the reddest flag of all. **[linter]** flags every term below by
word boundary, case-insensitive, inflections included.

**Inflated verbs.** delve, leverage, utilise, harness, streamline, underscore,
foster, elevate, surpass, unlock, embark, emphasise, showcase, bolster, enhance.

**Prestige nouns and borrowed-grandeur metaphors.** tapestry, landscape, realm,
mosaic, ecosystem, symphony, beacon, cornerstone, bedrock, testament, odyssey,
kaleidoscope, interplay.

**Inflated adjectives.** pivotal, robust, seamless, cutting-edge, multifaceted,
vibrant, bustling, meticulous, crucial, paramount, unwavering, transformative,
revolutionary, intricate.

**Formulaic transitions.** furthermore, moreover, consequently, notably,
importantly, additionally.

**Stock phrases.** in today's ever-evolving world, it's important to note, when
it comes to, in the realm of, at the heart of, in conclusion, in essence, align
with.

**Assistant chatter.** Certainly, Great question, I hope this helps, Let's dive
in, Remember that.

The fix is never a synonym swap. Reach for the plain word a person would use, or
cut the sentence. "We integrate your stack", not "we weave a tapestry of
solutions".

**The earned-word set. [linter, advisory].** Latinate formality that a plain
word almost always beats. Not slop in the kill-list sense, so it is flagged as
advisory polish: an occurrence may stand, but only when the big word carries
meaning the plain one does not, and you say what that meaning is (see craft.md
Principle 7, the swap test).

| flagged | plain word |
|---|---|
| commence, commencement | start |
| endeavour / endeavor | try |
| ascertain | find out |
| facilitate | help |
| necessitate | require |
| subsequently | then, later |
| aforementioned | that, this |
| utilisation / utilization | use |
| prior to | before |
| in order to | to |
| in the event that | if |
| with regard(s) to | about |
| numerous | many |

The linter also flags a marketing-register set the research surfaced (world-class,
enterprise-grade, supercharge, synergy, game-changing, unprecedented and kin, plus
dead outreach phrases like "hope this finds you well"). Register-specific
kill-lists, for persuasive, practitioner and warm writing, live in
[tones.md](tones.md), since what counts as slop shifts with the voice.

## 2. Model-era drift

The kill list is not eternal. Each generation sheds some habits and grows new
ones, so this list is **versioned, not fixed**. Revisit it as models drift, and
keep the linter's embedded copy in step with this file. The same lockstep rule
covers the earned-word set in section 1: the table there and the linter's
`_EARNED` list change together or not at all.

- **GPT-4 era.** delve, tapestry, testament, meticulous, pivotal, underscore,
  vibrant, intricate.
- **GPT-4o era.** align with, bolstered, enhance, fostering, highlighting,
  showcasing, underscore.
- **GPT-5.x era.** emphasising, enhance, highlighting, showcasing, plus semicolon
  overuse and undue "notability" framing. The defining structural tell is
  **length normalisation**: outputs cluster at a characteristic length for a
  prompt rather than tracking the actual information need. As of 2026, GPT-5.5 is
  detected mostly by this length confound, and reads as topically complete but
  semantically thin, covering the territory without the selective emphasis of a
  writer with a stake in the question.
- **Claude Opus 4.x era.** Carries a genuine stylistic fingerprint independent of
  length, one that survives heavy human editing. Watch for **contextually
  inappropriate hedging**: hedge-to-booster ratios above human norms, hedging
  where a person would simply assert and confidence where a person would qualify.
  Also explicit reasoning traces leaking into ordinary prose ("This is a complex
  question requiring...") and the polished, hedged, marketing-shaped default
  voice the model falls back to when the context is underspecified.
- **Gemini 3.x era.** Outputs carry SynthID-Text watermarking, a statistical
  provenance signal absent from Anthropic and OpenAI text. It is not visible to a
  reader and degrades under paraphrasing, so it is a provenance fact rather than a
  prose tell.

When you flag a term, knowing its era is useful context, not a reason to spare a
current one. The linter flags the union of all eras.

## 3. Syntactic and rhetorical tells

Harder to grep than words, and often the stronger signal. These are sentence
shapes, not vocabulary.

**Negative parallelism (the antithesis tic). [linter] + [judgement].** Negate a
familiar idea, then replace it with something grander. "It's not just a
dashboard, it's a command centre." "It's less about efficiency and more about
transformation." The single most recognised structural tell after the em dash.
The linter catches the common wordings; the model catches the rest, including the
ones spread across two sentences. Cure it at the level of the category, not the
phrase: state what the thing is, directly. Keep contrast as a rare, high-impact
move, not a reflex.

**The rule of three (tricolon). [judgement].** Three parallel items, almost
always equal in length and punctuation, reached for when there is nothing
specific to say. "Speed, efficiency and innovation." Humans use the tricolon
too, so the flattened, content-free version is the tell. Try two items, or four,
or the one that matters.

**The participle trap. [linter].** An "-ing" phrase bolted to a sentence to fake
analysis. "Highlighting its importance. Underscoring its significance.
Contributing to the broader picture." Nobody is doing the highlighting. If the
point matters, give it a full sentence with a real claim.

**False ranges and puffery. [judgement].**

- False range: "from ancient traditions to modern innovations." Sounds sweeping,
  names nothing. If you cannot name the meaningful middle, the range is fake.
- Puffery: "a pivotal moment", "a seismic shift". State what happened and let the
  reader judge the size.
- Weasel attribution: "has been described as...", opinions credited to no one.

## 4. Punctuation tells

**The em dash. [linter]. The headline tell.** GPT-3.5 barely used it; GPT-4o used
roughly ten times more, and later models pushed further. The mark is centuries
old and beloved by careful writers, which is why the backlash also produces false
accusations. For this project the verdict is absolute: **zero em dashes, no
exceptions.** The linter also catches the workarounds: en dash used as a clause
break, the double hyphen, and the spaced hyphen. Numeric ranges keep their en
dash. Restructure into commas, full stops or parentheses. Restructure, do not
swap.

**Lesser punctuation signals.**

- Curly "smart" quotes and apostrophes where a person typing fast would leave
  straight ones. **[linter].**
- Semicolon overuse, the newer GPT-5 era habit. **[judgement].**
- Flawless, evenly distributed commas with no improvised punctuation anywhere.
  **[judgement].**

## 5. Structural tells [judgement]

The scaffolding survives even when the wording is edited, which is why it is such
a durable signal.

- **Intro, point, point, point, conclusion.** The five-beat template that fits
  any topic and therefore fits none.
- **Paragraph uniformity.** Every paragraph follows the same internal recipe.
  Nothing is wrong with any one of them, then it repeats five times.
- **The dutiful closing line.** A summary the reader did not need. Humans stop
  once the point lands.
- **Metronomic rhythm. [linter, heuristic].** A 14 to 22 word median with little
  variance. Read it aloud and you hear a steady, machine-like pulse. The linter
  flags low sentence-length variance on texts of six or more sentences as
  `low-burstiness`, advisory only, since constrained genres are naturally even.
- **Low lexical diversity. [linter, heuristic].** AI prose reuses a narrower
  vocabulary, by some measures roughly a quarter of the unique words a person
  would use per passage. The linter flags a low type-token ratio on texts of a
  hundred words or more as `low-lexical-diversity`, advisory only.
- **Repeated openers. [linter].** "This study shows...", "It is crucial to..."
  starting sentence after sentence.

## 6. Tonal tells [judgement]

- **Relentless courtesy and neutrality.** A friendliness no adult uses unless
  they work in HR or support.
- **Reflexive hedging. [linter, phrases].** Confidence drained out by habit:
  "it's worth noting", "it's important to", "arguably", "generally speaking", "in
  many cases", "it could be argued". The linter catches the set phrases; the
  deeper tell is hedging where a person would assert and asserting where a person
  would hedge.
- **Smoothed emotional tone.** No edges, no asymmetry, nothing risked.
- **Fake intimacy.** "Here's the thing." "Here's an uncomfortable truth."
  Pretending to level with you.
- **Empty intensifiers.** "Genuinely", "truly", "actually" used to sound sincere
  while intensifying nothing.
- **Emoji-bulleted social posts** with a titled intro, the classic LinkedIn
  giveaway.

## 7. Signals that survive humanisation [judgement]

The deepest 2026 detectors do not read vocabulary at all, and surface edits do
not touch them. None is regexable, so they live here as judgement guidance, not
in the linter. They matter because they tell you what humanising must actually
change: structure and stance, not words.

- **Discourse-level coherence.** AI text connects each sentence to its neighbours
  in low-variance, predictable ways. Human writing drifts, retrieves an
  antecedent from three paragraphs back, and argues non-linearly. A sentence-level
  rewrite cannot rebuild macro-structure, which is why it survives paraphrasing.
- **Surprisal variance (burstiness, done properly).** The real signal is not
  average predictability but how much it fluctuates. Human writing spikes and
  dips: tangents, asides, a sudden short sentence. AI holds surprisal in a narrow
  band. This is the rigorous version of "vary the rhythm".
- **Frontier-LLM stylistic signature.** Frontier models share a latent style that
  human text does not occupy. A humaniser that is itself an LLM just swaps one
  model's signature for another's and stays in the same region. This is why
  running AI text through another AI does not make it human.
- **Embedding geometry and trigram cadence.** Intrinsic dimensionality of the
  text manifold and character-trigram cohesion both separate human from machine
  and both resist synonym swaps. You cannot edit your way out of them at the word
  level; you change them only by genuinely restructuring.

The practical reading for a human analyst without these tools: ask whether the
text has the selective emphasis and argument topology of someone with a specific
stake in the question. That is the thing the tells lack and the thing
[craft.md](craft.md) tries to put back.

## 8. False positives, and why this skill does not chase a score

Every detector trades precision against recall, and the cost lands on specific
human writers. Documented, repeatedly:

- **Non-native English writers.** Over 61% of TOEFL essays by non-native students
  were flagged as AI in one foundational study, because lower lexical diversity
  and simpler syntax score the same way AI does.
- **Neurodivergent writers.** ADHD, autistic and dyslexic writers are flagged
  more often, for the repeated phrasing and formulaic structure that lower
  cognitive load.
- **Formally trained and heavily edited writers.** Clean academic structure,
  grammar-checked prose and predictable essay shape read as AI to a detector.
  Tools have flagged the US Constitution and the Bible.

So the goal is never to beat a given detector. Chasing a score punishes exactly
these writers and rewards nothing. The honest aim is signal, specificity and a
point of view.

## Read this before trusting any of it

These are probabilities, not proof. Detectors produce false positives, and
skilled writers use em dashes, tricolons and antithesis on purpose. People have
been wrongly accused over a single dash.

The goal is not to defeat a detector. It is to write with signal, specificity and
a point of view, which happens to be what the tells lack. Gaming a score by
swapping synonyms changes nothing the detectors measure. Structure and stance are
what move the needle. See [craft.md](craft.md) for what to do instead.
