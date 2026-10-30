#!/usr/bin/env python3
"""Pre-renders the first-person view of SEPTEM as engraved, 1-bit panels.

Every wall face the player can see (by depth and lateral offset) is rendered once
here in perspective, shaded by tone and translated into hatching: line pattern
that follows the surface, swelling with darkness, the way a burin cuts. The game
composes the view at run time by drawing these panels far to near.

Outputs:
  include/gen/septem_view.h  tile data (+ masks) for the base view and each panel
  build/preview/*.png        reference renders of sample views (with --preview)

Colour indices (shared by every BG and sprite palette):
  0 transparent, 1 black #000000, 2 white #FFFFFF, 3 blood red #D00024
"""

import argparse
import os
import sys

import numpy as np
from PIL import Image

W, H = 240, 160
CX = 120          # screen centre x
HY = 86           # horizon line (a little low: the vaults tower above)
F = 80.0          # focal length in pixels per unit at z = 1
EYE = 0.5         # eye height above the flooded floor
TOP = 1.0         # wall top above eye level
NEAR = 0.22       # near clip plane
MAX_D = 4         # deepest cell row drawn
MAX_L = 4         # widest lateral offset drawn
FOG_END = 4.6     # beyond this distance everything is black

T, BLACK, WHITE, RED = 0, 1, 2, 3
PALETTE = [(0, 0, 0), (0, 0, 0), (255, 255, 255), (0xD0, 0x00, 0x24)]

# Wall types stored in the map.
WALL, WINDOW = 1, 2

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ---------------------------------------------------------------------------
# Tone -> engraving
# ---------------------------------------------------------------------------

def fog(z):
    """Darkness added by distance: near is lit, far drowns in black."""
    return np.clip((z - 0.6) / (FOG_END - 0.6), 0.0, 1.0) ** 1.15


def hatch(phase, tone, cross_phase=None, along=None):
    """1-bit hatching. `phase` advances by 1 per hatch line; the dark part of
    each line period grows with `tone` (0 = white paper, 1 = solid black).
    In light areas lines break into dashes (`along` runs along the line); above
    ~0.55 a second set of lines (cross hatching) comes in."""
    f = phase - np.floor(phase)
    dark = f < np.clip(0.12 + tone * 1.0, 0.0, 1.0)
    if along is not None:
        line = np.floor(phase)
        jitter = np.sin(line * 91.7) * 0.5 + 0.5
        a = along / 6.0 + jitter
        keep = (a - np.floor(a)) < np.clip(tone / 0.38, 0.0, 1.0)
        dark &= keep | (tone >= 0.38)
    if cross_phase is not None:
        g = cross_phase - np.floor(cross_phase)
        cross = (tone > 0.55) & (g < np.clip((tone - 0.55) * 1.6, 0.0, 1.0))
        dark |= cross
    dark |= tone > 0.9
    return dark


# ---------------------------------------------------------------------------
# Surfaces
# ---------------------------------------------------------------------------

def light(z, v):
    """Doré's staging: a dark foreground frames a lit middle distance that
    sinks into black. Vaults above and the flood below are in shadow."""
    near = np.clip((1.2 - z) / 0.8, 0, 1) * 0.42
    far = fog(z) * 1.05
    top = np.clip((v - 0.3) / 0.7, 0, 1) ** 1.4 * 0.7
    low = np.clip((-0.25 - v) / 0.25, 0, 1) * 0.35
    return near + far + top + low


def block_hash(row, col):
    h = np.sin(row * 12.9898 + col * 78.233) * 43758.5453
    return h - np.floor(h)


def stone_tone(u, v, z, side):
    """Tone and joints for old ashlar masonry at surface coords (u, v)."""
    course = 0.25
    row = np.floor((v + EYE) / course)
    # Blocks of irregular length, staggered per course.
    shift = block_hash(row, 3.0) * 0.5
    blen = 0.42 + block_hash(row, 7.0) * 0.2
    col = np.floor((u + shift) / blen)
    fv = (v + EYE) / course - row          # 0..1 inside a course (bottom->top)
    fu = (u + shift) / blen - col          # 0..1 inside a block

    h = block_hash(row, col)
    base = (-0.06 if not side else 0.04) + (h - 0.5) * 0.18
    # Each block darkens towards its lower edge (shadow under the course above).
    base = base + (0.55 - fv) * 0.16
    tone = np.clip(base + light(z, v), 0, 1)

    px = z / F
    joint_h = (fv * course < px * 1.0)
    joint_v = (fu * blen < px * 1.0)
    highlight = (fv * course > course - px * 1.6) & (fv * course <= course - px * 0.6)
    highlight &= (tone < 0.62)
    return tone, joint_h | joint_v, highlight


def window_mask(u, v, u0):
    """Pointed lancet window in a wall face starting at surface u0."""
    cu = u0 + 0.5
    hw = 0.13
    du = np.abs(u - cu)
    bottom, spring = -0.05, 0.62
    inside_rect = (du < hw) & (v > bottom) & (v < spring)
    # Gothic pointed arch: two circular arcs meeting at the apex.
    r = hw * 2.0
    a1 = (u - (cu + hw - r)) ** 2 + (v - spring) ** 2 < r * r
    a2 = (u - (cu - hw + r)) ** 2 + (v - spring) ** 2 < r * r
    inside_arch = (v >= spring) & a1 & a2 & (du < hw)
    inside = inside_rect | inside_arch
    # Moulding: a band around the opening.
    band = 0.035
    du2 = du - band
    rect2 = (du2 < hw) & (v > bottom - band) & (v < spring)
    r2 = r + band
    b1 = (u - (cu + hw - r)) ** 2 + (v - spring) ** 2 < r2 * r2
    b2 = (u - (cu - hw + r)) ** 2 + (v - spring) ** 2 < r2 * r2
    arch2 = (v >= spring) & b1 & b2 & (du < hw + band)
    frame = (rect2 | arch2) & ~inside
    mullion = inside & (np.abs(u - cu) < 0.012)
    return inside, frame, mullion


def shade_wall(u, v, z, side, kind):
    """Return a colour index image for a wall surface sample."""
    tone, joints, highlight = stone_tone(u, v, z, side)
    # Front faces are cut with horizontal lines, receding faces with vertical
    # ones: the change of direction is what separates planes in an engraving.
    if side:
        phase, cross, along = xs / 3.0, (ys + xs * 0.5) / 3.0, ys
    else:
        phase, cross, along = ys / 3.0, (xs - ys * 0.5) / 3.0, xs
    dark = hatch(phase, tone, cross, along)
    out = np.where(dark, BLACK, WHITE)
    out = np.where(joints & (tone < 0.9), BLACK, out)
    out = np.where(highlight, WHITE, out)
    if kind == WINDOW:
        inside, frame, mullion = window_mask(u, v, np.floor(u))
        # Light pouring through: bare paper, a few thin lines, fading with depth.
        glow_t = np.clip(fog(z) * 1.2 + np.clip(v - 0.6, 0, 1) * 0.3, 0, 1)
        glow = np.where(hatch(ys / 4.0, glow_t * 0.9), BLACK, WHITE)
        fr = np.where(hatch(cross, np.clip(0.6 + fog(z), 0, 1)), BLACK, WHITE)
        out = np.where(frame, fr, out)
        out = np.where(inside, glow, out)
        out = np.where(mullion, BLACK, out)
    return out


def zref_scale(z):
    # Freeze the hatch density per depth band so lines stay continuous across a
    # face but get denser (darker) with distance.
    return np.maximum(np.round(z * 2.0) / 2.0, 0.5)


# ---------------------------------------------------------------------------
# Faces
# ---------------------------------------------------------------------------

ys, xs = np.mgrid[0:H, 0:W].astype(np.float64)
xs += 0.5
ys += 0.5


def render_front(l, d, kind):
    """Face of cell (l, d) towards the viewer: plane z = d - 0.5."""
    z = d - 0.5
    X = (xs - CX) * z / F
    Y = (HY - ys) * z / F
    m = (X >= l - 0.5) & (X < l + 0.5) & (Y >= -EYE) & (Y < TOP)
    if not m.any():
        return None
    u = X - (l - 0.5)
    zz = np.full_like(X, z)
    img = shade_wall(u, Y, zz, False, kind)
    # Crisp edges: black frame on the face's outline.
    edge = m & ~(np.roll(m, 1, 1) & np.roll(m, -1, 1) & np.roll(m, 1, 0) & np.roll(m, -1, 0))
    img = np.where(edge, BLACK, img)
    return np.where(m, img, T)


def render_side(l, d, kind):
    """Side face of cell (l, d) facing the corridor axis."""
    xp = l + 0.5 if l < 0 else l - 0.5
    dx = xs - CX
    with np.errstate(divide='ignore', invalid='ignore'):
        z = xp * F / dx
    z0, z1 = max(d - 0.5, NEAR), d + 0.5
    m = (z >= z0) & (z < z1) & np.isfinite(z)
    Y = (HY - ys) * np.where(m, z, 1.0) / F
    m &= (Y >= -EYE) & (Y < TOP)
    if not m.any():
        return None
    u = (z - (d - 0.5)) if l < 0 else ((d + 0.5) - z)
    u = np.where(m, u, 0.0)
    zz = np.where(m, z, 1.0)
    img = shade_wall(u, Y, zz, True, kind)
    edge = m & ~(np.roll(m, 1, 1) & np.roll(m, -1, 1))
    img = np.where(edge, BLACK, img)
    return np.where(m, img, T)


def render_base():
    """Flooded floor and the black vaults: drawn under every view."""
    img = np.full((H, W), BLACK, np.uint8)
    below = ys > HY
    with np.errstate(divide='ignore'):
        z = np.where(below, EYE * F / (ys - HY), 99.0)
    X = (xs - CX) * z / F
    fz = fog(z)
    near = np.clip((1.0 - z) / 0.6, 0, 1) * 0.35
    tone = np.clip(0.16 + near * 1.2 + fz * 1.2, 0, 1)
    # Black water, cut with fine horizontal lines that thicken into the dark.
    water = np.where(hatch(ys / 2.5, tone, None, xs * 0.6), BLACK, WHITE)
    # Reflected glints: short white dashes rippling on the surface.
    rip = np.sin(X * 7.0 + np.sin(z * 5.0) * 2.0) * np.sin(z * 11.0 + X * 1.7)
    glint = (rip > 0.75) & (fz < 0.55)
    water = np.where(glint & (np.floor(ys) % 2 == 0), WHITE, water)
    img = np.where(below, water, img)
    return img.astype(np.uint8)


# ---------------------------------------------------------------------------
# Panel table
# ---------------------------------------------------------------------------

def panel_list():
    """All (kind, face, l, d) panels in a fixed order."""
    out = []
    for kind in (WALL, WINDOW):
        for d in range(0, MAX_D + 1):
            for l in range(-MAX_L, MAX_L + 1):
                if d >= 1:
                    out.append((kind, 'front', l, d))
                if l != 0:
                    out.append((kind, 'side', l, d))
    return out


def render_panel(kind, face, l, d):
    return render_front(l, d, kind) if face == 'front' else render_side(l, d, kind)


# ---------------------------------------------------------------------------
# Composition (mirrors src/view.cpp, used for previews)
# ---------------------------------------------------------------------------

def compose(grid, px, py, facing, panels, base):
    """grid[y][x] wall codes; facing 0=N(-y) 1=E 2=S 3=W."""
    fx, fy = [(0, -1), (1, 0), (0, 1), (-1, 0)][facing]
    rx, ry = -fy, fx
    img = base.copy()

    def cell(l, d):
        x, y = px + fx * d + rx * l, py + fy * d + ry * l
        if 0 <= y < len(grid) and 0 <= x < len(grid[0]):
            return grid[y][x]
        return WALL

    for d in range(MAX_D, -1, -1):
        for a in range(MAX_L, -1, -1):
            for l in ((-a, a) if a else (0,)):
                k = cell(l, d)
                if not k:
                    continue
                if l != 0:
                    inner = l + 1 if l < 0 else l - 1
                    if not cell(inner, d):
                        p = panels.get((k, 'side', l, d))
                        if p is not None:
                            img = np.where(p != T, p, img)
                if d >= 1 and not cell(l, d - 1):
                    p = panels.get((k, 'front', l, d))
                    if p is not None:
                        img = np.where(p != T, p, img)
    return img


def to_png(idx, path, scale=2):
    im = Image.fromarray(idx.astype(np.uint8), 'P')
    flat = []
    for c in PALETTE:
        flat += list(c)
    im.putpalette(flat + [0] * (768 - len(flat)))
    if scale != 1:
        im = im.resize((im.width * scale, im.height * scale), Image.NEAREST)
    im.save(path)


# ---------------------------------------------------------------------------
# GBA tile export
# ---------------------------------------------------------------------------

def tiles_of(idx):
    """(H, W) index image -> dict tile_no -> (data[8], mask[8]) as 4bpp rows."""
    out = {}
    for ty in range(H // 8):
        for tx in range(W // 8):
            blk = idx[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
            if not (blk != T).any():
                continue
            data, mask = [], []
            for r in range(8):
                dv = mv = 0
                for c in range(8):
                    p = int(blk[r, c])
                    if p != T:
                        dv |= (p & 0xF) << (c * 4)
                        mv |= 0xF << (c * 4)
                data.append(dv)
                mask.append(mv)
            out[ty * (W // 8) + tx] = (data, mask)
    return out


def write_header(path, base, panels):
    keys = panel_list()
    lines = [
        '// Generated by tools/engrave_world.py. Do not edit.',
        '#ifndef SEPTEM_VIEW_GEN_H',
        '#define SEPTEM_VIEW_GEN_H',
        '',
        '#include "bn_common.h"',
        '',
        'namespace septem::gen',
        '{',
        f'    constexpr int max_depth = {MAX_D};',
        f'    constexpr int max_lateral = {MAX_L};',
        '',
        '    struct panel_tile',
        '    {',
        '        uint16_t index;   // screen tile, row-major 30x20',
        '        uint16_t opaque;  // 1 = mask is all ones',
        '        uint32_t data[8];',
        '        uint32_t mask[8];',
        '    };',
        '',
        '    struct panel',
        '    {',
        '        const panel_tile* tiles;',
        '        int count;',
        '    };',
        '',
    ]
    bt = tiles_of(base)
    lines.append('    alignas(4) inline constexpr uint32_t base_view[600 * 8] = {')
    for t in range(600):
        data = bt.get(t, ([0x11111111] * 8, None))[0]
        lines.append('        ' + ', '.join(f'0x{v:08X}' for v in data) + ',')
    lines.append('    };')
    lines.append('')

    names = []
    for key in keys:
        kind, face, l, d = key
        name = f'p_{kind}_{face}_{"m" if l < 0 else ""}{abs(l)}_{d}'
        p = panels.get(key)
        tl = tiles_of(p) if p is not None else {}
        names.append((name, len(tl)))
        if not tl:
            continue
        lines.append(f'    inline constexpr panel_tile {name}[] = {{')
        for t, (data, mask) in sorted(tl.items()):
            opaque = int(all(m == 0xFFFFFFFF for m in mask))
            lines.append(
                f'        {{ {t}, {opaque}, {{ ' + ', '.join(f'0x{v:08X}' for v in data) +
                ' }, { ' + ', '.join(f'0x{v:08X}' for v in mask) + ' } },')
        lines.append('    };')
    lines.append('')
    lines.append('    // Indexed by [kind - 1][face][lateral + max_lateral][depth]; face 0 = front, 1 = side.')
    lines.append(f'    inline constexpr panel panels[2][2][{2 * MAX_L + 1}][{MAX_D + 1}] = {{')
    lookup = dict(zip(keys, names))
    for kind in (WALL, WINDOW):
        lines.append('        {')
        for face in ('front', 'side'):
            lines.append('            {')
            for l in range(-MAX_L, MAX_L + 1):
                row = []
                for d in range(MAX_D + 1):
                    nm = lookup.get((kind, face, l, d))
                    if nm and nm[1]:
                        row.append(f'{{ {nm[0]}, {nm[1]} }}')
                    else:
                        row.append('{ nullptr, 0 }')
                lines.append('                { ' + ', '.join(row) + ' },')
            lines.append('            },')
        lines.append('        },')
    lines.append('    };')
    lines += ['}', '', '#endif', '']
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as fh:
        fh.write('\n'.join(lines))


# ---------------------------------------------------------------------------

SAMPLE = [
    "1111111111111111",
    "1210000200001201",
    "1010110001101001",
    "1000100000100011",
    "1110101010101001",
    "1000001010000021",
    "1011111011111001",
    "1200001010000001",
    "1110101010111101",
    "1000101010100001",
    "1011101010101111",
    "1000001010000001",
    "1110121012111111",
    "1000000010000001",
    "1011111000111101",
    "1111111211111111",
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--preview', action='store_true')
    args = ap.parse_args()

    base = render_base()
    panels = {}
    for key in panel_list():
        p = render_panel(*key)
        if p is not None:
            panels[key] = p.astype(np.uint8)

    write_header(os.path.join(ROOT, 'include', 'gen', 'septem_view.h'), base, panels)
    total = sum(len(tiles_of(p)) for p in panels.values())
    print(f'{len(panels)} panels, {total} panel tiles')

    if args.preview:
        out = os.path.join(ROOT, 'build', 'preview')
        os.makedirs(out, exist_ok=True)
        grid = [[int(c) for c in row] for row in SAMPLE]
        views = [(7, 14, 0, 'nave'), (7, 13, 3, 'aisle'), (7, 7, 0, 'window'),
                 (13, 5, 1, 'chapel'), (1, 13, 0, 'west')]
        for x, y, f, name in views:
            to_png(compose(grid, x, y, f, panels, base), os.path.join(out, f'{name}.png'))
        print('previews in', out)


if __name__ == '__main__':
    sys.exit(main())
