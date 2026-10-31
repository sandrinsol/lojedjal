#!/usr/bin/env python3
"""Engraves the Somnolent Monk: duel poses and distance views.

  assets/monk.png      64x1280: 5 poses x 4 quadrants (TL, TR, BL, BR) of a
                       128x128 figure: idle, wind-up, strike, stagger, death
  assets/monk_far.png  64x192: the idle monk 2, 3 and 4 cells away, darkened
                       by distance (bottom-aligned on the water line)

The monk is built from parts (cowl, robe, sleeves, hands, chain, censer) at a
scale, so the far views are drawn at their size rather than shrunk.
"""

import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engrave_sprites import (BLACK, RED, T, WHITE, ellipse_mask, engrave_part,  # noqa: E402
                             poly_mask, save)
from scipy import ndimage  # noqa: E402

POSES = ['idle', 'windup', 'strike', 'stagger', 'death']


def monk(pose, size=128, s=1.0, fog=0.0):
    """Draw the monk in `pose` on a size x size canvas at scale `s` (1 = 128 px
    tall), feet on the bottom edge, centred."""
    c = np.zeros((size, size), np.uint8)
    ox = size / 2 - 64 * s
    oy = size - 128 * s

    def P(pts):
        return [(ox + x * s, oy + y * s) for x, y in pts]

    def E(box):
        x0, y0, x1, y1 = box
        return (ox + x0 * s, oy + y0 * s, ox + x1 * s, oy + y1 * s)

    def part(pts, angle, tone, **kw):
        engrave_part(c, poly_mask(size, size, P(pts)), angle, min(1.0, tone + fog),
                     spacing=max(1.9, 2.6 * min(1.0, s * 1.4)), **kw)

    def blob(box, angle, tone, **kw):
        engrave_part(c, ellipse_mask(size, size, E(box)), angle, min(1.0, tone + fog),
                     spacing=max(1.9, 2.6 * min(1.0, s * 1.4)), **kw)

    # Pose parameters: hood offset, body drop, arm/hand/censer placement.
    hx, hy, drop = 0, 0, 0
    if pose == 'windup':
        hx, hy = 6, 4
    elif pose == 'strike':
        hy = 12
    elif pose == 'stagger':
        hx, hy = 14, 2
    elif pose == 'death':
        hy, drop = 46, 40

    # Robe: a heavy hunched bell, hem lost in the water.
    if pose == 'death':
        robe = [(26, 76 + 0), (46, 66), (82, 66), (102, 76), (122, 128), (6, 128)]
    elif pose == 'stagger':
        robe = [(36, 46), (52, 36), (90, 38), (104, 50), (112, 128), (24, 128)]
    else:
        robe = [(30, 46 + hy // 2), (44, 34 + hy), (84, 34 + hy), (98, 46 + hy // 2), (108, 128), (20, 128)]
    part(robe, 92, 0.84, curve=1.0)
    # Deep folds falling from the shoulders.
    for fx0, fx1 in ((50, 40), (64, 64), (78, 90)):
        top = 52 + drop
        part([(fx0 - 1.5, top), (fx0 + 1.5, top), (fx1 + 3, 128), (fx1 - 3, 128)], 90, 0.92, rim=False)

    # Cowl and the dark of the face.
    hood = (42 + hx, 4 + hy, 86 + hx, 48 + hy)
    blob(hood, 65, 0.72, curve=1.0)
    face = (53 + hx, 16 + hy, 75 + hx, 44 + hy)
    fm = ellipse_mask(size, size, E(face))
    c[fm] = BLACK
    # A slack, pale jaw and closed eyes in the shadow of the cowl.
    if fog < 0.5:
        jaw = (57 + hx, 32 + hy, 71 + hx, 43 + hy)
        jm = ellipse_mask(size, size, E(jaw)) & fm
        ys, xs = np.mgrid[0:size, 0:size]
        c[jm & ((ys % 2) == 0)] = WHITE
        for ex in (60, 68):
            x0 = int(ox + (ex - 3 + hx) * s)
            x1 = int(ox + (ex + 1 + hx) * s)
            y = int(oy + (27 + hy) * s)
            if 0 <= y < size:
                c[y, max(0, x0):max(0, x1)] = WHITE

    # Arms, hands and the censer, by pose.
    def sleeve(a, b, w):
        (x0, y0), (x1, y1) = a, b
        dx, dy = x1 - x0, y1 - y0
        ln = math.hypot(dx, dy)
        nx, ny = -dy / ln * w, dx / ln * w
        part([(x0 + nx, y0 + ny), (x1 + nx * 0.8, y1 + ny * 0.8), (x1 - nx * 0.8, y1 - ny * 0.8),
              (x0 - nx, y0 - ny)], math.degrees(math.atan2(dy, dx)) + 90, 0.68)

    def chain(a, b):
        (x0, y0), (x1, y1) = a, b
        n = int(math.hypot(x1 - x0, y1 - y0) / 3)
        for i in range(n + 1):
            t = i / max(n, 1)
            x = ox + (x0 + (x1 - x0) * t) * s
            y = oy + (y0 + (y1 - y0) * t) * s
            r = 1.3 * s
            m = ellipse_mask(size, size, (x - r, y - r, x + r, y + r))
            c[m] = BLACK if i % 2 else WHITE

    def censer(cx, cy, r):
        blob((cx - r, cy - r, cx + r, cy + r), 30, 0.45, curve=1.0)
        # Pierced holes where the coals glow white.
        for k in range(6):
            a = k * math.pi / 3 + 0.3
            px, py = cx + math.cos(a) * r * 0.55, cy + math.sin(a) * r * 0.55
            hr = max(0.9, r * 0.12)
            m = ellipse_mask(size, size, E((px - hr, py - hr, px + hr, py + hr)))
            c[m] = WHITE
        # Cap and ring.
        part([(cx - r * 0.5, cy - r * 0.9), (cx + r * 0.5, cy - r * 0.9), (cx + r * 0.25, cy - r * 1.3),
              (cx - r * 0.25, cy - r * 1.3)], 0, 0.75)

    def hands(cx, cy, w=9, h=7):
        blob((cx - w, cy - h, cx + w, cy + h), 20, 0.22, curve=1.0)

    if pose == 'idle':
        sleeve((38, 50), (58, 88), 7)
        sleeve((90, 50), (70, 88), 7)
        hands(64, 92)
        chain((64, 98), (64, 106))
        censer(64, 114, 9)
    elif pose == 'windup':
        sleeve((40, 50), (58, 10), 7)
        sleeve((92, 50), (74, 10), 7)
        hands(66, 6)
        chain((66, 0), (52, -4))
        censer(46, 4, 10)
    elif pose == 'strike':
        sleeve((38, 56), (56, 64), 8)
        sleeve((90, 56), (72, 64), 8)
        hands(64, 64)
        chain((64, 70), (64, 80))
        # Motion lines above the falling censer.
        for k in range(4):
            y = 66 + k * 4
            part([(40 + k * 3, y), (88 - k * 3, y), (88 - k * 3, y + 1.4), (40 + k * 3, y + 1.4)], 0, 0.95,
                 rim=False)
        censer(64, 100, 22)
    elif pose == 'stagger':
        sleeve((40, 52), (10, 66), 7)
        hands(8, 68, 7, 6)
        sleeve((100, 52), (104, 80), 7)
        hands(104, 84)
        chain((104, 90), (112, 96))
        censer(116, 102, 9)
    elif pose == 'death':
        sleeve((34, 80), (22, 110), 8)
        sleeve((94, 80), (106, 110), 8)
        hands(20, 114)
        hands(108, 114)
        censer(88, 122, 8)

    # The flood: water lines cut across the hem, with white glints.
    wl = int(oy + 116 * s)
    ys, xs = np.mgrid[0:size, 0:size]
    water = (ys >= wl) & (c != T)
    c[water & (ys % 2 == 1)] = BLACK
    c[water & (ys % 2 == 0) & ((xs + ys * 3) % 7 < 2)] = WHITE

    if pose == 'death':
        # Blood spilling from under the cowl onto the water: the only colour.
        pool = ellipse_mask(size, size, E((40, 108, 92, 124)))
        c[pool & (c != T) & (ys % 2 == 0)] = RED
        c[pool & (ys % 2 == 0) & (c == T)] = RED
        trail = poly_mask(size, size, P([(60 + hx, 46 + hy), (68 + hx, 46 + hy), (70, 110), (58, 110)]))
        c[trail & (c != T)] = RED

    # Solid black margin so the figure reads against the walls.
    m = c != T
    c[ndimage.binary_dilation(m, iterations=max(1, int(round(2 * s)))) & ~m] = BLACK
    return c


def main():
    frames = []
    for pose in POSES:
        img = monk(pose)
        for qy in (0, 64):
            for qx in (0, 64):
                frames.append(img[qy:qy + 64, qx:qx + 64])
    save(np.vstack(frames), 'monk.png')

    far = []
    for d, fogv in ((2, 0.12), (3, 0.28), (4, 0.42)):
        far.append(monk('idle', size=64, s=1.0 / d, fog=fogv))
    save(np.vstack(far), 'monk_far.png')

    # Preview sheet.
    from PIL import Image
    prev = np.zeros((128, 128 * len(POSES)), np.uint8)
    for i, pose in enumerate(POSES):
        prev[:, i * 128:(i + 1) * 128] = monk(pose)
    rgb = np.zeros(prev.shape + (3,), np.uint8)
    rgb[:] = (70, 70, 70)
    rgb[prev == BLACK] = (0, 0, 0)
    rgb[prev == WHITE] = (255, 255, 255)
    rgb[prev == RED] = (0xD0, 0, 0x24)
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'build', 'preview')
    os.makedirs(out, exist_ok=True)
    Image.fromarray(rgb).resize((prev.shape[1] * 2, 256), Image.NEAREST).save(os.path.join(out, 'monk.png'))
    print('monk poses and distance views written')


if __name__ == '__main__':
    main()
