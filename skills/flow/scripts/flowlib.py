"""Shared helpers for the Flow scanners. Stdlib only."""

import os
import re
from pathlib import Path

SOURCE_SUFFIXES = {".dart", ".css", ".scss", ".ts", ".tsx", ".js", ".jsx", ".html", ".vue", ".svelte"}
SKIP_DIRS = {
    "node_modules", "build", "dist", "out", "target", "vendor", "coverage",
    ".git", ".dart_tool", ".next", ".svelte-kit", ".turbo", "ios", "android",
}
SKIP_SUFFIXES = (".g.dart", ".freezed.dart", ".min.css", ".min.js")

COLOUR = re.compile(r"#[0-9a-fA-F]{3,8}\b|0x[0-9a-fA-F]{8}\b|rgba?\([^)]*\)")
NUMBER = re.compile(r"-?\d+(?:\.\d+)?")


def source_files(root):
    """Source files under root, pruning skipped directories before descending."""
    root = Path(root)
    if root.is_file():
        return [root]
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for name in sorted(filenames):
            path = Path(dirpath, name)
            if path.suffix in SOURCE_SUFFIXES and not name.endswith(SKIP_SUFFIXES):
                found.append(path)
    return found


def site(path, root):
    """file:line stays readable: paths are relative to the scanned root."""
    root = Path(root)
    base = root.parent if root.is_file() else root
    try:
        return str(path.relative_to(base))
    except ValueError:
        return str(path)


def canonical(literal):
    """0xFFA1A1AA, #a1a1aa and rgb(161,161,170) are one colour, not three."""
    text = literal.strip().upper()
    if text.startswith("RGB"):
        parts = NUMBER.findall(text)[:3]
        if len(parts) < 3:
            raise ValueError(f"unparseable colour: {literal}")
        return "#" + "".join(f"{int(float(p)):02X}" for p in parts)
    digits = text.lstrip("#")
    if digits.startswith("0X"):
        digits = digits[2:]
    if len(digits) == 8:
        digits = digits[2:]
    if len(digits) == 3:
        digits = "".join(c * 2 for c in digits)
    if len(digits) != 6:
        raise ValueError(f"unparseable colour: {literal}")
    return f"#{digits}"
