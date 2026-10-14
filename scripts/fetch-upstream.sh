#!/usr/bin/env bash
# Clone OthmanAdi/planning-with-files at the pinned SHA into vendor/planning-with-files.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PIN="ff349ebe322b4f86c3416a6fbcde515f1de32e8b"
DEST="$ROOT/vendor/planning-with-files"
REPO="https://github.com/OthmanAdi/planning-with-files.git"

if [[ -x /usr/local/opt/git/bin/git ]]; then
  export PATH="/usr/local/opt/git/bin:$PATH"
elif [[ -x /opt/homebrew/opt/git/bin/git ]]; then
  export PATH="/opt/homebrew/opt/git/bin:$PATH"
fi

mkdir -p "$ROOT/vendor"

if [[ -d "$DEST/.git" ]]; then
  git -C "$DEST" fetch --depth 1 origin "$PIN"
  git -C "$DEST" checkout --force "$PIN"
else
  rm -rf "$DEST"
  git clone "$REPO" "$DEST"
  git -C "$DEST" checkout "$PIN"
fi

HEAD="$(git -C "$DEST" rev-parse HEAD)"
if [[ "$HEAD" != "$PIN" ]]; then
  echo "vendor pin mismatch: expected $PIN got $HEAD" >&2
  exit 1
fi

echo "vendor/planning-with-files @ $HEAD"
