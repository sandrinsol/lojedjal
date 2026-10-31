#!/usr/bin/env python3
"""Imports the generated artwork in assets/raw/ (see artwork.md) as game art.

Each source image is reduced to the game's size and to its three colours
(black, white, blood red #D00024), cut out from its background and outlined
in black so it reads against the corridor. Runs after the procedural
engravers and replaces their output wherever a source image exists.

  hands.png       left gauntlet (raw/gauntlet.png); its red gems stay in the
                  art, spent gems are covered by the gem sprite
  left_1..6.png   left hand with the flask: held with 0..3 draughts left
                  (raw/flask_hold_N), drinking (flask_drink, flask_drink_0)
  arm_0..10.png   right arm: rest (raw/arm_sword.png), strike_1..4,
                  block_1..3, parry_1..3
                  (the baked-in "III" is erased: the game brands the real count)
  gem.png         2 frames: lit (empty: the gauntlet's own gem shows) / spent
  monk.png        Somnolent Monk duel poses, 128x128 in 64x64 quadrants
  monk_far.png    the idle monk 2, 3 and 4 cells away
  title.png       raw/title.png with SEPTEM cut in white
  death.png       raw/death.png, shown when the player falls

Positions the game needs (gem centres, brand centre) are measured from the
art and written to include/gen/septem_layout.h.
"""

import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engrave_sprites import BLACK, RED, SERIF, T, WHITE, save  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, 'assets', 'raw')

# Where the hands sit: (left, top, size) of each square source on screen.
GAUNTLET = (-14, 58, 112)
FLASK = (-24, 14, 150)     # the flask held up: larger, nearer the middle
ARM = (80, 0, 168)

MONK_POSES = ['idle', 'windup', 'strike', 'stagger', 'death']


def have(name):
    return os.path.exists(os.path.join(RAW, f'{name}.png'))


def load(name, background='alpha'):
    """Source image -> lightness (0 black .. 1 white), red mask, opacity."""
    im = np.asarray(Image.open(os.path.join(RAW, f'{name}.png')).convert('RGBA')).astype(np.float64) / 255
    rgb, alpha = im[..., :3], im[..., 3]
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    # Blood red in any shade: bright gems, dark burned numerals.
    red = (r > 0.25) & (r - g > 0.18) & (r - b > 0.14)
    # Semi-transparent parts (a robe drawn see-through) keep their own tones.
    light = 0.299 * r + 0.587 * g + 0.114 * b
    opaque = alpha > 0.06
    if background == 'ink':
        # Black ink kept only as alpha: white paper is transparent.
        light = light * alpha + (1 - alpha)
        opaque = figure_on_white(light)
    elif background == 'black':
        opaque = figure_on_black(light)
    elif background == 'none':
        opaque = np.ones_like(alpha, bool)
    return light, red & opaque, opaque


def figure_on_black(light):
    """Separate a figure drawn on a black background: the black connected to
    the top and upper sides of the image is background."""
    small = np.asarray(Image.fromarray((light * 255).astype(np.uint8)).resize(
        (light.shape[1] // 4, light.shape[0] // 4), Image.BOX)) / 255.0
    dark = small < 0.16
    labels, _ = ndimage.label(dark)
    h, w = dark.shape
    seeds = set(labels[0, :]) | set(labels[: h * 2 // 5, 0]) | set(labels[: h * 2 // 5, -1])
    seeds.discard(0)
    bg = np.isin(labels, list(seeds))
    bg = ndimage.binary_opening(bg, iterations=1)
    big = np.asarray(Image.fromarray(bg.astype(np.uint8) * 255).resize(
        (light.shape[1], light.shape[0]), Image.NEAREST)) > 127
    return ~big


def figure_on_white(light):
    """Separate a figure drawn on white paper: the white connected to the
    image border (through gaps narrower than the outline) is background."""
    small = np.asarray(Image.fromarray((light * 255).astype(np.uint8)).resize(
        (light.shape[1] // 4, light.shape[0] // 4), Image.BOX)) / 255.0
    paper = ~ndimage.binary_dilation(small < 0.7, iterations=1)
    labels, _ = ndimage.label(paper)
    seeds = set(labels[0, :]) | set(labels[-1, :]) | set(labels[:, 0]) | set(labels[:, -1])
    seeds.discard(0)
    bg = ndimage.binary_dilation(np.isin(labels, list(seeds)), iterations=1)
    big = np.asarray(Image.fromarray(bg.astype(np.uint8) * 255).resize(
        (light.shape[1], light.shape[0]), Image.NEAREST)) > 127
    return ~big


def reduce(light, red, opaque, size, threshold=0.5, red_cover=0.3):
    """Downscale to `size` (w, h) and quantise to the palette indices."""
    def shrink(a):
        return np.asarray(Image.fromarray((a * 255).astype(np.uint8)).resize(size, Image.BOX)) / 255.0
    cover = shrink(opaque.astype(np.float64))
    lit = shrink(light * opaque) / np.maximum(cover, 1e-3)
    redness = shrink(red.astype(np.float64))
    out = np.full(lit.shape, T, np.uint8)
    inside = cover > 0.5
    out[inside] = np.where(lit[inside] > threshold, WHITE, BLACK)
    out[inside & (redness > red_cover)] = RED
    # Lone white or black pixels are noise at this size, not engraving.
    for colour, other in ((WHITE, BLACK), (BLACK, WHITE)):
        m = out == colour
        lonely = m & (ndimage.convolve(m.astype(int), np.ones((3, 3), int), mode='constant') == 1)
        out[lonely & inside] = other
    return out


def outline(c, width=1):
    m = c != T
    c[ndimage.binary_dilation(m, iterations=width) & ~m] = BLACK
    return c


def place(img, left, top):
    """Paste a screen-space image into a 256x256 BG canvas (screen at 8, 48)."""
    c = np.zeros((256, 256), np.uint8)
    h, w = img.shape
    X, Y = left + 8, top + 48
    x0, y0 = max(0, -X), max(0, -Y)
    x1, y1 = min(w, 256 - X), min(h, 256 - Y)
    region = img[y0:y1, x0:x1]
    dst = c[Y + y0:Y + y1, X + x0:X + x1]
    dst[region != T] = region[region != T]
    # Keep nothing below the visible screen: the BG wraps around.
    c[48 + 160:, :] = T
    c[:, 8 + 240:] = T
    return c


def red_blobs(img):
    labels, n = ndimage.label(img == RED)
    blobs = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(labels == i)
        blobs.append((len(xs), xs.min(), ys.min(), xs.max(), ys.max()))
    return sorted(blobs, reverse=True)


# ---------------------------------------------------------------------------

# Left-hand frames: the gauntlet at rest, then the flask held up with 0..3
# draughts left, then drinking (with blood flowing, and the last one gone).
LEFT_FRAMES = ['gauntlet', 'flask_hold_0', 'flask_hold_1', 'flask_hold_2', 'flask_hold_3',
               'flask_drink', 'flask_drink_0']


def find_gems(img, name):
    """The gauntlet's three gems: round red blobs of similar size on the
    knuckles, left of anything else red (the flask's blood is on the right)."""
    blobs = []
    for size, x0, y0, x1, y1 in red_blobs(img):
        w, h = x1 - x0 + 1, y1 - y0 + 1
        if 4 <= size and 0.5 <= w / h <= 2.0 and max(w, h) <= img.shape[1] * 0.12:
            blobs.append((size, x0, y0, x1, y1))
    blobs = sorted(blobs, key=lambda b: (b[1] + b[3]) / 2)
    # Keep the three leftmost blobs of a gem's size.
    big = sorted(blobs, reverse=True)[:6]
    sizes = sorted(b[0] for b in big)
    floor = sizes[len(sizes) // 2] * 0.35 if sizes else 0
    gems = [b for b in blobs if b[0] >= floor][:3]
    if len(gems) != 3:
        raise SystemExit(f'{name}: expected 3 red gems, found {len(gems)}')
    return gems


def left_hand():
    """hands.png and flask_*.png BGs; gem centres (screen) for every frame."""
    all_centres = []
    radius = 0
    for i, name in enumerate(LEFT_FRAMES):
        left, top, s = GAUNTLET if i == 0 else FLASK
        img = outline(reduce(*load(name), (s, s), threshold=0.45, red_cover=0.25))
        gems = find_gems(img, name)
        save(place(img, left, top), 'hands.png' if i == 0 else f'left_{i}.png')
        all_centres.append([(left + (b[1] + b[3]) / 2, top + (b[2] + b[4]) / 2) for b in gems])
        if i == 0:
            radius = max(max(b[3] - b[1], b[4] - b[2]) for b in gems) / 2 + 1
    return all_centres, radius


def spent_gem(radius):
    """2 frames, 16x16: lit (empty) and spent (a black hollow, thin white rim)."""
    c = np.zeros((32, 16), np.uint8)
    ys, xs = np.mgrid[0:16, 0:16] + 0.5
    d = np.hypot(xs - 8, ys - 8)
    hollow = d <= radius + 0.6
    frame = c[16:]
    frame[hollow] = BLACK
    frame[hollow & (d > radius - 0.6) & (ys < 8)] = WHITE
    save(c, 'gem.png')


def arms():
    left, top, s = ARM
    brand = None
    frames = ['arm_sword'] + [f'strike_{i}' for i in range(1, 5)] + \
             [f'block_{i}' for i in range(1, 4)] + [f'parry_{i}' for i in range(1, 4)]
    for i, name in enumerate(frames):
        img = outline(reduce(*load(name), (s, s), threshold=0.5, red_cover=0.12))
        blobs = red_blobs(img)
        if blobs:
            # Erase each painted mark on its own (bare skin, ready for the
            # real brand), so stray red specks don't blank a large box.
            for _, bx0, by0, bx1, by1 in blobs:
                box = img[max(0, by0 - 1):by1 + 2, max(0, bx0 - 1):bx1 + 2]
                box[box != T] = WHITE
            if i == 0:
                x0 = min(b[1] for b in blobs)
                y0 = min(b[2] for b in blobs)
                x1 = max(b[3] for b in blobs)
                y1 = max(b[4] for b in blobs)
                brand = (left + (x0 + x1) / 2, top + (y0 + y1) / 2)
        save(place(img, left, top), f'arm_{i}.png')
    if brand is None:
        raise SystemExit('arm_sword: no red brand found to measure')
    return brand


def monk():
    frames = []
    for pose in MONK_POSES:
        bg = {'idle': 'black', 'stagger': 'ink'}.get(pose, 'alpha')
        img = outline(reduce(*load(f'monk_{pose}', bg), (128, 128), threshold=0.42))
        for qy in (0, 64):
            for qx in (0, 64):
                frames.append(img[qy:qy + 64, qx:qx + 64])
    save(np.vstack(frames), 'monk.png')

    light, red, opaque = load('monk_idle', 'black')
    far = []
    for d, fogv in ((2, 0.12), (3, 0.24), (4, 0.36)):
        size = 128 // d
        small = outline(reduce(light, red, opaque, (size, size), threshold=0.42 + fogv))
        c = np.zeros((64, 64), np.uint8)
        c[64 - size:, (64 - size) // 2:(64 - size) // 2 + size] = small
        far.append(c)
    save(np.vstack(far), 'monk_far.png')


def scene(name):
    """A full-screen 3:2 image -> 240x160 indices."""
    light, red, opaque = load(name, 'none')
    return reduce(light, red, opaque, (240, 160), threshold=0.4)


def title():
    out = scene('title')
    ss = 4
    im = Image.new('L', (240 * ss, 160 * ss), 0)
    d = ImageDraw.Draw(im)
    font = ImageFont.truetype(SERIF, 30 * ss)
    text = 'SEPTEM'
    widths = [d.textbbox((0, 0), ch, font=font)[2] for ch in text]
    track = 6 * ss
    x = (240 * ss - sum(widths) - track * (len(text) - 1)) / 2
    for ch, w in zip(text, widths):
        d.text((x, 10 * ss), ch, font=font, fill=255)
        x += w + track
    f2 = ImageFont.truetype(SERIF, 8 * ss)
    msg = 'PRESS START'
    bb = d.textbbox((0, 0), msg, font=f2)
    d.text(((240 * ss - (bb[2] - bb[0])) / 2, 146 * ss), msg, font=f2, fill=255)
    letters = np.asarray(im.resize((240, 160), Image.BOX)) >= 110
    halo = ndimage.binary_dilation(letters, iterations=2) & ~letters
    out[halo] = BLACK
    out[letters] = WHITE
    out[52, 72:168] = RED
    out[53, 80:160] = RED
    c = np.full((256, 256), BLACK, np.uint8)
    c[48:208, 8:248] = out
    save(c, 'title.png')


def death():
    # Off-screen border transparent, so the screen's black is real ink (palette
    # slot 0 is always transparent on the GBA) and covers everything below.
    c = np.zeros((256, 256), np.uint8)
    c[48:208, 8:248] = scene('death')
    save(c, 'death.png')


def write_layout(all_gems, radius, brand):
    path = os.path.join(ROOT, 'include', 'gen', 'septem_layout.h')
    gems = all_gems[0]
    gx = ', '.join(str(int(round(x))) for x, _ in gems)
    gy = ', '.join(str(int(round(y))) for _, y in gems)
    rows_x = ',\n        '.join('{ ' + ', '.join(str(int(round(x))) for x, _ in g) + ' }' for g in all_gems)
    rows_y = ',\n        '.join('{ ' + ', '.join(str(int(round(y))) for _, y in g) + ' }' for g in all_gems)
    with open(path, 'w') as fh:
        fh.write(f'''// Generated by tools/import_art.py from the artwork in assets/raw. Do not edit.
#ifndef SEPTEM_LAYOUT_GEN_H
#define SEPTEM_LAYOUT_GEN_H

namespace septem::gen
{{
    // Screen positions measured from the art: the gauntlet's three gems and
    // the centre of the brand on the right forearm.
    constexpr int gem_x[3] = {{ {gx} }};
    constexpr int gem_y[3] = {{ {gy} }};
    constexpr int left_frames = {len(all_gems)};

    // The gems in every left-hand frame (0 the gauntlet, 1..4 the flask held
    // with 0..3 draughts left, 5 drinking, 6 the last draught gone).
    constexpr int left_gem_x[{len(all_gems)}][3] = {{
        {rows_x}
    }};
    constexpr int left_gem_y[{len(all_gems)}][3] = {{
        {rows_y}
    }};
    constexpr int brand_x = {int(round(brand[0]))};
    constexpr int brand_y = {int(round(brand[1]))};
}}

#endif
''')
    print(f'gems at {gx} / {gy} (r {radius:.1f}), brand at {brand[0]:.0f},{brand[1]:.0f}')


def main():
    needed = LEFT_FRAMES + ['arm_sword', 'strike_1', 'strike_2', 'strike_3', 'strike_4', 'title', 'death'] + \
             [f'block_{i}' for i in range(1, 4)] + [f'parry_{i}' for i in range(1, 4)] + \
             [f'monk_{p}' for p in MONK_POSES]
    missing = [n for n in needed if not have(n)]
    if missing:
        print('import_art: missing assets/raw/' + ', '.join(missing) + '; keeping the engraved placeholders')
        return
    gems, radius = left_hand()
    spent_gem(radius)
    brand = arms()
    monk()
    title()
    death()
    write_layout(gems, radius, brand)
    print('imported artwork from assets/raw')


if __name__ == '__main__':
    main()
