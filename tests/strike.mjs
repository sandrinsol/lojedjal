// Swings the sword in the harness and saves each pose to tests/out/strike_*.png.
import path from 'node:path';
const harness = process.env.GBTEST_HARNESS ?? '/home/user/sandrinsol/gb-gbc-gba-test-mcp/harness';
const { EmuHarness } = await import(path.join(harness, 'driver.mjs'));
const root = path.dirname(path.dirname(new URL(import.meta.url).pathname));
const emu = await EmuHarness.launch(path.join(root, 'septem.gba'));
await emu.waitFrames(60);
await emu.tap('START');
await emu.waitFrames(30);
await emu.tap('A', 1, 0);
const seen = [];
for (let f = 0; f < 32; f++) {
  await emu.waitFrames(1);
  const pose = await emu.readU32('arm_pose') | 0;
  if (!seen.includes(pose) || f === 31) {
    seen.push(pose);
    await emu.screenshot(path.join(root, 'tests', 'out', `strike_${seen.length - 1}_pose${pose}.png`));
  }
}
console.log('poses in order:', seen.join(' '));
// Movement is locked mid-swing and works again after.
await emu.tap('A', 1, 0); await emu.waitFrames(3); await emu.tap('UP', 1, 0); await emu.waitFrames(30);
console.log('y after UP mid-swing:', await emu.readU32('player_y') | 0);
await emu.tap('UP'); await emu.waitFrames(10);
console.log('y after UP at rest:', await emu.readU32('player_y') | 0);
await emu.close();
