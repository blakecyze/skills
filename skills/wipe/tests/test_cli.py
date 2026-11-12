import io
import json
import subprocess
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

import support  # noqa: F401
import capture
import store
import wipe
from pngs import write_png


class SnapTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name).resolve()
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=self.root, check=True)
        cwd = Path.cwd()
        import os
        os.chdir(self.root)
        self.addCleanup(os.chdir, cwd)

    def run_main(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = wipe.main(list(argv))
        return code, out.getvalue(), err.getvalue()

    def png(self, name, w=100, h=80):
        return str(write_png(self.root / name, w, h, (10, 20, 30)))

    def test_snap_image_twice(self):
        a, b = self.png("a.png"), self.png("b.png")
        self.assertEqual(self.run_main("snap", "--image", a, "--note", "before")[0], 0)
        self.assertEqual(self.run_main("snap", "--image", b, "--note", "after")[0], 0)
        m = store.load_run(self.root, "main")
        self.assertEqual([v["label"] for v in m["versions"]], ["v0", "v1"])
        self.assertEqual(m["versions"][0]["method"], "image")
        self.assertEqual(m["routes"], ["screen"])
        self.assertEqual(m["viewport"], [1280, 800])
        exclude = (self.root / ".git" / "info" / "exclude").read_text()
        self.assertIn("/.wipe/", exclude.splitlines())

    def test_size_mismatch_warns(self):
        self.run_main("snap", "--image", self.png("a.png", 100, 80), "--note", "a")
        code, _, err = self.run_main("snap", "--image", self.png("b.png", 100, 120), "--note", "b")
        self.assertEqual(code, 0)
        self.assertIn("warning:", err)

    def test_run_name_is_slugged(self):
        self.run_main("snap", "--image", self.png("a.png"), "--note", "a", "--run", "feat/../x")
        self.assertTrue(store.run_dir(self.root, "feat-x").is_dir())

    def test_full_without_playwright_warns(self):
        page = self.root / "p.html"
        page.write_text("<p>hi</p>")

        def fake_chrome(cmd):
            out = [c for c in cmd if c.startswith("--screenshot=")][0].split("=", 1)[1]
            write_png(out, 20, 10, (1, 1, 1))

        with mock.patch.object(capture, "_has_playwright", return_value=False), \
                mock.patch.object(capture, "find_chrome", return_value="/bin/chrome"), \
                mock.patch.object(capture, "_run_chrome", side_effect=fake_chrome):
            code, _, err = self.run_main("snap", "--url", page.as_uri(), "--full", "--note", "x")
        self.assertEqual(code, 0)
        self.assertIn("Playwright", err)
        m = store.load_run(self.root, "main")
        self.assertEqual(m["versions"][0]["method"], "chrome")
        self.assertEqual(m["routes"], ["/"])
        self.assertEqual(m["base_url"], page.as_uri())

    def test_theme_both_and_routes(self):
        seen = []

        def fake_capture(url, out, viewport, theme, scale=2, method="auto", full=False):
            seen.append((url, theme))
            write_png(out, 20, 10, (1, 1, 1))
            return "chrome"

        with mock.patch.object(capture, "capture", side_effect=fake_capture):
            code, _, _ = self.run_main("snap", "/a", "--url", "http://x.test/", "--theme", "both",
                                       "--note", "n")
        self.assertEqual(code, 0)
        self.assertEqual(seen, [("http://x.test/a", "light"), ("http://x.test/a", "dark")])
        m = store.load_run(self.root, "main")
        self.assertEqual(m["routes"], ["/a", "/a@dark"])

    def fake_capture(self, url, out, viewport, theme, scale=2, method="auto", full=False):
        write_png(out, 20, 10, (1, 1, 1))
        return "chrome"

    def test_measure_reuses_saved_base_url(self):
        with mock.patch.object(capture, "capture", side_effect=self.fake_capture):
            self.assertEqual(self.run_main("snap", "/pricing", "--url", "http://x.test", "--note", "a")[0], 0)
            with mock.patch.object(capture, "_has_playwright", return_value=True), \
                    mock.patch.object(capture, "measure", return_value={"requests": 1}) as m:
                code, _, _ = self.run_main("snap", "/pricing", "--measure", "--note", "b")
        self.assertEqual(code, 0)
        self.assertEqual(m.call_args[0][0], "http://x.test/pricing")
        self.assertEqual(store.load_run(self.root, "main")["versions"][1]["measure"], {"requests": 1})

    def test_measure_without_any_url_is_usage_error(self):
        with mock.patch.object(capture, "_has_playwright", return_value=True):
            code, _, err = self.run_main("snap", "--measure", "--note", "a")
        self.assertEqual(code, 2)
        self.assertIn("--url", err)

    def test_playwright_errors_exit_1_without_traceback(self):
        boom = capture.CaptureError("Playwright failed for http://x.test: Timeout")
        base = ["snap", "--url", "http://x.test", "--note", "n"]
        with mock.patch.object(capture, "_has_playwright", return_value=True), \
                mock.patch.object(capture, "_playwright_capture", side_effect=boom):
            code, _, err = self.run_main(*base, "--method", "playwright")
        self.assertEqual(code, 1)
        self.assertIn("error: Playwright failed", err)
        self.assertNotIn("Traceback", err)
        with mock.patch.object(capture, "_has_playwright", return_value=True), \
                mock.patch.object(capture, "capture", side_effect=self.fake_capture), \
                mock.patch.object(capture, "measure", side_effect=boom):
            code, _, err = self.run_main(*base, "--measure")
        self.assertEqual(code, 1)
        self.assertIn("error: Playwright failed", err)
        self.assertNotIn("Traceback", err)

    def test_measure_needs_playwright(self):
        with mock.patch.object(capture, "_has_playwright", return_value=False):
            code, _, err = self.run_main("snap", "--measure", "--url", "http://x.test", "--note", "n")
        self.assertEqual(code, 3)
        self.assertIn("venv", err)


if __name__ == "__main__":
    unittest.main()
