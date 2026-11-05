---
name: vitrine
description: "Use when images present work and feel plain, samey, or forgettable, or the user wants to showcase something better: product shots, thumbnails, feed or project cards, heroes, Open Graph images, app store screens, portfolio grids, snippet previews. Also for \"audit our thumbnails\", \"art-direct this\", \"what should this shot be\", or choosing grounds, crops, angles, or lighting. Not for refining the surrounding interface or finding references."
argument-hint: "[scope] [review|direct|apply] [focus]"
---

# Vitrine

Show each thing so it reads at a glance and earns a second look.

## Controls

`[scope] [review|direct|apply] [focus]`

All optional. An audit or "why is this plain" is `review` and stays read-only. `direct` plans shots and shows options as images. `apply` changes only the places the user names; a shot approved for a thumbnail has not been approved for a project page, so ask before anywhere else. Focus such as `colour`, `crop`, or `set` narrows the pass.

## Principles

- A shot is four decisions: **angle, crop, ground, light**. Neighbours change at least two. Give the whole set one new ground and you have a new sameness, so vary them within a palette of three to five grounds.
- Start from one sentence the shot must say. "These keys look soft and pressable" gets a macro; "it's a nice product" gets another centred three-quarter.
- Value before colour. If the outline melts into the ground, no hue will save it.
- Decide the crop first. Let things run off the frame.
- One loud colour per frame. An accent appearing twice ties object to ground.
- Remove light before adding it. Fill flattens; shape comes from what stays dark.
- Art direction beats engineering. Excellent prerenders on a ground chosen for that object, with a moment of motion that answers the visitor, beat live 3D.
- Judge at the size and on the page where it ships. A difference visible at 1600 px can vanish on a 300 px card.

## Review

1. Get the images as people meet them: display order, ship width, ratio, page, themes. Prefer a screenshot of the real page.
2. Run `python3 <skill>/scripts/vitrine.py <images in display order> --sheet <temp>/sheet.png --size <ship width>`, with `<skill>` resolved from this file's folder. Keep the sheet out of the repo. Its error says how to get Pillow into a temporary environment; if that fails too, label findings unmeasured.
3. Open the sheet and judge from it. Check the set first, then each image against the failures below. `jump` is the L\* step at the object's outline, `fill` the share of the frame its box covers, and `edges` the sides it reaches. Shadows and floor lines inflate the last two, so treat all of these as leads and confirm each by eye.

| Failure | Looks like | Fix |
|---|---|---|
| Samey | Neighbours share angle, crop, ground, and light | Change at least two per neighbour |
| Too much | Everything competes | Remove elements; one loud colour |
| Too little | Nothing to look at | Add a detail, a shadow, or a crop |
| Boxed | Whole object or window shrunk into a frame | Crop in; run off the edge |
| Flat | Everything has the same weight | Add value contrast and a focal point |
| Bland | Competent, forgettable | Change the ground or the angle |

Return, in this order:

1. **Verdict:** the set's main problem, in one sentence, with its measurement.
2. **Shots:** a row per image with `says`, `angle`, `crop`, `ground`, `light`, and `failure`, or `keep`.
3. **Changes:** the few with most value, each naming the image and what becomes of its angle, crop, ground as a hex value, light, or place in the order. Each should differ from its neighbours.
4. **Leave alone:** what already works.
5. **Unverified:** what was judged by eye, and whether it was seen on the real page in both themes.

A strong set gets a short review. Findings need not be manufactured.

## Direct

Pick the message, then a shot family, ground, and light. Show 8 to 12 different setups as a low-quality sheet, never four variations on one idea. Say which are worse and reshoot the misses with one specific fix each. The user chooses from images, not descriptions. Then finish at full quality, encode, and check at real size in both themes against the project's budgets.

## Apply

Read the project's rules first. Change the named places only, using its existing image pipeline. Inspect the result on the real page at ship size in both themes, and report what changed.

## References

Load only what the proposed changes need; a review of web cards starts with `surfaces.md`.

| Work | Reference |
|---|---|
| Angles, lenses, crops, depth of field | [frame.md](references/frame.md) |
| Grounds and colour strategy | [colour.md](references/colour.md) |
| Lighting, materials, 3D model faults | [light.md](references/light.md) |
| Websites, apps, snippets, motion, live layers, marketing kits | [surfaces.md](references/surfaces.md) |

This is craft practice with no engagement or A/B evidence behind it. Say so if asked to promise results.
