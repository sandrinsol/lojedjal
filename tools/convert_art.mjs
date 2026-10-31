#!/usr/bin/env node
// Converts the engraved PNGs in assets/ into Butano .bmp + .json pairs in
// graphics/, using the gb-gbc-gba-test-mcp harness converters (the same code
// as its `sprite` and `background` MCP tools).
//
// The gb-gbc-gba-test-mcp clone is found as described in tools/paths.mjs.
import path from 'node:path';
import { readFile } from 'node:fs/promises';
import { importHarness, root } from './paths.mjs';

const { convertSprite, writeSpriteSource } = await importHarness('sprite.mjs');
const { convertBackground, writeBackgroundSource } = await importHarness('background.mjs');
const asset = (f) => path.join(root, 'assets', f);
const out = (f) => path.join(root, 'graphics', f);

const ALLOWED = new Set(['0,0,0', '255,255,255', '208,0,36']);

// Strict palette: black, white and blood red only (plus transparency).
async function checkPalette(file) {
  const { decodePng } = await importHarness('png.mjs');
  const img = decodePng(await readFile(file));
  for (let i = 0; i < img.width * img.height; i++) {
    const o = i * img.channels;
    if (img.channels === 4 && img.data[o + 3] < 128) continue;
    const key = `${img.data[o]},${img.data[o + 1]},${img.data[o + 2]}`;
    if (!ALLOWED.has(key)) throw new Error(`${path.basename(file)}: colour ${key} at pixel ${i} is not black, white or #D00024`);
  }
}

const backgrounds = ['hands', 'left_1', 'left_2', 'left_3', 'left_4', 'left_5', 'left_6',
  'arm_0', 'arm_1', 'arm_2', 'arm_3', 'arm_4', 'arm_5', 'arm_6', 'arm_7', 'arm_8', 'arm_9', 'arm_10', 'vignette_1', 'vignette_2', 'vignette_3', 'title', 'death'];
const sprites = [['gem', 16, 16], ['brand', 32, 16], ['monk', 64, 64], ['monk_far', 64, 64]];

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
