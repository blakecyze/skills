# Contributing

mimesis is a reference corpus with a linter attached. The guidelines outrank the model, so most contributions are corpus work, not code.

## Proposing a change

Open an issue first. For a new tell: name it, show two real examples, and say which section of `reference/tells.md` it belongs in. A tell without examples is a hunch.

The kill list and the linter's embedded copy move in lockstep or not at all. A PR that changes one without the other will be asked to finish the job.

## Testing

Run the changed linter on a real piece of your own writing and check the findings are ones you would act on. A rule that flags good prose is worse than no rule. Note that the reference files flag themselves heavily; they catalogue the banned terms as data, and that is expected, not a failure.

## PR expectations

Match the voice of the existing references. UK spelling. No em dashes, obviously. Model-era claims need a date and a source; "everyone knows" is not a citation.

One tell, tone, or rule per PR. Corpus changes and linter changes may share a commit only when they are the same change.
