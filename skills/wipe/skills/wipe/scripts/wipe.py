#!/usr/bin/env python3
"""Wipe: save each UI pass as a version, compare versions, render before/after clips."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import capture  # noqa: E402
import page  # noqa: E402
import repo  # noqa: E402
import store  # noqa: E402

PLAYWRIGHT_HELP = ("Needs Playwright. Run: python3 -m venv <temp>/v && <temp>/v/bin/pip install playwright, "
                   "then use <temp>/v/bin/python.")


class UsageError(Exception):
    """Bad arguments for this run. main prints it and exits 2."""


def warn(text):
    print(f"warning: {text}", file=sys.stderr)


def parse_viewport(text):
    try:
        w, h = text.lower().split("x")
        w, h = int(w), int(h)
        if w < 1 or h < 1:
            raise ValueError
        return (w, h)
    except ValueError:
        raise argparse.ArgumentTypeError(f"viewport must look like 1280x800, got {text!r}")


def build_parser():
    p = argparse.ArgumentParser(prog="wipe", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("snap", help="capture the current UI as the next version")
    s.add_argument("routes", nargs="*", help="routes to capture, such as /pricing")
    s.add_argument("--note", required=True, help="what this version is")
    s.add_argument("--url", help="base URL; saved and reused by later snaps")
    s.add_argument("--image", action="append", default=[], help="use an existing PNG instead of capturing")
    s.add_argument("--run", help="run name (default: current branch)")
    s.add_argument("--viewport", type=parse_viewport, help="WxH, default 1280x800")
    s.add_argument("--theme", choices=["light", "dark", "both"], help="default light")
    s.add_argument("--full", action="store_true", help="full-page capture (needs Playwright)")
    s.add_argument("--measure", action="store_true", help="record load metrics (needs Playwright)")
    s.add_argument("--method", choices=["auto", "playwright", "chrome"], default="auto")

    s = sub.add_parser("show", help="build the compare page and open it")
    s.add_argument("a", nargs="?", metavar="A", help="the before version, such as 0 or v0 (default: the second latest)")
    s.add_argument("b", nargs="?", metavar="B", help="the after version (default: the latest)")
    s.add_argument("--run", help="run name (default: current branch)")
    s.add_argument("--route", help="route to show first (default: the first one)")
    s.add_argument("--no-open", action="store_true", help="only print the page's path")

    s = sub.add_parser("embed", help="write a standalone <before-after> snippet for two versions")
    s.add_argument("a", metavar="A", help="the before version, such as 0 or v0")
    s.add_argument("b", metavar="B", help="the after version")
    s.add_argument("--run", help="run name (default: current branch)")
    s.add_argument("--route", help="route to use (default: the first one)")
    s.add_argument("--out", help="folder to write (default: .wipe/<run>/embed-vA-vB)")
    return p


def cmd_snap(args) -> int:
    root, manifest = load(args)
    run = manifest["run"]
    first = not manifest["versions"]
    viewport = args.viewport or (tuple(manifest["viewport"]) if manifest["viewport"] else (1280, 800))
    theme_arg = args.theme or manifest["theme"] or "light"
    themes = ["light", "dark"] if theme_arg == "both" else [theme_arg]

    if args.measure and not capture._has_playwright():
        print(f"error: --measure {PLAYWRIGHT_HELP}", file=sys.stderr)
        return 3
    if args.method == "playwright" and not capture._has_playwright():
        print(f"error: --method playwright {PLAYWRIGHT_HELP}", file=sys.stderr)
        return 3
    base_url = args.url or manifest["base_url"]
    if args.measure and not base_url:
        print("error: --measure needs --url", file=sys.stderr)
        return 2

    images, method, measures = {}, None, {}
    with tempfile.TemporaryDirectory(prefix="wipe-snap-") as tmp:
        tmp = Path(tmp)
        if args.image:
            routes = args.routes or ["screen"]
            if len(args.image) != len(routes):
                print(f"error: {len(args.image)} --image file(s) for {len(routes)} route(s); "
                      "pass one image per route, in order", file=sys.stderr)
                return 2
            for route, img in zip(routes, args.image):
                if not Path(img).is_file():
                    print(f"error: image not found: {img}", file=sys.stderr)
                    return 2
                images[route] = Path(img)
            method, scale = "image", 1
        else:
            if not base_url:
                print("error: give --url or --image", file=sys.stderr)
                return 2
            scale = 2
            routes = args.routes or ["/"]
            targets = []
            for route in routes:
                url = base_url if not args.routes else base_url.rstrip("/") + route
                targets.append((route, url))
            used = set()
            try:
                for route, url in targets:
                    for theme in themes:
                        key = f"{route}@dark" if theme_arg == "both" and theme == "dark" else route
                        out = tmp / f"{len(images)}.png"
                        used.add(capture.capture(url, out, viewport, theme, scale=scale,
                                                 method=args.method, full=args.full))
                        images[key] = out
                if args.measure:
                    measures = {"measure": capture.measure(targets[0][1], viewport)}
            except capture.CaptureError as e:
                print(f"error: {e}", file=sys.stderr)
                return 1
            method = "playwright" if "playwright" in used else "chrome"

        if not first:
            for w in store.check_conditions(manifest, viewport, theme_arg, list(images)):
                warn(w)
            v0 = manifest["versions"][0]["images"]
            for route, src in images.items():
                if route in v0:
                    old = store.image_size(store.run_dir(root, run) / v0[route])
                    new = store.image_size(src)
                    if old != new:
                        warn(f"{route} is {new[0]}x{new[1]}; v0 was {old[0]}x{old[1]}.")
        store.ensure_excluded(root)
        if first:
            manifest["viewport"] = list(viewport)
            manifest["theme"] = theme_arg
        if args.url:
            manifest["base_url"] = args.url
        version = store.add_version(root, manifest, args.note, images, method, scale,
                                    measures.get("measure"))
    store.save_run(root, manifest)
    print(f"{version['label']} saved in {store.DIR}/{run} ({method}, {len(images)} image(s))")
    return 0


def load(args):
    """Project root and the manifest of the run named by --run (default: the current branch)."""
    root = repo.find_root(Path.cwd())
    run = store.slug(args.run) if args.run else store.default_run(root)
    return root, store.load_run(root, run)


def version_index(text: str, count: int) -> int:
    t = text.lower()
    t = t[1:] if t.startswith("v") else t
    if not t.isdigit():
        raise UsageError(f"a version is a number such as 2 or v2, not {text!r}")
    if int(t) >= count:
        raise UsageError(f"there is no v{int(t)}; this run has v0 to v{count - 1}")
    return int(t)


def choose(manifest: dict, a, b, route):
    """Resolve A, B and the route from the arguments, or raise UsageError."""
    versions = manifest["versions"]
    if len(versions) < 2:
        raise UsageError(f"comparing needs two versions; run {manifest['run']!r} has {len(versions)}. "
                         "Save another with snap first.")
    if a is None:
        a, b = len(versions) - 2, len(versions) - 1
    elif b is None:
        raise UsageError("give two versions, such as 0 2, or none for the latest two")
    else:
        a, b = version_index(a, len(versions)), version_index(b, len(versions))
    if a == b:
        raise UsageError("pick two different versions")
    if route is None:
        route = page.default_route(manifest, b)
    elif route not in manifest["routes"]:
        raise UsageError(f"no route {route} in this run; it has {', '.join(manifest['routes'])}")
    return a, b, route


def open_file(path: Path) -> None:
    opener = "open" if sys.platform == "darwin" else "xdg-open"
    if shutil.which(opener):
        subprocess.Popen([opener, str(path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def cmd_show(args) -> int:
    root, manifest = load(args)
    a, b, route = choose(manifest, args.a, args.b, args.route)
    path = page.build_page(root, manifest, a, b, route)
    print(path)
    if not args.no_open:
        open_file(path)
    return 0


def cmd_embed(args) -> int:
    root, manifest = load(args)
    a, b, route = choose(manifest, args.a, args.b, args.route)
    for v in (a, b):
        if route not in manifest["versions"][v]["images"]:
            raise UsageError(f"v{v} has no capture of {route}")
    out = Path(args.out) if args.out else store.run_dir(root, manifest["run"]) / f"embed-v{a}-v{b}"
    print(page.build_embed(root, manifest, a, b, route, out))
    return 0


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    commands = {"snap": cmd_snap, "show": cmd_show, "embed": cmd_embed}
    try:
        return commands[args.cmd](args)
    except UsageError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
