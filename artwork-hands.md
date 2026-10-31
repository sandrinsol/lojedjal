# SEPTEM: artwork prompts, round 2 (hands, flask, block and parry)

New prompts for the ChatGPT Project, in the same style and with the same
reference library as `artwork.md`. They cover:

1. **The left gauntlet, redrawn.** The current one reads as a right hand.
2. **The healing flask:** the left hand drinking from it, with the blood inside
   shown full, two-thirds full and one-third full, so the flask itself shows
   how many draughts are left.
3. **Block and parry:** the right arm and sword raising a guard, taking a blow,
   and turning a blow aside with a perfect parry.

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

## How the game will use them

| Moment | Frames |
|---|---|
| Exploring, at rest | gauntlet (left) and `arm_sword` (right), as now |
| Drinking (B) | `flask_hold_N` → `flask_drink` → `flask_hold_N-1` → gauntlet |
| Pressing S early | `block_1` → `block_2`, held until the blow; on impact `block_3` |
| Perfect parry | `parry_1` → `parry_2` (+ spark, white flash) → `parry_3` → rest |
| The flask on screen | at rest, the gauntlet shows no flask; the level is seen each time you drink |

## What to send me

Save each final image in `assets/raw/` under the file name given above, then
upload it here or commit it. Approved references (`REF_char_gauntlet`,
`REF_char_flask`) can also go in `assets/refs/`.

**Files expected:** `gauntlet.png` (replacement), `flask.png`,
`flask_hold_3.png`, `flask_hold_2.png`, `flask_hold_1.png`, `flask_hold_0.png`,
`flask_drink.png`, `block_1.png`, `block_2.png`, `block_3.png`, `parry_1.png`,
`parry_2.png`, `parry_3.png`, and optionally `parry_spark.png`.
