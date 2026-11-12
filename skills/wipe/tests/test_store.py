import subprocess
import tempfile
import unittest
from pathlib import Path

import support  # noqa: F401
import repo
import store
from pngs import write_png


def git(root, *args):
    subprocess.run(["git", *args], cwd=str(root), check=True, capture_output=True)


class StoreTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = Path(self._tmp.name).resolve()

    def init_git(self, branch="main"):
        git(self.root, "init", "-q", "-b", branch)

    def test_empty_manifest(self):
        m = store.load_run(self.root, "x")
        self.assertEqual(m["versions"], [])
        self.assertIsNone(m["viewport"])

    def test_add_version_copies_and_numbers(self):
        a = write_png(self.root / "a.png", 4, 4, (1, 2, 3))
        m = store.load_run(self.root, "x")
        v0 = store.add_version(self.root, m, "before", {"/pricing": a}, "chrome", 2, None)
        v1 = store.add_version(self.root, m, "after", {"/pricing": a}, "chrome", 2, None)
        self.assertEqual((v0["label"], v1["label"]), ("v0", "v1"))
        self.assertTrue((store.run_dir(self.root, "x") / "v1" / "pricing.png").is_file())
        store.save_run(self.root, m)
        self.assertEqual(store.load_run(self.root, "x"), m)
        self.assertEqual(m["routes"], ["/pricing"])

    def test_route_slug_stable_across_versions(self):
        a = write_png(self.root / "a.png", 4, 4, (1, 2, 3))
        m = store.load_run(self.root, "x")
        store.add_version(self.root, m, "", {"/a-b": a}, "chrome", 2)
        v1 = store.add_version(self.root, m, "", {"/a/b": a, "/a-b": a}, "chrome", 2)
        self.assertEqual(v1["images"]["/a-b"], "v1/a-b.png")
        self.assertNotEqual(v1["images"]["/a/b"], "v1/a-b.png")

    def test_route_slugs_distinct(self):
        self.assertEqual(store.route_slug("/", set()), "index")
        self.assertEqual(store.route_slug("/pricing/", set()), "pricing")
        first = store.route_slug("/a-b", set())
        second = store.route_slug("/a/b", {first})
        self.assertNotEqual(first, second)
        self.assertNotIn("?", store.route_slug("/pricing?plan=pro", set()))

    def test_branch_run_name(self):
        self.init_git("feat/card-polish")
        self.assertEqual(store.default_run(self.root), "feat-card-polish")

    def test_no_git_repo(self):
        self.assertEqual(store.default_run(self.root), "default")
        self.assertIsNone(repo.git_info(self.root)["sha"])
        store.ensure_excluded(self.root)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_missing_git_binary(self):
        import os
        old = os.environ["PATH"]
        os.environ["PATH"] = str(self.root)
        try:
            self.assertEqual(repo.find_root(self.root), self.root)
            self.assertFalse(repo.is_git(self.root))
            self.assertIsNone(repo.current_branch(self.root))
            self.assertEqual(repo.git_info(self.root), {"sha": None, "dirty": False})
            self.assertEqual(store.default_run(self.root), "default")
            store.ensure_excluded(self.root)
        finally:
            os.environ["PATH"] = old
        self.assertEqual(list(self.root.iterdir()), [])

    def test_exclude_once(self):
        self.init_git()
        store.ensure_excluded(self.root)
        store.ensure_excluded(self.root)
        lines = (self.root / ".git" / "info" / "exclude").read_text().splitlines()
        self.assertEqual(lines.count("/.wipe/"), 1)
        self.assertFalse((self.root / ".gitignore").exists())

    def test_check_conditions(self):
        a = write_png(self.root / "a.png", 4, 4, (1, 2, 3))
        m = store.load_run(self.root, "x")
        m.update(viewport=[1280, 800], theme="light")
        store.add_version(self.root, m, "", {"/": a}, "chrome", 2)
        self.assertEqual(store.check_conditions(m, (1280, 800), "light", ["/"]), [])
        warn = store.check_conditions(m, (1440, 900), "light", ["/"])
        self.assertEqual(len(warn), 1)
        self.assertIn("1440x900", warn[0])
        self.assertIn("1280x800", warn[0])
        self.assertEqual(len(store.check_conditions(m, (1280, 800), "light", ["/", "/new"])), 1)

    def test_image_size(self):
        p = write_png(self.root / "p.png", 31, 17, (9, 9, 9))
        self.assertEqual(store.image_size(p), (31, 17))
        p.write_bytes(p.read_bytes()[:20])
        with self.assertRaises(ValueError):
            store.image_size(p)

    def test_git_info_and_worktree(self):
        self.init_git()
        self.assertIsNone(repo.git_info(self.root)["sha"])
        (self.root / "f.txt").write_text("x")
        git(self.root, "add", "f.txt")
        git(self.root, "-c", "user.name=wipe", "-c", "user.email=wipe@example.invalid",
            "commit", "-q", "-m", "init")
        info = repo.git_info(self.root)
        self.assertTrue(info["sha"])
        self.assertFalse(info["dirty"])
        (self.root / "new.html").write_text("untracked")
        self.assertTrue(repo.git_info(self.root)["dirty"])
        (self.root / "new.html").unlink()
        (self.root / "f.txt").write_text("y")
        self.assertTrue(repo.git_info(self.root)["dirty"])
        wt = self.root.parent / (self.root.name + "-wt")
        self.addCleanup(lambda: repo.remove_worktree(self.root, wt))
        self.assertEqual(repo.add_worktree(self.root, "HEAD", wt), wt)
        self.assertTrue((wt / "f.txt").is_file())
        repo.remove_worktree(self.root, wt)
        self.assertFalse(wt.exists())


if __name__ == "__main__":
    unittest.main()
