#!/usr/bin/env python3
"""Engraves SEPTEM's sprites and overlay backgrounds as RGBA PNGs in assets/.

Forms are built from flat parts (plates, wraps, flesh). Each part is shaded by
a light from above, then cut into hatching along its own direction, with a
black contour and a white lit edge, like a burin engraving.

  assets/hands.png      256x256 BG: the left gauntlet, drawn large
  assets/arm_N.png      256x256 BG: right arm + sword; 0 rest, 1-4 the strike
  assets/gem.png        16x32   2 frames: lit (red) / spent (hollow)
  assets/brand.png      32x256  16 frames: blank, I .. XV, burned in red
  assets/vignette_N.png 256x256 health levels 1..3, red hatching from the edges
  assets/title.png      256x256 title screen
"""

import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, 'assets')

T, BLACK, WHITE, RED = 0, 1, 2, 3
RGBA = {T: (0, 0, 0, 0), BLACK: (0, 0, 0, 255), WHITE: (255, 255, 255, 255),
        RED: (0xD0, 0x00, 0x24, 255)}
SERIF = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
SERIF_REG = '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'


def save(idx, name):
    h, w = idx.shape
    rgba = np.zeros((h, w, 4), np.uint8)
    for k, c in RGBA.items():
        rgba[idx == k] = c
    os.makedirs(ASSETS, exist_ok=True)
    Image.fromarray(rgba, 'RGBA').save(os.path.join(ASSETS, name))


def poly_mask(w, h, pts, ss=4):
    im = Image.new('L', (w * ss, h * ss), 0)
    ImageDraw.Draw(im).polygon([(x * ss, y * ss) for x, y in pts], fill=255)
    im = im.resize((w, h), Image.BOX)
    return np.asarray(im) >= 128


def ellipse_mask(w, h, box, ss=4):
    im = Image.new('L', (w * ss, h * ss), 0)
    x0, y0, x1, y1 = box
    ImageDraw.Draw(im).ellipse((x0 * ss, y0 * ss, x1 * ss, y1 * ss), fill=255)
    im = im.resize((w, h), Image.BOX)
    return np.asarray(im) >= 128


def engrave_part(canvas, mask, angle, tone, spacing=2.6, light=(0.35, -1.0), rim=True,
                 curve=0.0):
    """Shade one part and cut it into `canvas` (index image) over what is there."""
    h, w = mask.shape
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float64) + 0.5
    dist = ndimage.distance_transform_edt(mask)
    gy, gx = np.gradient(ndimage.gaussian_filter(dist, 1.0))
    n = np.hypot(gx, gy) + 1e-6
    lx, ly = light
    ln = math.hypot(lx, ly)
    # Inward gradient facing away from the light = lit edge.
    facing = -(gx * lx + gy * ly) / (n * ln)
    edge_w = np.exp(-dist / 3.0)
    t = tone - facing * 0.35 * edge_w
    # Rounded forms: the middle of a part turns a little towards the light.
    t = t - np.clip(dist / 6.0, 0, 1) * 0.08
    t = np.clip(t, 0, 1)

    a = math.radians(angle)
    along = xs * math.cos(a) + ys * math.sin(a)
    across = -xs * math.sin(a) + ys * math.cos(a)
    # Lines bow slightly across the form, following its swell.
    across = across + curve * np.sin(np.clip(dist / 5.0, 0, 1) * math.pi / 2) * 1.5
    phase = across / spacing
    f = phase - np.floor(phase)
    dark = f < np.clip(0.15 + t * 0.95, 0, 1)
    light_cut = (t < 0.3)
    dash = (along / 4.0 + np.sin(np.floor(phase) * 7.1)) % 1.0
    dark &= ~light_cut | (dash < t / 0.3)
    g = (along / spacing) % 1.0
    dark |= (t > 0.6) & (g < (t - 0.6) * 1.8)
    dark |= t > 0.9

    out = np.where(dark, BLACK, WHITE)
    if rim:
        inner = dist <= 1.0
        out = np.where(inner, BLACK, out)
        lit_rim = (dist > 1.0) & (dist <= 2.0) & (facing > 0.35)
        out = np.where(lit_rim, WHITE, out)
    canvas[mask] = out[mask]
    return canvas


def scaled(pts, k, ox=0.0, oy=0.0):
    return [(x * k + ox, y * k + oy) for x, y in pts]


def silhouette(c, width=2):
    """Solid black margin round the drawn shapes so they read against the walls."""
    m = c != T
    grown = ndimage.binary_dilation(m, iterations=width)
    c[grown & ~m] = BLACK
    return c


# ---------------------------------------------------------------------------
# Left gauntlet: an armoured hand raised palm-away, three gem sockets on the
# knuckle plate.
# ---------------------------------------------------------------------------

GEM_SOCKETS = [(17, 30), (26, 27), (35, 25)]   # centres, sprite space


K = 1.5           # hands are drawn at this scale on their own BG layer


def gauntlet():
    W, H = 104, 96
    c = np.zeros((H, W), np.uint8)
    # Vambrace leaving the bottom-left corner, then the flared cuff.
    parts = [
        ([(0, 64), (0, 50), (24, 44), (34, 64)], 75, 0.62, 0.0),
        ([(0, 52), (2, 42), (30, 36), (34, 46), (26, 48)], 70, 0.42, 0.6),
    ]
    # Fingers: four armoured lames, each three plates, rising and curling.
    fingers = [
        [(10, 30), (8, 22), (7, 15), (8, 9)],
        [(19, 28), (18, 18), (18, 10), (19, 3)],
        [(28, 25), (28, 16), (29, 8), (31, 2)],
        [(37, 24), (38, 16), (40, 10), (42, 5)],
    ]
    # Thumb from the right side of the hand, angled up and out.
    thumb = [(43, 36), (50, 31), (55, 25), (58, 19)]
    # Back of the hand (knuckle plate).
    plate = [(4, 40), (8, 30), (24, 25), (42, 22), (47, 30), (44, 38), (26, 42)]

    parts = [(scaled(p, K, 0, 0), a, t, cv) for p, a, t, cv in parts]
    fingers = [scaled(f, K) for f in fingers]
    thumb = scaled(thumb, K)
    plate = scaled(plate, K)
    for pts, ang, tone, curve in parts:
        engrave_part(c, poly_mask(W, H, pts), ang, tone, curve=curve)
    for fi, joints in enumerate(fingers + [thumb]):
        width = (3.6 if fi < 4 else 4.0) * K
        for j in range(len(joints) - 1):
            (x0, y0), (x1, y1) = joints[j], joints[j + 1]
            dx, dy = x1 - x0, y1 - y0
            ln = math.hypot(dx, dy)
            nx, ny = -dy / ln * width, dx / ln * width
            # Each lame overlaps the next a little, like riveted plates.
            ex, ey = dx / ln * 1.2 * K, dy / ln * 1.2 * K
            pts = [(x0 + nx - ex, y0 + ny - ey), (x1 + nx * 0.9, y1 + ny * 0.9),
                   (x1 - nx * 0.9, y1 - ny * 0.9), (x0 - nx - ex, y0 - ny - ey)]
            tone = 0.48 + j * 0.06 + (0.1 if fi == 4 else 0)
            ang = math.degrees(math.atan2(dy, dx)) + 90
            engrave_part(c, poly_mask(W, H, pts), ang, tone, spacing=2.4)
        # Fingertip, a small pointed cap.
        (x0, y0), (x1, y1) = joints[-2], joints[-1]
        dx, dy = x1 - x0, y1 - y0
        ln = math.hypot(dx, dy)
        tip = (x1 + dx / ln * 3.0 * K, y1 + dy / ln * 3.0 * K)
        nx, ny = -dy / ln * width * 0.8, dx / ln * width * 0.8
        engrave_part(c, poly_mask(W, H, [(x1 + nx, y1 + ny), tip, (x1 - nx, y1 - ny)]),
                     0, 0.35, spacing=2.4)
    engrave_part(c, poly_mask(W, H, plate), 20, 0.36, curve=1.0)
    # Gem settings: dark bezels; the gems themselves are a separate sprite.
    for gx, gy in GEM_SOCKETS:
        gx, gy = gx * K, gy * K
        m = ellipse_mask(W, H, (gx - 5.5, gy - 5.0, gx + 5.5, gy + 5.0))
        c[m] = BLACK
    return silhouette(c)


def gem():
    W, H = 16, 16
    frames = []
    for lit in (True, False):
        c = np.zeros((H, W), np.uint8)
        outer = ellipse_mask(W, H, (4, 4.5, 12, 11.5))
        inner = ellipse_mask(W, H, (5.2, 5.6, 10.8, 10.4))
        if lit:
            c[outer] = BLACK
            c[inner] = RED
            # Facet lines and a white glint, upper left.
            c[8, 6:10] = np.where(c[8, 6:10] == RED, BLACK, c[8, 6:10])
            c[6, 6] = WHITE
            c[6, 7] = WHITE
            c[7, 6] = WHITE
        else:
            c[outer] = BLACK
            ring = outer & ~ellipse_mask(W, H, (4.9, 5.4, 11.1, 10.6))
            c[ring & (np.mgrid[0:H, 0:W][0] < 8)] = WHITE
        frames.append(c)
    save(np.vstack(frames), 'gem.png')


# ---------------------------------------------------------------------------
# Right forearm: the inner side, bare and pale, wrapped at the wrist, a fist
# closed on the hilt. The brand is burned on the flat of the forearm.
# ---------------------------------------------------------------------------

BRAND_POS = (22, 30)   # top-left of the 32x16 brand, sprite space


def forearm():
    W, H = 104, 96
    c = np.zeros((H, W), np.uint8)
    # Ragged sleeve at the bottom-right corner.
    sleeve = [(36, 64), (40, 54), (46, 56), (50, 48), (56, 52), (60, 46), (64, 47), (64, 64)]
    # Bare forearm rising to the upper left, inner side towards us.
    arm = [(40, 60), (16, 26), (14, 20), (26, 14), (32, 18), (60, 50)]
    # Linen wraps at the wrist.
    wraps = [
        [(13, 23), (25, 15), (28, 19), (16, 27)],
        [(16, 27), (28, 19), (30, 23), (19, 31)],
    ]
    # Fist (seen from the palm side), knuckles up, closed on the sword's grip.
    fist = [(6, 16), (8, 6), (18, 1), (26, 4), (28, 13), (22, 18), (12, 21)]
    sleeve, arm, fist = (scaled(p, K) for p in (sleeve, arm, fist))
    wraps = [scaled(w, K) for w in wraps]
    engrave_part(c, poly_mask(W, H, arm), -40, 0.24, curve=1.0)
    for w in wraps:
        engrave_part(c, poly_mask(W, H, w), 55, 0.42, spacing=2.2)
    engrave_part(c, poly_mask(W, H, fist), -30, 0.38, curve=1.0)
    # Finger creases across the fist.
    for k in range(3):
        y = int((7 + k * 4) * K)
        for x in range(int((10 + k) * K), int((25 - k) * K)):
            if c[y, x] != T and (x + k) % 5 != 0:
                c[y, x] = BLACK
    engrave_part(c, poly_mask(W, H, sleeve), 100, 0.66, curve=0.5)
    # Quiet, pale skin where the numerals are burned.
    bx, by = BRAND_POS
    bx, by = int(bx * K), int(by * K)
    zone = np.zeros_like(c, bool)
    zone[by + 2:by + 14, bx + 2:bx + 30] = True
    zone &= poly_mask(W, H, arm)
    ys_, xs_ = np.mgrid[0:H, 0:W]
    c[zone] = np.where((ys_[zone] + xs_[zone]) % 4 == 0, BLACK, WHITE)
    return silhouette(c)


# Hands layer: where each hand sits on screen (top-left, screen space).
GAUNTLET_AT = (-6, 160 - 92)
FOREARM_AT = (240 - 100, 160 - 92)


# The sword: raised in the right fist, the blade rising along the right side of
# the view so the corridor stays clear. Screen space.
SWORD_BASE = (169, 66)    # centre of the crossguard
SWORD_TIP = (209, -4)     # off the top edge: the blade runs out of frame


def sword(c, base=SWORD_BASE, tip=SWORD_TIP):
    """Cut a longsword into a 256x256 BG canvas (screen + (8, 48))."""
    S = c.shape[0]
    bx, by = base
    tx, ty = tip
    dx, dy = tx - bx, ty - by
    ln = math.hypot(dx, dy)
    ux, uy = dx / ln, dy / ln          # along the blade
    nx, ny = -uy, ux                   # across the blade
    o = lambda x, y: (x + 8, y + 48)   # screen -> canvas

    # Blade: broad at the ricasso, tapering to the point.
    w0, w1 = 6.5, 2.2
    base = (bx + ux * 2, by + uy * 2)
    blade = [o(base[0] + nx * w0, base[1] + ny * w0), o(tx + nx * w1, ty + ny * w1),
             o(tx + ux * 4, ty + uy * 4), o(tx - nx * w1, ty - ny * w1),
             o(base[0] - nx * w0, base[1] - ny * w0)]
    m = poly_mask(S, S, blade)
    ys, xs = np.mgrid[0:S, 0:S].astype(np.float64)
    across = (xs - (bx + 8)) * nx + (ys - (by + 48)) * ny
    along = (xs - (bx + 8)) * ux + (ys - (by + 48)) * uy
    half = w0 + (w1 - w0) * np.clip(along / ln, 0, 1)
    rel = across / np.maximum(half, 0.5)          # -1 .. 1 across the blade
    # Steel: the edge towards the light is bare paper, the far bevel is cut
    # with fine lines along the blade, and the fuller is a black groove.
    tone = np.where(rel < 0, 0.05, 0.75) + np.clip(along / ln, 0, 1) * 0.12
    phase = along / 2.0
    dark = ((phase - np.floor(phase)) < tone) & (rel >= 0)
    dash = ((along / 5.0) % 1.0) < 0.35
    dark |= (rel < 0) & (rel > -0.75) & dash & (((across / 2.0) % 1.0) < 0.5)
    fuller = (np.abs(rel + 0.05) < 0.14) & (along > 3) & (along < ln * 0.75)
    out = np.where(dark | fuller, BLACK, WHITE)
    edge = m & ~ndimage.binary_erosion(m)
    out = np.where(edge, BLACK, out)
    c[m] = out[m]

    # Crossguard: a straight gothic bar with drooping quillon ends.
    g = 19.0
    guard = [o(bx + nx * g + ux * 2.6, by + ny * g + uy * 2.6),
             o(bx - nx * g + ux * 2.6, by - ny * g + uy * 2.6),
             o(bx - nx * (g + 2) - ux * 3, by - ny * (g + 2) - uy * 3),
             o(bx - nx * (g - 2) - ux * 2.2, by - ny * (g - 2) - uy * 2.2),
             o(bx + nx * (g - 2) - ux * 2.2, by + ny * (g - 2) - uy * 2.2),
             o(bx + nx * (g + 2) - ux * 3, by + ny * (g + 2) - uy * 3)]
    engrave_part(c, poly_mask(S, S, guard), math.degrees(math.atan2(ny, nx)), 0.5, spacing=2.0)
    # Grip below the guard, into the fist (the fist is drawn over it).
    grip = [o(bx + nx * 2.6, by + ny * 2.6), o(bx - nx * 2.6, by - ny * 2.6),
            o(bx - nx * 2.6 - ux * 16, by - ny * 2.6 - uy * 16),
            o(bx + nx * 2.6 - ux * 16, by + ny * 2.6 - uy * 16)]
    engrave_part(c, poly_mask(S, S, grip), math.degrees(math.atan2(uy, ux)) + 90, 0.72, spacing=2.0)
    return c


def paste(c, img, at):
    h, w = img.shape
    X, Y = at[0] + 8, at[1] + 48
    sx0, sy0 = max(0, -X), max(0, -Y)
    dst = c[Y + sy0:Y + h, X + sx0:X + w]
    src = img[sy0:sy0 + dst.shape[0], sx0:sx0 + dst.shape[1]]
    dst[src != T] = src[src != T]


def outline(c, width=2):
    m = c != T
    c[ndimage.binary_dilation(m, iterations=width) & ~m] = BLACK


def hands():
    """hands.png: the left gauntlet. arm_0.png: the right arm at rest."""
    S = 256
    c = np.zeros((S, S), np.uint8)
    paste(c, gauntlet(), GAUNTLET_AT)
    save(c, 'hands.png')

    c = np.zeros((S, S), np.uint8)
    sword(c)
    outline(c)
    paste(c, forearm(), FOREARM_AT)
    save(c, 'arm_0.png')
    # Screen positions of the gem centres and the brand, for the game code.
    gems = [(GAUNTLET_AT[0] + gx * K, GAUNTLET_AT[1] + gy * K) for gx, gy in GEM_SOCKETS]
    brand_at = (FOREARM_AT[0] + BRAND_POS[0] * K, FOREARM_AT[1] + BRAND_POS[1] * K)
    return gems, brand_at


# ---------------------------------------------------------------------------
# Strike: the right arm swings the sword from high right, across the view, to
# low left. Each pose: wrist, blade direction, blade length, and the arc of
# the swing (start and end blade angles) cut as engraved speed lines.
# ---------------------------------------------------------------------------

ELBOW = (262, 182)
STRIKE_POSES = [
    # wind-up: raised high on the right, blade cocked back over the shoulder
    dict(wrist=(204, 62), dir=(0.42, -1.0), length=96, sweep=None),
    # the cut: blade flat across the view
    dict(wrist=(132, 100), dir=(-1.0, -0.22), length=104, sweep=(-100, -168)),
    # follow-through: low left, blade running out of the bottom corner
    dict(wrist=(74, 136), dir=(-0.78, 0.62), length=96, sweep=(-168, -218)),
    # recovery: coming back up towards guard
    dict(wrist=(160, 112), dir=(-0.18, -1.0), length=84, sweep=None),
]


def speed_lines(c, wrist, a0, a1, r0, r1):
    """A fan of engraved arcs between blade angles a0..a1 (degrees)."""
    S = c.shape[0]
    ys, xs = np.mgrid[0:S, 0:S].astype(np.float64)
    dx, dy = xs - (wrist[0] + 8), ys - (wrist[1] + 48)
    r = np.hypot(dx, dy)
    ang = np.degrees(np.arctan2(dy, dx))
    lo, hi = min(a0, a1), max(a0, a1)
    # Unwrap angles into the sweep's range.
    ang = np.where(ang > hi, ang - 360, ang)
    ang = np.where(ang < lo, ang + 360, ang)
    inside = (ang >= lo) & (ang <= hi) & (r >= r0) & (r <= r1)
    # Lines thin out away from the blade's end of the sweep.
    t = (ang - a0) / (a1 - a0)            # 0 at the start, 1 at the blade
    ring = (r / 4.0) % 1.0
    dark = ring < 0.22 + 0.3 * np.clip(t, 0, 1)
    # Broken towards the tail, as a burin lifting off the plate.
    broken = ((ang * 0.9 + r * 0.3) % 6.0) < (6.0 * np.clip(t * 1.4, 0, 1))
    c[inside & dark & broken] = BLACK
    c[inside & ~dark & broken & (c == T)] = WHITE


def arm_pose(wrist, d, length, sweep):
    S = 256
    c = np.zeros((S, S), np.uint8)
    o = lambda x, y: (x + 8, y + 48)
    ln = math.hypot(*d)
    ux, uy = d[0] / ln, d[1] / ln
    if sweep:
        speed_lines(c, wrist, sweep[0], sweep[1], 24, length + 6)
    guard = (wrist[0] + ux * 12, wrist[1] + uy * 12)
    tip = (guard[0] + ux * length, guard[1] + uy * length)
    sword(c, guard, tip)
    outline(c)
    # Forearm from the elbow (off screen, bottom right) to the wrist.
    ex, ey = ELBOW
    ax, ay = wrist[0] - ex, wrist[1] - ey
    al = math.hypot(ax, ay)
    nx, ny = -ay / al, ax / al
    w0, w1 = 22, 12
    arm = [o(ex + nx * w0, ey + ny * w0), o(wrist[0] + nx * w1, wrist[1] + ny * w1),
           o(wrist[0] - nx * w1, wrist[1] - ny * w1), o(ex - nx * w0, ey - ny * w0)]
    part = np.zeros_like(c)
    engrave_part(part, poly_mask(S, S, arm), math.degrees(math.atan2(ay, ax)), 0.3, curve=1.0)
    # Linen wraps just behind the wrist.
    for k in range(2):
        f0, f1 = 0.08 + k * 0.09, 0.15 + k * 0.09
        p0 = (wrist[0] - ax * f0, wrist[1] - ay * f0)
        p1 = (wrist[0] - ax * f1, wrist[1] - ay * f1)
        ww = w1 + 2 + k * 2
        wrap = [o(p0[0] + nx * ww, p0[1] + ny * ww), o(p1[0] + nx * ww, p1[1] + ny * ww),
                o(p1[0] - nx * ww, p1[1] - ny * ww), o(p0[0] - nx * ww, p0[1] - ny * ww)]
        engrave_part(part, poly_mask(S, S, wrap), math.degrees(math.atan2(ay, ax)) + 60, 0.45, spacing=2.2)
    # Ragged sleeve where the arm leaves the frame.
    sl = (ex - ax * 0.18, ey - ay * 0.18)
    sleeve = [o(ex + nx * 30, ey + ny * 30), o(sl[0] + nx * 26, sl[1] + ny * 26),
              o(sl[0] + ax * 0.05, sl[1] + ay * 0.05), o(sl[0] - nx * 26, sl[1] - ny * 26),
              o(ex - nx * 30, ey - ny * 30)]
    engrave_part(part, poly_mask(S, S, sleeve), 100, 0.66, curve=0.5)
    # The fist, closed over the grip.
    fist = ellipse_mask(S, S, (wrist[0] + 8 - 13, wrist[1] + 48 - 11, wrist[0] + 8 + 13, wrist[1] + 48 + 11))
    engrave_part(part, fist, math.degrees(math.atan2(uy, ux)), 0.4, curve=1.0)
    outline(part)
    c[part != T] = part[part != T]
    return c


def strike():
    for i, pose in enumerate(STRIKE_POSES, start=1):
        save(arm_pose(pose['wrist'], pose['dir'], pose['length'], pose['sweep']), f'arm_{i}.png')



ROMAN = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X',
         'XI', 'XII', 'XIII', 'XIV', 'XV']


def brand():
    W, H = 32, 16
    font = ImageFont.truetype(SERIF, 11)
    frames = []
    for s in ROMAN:
        c = np.zeros((H, W), np.uint8)
        if s:
            im = Image.new('L', (W * 4, H * 4), 0)
            d = ImageDraw.Draw(im)
            f4 = ImageFont.truetype(SERIF, 60 if len(s) < 3 else 50 if len(s) < 4 else 40)
            bb = d.textbbox((0, 0), s, font=f4)
            tw, th = bb[2] - bb[0], bb[3] - bb[1]
            d.text(((W * 4 - tw) / 2 - bb[0], (H * 4 - th) / 2 - bb[1]), s, font=f4, fill=255)
            # Burned skin: slight slant, as if seared on by hand.
            im = im.transform(im.size, Image.AFFINE, (1, 0.18, -6, 0, 1, 0), Image.BILINEAR)
            m = np.asarray(im.resize((W, H), Image.BOX)) >= 110
            # A black scorched edge round each red stroke.
            halo = ndimage.binary_dilation(m) & ~m
            c[halo] = BLACK
            c[m] = RED
        frames.append(c)
    save(np.vstack(frames), 'brand.png')
    del font


# ---------------------------------------------------------------------------
# Health vignette: red hatching cut inward from the screen edges.
# ---------------------------------------------------------------------------

def vignette(level):
    S = 256
    c = np.zeros((S, S), np.uint8)
    ys, xs = np.mgrid[0:S, 0:S].astype(np.float64) + 0.5
    # Visible screen inside the 256x256 map when the bg is centred.
    sx, sy = xs - 8, ys - 48
    inside = (sx >= 0) & (sx < 240) & (sy >= 0) & (sy < 160)
    # Distance to the nearest screen edge, normalised (0 edge, 1 centre).
    e = np.minimum(np.minimum(sx, 240 - sx) / 120.0, np.minimum(sy, 160 - sy) / 80.0)
    ang = np.arctan2(sy - 80, (sx - 120) * 0.67)
    # Uneven reach: strokes of different lengths, like spreading blood.
    n = (np.sin(ang * 23.0) * 0.5 + np.sin(ang * 9.0 + 1.3) * 0.35 + np.sin(ang * 51.0) * 0.15)
    reach = [0.0, 0.10, 0.19, 0.32][level] * (1.0 + n * 0.4)
    stroke_phase = ang * 140.0 / math.pi
    f = stroke_phase - np.floor(stroke_phase)
    # Strokes thicken towards the edge and taper to a point inward.
    width = np.clip(1.0 - e / np.maximum(reach, 1e-3), 0, 1)
    red = (e < reach) & (f < 0.15 + width * 0.6)
    # Solid crust right at the edge for the deeper wounds.
    red |= e < reach * (0.10 + level * 0.05)
    if level == 3:
        # Last stand: a second set of strokes crossing the first.
        g = (ang * 90.0 / math.pi + e * 6.0) % 1.0
        red |= (e < reach * 0.8) & (g < 0.2 * width + 0.05)
    c[red & inside] = RED
    # Black edging on the stroke tips keeps the red engraved, not glowing.
    save(c, f'vignette_{level}.png')


# ---------------------------------------------------------------------------
# Title: SEPTEM cut in white on black, a single red stroke beneath.
# ---------------------------------------------------------------------------

def title():
    S = 256
    c = np.full((S, S), BLACK, np.uint8)
    ox, oy = 8, 48
    ss = 4
    im = Image.new('L', (240 * ss, 160 * ss), 0)
    d = ImageDraw.Draw(im)
    font = ImageFont.truetype(SERIF, 34 * ss)
    text = 'SEPTEM'
    # Wide letter spacing, as on a carved lintel.
    widths = [d.textbbox((0, 0), ch, font=font)[2] for ch in text]
    track = 7 * ss
    total = sum(widths) + track * (len(text) - 1)
    x = (240 * ss - total) / 2
    for ch, w in zip(text, widths):
        d.text((x, 44 * ss), ch, font=font, fill=255)
        x += w + track
    letters = np.asarray(im.resize((240, 160), Image.BOX)) >= 128
    ys, xs = np.mgrid[0:160, 0:240]
    # Letters are cut: white with horizontal hatching growing towards the base.
    dist = ndimage.distance_transform_edt(letters)
    rel = np.clip((ys - 50) / 34.0, 0, 1)
    hatch_dark = ((ys % 3) == 0) & (rel > 0.45) & (dist > 1.2)
    sub = letters.copy()
    out = np.full((160, 240), BLACK, np.uint8)
    out[sub] = WHITE
    out[hatch_dark & sub] = BLACK
    # Blood-red rule under the name.
    out[96, 72:168] = RED
    out[97, 80:160] = RED
    # Subtitle.
    im2 = Image.new('L', (240 * ss, 160 * ss), 0)
    d2 = ImageDraw.Draw(im2)
    f2 = ImageFont.truetype(SERIF, 9 * ss)
    msg = 'PRESS START'
    bb = d2.textbbox((0, 0), msg, font=f2)
    d2.text(((240 * ss - (bb[2] - bb[0])) / 2, 128 * ss), msg, font=f2, fill=255)
    sub2 = np.asarray(im2.resize((240, 160), Image.BOX)) >= 90
    out[sub2] = WHITE
    c[oy:oy + 160, ox:ox + 240] = out
    save(c, 'title.png')


def main():
    gems, brand_at = hands()
    strike()
    gem()
    brand()
    for lv in (1, 2, 3):
        vignette(lv)
    title()
    print('sprites and overlays written to', ASSETS)
    print('gem centres:', [(round(x), round(y)) for x, y in gems])
    print('brand top-left:', (round(brand_at[0]), round(brand_at[1])))


if __name__ == '__main__':
    main()
