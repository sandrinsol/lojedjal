# SEPTEM — Design Document

A first-person, grid-based dark fantasy Soulslike RPG for the Game Boy Advance.
It must look like a Gustave Doré biblical engraving brought to life, with blood red
as its only colour accent.

## Palette (strict)

| Name        | Design hex | GBA BGR555 value | Shown on hardware |
|-------------|-----------|------------------|-------------------|
| Pure black  | `#000000` | `0x0000`         | `#000000`         |
| Pure white  | `#FFFFFF` | `0x7FFF`         | `#FFFFFF`         |
| Blood red   | `#D00024` | `0x101A`         | `#D00020`         |

The GBA has 5 bits per channel. Blue `0x24` rounds to `0x20`, a difference you can't
see. Art tools snap to these three exact values; any other colour is a build error.
There are no gradients, and tone comes from line density alone.

## Art direction

- **Method:** hand-hatched 1-bit pixel art. Directional hatching and cross-hatching
  follow the form, the way an engraver cuts. No ordered dither or halftone.
- **Subjects:** gothic medieval architecture, ruined cathedrals, crypts, ancient
  castles, fallen angels, grotesque demons, undead knights, religious symbolism.
- **Mood:** oppressive, mysterious, solemn, violent, ancient, supernatural.
- **Never:** anime, cartoon, cel shading, vector look, generic fantasy concept art,
  modern digital painting, smooth gradients, excessive ornament, random "AI" detail.
- **Red is rare and meaningful:** blood, lit mana gems, the death brand, the health
  vignette, and Sin-related omens. Nothing else.

## Premise

You are a nameless **lost soul** who must defeat the **Seven Sins**, one per stage,
to be redeemed. Stage I is **Sloth**.

## Presentation: no HUD

Everything is shown through the body and the world:

- **Health:** a *bleeding vignette*. Red hatching strokes creep inward from the
  screen edges as HP drops. The strokes are engraved lines, not a gradient.
  It's built with palette swaps and an overlay layer.
- **Mana:** **3 gems** set in the **left gauntlet**, which is always visible at the
  bottom-left and sways as you step. A charged gem is lit red; a spent gem is a
  black, hollow socket.
- **Deaths:** counted and **branded as a Roman numeral** on the **inner forearm of
  the right arm** (I, II, III, …), in red. The right forearm is **always visible**
  at the bottom-right, opposite the gauntlet.

## Exploration

- Grid crawler: one tile per step, 90° turns. Wall views are pre-drawn engraving
  panels, layered by depth (near, mid, far) and side.
- **Visible, fixed foes:** enemies stand on, or slowly patrol, grid cells and can
  be seen down corridors. Stepping in front of one starts a duel. There are no
  random encounters.

## Combat: timed turn-based duel

- The enemy fills the view, and you and it take turns.
- On the enemy's turn it shows a wind-up, then strikes, using engraving poses.
  **R blocks** (the blow lands for 1 instead of 3). **R in the last moments
  before impact is a perfect parry**: no damage, he staggers, and your next
  strike lands twice as hard.
- **Controls during a duel** (no menus):

| Button | Action |
|--------|--------|
| A | Strike (right hand) |
| R | Block; a perfect parry when timed |
| B | Drink a health vial |
| L | Cast the equipped spell |

- **Mana refills at the start of every fight** (all 3 gems).
- **Parry window:** 10 frames normally, 6 frames under Sloth's lullaby curse.
- **Health vials:** 3 vials of blessed blood. Drinking one takes your turn.
  Vials refill at the shrine.

### Duel numbers (Somnolent Monk, first build)

| | |
|---|---|
| Player health | 12; the red vignette deepens every 3 lost (4 monk blows kill) |
| Monk blow | 3 damage; 1 blocked or under WARD; 0 blocked under WARD |
| Monk health | 4; a strike deals 1, a riposte after a parry 2 |
| Monk wind-up | holds the censer 30–90 frames (uneven, to bait an early block) |
| The blow | 18 frames falling. R in the last 10 is a perfect parry: no damage, he staggers. R any earlier (or held) blocks |
| Parry cue | As the last 10 frames begin, the monk turns pure white for 4 frames; a perfect parry turns the whole screen white for 3 |
| Vial | +6 health, takes your turn (3 per life) |
| WARD | 1 gem, softens the next 2 blows |

The player acts first; after each action the monk takes his turn. Monks block
movement and are seen down a corridor up to 4 cells away.

## Spells and progression

- Only **one spell** is equipped at a time.
- **Starting spell: WARD.** Raises defence for 2 turns.
- Beating a Sin grants a new spell; Sloth gives the first "real" one.
- At the start of the next stage you choose: **keep your current spell and upgrade
  it**, or **switch to the new one**.
- There are no stats and no levelling. Spells are the only progression.

## Stage structure and death

- **One shrine per stage, at the end** (after the boss). It refills the vials and
  is where you choose a spell.
- **Death = full reset:** you go back to the stage start and every enemy returns.
  The brand on the forearm goes up by one. Stages are short and learnable.

## Stage I: Sloth, the Drowned Abbey

A flooded, half-sunken abbey where monks have sat motionless for centuries.

- **Enemies:** Somnolent Monk (slow, crushing blows), Moth-Wraith, Chained Sleeper.
- **Boss: SLOTH**, a colossal bloated figure enthroned on sleeping bodies. Its
  wind-ups are extremely slow and deceptive (they test patience on parries), and
  lullaby curses shrink your parry window.

## Audio

Mostly ambient while exploring: drips, distant choir drones, chains, footsteps on
stone. Organ and choir music only in boss duels. DirectSound through Maxmod
(Butano).

## Technical

- **Toolchain:** Butano (C++, devkitARM).
- **Testing:** the [gb-gbc-gba-test MCP](https://github.com/sandrinsol/gb-gbc-gba-test-mcp)
  harness. Use `build` and `check` on every change, `describe` with watched variables
  (`hp`, `gems`, `deaths`, `duel_state`), golden screenshots for the engraving look,
  and `run_sequence` scripts for parry timing.
- Art goes in as PNGs through the MCP `background` and `sprite` converters, with a
  palette check that rejects any colour except the three above.

## Open items

- The name and effect of the spell granted by Sloth (to be decided).
