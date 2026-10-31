// Checks the hand animations in a duel: drinking from the flask (left hand
// frames follow the draughts left), the block (raise, hold, the blow lands)
// and the perfect parry (meeting, clash, turned aside). Screenshots go to
// tests/out/anim_*.png. Exits non-zero on a failed check.
import path from 'node:path';
import { importHarness, root } from '../tools/paths.mjs';
const { EmuHarness } = await importHarness('driver.mjs');
const shot = (emu, n) => emu.screenshot(path.join(root, 'tests', 'out', `anim_${n}.png`));
let failures = 0;
const expect = (label, ok, got) => { console.log(`${ok ? 'ok  ' : 'FAIL'} ${label}${got !== undefined ? ` (${JSON.stringify(got)})` : ''}`); if (!ok) failures++; };
const PLAYER_TURN = 1, ENEMY_WINDUP = 3, ENEMY_STRIKE = 4;

const emu = await EmuHarness.launch(path.join(root, 'septem.gba'));
const v = async (n) => (await emu.readU32(n)) | 0;
const until = (n, value, maxFrames = 600) => emu.waitFor({ address: n, as: 's32', op: 'eq', value }, { maxFrames, precise: true });
await emu.waitFrames(60); await emu.tap('START'); await emu.waitFrames(20);
for (let i = 0; i < 4; i++) { await emu.tap('UP'); await emu.waitFrames(20); }
await until('duel_state', PLAYER_TURN, 200);

// Take a hit so a draught can be drunk (B needs missing health).
await emu.writeU32('hp', 6);

// --- Drinking: full flask (3), drink, two left ------------------------------
await emu.tap('B', 1, 0);
expect('B lifts the full flask', (await until('left_pose', 4, 10)).met, await v('left_pose'));
await emu.waitFrames(6); await shot(emu, '1_flask_full');
expect('then drinks', (await until('left_pose', 5, 40)).met);
await emu.waitFrames(10); await shot(emu, '2_drinking');
expect('then shows two draughts left', (await until('left_pose', 3, 40)).met && await v('vials') === 2, { left: await v('left_pose'), vials: await v('vials') });
await emu.waitFrames(6); await shot(emu, '3_flask_two_thirds');
expect('and lowers the flask', (await until('left_pose', 0, 40)).met);

// --- Block: raise, hold, the blow lands -------------------------------------
await until('duel_state', ENEMY_WINDUP, 300);
await emu.tap('R', 1, 0);
expect('R raises the guard', (await until('arm_pose', 5, 6)).met, await v('arm_pose'));
await emu.waitFrames(2); await shot(emu, '4_block_raise');
expect('and holds it', (await until('arm_pose', 6, 12)).met, await v('arm_pose'));
await emu.waitFrames(4); await shot(emu, '5_block_held');
expect('the blow lands on the guard', (await until('arm_pose', 7, 200)).met, await v('arm_pose'));
await emu.waitFrames(2); await shot(emu, '6_block_impact');
expect('a block costs 1', await v('last_defence') === 3);
expect('the arm returns to rest', (await until('arm_pose', 0, 30)).met);

// --- Perfect parry: meeting, clash, turned aside -----------------------------
await until('duel_state', PLAYER_TURN, 300);
await emu.tap('A');
await until('duel_state', ENEMY_STRIKE, 300);
await until('parry_window_open', 1, 40);
await emu.tap('R', 1, 0);
expect('a perfect parry snaps the blade up', (await until('arm_pose', 8, 6)).met, await v('arm_pose'));
expect('the clash', (await until('arm_pose', 9, 10)).met);
await emu.waitFrames(5); await shot(emu, '7_parry_clash');
expect('turned aside', (await until('arm_pose', 10, 14)).met);
await emu.waitFrames(4); await shot(emu, '8_parry_aside');
expect('it was a perfect parry', await v('last_defence') === 1);
expect('the arm returns to rest', (await until('arm_pose', 0, 30)).met);

await emu.close();
console.log(failures ? `${failures} check(s) failed` : 'all animation checks passed');
process.exit(failures ? 1 : 0);
