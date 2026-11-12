"""Before/after clips: timeline, frame composition and encoding.

Frames are drawn with Pillow and piped as raw RGB into ffmpeg, which writes the MP4; the GIF is
made from the MP4. Pillow is imported inside the functions that draw, so importing this module
needs the standard library only.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from collections import namedtuple
from pathlib import Path

import store

Frame = namedtuple("Frame", "kind route a b p scroll")
Layout = namedtuple("Layout", "w h x y win_w win_h radius ground base mask")
Fonts = namedtuple("Fonts", "label ver note title row small")

W, H, FPS = 1600, 900, 30
WIN_H, WIN_Y, RADIUS = 728, 44, 18
WIN_W = round(WIN_H * 1.6)

# Timeline, in seconds.
WIPE, HOLD, HOLD_LAST = 1.7, 1.1, 1.8
RETURN, RETURN_HOLD = 1.4, 0.7
OPEN_MOVING_P = 0.22
OUTRO, RECEIPT = 1.6, 2.4
# A tall page on its last hold: still, pan down, still, pan back, still.
SCROLL_STEPS = ((0.4, 0, 0), (2.2, 0, 1), (0.8, 1, 1), (1.4, 1, 0), (0.4, 0, 0))

LABEL_MIN = 230  # A side narrower than this hides its label.
WHITE = (250, 248, 244)
BETTER, WORSE, SAME = (0x3e, 0xcf, 0x8e), (0xff, 0x5a, 0x4f), (128, 128, 124)
# Receipt metrics: manifest key, label, unit. Lower is better for all of them.
METRICS = (("transfer_kb", "Transfer", "kb"), ("requests", "Requests", "count"),
           ("dom_nodes", "DOM nodes", "count"), ("lcp_ms", "LCP", "ms"))
GIF_FILTER = ("fps=12,scale={w}:-1:flags=lanczos,split[s0][s1];[s0]palettegen=stats_mode=diff:max_colors=160[p];"
              "[s1][p]paletteuse=dither=bayer:bayer_scale=4:diff_mode=rectangle")
FONT_DIRS = (Path.home() / "Library/Fonts", Path("/Library/Fonts"), Path("/usr/share/fonts"))


class ClipError(Exception):
    """Rendering failed (ffmpeg error). The message is ready to print."""


def find_ffmpeg():
    return shutil.which("ffmpeg")


def has_pillow() -> bool:
    try:
        import PIL  # noqa: F401
    except ImportError:
        return False
    return True


def parse_hex(text: str) -> tuple:
    m = re.fullmatch(r"#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})", text.strip())
    if not m:
        raise ValueError(f"a colour looks like #0e0e0d, not {text!r}")
    h = m.group(1)
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# Timeline

def ease(t: float) -> float:
    """Cubic ease-in-out on [0, 1]."""
    t = max(0.0, min(1.0, t))
    return 4 * t ** 3 if t < 0.5 else 1 - (-2 * t + 2) ** 3 / 2


def _count(seconds, fps):
    return max(1, round(seconds * fps))


def _ramp(seconds, fps, start=0.0, end=1.0, t0=0.0):
    """Eased values from start to end, beginning at t0 of the curve, over the given seconds."""
    n = _count(seconds, fps)
    if n == 1:
        return [end]
    return [start + (end - start) * ease(t0 + (1 - t0) * i / (n - 1)) for i in range(n)]


def _inverse_ease(p):
    lo, hi = 0.0, 1.0
    for _ in range(40):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if ease(mid) < p else (lo, mid)
    return lo


def plan_frames(versions: list, routes: list, fps: int = 30, loop: bool = True, open_moving: bool = False,
                outro: bool = False, receipt: bool = False, scroll_routes=()) -> list:
    """Every frame of the clip, in order.

    Each route wipes through the versions in turn: the handle sweeps left to right, revealing the
    next version on its left, then holds. With loop, the clip ends by sweeping from the last version
    back to the first, so a looping GIF has no seam. A route in scroll_routes pans down and back on
    its last hold. Receipt then outro cards come last.
    """
    frames = []
    first, last = versions[0], versions[-1]
    for r, route in enumerate(routes):
        pairs = list(zip(versions, versions[1:]))
        for i, (a, b) in enumerate(pairs):
            t0 = _inverse_ease(OPEN_MOVING_P) if open_moving and r == 0 and i == 0 else 0.0
            frames += [Frame("wipe", route, a, b, p, 0.0) for p in _ramp(WIPE * (1 - t0), fps, t0=t0)]
            if i < len(pairs) - 1:
                frames += [Frame("wipe", route, a, b, 1.0, 0.0)] * _count(HOLD, fps)
            elif route in scroll_routes:
                for seconds, s0, s1 in SCROLL_STEPS:
                    values = _ramp(seconds, fps, s0, s1) if s0 != s1 else [float(s0)] * _count(seconds, fps)
                    frames += [Frame("wipe", route, a, b, 1.0, s) for s in values]
            else:
                frames += [Frame("wipe", route, a, b, 1.0, 0.0)] * _count(HOLD_LAST, fps)
    route = routes[-1]
    if loop:
        frames += [Frame("wipe", route, first, last, p, 0.0) for p in _ramp(RETURN, fps, 1.0, 0.0)]
        frames += [Frame("wipe", route, first, last, 0.0, 0.0)] * _count(RETURN_HOLD, fps)
    for kind, seconds, wanted in (("receipt", RECEIPT, receipt), ("outro", OUTRO, outro)):
        if wanted:
            n = _count(seconds, fps)
            frames += [Frame(kind, route, first, last, i / max(n - 1, 1), 0.0) for i in range(n)]
    return frames


# Drawing

def make_layout(ground: tuple):
    """Canvas, window geometry, and the pre-drawn ground (with the window's shadow) and window mask."""
    from PIL import Image, ImageDraw, ImageFilter
    x = (W - WIN_W) // 2
    base = Image.new("RGB", (W, H), ground)
    shadow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(shadow).rounded_rectangle(
        (x + 10, WIN_Y + 26, x + WIN_W - 10, WIN_Y + WIN_H + 26), RADIUS, fill=190)
    base.paste((0, 0, 0), (0, 0), shadow.filter(ImageFilter.GaussianBlur(34)))
    mask = Image.new("L", (WIN_W, WIN_H), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, WIN_W - 1, WIN_H - 1), RADIUS, fill=255)
    return Layout(W, H, x, WIN_Y, WIN_W, WIN_H, RADIUS, ground, base, mask)


def _font_files():
    """(semibold, medium) paths: Inter, then SF, then DejaVu Sans. Either may be None."""
    for d in FONT_DIRS:
        if not d.is_dir():
            continue
        semi = next(d.rglob("Inter-SemiBold.[ot]tf"), None)
        medium = next(d.rglob("Inter-Medium.[ot]tf"), None)
        if semi or medium:
            return semi or medium, medium or semi
    sf = Path("/System/Library/Fonts/SFNS.ttf")
    if sf.is_file():
        return sf, sf
    root = Path("/usr/share/fonts")
    if root.is_dir():
        bold = next(root.rglob("DejaVuSans-Bold.ttf"), None)
        book = next(root.rglob("DejaVuSans.ttf"), None)
        if bold or book:
            return bold or book, book or bold
    return None, None


def load_fonts():
    from PIL import ImageFont

    def get(path, size, variation):
        if path is None:
            try:
                return ImageFont.load_default(size)
            except TypeError:  # Pillow before 10.1 has no scalable default.
                return ImageFont.load_default()
        font = ImageFont.truetype(str(path), size)
        if path.name == "SFNS.ttf":
            try:
                font.set_variation_by_name(variation)
            except (OSError, ValueError):
                pass
        return font

    semi, medium = _font_files()
    return Fonts(label=get(semi, 15, "Semibold"), ver=get(semi, 14, "Semibold"),
                 note=get(medium, 14, "Medium"), title=get(semi, 30, "Semibold"),
                 row=get(semi, 34, "Semibold"), small=get(medium, 24, "Medium"))


def prepare_shots(images: dict, layout) -> dict:
    """Scale each capture to the window's width and pad (never stretch) so a route's versions match.

    images maps (version, route) to a PNG path. Shorter captures are top-aligned and padded with
    their own bottom-left colour, to the tallest capture of the route or the window, if taller.
    """
    from PIL import Image
    scaled = {}
    for key, path in images.items():
        with Image.open(path) as src:
            h = max(1, round(src.height * layout.win_w / src.width))
            scaled[key] = src.convert("RGB").resize((layout.win_w, h), Image.LANCZOS)
    heights = {}
    for (_, route), im in scaled.items():
        heights[route] = max(heights.get(route, layout.win_h), im.height)
    shots = {}
    for key, im in scaled.items():
        target = heights[key[1]]
        if im.height < target:
            padded = Image.new("RGB", (layout.win_w, target), im.getpixel((0, im.height - 1)))
            padded.paste(im, (0, 0))
            im = padded
        shots[key] = im
    return shots


def _note(v, notes):
    note = notes.get(v) or ""
    return note[:47].rstrip() + "…" if len(note) > 48 else note


def _label(v, notes):
    note = _note(v, notes)
    return f"v{v} · {note}" if note else f"v{v}"


def _pill(d, x, y, text, font, right=False):
    """A dark label pill with its left edge (or right edge, if right) at x."""
    w, h = _pill_width(d, text, font), 34
    if right:
        x -= w
    d.rounded_rectangle((x, y, x + w, y + h), h // 2, fill=(20, 20, 18, 215))
    d.text((x + 14, y + h / 2), text, font=font, fill=WHITE, anchor="lm")


def _pill_width(d, text, font):
    l, _, r, _ = d.textbbox((0, 0), text, font=font)
    return r - l + 28


def _handle(d, x, layout):
    top, bottom = layout.y, layout.y + layout.win_h
    d.rectangle((x - 3, top, x + 3, bottom), fill=(0, 0, 0, 50))
    d.rectangle((x - 1, top, x + 1, bottom), fill=(255, 255, 255, 240))
    cy = top + layout.win_h // 2
    d.ellipse((x - 21, cy - 19, x + 21, cy + 23), fill=(0, 0, 0, 60))
    d.ellipse((x - 20, cy - 20, x + 20, cy + 20), fill=(255, 255, 255, 255))
    for s in (-1, 1):
        d.line([(x + s * 4, cy - 6), (x + s * 10, cy), (x + s * 4, cy + 6)], fill=(30, 30, 28), width=3,
               joint="curve")


def _strip(d, current, layout, fonts, notes):
    """The row of versions under the window, with the current one highlighted."""
    sy = layout.y + layout.win_h + 46
    items = [(f"v{v}", _note(v, notes), v) for v in notes]
    gap = 22
    tags = [d.textlength(tag, font=fonts.ver) + 30 for tag, _, _ in items]
    ws = [w + (8 + d.textlength(note, font=fonts.note) if note else 0) for w, (_, note, _) in zip(tags, items)]
    with_notes = sum(ws) + gap * (len(items) - 1) <= layout.w - 80  # Too many to fit: tags only.
    if not with_notes:
        ws = tags
    x = (layout.w - sum(ws) - gap * (len(items) - 1)) / 2
    for (tag, note, v), w in zip(items, ws):
        on = v == current
        if on:
            d.rounded_rectangle((x, sy - 17, x + w, sy + 17), 17, fill=(255, 255, 255, 30))
        d.text((x + 15, sy), tag, font=fonts.ver, fill=(255, 255, 255, 255 if on else 110), anchor="lm")
        if with_notes and note:
            d.text((x + 15 + d.textlength(tag, font=fonts.ver) + 8, sy), note, font=fonts.note,
                   fill=(255, 255, 255, 200 if on else 80), anchor="lm")
        x += w + gap


def _outro_card(frame, layout, fonts, text):
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (layout.w, layout.h), layout.ground)
    alpha = round(255 * ease(min(1.0, frame.p / 0.25)))  # Fades in over the first 0.4 s.
    d = ImageDraw.Draw(img, "RGBA")
    d.text((layout.w / 2, layout.h / 2), text or "", font=fonts.title, fill=WHITE + (alpha,), anchor="mm")
    return img


def _show(value, unit):
    if unit == "kb":
        return f"{value:.1f} KB" if value < 10 else f"{value:.0f} KB"
    return f"{value:.0f} ms" if unit == "ms" else f"{value:.0f}"


def receipt_rows(first: dict, last: dict) -> list:
    """(label, before text, after text, direction) per metric both versions have.

    Direction is -1 for better, 0 for no change and 1 for worse; lower is better for every metric.
    A change under 3% is no change, as is any change under 1 for counts.
    """
    rows = []
    for key, label, unit in METRICS:
        a, b = first.get(key), last.get(key)
        if a is None or b is None:
            continue
        delta = b - a
        small = abs(delta) < 0.03 * abs(a) or (unit == "count" and abs(delta) < 1)
        rows.append((label, _show(a, unit), _show(b, unit), 0 if small else (-1 if delta < 0 else 1)))
    return rows


def receipt_problem(manifest: dict, versions: list) -> str | None:
    """Why the first and last chosen versions can't be compared, or None if they can."""
    ends = (versions[0], versions[-1])
    for v in ends:
        if not manifest["versions"][v].get("measure"):
            return f"v{v} has no measurements; snap it with --measure to get a receipt"
    first, last = (manifest["versions"][v]["measure"] for v in ends)
    if first.get("host") != last.get("host"):
        return "versions were measured on different hosts"
    return None


def receipt_footer(host: str) -> str:
    name = host.rsplit(":", 1)[0] if re.search(r":\d+$", host) else host
    dev = name in ("localhost", "127.0.0.1") or name.endswith(".local")
    return f"{host} · dev server" if dev else host


def _receipt_card(frame, layout, fonts, receipt):
    """A centred card of metric rows: label, before to after, and a coloured direction triangle."""
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (layout.w, layout.h), layout.ground)
    rows, footer = receipt if receipt else ([], "")
    alpha = round(255 * ease(min(1.0, frame.p / 0.2)))
    d = ImageDraw.Draw(img, "RGBA")
    row_h, pad = 96, 52
    cw = 960
    ch = pad * 2 + 70 + row_h * len(rows) + (56 if footer else 0)
    x, y = (layout.w - cw) // 2, (layout.h - ch) // 2
    d.rounded_rectangle((x, y, x + cw, y + ch), layout.radius, fill=(255, 255, 255, round(14 * alpha / 255)),
                        outline=(255, 255, 255, round(22 * alpha / 255)), width=1)
    ink = lambda c, a=255: tuple(c) + (round(a * alpha / 255),)  # noqa: E731
    left, right = x + pad, x + cw - pad
    d.text((left, y + pad + 16), f"v{frame.a} \u2192 v{frame.b}", font=fonts.small, fill=ink(WHITE, 130), anchor="lm")
    top = y + pad + 70
    for i, (label, before, after, direction) in enumerate(rows):
        cy = top + i * row_h + row_h // 2
        d.line((left, top + i * row_h, right, top + i * row_h), fill=ink(WHITE, 24), width=1)
        colour = SAME if direction == 0 else (BETTER if direction < 0 else WORSE)
        d.text((left, cy), label, font=fonts.small, fill=ink(WHITE, 170), anchor="lm")
        tx = right - 12
        if direction:  # Triangle: up for worse (higher), down for better (lower).
            pts = [(tx - 12, cy + 9), (tx + 12, cy + 9), (tx, cy - 11)] if direction > 0 else \
                  [(tx - 12, cy - 9), (tx + 12, cy - 9), (tx, cy + 11)]
        else:
            pts = [(tx - 12, cy), (tx + 12, cy)]
        if direction:
            d.polygon(pts, fill=ink(colour))
        else:
            d.line(pts, fill=ink(colour), width=4)
        ax = tx - 54
        d.text((ax, cy), after, font=fonts.row, fill=ink(WHITE), anchor="rm")
        after_w = d.textlength(after, font=fonts.row)
        sx = ax - after_w - 30
        d.line((sx - 22, cy, sx, cy), fill=ink(WHITE, 90), width=2)
        d.line([(sx - 8, cy - 7), (sx, cy), (sx - 8, cy + 7)], fill=ink(WHITE, 90), width=2, joint="curve")
        d.text((sx - 38, cy), before, font=fonts.row, fill=ink(WHITE, 110), anchor="rm")
    if footer:
        fy = top + len(rows) * row_h
        d.line((left, fy, right, fy), fill=ink(WHITE, 24), width=1)
        d.text((left, fy + 36), footer, font=fonts.small, fill=ink(WHITE, 100), anchor="lm")
    return img


def compose(frame: Frame, shots: dict, layout, fonts, notes: dict, outro: str | None = None,
            receipt: tuple | None = None):
    """One frame as a PIL image. notes maps each chosen version, in clip order, to its note.

    receipt is (rows, footer) for receipt frames."""
    if frame.kind == "outro":
        return _outro_card(frame, layout, fonts, outro)
    if frame.kind == "receipt":
        return _receipt_card(frame, layout, fonts, receipt)
    from PIL import ImageDraw
    sa, sb = shots[(frame.a, frame.route)], shots[(frame.b, frame.route)]
    top = round(frame.scroll * (sa.height - layout.win_h))
    win = sa.crop((0, top, layout.win_w, top + layout.win_h))
    hx = round(frame.p * layout.win_w)
    if hx > 0:
        win.paste(sb.crop((0, top, hx, top + layout.win_h)), (0, 0))
    img = layout.base.copy()
    img.paste(win, (layout.x, layout.y), layout.mask)
    d = ImageDraw.Draw(img, "RGBA")

    # Labels sit in the bottom corners: the newer version left of the handle, the older right.
    y = layout.y + layout.win_h - 52
    left, right = _label(frame.b, notes), _label(frame.a, notes)
    if hx > max(LABEL_MIN, _pill_width(d, left, fonts.label) + 36):
        _pill(d, layout.x + 18, y, left, fonts.label)
    if layout.win_w - hx > max(LABEL_MIN, _pill_width(d, right, fonts.label) + 36):
        _pill(d, layout.x + layout.win_w - 18, y, right, fonts.label, right=True)
    if 0 < frame.p < 1:
        _handle(d, layout.x + hx, layout)
    _strip(d, frame.b if frame.p > 0.5 else frame.a, layout, fonts, notes)
    return img


# Encoding

def _ffmpeg(args, what, feed=None):
    """Run ffmpeg quietly, writing each chunk of feed to its stdin.

    If anything goes wrong on our side (a frame fails to draw, Ctrl-C), ffmpeg is killed and
    reaped, rather than left to finish a truncated file. A failure on ffmpeg's side raises ClipError
    with the last line of its log.
    """
    with tempfile.TemporaryFile() as log:
        quiet = ["-y", "-loglevel", "error"] + ([] if feed is not None else ["-nostdin"])
        proc = subprocess.Popen(["ffmpeg", *quiet, *args], stdout=subprocess.DEVNULL, stderr=log,
                                stdin=subprocess.PIPE if feed is not None else None)
        try:
            if feed is not None:
                try:
                    for chunk in feed:
                        proc.stdin.write(chunk)
                    proc.stdin.close()
                except BrokenPipeError:
                    pass  # ffmpeg stopped early; its exit code and log say why.
            code = proc.wait()
        except BaseException:
            proc.kill()
            proc.wait()
            raise
        finally:
            if proc.stdin and not proc.stdin.closed:  # Unflushed bytes to a dead ffmpeg: ignore.
                try:
                    proc.stdin.close()
                except OSError:
                    pass
        if code:
            log.seek(0)
            message = log.read().decode("utf-8", "replace").strip()
            tail = message.splitlines()[-1] if message else f"exit code {code}"
            raise ClipError(f"ffmpeg failed making {what}: {tail}")


def _frame_bytes(frames, shots, layout, fonts, notes, outro, receipt=None):
    previous, data = None, b""
    for frame in frames:
        if frame != previous:  # Holds repeat a frame; draw it once.
            data = compose(frame, shots, layout, fonts, notes, outro=outro, receipt=receipt).tobytes()
            previous = frame
        yield data


def render(root, manifest: dict, versions: list, routes: list, out_dir: Path, ground: str, loop: bool,
           open_moving: bool, outro_text: str | None, receipt: bool, scroll: bool,
           gif_width: int = 960) -> dict:
    """Render clip.mp4 and clip.gif into out_dir. Returns their paths by kind."""
    layout = make_layout(parse_hex(ground))
    fonts = load_fonts()
    run = store.run_dir(root, manifest["run"])
    images = {(v, r): run / manifest["versions"][v]["images"][r] for v in versions for r in routes}
    shots = prepare_shots(images, layout)
    tall = {r for r in routes if shots[(versions[-1], r)].height > layout.win_h} if scroll else set()
    notes = {v: manifest["versions"][v].get("note") or "" for v in versions}
    card = None
    if receipt:
        first, last = (manifest["versions"][v]["measure"] for v in (versions[0], versions[-1]))
        card = (receipt_rows(first, last), receipt_footer(first.get("host") or ""))
    fps = FPS
    frames = plan_frames(versions, routes, fps=fps, loop=loop, open_moving=open_moving,
                         outro=outro_text is not None, receipt=receipt, scroll_routes=tall)

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    mp4, gif = out_dir / "clip.mp4", out_dir / "clip.gif"
    try:
        _ffmpeg(["-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{layout.w}x{layout.h}", "-r", str(fps),
                 "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", "-preset", "slow",
                 "-movflags", "+faststart", str(mp4)], mp4.name,
                feed=_frame_bytes(frames, shots, layout, fonts, notes, outro_text, card))
        _ffmpeg(["-i", str(mp4), "-vf", GIF_FILTER.format(w=gif_width), "-loop", "0", str(gif)], gif.name)
    except BaseException:
        for f in (mp4, gif):  # Never leave a truncated clip that looks finished.
            f.unlink(missing_ok=True)
        raise
    return {"mp4": mp4, "gif": gif}
