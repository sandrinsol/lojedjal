#!/usr/bin/env node
// Converts the engraved PNGs in assets/ into Butano .bmp + .json pairs in
// graphics/, using the gb-gbc-gba-test-mcp harness converters (the same code
// as its `sprite` and `background` MCP tools).
//
// GBTEST_HARNESS points at the harness folder of a gb-gbc-gba-test-mcp clone.
import path from 'node:path';
import { readFile } from 'node:fs/promises';

const harness = process.env.GBTEST_HARNESS ?? '/home/user/sandrinsol/gb-gbc-gba-test-mcp/harness';
const { convertSprite, writeSpriteSource } = await import(path.join(harness, 'sprite.mjs'));
const { convertBackground, writeBackgroundSource } = await import(path.join(harness, 'background.mjs'));

const root = path.dirname(path.dirname(new URL(import.meta.url).pathname));
const asset = (f) => path.join(root, 'assets', f);
const out = (f) => path.join(root, 'graphics', f);

const ALLOWED = new Set(['0,0,0', '255,255,255', '208,0,36']);

// Strict palette: black, white and blood red only (plus transparency).
async function checkPalette(file) {
  const { decodePng } = await import(path.join(harness, 'png.mjs'));
  const img = decodePng(await readFile(file));
  for (let i = 0; i < img.width * img.height; i++) {
    const o = i * img.channels;
    if (img.channels === 4 && img.data[o + 3] < 128) continue;
    const key = `${img.data[o]},${img.data[o + 1]},${img.data[o + 2]}`;
    if (!ALLOWED.has(key)) throw new Error(`${path.basename(file)}: colour ${key} at pixel ${i} is not black, white or #D00024`);
  }
}

const backgrounds = ['hands', 'arm_0', 'arm_1', 'arm_2', 'arm_3', 'arm_4', 'vignette_1', 'vignette_2', 'vignette_3', 'title'];
const sprites = [['gem', 16, 16], ['brand', 32, 16]];

for (const name of backgrounds) {
  await checkPalette(asset(`${name}.png`));
  const conv = convertBackground(await readFile(asset(`${name}.png`)), {
    target: 'gba4',
    transparent: name === 'title' ? '#000000' : 'alpha',
  });
  await writeBackgroundSource(conv, out(`${name}.bmp`), name);
  console.log(`${name}: ${conv.tileCount} tiles`);
}
for (const [name, width, height] of sprites) {
  await checkPalette(asset(`${name}.png`));
  const conv = convertSprite(await readFile(asset(`${name}.png`)), { target: 'gba4', width, height, transparent: 'alpha' });
  await writeSpriteSource(conv, out(`${name}.bmp`), name);
  console.log(`${name}: ${conv.frames} frame(s)`);
}
