#!/usr/bin/env python3
"""Find values that escape the design scale. Backs FLOW-04 and flow-tokens.

  scan_tokens.py lib/
  scan_tokens.py lib/ --config flow.config.json
  scan_tokens.py lib/ --report frequency
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

SOURCE_SUFFIXES = {".dart", ".css", ".scss", ".ts", ".tsx", ".js", ".jsx", ".html", ".vue", ".svelte"}
SKIP_DIRS = {"node_modules", "build", "dist", ".git", ".dart_tool", "vendor", "coverage", ".next"}
SKIP_SUFFIXES = (".g.dart", ".freezed.dart", ".min.css", ".min.js")

SPACING_PROPS = r"padding|margin|gap|spacing|inset|top|left|right|bottom|width|height|size"
PATTERNS = {
    "spacing": [
        re.compile(rf"\b(?:{SPACING_PROPS})[A-Za-z]*\s*[:=]\s*(\d+(?:\.\d+)?)\b", re.I),
        re.compile(r"\bEdgeInsets\.(?:all|symmetric|only|fromLTRB)\(([^)]*)\)"),
        re.compile(rf"\b(?:{SPACING_PROPS})[a-z-]*\s*:\s*(-?\d+(?:\.\d+)?)(?:px|rem)", re.I),
    ],
    "type": [
        re.compile(r"\bfont-?[Ss]ize\s*[:=]\s*(\d+(?:\.\d+)?)(?:px|rem)?", re.I),
    ],
    "radius": [
        re.compile(r"\b(?:border-?[Rr]adius|circular|Radius\.circular)\s*[:=(]\s*(\d+(?:\.\d+)?)", re.I),
    ],
}
ARBITRARY = re.compile(r"(?:\[|\()(\d+(?:\.\d+)?)(px|rem)(?:\]|\))")
COLOUR = re.compile(r"#[0-9a-fA-F]{3,8}\b|0x[0-9a-fA-F]{8}\b|rgba?\([^)]*\)")
NUMBER = re.compile(r"-?\d+(?:\.\d+)?")


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


def canonical(literal):
    """0xFFA1A1AA, #a1a1aa and rgb(161,161,170) are one colour, not three."""
    text = literal.strip().upper()
    if text.startswith("RGB"):
        parts = NUMBER.findall(text)[:3]
        return "#" + "".join(f"{int(float(p)):02X}" for p in parts)
    digits = text.lstrip("#")
    if digits.startswith("0X"):
        digits = digits[2:]
    if len(digits) == 8:
        digits = digits[2:]
    if len(digits) == 3:
        digits = "".join(c * 2 for c in digits)
    return f"#{digits}"


def source_files(root):
    root = Path(root)
    if root.is_file():
        return [root]
    return [
        p for p in sorted(root.rglob("*"))
        if p.suffix in SOURCE_SUFFIXES
        and not SKIP_DIRS & set(p.parts)
        and not p.name.endswith(SKIP_SUFFIXES)
    ]


def normalise(raw, line):
    """rem values are px at a 16px root; everything else is taken literally."""
    value = float(raw)
    if "rem" in line and value < 8:
        value *= 16
    return int(value) if value == int(value) else value


def scan(root):
    hits = defaultdict(list)
    colours = defaultdict(list)
    for path in source_files(root):
        for number, line in enumerate(path.read_text(errors="ignore").splitlines(), 1):
            site = f"{path}:{number}"
            for kind, patterns in PATTERNS.items():
                for pattern in patterns:
                    for match in pattern.findall(line):
                        for raw in NUMBER.findall(match):
                            hits[kind].append((normalise(raw, line), site))
            for raw, unit in ARBITRARY.findall(line):
                hits["spacing"].append((normalise(raw, unit), site))
            for match in COLOUR.findall(line):
                colours[canonical(match)].append(site)
    return hits, colours


def report_violations(hits, colours, scale, threshold):
    total = 0
    print("## Scale adherence\n")
    for kind in ("spacing", "type", "radius"):
        off = Counter(v for v, _ in hits[kind] if v not in scale[kind])
        if not off:
            continue
        sites = defaultdict(list)
        for value, site in hits[kind]:
            if value not in scale[kind]:
                sites[value].append(site)

        print(f"### {kind.title()} — FLOW-04\n")
        print("| Value | Count | Nearest on scale | Status | First seen |")
        print("|---|---|---|---|---|")
        for value, count in off.most_common():
            nearest = min(scale[kind], key=lambda s: abs(s - value))
            status = "de facto token — promote or migrate" if count >= threshold else "drift — snap"
            print(f"| `{value}` | {count} | `{nearest}` | {status} | `{sites[value][0]}` |")
            total += count
        print()

    hardcoded = {c: s for c, s in colours.items() if len(s) >= 1}
    if hardcoded:
        print(f"### Hardcoded colours — FLOW-09\n")
        print(f"{len(hardcoded)} distinct literal colours across {sum(len(s) for s in hardcoded.values())} sites.\n")
        print("| Colour | Count | First seen |")
        print("|---|---|---|")
        for colour, sites in sorted(hardcoded.items(), key=lambda kv: -len(kv[1]))[:20]:
            print(f"| `{colour}` | {len(sites)} | `{sites[0]}` |")
        print()

    print(f"**{total} off-scale values.** Run with `--report frequency` to see the full picture before migrating.")


def report_frequency(hits):
    print("## Value frequency\n")
    for kind in ("spacing", "type", "radius"):
        counts = Counter(v for v, _ in hits[kind])
        if not counts:
            continue
        print(f"### {kind.title()}\n")
        print("| Value | Count |")
        print("|---|---|")
        for value, count in counts.most_common(25):
            print(f"| `{value}` | {count} |")
        print()


def main():
    parser = argparse.ArgumentParser(description="Find values that escape the design scale")
    parser.add_argument("path", help="file or directory to scan")
    parser.add_argument("--config", metavar="PATH", help="flow.config.json overriding the defaults")
    parser.add_argument("--report", choices=("violations", "frequency"), default="violations")
    parser.add_argument("--threshold", type=int, default=10,
                        help="uses above which an off-scale value counts as a de facto token")
    args = parser.parse_args()

    hits, colours = scan(args.path)
    if args.report == "frequency":
        report_frequency(hits)
    else:
        report_violations(hits, colours, load_scale(args.config), args.threshold)
    return 0


if __name__ == "__main__":
    sys.exit(main())
