#!/bin/sh
# lint-skills — static checks for kanso SKILL.md files.
#
# Checks: frontmatter present, name matches directory, description is
# trigger-shaped ("Use when…") and within the 1024-char spec limit,
# SKILL.md under 500 lines, no unspaced em dashes, no US spellings.
#
# Usage: scripts/lint-skills.sh [skills-dir]

set -u

dir="${1:-skills}"
fail=0

err() { printf '%s %s: %s\n' "$(printf '\342\234\227')" "$1" "$2"; fail=1; }

for skill in "$dir"/*/SKILL.md; do
  [ -f "$skill" ] || continue
  d="$(basename "$(dirname "$skill")")"

  head -n1 "$skill" | grep -q '^---$' || err "$d" "missing frontmatter opening fence"

  fm="$(awk '/^---$/{n++; next} n==1{print} n>=2{exit}' "$skill")"
  name="$(printf '%s\n' "$fm" | sed -n 's/^name:[[:space:]]*//p' | head -n1)"
  desc="$(printf '%s\n' "$fm" | sed -n 's/^description:[[:space:]]*//p' | head -n1)"

  [ -n "$name" ] || err "$d" "no name in frontmatter"
  [ -n "$desc" ] || err "$d" "no description in frontmatter"
  [ "$name" = "$d" ] || err "$d" "name '$name' does not match directory"

  case "$desc" in
    "Use when"*) ;;
    *) err "$d" "description should start with 'Use when' (trigger conditions, not workflow)" ;;
  esac

  [ "${#desc}" -le 1024 ] || err "$d" "description is ${#desc} chars (spec max 1024)"

  lines="$(wc -l < "$skill" | tr -d ' ')"
  [ "$lines" -le 500 ] || err "$d" "SKILL.md is $lines lines (keep under 500)"

  # Spaced em dashes are house style; the unspaced kind is the tell.
  if grep -nE '[^ ]—|—[^ ]' "$skill" >/dev/null 2>&1; then
    err "$d" "unspaced em dash on line(s): $(grep -nE '[^ ]—|—[^ ]' "$skill" | cut -d: -f1 | tr '\n' ' ')"
  fi

  us="$(grep -niE '\b(behavior|behaviors|organize[sd]?|optimize[sd]?|analyze[sd]?|favor|honor|color)\b' "$skill" | head -n3 || true)"
  [ -z "$us" ] || err "$d" "US spelling: $us"
done

if [ "$fail" -eq 0 ]; then
  printf '%s all skills pass\n' "$(printf '\342\234\223')"
fi
exit "$fail"
