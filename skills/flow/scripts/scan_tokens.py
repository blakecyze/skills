#!/usr/bin/env python3
"""Find values that escape the design scale. Backs FLOW-04 and flow-tokens.

  scan_tokens.py lib/
  scan_tokens.py lib/ --config flow.config.json
  scan_tokens.py lib/ --report frequency
  scan_tokens.py lib/ --top 30
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from flowlib import COLOUR, NUMBER, canonical, site, source_files

STYLE_SUFFIXES = {".css", ".scss", ".html"}
CODE_SUFFIXES = {".ts", ".tsx", ".js", ".jsx", ".vue", ".svelte"}

SPACING_PROPS = r"padding|margin|gap|spacing|inset|top|left|right|bottom|width|height|size"

# Stylesheets: a bare number after a spacing property is a design value.
# Code: it is usually geometry, so require a unit or a Tailwind arbitrary value.
UNITLESS_SPACING = re.compile(rf"\b(?:{SPACING_PROPS})[A-Za-z]*\s*[:=]\s*(\d+(?:\.\d+)?)\b", re.I)
UNIT_SPACING = re.compile(rf"\b(?:{SPACING_PROPS})[a-z-]*\s*:\s*(-?\d+(?:\.\d+)?)(?:px|rem)", re.I)
EDGE_INSETS = re.compile(r"\bEdgeInsets\.(?:all|symmetric|only|fromLTRB)\(([^)]*)\)")
SIZED_BOX = re.compile(r"\b(?:SizedBox|Gap)\(\s*(?:(?:width|height):\s*)?(\d+(?:\.\d+)?)")
FONT_SIZE = re.compile(r"\bfont-?[Ss]ize\s*[:=]\s*(\d+(?:\.\d+)?)(?:px|rem)?", re.I)
RADIUS = re.compile(r"\b(?:border-?[Rr]adius|circular|Radius\.circular)\s*[:=(]\s*(\d+(?:\.\d+)?)", re.I)
ARBITRARY = re.compile(r"(?:\[|\()(\d+(?:\.\d+)?)(px|rem)(?:\]|\))")

PATTERNS = {
    "style": {"spacing": [UNITLESS_SPACING, UNIT_SPACING], "type": [FONT_SIZE], "radius": [RADIUS]},
    "code": {"spacing": [UNIT_SPACING], "type": [FONT_SIZE], "radius": [RADIUS]},
    ".dart": {"spacing": [EDGE_INSETS, SIZED_BOX], "type": [FONT_SIZE], "radius": [RADIUS]},
}
SPACING_FLOOR = 3  # 1 and 2 are hairlines, borders, z-index, and opacity, not spacing


def patterns_for(path):
    if path.suffix in STYLE_SUFFIXES:
        return PATTERNS["style"]
    if path.suffix in CODE_SUFFIXES:
        return PATTERNS["code"]
    return PATTERNS.get(path.suffix, PATTERNS["code"])


def load_scale(config_path):
    root = Path(__file__).resolve().parent.parent
    scale = json.loads((root / "tokens" / "flow.defaults.json").read_text())
    if config_path:
        override = json.loads(Path(config_path).read_text())
        for key, value in override.items():
            if isinstance(value, dict) and isinstance(scale.get(key), dict):
                scale[key].update(value)
            else:
                scale[key] = value
    return {
        "spacing": set(scale["spacing"]["ramp"]) | {0},
        "type": set(scale["type"]["scale"].values()),
        "radius": {v for v in scale["radius"].values() if isinstance(v, (int, float))},
    }


def normalise(raw, line):
    """rem values are px at a 16px root; everything else is taken literally."""
    value = float(raw)
    if "rem" in line and value < 8:
        value *= 16
    return int(value) if value == int(value) else value


def scan(root):
    hits = defaultdict(list)
    colours = defaultdict(list)
    files = source_files(root)
    for path in files:
        patterns = patterns_for(path)
        for number, line in enumerate(path.read_text(errors="ignore").splitlines(), 1):
            where = f"{site(path, root)}:{number}"
            for kind, kind_patterns in patterns.items():
                for pattern in kind_patterns:
                    for match in pattern.findall(line):
                        for raw in NUMBER.findall(match):
                            value = normalise(raw, line)
                            if kind == "spacing" and abs(value) < SPACING_FLOOR:
                                continue
                            hits[kind].append((value, where))
            for raw, unit in ARBITRARY.findall(line):
                hits["spacing"].append((normalise(raw, unit), where))
            for match in COLOUR.findall(line):
                try:
                    colours[canonical(match)].append(where)
                except ValueError:
                    continue
    return hits, colours, len(files)


def report_violations(hits, colours, scale, threshold, top):
    off_scale = {}
    for kind in ("spacing", "type", "radius"):
        sites = defaultdict(list)
        for value, where in hits[kind]:
            if value not in scale[kind]:
                sites[value].append(where)
        if sites:
            off_scale[kind] = sites

    total = sum(len(s) for kind in off_scale.values() for s in kind.values())
    distinct = sum(len(kind) for kind in off_scale.values())
    print(f"**{total} off-scale values, {distinct} distinct, {len(colours)} literal colours.** "
          f"Showing the top {top} per kind; singletons are counted, not listed.\n")

    for kind, sites in off_scale.items():
        ranked = sorted(sites.items(), key=lambda kv: -len(kv[1]))
        listed = [(v, s) for v, s in ranked if len(s) > 1][:top]
        singles = sum(1 for _, s in ranked if len(s) == 1)
        hidden = len(ranked) - len(listed) - singles
        if not listed:
            print(f"### {kind.title()} — FLOW-04: {singles} singletons only, nothing repeated.\n")
            continue
        print(f"### {kind.title()} — FLOW-04\n")
        print("| Value | Count | Nearest | Status | First seen |")
        print("|---|---|---|---|---|")
        for value, where in listed:
            nearest = min(scale[kind], key=lambda s: abs(s - value))
            status = "de facto — promote or migrate" if len(where) >= threshold else "drift — snap"
            print(f"| `{value}` | {len(where)} | `{nearest}` | {status} | `{where[0]}` |")
        tail = []
        if hidden:
            tail.append(f"{hidden} more repeated values")
        if singles:
            tail.append(f"{singles} singletons")
        if tail:
            print(f"\n+{', '.join(tail)}. Run `--report frequency` or raise `--top` to see them.")
        print()

    if colours:
        sites = sum(len(s) for s in colours.values())
        print(f"### Colours — FLOW-09\n\n{len(colours)} distinct literal colours across {sites} sites. "
              "Run `contrast.py --scan` for ratios and locations.")


def report_frequency(hits, top):
    print("## Value frequency\n")
    for kind in ("spacing", "type", "radius"):
        counts = Counter(v for v, _ in hits[kind])
        if not counts:
            continue
        print(f"### {kind.title()}\n")
        print("| Value | Count |")
        print("|---|---|")
        for value, count in counts.most_common(top):
            print(f"| `{value}` | {count} |")
        if len(counts) > top:
            print(f"\n+{len(counts) - top} more values.")
        print()


def main():
    parser = argparse.ArgumentParser(description="Find values that escape the design scale")
    parser.add_argument("path", help="file or directory to scan")
    parser.add_argument("--config", metavar="PATH", help="flow.config.json overriding the defaults")
    parser.add_argument("--report", choices=("violations", "frequency"), default="violations")
    parser.add_argument("--threshold", type=int, default=10,
                        help="uses above which an off-scale value counts as a de facto token")
    parser.add_argument("--top", type=int, default=15, help="rows per table")
    args = parser.parse_args()

    hits, colours, file_count = scan(args.path)
    print(f"## Scan: {args.path} ({file_count} files)\n")
    if args.report == "frequency":
        report_frequency(hits, args.top)
    else:
        report_violations(hits, colours, load_scale(args.config), args.threshold, args.top)
    return 0


if __name__ == "__main__":
    sys.exit(main())
