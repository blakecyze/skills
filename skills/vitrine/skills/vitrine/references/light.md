# Light, materials, model

For 3D renders and physical shoots. Values are Tested on one device in Blender 5.2 Cycles and judged by eye, so treat them as starting points. `W` is the object's width. Quoted watts assume W = 1.9 m; multiply by (W / 1.9)² for another scene size.

## Contents

- [How light works on a product](#how-light-works-on-a-product)
- [Setups](#setups)
- [Rules](#rules)
- [Materials](#materials)
- [Model faults](#model-faults)
- [Pitfalls](#pitfalls)

## How light works on a product

Light does two jobs: it draws shadows on the ground and reflections on the object. On a shiny object you design what it reflects, not just how bright it is.

A light appears in a surface only at the mirror direction of the camera. To put a highlight on a face, reflect the camera direction about that face's normal and put the light there. A front-facing band mirrors the floor, so only a low card can light it.

Work one surface at a time, with each light separately adjustable. Sourced: [Peter Belanger](https://www.imaging-resource.com/?p=42229). Soft-edged sources stop square lights leaving hard lines in glass. Sourced: [Stash](https://www.stashmedia.tv/futhark-studios-blazes-onto-the-stash-radar-with-nothing-ear-buds-2-spec-spot/).

## Setups

Position is (side, front to back, height) in W from the object, with the camera at negative front to back. Sizes are in W.

| Setup | Says | Lights | Ground |
|---|---|---|---|
| Colour block, hard key | Bold, branded | Key 0.2 at (-1.8, -2.4, 2.6), 620 W, near white. Rim 1.6 at (1, 2.1, 1.3), 120 W | `#E23A00`, roughness 0.75, world same colour at 0.12 |
| Own colour, long shadow | Calm, expensive | Key 0.16 at (-2.4, -1.2, 1.6), 1300 W, warm. Top 2.1, 90 W | `#E7D9C2`, world 0.2 |
| Dark field | Premium, screen alive | Strip 3.7×0.26 behind at (0, 1.8, 1.1), 700 W. Side strip 120 W. Low front card 95 W. All light-linked to the object | `#101114`, roughness 0.42, world 0.02. Screen emission 2.2 |
| Screen as light | Real place, device on | Warm lamp 1.2, 340 W. Warm back strip 120 W | `#3A2A20`, roughness 0.32, world 0.025. Screen emission 2.6 |
| Raking | Crafted, tactile | Low light 0.16 skimming the surface, 420 W | Dark, `#2B2C30`. For macros of grooves and bevels |
| Window / gobo | A moment, a story | Tiny warm light 0.06, 3400 W, through slats | `#E8DCC6`. Once per set; shadows across a screen hurt it |
| Sky wall | Heroic, airy | Sun 0.13, 1800 W. Separate wall wash 900 W | `#8FB6E6`, world 0.45. Pair with a low camera and a wide lens |
| Soft elevation | Precise, product sheet | Soft top 2.6, 240 W. Key 0.8, 280 W | `#AEB4BB`, world 0.22. Straight on |

## Rules

- Light size sets shadow softness; light height sets shadow length.
- Use one clear primary direction, with some areas deliberately under-lit. Sourced: [Will Gibbons](https://www.willgibbons.com/realistic-rendering/).
- Keep ambient low, 0.02 to 0.15 for anything moody. It is the commonest cause of flatness.
- A warm key and cool fill, 500 to 1000 K apart, add richness for free. Sourced, weak.
- Glossy floors mirror your lights. Light-link rim and strip lights to the object, or raise floor roughness.
- Black cards must set `visible_diffuse = False`, or they leave a dark streak on the floor even with shadow rays off.
- Slats near the object give crisp stripes; near the light they blur into bands.
- Don't let a reflection fog a live screen. Keep the glass layer soft or swap in a low-reflection one.

Untested but promising: emission planes with faded edges, Multiple Importance Sampling on reflecting area lights, and Spread for gridded softbox behaviour. For white on white, no light on the sides so edges shade into an outline. Treat unrendered recipes as hypotheses: a blank "reflection softbox" recipe from research made the image worse.

## Materials

| Part | Value that worked |
|---|---|
| Matte shell | Roughness 0.42, coat 0.2, coat roughness 0.25 |
| Frosted gel keys | Roughness 0.4, subsurface 1.0 scale 0.09, coat 0.7 / 0.28 |
| Lit key | Emission 0.3 live, up to 1.8 in macros; too much goes pale under AgX |
| Screen | Black base, emission 1 to 2.6, roughness 0.3; higher in dark sets |
| Floor | Roughness 0.75 matte, 0.3 to 0.45 for a reflection |

AgX Punchy at exposure 0.05 worked throughout but pales bright colours. Compare Khronos PBR Neutral or Standard if a brand colour must be exact; this is forum opinion, not compared here.

For post, crush whites and blacks slightly, keep bloom and grain subtle, and grade before encoding. Skip grain in live frames, since it costs bytes.

## Model faults

Model quality shows at macro, so fix geometry before lighting.

- Booleans plus smooth bevels leave creases around cuts in flat faces. Add a Weighted Normal modifier: `mode = FACE_AREA`, `weight = 100`, `keep_sharp = True`.
- Bevels must survive downscaling: 0.7% of W came to 3 to 4 px in a 960 px frame with the object about half its width. Try 1 to 1.5%. Untested.
- One thin part line and a screw or printed mark give high return per pixel. Sourced: Gibbons.
- Vary roughness slightly; one value flattens surfaces. Sourced.
- Keep a separate object for each moving part from the start, so it can be layered later.

## Pitfalls

| Mistake | Symptom | Fix |
|---|---|---|
| More fill to fix flatness | Greyer and flatter | Remove fill; lower world strength |
| Strong light on a saturated ground | Salmon instead of orange | Deeper base, about 40% of the light |
| Very low f-stop | Macro turns to mush | Raise it; focus on the hero |
| Glossy floor with strips | Blown-out floor | Light-link strips; rougher floor |
| Flags touching the floor | Faint dark streak | `visible_diffuse = False`; lift them |
| Reflections on a live screen | Fogged, unreadable | Reduce or soften glass |
| Mid-distance low angle | Object looks small | Move close with a wide lens |
| Low-resolution screen captures | Soft in macros | Recapture at full resolution |
