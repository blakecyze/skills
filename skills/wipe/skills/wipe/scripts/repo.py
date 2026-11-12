"""Git helpers for Wipe: root, branch, sha, worktrees. Standard library only."""

from __future__ import annotations

import subprocess
from pathlib import Path


def _git(root, *args):
    try:
        return subprocess.run(["git", *args], cwd=str(root), check=False,
                              capture_output=True, text=True)
    except OSError as e:  # git not installed: behave as "not a repo"
        return subprocess.CompletedProcess(["git", *args], 127, "", str(e))


def find_root(start: Path) -> Path:
    """Git toplevel containing start, else start."""
    start = Path(start).resolve()
    if not start.is_dir():
        return start
    out = _git(start, "rev-parse", "--show-toplevel")
    return Path(out.stdout.strip()).resolve() if out.returncode == 0 and out.stdout.strip() else start


def is_git(root: Path) -> bool:
    return Path(root).is_dir() and _git(root, "rev-parse", "--git-dir").returncode == 0


def current_branch(root: Path):
    """Branch name, or None when detached or not a repo. Works on unborn branches."""
    out = _git(root, "branch", "--show-current")
    name = out.stdout.strip() if out.returncode == 0 else ""
    return name or None


def git_info(root: Path) -> dict:
    """Short sha and whether the working tree has changes. sha is None without a commit."""
    sha = _git(root, "rev-parse", "--short", "HEAD")
    if sha.returncode != 0:
        return {"sha": None, "dirty": False}
    status = _git(root, "status", "--porcelain")  # untracked counts: a new page is not in the commit
    return {"sha": sha.stdout.strip(), "dirty": bool(status.stdout.strip())}


def add_worktree(root: Path, ref: str, path: Path) -> Path:
    """Check out ref detached at path. Raises RuntimeError with git's message on failure."""
    out = _git(root, "worktree", "add", "--detach", str(path), ref)
    if out.returncode != 0:
        raise RuntimeError(out.stderr.strip() or "git worktree add failed")
    return Path(path)


def remove_worktree(root: Path, path: Path) -> None:
    _git(root, "worktree", "remove", "--force", str(path))
