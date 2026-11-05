#!/usr/bin/env python3
"""Measure how images present what they show, and build a sheet at the size they ship.

  vitrine.py a.png b.png c.jpg
  vitrine.py shots/*.jpg --sheet /tmp/sheet.png --size 300

Order matters: pass images in the order they sit next to each other. Needs Pillow.
"""

import argparse
import math
import statistics
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageOps
except ImportError:
    sys.exit("Needs Pillow. Run: python3 -m venv <temp>/v && <temp>/v/bin/pip install pillow, then use <temp>/v/bin/python. If that fails, judge by eye and call the findings unmeasured.")

ANALYSIS_EDGE = 220
RING = 0.04
INSET = 3  # Pixels past the step before sampling, on the analysis scale.
EDGE_STEP = 0.015  # Oklab change across two pixels that counts as an outline, not a falloff.
SAME_COLOUR = 0.045  # Oklab distance at which two grounds read as different.
UNIFORM_GROUND = 0.6  # Share of border rays that must cross open ground first.
LOW_JUMP = 8  # L* points. Calibrated by eye on 18 images; a lead, not a law.
FILLS_FRAME = 0.85
LOUD_CHROMA, LOUD_AREA = 0.10, 0.015
SMALL_FILL = 0.2
SAME_FILL, SAME_CENTRE = 0.10, 0.06


def to_linear(channel):
    c = channel / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


LINEAR = [to_linear(i) for i in range(256)]


def lstar(y):
    return 116 * y ** (1 / 3) - 16 if y > 0.008856 else 903.3 * y


def oklab(rgb):
    r, g, b = LINEAR[rgb[0]], LINEAR[rgb[1]], LINEAR[rgb[2]]
    l = (0.4122 * r + 0.5363 * g + 0.0514 * b) ** (1 / 3)
    m = (0.2119 * r + 0.6807 * g + 0.1074 * b) ** (1 / 3)
    s = (0.0883 * r + 0.2817 * g + 0.6300 * b) ** (1 / 3)
    return (0.2105 * l + 0.7936 * m - 0.0041 * s, 1.9780 * l - 2.4286 * m + 0.4506 * s, 0.0259 * l + 0.7828 * m - 0.8087 * s)


def distance(a, b):
    return math.dist(a, b)


def luminance_star(rgb):
    return lstar(0.2126 * LINEAR[rgb[0]] + 0.7152 * LINEAR[rgb[1]] + 0.0722 * LINEAR[rgb[2]])


def median_rgb(pixels):
    return tuple(int(statistics.median(p[i] for p in pixels)) for i in range(3))


def hex_of(rgb):
    return "#%02x%02x%02x" % tuple(rgb)


def loud_colours(pixels):
    """Hue families carrying real area at high chroma. Adjacent 30-degree bins count as one."""
    bins = [[] for _ in range(12)]
    for rgb in pixels:
        _, a, b = oklab(rgb)
        if math.hypot(a, b) >= LOUD_CHROMA:
            bins[int((math.degrees(math.atan2(b, a)) % 360) // 30)].append(rgb)
    share = [len(items) / len(pixels) for items in bins]
    families, seen = [], set()
    for start in range(12):
        if start in seen or share[start] < LOUD_AREA / 3:
            continue
        group, step = [], start
        while share[step % 12] >= LOUD_AREA / 3 and step % 12 not in seen:
            seen.add(step % 12)
            group.append(step % 12)
            step += 1
        step = start - 1
        while share[step % 12] >= LOUD_AREA / 3 and step % 12 not in seen:
            seen.add(step % 12)
            group.append(step % 12)
            step -= 1
        if sum(share[i] for i in group) >= LOUD_AREA:
            families.append(hex_of(median_rgb([p for i in group for p in bins[i]])))
    return families


def ray_edges(labs, values, w, h):
    """Walk in from every side to the first sharp step. Lit grounds fall off slowly, outlines do not."""
    sides = {
        "L": [[y * w + x for x in range(w)] for y in range(0, h, 2)],
        "R": [[y * w + x for x in range(w - 1, -1, -1)] for y in range(0, h, 2)],
        "T": [[y * w + x for y in range(h)] for x in range(0, w, 2)],
        "B": [[y * w + x for y in range(h - 1, -1, -1)] for x in range(0, w, 2)],
    }
    found = {}
    for side, rays in sides.items():
        hits = []
        for ray in rays:
            for i in range(len(ray) - 2):
                if distance(labs[ray[i]], labs[ray[i + 2]]) >= EDGE_STEP:
                    hits.append((i, ray))
                    break
        found[side] = hits
    return found


def measure(path):
    source = Image.open(path)
    width, height = source.size
    image = ImageOps.exif_transpose(source).convert("RGB")
    image.thumbnail((ANALYSIS_EDGE, ANALYSIS_EDGE))
    w, h = image.size
    pixels = list(image.getdata())
    labs = [oklab(p) for p in pixels]
    values = [luminance_star(p) for p in pixels]
    result = {
        "path": path,
        "name": Path(path).name,
        "size": f"{width}x{height}",
        "kb": Path(path).stat().st_size // 1024,
        "loud": loud_colours(pixels),
        "ground": None,
    }
    edges = ray_edges(labs, values, w, h)
    margin = max(2, round(max(w, h) * RING))
    rays = {"L": len(range(0, h, 2)), "R": len(range(0, h, 2)), "T": len(range(0, w, 2)), "B": len(range(0, w, 2))}
    # A ground exists if most of the frame's border leads somewhere before anything happens.
    open_rays = sum(rays[side] - sum(i < margin for i, _ in hits) for side, hits in edges.items())
    if open_rays < sum(rays.values()) * UNIFORM_GROUND:
        return result
    walked = [ray[k] for hits in edges.values() for i, ray in hits for k in range(max(i - 1, 0))]
    if not walked:
        return result
    ground_rgb = median_rgb([pixels[k] for k in walked])
    result["ground"] = hex_of(ground_rgb)
    result["ground_lab"] = oklab(ground_rgb)
    result["ground_l"] = luminance_star(ground_rgb)
    jumps, xs, ys = [], [], []
    for side, hits in edges.items():
        if len(hits) < rays[side] * 0.15:
            continue
        steps = []
        for i, ray in hits:
            k = ray[i + 1]
            xs.append(k % w)
            ys.append(k // w)
            if i >= margin:
                steps.append(abs(values[ray[min(i + INSET, len(ray) - 1)]] - values[ray[max(i - 1, 0)]]))
        if steps:
            jumps.append(statistics.median(steps))
    if not xs:
        result["fill"] = 0
        return result
    xs.sort()
    ys.sort()
    trim = len(xs) // 50
    x0, x1, y0, y1 = xs[trim], xs[-1 - trim], ys[trim], ys[-1 - trim]
    result["fill"] = ((x1 - x0 + 1) * (y1 - y0 + 1)) / (w * h)
    result["centre"] = ((x0 + x1) / 2 / w, (y0 + y1) / 2 / h)
    result["touches"] = "".join(side for side, hit in zip("TRBL", (y0 < margin, x1 >= w - margin, y1 >= h - margin, x0 < margin)) if hit)
    result["jump"] = statistics.median(jumps) if jumps else None
    return result


def flags(shot):
    found = []
    if shot["ground"] is None:
        found.append("no clear ground: too much happens at the border to measure jump and fill")
    else:
        jump, fill = shot.get("jump"), shot.get("fill", 0)
        if fill >= FILLS_FRAME:
            found.append("fills the frame: outline contrast not measured, judge by eye")
        elif jump is not None and jump < LOW_JUMP:
            found.append(f"low value jump ({jump:.0f} L*): the outline melts into the ground without a strong shadow")
        if fill and fill < SMALL_FILL:
            found.append(f"small in frame ({fill:.0%}): check it reads at ship size")
    if len(shot["loud"]) > 1:
        found.append(f"{len(shot['loud'])} loud colours compete: {', '.join(shot['loud'])}")
    return found


def compare(a, b):
    """What visibly changes between neighbours. Only ground and crop can be measured; angle and light are for the eye."""
    if a["ground"] is None or b["ground"] is None or "centre" not in a or "centre" not in b:
        return None
    ground = distance(a["ground_lab"], b["ground_lab"]) >= SAME_COLOUR
    crop = abs(a["fill"] - b["fill"]) >= SAME_FILL or math.dist(a["centre"], b["centre"]) >= SAME_CENTRE or a["touches"] != b["touches"]
    return ground, crop


def sheet(shots, out, size, columns):
    """Every image at ship width, on a light page and a dark page."""
    columns = columns or min(len(shots), 4)
    gap, label = 16, 18
    tiles = []
    for shot in shots:
        tile = ImageOps.exif_transpose(Image.open(shot["path"])).convert("RGB")
        tile.thumbnail((size, size * 2), Image.LANCZOS)
        tiles.append(tile)
    row_height = max(t.height for t in tiles) + label
    rows = math.ceil(len(tiles) / columns)
    band = rows * (row_height + gap) + gap
    canvas = Image.new("RGB", (columns * (size + gap) + gap, band * 2), "#ffffff")
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, band, canvas.width, band * 2), fill="#111114")
    for top, ink in ((0, "#555555"), (band, "#aaaaaa")):
        for i, (tile, shot) in enumerate(zip(tiles, shots)):
            x = gap + (i % columns) * (size + gap)
            y = top + gap + (i // columns) * (row_height + gap)
            canvas.paste(tile, (x, y))
            draw.text((x, y + tile.height + 3), shot["name"][: size // 6], fill=ink)
    canvas.save(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("images", nargs="+")
    parser.add_argument("--sheet", help="write a contact sheet here")
    parser.add_argument("--size", type=int, default=300, help="ship width in px for the sheet (default 300)")
    parser.add_argument("--columns", type=int)
    args = parser.parse_args()

    shots, failed = [], []
    for path in args.images:
        try:
            shots.append(measure(path))
        except OSError as error:
            failed.append(f"{path}: cannot decode ({error}). Convert a copy to PNG with ffmpeg or sips and measure that.")
    for line in failed:
        print(f"skipped: {line}")
    for shot in shots:
        if shot["ground"]:
            detail = f"ground {shot['ground']} L*{shot['ground_l']:.0f}"
            if shot.get("fill"):
                jump = "-" if shot["jump"] is None else f"{shot['jump']:.0f}"
                detail += f"  jump {jump}  fill {shot['fill']:.0%}  edges {shot['touches'] or '-'}"
        else:
            detail = "no clear ground"
        print(f"{shot['name']}  {shot['size']}  {shot['kb']} KB  {detail}  loud {len(shot['loud'])}")
        for line in flags(shot):
            print(f"  - {line}")
    pairs = [(a, b, compare(a, b)) for a, b in zip(shots, shots[1:])]
    comparable = [pair for pair in pairs if pair[2] is not None]
    samey = [(a, b) for a, b, change in comparable if change == (False, False)]
    for a, b in samey:
        print(f"neighbours: {a['name']} and {b['name']} share a ground and a crop")
    grounds = [s["ground_lab"] for s in shots if s["ground"]]
    distinct = []
    for ground in grounds:
        if all(distance(ground, seen) >= SAME_COLOUR for seen in distinct):
            distinct.append(ground)
    if len(shots) > 2 and all(s["ground"] and s.get("fill") and not s["touches"] for s in shots):
        print("set: every image holds the whole object inside the frame; nothing crops in")
    if len(shots) > 2 and len(distinct) == 1 and len(grounds) == len(shots):
        print("set: every image sits on the same ground")
    if len(shots) > 1:
        print(f"set: {len(shots)} images, {len(distinct)} distinct grounds in the {len(grounds)} measured, {len(samey)} of {len(comparable)} measurable neighbours (of {len(pairs)}) share both ground and crop")
        print("Measured: ground, crop, value, colour. Angle and light need your eye. Thresholds are leads, not laws.")
    if args.sheet and shots:
        sheet(shots, args.sheet, args.size, args.columns)
        print(f"sheet: {args.sheet}")


if __name__ == "__main__":
    main()
