// Verifies no BG's referenced tiles overlap another BG's map in VRAM (reads the
// real map entries instead of assuming tiles 0..max are used).
import path from 'node:path';
import { importHarness, root } from '../tools/paths.mjs';
const { EmuHarness } = await importHarness('driver.mjs');
const emu = await EmuHarness.launch(path.join(root, 'septem.gba'));
await emu.waitFrames(60); await emu.tap('START'); await emu.waitFrames(30);
let bad = 0;
for (const [label, keys] of [['rest', []], ['wounded', ['SELECT', 'SELECT', 'SELECT']], ['mid-strike', ['A']]]) {
  for (const k of keys) { await emu.tap(k); await emu.waitFrames(2); }
  if (label === 'mid-strike') await emu.waitFrames(8);
  const io = await emu.readMemory(0x04000000, 0x10);
  const dispcnt = io[0] | (io[1] << 8);
  const bgs = [];
  for (let n = 0; n < 4; n++) {
    if (!(dispcnt & (0x100 << n))) continue;
    const cnt = io[8 + n * 2] | (io[9 + n * 2] << 8);
    const cb = (cnt >> 2) & 3, sb = (cnt >> 8) & 31;
    const map = await emu.readMemory(0x06000000 + sb * 0x800, 0x800);
    const bytes = new Set();
    for (let i = 0; i < 1024; i++) {
      const t = (map[i * 2] | (map[i * 2 + 1] << 8)) & 0x3ff;
      bytes.add(Math.floor((cb * 0x4000 + t * 32) / 0x800)); // screen block holding the tile
    }
    bgs.push({ n, sb, tileBlocks: bytes });
  }
  for (const a of bgs) for (const b of bgs) {
    if (a.n !== b.n && a.tileBlocks.has(b.sb)) { bad++; console.log(`${label}: BG${a.n} uses tiles inside BG${b.n}'s map (screen block ${b.sb})`); }
  }
  console.log(`${label}: BGs ${bgs.map((b) => `BG${b.n}@sb${b.sb}`).join(' ')} checked`);
}
console.log(bad ? `${bad} real overlap(s)` : 'no real overlaps');
await emu.close();
process.exit(bad ? 1 : 0);
