# SEPTEM: artwork prompts, round 3

The next images for the ChatGPT Project, in the same style and with the same
reference library as `artwork.md` and `artwork-hands.md`. The project
instructions from `artwork.md` still apply; add nothing new to the project.

| # | Images | What they add to the game |
|---|---|---|
| 1 | Dungeon variety: decayed wall, niche, dry floor, vault | Corridors stop looking identical; landmarks; a ceiling |
| 2 | Parry spark, turn streaks | A spark on a perfect parry; speed lines when turning |
| 3 | WARD casting, 3 frames | The spell has its own animation from the gauntlet |
| 4 | Player death, 3 frames | The fall before the death screen |
| 5 | Somnolent Monk, side views | Monks seen beside your path, not only straight ahead |

**Make them in this order:** 1, 2, 3, 4, 5. Within each section, make the image
marked **anchor** first; the others attach it.

---

## References to attach

| Reference | What it is | Where it comes from |
|---|---|---|
| `REF_style_01` | Corridor style anchor | first round |
| `REF_style_02` | Monk idle, figure style anchor | first round |
| `REF_place_wall` | The approved stone wall (`assets/raw/wall_stone.png`, round 2) | upload it under this name if it isn't in the project yet |
| `REF_char_gauntlet` | The new left gauntlet (`assets/raw/gauntlet.png`, round 2) | upload under this name |
| `REF_char_arm` | The right arm with sword (`assets/raw/arm_sword.png`) | first round |
| `REF_char_monk` | The Somnolent Monk (`assets/raw/monk_idle.png`) | first round |

---

## Framing rules

- **Textures (section 1):** square, flat and front-on, tiling on all four edges,
  evenly lit, an even middle tone made only of hatching. Paste the texture
  rules below at the end of every texture prompt.
- **Hands (sections 3 and 4):** square, cut-out, transparent background, about
  1254 × 1254. The left forearm enters from the **bottom-left** corner, the
  right from the **bottom-right**, at the same place and size as
  `REF_char_gauntlet` and `REF_char_arm`, so frames line up when swapped.
- **Figures (section 5):** square, cut-out, transparent background, feet or
  hem on the bottom edge, the same height as `REF_char_monk`.
- **Blood red #D00024** only where a prompt asks for it: the gems, blood, and
  the forearm numeral. The game finds the gems and the brand by their red.

### Texture rules (paste after every prompt in section 1)

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

---

## 1. Dungeon variety

Attach `REF_style_01` and `REF_place_wall` to every prompt in this section.

### 1a. Stone wall, decayed

`assets/raw/wall_stone_b.png` · square · seamless

```
Texture: the SAME wall as REF_place_wall (same courses, same block size, same
hatching, same tone), but older and wetter: two or three blocks cracked through,
one block missing a corner, dark water stains running down in vertical streaks
of denser hatching, a few roots in the joints. It must tile with REF_place_wall
side by side.
```

### 1b. Wall with a carved niche

`assets/raw/wall_niche.png` · square

```
Texture: the SAME stone wall as REF_place_wall, front-on, with a shallow pointed
niche carved into the centre, holding a small weathered statue of a hooded saint
with its face worn away and its hands folded. The niche's back is dark, densely
cross-hatched; the statue is lit evenly and hatched like the stone. The left and
right edges tile with REF_place_wall.
```

### 1c. Dry stone floor

`assets/raw/floor_stone.png` · square · seamless · seen from above

```
Texture, seen from directly above: the dry stone floor of the same abbey, large
square worn flagstones, three across, with thick dark joints, matching the
stone of REF_place_wall. Each flagstone hatched with parallel lines in a
slightly different direction, a few cracks, a little grit in the joints.
```

### 1d. Vaulted ceiling

`assets/raw/ceiling_vault.png` · square · seamless · seen from below

```
Texture, seen from directly below: the underside of a ribbed gothic vault,
the stone ribs crossing as a regular diagonal lattice of thick bands, the
panels between them densely cross-hatched almost to black, the ribs lighter and
hatched along their length. Dark overall: about three quarters ink.
```

(For the ceiling only, replace "MIDDLE grey … half ink" in the texture rules
with "DARK: about three quarters ink".)

**Before approving a texture:**
1. Shrink it to 64 × 64: it should still read as stone, an even grey.
2. Tile four copies in a 2 × 2 grid: there should be no visible seam.
3. Put it next to `REF_place_wall`: it should be a similar tone.

---

## 2. Effects

### 2a. Parry spark

`assets/raw/parry_spark.png` · square · cut-out · attach `REF_style_01`

```
Cut-out: a burst of light where two weapons clash, engraved like a woodblock
star: eight to twelve sharp straight rays of different lengths radiating from a
small white centre, a broken ring of white sparks around it. Pure white with clean
black outlines, nothing else. Bold, readable at 32 pixels. Transparent
background.
```

### 2b. Turn streaks

`assets/raw/turn_streaks.png` · **3:2 landscape** · cut-out · attach `REF_style_01`

```
Cut-out, wide 3:2: a band of long horizontal engraved speed lines sweeping
across the whole image from edge to edge, densest through the middle third and
thinning towards the top and bottom, each line thick in its middle and tapering
at both ends, broken here and there like a burin lifting off the plate. Pure
black lines only, transparent background, nothing else: no objects, no frame.
```

The game lays this over the view for a few frames while you turn, so it must be
plain lines and nothing else.

---

## 3. WARD: the spell cast from the gauntlet

The left hand raises the gauntlet and one gem burns out into a ward of light.
Three frames, made in one chat so the pose stays consistent.

**Every prompt starts with:**

```
Attached: REF_style_01 (style) and REF_char_gauntlet (the same left hand and
arm, the same plate armour, the same three red gems). The forearm enters from
the bottom-left corner at the same place and size as REF_char_gauntlet. Cut-out,
transparent background, bold engraving, black and white only except where red
is named.
```

### 3a. Raise (anchor)

`assets/raw/ward_1.png`

```
WARD, frame 1, RAISING: the left gauntlet lifts and turns so the palm faces
away from the viewer, fingers spread wide and straight, as if pressing against
an invisible wall. The three gems on the knuckle plate are flat blood red
#D00024; the middle one has a small white glint, beginning to glow.
```

### 3b. The ward forms

`assets/raw/ward_2.png` · attach `ward_1.png` as well

```
WARD, frame 2, THE WARD FORMS: the same raised, spread hand. From the middle
gem a burst of white light spreads outward: a ring of engraved white rays and
a circle of fine concentric lines in front of the palm, like a halo cut into a
woodblock, reaching beyond the fingertips. The middle gem is pure white with a
black outline (its red is spent); the other two stay red.
```

### 3c. The ward holds

`assets/raw/ward_3.png` · attach `ward_1.png` as well

```
WARD, frame 3, THE WARD HOLDS: the same raised hand, the halo now a thin,
steady ring of white with a few sparse rays, as if a pane of light hangs in
front of the palm. The middle gem is a dark empty socket (spent); the other two
stay red.
```

The game recolours the gems to match how much mana you really have, so it
doesn't matter which gem is drawn as spent, as long as the other two stay red.

---

## 4. Player death

Three frames played before the death screen: the view tips forward into the
water. All from the player's eyes.

### 4a. The blow (anchor)

`assets/raw/fall_1.png` · square · cut-out · attach `REF_style_01`, `REF_char_gauntlet`, `REF_char_arm`

```
Attached: REF_style_01 (style), REF_char_gauntlet (left hand) and REF_char_arm
(right arm with sword). Cut-out, first-person, transparent background: struck,
both hands thrown outward and down, the left gauntlet entering from the
bottom-left and opening, the right fist entering from the bottom-right and
loosening its grip on the sword, the sword tilting away. Splashes of flat blood
red #D00024 spattering from the top edge of the image. Bold engraving.
```

### 4b. Falling

`assets/raw/fall_2.png` · 3:2 landscape · full scene · attach `REF_style_01`, `fall_1.png`

```
First-person, full scene: the wearer falls forward. The corridor of the abbey
tilts steeply, the black flood water rushing up to fill the lower two thirds,
the walls leaning in at an angle. The sword drops away into the water at the
lower right, the gauntleted left hand reaching out at the lower left. Bold
engraving, black and white, a few drops of blood red #D00024 in the air.
```

### 4c. Under the water

`assets/raw/fall_3.png` · 3:2 landscape · full scene · attach `REF_style_01`

```
First-person, full scene, face down in the water: almost everything is solid
black. Near the top, the underside of the water's surface as a few broken white
engraved ripples, and a thread of blood red #D00024 drifting across them.
Nothing else. Leave the bottom half empty black.
```

---

## 5. Somnolent Monk, side views

Monks standing beside your path, not straight ahead, are seen side-on. Make the
left-facing one first (**anchor**), then ask for its mirror.

### 5a. Facing left (anchor)

`assets/raw/monk_side.png` · square · cut-out · attach `REF_style_02`, `REF_char_monk`

```
Attached: REF_style_02 (style) and REF_char_monk (design). The SAME Somnolent
Monk, same sodden cowl, same slack sleeping face, same censer on its chain,
same bulk. Turned to stand in PROFILE facing LEFT, as if seen from beside him in
a corridor: hunched, head sunk forward, the censer hanging still from one hand
at his side. Full figure, the hem of the robe on the bottom edge, the same height
in the image as REF_char_monk. Bold engraving, black and white, transparent
background.
```

### 5b. Facing right

`assets/raw/monk_side_r.png` · attach `monk_side.png`

```
Same image, mirrored left to right: the same monk in profile facing RIGHT. Keep
everything else identical.
```

(If the mirror comes out differently, the game can flip `monk_side.png` itself.
Send whatever you get.)

---

## What to send me

Save each final image under the file name given, then upload it as a file here
or commit it to `assets/raw/`.

**Files expected:** `wall_stone_b.png`, `wall_niche.png`, `floor_stone.png`,
`ceiling_vault.png`, `parry_spark.png`, `turn_streaks.png`, `ward_1.png`,
`ward_2.png`, `ward_3.png`, `fall_1.png`, `fall_2.png`, `fall_3.png`,
`monk_side.png`, and optionally `monk_side_r.png`.
