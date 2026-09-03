# Motion reference

Tier 2 reference for `flow-motion`. Values here are quoted, never paraphrased and never recalled from memory. Adapted from Emil Kowalski's animation philosophy (animations.dev) in Flow's own words.

## Frequency tiers

| Tier | Seen | Motion allowed |
|---|---|---|
| constant | 100+ a day, or keyboard-initiated | None. Ever |
| frequent | Tens a day (hover, list navigation) | Near-imperceptible: fast, subtle, or nothing |
| occasional | Modals, drawers, toasts | Standard |
| rare | Onboarding, first-run, success | Delight budget |

## Tool ladder

Stop at the first rung that fits.

| Need | Tool |
|---|---|
| Hover, press, colour, class-controlled state toggle | CSS transition |
| Entry animation on mount, no JS state | CSS `@starting-style` |
| Predetermined motion that must stay smooth under load | CSS animation (off the main thread) |
| Programmatic control, CSS performance, no library | WAAPI (`element.animate()`) |
| Springs, layout animation, exits, gestures | Motion (motion.dev) |

CSS animations keep running while the main thread is busy; `requestAnimationFrame`-driven motion drops frames during load. Predetermined motion goes to CSS, dynamic and interruptible motion to JS.

## Easing

| Situation | Easing |
|---|---|
| Entering or exiting | `ease-out` |
| Moving or morphing on screen | `ease-in-out` |
| Hover or colour change | `ease` |
| Constant motion (marquee, progress) | `linear` |
| Default when unsure | `ease-out` |

`ease-in` on UI is always FLOW-M2: it delays the exact moment the user is watching. Built-in browser curves are too weak for deliberate motion; use these:

```css
--ease-out: cubic-bezier(0.23, 1, 0.32, 1);      /* strong ease-out for UI */
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);  /* strong in-out for on-screen movement */
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);   /* iOS-like drawer curve */
```

A curve not listed here comes from easing.dev or easings.co, never hand-rolled.

## Duration budgets

| Element | Budget |
|---|---|
| Button press feedback | 100 to 160ms |
| Tooltip, small popover | 125 to 200ms |
| Dropdown, select | 150 to 250ms |
| Modal, drawer | 200 to 500ms |
| Marketing or explanatory | May run longer |

UI motion stays under 300ms. Anything over budget is FLOW-M3 unless the reason is stated in the finding or a comment.

## Springs

Use a spring when the motion is a gesture the user can interrupt or reverse, drag with momentum, or an element that should feel alive.

```js
{ type: "spring", duration: 0.5, bounce: 0.2 }             // perceptual: easier to reason about
{ type: "spring", mass: 1, stiffness: 100, damping: 10 }   // physical: more control
```

Bounce stays between 0.1 and 0.3, and most UI wants none; reserve bounce for drag-to-dismiss and playful moments.

## Properties

- `transform` and `opacity` only; they skip layout and paint. `width`, `height`, `margin`, `padding`, `top`, `left` trigger all three: FLOW-M6.
- `height` is tolerated for accordions, where no transform equivalent exists.
- Entrances start at `scale(0.9)` to `scale(0.97)` plus `opacity: 0`. `scale(0)` is FLOW-M4: nothing real appears from nothing.
- Trigger-anchored surfaces (popover, dropdown, menu, tooltip) set `transform-origin` at the trigger. Modals stay centred.
- Percentages in `translate()` are relative to the element's own size; prefer them over hardcoded pixels.
- In Motion, write the full transform string. The `x`/`y`/`scale` shorthands are not hardware-accelerated and drop frames under load.
- Never drive child transforms from a CSS variable set on the parent; it recalculates styles for every child.

## Choreography

- Groups enter with a 30 to 80ms stagger, not all at once.
- Deliberate phases run slow, system responses snap: a hold-to-confirm holds for around 2s linear, the release answers in about 200ms ease-out.
- Exits mirror entrances. A toast that slides in from the bottom leaves through the bottom.

## Gates

Both ship with the animation, every time.

```css
@media (prefers-reduced-motion: reduce) {
  .element { animation: fade 0.2s ease; } /* keep opacity and colour, drop movement */
}

@media (hover: hover) and (pointer: fine) {
  .element:hover { transform: scale(1.05); } /* touch fires false hovers on tap */
}
```

```jsx
const reduce = useReducedMotion();
const closedX = reduce ? 0 : '-100%';
```

Reduced motion means fewer and gentler animations, not zero. Keep the transitions that aid comprehension; remove the movement.
