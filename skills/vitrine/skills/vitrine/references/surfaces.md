# Websites, apps, snippets, motion

Labels: **Measured** from assets or the browser. **Sourced** from a practitioner. **Observed** read from pages. **Judgement** opinion.

## Contents

- [Websites and apps](#websites-and-apps)
- [Snippets and components](#snippets-and-components)
- [Motion](#motion)
- [A shot as a live element](#a-shot-as-a-live-element)
- [Marketing kit](#marketing-kit)

## Websites and apps

- Keep a current, nearly flat device constant and change the surface per project. Observed: [Metalab](https://www.metalab.com/work), [Instrument](https://www.instrument.com/work).
- Choose the surface from the product. Observed, as with the sand and pebble surfaces those studios use.
- Fixed ratios vary by site: 1:1 Instrument, 4:5 Basic, 3:2 Pentagram, 4:3 Awwwards. Mixed native ratios in masonry also work. Observed.
- Mix in non-device cards, such as a logo on colour, to break repetition. Observed: Instrument.
- Poster plus video is the norm. No page read ships a scaled live iframe of a project in a grid, so live embeds are a real differentiator. Observed.
- A shared bezel PNG layered over video is cheap. Observed.
- Wrong chrome reads as fake: an address bar on a native Mac app, a fake iOS status bar. Sourced: [Stageshow](https://benji.org/stageshow).
- Dated tells: stock plinth scenes, purple gradients, isometric scenes, overlapping device fans. Mostly one vendor blog.
- A reasonable tiering is art-directed posters for most projects, live embeds for snippets, and a hero 3D device for one or two. Judgement.

## Snippets and components

Six framing families, Observed:

1. Wall of loops ([Rauno Craft](https://rauno.me/craft))
2. Editorial inline stage (Emil Kowalski, Josh Comeau)
3. Docked instrument beside prose (Devouring Details)
4. Library preview with code tabs (Magic UI, Motion Primitives, shadcn/ui)
5. Gallery index of posters (Aceternity, Codrops, Origin)
6. Marketing stage (Cursor's painted backdrop, Family's bento tiles)

Rauno Craft, Measured: three columns about 325 px wide, 12 px radius, 68 muted loops, no iframes on the index, heights 106 to 329 px, each card with its own ground, title inside the media, and a typed action such as "View Prototype".

- Give each demo its own ground from a small palette. Adding a dot grid to every card swaps one uniform for another. Judgement.
- Crop tighter than fitting it in. Sourced: Stageshow.
- Vary heights; in bento, only a third to a half of tiles should show UI. Sourced: Stageshow.
- Typed actions beat one identical hover button, which also says nothing on touch. Observed.
- Put the caption inside the piece. Observed.
- No data was found on autoplay versus hover or on code reveal.

## Motion

Apple's current AirPods Pro and MacBook Air pages use short 30 fps prerendered clips with `preload="none"`, triggered by scroll keyframes and ending on a matching still, not the 2019 scroll flipbook. Their stylesheets have no `perspective`, `preserve-3d`, `animation-timeline`, or `view-transition`. Measured from entry bundles only.

| Use | Avoid |
|---|---|
| Real controls laid over a prerender | Scroll-scrubbed flipbooks in a feed |
| One-shot reveal on first entry, ending on the rest pose | Hover-scrubbed video |
| View transition into the project page | Foil and holographic gimmicks |
| Slow settle back to rest, about 500 to 600 ms | Auto-rotate |

- Springs: Apple's most common is stiffness 100, damping 20, with common durations of 0.3 s and 0.5 s. Bounce is rare. Measured.
- Novelty: about 90% familiar, 10% novel. Sourced: [Rauno](https://rauno.me/craft/novelty).
- The more often something is seen, the less it should animate. Sourced: Emil Kowalski.
- Loop ends match their starts exactly, and every change has a visible cause. Sourced: Stageshow.
- Tilt isn't required. A single gorgeous pose with working controls beat a 57-pose tilt grid at a fraction of the bytes, in one project.

## A shot as a live element

One prerendered pose split into layers, with real controls over it. Used on one project card.

**Layers** (Cycles, film transparent, floor as an opaque mesh):

- `case`: body and ground, screen as a holdout hole, keys hidden from camera but casting shadows
- `keys`: all keys at rest, everything else held out
- `lit1..n`: each lit key alone, in its own border-cropped box
- `knob`: the moving part, everything else held out
- `glass`: the screen's reflections with emission off, softened about 40% so it never fogs the live screen
- `poster`: the full shot, for first paint and phones

Keep the floor in every layer as a holdout, because it bounces colour onto keys and knob.

**Runtime:** a 2D canvas redraws only on change, the live screen canvas is warped into its corners with `matrix3d`, and real `<button>` and `<input type="range">` controls sit over their renders.

**Performance:** a real `<img>` poster so LCP has an element, nothing streamed after load, one `fetchpriority="high"` per page, hashed frames, and a check against the route's budget. Match the frame to its card so nothing jumps: same aspect, pose, and background colour.

## Marketing kit

Six shots per product, once a scene exists. Add a colourways shot if the product has a range.

| Shot | Use |
|---|---|
| Signature hero, strong colour | Feed poster, Open Graph, launch post |
| Calm three-quarter | Project page header |
| Detail macro | "How it's made", thread images |
| Second detail | Next to feature copy |
| Dark, screen on | Contrast within a page, dark-mode hero |
| Graphic square | Social, avatars, grids |
