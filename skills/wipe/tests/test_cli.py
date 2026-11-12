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


class HousekeepingTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name).resolve()
        self.git("init", "-q", "-b", "main")
        for n in ("one", "two"):
            (self.root / "f.txt").write_text(n)
            self.git("add", "f.txt")
            self.git("-c", "user.name=wipe", "-c", "user.email=wipe@example.invalid",
                     "commit", "-q", "-m", n)
        import os
        cwd = Path.cwd()
        os.chdir(self.root)
        self.addCleanup(os.chdir, cwd)
        self.addCleanup(self.drop_worktrees)

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, check=True, capture_output=True, text=True)

    def drop_worktrees(self):
        import shutil
        for wt in store.load_run(self.root, "main")["worktrees"]:
            shutil.rmtree(wt, ignore_errors=True)

    def run_main(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = wipe.main(list(argv))
        return code, out.getvalue(), err.getvalue()

    def snap(self, note):
        img = str(write_png(self.root / "x.png", 10, 10, (1, 2, 3)))
        self.assertEqual(self.run_main("snap", "--image", img, "--note", note)[0], 0)

    def test_base_creates_worktree(self):
        code, out, _ = self.run_main("base", "HEAD~1")
        self.assertEqual(code, 0)
        path = Path(out.strip())
        self.assertTrue(path.is_dir())
        self.assertTrue(path.name.startswith("wipe-main-"))
        head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=path, capture_output=True, text=True).stdout
        self.assertEqual(head.strip(), self.git("rev-parse", "HEAD~1").stdout.strip())
        self.assertEqual(store.load_run(self.root, "main")["worktrees"], [str(path)])

    def test_base_twice_reuses(self):
        _, first, _ = self.run_main("base", "HEAD~1")
        code, second, _ = self.run_main("base", "HEAD~1")
        self.assertEqual((code, second), (0, first))
        self.assertEqual(len(store.load_run(self.root, "main")["worktrees"]), 1)

    def test_base_unknown_ref(self):
        code, _, err = self.run_main("base", "nope")
        self.assertEqual(code, 2)
        self.assertIn("nope", err)

    def test_base_existing_unrecorded_path_is_usage_error(self):
        path = Path(tempfile.gettempdir()) / "wipe-main-head-1"
        path.mkdir()
        self.addCleanup(path.rmdir)
        code, _, err = self.run_main("base", "HEAD~1")
        self.assertEqual(code, 2)
        self.assertIn("exists", err)

    def test_base_outside_git(self):
        import os
        with tempfile.TemporaryDirectory() as d:
            os.chdir(Path(d).resolve())
            code, _, err = self.run_main("base", "HEAD")
        self.assertEqual(code, 2)
        self.assertIn("git", err)
        self.assertNotIn("Traceback", err)

    def test_clean_removes(self):
        _, out, _ = self.run_main("base", "HEAD~1")
        path = Path(out.strip())
        self.assertEqual(self.run_main("clean")[0], 0)
        self.assertFalse(path.exists())
        self.assertNotIn(path.name, self.git("worktree", "list").stdout)
        self.assertEqual(store.load_run(self.root, "main")["worktrees"], [])

    def test_clean_tolerates_hand_deleted_worktree(self):
        import shutil
        _, out, _ = self.run_main("base", "HEAD~1")
        shutil.rmtree(out.strip())
        self.assertEqual(self.run_main("clean")[0], 0)
        self.assertEqual(store.load_run(self.root, "main")["worktrees"], [])
        self.assertNotIn("wipe-main", self.git("worktree", "list").stdout)

    def test_clean_all_deletes_run_only(self):
        self.snap("a")
        self.run_main("base", "HEAD~1")
        (self.root / ".wipe" / "other").mkdir()
        self.assertEqual(self.run_main("clean", "--all")[0], 0)
        self.assertFalse((self.root / ".wipe" / "main").exists())
        self.assertTrue((self.root / ".wipe" / "other").is_dir())
        self.assertTrue((self.root / "f.txt").is_file())

    def test_clean_with_nothing_is_ok(self):
        self.assertEqual(self.run_main("clean")[0], 0)

    def test_list_runs(self):
        self.snap("before")
        self.snap("after")
        code, out, _ = self.run_main("list")
        self.assertEqual(code, 0)
        self.assertIn("main", out)
        self.assertIn("2 versions", out)
        self.assertIn("v0", out)
        self.assertIn("after", out)

    def test_list_singular_and_empty(self):
        code, out, _ = self.run_main("list")
        self.assertEqual((code, out.strip()), (0, "no runs yet"))
        self.snap("only")
        self.assertIn("1 version\n", self.run_main("list")[1])


if __name__ == "__main__":
    unittest.main()
