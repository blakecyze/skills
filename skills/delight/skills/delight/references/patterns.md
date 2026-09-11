# Feedback patterns

Read the section that matches the interaction. These are design heuristics, not fixed duration tokens or promises about retention.

## Quiet craft

For frequently used tools, satisfaction often comes from clear local changes: the edited row settles into place, a saved value remains visible, keyboard focus follows the task. Keep controls discoverable when reducing chrome. Shortcuts complement visible actions.

Distinguish press, pending, success, disabled, and error. A depressed button means input registered; it does not mean the request succeeded. Let the real work determine loading time. Never hold completion for an animation's minimum running time.

## Channels

| Channel | Useful job | Constraint worth checking |
|---|---|---|
| Motion | Connect an action to a changed object or spatial destination | Interrupt cleanly; preserve the final state under reduced motion |
| Particles | Brief emphasis on an infrequent achievement | Keep content legible and controls clickable; remove particles when finished |
| Sound | Confirm an event outside the user's visual focus or support an established sonic identity | Respect available platform and app sound controls; pair with a visible result |
| Haptics | Reinforce a discrete action on supported hardware | Use platform patterns; graceful absence on unsupported devices; verify on hardware |
| Copy | Explain the result or recovery step | Clarity survives without the joke; avoid blame and invented causes |

Prefer one coherent response over a stack of unrelated effects. Avoid screen shake and flashing as defaults in product UI. Frequency, affected screen area, duration, and simultaneous channels all increase the attention cost; particle count alone does not describe intensity.

## Empty, error, first run

- **No data yet:** explain what belongs here and provide the relevant first action. Artwork can disappear without losing the instruction.
- **No search results:** preserve the query and filters; offer a relevant adjustment. Do not show first-run onboarding for an established user's empty search.
- **Finished:** a quiet all-clear may be sufficient. Do not invent another task just to fill the screen.
- **Failure:** state the known problem, preserve useful input, and show the available recovery. If the cause is unknown, say what is known. Serious loss needs a calm tone.
- **First run:** teach through the first useful action. Keep optional tours skippable and repeat visits efficient. Confirm actual progress instead of celebrating permission grants or marketing consent.

## Example: repeated save

For a note editor, retain the text and show saving status while the request runs. Confirm beside the saved object after acknowledgement. If it fails, preserve the draft and offer recovery. A small check can carry the response with sound off and motion reduced. Another edit cancels stale feedback and starts the new pending state.
