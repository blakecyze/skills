import importlib.util
import io
import os
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

import support  # noqa: F401
import clip
import store
import wipe
from pngs import write_png

HAS_PIL = importlib.util.find_spec("PIL") is not None
HAS_FFMPEG = shutil.which("ffmpeg") is not None
LOOP = 1.7 + 1.1 + 1.7 + 1.8 + 1.4 + 0.7


class TimelineTests(unittest.TestCase):
    def test_ease_bounds(self):
        self.assertEqual(clip.ease(0), 0)
        self.assertEqual(clip.ease(1), 1)
        self.assertAlmostEqual(clip.ease(0.5), 0.5)
        samples = [clip.ease(i / 100) for i in range(101)]
        self.assertEqual(samples, sorted(samples))

    def test_plan_loop_seamless(self):
        frames = clip.plan_frames([0, 1, 2], ["/"])
        first, last = frames[0], frames[-1]
        self.assertEqual((first.kind, first.a, first.p), ("wipe", 0, 0))
        self.assertEqual((last.kind, last.a, last.p), ("wipe", 0, 0))
        self.assertAlmostEqual(len(frames) / 30, LOOP, delta=0.1)

    def test_plan_no_loop_ends_on_last(self):
        frames = clip.plan_frames([0, 1, 2], ["/"], loop=False)
        self.assertEqual((frames[-1].b, frames[-1].p), (2, 1))
        self.assertAlmostEqual(len(frames) / 30, 1.7 + 1.1 + 1.7 + 1.8, delta=0.1)

    def test_plan_open_moving(self):
        frames = clip.plan_frames([0, 1], ["/"], open_moving=True)
        self.assertAlmostEqual(frames[0].p, 0.22, delta=0.01)
        self.assertGreater(frames[1].p, frames[0].p)

    def test_plan_routes_sequence(self):
        frames = clip.plan_frames([0, 1, 2], ["/a", "/b"])
        routes = [f.route for f in frames]
        last_a = max(i for i, r in enumerate(routes) if r == "/a")
        first_b = routes.index("/b")
        self.assertLess(last_a, first_b)
        # The return sweep (handle moving right to left) happens once, at the end.
        sweeps = [i for i in range(1, len(frames)) if frames[i].p < frames[i - 1].p
                  and frames[i].a == frames[i - 1].a]
        self.assertTrue(sweeps)
        self.assertTrue(all(frames[i].route == "/b" for i in sweeps))
        self.assertEqual(len({(frames[i].a, frames[i].b) for i in sweeps}), 1)
        self.assertGreater(min(sweeps), first_b)

    def test_plan_outro_receipt(self):
        frames = clip.plan_frames([0, 1], ["/"], outro=True, receipt=True)
        kinds = [f.kind for f in frames]
        self.assertEqual(kinds[-1], "outro")
        first_receipt, first_outro = kinds.index("receipt"), kinds.index("outro")
        self.assertLess(first_receipt, first_outro)
        self.assertEqual(set(kinds[first_receipt:first_outro]), {"receipt"})
        self.assertEqual(set(kinds[first_outro:]), {"outro"})
        wipes = [f for f in frames if f.kind == "wipe"]
        self.assertEqual((wipes[-1].a, wipes[-1].p), (0, 0))  # The loop return came first.
        self.assertAlmostEqual(kinds.count("receipt") / 30, 2.4, delta=0.05)
        self.assertAlmostEqual(kinds.count("outro") / 30, 1.6, delta=0.05)

    def test_plan_scroll_pans_down_and_back(self):
        frames = clip.plan_frames([0, 1], ["/"], loop=False, scroll_routes={"/"})
        scrolls = [f.scroll for f in frames]
        self.assertEqual(scrolls[0], 0)
        self.assertEqual(max(scrolls), 1)
        self.assertEqual(scrolls[-1], 0)
        self.assertTrue(all(f.p == 1 for f in frames if f.scroll > 0))

    def test_parse_hex(self):
        self.assertEqual(clip.parse_hex("#0e0e0d"), (14, 14, 13))
        self.assertEqual(clip.parse_hex("fff"), (255, 255, 255))
        with self.assertRaises(ValueError):
            clip.parse_hex("#12345")


@unittest.skipUnless(HAS_PIL, "needs Pillow")
class ComposeTests(unittest.TestCase):
    def test_compose_pads_shorter_shot(self):
        from PIL import Image
        with tempfile.TemporaryDirectory() as tmp:
            short = Image.new("RGB", (100, 80), (255, 0, 0))
            short.paste((0, 0, 255), (0, 40, 100, 80))  # Top half red, bottom half blue.
            short.save(Path(tmp) / "short.png")
            write_png(Path(tmp) / "tall.png", 100, 120, (0, 200, 0))
            layout = clip.make_layout((14, 14, 13))
            shots = clip.prepare_shots({(0, "/"): Path(tmp) / "short.png",
                                        (1, "/"): Path(tmp) / "tall.png"}, layout)
        a, b = shots[(0, "/")], shots[(1, "/")]
        self.assertEqual(a.size, b.size)
        self.assertEqual(a.width, layout.win_w)
        self.assertEqual(b.height, round(120 * layout.win_w / 100))
        # Scaled by width, not stretched: red ends near 466 px, so 600 px is blue.
        self.assertEqual(a.getpixel((10, 600)), (0, 0, 255))
        fonts = clip.load_fonts()
        notes = {0: "before", 1: "after"}
        for frame in (clip.Frame("wipe", "/", 0, 1, 0.5, 0.0), clip.Frame("wipe", "/", 0, 1, 1.0, 1.0),
                      clip.Frame("outro", "/", 0, 1, 0.5, 0.0), clip.Frame("receipt", "/", 0, 1, 0.5, 0.0)):
            img = clip.compose(frame, shots, layout, fonts, notes, outro="npx skills add")
            self.assertEqual(img.size, (1600, 900))


class ClipCliTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name).resolve()
        cwd = Path.cwd()
        os.chdir(self.root)
        self.addCleanup(os.chdir, cwd)

    def make_run(self, count, routes=("/",)):
        m = store.load_run(self.root, "x")
        for i in range(count):
            images = {r: write_png(self.root / f"s{i}-{n}.png", 64, 40, (i * 80, 120, 200 - i * 60))
                      for n, r in enumerate(routes)}
            store.add_version(self.root, m, f"pass {i}", images, "chrome", 2)
        store.save_run(self.root, m)
        return m

    def run_main(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = wipe.main(list(argv))
        return code, out.getvalue(), err.getvalue()

    def test_clip_needs_two(self):
        self.make_run(1)
        code, _, err = self.run_main("clip", "--run", "x")
        self.assertEqual(code, 2)
        self.assertIn("two versions", err)
        self.assertNotIn("Traceback", err)

    def test_clip_bad_arguments(self):
        self.make_run(3)
        for argv, text in ((["--versions", "1"], "two versions"), (["--versions", "0,7"], "no v7"),
                           (["--routes", "/nope"], "no route /nope"), (["--ground", "red"], "--ground")):
            code, _, err = self.run_main("clip", "--run", "x", *argv)
            self.assertEqual(code, 2, argv)
            self.assertIn(text, err)

    def test_clip_without_ffmpeg(self):
        self.make_run(2)
        empty = self.root / "empty-bin"
        empty.mkdir()
        # PIL blocked too: the no-ffmpeg path must work with the standard library alone.
        with mock.patch.dict(os.environ, {"PATH": str(empty)}), mock.patch.dict(sys.modules, {"PIL": None}):
            code, _, err = self.run_main("clip", "--run", "x")
        self.assertEqual(code, 3)
        self.assertIn("no video was made", err)
        self.assertTrue((store.run_dir(self.root, "x") / "index.html").exists())
        self.assertFalse((store.run_dir(self.root, "x") / "clip.mp4").exists())

    def test_clip_without_pillow(self):
        self.make_run(2)
        with mock.patch.object(clip, "find_ffmpeg", return_value="/bin/ffmpeg"), \
                mock.patch.dict(sys.modules, {"PIL": None}):
            code, _, err = self.run_main("clip", "--run", "x")
        self.assertEqual(code, 3)
        self.assertIn("venv", err)

    @unittest.skipUnless(HAS_PIL and HAS_FFMPEG, "needs Pillow and ffmpeg")
    def test_render_outputs(self):
        self.make_run(3)
        with mock.patch.object(clip, "FPS", 4):
            code, out, err = self.run_main("clip", "--run", "x", "--versions", "v0,1,2", "--gif-width", "320")
        self.assertEqual(code, 0, err)
        self.assertEqual(err, "")
        run = store.run_dir(self.root, "x")
        self.assertTrue((run / "clip.mp4").stat().st_size > 0)
        self.assertEqual((run / "clip.gif").read_bytes()[:6], b"GIF89a")
        self.assertIn(str(run / "clip.gif"), out)


if __name__ == "__main__":
    unittest.main()
