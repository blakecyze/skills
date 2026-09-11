# Character state model

## Reaction contract

| Field | What it decides |
|---|---|
| Trigger | Which product event actually warrants this reaction |
| Pose | The readable silhouette and expression at rest |
| Transition | How the reaction starts without snapping from the current pose |
| Exit | Completion, new input, navigation, cancellation, or replacement |
| Priority | What happens if speech, success, and another event compete |
| Equivalent | Still pose and independent text or status under reduced motion |

An event arriving mid-reaction should transition or replace it deliberately. Do not make the user wait for a queue of old emotions. A neutral recovery pose is better than a permanent error face after the task succeeds.

## Production scale

- **Static set:** ideal for empty states and occasional success artwork. Keep view boxes, optical size, and anchors consistent so swaps do not shift layout.
- **Short authored clips:** useful for a small fixed reaction vocabulary. Supply start/end poses and cancellation behaviour; do not assume arbitrary clips blend correctly.
- **Interactive runtime:** useful for combinatorial input such as gaze, expression, and speech. Separate independent channels where necessary, with explicit precedence at interruptions.
- **Speech-driven character:** map speech data to mouth shapes only with a real timing source. Define neutral mouth on pause, stop, missing audio, and completion. Captions and mute behaviour remain part of the UI.

Choose tooling from the current stack, team capability, and output requirements. File size and runtime cost matter on the actual target device; a small export does not prove cheap rendering.

## Review board

Inspect the poses together at both authoring and product size. Check fixed features, accessory consistency, palette, expression clarity, crop, and contrast with the target background. Include still and failed-asset states. Use cultural review where a metaphor or gesture carries the message; do not claim universality from one reference product.
