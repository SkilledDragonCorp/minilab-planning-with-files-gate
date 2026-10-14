#!/usr/bin/env bash
# Copied verbatim from .github/workflows/tests.yml (vitest jobs) at
# ff349ebe322b4f86c3416a6fbcde515f1de32e8b — each line in its own subshell.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ ! -d "$ROOT/vendor/planning-with-files/.git" ]]; then
  bash "$ROOT/scripts/fetch-upstream.sh"
fi

(
  cd "$ROOT/vendor/planning-with-files/.pi/skills/planning-with-files/extensions/planning-with-files"
  npm ci --no-audit --no-fund && npm test
)

(
  cd "$ROOT/vendor/planning-with-files/.opencode/packages/opencode-planning-with-files"
  npm ci --no-audit --no-fund && npm run build && npm test
)

(
  cd "$ROOT/vendor/planning-with-files/.dsh/packages/dsh-planning-with-files"
  npm ci --no-audit --no-fund && npm run build && npm test
)
