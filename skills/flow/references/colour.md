# Colour

Loaded for FLOW-05, FLOW-06, FLOW-09. Gestalt: figure and ground (05) and similarity (09).

## The two-bucket rule

Every colour in an interface belongs to exactly one bucket.

**Neutral.** Carries structure: surfaces, text, borders, dividers, disabled states. Does the overwhelming majority of the work. Most well-made interfaces are 90% neutral.

**Semantic.** Carries meaning: primary action, success, warning, danger, informational. Reserved. A semantic colour appearing decoratively is FLOW-09, because it teaches users that the colour means nothing.

There is no third bucket. "Brand colour used as a background wash because the section felt empty" is decoration wearing a semantic colour's clothes.

## The neutral ramp

Eight to ten steps from white to near-black. Steps must be perceptually even, which is why the ramp is authored in a perceptual space (OKLCH or LCH) and exported to hex, not picked by eye in HSL.

A usable default assignment:

| Step | Role |
|---|---|
| 0 | page background |
| 1 | raised surface |
| 2 | subtle fill, hover on surface |
| 3 | borders, dividers |
| 4 | disabled text, placeholders |
| 5 | secondary text |
| 6 | body text |
| 7 | headings, high emphasis |

Pure `#000` for text is rarely right on a white background; it vibrates. Pure `#FFF` text on a dark background is usually fine. Dark themes are not inverted light themes: elevation goes lighter rather than darker, and saturated colours need reducing to avoid glare.

## Contrast

Non-negotiable, and always computed by `scripts/contrast.py`, never estimated.

| Content | Minimum |
|---|---|
| Body text | 4.5:1 |
| Text 18pt+ or 14pt bold | 3:1 |
| Icons and interface boundaries | 3:1 |
| Focus indicators | 3:1 against both the component and its background |
| Disabled elements | exempt, but must still read as disabled |

A contrast failure is always Tier 1. It is not a polish item and it is not a trade-off against aesthetics.

## Emphasis levels

Define exactly three and stop.

1. **Primary.** Filled, semantic colour. **One per view.** Two is FLOW-06.
2. **Secondary.** Outlined or subtle-filled, neutral.
3. **Tertiary.** Text only, no container.

Destructive actions are their own case: styled with the danger colour, but still secondary in weight unless deletion genuinely is the primary purpose of the screen.

## Colour is never the only signal

Anything communicated by colour is also communicated by shape, icon, text, or position. Error states get an icon and a message, not just a red border. This is an accessibility requirement and it also survives greyscale, low-quality screens, and sunlight.

## Elevation

Pick one elevation device and use it consistently: shadow, border, or background shift. Using all three on one card is FLOW-05.

Shadows should be soft, low-opacity, and vertically offset, because light comes from above. A shadow with no offset reads as a glow. Two elevation levels are usually enough for an app; more than three means the layering model is confused.

## Common failures

- The brand colour used for a heading, then again for the submit button, so neither reads as the action (FLOW-09)
- A card with a border, a shadow, and a tinted background all doing the same job (FLOW-05)
- Grey text on a grey background at 3.1:1 because it "looked softer"
- Twelve one-off hex values that are all almost the same grey
- A dark theme built by inverting the light ramp, with saturated accents left untouched
