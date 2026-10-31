// Fights the Somnolent Monk in the harness: approach, parry, riposte, take a
// blow, kill him; then a second run dies to check the brand and the reset.
// Screenshots go to tests/out/duel_*.png. Exits non-zero on a failed check.
import path from 'node:path';
const harness = process.env.GBTEST_HARNESS ?? '/home/user/sandrinsol/gb-gbc-gba-test-mcp/harness';
const { EmuHarness } = await import(path.join(harness, 'driver.mjs'));
const root = path.dirname(path.dirname(new URL(import.meta.url).pathname));
const shot = (emu, n) => emu.screenshot(path.join(root, 'tests', 'out', `duel_${n}.png`));
let failures = 0;
const expect = (label, ok, got) => { console.log(`${ok ? 'ok  ' : 'FAIL'} ${label}${got !== undefined ? ` (${JSON.stringify(got)})` : ''}`); if (!ok) failures++; };

async function start() {
  const emu = await EmuHarness.launch(path.join(root, 'septem.gba'));
  await emu.waitFrames(60); await emu.tap('START'); await emu.waitFrames(20);
  emu.v = async (n) => (await emu.readU32(n)) | 0;
  emu.until = (n, value, maxFrames = 600) => emu.waitFor({ address: n, as: 's32', op: 'eq', value }, { maxFrames, precise: true });
  return emu;
}
const PLAYER_TURN = 1, ENEMY_WINDUP = 3, ENEMY_STRIKE = 4;

// --- Run 1: win -------------------------------------------------------------
let emu = await start();
await emu.tap('UP'); await emu.waitFrames(20); await shot(emu, '1_far4');
await emu.tap('UP'); await emu.waitFrames(20);
await emu.tap('UP'); await emu.waitFrames(20); await shot(emu, '2_far2');
await emu.tap('UP');
expect('duel starts one cell from the monk', (await emu.until('duel_state', PLAYER_TURN, 200)).met, { y: await emu.v('player_y') });
expect('mana is full', await emu.v('gems') === 3);
await shot(emu, '3_face_to_face');

await emu.tap('A');
await emu.until('duel_state', ENEMY_WINDUP, 200);
expect('strike hurts him', await emu.v('enemy_hp') === 3, await emu.v('enemy_hp'));
await emu.waitFrames(10); await shot(emu, '4_windup');
await emu.until('duel_state', ENEMY_STRIKE, 200);
await emu.waitFrames(12);               // into the last 10 frames of the 18-frame blow
await emu.tap('R', 1, 0);
await emu.waitFrames(2); await shot(emu, '5_parried');
expect('timed R parries', await emu.v('last_defence') === 1 && await emu.v('hp') === 12, { def: await emu.v('last_defence'), hp: await emu.v('hp') });

await emu.until('duel_state', PLAYER_TURN, 200);
await emu.tap('A');
await emu.until('duel_state', ENEMY_WINDUP, 200);
expect('riposte after a parry hits twice as hard', await emu.v('enemy_hp') === 1, await emu.v('enemy_hp'));

await emu.until('duel_state', ENEMY_STRIKE, 200);
await emu.waitFrames(3); await shot(emu, '6_blow_falls');
await emu.tap('R', 1, 0);               // too early: a flinch
await emu.until('duel_state', PLAYER_TURN, 200);
expect('an early R is a flinch and the blow lands', await emu.v('last_defence') === 3 && await emu.v('hp') === 9, { def: await emu.v('last_defence'), hp: await emu.v('hp'), wounds: await emu.v('wounds') });
await shot(emu, '7_wounded');

await emu.tap('B');
await emu.until('duel_state', ENEMY_WINDUP, 200);
expect('a vial heals and is used up', await emu.v('hp') === 12 && await emu.v('vials') === 2, { hp: await emu.v('hp'), vials: await emu.v('vials') });
await emu.until('duel_state', PLAYER_TURN, 300);
await emu.tap('A');
await emu.until('duel_state', 0, 300);
expect('the monk falls', await emu.v('enemy_hp') <= 0 && await emu.v('game_state') === 1);
await emu.waitFrames(10); await shot(emu, '8_victory');
const y0 = await emu.v('player_y');
await emu.tap('UP'); await emu.waitFrames(20);
await emu.tap('UP'); await emu.waitFrames(20);
expect('his cell is free to walk through', await emu.v('player_y') === y0 - 2, { from: y0, to: await emu.v('player_y') });
await emu.close();

// --- Run 2: death -----------------------------------------------------------
emu = await start();
for (let i = 0; i < 4; i++) { await emu.tap('UP'); await emu.waitFrames(20); }
await emu.until('duel_state', PLAYER_TURN, 200);
await emu.tap('L');
await emu.until('duel_state', ENEMY_WINDUP, 200);
expect('WARD spends a gem', await emu.v('gems') === 2 && await emu.v('ward_turns') === 2);
await emu.until('duel_state', PLAYER_TURN, 300);
expect('WARD softens the blow', await emu.v('hp') === 11, await emu.v('hp'));
await emu.writeU32('hp', 1);
await emu.tap('A');
await emu.until('duel_state', 7, 400);   // dying
await emu.waitFrames(80); await shot(emu, '9_dying');
await emu.until('game_state', 1, 300);
await emu.waitFrames(10);
expect('death brands the forearm', await emu.v('deaths') === 1);
expect('the stage restarts at the gate', await emu.v('player_x') === 7 && await emu.v('player_y') === 14 && await emu.v('hp') === 12 && await emu.v('vials') === 3);
await shot(emu, '10_branded');
for (let i = 0; i < 4; i++) { await emu.tap('UP'); await emu.waitFrames(20); }
expect('the monk stands again', (await emu.until('duel_state', PLAYER_TURN, 200)).met && await emu.v('enemy_hp') === 4);
await emu.close();

console.log(failures ? `${failures} check(s) failed` : 'all duel checks passed');
process.exit(failures ? 1 : 0);
