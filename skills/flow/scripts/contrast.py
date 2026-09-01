#!/usr/bin/env python3
"""WCAG 2.1 contrast ratios. Models must not estimate these.

  contrast.py "#18181B" "#FFFFFF"
  contrast.py --scan lib/ --config flow.config.json
  contrast.py --matrix "#FFF" "#A1A1AA" "#52525B"
"""

import argparse
import json
import re
import sys
from itertools import combinations
from pathlib import Path

HEX = re.compile(r"#([0-9a-fA-F]{3,8})\b")
ARGB = re.compile(r"0x([0-9a-fA-F]{8})\b")
RGB_FUNC = re.compile(r"rgba?\(\s*(\d+)[,\s]+(\d+)[,\s]+(\d+)")

SOURCE_SUFFIXES = {".dart", ".css", ".scss", ".ts", ".tsx", ".js", ".jsx", ".html", ".vue", ".svelte"}
SKIP_DIRS = {"node_modules", "build", "dist", ".git", ".dart_tool", "ios", "android", "vendor", "coverage"}


def parse(value):
    """Return (r, g, b) from hex, 0xAARRGGBB, or rgb()."""
    value = value.strip()

    match = RGB_FUNC.match(value)
    if match:
        return tuple(int(g) for g in match.groups())

    digits = value.lstrip("#")
    if digits.lower().startswith("0x"):
        digits = digits[2:]
    if len(digits) == 8:
        digits = digits[2:]
    if len(digits) == 3:
        digits = "".join(c * 2 for c in digits)
    if len(digits) != 6:
        raise ValueError(f"unparseable colour: {value}")
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


def source_files(root):
    root = Path(root)
    if root.is_file():
        return [root]
    return [
        p for p in root.rglob("*")
        if p.suffix in SOURCE_SUFFIXES and not SKIP_DIRS & set(p.parts)
    ]


def collect(root):
    """Map colour -> [file:line] across a tree."""
    found = {}
    for path in source_files(root):
        for number, line in enumerate(path.read_text(errors="ignore").splitlines(), 1):
            for raw in HEX.findall(line):
                if len(raw) in (3, 6, 8):
                    found.setdefault(f"#{raw.upper()}", []).append(f"{path}:{number}")
            for raw in ARGB.findall(line):
                found.setdefault(f"#{raw[2:].upper()}", []).append(f"{path}:{number}")
    return found


def report_scan(root, config_path):
    backgrounds = load_backgrounds(config_path)
    found = collect(root)
    if not found:
        print("No colour literals found.")
        return

    print(f"## Contrast scan: {root}\n")
    print(f"Backgrounds tested: {', '.join(backgrounds)}\n")
    print("| Colour | " + " | ".join(f"vs {b}" for b in backgrounds) + " | Uses | First seen |")
    print("|---|" + "---|" * (len(backgrounds) + 2))

    for colour, sites in sorted(found.items(), key=lambda kv: -len(kv[1])):
        try:
            ratios = [ratio(colour, bg) for bg in backgrounds]
        except ValueError:
            continue
        note = "**fails on both**" if all(r < 3.0 for r in ratios) else ""
        cells = " | ".join(f"{r:.2f}" for r in ratios)
        print(f"| `{colour}` | {cells} | {len(sites)} | `{sites[0]}` {note} |")

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
    args = parser.parse_args()

    if args.scan:
        report_scan(args.scan, args.config)
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
