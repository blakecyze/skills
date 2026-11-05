# Vitrine

A vitrine is the glass case something sits in to be looked at. This one audits and art-directs how work gets shown: product shots, thumbnails, feed cards, heroes, and snippet previews. It finds why a set feels plain, then says exactly what to change.

## Install

```bash
npx skills@latest add blakecyze/skills --skill vitrine
```

For a local clone, replace `blakecyze/skills` with `.` from the repository root. Claude Code can use `/plugin marketplace add blakecyze/skills` followed by `/plugin install vitrine@cyze`.

## Use

```text
$vitrine review the project cards
$vitrine direct a launch image for the keyboard
$vitrine apply the feed thumbnails ground
```

The skill accepts optional scope, `review`, `direct`, or `apply`, and focus. A review stays read-only. Direct plans shots and shows options as images. Apply changes only the places you name, because a shot approved for a thumbnail has not been approved for a project page.

Every shot is four decisions: angle, crop, ground, and light. Sets go flat when those stop changing, so the audit checks neighbours as well as single images. [vitrine.py](skills/vitrine/scripts/vitrine.py) measures what it can, then builds a sheet at ship size on light and dark pages. It needs Pillow; without it the audit carries on by eye and says so.

Flow refines the interface around an image, and Yum finds references. Vitrine decides what the image itself should do.

## Limits

This is craft practice, not conversion data. No engagement or A/B evidence supports it. Tested values come from one device in Blender and are expressed relative to object size, so treat them as starting points. References label each claim Tested, Sourced, Observed, or Judgement.

Measured thresholds come from 18 images. They are leads to check against the sheet, and angle and light still need an eye.

Validation scenarios live in `evals/evals.json`. They require judging actual agent work; static validation does not execute them.

MIT. See [LICENSE](LICENSE).
