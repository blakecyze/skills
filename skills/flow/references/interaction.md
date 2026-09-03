# Interaction and states

Loaded for FLOW-11 and any Tier 1 accessibility finding.

## The state matrix

Every interactive element needs a defined treatment for each state it can occupy. Missing focus or disabled is Tier 1. Missing hover on a desktop target is Tier 2.

| State | Requirement |
|---|---|
| Default | the resting treatment |
| Hover | pointer devices only, never the only affordance |
| Focus-visible | **mandatory.** Visible ring, 3:1 contrast, at least 2px, offset from the element |
| Active / pressed | immediate visual response, under 100ms |
| Disabled | visually distinct, not merely faded to illegibility, and explains why where possible |
| Loading | in-place, preserving layout, not a full-screen spinner |
| Error | what happened and what to do, adjacent to the cause |

## Never remove the focus ring

`outline: none` without a replacement is the single most common accessibility failure in web interfaces. If the default ring is ugly, replace it. Do not delete it.

Use `:focus-visible` rather than `:focus` so pointer users do not see rings on click while keyboard users still do.

## Targets

| Platform | Minimum |
|---|---|
| iOS | 44 x 44pt |
| Android and Material | 48 x 48dp |
| Web, touch | 44 x 44px |
| Web, pointer only | 24 x 24px, with adequate spacing |

The *target* can exceed the *visual* size. A 24px icon with 10px of transparent padding meets a 44px target without looking heavy. This is the correct fix for a cramped icon row, not enlarging the icon.

Adjacent targets need at least 8px between their hit areas, more for destructive actions sitting next to routine ones.

## Empty, loading, and error states

These are the three screens users see when something goes wrong, and they are almost always the last thing designed. FLOW-11 exists mostly because of them.

**Empty.** An invitation, not an apology. Say what goes here and give the action that puts something here. A grey illustration and the word "Nothing" helps nobody.

**Loading.** Preserve layout. Skeletons that match the eventual content shape prevent the reflow jump. Below roughly 300ms, show nothing at all; a flashed spinner reads as a glitch.

**Error.** What failed, and what to do next. In the interface's voice, not a person's. No apologies, no exclamation marks, no stack traces. If a retry is possible, offer the retry in the message.

## Motion

Motion that answers a user action is welcome. Motion that plays on its own is a cost.

| Purpose | Duration |
|---|---|
| Micro feedback (hover, press) | 100 to 150ms |
| Transitions (expand, reveal) | 200 to 300ms |
| Page or route changes | 300 to 400ms |

Ease-out for entrances, ease-in for exits, ease-in-out for movement between two on-screen positions. Linear only for continuous indicators.

Respect `prefers-reduced-motion`. Reduced does not mean removed: replace movement with a cross-fade rather than cutting feedback entirely.

## Common failures

- Focus removed globally in a reset stylesheet, never restored
- Disabled buttons at 30% opacity, failing contrast and giving no reason
- A hover-only affordance, invisible on touch
- Full-page spinners that discard scroll position and layout
- An error toast that vanishes before it can be read, with no way to recall it
- Animation on every card entrance, which reads as generated rather than designed

## The little things

Craft details for `flow-access`. Substance adapted from jakub.kr/skills (better-accessibility).

- **Native first.** `<button>` for actions, `<a href>` for navigation; a `<div onClick>` is a Tier 1 finding. No ARIA beats bad ARIA.
- **Focus.** `:focus-visible` with at least a 2px solid perimeter, checked against every adjacent colour and forced-colors mode. An outline removed without a verified replacement is Tier 1.
- **Keyboard parity.** Every pointer interaction has a keyboard path. `tabindex` is 0 or -1, nothing else; composite widgets rove.
- **Targets.** 24px square minimum, 44px touch and 40px desktop preferred; extend with pseudo-elements; decorative overlays get `pointer-events: none`.
- **Forms.** Every input has a `<label for>`; placeholders are not labels. `autocomplete`, `name`, `type`, and `inputmode` set; paste never blocked; validate on submit and mark failures `aria-invalid="true"` with `aria-describedby` pointing at the message; submit stays enabled until the request starts.
- **Announcements.** `role="status"` for polite updates, `role="alert"` for urgent errors only, and the live region exists before the update lands.
- **Not colour alone.** Every status carries a second cue: icon, text, weight.
- **Structure.** One `<h1>`, properly nested headings, one `<main>`, skip-link first when navigation is long. 200% zoom and 320px width without horizontal scroll.
- **Media and motion.** Autoplay gets a visible pause; movement respects `prefers-reduced-motion` (see `motion.md`). Alt text names the purpose: "Search", not "magnifying glass".
