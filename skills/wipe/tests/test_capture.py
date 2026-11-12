import tempfile
import unittest
from unittest import mock
from pathlib import Path

import support  # noqa: F401
import capture


class FindChromeTests(unittest.TestCase):
    def test_find_chrome_on_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            exe = Path(tmp) / "chromium"
            exe.write_text("#!/bin/sh\n")
            exe.chmod(0o755)
            self.assertEqual(capture.find_chrome({"PATH": tmp}, "linux"), str(exe))
        with tempfile.TemporaryDirectory() as empty:
            self.assertIsNone(capture.find_chrome({"PATH": empty}, "linux"))


class ChromeCommandTests(unittest.TestCase):
    def cmd(self, theme="light"):
        base = Path("/tmp/my project")
        url = (base / "page.html").as_uri()
        return capture.chrome_command("/bin/chrome", url, base / "out.png", (1280, 800), 2, theme,
                                      base / "profile"), url

    def test_paths_with_spaces(self):
        cmd, url = self.cmd()
        self.assertIn("my%20project", url)
        self.assertIn("--screenshot=/tmp/my project/out.png", cmd)
        self.assertIn(url, cmd)
        self.assertIn("--window-size=1280,800", cmd)
        self.assertIn("--force-device-scale-factor=2", cmd)

    def test_dark_flag(self):
        dark, _ = self.cmd("dark")
        light, _ = self.cmd("light")
        self.assertIn(capture.DARK_FLAG, dark)
        self.assertNotIn(capture.DARK_FLAG, light)


class PlaywrightErrorTests(unittest.TestCase):
    def fake_playwright(self, raiser):
        import sys
        import types
        pkg = types.ModuleType("playwright")
        api = types.ModuleType("playwright.sync_api")

        class Error(Exception):
            pass

        api.Error = Error
        api.sync_playwright = lambda: raiser(Error)
        pkg.sync_api = api
        return mock.patch.dict(sys.modules, {"playwright": pkg, "playwright.sync_api": api})

    def test_errors_become_capture_error(self):
        def raiser(Error):
            raise Error("Timeout 30000ms exceeded\nlong log")
        with self.fake_playwright(raiser):
            with self.assertRaises(capture.CaptureError) as c:
                capture._playwright_capture("http://x.test", Path("/tmp/x.png"), (1, 1), "light", 2, False)
            self.assertIn("Timeout", str(c.exception))
            self.assertNotIn("long log", str(c.exception))
            with self.assertRaises(capture.CaptureError):
                capture.measure("http://x.test", (1, 1))


if __name__ == "__main__":
    unittest.main()
