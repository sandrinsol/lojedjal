// Plays SEPTEM in the gb-gbc-gba-test harness (headless mGBA) and saves
// screenshots of the title and a short walk to tests/out/.
import path from 'node:path';
import { importHarness, root } from '../tools/paths.mjs';
const { EmuHarness } = await importHarness('driver.mjs');
const out = (f) => path.join(root, 'tests', 'out', f);

const emu = await EmuHarness.launch(path.join(root, 'septem.gba'));
const vars = async () => {
  const r = {};
  for (const n of ['game_state', 'player_x', 'player_y', 'facing', 'wounds', 'gems', 'deaths', 'cpu_usage']) r[n] = await emu.readU32(n) | 0;
  return r;
};
await emu.waitFrames(60);
await emu.screenshot(out('0_title.png'));
await emu.tap('START');
await emu.waitFrames(30);
await emu.screenshot(out('1_start.png'));
console.log('start', await vars());
const walk = [['UP', '2_forward'], ['UP', '3_forward'], ['RIGHT', '4_turn'], ['LEFT', '5_back'], ['UP', '6_forward'], ['UP', '7_forward'], ['UP', '8_forward'], ['RIGHT', '9_turn']];
for (const [b, name] of walk) {
  await emu.tap(b);
  await emu.waitFrames(20);
  await emu.screenshot(out(`${name}.png`));
  console.log(name, await vars());
}
for (const k of ['SELECT', 'SELECT', 'L']) { await emu.tap(k); await emu.waitFrames(4); }
await emu.waitFrames(10);
await emu.screenshot(out('10_wounded.png'));
console.log('wounded', await vars());
for (const k of ['SELECT', 'SELECT']) { await emu.tap(k); await emu.waitFrames(4); }
await emu.waitFrames(10);
await emu.screenshot(out('11_died.png'));
console.log('died', await vars());
await emu.close();
