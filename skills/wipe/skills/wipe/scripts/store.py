"""Runs, versions and the manifest. Standard library only."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import struct
from datetime import datetime, timezone
from pathlib import Path

import repo

DIR = ".wipe"
EXCLUDE_LINE = "/.wipe/"


def slug(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s or "index"


def route_slug(route: str, taken: set) -> str:
    """Slug for a route; a short hash is appended when the plain slug is taken."""
    plain = slug(route)
    if plain not in taken:
        return plain
    return f"{plain}-{hashlib.sha1(route.encode()).hexdigest()[:6]}"


def default_run(root: Path) -> str:
    branch = repo.current_branch(root) if repo.is_git(root) else None
    return slug(branch) if branch else "default"


def run_dir(root: Path, run: str) -> Path:
    return Path(root) / DIR / run


def _empty(run):
    return {"run": run, "base_url": None, "viewport": None, "theme": None,
            "routes": [], "worktrees": [], "versions": []}


def load_run(root: Path, run: str) -> dict:
    f = run_dir(root, run) / "manifest.json"
    if not f.exists():
        return _empty(run)
    return json.loads(f.read_text())


def save_run(root: Path, manifest: dict) -> None:
    d = run_dir(root, manifest["run"])
    d.mkdir(parents=True, exist_ok=True)
    (d / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


def ensure_excluded(root: Path) -> None:
    """Add /.wipe/ to .git/info/exclude once. Never touches .gitignore."""
    if not repo.is_git(root):
        return
    out = repo._git(root, "rev-parse", "--git-path", "info/exclude")
    if out.returncode != 0:
        return
    f = Path(root) / out.stdout.strip()
    existing = f.read_text() if f.exists() else ""
    if EXCLUDE_LINE in existing.splitlines():
        return
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(existing + ("" if not existing or existing.endswith("\n") else "\n") + EXCLUDE_LINE + "\n")


def add_version(root: Path, manifest: dict, note: str, images: dict, method: str,
                scale: int, measure=None) -> dict:
    """Copy images into the next vN folder and append the version. Does not save."""
    index = len(manifest["versions"])
    label = f"v{index}"
    known = {}
    for v in manifest["versions"]:
        for route, rel in v["images"].items():
            known.setdefault(route, Path(rel).stem)
    taken = set(known.values())
    dest = run_dir(root, manifest["run"]) / label
    dest.mkdir(parents=True, exist_ok=True)
    rels = {}
    for route, src in images.items():
        if route not in known:
            known[route] = route_slug(route, taken)
            taken.add(known[route])
        shutil.copyfile(src, dest / f"{known[route]}.png")
        rels[route] = f"{label}/{known[route]}.png"
        if route not in manifest["routes"]:
            manifest["routes"].append(route)
    info = repo.git_info(root)
    version = {"index": index, "label": label, "note": note,
               "time": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
               "sha": info["sha"], "dirty": info["dirty"], "method": method,
               "scale": scale, "images": rels, "measure": measure}
    manifest["versions"].append(version)
    return version


def check_conditions(manifest: dict, viewport, theme, routes) -> list:
    """Warnings for a snap whose conditions differ from the run's earlier versions."""
    if not manifest["versions"]:
        return []
    out = []
    old = manifest.get("viewport")
    if old and list(old) != list(viewport):
        out.append(f"Viewport is {viewport[0]}x{viewport[1]}; earlier versions used {old[0]}x{old[1]}.")
    if manifest.get("theme") and manifest["theme"] != theme:
        out.append(f"Theme is {theme}; earlier versions used {manifest['theme']}.")
    new = [r for r in routes if r not in manifest["routes"]]
    if new:
        out.append(f"New route{'s' if len(new) > 1 else ''} not in earlier versions: {', '.join(new)}.")
    return out


def image_size(path: Path) -> tuple:
    """Width and height from the PNG IHDR chunk."""
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n" or head[12:16] != b"IHDR":
        raise ValueError(f"Not a PNG: {path}")
    return struct.unpack(">II", head[16:24])
