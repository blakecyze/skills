#!/usr/bin/env bash
# Pull the standalone libraries into this monorepo and report what changed.
# kanso, mimesis, and swarm are canonical in their own repos; flow is
# canonical here and has no standalone repo.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT INT TERM

for lib in kanso mimesis swarm; do
  git clone -q --depth 1 "https://github.com/blakecyze/$lib.git" "$TMP/$lib"
  rsync -a --delete \
    --exclude '.git' \
    --exclude '.claude-plugin/marketplace.json' \
    "$TMP/$lib/" "$ROOT/skills/$lib/"
  rm -f "$ROOT/skills/$lib/.claude-plugin/marketplace.json"
  printf '%s: synced\n' "$lib"
done

cd "$ROOT"
if git diff --quiet && [ -z "$(git status --porcelain)" ]; then
  echo "No drift. Monorepo matches the standalone repos."
else
  echo "Drift pulled in:"
  git status --porcelain
  echo "Review, commit, and push."
fi
