import json
import re
import unittest
from pathlib import Path

import support
import page
import store
from pngs import write_png

DATA = re.compile(r'<script type="application/json" id="wipe-data">(.*?)</script>', re.S)


def page_data(html: str) -> dict:
    return json.loads(DATA.search(html).group(1))


class PageTests(support.TempProject):
    def make_run(self, count, routes=("/pricing",), run="x"):
        m = store.load_run(self.root, run)
        for i in range(count):
            images = {r: write_png(self.root / f"s{i}-{n}.png", 8, 6, (i * 40, 20, 30))
                      for n, r in enumerate(routes)}
            store.add_version(self.root, m, f"note {i} <b>&", images, "chrome", 2)
        store.save_run(self.root, m)
        return m

    def test_page_references_versions(self):
        m = self.make_run(2)
        path = page.build_page(self.root, m)
        self.assertEqual(path, store.run_dir(self.root, "x") / "index.html")
        html = path.read_text()
        self.assertIn("v0/pricing.png", html)
        self.assertIn("v1/pricing.png", html)
        notes = [v["note"] for v in page_data(html)["manifest"]["versions"]]
        self.assertEqual(notes, ["note 0 <b>&", "note 1 <b>&"])
        self.assertNotIn("<b>", html)  # notes are escaped inside the JSON block

    def test_note_with_placeholder_cannot_break_page(self):
        m = store.load_run(self.root, "x")
        img = {"/pricing": write_png(self.root / "p.png", 8, 6, (1, 2, 3))}
        store.add_version(self.root, m, "see __COMPONENT__ and __RUN__", img, "chrome", 2)
        store.add_version(self.root, m, "__DATA__", img, "chrome", 2)
        store.save_run(self.root, m)
        html = page.build_page(self.root, m).read_text()
        data = page_data(html)
        self.assertEqual(data["manifest"]["versions"][0]["note"], "see __COMPONENT__ and __RUN__")
        self.assertEqual(data["manifest"]["versions"][1]["note"], "__DATA__")
        self.assertEqual(html.count("customElements.define"), page.COMPONENT.read_text().count("customElements.define"))

    def test_page_inlines_component(self):
        html = page.build_page(self.root, self.make_run(2)).read_text()
        self.assertIn("customElements.define('before-after'", html)
        self.assertNotIn('src="before-after.js"', html)

    def test_component_small(self):
        js = (Path(page.__file__).parent / "before-after.js").read_text()
        js = re.sub(r"/\*.*?\*/", "", js, flags=re.S)
        js = re.sub(r"^\s*//.*$", "", js, flags=re.M)
        js = re.sub(r"\s+", " ", js).strip()
        self.assertLess(len(js.encode()), 2048)

    def test_page_lists_sizes_and_defaults(self):
        m = self.make_run(3, routes=("/", "/about"))
        data = page_data(page.build_page(self.root, m).read_text())
        self.assertEqual((data["a"], data["b"], data["route"]), (1, 2, "/"))
        self.assertEqual(data["sizes"]["v2/about.png"], [8, 6])

    def test_embed_files(self):
        m = self.make_run(3)
        out = self.root / "embed"
        snippet = page.build_embed(self.root, m, 0, 2, "/pricing", out)
        self.assertEqual(snippet, out / "snippet.html")
        for name in ("before.png", "after.png", "before-after.js", "snippet.html"):
            self.assertTrue((out / name).is_file(), name)
        self.assertEqual((out / "after.png").read_bytes(),
                         (store.run_dir(self.root, "x") / "v2" / "pricing.png").read_bytes())
        text = snippet.read_text()
        for ref in ('"before.png"', '"after.png"', '"before-after.js"'):
            self.assertIn(ref, text)
        self.assertIn("v2 · note 2 &lt;b&gt;&amp;", text)

    def test_show_needs_two(self):
        self.make_run(1)
        code, _, err = self.run_main("show", "--run", "x", "--no-open")
        self.assertEqual(code, 2)
        self.assertIn("two versions", err)
        self.assertNotIn("Traceback", err)

    def test_show_pair_selection(self):
        self.make_run(3)
        code, out, _ = self.run_main("show", "0", "v2", "--run", "x", "--no-open")
        self.assertEqual(code, 0)
        path = store.run_dir(self.root, "x") / "index.html"
        self.assertIn(str(path), out)
        data = page_data(path.read_text())
        self.assertEqual((data["a"], data["b"]), (0, 2))

    def test_show_rejects_bad_pairs(self):
        self.make_run(2)
        for argv in (["0"], ["0", "5"], ["1", "1"], ["0", "x"]):
            code, _, err = self.run_main("show", *argv, "--run", "x", "--no-open")
            self.assertEqual(code, 2, argv)
            self.assertNotIn("Traceback", err)
        code, _, err = self.run_main("show", "--route", "/nope", "--run", "x", "--no-open")
        self.assertEqual(code, 2)
        self.assertIn("/nope", err)

    def test_embed_cli_default_out(self):
        self.make_run(2)
        code, out, _ = self.run_main("embed", "0", "1", "--run", "x")
        self.assertEqual(code, 0)
        snippet = store.run_dir(self.root, "x") / "embed-v0-v1" / "snippet.html"
        self.assertTrue(snippet.is_file())
        self.assertIn(str(snippet), out)


if __name__ == "__main__":
    unittest.main()
