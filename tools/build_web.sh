#!/usr/bin/env bash
# Assembles web/ for static hosting (Vercel): the built ROM plus the EmulatorJS
# bundle (GBA core only) from a gb-gbc-gba-test-mcp clone.
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
emu="${GBTEST_REPO:-/home/user/sandrinsol/gb-gbc-gba-test-mcp}"
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
