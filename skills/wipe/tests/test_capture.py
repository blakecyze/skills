import os
import tempfile
import unittest
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


if __name__ == "__main__":
    unittest.main()
