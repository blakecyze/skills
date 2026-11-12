"""Puts the skill's scripts on sys.path. Import this first in each test module."""

import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "skills" / "wipe" / "scripts"
TESTS = Path(__file__).resolve().parent
for p in (str(SCRIPTS), str(TESTS)):
    if p not in sys.path:
        sys.path.insert(0, p)


class TempProject(unittest.TestCase):
    """Each test runs in a fresh temporary folder, self.root, as the working directory."""

    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name).resolve()
        cwd = Path.cwd()
        os.chdir(self.root)
        self.addCleanup(os.chdir, cwd)

    def run_main(self, *argv):
        """wipe.main(argv) as (exit code, stdout, stderr)."""
        import wipe
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = wipe.main(list(argv))
        return code, out.getvalue(), err.getvalue()
