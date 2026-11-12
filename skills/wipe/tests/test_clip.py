import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import support
import clip
import store
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


class ReceiptTests(unittest.TestCase):
    A = {"transfer_kb": 420.0, "requests": 40, "dom_nodes": 900, "lcp_ms": 1200, "host": "localhost:3000", "runs": 3}

    def manifest(self, first, last):
        return {"versions": [{"measure": first}, {"measure": None}, {"measure": last}]}

    def test_receipt_rows_direction(self):
        b = dict(self.A, transfer_kb=310.0, dom_nodes=905, lcp_ms=1500, requests=40)
        rows = {r[0]: r for r in clip.receipt_rows(self.A, b)}
        self.assertEqual(rows["Transfer"][1:], ("420 KB", "310 KB", -1))
        self.assertEqual(rows["DOM nodes"][3], 0)
        self.assertEqual(rows["LCP"][1:], ("1200 ms", "1500 ms", 1))
        self.assertEqual(rows["Requests"][3], 0)

    def test_receipt_thresholds(self):
        b = dict(self.A, transfer_kb=410.0, requests=38, lcp_ms=1230)
        rows = {r[0]: r[3] for r in clip.receipt_rows(self.A, b)}
        self.assertEqual((rows["Transfer"], rows["Requests"], rows["LCP"]), (0, -1, 0))
        self.assertEqual(clip.receipt_rows({"transfer_kb": 4.25}, {"transfer_kb": 3.1})[0][1:], ("4.2 KB", "3.1 KB", -1))

    def test_receipt_zero_values(self):
        rows = clip.receipt_rows({"transfer_kb": 0, "lcp_ms": 0, "requests": 0},
                                 {"transfer_kb": 0, "lcp_ms": 0, "requests": 0})
        self.assertEqual([r[3] for r in rows], [0, 0, 0])
        rows = {r[0]: r[3] for r in clip.receipt_rows({"transfer_kb": 0, "lcp_ms": 0}, {"transfer_kb": 5, "lcp_ms": 100})}
        self.assertEqual(rows, {"Transfer": 1, "LCP": 1})

    def test_receipt_missing_measure(self):
        problem = clip.receipt_problem(self.manifest(self.A, None), [0, 2])
        self.assertIn("v2", problem)
        self.assertIn("v0", clip.receipt_problem(self.manifest(None, self.A), [0, 2]))
        self.assertIsNone(clip.receipt_problem(self.manifest(self.A, self.A), [0, 2]))

    def test_receipt_host_mismatch(self):
        problem = clip.receipt_problem(self.manifest(self.A, dict(self.A, host="example.com")), [0, 2])
        self.assertEqual(problem, "versions were measured on different hosts")

    def test_receipt_ignores_port(self):
        other = dict(self.A, host="localhost:5173")
        self.assertIsNone(clip.receipt_problem(self.manifest(self.A, other), [0, 2]))
        far = dict(self.A, host="example.com")
        self.assertEqual(clip.receipt_problem(self.manifest(self.A, far), [0, 2]),
                         "versions were measured on different hosts")
        self.assertIsNone(clip.receipt_problem(self.manifest(far, dict(far, host="example.com:8443")), [0, 2]))

    def test_receipt_one_sided_production(self):
        prod = dict(self.A, production=True)
        self.assertEqual(clip.receipt_problem(self.manifest(self.A, prod), [0, 2]),
                         "only one version was marked as a production build")
        self.assertIsNone(clip.receipt_problem(self.manifest(prod, prod), [0, 2]))

    def test_receipt_footer_production(self):
        self.assertEqual(clip.receipt_footer("example.com", True), "example.com · production build")
        self.assertEqual(clip.receipt_footer("localhost:3000", True), "localhost:3000 · production build")
        self.assertEqual(clip.receipt_footer("localhost:3000", False), "localhost:3000 · dev server")
        self.assertEqual(clip.receipt_footer("example.com", False), "example.com")

    def test_receipt_route_must_be_in_clip(self):
        a = dict(self.A, route="/pricing")
        m = self.manifest(a, a)
        self.assertIsNone(clip.receipt_problem(m, [0, 2], ["/", "/pricing"]))
        self.assertEqual(clip.receipt_problem(m, [0, 2], ["/"]),
                         "the receipt measured /pricing, which this clip doesn't show")
        self.assertIsNone(clip.receipt_problem(self.manifest(self.A, self.A), [0, 2], ["/"]))

    def test_receipt_footer_names_route_and_all_dev_hosts(self):
        self.assertEqual(clip.receipt_footer("localhost:3000", False, "/pricing"),
                         "/pricing · localhost:3000 · dev server")
        for host in ("0.0.0.0:3000", "[::1]:3000", "::1", "0.0.0.0"):
            self.assertIn("dev server", clip.receipt_footer(host), host)

    def test_receipt_card_uses_last_version_host(self):
        first = dict(self.A, host="localhost:49999", route="/")
        last = dict(self.A, host="localhost:3000", route="/")
        card = clip.receipt_card_data(first, last)
        self.assertIn("localhost:3000", card[1])
        self.assertNotIn("49999", card[1])

    def test_receipt_dev_label(self):
        self.assertIn("dev server", clip.receipt_footer("localhost:3000"))
        self.assertIn("dev server", clip.receipt_footer("127.0.0.1:8080"))
        self.assertIn("dev server", clip.receipt_footer("app.local"))
        self.assertNotIn("dev server", clip.receipt_footer("example.com"))
        self.assertEqual(clip.receipt_footer("local file"), "local file")


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
        rows = clip.receipt_rows(ReceiptTests.A, dict(ReceiptTests.A, transfer_kb=310.0))
        img = clip.compose(clip.Frame("receipt", "/", 0, 1, 1.0, 0.0), shots, layout, fonts, notes,
                           receipt=(rows, "localhost:3000 \u00b7 dev server"))
        self.assertEqual(img.size, (1600, 900))
        self.assertIn((0x3e, 0xcf, 0x8e), {c for _, c in img.getcolors(1 << 20)})


class ClipCliTests(support.TempProject):
    def make_run(self, count, routes=("/",)):
        m = store.load_run(self.root, "x")
        for i in range(count):
            images = {r: write_png(self.root / f"s{i}-{n}.png", 64, 40, (i * 80, 120, 200 - i * 60))
                      for n, r in enumerate(routes)}
            store.add_version(self.root, m, f"pass {i}", images, "chrome", 2)
        store.save_run(self.root, m)
        return m

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

    def stub_ffmpeg(self, body):
        """Put a fake ffmpeg alone on PATH."""
        bin_dir = self.root / "stub-bin"
        bin_dir.mkdir()
        stub = bin_dir / "ffmpeg"
        stub.write_text("#!/bin/sh\n" + body + "\n", encoding="utf-8")
        stub.chmod(0o755)
        return mock.patch.dict(os.environ, {"PATH": str(bin_dir)})

    def test_clip_routes_without_slash(self):
        self.make_run(2, routes=("/pricing",))
        with mock.patch.dict(os.environ, {"PATH": str(self.root)}):  # No ffmpeg: stops at the page.
            code, _, err = self.run_main("clip", "--run", "x", "--routes", "pricing")
        self.assertEqual(code, 3, err)

    def assert_failed_cleanly(self, code, err):
        self.assertEqual(code, 1)
        self.assertIn("error:", err)
        self.assertNotIn("Traceback", err)
        run = store.run_dir(self.root, "x")
        self.assertFalse((run / "clip.mp4").exists())
        self.assertFalse((run / "clip.gif").exists())

    @unittest.skipUnless(HAS_PIL, "needs Pillow")
    def test_ffmpeg_failure_leaves_no_clip(self):
        self.make_run(2)
        # Writes a partial output (its last argument), then fails.
        with self.stub_ffmpeg('for a; do last="$a"; done; echo partial > "$last"; exit 1'), \
                mock.patch.object(clip, "FPS", 2):
            code, _, err = self.run_main("clip", "--run", "x")
        self.assert_failed_cleanly(code, err)
        self.assertIn("ffmpeg failed making clip.mp4", err)

    @unittest.skipUnless(HAS_PIL, "needs Pillow")
    def test_failed_render_keeps_the_previous_clip(self):
        self.make_run(2)
        run = store.run_dir(self.root, "x")
        for name in ("clip.mp4", "clip.gif"):
            (run / name).write_text("old")
        with self.stub_ffmpeg('for a; do last="$a"; done; echo partial > "$last"; exit 1'), \
                mock.patch.object(clip, "FPS", 2):
            code, _, _ = self.run_main("clip", "--run", "x")
        self.assertEqual(code, 1)
        self.assertEqual([(run / n).read_text() for n in ("clip.mp4", "clip.gif")], ["old", "old"])
        self.assertEqual(sorted(p.name for p in run.iterdir() if "clip" in p.name), ["clip.gif", "clip.mp4"])

    @unittest.skipUnless(HAS_PIL, "needs Pillow")
    def test_compose_failure_kills_ffmpeg(self):
        self.make_run(2)
        procs = []
        real_popen = subprocess.Popen

        def popen(*args, **kwargs):
            procs.append(real_popen(*args, **kwargs))
            return procs[-1]

        # The stub reads frames until stdin closes, then writes an output, as ffmpeg would.
        with self.stub_ffmpeg('for a; do last="$a"; done; /bin/cat > "$last"'), \
                mock.patch.object(clip, "FPS", 2), \
                mock.patch.object(clip.subprocess, "Popen", side_effect=popen), \
                mock.patch.object(clip, "compose", side_effect=[mock.DEFAULT, KeyError("boom")],
                                  wraps=clip.compose):
            code, _, err = self.run_main("clip", "--run", "x")
        self.assert_failed_cleanly(code, err)
        self.assertIn("KeyError", err)
        self.assertEqual(len(procs), 1)
        self.assertLess(procs[0].returncode, 0)  # Killed, and reaped (returncode is set).

    @unittest.skipUnless(HAS_PIL and HAS_FFMPEG, "needs Pillow and ffmpeg")
    def test_receipt_problem_renders_without_card(self):
        self.make_run(2)
        with mock.patch.object(clip, "FPS", 4), mock.patch.object(clip, "plan_frames",
                                                                  wraps=clip.plan_frames) as plan:
            code, _, err = self.run_main("clip", "--run", "x", "--receipt", "--gif-width", "320")
        self.assertEqual(code, 0, err)
        self.assertIn("note: no receipt card: v0 has no measurements", err)
        self.assertFalse(plan.call_args.kwargs["receipt"])

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
