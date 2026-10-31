# SEPTEM: artwork prompts for GPT image generation

Prompts for generating SEPTEM's art in a ChatGPT Project. The game shows
everything at **240 × 160 pixels in three colours**, so these prompts ask for
images that survive that reduction: bold, widely spaced engraving lines, big
shapes, and strong black/white masses. Fine Doré-style hairlines would turn
to grey mush.

## How to use this file

1. Create a ChatGPT Project named **SEPTEM**.
2. Paste the **Project instructions** block below into the project's
   instructions. Every chat in the project then inherits the style.
3. Build the **reference library** first (see below): a style anchor, then one
   anchor per character. Each image you approve goes into the project's files
   (its sources) under a fixed `REF_` name, so every later chat can follow it.
4. Generate each asset in its own chat with the prompt from its section,
   **attaching the references listed for it**.
5. Put the results in `assets/raw/` in the repo with the file name given for
   each asset. I'll reduce them to 3 colours and GBA size, clean the pixels up and
   wire them into the game.

Ask for **PNG**. Ask for a **transparent background** wherever a section says
"cut-out".

---

## Project instructions (paste into the ChatGPT Project)

```
You are the illustrator for SEPTEM, a dark fantasy game. Every image you make
is a 19th-century wood engraving in the manner of Gustave Doré's illustrations
for the Bible and Dante's Inferno, brought to a Game Boy Advance screen.

STYLE (always)
- Pure engraving: every tone is built only from black lines on white paper:
  parallel hatching, cross-hatching, and lines that follow the form (contour
  hatching). Lines swell where the shadow deepens and taper into the light.
- Strong chiaroscuro as in Doré: deep, solid black masses; a few areas of bare
  white paper where light falls; dramatic light from one source.
- BOLD and COARSE: lines must be thick and widely spaced, roughly 1/100 of the
  image width apart, so the picture still reads when shrunk to 240x160 pixels.
  Large, simple silhouettes. Few, big shapes.
- Colour: ONLY pure black #000000 and pure white #FFFFFF. Blood red #D00024 is
  allowed ONLY where the prompt asks for it, as flat red with no shading.
  No grey, no tint, no paper colour, no sepia, no gradients, no blur, no glow,
  no soft shading, no texture noise.
- Subjects: gothic medieval architecture, ruined cathedrals, crypts, flooded
  abbeys, fallen angels, grotesque demons, undead knights, religious symbolism.
- Mood: oppressive, mysterious, solemn, violent, ancient, supernatural.

NEVER
anime, manga, cartoon, comic-book or cel shading, vector or flat illustration,
generic fantasy concept art, modern digital painting, airbrush, smooth
gradients, 3D render, photorealism, lens effects, bloom, excessive ornament,
filigree for its own sake, random small details, text, letters, signatures,
watermarks, frames or borders (unless asked).

REFERENCES (the project's files)
- Files named REF_*.png in this project are approved SEPTEM art. They are the
  canon: match them before anything written here.
- REF_style_*: match their line weight, line spacing, amount of solid black,
  and how light falls. Do not copy their composition or subject.
- REF_char_* and REF_place_*: the approved design of a character or place.
  Keep its proportions, silhouette, costume, props and face exactly; change
  only the pose, angle or framing the prompt asks for.
- SEPTEM_canon.md lists every reference and the traits that must not change.
  Follow it.
- When images are attached to a message, they take priority over project
  files. If a prompt names a REF_ file that is not attached, use the project
  file of that name.
- Never mix two characters' designs. Never invent a new design for a
  character that already has a REF_char_ file.

OUTPUT
- Square or 3:2 as asked, PNG.
- Cut-outs: the subject alone on a fully transparent background, nothing
  touching the edges unless asked, a clean closed black outline around it.
- Never add colour beyond black, white and the requested blood red.
```

---

## Reference library

Consistency comes from approved images, not from longer prompts. Every image
you approve becomes a reference that the following ones must match.

### Naming

| Kind | File name | What it fixes |
|---|---|---|
| Style anchor | `REF_style_01.png`, `REF_style_02.png` | Line weight, spacing, black density, lighting. Two or three in total, no more. |
| Character | `REF_char_monk.png`, `REF_char_sloth.png`, `REF_char_gauntlet.png`, `REF_char_arm.png` | The design of one character or prop, in its neutral pose |
| Place | `REF_place_abbey.png` | The architecture and mood of a stage |
| The canon | `SEPTEM_canon.md` | A text file listing the references and their fixed traits |

### Build it in this order

1. **Style anchor.** Generate the corridor reference shot (2e) and the title
   (1). Iterate until one is exactly right, then save it as
   `REF_style_01.png` and upload it to the project's files. A second anchor
   with a figure in it (the Somnolent Monk idle, 4a) makes `REF_style_02.png`.
2. **Characters.** For each character, generate the idle or neutral pose with
   `REF_style_01` attached. When it's right, save it as `REF_char_<name>.png`
   and upload it. Every other pose of that character is then made from it.
3. **Places.** The stage card (2a) becomes `REF_place_abbey.png`; the shrine
   and textures of that stage use it.
4. After each approval, add a line to `SEPTEM_canon.md` and re-upload it.

### Attach the references in the chat too

Image generation does not always look at project files on its own, so the
reliable way is to **attach the listed references to the message** each time,
as well as keeping them in the project files. Attach at most three: the style
anchor, plus the character or place reference.

### The approval prompt

When an image is right, before saving it, ask in the same chat:

```
This image is approved as canon for SEPTEM. In 5 to 8 short bullet points,
list the traits that must stay identical in every future image of this
character / place / style (silhouette, proportions, costume, props, face,
line weight, black density, light direction). No commentary.
```

Paste the answer into `SEPTEM_canon.md` under the reference's name.

### SEPTEM_canon.md template

Start the file with this, then fill it in as you approve images:

```
# SEPTEM canon: approved references

All images: Doré wood engraving, bold coarse lines, black and white only,
blood red #D00024 only where named.

## REF_style_01 (corridor)
- (traits from the approval prompt)

## REF_char_monk (Somnolent Monk, idle)
- (traits from the approval prompt)
```

### Which references each asset uses

| Asset | Attach |
|---|---|
| 1 Title, 2a Stage card, 6 Shrine, 7 Death screen | `REF_style_01`, `REF_place_abbey` (once it exists) |
| 2b–2d Textures | `REF_style_01`, `REF_place_abbey` |
| 2e Corridor shot | — (it becomes `REF_style_01`) |
| 3a Gauntlet | `REF_style_01` → approve as `REF_char_gauntlet` |
| 3b Arm with sword | `REF_style_01`, `REF_char_gauntlet` (same hands) → approve as `REF_char_arm` |
| 3c Strike poses | `REF_style_01`, `REF_char_arm` |
| 4a Monk idle | `REF_style_01` → approve as `REF_char_monk` (and `REF_style_02`) |
| 4a Monk poses | `REF_style_02`, `REF_char_monk` |
| 4b Moth-Wraith, 4c Chained Sleeper | `REF_style_02` → approve as `REF_char_wraith` / `REF_char_sleeper`, then their poses with those |
| 5 Sloth | `REF_style_02`, `REF_place_abbey` → approve as `REF_char_sloth`, then its poses with it |
| 8 Small graphics | `REF_style_01`, plus `REF_char_gauntlet` for the gem |

### Lines to start a prompt with

New design, following the style:

```
Attached: REF_style_01 (style only). Match its line weight, line spacing,
black density and lighting exactly. Do not copy its composition or subject.
```

A new pose of an approved character:

```
Attached: REF_style_02 (style) and REF_char_monk (design). This is the same
character: keep the proportions, silhouette, costume, props and face
identical, as listed in SEPTEM_canon.md. Change only the pose described below.
```

### When it drifts anyway

- Re-attach the references and say:
  `Compare your image with the attached references and redraw it so the line weight, line spacing and design match them exactly.`
- If a chat keeps drifting, start a fresh chat in the project: long chats
  slowly lose the style.
- Don't approve "nearly right" images as references: their errors get copied
  into everything after them.

---

## Reusable prompt pieces

Paste these at the end of any prompt when a result drifts:

- **Drifting to grey or too fine:**
  `Redraw with thicker, more widely spaced engraving lines and only pure black and pure white. No grey at all. Simplify the shapes.`
- **Drifting to cartoon:**
  `Make it a 19th-century wood engraving like Gustave Doré's Bible: solemn, anatomical, heavy chiaroscuro. No cartoon or comic shading.`
- **Too busy:**
  `Remove small ornaments and incidental details. Keep only the large forms and the light.`
- **Red spreading:**
  `Blood red #D00024 only where I asked; everything else strictly black and white.`
- **Character changing design:**
  `Keep the character exactly as in the attached REF_char image: same proportions, costume, props and face. Change only the pose.`

---

## 1. Title screen

`assets/raw/title.png` · 3:2 landscape · full scene · attach `REF_style_01`

```
Title screen for SEPTEM. A colossal ruined gothic cathedral nave seen from the
floor, flooded with still black water. Seven broken pointed arches recede into
darkness. A single shaft of white light falls from a shattered rose window
high above onto a lone hooded figure standing knee-deep in the water, seen
from behind, tiny against the architecture. The upper third is solid black
vaulting where the word SEPTEM will be placed later: leave that area as empty
black. 3:2 landscape, bold coarse engraving lines, pure black and white only.
```

## 2. Stage I: The Drowned Abbey (scenes and textures)

### 2a. Stage card

`assets/raw/sloth_card.png` · 3:2 landscape · full scene · attach `REF_style_01` · approve as `REF_place_abbey`

```
Stage card for "Sloth: the Drowned Abbey". The flooded interior of a
Romanesque-gothic abbey church: columns rising out of black water, monks
sitting motionless along the walls with their heads bowed, cowls pulled low,
some half submerged, as if asleep for centuries. Moths drift in the single
beam of light from a narrow lancet window. Stillness, dread, heaviness.
3:2 landscape, bold engraving, pure black and white only.
```

### 2b. Wall texture: ashlar stone

`assets/raw/wall_stone.png` · attach `REF_style_01`, `REF_place_abbey` · square · flat, front-on, seamless

```
A flat, front-on, seamlessly tileable texture of an ancient abbey wall: large
rough-cut stone blocks in staggered courses, worn edges, dark mortar joints,
the lowest course soaked and darker from flood water. Lit evenly from the
upper left. Drawn as a bold wood engraving with horizontal hatching following
the courses. No perspective, no vignette, no shadows at the edges, edges must
tile. Square, pure black and white only.
```

### 2c. Wall texture: lancet window

`assets/raw/wall_window.png` · attach `REF_style_01`, `REF_place_abbey` · square · flat, front-on

```
The same abbey stone wall, front-on and flat, with one tall narrow pointed
gothic lancet window in the centre, a thin stone mullion splitting it, and a
moulded frame. Through the window: bare white light, almost blank paper with a
few thin horizontal lines. The surrounding stone is in shadow and densely
hatched so the window glows by contrast. No perspective. Square, pure black
and white only.
```

### 2d. Floor: still flood water

`assets/raw/floor_water.png` · attach `REF_style_01`, `REF_place_abbey` · square · flat, seen from above

```
Seen from directly above: still black flood water over a stone floor. Drawn
only with long horizontal engraved lines whose thickness swells and thins to
suggest slow ripples, with a few short white glints. Seamlessly tileable,
no perspective. Square, pure black and white only.
```

### 2e. Corridor reference shot

`assets/raw/corridor_ref.png` · 3:2 landscape · full scene

This one is a look-and-feel reference for the 3D view, not a game asset. Make
it first: once approved it becomes `REF_style_01`, the style anchor for
everything else.

```
First-person view down a narrow flooded corridor of a gothic abbey, eye level
just above the water. Stone walls of big blocks recede to a vanishing point,
the far end lost in solid black. One lancet window on the left wall throws a
pale shape of light on the water. Dark foreground, lit middle distance, black
depths, as Doré stages his scenes. Bold engraving, pure black and white only,
3:2 landscape.
```

## 3. The player's hands (the HUD)

There is no HUD: the hands are the interface. Both are drawn as cut-outs and
placed in the bottom corners of the screen.

### 3a. Left gauntlet with the three mana gems

`assets/raw/gauntlet.png` · square · cut-out · attach `REF_style_01` · approve as `REF_char_gauntlet`

```
Cut-out: a left hand in a battered medieval plate gauntlet, seen from the
wearer's own point of view, raised palm-away with the fingers slightly spread
and curled, the forearm entering from the bottom-left corner of the image.
Riveted articulated finger plates, a flared cuff. Set into the knuckle plate:
three round gems in a row, drawn as flat blood red #D00024 with a tiny white
glint and a black bezel; the rest of the image is black and white only. Bold
engraving, strong black outline, transparent background, the arm touches only
the bottom-left edge.
```

Variant for spent mana, same composition:

```
Same gauntlet, same pose and framing, but the three gem sockets are empty:
black hollows with a thin white rim. No red at all.
```

### 3b. Right arm with sword and death brand

`assets/raw/arm_sword.png` · square · cut-out · attach `REF_style_01`, `REF_char_gauntlet` · approve as `REF_char_arm`

```
Cut-out: a right forearm and fist seen from the wearer's own point of view,
the bare inner forearm towards the viewer, entering from the bottom-right
corner. A ragged dark sleeve at the elbow, linen strips wrapped around the
wrist. The fist grips a long straight medieval longsword held upright, the
blade rising towards the top-right of the image, with a plain cruciform
crossguard and a central groove (fuller) on the blade. On the pale skin of the
inner forearm, a burned-in Roman numeral "III" in flat blood red #D00024 with a
black scorched edge. Everything else pure black and white. Bold engraving,
transparent background.
```

### 3c. Strike: four poses

`assets/raw/strike_1.png` … `strike_4.png` · square · cut-out, same arm as 3b

Attach `REF_style_01` and `REF_char_arm` for all four.

```
Same right arm and longsword as the attached image, same style. Pose 1 of a
sword strike, seen from the wearer's point of view: WIND-UP. The arm is raised
high on the right, the blade cocked back over the shoulder towards the top-right
corner. Transparent background, black and white only.
```

```
Pose 2: THE CUT. The arm sweeps across the image, the blade flat and
horizontal across the centre, pointing left. Behind the blade, a fan of curved
engraved speed lines marks the arc of the swing. Transparent background, black
and white only.
```

```
Pose 3: FOLLOW-THROUGH. The blade has passed through and points down to the
bottom-left corner; the arm crosses the lower part of the image. A short tail
of curved speed lines. Transparent background, black and white only.
```

```
Pose 4: RECOVERY. The arm comes back up, the blade nearly upright near the
centre-right, returning to guard. Transparent background, black and white only.
```

## 4. Enemies of Stage I

Enemies are seen face-on, filling most of the view during a duel. For each one:
an idle pose, a wind-up, a strike, a staggered pose (after you parry), and a
death. Make the idle pose first with `REF_style_02` (or `REF_style_01` for
the monk, the first figure); approve it as `REF_char_<name>`, then make every
other pose with that file attached.

### 4a. Somnolent Monk

`assets/raw/monk_idle.png`, `monk_windup.png`, `monk_strike.png`, `monk_stagger.png`, `monk_death.png` · square · cut-out · idle: attach `REF_style_01`, approve as `REF_char_monk` and `REF_style_02`

```
Cut-out, full figure, facing the viewer: a SOMNOLENT MONK, an undead monk who
has slept standing in a flooded abbey for centuries. Enormous, hunched, heavy;
a sodden black cowl hangs over a face that is only a slack grey jaw and closed,
sunken eyes. Bloated hands drag a huge iron censer on a chain. Water drips
from the hem of the robe. Slow, crushing, terrible. Bold engraving with deep
blacks in the robe folds, a few white highlights on the hands and the jaw.
Pure black and white, transparent background, the hem of the robe reaching the
bottom edge.
```

Poses (attach `REF_style_02` and `REF_char_monk`):

```
Same Somnolent Monk. WIND-UP: he lifts the iron censer slowly overhead with
both arms, the chain taut, his head lolling to one side, eyes still closed.
Same framing and style, transparent background.
```

```
Same Somnolent Monk. STRIKE: the censer comes crashing down towards the viewer,
large in the foreground, the monk lurching forward. Short engraved motion lines
behind the censer. Same framing, transparent background.
```

```
Same Somnolent Monk. STAGGERED: knocked off balance by a parry, the censer
swinging away, the body twisting back, one hand flung out, the cowl slipping to
reveal more of the slack face. Same framing, transparent background.
```

```
Same Somnolent Monk. DEATH: collapsing forward onto his knees in the water,
head sunk, robe spreading; a spill of flat blood red #D00024 from under the
cowl is the only colour. Same framing, transparent background.
```

### 4b. Moth-Wraith

`assets/raw/wraith_idle.png` (+ windup / strike / stagger / death) · square · cut-out · attach `REF_style_02` · approve as `REF_char_wraith`

```
Cut-out: a MOTH-WRAITH, a gaunt, almost weightless phantom of a nun whose torn
veils have become huge dusty moth wings, spread wide. A skeletal face with
hollow eyes, long thin fingers ending in hooks. Floating above the water, the
lower body dissolving into strands. Delicate but menacing. Bold engraving,
the wings hatched with radiating lines and pale eye-spot patterns in white.
Pure black and white, transparent background.
```

### 4c. Chained Sleeper

`assets/raw/sleeper_idle.png` (+ windup / strike / stagger / death) · square · cut-out · attach `REF_style_02` · approve as `REF_char_sleeper`

```
Cut-out: a CHAINED SLEEPER, a gigantic emaciated penitent bound to a broken
pillar by heavy chains around the chest and wrists, head drooping in sleep,
long matted hair hiding the face. When it wakes it swings the loose ends of
its chains. Bold engraving, emphasising the iron chains with strong white
highlights against the dark body. Pure black and white, transparent
background, the pillar base at the bottom edge.
```

## 5. Boss: SLOTH

`assets/raw/sloth_idle.png` (+ the poses below) · square or 3:2 · cut-out · attach `REF_style_02`, `REF_place_abbey` · approve as `REF_char_sloth`

```
Cut-out, boss: SLOTH, the first of the Seven Sins. A colossal bloated figure,
half man, half drowned idol, enthroned on a mound of sleeping bodies heaped
in black water. Pale swollen flesh in great folds, a tiny crowned head sunk
into the shoulders, eyes heavy-lidded and half open, a lazy terrible smile.
One immense arm hangs limp over the side of the throne, fingers trailing in
the water. Moths circle the crown. Monumental, grotesque, solemn, in the
manner of Doré's demons. Bold engraving, deep blacks under the folds, white
light only on the brow, the crown and the hanging hand. Pure black and white,
transparent background.
```

Poses (attach `REF_style_02` and `REF_char_sloth`):

```
Same SLOTH. SLOW WIND-UP: the hanging arm rises from the water with agonising
slowness, water pouring from it, the palm opening towards the viewer. Same
framing, transparent background.
```

```
Same SLOTH. CRUSHING BLOW: the vast palm slams down towards the viewer,
filling the foreground, the sleeping bodies on the throne stirring.
Engraved motion lines. Same framing, transparent background.
```

```
Same SLOTH. LULLABY: the head tilts back, mouth open in a soundless song;
curling engraved lines like drifting sound and heavy sleep spiral out
from the mouth across the image. Same framing, transparent background.
```

```
Same SLOTH. DEFEATED: the figure sags and slides into the water, the throne of
sleepers awakening and turning their faces up; from the wound in its chest, a
flat blood red #D00024 stream, the only colour. Same framing, transparent
background.
```

## 6. Shrine (end of the stage)

`assets/raw/shrine.png` · 3:2 landscape · full scene · attach `REF_style_01`, `REF_place_abbey`

```
The shrine at the end of the Drowned Abbey: a small apse with a stone altar
rising from the water, one tall candle burning on it with a hard white flame,
the only light, casting long rays across the vault. Above the altar a weathered
relief of an angel with folded wings, its face worn away. Three empty glass
vials stand on the altar. Calm after the dread. Bold engraving, 3:2 landscape,
pure black and white only.
```

## 7. Death screen

`assets/raw/death.png` · 3:2 landscape · full scene · attach `REF_style_01`, `REF_char_arm`

```
Death screen: the lost soul lies face down in the black flood water, arms out,
seen from above. From the right forearm, a burning Roman numeral glows in flat
blood red #D00024, the only colour, reflected faintly as red lines in the water.
Everything else is solid black with a few engraved ripples in white. Leave the
top half empty black. 3:2 landscape.
```

## 8. Small graphics

### 8a. Mana gem, close-up

`assets/raw/gem.png` · square · cut-out · attach `REF_style_01`, `REF_char_gauntlet`

```
Cut-out: a single cabochon gem in a heavy black iron bezel, the stone flat blood
red #D00024 with one small white glint and two black facet lines. Simple, bold,
readable at 16 pixels. Transparent background.
```

### 8b. Health vial

`assets/raw/vial.png` · square · cut-out · attach `REF_style_01`

```
Cut-out: a small medieval glass vial of blessed blood, stoppered with wax,
a tag of cloth tied at the neck. The liquid is flat blood red #D00024, the
glass drawn in black engraved lines with sharp white highlights. Readable at
16 to 24 pixels. Transparent background.
```

### 8c. Seven Sins sigils (for the stage select and boss doors)

`assets/raw/sigil_sloth.png` (then pride, greed, wrath, envy, gluttony, lust) · square · cut-out · attach `REF_style_01`; approve the first as `REF_char_sigil` and attach it for the other six

```
Cut-out: a heraldic sigil for the sin of SLOTH, carved in stone like a relief on
a cathedral door: a coiled sleeping serpent around a snuffed candle, inside a
pointed gothic quatrefoil. Bold engraving, pure black and white, transparent
background, readable at 32 pixels.
```

---

## What to send me

Put each final image in `assets/raw/` under its asset name (not the `REF_`
name). The `REF_` files are for ChatGPT; you can also commit them to
`assets/refs/` so the canon is kept with the game.

## What happens to your images

The game can only show three colours and a 240 × 160 screen, so each image
goes through a conversion step in the repo:

| Asset | In-game size |
|---|---|
| Full scenes (title, stage card, shrine, death) | 240 × 160 |
| Wall textures | mapped onto the 3D corridor panels |
| Hands and strike poses | about 104 × 96 each |
| Enemies (duel view) | up to about 128 × 128 |
| Boss | up to about 200 × 150 |
| Gem, vial | 16 × 16 / 24 × 24 |
| Sigils | 32 × 32 |

The conversion turns every pixel into black, white or blood red and removes
stray single pixels. Large, bold line work therefore matters more than detail.
If an image looks good as a thumbnail the size of a postage stamp, it will work
in the game.
