# SEPTEM: artwork prompts, round 2 (hands, flask, block, parry, walls and floors)

New prompts for the ChatGPT Project, in the same style and with the same
reference library as `artwork.md`. They cover:

1. **The left gauntlet, redrawn.** The current one reads as a right hand.
2. **The healing flask:** the left hand drinking from it, with the blood inside
   shown full, two-thirds full and one-third full, so the flask itself shows
   how many draughts are left.
3. **Block and parry:** the right arm and sword raising a guard, taking a blow,
   and turning a blow aside with a perfect parry.
4. **Walls and floors for the dungeon**, redrawn so they read in the 3D view,
   with variants.

The project instructions from `artwork.md` still apply: same style, colours
and output rules. Paste nothing new into the project; just use the prompts below.

---

## Before you start: references to attach

| Reference | What it is | Attach for |
|---|---|---|
| `REF_style_01` | The corridor style anchor | everything |
| `REF_char_arm` | The approved right arm with sword (`assets/raw/arm_sword.png`) | the gauntlet's plate design, all block and parry poses |
| `REF_char_gauntlet` | The **new** left gauntlet, once you approve it in section 1 | every flask pose |
| `REF_char_flask` | The flask, once you approve it in section 2a | every drinking pose |

`REF_char_arm` already exists: it's `arm_sword.png` from the first round. If it
isn't in the project's files yet, upload it under that name before starting.

**Order:** 1 (gauntlet), 2a (flask), 2b–2c (drinking), 3 (block and parry).
Each step uses the reference approved in the one before.

---

## Framing rules for every hand image

The game swaps these images in place frame by frame, so they must line up:

- **Square, cut-out, transparent background**, the same size as the first round
  (about 1254 × 1254).
- **Left hand:** the forearm always enters from the **bottom-left corner**, at
  the same place and the same size in every image.
- **Right hand:** the forearm always enters from the **bottom-right corner**, at
  the same place and the same size as `REF_char_arm`.
- **Blood red #D00024** only for: the three gems on the left gauntlet, the blood
  in the flask, and the Roman numeral on the right forearm. Nothing else may be
  red (the game finds the gems and the brand by their red).
- Bold engraving lines that still read when shrunk to about 110–170 pixels.

---

## 1. Left gauntlet (replaces the current one)

`assets/raw/gauntlet.png` · square · cut-out · attach `REF_style_01`, `REF_char_arm` · approve as `REF_char_gauntlet` (replace the old one in the project's files)

The old image shows the thumb on the wrong side for a left hand seen by its
wearer. The prompt below spells out which side the thumb must be on.

```
Attached: REF_style_01 (style) and REF_char_arm (the right arm; match its plate
armour, rivets, linen wrappings and line weight, but this is the OTHER hand).

Cut-out: the wearer's own LEFT hand, seen from their own eyes (first-person),
raised in front of them with the BACK of the hand towards the viewer, fingers
up and slightly spread, slightly curled. Because it is a left hand seen from
behind, the THUMB is on the RIGHT side of the hand, pointing up and to the right,
towards the centre of the image; the little finger is on the far left. The
forearm enters from the bottom-left corner of the image and rises diagonally up
and to the right.

Battered medieval plate gauntlet: articulated riveted finger plates, a broad
knuckle plate, a flared cuff, worn leather and linen strips at the wrist,
matching the attached right arm. Set in a row across the knuckle plate: three
large round gems, clearly separated from each other, drawn as flat blood red
#D00024 with one tiny white glint and a thick black bezel. Everything else pure
black and white. Bold engraving, strong black outline, transparent background;
the arm touches only the bottom-left edge.
```

**Check before approving:** hold up your own left hand, back towards your face.
Your thumb is on the right. The image must match.

If it comes out as a right hand anyway:

```
This is a right hand. Mirror the hand only: the thumb must be on the RIGHT side of
the image, the little finger on the LEFT, the back of the hand towards the viewer,
the forearm still entering from the bottom-left corner.
```

---

## 2. The healing flask

The vials of blessed blood become **one flask holding three draughts**. The
blood inside shows how many are left:

| Draughts left | Blood level |
|---|---|
| 3 | full (to the shoulder of the flask) |
| 2 | two-thirds |
| 1 | one-third |
| 0 | empty |

Three engraved rings on the glass mark the thirds, so the level reads at a glance
even at a tiny size.

### 2a. The flask on its own (the design reference)

`assets/raw/flask.png` · square · cut-out · attach `REF_style_01` · approve as `REF_char_flask`

```
Cut-out, close-up: a small heavy medieval glass flask for blessed blood, round-
bellied with a short neck, stoppered with dark wax and bound at the neck with a
twist of cord and a tiny lead seal. Three thin engraved rings run around the
glass at one-third, two-thirds and the shoulder, like measuring marks. It is
FULL: flat blood red #D00024 liquid up to the top ring, with a flat level line
and one white glint on the glass. The glass is drawn with black engraved lines
and sharp white highlights; the empty glass above the blood is white. Bold,
simple, readable at 24 pixels. Transparent background.
```

### 2b. Holding the flask up: four fill levels

`assets/raw/flask_hold_3.png`, `flask_hold_2.png`, `flask_hold_1.png`, `flask_hold_0.png` · square · cut-out · attach `REF_style_01`, `REF_char_gauntlet`, `REF_char_flask`

The left hand lifts the flask in front of the wearer's eyes, before and after
drinking. Make the full one first, then ask for the other three in the same chat
so the pose stays identical.

```
Attached: REF_style_01 (style), REF_char_gauntlet (the same left hand and arm,
same armour, same three red gems) and REF_char_flask (the same flask).

Cut-out, first-person: the wearer's left gauntleted hand raises the flask in
front of their eyes, held upright by the neck between thumb and fingers, the
back of the hand towards the viewer, the forearm entering from the bottom-left
corner of the image at the same place and size as in REF_char_gauntlet. The
flask is large in the image, its belly near the centre-left. It is FULL: the blood
reaches the top ring. Blood red #D00024 only for the blood and the gauntlet's three
gems. Bold engraving, transparent background.
```

Then, one at a time:

```
Same image, same pose, same framing and size. Only change the blood: it now
reaches the SECOND ring (two-thirds full). Above it the glass is empty and white.
```

```
Same image, same pose, same framing and size. Only change the blood: it now
reaches the FIRST ring (one-third full).
```

```
Same image, same pose, same framing and size. The flask is now EMPTY: no blood,
only a few red drops clinging to the bottom of the glass.
```

### 2c. Drinking

`assets/raw/flask_drink.png` · square · cut-out · attach `REF_style_01`, `REF_char_gauntlet`, `REF_char_flask`

```
Attached: REF_style_01 (style), REF_char_gauntlet (the same left hand and arm)
and REF_char_flask (the same flask).

Cut-out, first-person: the wearer drinks. The left gauntleted hand has tipped the
flask up to their mouth: the bottom of the flask points up towards the top of the
image and is large and close, the neck out of sight below the viewer's face, the
forearm entering from the bottom-left corner and rising steeply. A thin stream
of blood red #D00024 runs down inside the glass towards the mouth. The gauntlet's
three red gems are visible on the knuckles. Bold engraving, transparent
background.
```

In the game the drink plays as: hold (current level) → drink → hold (one
level lower) → the hand lowers back to rest.

---

## 3. Block and parry (right arm and sword)

All of these use the right arm and sword from `REF_char_arm`: same gauntleted
fist, linen wrappings, ragged dark sleeve and the burned Roman numeral III on the
inner forearm, entering from the bottom-right corner at the same place and size.

Every prompt starts with:

```
Attached: REF_style_01 (style) and REF_char_arm (design). Same right arm, same
sword, same armour and wrappings, same red numeral III on the inner forearm, the
forearm entering from the bottom-right corner at the same place and size as
REF_char_arm. Change only the pose described below. Cut-out, transparent
background, bold engraving, black and white only except the red numeral.
```

### 3a. Block: three frames

`assets/raw/block_1.png`, `block_2.png`, `block_3.png` · square · cut-out · attach `REF_style_01`, `REF_char_arm`

```
BLOCK, frame 1, RAISING THE GUARD: the sword swings up and across in front of the
wearer, the blade turning flat and rising towards horizontal, the fist moving
towards the centre of the image. Short engraved motion lines behind the blade.
```

```
BLOCK, frame 2, GUARD HELD: the sword held flat and high across the upper part of
the image, the blade horizontal and pointing left, edge up, braced to take a blow
from above. The fist at the centre-right, the forearm rising from the
bottom-right corner, the numeral III visible on the inner forearm. Tense and
still, no motion lines.
```

```
BLOCK, frame 3, THE BLOW LANDS: the same high guard, but the blade is driven down
and bent slightly under a heavy impact from above, the fist pushed lower, the arm
straining. Short jagged engraved impact lines burst from the top edge of the blade
where the blow struck. No sparks of colour: black and white only (the red numeral
stays).
```

### 3b. Perfect parry: three frames

`assets/raw/parry_1.png`, `parry_2.png`, `parry_3.png` · square · cut-out · attach `REF_style_01`, `REF_char_arm`

```
PERFECT PARRY, frame 1, THE MEETING: the sword snaps up at an angle from lower
right to upper left, quick and precise, its edge meeting an unseen blow at the
upper centre of the image. Sharp motion lines along the path of the snap.
```

```
PERFECT PARRY, frame 2, THE CLASH: the same angled sword at the instant of the
clash. From the point where the blade meets the blow (upper centre) a burst of
white light radiates outward: sharp straight engraved rays and a ring of white
sparks, pure white with black outlines, like a star cut into a woodblock. The
light is the brightest thing in the image.
```

```
PERFECT PARRY, frame 3, TURNED ASIDE: the blow has been thrown aside: the sword
has swept outward to the right and slightly down, the blade pointing to the
upper right, the arm open and ready to strike. A short curved tail of motion lines
shows the outward sweep. A few last white sparks drift away.
```

### 3c. The clash spark on its own (optional)

`assets/raw/parry_spark.png` · square · cut-out · attach `REF_style_01`

```
Cut-out: a burst of light where two weapons clash, engraved like a woodblock
star: eight to twelve sharp straight rays of different lengths radiating from a
small white centre, a broken ring of white sparks around it. Pure white with clean
black outlines, nothing else. Bold, readable at 32 pixels. Transparent
background.
```

The game can lay it over the monk's censer at the moment of a perfect parry,
together with the white screen flash it already has.

---

## 4. Walls and floors

### Why the first textures don't work in the game

The corridor is drawn by wrapping these images onto walls and floor in
perspective. A wall right in front of you is only about 160 pixels tall on the
GBA screen; a wall three steps away is about 40. The first textures failed in
three ways:

- **The stone wall is mostly white.** Its blocks turn into white blobs when
  shrunk; there is no mid-tone between the white faces and the black joints.
- **The water is almost all black**, so the floor reads as a hole.
- **They carry their own lighting.** The game adds its own darkness with
  distance, at the top of the vault and near the water; light painted into the
  texture fights it.

### Rules for every texture

Add these lines to the end of every prompt in this section:

```
Texture rules: perfectly flat and front-on (no perspective, no vanishing point),
square, seamlessly tileable on ALL FOUR edges (left matches right, top matches
bottom). Lit EVENLY across the whole image: no vignette, no gradient, no darker
corners, no light source of its own. The overall tone is a MIDDLE grey made only
of black lines on white (about half ink, half paper): every face is hatched with
regular, parallel, evenly spaced lines about 1/80 of the image width apart; no
area is plain white bigger than a stone face's highlight, no area solid black
except the joints. Pure black and white only, no grey pixels.
```

Attach `REF_style_01` to every prompt here. Approve the first stone wall as
`REF_place_wall`, then attach it as well to every other wall prompt so the stone
matches.

### 4a. Stone wall (the main wall)

`assets/raw/wall_stone.png` · square · seamless · attach `REF_style_01` · approve as `REF_place_wall`

```
Texture: an ancient abbey wall of dressed stone blocks, front-on. Exactly four
horizontal courses of blocks from top to bottom and about three blocks per
course, staggered like brickwork. Thick black mortar joints. Every block face
is hatched with horizontal engraved lines that follow the course, a little
denser towards the lower edge of each block (its shadow side), with a thin
white chamfer along the top edge of each block. Worn corners, a few cracks and
chips, no moss, no carvings.
```

### 4b. Stone wall, decayed (variant)

`assets/raw/wall_stone_b.png` · square · seamless · attach `REF_style_01`, `REF_place_wall`

```
Texture: the SAME wall as REF_place_wall (same courses, same block size, same
hatching, same tone), but older and wetter: two or three blocks cracked through,
one block missing a corner, dark water stains running down in vertical streaks
of denser hatching, a few roots in the joints. It must tile with REF_place_wall
side by side.
```

### 4c. Wall with a lancet window

`assets/raw/wall_window.png` · square · attach `REF_style_01`, `REF_place_wall`

```
Texture: the SAME stone wall as REF_place_wall, front-on, with one tall narrow
pointed gothic lancet window in the centre, taking up about a third of the
width and three quarters of the height, a thin stone mullion splitting it and a
moulded stone frame. Through the window: bare white light, almost blank paper
crossed by a few thin horizontal lines. The stone around it keeps the same
middle tone as REF_place_wall, so the window is the only large bright shape.
The left and right edges tile with REF_place_wall.
```

### 4d. Wall with a carved niche (variant)

`assets/raw/wall_niche.png` · square · attach `REF_style_01`, `REF_place_wall`

```
Texture: the SAME stone wall as REF_place_wall, front-on, with a shallow pointed
niche carved into the centre, holding a small weathered statue of a hooded saint
with its face worn away and its hands folded. The niche's back is dark, densely
cross-hatched; the statue is lit evenly and hatched like the stone. The left and
right edges tile with REF_place_wall.
```

### 4e. Flooded floor

`assets/raw/floor_water.png` · square · seamless · seen from above · attach `REF_style_01`

```
Texture, seen from directly above: a stone floor of large square flagstones
under a few inches of still black water. The flagstone joints are visible
through the water as thick dark lines in a regular grid, three flagstones
across. The water is drawn with long horizontal engraved lines, evenly spaced,
broken here and there by short white ripple glints; overall a middle tone, NOT
solid black: half ink, half paper.
```

### 4f. Dry floor (variant)

`assets/raw/floor_stone.png` · square · seamless · seen from above · attach `REF_style_01`, `REF_place_wall`

```
Texture, seen from directly above: the dry stone floor of the same abbey, large
square worn flagstones, three across, with thick dark joints, matching the
stone of REF_place_wall. Each flagstone hatched with parallel lines in a
slightly different direction, a few cracks, a little grit in the joints.
```

### 4g. Vaulted ceiling (optional)

`assets/raw/ceiling_vault.png` · square · seamless · seen from below · attach `REF_style_01`

```
Texture, seen from directly below: the underside of a ribbed gothic vault,
the stone ribs crossing as a regular diagonal lattice of thick bands, the
panels between them densely cross-hatched almost to black, the ribs lighter and
hatched along their length. Dark overall: about three quarters ink.
```

Right now the vaults above the walls are drawn plain black; with this texture
the game can show them.

### Check before approving a texture

1. **Shrink it to a 64 × 64 thumbnail.** It should still read as stone or
   water, and look an even middle grey, not mostly white and not mostly black.
2. **Tile it.** Put four copies in a 2 × 2 grid: there must be no visible seam
   and no repeating dark corner.
3. **Check that every texture is a similar middle tone** (the window's opening
   is the one exception). The game's fog provides all the light and shadow.

---

## How the game will use them

| Moment | Frames |
|---|---|
| Exploring, at rest | gauntlet (left) and `arm_sword` (right), as now |
| Drinking (B) | `flask_hold_N` → `flask_drink` → `flask_hold_N-1` → gauntlet |
| Pressing S early | `block_1` → `block_2`, held until the blow; on impact `block_3` |
| Perfect parry | `parry_1` → `parry_2` (+ spark, white flash) → `parry_3` → rest |
| The flask on screen | at rest, the gauntlet shows no flask; the level is seen each time you drink |
| The corridor | walls mix `wall_stone` and `wall_stone_b`; `W` cells use `wall_window`; the floor is `floor_water` (or `floor_stone` in dry areas); `wall_niche` and the ceiling as features once the map editor has cells for them |

## What to send me

Save each final image in `assets/raw/` under the file name given above, then
upload it here or commit it. Approved references (`REF_char_gauntlet`,
`REF_char_flask`) can also go in `assets/refs/`.

**Files expected:** `gauntlet.png` (replacement), `flask.png`,
`flask_hold_3.png`, `flask_hold_2.png`, `flask_hold_1.png`, `flask_hold_0.png`,
`flask_drink.png`, `block_1.png`, `block_2.png`, `block_3.png`, `parry_1.png`,
`parry_2.png`, `parry_3.png`, optionally `parry_spark.png`; and for the
dungeon `wall_stone.png` (replacement), `wall_stone_b.png`, `wall_window.png`
(replacement), `wall_niche.png`, `floor_water.png` (replacement),
`floor_stone.png`, and optionally `ceiling_vault.png`.
