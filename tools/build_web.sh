#!/usr/bin/env bash
# Assembles web/ for static hosting (Vercel): the built ROM plus the EmulatorJS
# bundle (GBA core only) from a gb-gbc-gba-test-mcp clone, by default the one
# next to this repo (../gb-gbc-gba-test-mcp); GBTEST_REPO overrides it.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
emu="${GBTEST_REPO:-$root/../gb-gbc-gba-test-mcp}"
if [ ! -d "$emu/data" ]; then
  echo "gb-gbc-gba-test-mcp not found at $emu: clone it next to this repo or set GBTEST_REPO" >&2
  exit 1
fi
web="$root/web"
rm -rf "$web/data"
mkdir -p "$web/data/cores" "$web/data/compression"
cp "$emu"/data/{loader.js,emulator.min.js,emulator.min.css,version.json} "$web/data/"
cp "$emu"/data/compression/* "$web/data/compression/"
cp "$emu"/data/cores/{cores.json,mgba-wasm.data,mgba-legacy-wasm.data} "$web/data/cores/"
cp -r "$emu/data/cores/reports" "$web/data/cores/"
cp "$emu/LICENSE" "$web/LICENSE"
cp "$emu/NOTICE.md" "$web/NOTICE.md"
cp "$root/septem.gba" "$web/septem.gba"
echo "web/ ready: $(du -sh "$web" | cut -f1)"
