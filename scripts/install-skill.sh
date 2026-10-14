#!/usr/bin/env bash
# Install planning-with-files from the pinned local clone into .claude/skills/ only.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ ! -d "$ROOT/vendor/planning-with-files/.git" ]]; then
  bash "$ROOT/scripts/fetch-upstream.sh"
fi

export DISABLE_TELEMETRY=1
export DO_NOT_TRACK=1

# Exact skills CLI install (pinned). -a claude-code writes .claude/skills only.
DISABLE_TELEMETRY=1 bun --bun x skills@1.7.2 add \
  ./vendor/planning-with-files \
  --skill planning-with-files \
  -a claude-code \
  -y \
  --copy

if [[ -e "$ROOT/.agents/skills" ]]; then
  echo "Forbidden mirror created: .agents/skills" >&2
  exit 1
fi
if [[ -e "$ROOT/.cursor/skills" ]]; then
  echo "Forbidden mirror created: .cursor/skills" >&2
  exit 1
fi

TARGET="$ROOT/.claude/skills/planning-with-files/SKILL.md"
if [[ ! -f "$TARGET" ]]; then
  echo "Expected $TARGET after skills CLI install" >&2
  exit 1
fi

echo "install-skill: OK -> $TARGET"
