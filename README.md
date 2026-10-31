# SEPTEM

A first-person, grid-based dark fantasy Soulslike for the Game Boy Advance, drawn
like a Gustave Doré engraving: black, white, and blood red (#D00024) only.
The design is in [DESIGN.md](DESIGN.md).

**Current build:** title screen and Stage I (the Drowned Abbey) with the
Somnolent Monk duel. The HUD-less interface is in place: three mana gems on the
left gauntlet, the death brand on the right forearm, and a red hatched vignette
for wounds. In a duel: A strike, R block (timed: a perfect parry), B vial, L cast WARD. Dying
brands the arm and restarts the stage.

## Editing the map

Open **/editor.html** on the game's site (linked from the player as "EDIT THE
MAP"). Paint walls, window walls and floor, place the start and its facing, then
**Play this map**: the page writes your layout into the ROM's map block and boots
it, no rebuild needed. Your map stays saved in your browser; copy or download it
as text.

To make a map the game's own Stage I, put its text in `maps/drowned_abbey.txt`
and run `make map` (or send the text to Claude to commit). Map text:
`#` wall, `W` window wall, `.` floor, `M` Somnolent Monk, `^ > v <` start facing N / E / S / W;
8 to 32 cells each way.

## Layout

| Path | What |
|---|---|
| `src/`, `include/` | Game code (Butano, C++) |
| `include/gen/septem_view.h` | Generated: engraved view panels as GBA tiles |
| `tools/engrave_world.py` | Renders the first-person wall/floor panels as hatched engravings |
| `tools/engrave_sprites.py` | Engraves the hands, gems, brand numerals, vignettes and title |
| `tools/engrave_monk.py` | Engraves the Somnolent Monk: five duel poses and three distance views |
| `tools/import_art.py` | Turns the generated artwork in `assets/raw/` (see `artwork.md`) into game art: three colours, game sizes, cut-outs; measures the gem and brand positions into `include/gen/septem_layout.h` |
| `assets/raw/`, `assets/refs/` | Generated source artwork and the style references |
| `tools/convert_art.mjs` | PNG → Butano `.bmp`/`.json` via the gb-gbc-gba-test-mcp converters (rejects any colour outside the palette) |
| `assets/` → `graphics/` | Generated art → Butano imports |
| `tests/` | Harness scripts: `play.mjs` (walkthrough), `strike.mjs` (sword swing), `duel.mjs` (fights the monk: perfect parry, riposte, block, vial, WARD, death and reset), `hands_anim.mjs` (flask, block and parry frames), `mcp_check.mjs` (MCP `check` + `describe`), `vram_overlap.mjs` (reads every BG map to rule out real VRAM overlaps), `map_patch.mjs` (patches a map in as the editor does and checks the start) |
| `maps/` | Map text files; `tools/build_map.py` turns one into the ROM map block |
| `web/` | Static player site (EmulatorJS + mGBA) and the map editor, deployed to Vercel |

## Set up locally

Put the repos side by side; the build, the art tools, the tests and the MCP
server all find each other there with no paths to configure:

```
your-folder/
├── lojedjal/               this repo
├── gb-gbc-gba-test-mcp/    git clone https://github.com/sandrinsol/gb-gbc-gba-test-mcp
└── butano/                 git clone https://github.com/GValiente/butano
```

Also needed:

- devkitPro with devkitARM (`dkp-pacman -S gba-dev`, or the Windows installer)
- Python 3 with numpy, scipy and Pillow (`pip install numpy scipy pillow`)
- Node 20+, and `npm install` in `gb-gbc-gba-test-mcp/harness`

To use other locations, set `GBTEST_REPO` (the gb-gbc-gba-test-mcp clone) and
`BUTANO` (the Butano clone).

The built game is committed as `web/septem.gba`, so you can play it in any GBA
emulator, or serve `web/` (for example `python3 -m http.server` in that folder)
to play it in the browser player, without building anything.

## Build

```bash
make art
```

```bash
make -j8
```

```bash
./tools/build_web.sh
```

`make art` regenerates the game art from `assets/raw`, `make` builds
`septem.gba`, and `build_web.sh` copies it with the emulator into `web/`.

## Test

The [gb-gbc-gba-test MCP](https://github.com/sandrinsol/gb-gbc-gba-test-mcp) server is
configured in `.mcp.json` (it starts the clone next to this repo, or the one in
`GBTEST_REPO`); `gbtest.json` names the watched variables (`player_x`,
`facing`, `wounds`, `gems`, `deaths`, `cpu_usage`).

```bash
node tests/mcp_check.mjs
```

```bash
node tests/play.mjs
```
