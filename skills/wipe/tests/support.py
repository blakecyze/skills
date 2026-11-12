"""Puts the skill's scripts on sys.path. Import this first in each test module."""

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "skills" / "wipe" / "scripts"
TESTS = Path(__file__).resolve().parent
for p in (str(SCRIPTS), str(TESTS)):
    if p not in sys.path:
        sys.path.insert(0, p)
