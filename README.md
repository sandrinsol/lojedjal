# SEPTEM

A first-person, grid-based dark fantasy Soulslike for the Game Boy Advance, drawn
like a Gustave Doré engraving: black, white, and blood red (#D00024) only.
The design is in [DESIGN.md](DESIGN.md).

**Current build:** title screen and exploration of Stage I (the Drowned Abbey).
The HUD-less interface is in place: three mana gems on the left gauntlet, the
death brand on the right forearm, and a red hatched vignette for wounds. These are
on preview keys until duels exist (SELECT wound, L spend gem, R restore).

## Layout

| Path | What |
|---|---|
| `src/`, `include/` | Game code (Butano, C++) |
| `include/gen/septem_view.h` | Generated: engraved view panels as GBA tiles |
| `tools/engrave_world.py` | Renders the first-person wall/floor panels as hatched engravings |
| `tools/engrave_sprites.py` | Engraves the hands, gems, brand numerals, vignettes and title |
| `tools/convert_art.mjs` | PNG → Butano `.bmp`/`.json` via the gb-gbc-gba-test-mcp converters (rejects any colour outside the palette) |
| `assets/` → `graphics/` | Generated art → Butano imports |
| `tests/` | Harness scripts: `play.mjs` (walkthrough screenshots), `mcp_check.mjs` (MCP `check` + `describe`) |
| `web/` | Static player site (EmulatorJS + mGBA) deployed to Vercel |

## Build

Needs devkitARM (or the equivalent set up from devkitPro's sources), Butano, Python 3
with numpy, scipy and Pillow, and Node 20 with a clone of
[gb-gbc-gba-test-mcp](https://github.com/sandrinsol/gb-gbc-gba-test-mcp).

```bash
make art
```

```bash
make -j8 BUTANO=/path/to/butano
```

```bash
./tools/build_web.sh
```

## Test

The [gb-gbc-gba-test MCP](https://github.com/sandrinsol/gb-gbc-gba-test-mcp) server is
configured in `.mcp.json`; `gbtest.json` names the watched variables (`player_x`,
`facing`, `wounds`, `gems`, `deaths`, `cpu_usage`).

```bash
node tests/mcp_check.mjs
```

```bash
node tests/play.mjs
```
