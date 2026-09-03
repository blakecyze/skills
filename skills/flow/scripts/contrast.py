#!/usr/bin/env python3
"""WCAG 2.1 contrast ratios. Models must not estimate these.

  contrast.py "#18181B" "#FFFFFF"
  contrast.py --scan lib/ --config flow.config.json
  contrast.py --matrix "#FFF" "#A1A1AA" "#52525B"
"""

import argparse
import json
import sys
from itertools import combinations
from pathlib import Path

from flowlib import COLOUR, canonical, site, source_files


def parse(value):
    """Return (r, g, b) from hex, 0xAARRGGBB, or rgb()."""
    digits = canonical(value).lstrip("#")
    return tuple(int(digits[i:i + 2], 16) for i in (0, 2, 4))


def luminance(rgb):
    channels = []
    for raw in rgb:
        c = raw / 255
        channels.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
    r, g, b = channels
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    la, lb = luminance(parse(a)), luminance(parse(b))
    lighter, darker = max(la, lb), min(la, lb)
    return (lighter + 0.05) / (darker + 0.05)


def verdict(value):
    return {
        "body": "PASS" if value >= 4.5 else "FAIL",
        "large": "PASS" if value >= 3.0 else "FAIL",
        "ui": "PASS" if value >= 3.0 else "FAIL",
        "aaa": "PASS" if value >= 7.0 else "FAIL",
    }


def load_backgrounds(config_path):
    defaults = ["#FFFFFF", "#18181B"]
    if not config_path:
        return defaults
    config = json.loads(Path(config_path).read_text())
    neutral = config.get("colour", {}).get("neutral")
    return [neutral[0], neutral[-1]] if neutral else defaults


def collect(root):
    """Map canonical colour -> [file:line] across a tree."""
    found = {}
    for path in source_files(root):
        for number, line in enumerate(path.read_text(errors="ignore").splitlines(), 1):
            for raw in COLOUR.findall(line):
                try:
                    found.setdefault(canonical(raw), []).append(f"{site(path, root)}:{number}")
                except ValueError:
                    continue
    return found


def report_scan(root, config_path, top):
    backgrounds = load_backgrounds(config_path)
    found = collect(root)
    if not found:
        print("No colour literals found.")
        return

    rows = []
    for colour, sites in sorted(found.items(), key=lambda kv: -len(kv[1])):
        ratios = [ratio(colour, bg) for bg in backgrounds]
        rows.append((colour, ratios, sites))
    failing = [r for r in rows if all(x < 3.0 for x in r[1])]

    print(f"## Contrast scan: {root}\n")
    print(f"**{len(rows)} distinct colours across {sum(len(s) for _, _, s in rows)} sites. "
          f"{len(failing)} fail 3:1 against both backgrounds** ({', '.join(backgrounds)}).\n")

    print("| Colour | " + " | ".join(f"vs {b}" for b in backgrounds) + " | Uses | First seen |")
    print("|---|" + "---|" * (len(backgrounds) + 2))
    shown = failing + [r for r in rows if r not in failing]
    for colour, ratios, sites in shown[:top]:
        note = " **fails both**" if all(r < 3.0 for r in ratios) else ""
        cells = " | ".join(f"{r:.2f}" for r in ratios)
        print(f"| `{colour}` | {cells} | {len(sites)} | `{sites[0]}`{note} |")
    if len(rows) > top:
        print(f"\n+{len(rows) - top} more colours. Raise `--top` to see them.")

    print("\nRatios are against the extreme backgrounds only. A colour passing here can still")
    print("fail against a mid-ramp surface. Check real pairs with the two-argument form.")


def report_matrix(colours):
    print("| A | B | Ratio | Body 4.5 | Large 3.0 |")
    print("|---|---|---|---|---|")
    for a, b in combinations(colours, 2):
        value = ratio(a, b)
        v = verdict(value)
        print(f"| `{a}` | `{b}` | {value:.2f} | {v['body']} | {v['large']} |")


def main():
    parser = argparse.ArgumentParser(description="WCAG 2.1 contrast ratios")
    parser.add_argument("colours", nargs="*", help="two colours, or several with --matrix")
    parser.add_argument("--scan", metavar="PATH", help="extract colours from a file or tree")
    parser.add_argument("--config", metavar="PATH", help="flow.config.json for background candidates")
    parser.add_argument("--matrix", action="store_true", help="every pair among the given colours")
    parser.add_argument("--top", type=int, default=15, help="rows in the scan table, failures first")
    args = parser.parse_args()

    if args.scan:
        report_scan(args.scan, args.config, args.top)
        return 0

    if args.matrix:
        report_matrix(args.colours)
        return 0

    if len(args.colours) != 2:
        parser.error("give two colours, or use --scan / --matrix")

    value = ratio(*args.colours)
    v = verdict(value)
    print(f"{args.colours[0]} on {args.colours[1]}: {value:.2f}:1")
    print(f"  Body text (4.5:1)      {v['body']}")
    print(f"  Large text (3.0:1)     {v['large']}")
    print(f"  UI and focus (3.0:1)   {v['ui']}")
    print(f"  AAA body (7.0:1)       {v['aaa']}")
    return 0 if v["body"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
