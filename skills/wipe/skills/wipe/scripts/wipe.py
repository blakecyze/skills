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
import clip  # noqa: E402
import page  # noqa: E402
import repo  # noqa: E402
import store  # noqa: E402

PLAYWRIGHT_HELP = ("Needs Playwright. Run: python3 -m venv <temp>/v && <temp>/v/bin/pip install playwright, "
                   "then use <temp>/v/bin/python.")
PILLOW_HELP = ("Needs Pillow. Run: python3 -m venv <temp>/v && <temp>/v/bin/pip install pillow, "
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

    s = sub.add_parser("clip", help="render an MP4 and GIF that wipe through the versions (needs Pillow, ffmpeg)")
    s.add_argument("--run", help="run name (default: current branch)")
    s.add_argument("--versions", help="versions in order, such as 0,2,3 or v0,v2 (default: all)")
    s.add_argument("--routes", help="routes to play one after another, such as /,/pricing "
                                    "(default: the run's first route)")
    s.add_argument("--out", help="folder for clip.mp4 and clip.gif (default: .wipe/<run>)")
    s.add_argument("--ground", default="#0e0e0d", help="background colour (default: #0e0e0d)")
    s.add_argument("--no-loop", action="store_true",
                   help="end on the last version, without the sweep back to the first")
    s.add_argument("--open-moving", action="store_true", help="start with the first wipe already moving")
    s.add_argument("--outro", metavar="TEXT", help="end on a card showing TEXT, such as an install command")
    s.add_argument("--receipt", action="store_true", help="add a card comparing the first and last versions' numbers")
    s.add_argument("--scroll", action="store_true", help="pan down a capture taller than the window on its last hold")
    s.add_argument("--gif-width", type=int, default=960, help="GIF width in pixels (default: 960)")
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


def choose_clip(manifest: dict, versions_arg, routes_arg):
    """Resolve --versions and --routes into lists, or raise UsageError."""
    count = len(manifest["versions"])
    if versions_arg:
        versions = [version_index(t.strip(), count) for t in versions_arg.split(",")]
        if len(set(versions)) != len(versions):
            raise UsageError("--versions lists a version twice")
    else:
        versions = list(range(count))
    if versions_arg and len(versions) < 2:
        raise UsageError(f"a clip needs two versions; --versions names {len(versions)}")
    if len(versions) < 2:
        raise UsageError(f"a clip needs two versions; run {manifest['run']!r} has {count}. "
                         "Save another with snap first.")
    routes = [r.strip() for r in routes_arg.split(",")] if routes_arg else manifest["routes"][:1]
    for route in routes:
        if route not in manifest["routes"]:
            raise UsageError(f"no route {route} in this run; it has {', '.join(manifest['routes'])}")
        for v in versions:
            if route not in manifest["versions"][v]["images"]:
                raise UsageError(f"v{v} has no capture of {route}")
    return versions, routes


def cmd_clip(args) -> int:
    root, manifest = load(args)
    versions, routes = choose_clip(manifest, args.versions, args.routes)
    try:
        clip.parse_hex(args.ground)
    except ValueError as e:
        raise UsageError(f"--ground: {e}")
    if args.gif_width < 16:
        raise UsageError("--gif-width must be at least 16")
    # ffmpeg first: without it the compare page is still useful, and needs no Pillow.
    if not clip.find_ffmpeg():
        path = page.build_page(root, manifest, versions[0], versions[-1], routes[0])
        print(f"ffmpeg not found; no video was made. Compare page: {path}", file=sys.stderr)
        return 3
    if not clip.has_pillow():
        print(f"error: clip {PILLOW_HELP}", file=sys.stderr)
        return 3
    out = Path(args.out) if args.out else store.run_dir(root, manifest["run"])
    try:
        made = clip.render(root, manifest, versions, routes, out, args.ground, loop=not args.no_loop,
                           open_moving=args.open_moving, outro_text=args.outro, receipt=args.receipt,
                           scroll=args.scroll, gif_width=args.gif_width)
    except (clip.ClipError, OSError) as e:  # OSError: a capture missing or unreadable.
        print(f"error: {e}", file=sys.stderr)
        return 1
    for path in made.values():
        print(f"{path} ({path.stat().st_size / 1e6:.2f} MB)")
    size = made["gif"].stat().st_size / 1e6
    if size > 15:
        warn(f"clip.gif is {size:.1f} MB; X takes GIFs up to 15 MB. Try a smaller --gif-width.")
    return 0


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    commands = {"snap": cmd_snap, "show": cmd_show, "embed": cmd_embed, "clip": cmd_clip}
    try:
        return commands[args.cmd](args)
    except UsageError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
