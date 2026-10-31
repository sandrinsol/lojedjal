// Patches a test map into septem.gba with web/septem-map.js (as the editor
// does) and checks in the harness that the game starts where the map says.
import path from 'node:path';
import { importHarness, root } from '../tools/paths.mjs';
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import vm from 'node:vm';
const { EmuHarness } = await importHarness('driver.mjs');
const ctx = { window: {} };
vm.runInNewContext(await readFile(path.join(root, 'web', 'septem-map.js'), 'utf8'), ctx);
const M = ctx.window.SeptemMap;

const text = [
  '##########',
  '#........#',
  '#.######.#',
  '#.#W...#.#',
  '#.#..<.#.#',
  '#.#....#.#',
  '#.##W###.#',
  '#........#',
  '##########',
].join('\n');
const map = M.parse(text);
const rom = await readFile(path.join(root, 'septem.gba'));
const patched = M.patch(rom, map);
const back = M.serialize(M.readBlock(patched));
if (back !== text) throw new Error('round trip mismatch');

const out = path.join(root, 'tests', 'out', 'patched.gba');
await mkdir(path.dirname(out), { recursive: true });
await writeFile(out, patched);
const emu = await EmuHarness.launch(out, { symbols: path.join(root, 'septem.elf') });
await emu.waitFrames(60); await emu.tap('START'); await emu.waitFrames(20);
const read = async (n) => (await emu.readU32(n)) | 0;
const got = { x: await read('player_x'), y: await read('player_y'), facing: await read('facing') };
console.log('start', got);
// Facing west from (5,4): (4,4) and (3,4) are floor, then the wall at (2,4).
for (let i = 0; i < 4; i++) { await emu.tap('UP'); await emu.waitFrames(20); }
const after = await read('player_x');
console.log('x after 4 steps west:', after);
await emu.close();
const ok = got.x === 5 && got.y === 4 && got.facing === 3 && after === 3;
console.log(ok ? 'PASS' : 'FAIL');
process.exit(ok ? 0 : 1);
