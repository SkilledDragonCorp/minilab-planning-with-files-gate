#!/usr/bin/env bash
# Copied verbatim from .github/workflows/tests.yml (pytest job) at
# ff349ebe322b4f86c3416a6fbcde515f1de32e8b — run from repo root.
# Local/PEP-668: use a disposable venv so `python -m pip install` matches CI.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ ! -d "$ROOT/vendor/planning-with-files/.git" ]]; then
  bash "$ROOT/scripts/fetch-upstream.sh"
fi

# Prefer `python` on PATH (CI setup-python). Fall back to python3.
if ! command -v python >/dev/null 2>&1; then
  if command -v python3 >/dev/null 2>&1; then
    export PATH="$(dirname "$(command -v python3)"):$PATH"
    # If only python3 exists, expose a python shim for upstream tests that call `python`.
    SHIM_DIR="$(mktemp -d)"
    ln -sf "$(command -v python3)" "$SHIM_DIR/python"
    export PATH="$SHIM_DIR:$PATH"
  else
    echo "python not found on PATH" >&2
    exit 1
  fi
fi

VENV="$ROOT/vendor/.upstream-pytest-venv"
if [[ ! -x "$VENV/bin/python" ]]; then
  python -m venv "$VENV"
fi
# shellcheck disable=SC1091
source "$VENV/bin/activate"

cd "$ROOT/vendor/planning-with-files"
python -m pip install pytest pyyaml
python -c "import shutil, sys; sys.exit(0 if shutil.which('sh') else 1)"
python -m pytest tests/ -q --durations=20
