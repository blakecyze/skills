#!/bin/sh
# Install swarm skills for any Agent Skills-compatible tool
# (Codex CLI, Cursor, Gemini CLI, Grok Build, ...).
#
# Default: symlink each skill into ~/.agents/skills/ so the repo checkout
# stays the single source of truth and `git pull` updates every tool at once.
#
# Flags:
#   --project    install into ./.agents/skills/ of the current directory
#   --copy       copy instead of symlink (for filesystems/tools without symlinks)
#   --uninstall  remove previously installed skills from the target
set -eu

REPO_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
TARGET="$HOME/.agents/skills"
MODE=link
UNINSTALL=0

for arg in "$@"; do
  case "$arg" in
    --project)   TARGET="$PWD/.agents/skills" ;;
    --copy)      MODE=copy ;;
    --uninstall) UNINSTALL=1 ;;
    *) echo "usage: install.sh [--project] [--copy] [--uninstall]" >&2; exit 2 ;;
  esac
done

# Tools that keep a user-level skills dir of their own get the same links,
# so the repo checkout stays the only copy. Applied only for tools already
# present on this machine, and only for user-level installs.
EXTRA_TARGETS=""
if [ "$TARGET" = "$HOME/.agents/skills" ]; then
  for tool_home in "$HOME/.codex" "$HOME/.cursor" "$HOME/.gemini"; do
    [ -d "$tool_home" ] && EXTRA_TARGETS="$EXTRA_TARGETS $tool_home/skills"
  done
fi

for dir in "$TARGET" $EXTRA_TARGETS; do
  mkdir -p "$dir"
  for skill in "$REPO_DIR"/skills/*/; do
    name=$(basename "$skill")
    dest="$dir/$name"
    rm -rf "$dest"
    if [ "$UNINSTALL" -eq 1 ]; then
      echo "removed  $dest"
      continue
    fi
    if [ "$MODE" = copy ]; then
      cp -R "${skill%/}" "$dest"
    else
      ln -s "${skill%/}" "$dest"
    fi
    echo "installed $name -> $dest"
  done
done
