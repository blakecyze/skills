#!/usr/bin/env bash
# Flow installer for tools without a plugin system.
# Claude Code users do not need this: use /plugin marketplace add blakecyze/skills
set -euo pipefail

FLOW_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${TARGET:-$PWD}"

say()  { printf '  %s\n' "$1"; }
ok()   { printf '  \033[32m✓\033[0m %s\n' "$1"; }
warn() { printf '  \033[33m!\033[0m %s\n' "$1"; }

usage() {
  cat <<'USAGE'
Flow installer

  ./install.sh [target]        interactive, detects what the project uses
  ./install.sh --all [target]  install every adapter
  ./install.sh --cursor        .cursor/rules/flow.mdc
  ./install.sh --agents        append to AGENTS.md
  ./install.sh --copilot       .github/copilot-instructions.md
  ./install.sh --claude        copy skills into .claude/skills/
  ./install.sh --check         verify an existing install

Target defaults to the current directory. Flow itself is read from wherever
this script lives, so keep the repo somewhere stable or vendor it into the
project with --vendor.
USAGE
}

vendor() {
  if [ "$FLOW_ROOT" = "$TARGET/flow" ]; then
    return
  fi
  mkdir -p "$TARGET/flow"
  cp -r "$FLOW_ROOT/skills" "$FLOW_ROOT/references" "$FLOW_ROOT/tokens" "$FLOW_ROOT/scripts" "$TARGET/flow/"
  ok "Copied Flow into $TARGET/flow"
}

install_cursor() {
  mkdir -p "$TARGET/.cursor/rules"
  cp "$FLOW_ROOT/adapters/flow.mdc" "$TARGET/.cursor/rules/flow.mdc"
  ok "Cursor: .cursor/rules/flow.mdc"
}

install_agents() {
  if [ -f "$TARGET/AGENTS.md" ] && grep -q "Flow adapter" "$TARGET/AGENTS.md"; then
    warn "AGENTS.md already references Flow, skipping"
    return
  fi
  [ -f "$TARGET/AGENTS.md" ] && printf '\n' >> "$TARGET/AGENTS.md"
  cat "$FLOW_ROOT/adapters/AGENTS.md" >> "$TARGET/AGENTS.md"
  ok "Codex and friends: AGENTS.md"
}

install_copilot() {
  mkdir -p "$TARGET/.github"
  cp "$FLOW_ROOT/adapters/copilot-instructions.md" "$TARGET/.github/copilot-instructions.md"
  ok "Copilot: .github/copilot-instructions.md"
}

install_claude() {
  mkdir -p "$TARGET/.claude/skills"
  cp -r "$FLOW_ROOT/skills/." "$TARGET/.claude/skills/"
  ok "Claude Code: .claude/skills/ (plugin install is preferred, see README)"
}

check() {
  local fail=0
  command -v python3 >/dev/null || { warn "python3 not found; the scanners will not run"; fail=1; }
  python3 "$FLOW_ROOT/scripts/contrast.py" "#000000" "#FFFFFF" >/dev/null 2>&1 \
    && ok "contrast.py runs" || { warn "contrast.py failed"; fail=1; }
  python3 "$FLOW_ROOT/scripts/scan_tokens.py" "$FLOW_ROOT/scripts" >/dev/null 2>&1 \
    && ok "scan_tokens.py runs" || { warn "scan_tokens.py failed"; fail=1; }
  python3 -c "import json,sys; json.load(open('$FLOW_ROOT/tokens/flow.defaults.json'))" \
    && ok "flow.defaults.json is valid JSON" || { warn "flow.defaults.json is malformed"; fail=1; }
  for skill in flow-principles flow-audit flow-apply flow-tokens; do
    [ -f "$FLOW_ROOT/skills/$skill/SKILL.md" ] || { warn "missing skill: $skill"; fail=1; }
  done
  [ $fail -eq 0 ] && ok "All checks passed"
  return $fail
}

detect() {
  local found=0
  [ -d "$TARGET/.cursor" ] && { install_cursor; found=1; }
  [ -f "$TARGET/AGENTS.md" ] && { install_agents; found=1; }
  [ -d "$TARGET/.github" ] && { install_copilot; found=1; }
  [ -d "$TARGET/.claude" ] && { install_claude; found=1; }
  if [ $found -eq 0 ]; then
    warn "No agent config detected in $TARGET"
    say "Run with --all, or pick one: --cursor --agents --copilot --claude"
    return 1
  fi
}

main() {
  local mode="${1:---detect}"
  [ $# -gt 1 ] && TARGET="$2"

  printf '\nFlow → %s\n\n' "$TARGET"

  case "$mode" in
    -h|--help)  usage; return 0 ;;
    --check)    check; return $? ;;
    --cursor)   vendor; install_cursor ;;
    --agents)   vendor; install_agents ;;
    --copilot)  vendor; install_copilot ;;
    --claude)   install_claude ;;
    --all)      vendor; install_cursor; install_agents; install_copilot; install_claude ;;
    --detect)   vendor; detect ;;
    *)          TARGET="$mode"; vendor; detect ;;
  esac

  printf '\n'
  say "Next: run flow-tokens on this project before auditing anything."
  say "Without it, Flow measures your code against its own defaults."
  printf '\n'
}

main "$@"
