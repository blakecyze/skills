#!/bin/sh
# kanso-verify — PostToolUse hook. Runs a fast linter or syntax check on the
# file the model just edited. Fails loudly only when the change broke
# something; stays silent on pass or when there is nothing to run.
#
# Opt out by setting KANSO_VERIFY_HOOK=0.

set -eu

[ "${KANSO_VERIFY_HOOK:-1}" = "0" ] && exit 0

# Hook input arrives as JSON on stdin. We need tool_name and the edited path.
# jq handles escaped quotes and spaces in paths; the sed fallback covers
# environments without it.
input="$(cat)"

if command -v jq >/dev/null 2>&1; then
  tool="$(printf '%s' "$input" | jq -r '.tool_name // empty')"
  file="$(printf '%s' "$input" | jq -r '.tool_input.file_path // .tool_input.notebook_path // empty')"
else
  tool="$(printf '%s' "$input" | sed -n 's/.*"tool_name"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -n1)"
  file="$(printf '%s' "$input" | sed -n 's/.*"file_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -n1)"
fi

case "$tool" in
  Edit|Write|MultiEdit|NotebookEdit) ;;
  *) exit 0 ;;
esac

[ -z "$file" ] && exit 0
[ -f "$file" ] || exit 0

# Resolve project root by walking up to the nearest VCS or package marker.
root="$(dirname "$file")"
while [ "$root" != "/" ]; do
  for marker in .git package.json pyproject.toml go.mod Cargo.toml; do
    [ -e "$root/$marker" ] && break 2
  done
  root="$(dirname "$root")"
done
[ "$root" = "/" ] && exit 0

run_with_timeout() {
  # Hard cap so the hook never blocks the session noticeably.
  if command -v timeout >/dev/null 2>&1; then
    timeout 8 "$@"
  elif command -v gtimeout >/dev/null 2>&1; then
    gtimeout 8 "$@"
  else
    "$@"
  fi
}

surface() {
  printf '✗ kanso-verify: %s\n%s\n' "$1" "$2" >&2
  exit 2
}

ext="${file##*.}"

case "$ext" in
  ts|tsx|js|jsx|mjs|cjs)
    if [ -f "$root/package.json" ] && command -v npx >/dev/null 2>&1; then
      # Fastest configured linter wins: biome, then oxlint, then eslint.
      if [ -f "$root/biome.json" ] || [ -f "$root/biome.jsonc" ]; then
        out="$(cd "$root" && run_with_timeout npx --no-install @biomejs/biome lint "$file" 2>&1)" || surface "biome failed on $file" "$out"
      elif [ -f "$root/.oxlintrc.json" ]; then
        out="$(cd "$root" && run_with_timeout npx --no-install oxlint "$file" 2>&1)" || surface "oxlint failed on $file" "$out"
      elif [ -f "$root/.eslintrc" ] || [ -f "$root/.eslintrc.js" ] || [ -f "$root/.eslintrc.json" ] || [ -f "$root/eslint.config.js" ] || [ -f "$root/eslint.config.mjs" ]; then
        out="$(cd "$root" && run_with_timeout npx --no-install eslint --no-warn-ignored "$file" 2>&1)" || surface "eslint failed on $file" "$out"
      fi
    fi
    ;;
  py)
    if command -v ruff >/dev/null 2>&1; then
      out="$(cd "$root" && run_with_timeout ruff check "$file" 2>&1)" || surface "ruff failed on $file" "$out"
    elif command -v python3 >/dev/null 2>&1; then
      out="$(run_with_timeout python3 -m py_compile "$file" 2>&1)" || surface "syntax error in $file" "$out"
    fi
    ;;
  go)
    pkg="$(dirname "$file")"
    if command -v go >/dev/null 2>&1 && [ -f "$root/go.mod" ]; then
      out="$(cd "$root" && run_with_timeout go vet "./$(realpath --relative-to="$root" "$pkg" 2>/dev/null || echo "$pkg")" 2>&1)" || surface "go vet failed" "$out"
    fi
    ;;
  rs)
    if command -v cargo >/dev/null 2>&1 && [ -f "$root/Cargo.toml" ]; then
      out="$(cd "$root" && run_with_timeout cargo check --quiet 2>&1)" || surface "cargo check failed" "$out"
    fi
    ;;
esac

exit 0
