# Interface copy

Loaded for `flow-copy`, the only Flow skill allowed to change strings. Craft substance adapted from jakub.kr/skills (better-writing) in Flow's words.

## Buttons

- Start with the verb that names the action: "Send", "Save draft", "Delete project".
- Consequential confirmations repeat the consequence: "Delete project", never a bare "Yes".
- No exclamation marks, no "Let's go!", no "OK!".

## Errors

- Say how to fix it, next to the field that failed.
- Positive phrasing: "Use only letters", not "Don't use numbers".
- No blame, no drama, no exclamation marks. "Unable to load" beats "We couldn't load".

## Empty states

Three jobs in one short block: what this space is for, how to fill it, one clear action. "No results" does none of them. "No projects yet. Projects keep your tasks and files together. [Create a project]" does all three.

## Labels and links

- Links describe their destination and survive being read out of context: "Learn more about exports", never "Click here".
- Toggles are labelled for the ON state: "Send read receipts", not "Don't send read receipts".
- Placeholders show format only (`name@example.com`) and never replace a visible label; the label check belongs to `flow-access`.

## Consistency

- One capitalisation policy per element type, applied everywhere. Sentence case is the safer default.
- One term per concept across the product: "Archive" everywhere, not "Move to storage" in one corner.
- "You" in instructions; no "we" in errors.

## Tone by context

| Context | Tone |
|---|---|
| Success, onboarding | Warm, light |
| Routine actions | Neutral, minimal |
| Errors, destructive actions | Calm, plain, zero playfulness |
| Data loss, security | Serious, explicit |

Delight lives where kanso and Flow both put it: in rare moments, never in error paths.
